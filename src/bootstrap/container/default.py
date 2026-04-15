from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from access.api.app_api import AgentAppAPI
from access.api.runtime_api import RuntimeAPI
from access.api.workflow_api import WorkflowAPI
from adapters.approval.hermes_policy import HermesApprovalPolicyAdapter
from adapters.capability_registry.hermes_registry import HermesCapabilityRegistryAdapter
from adapters.capability_registry.model_registry import InMemoryModelRegistry
from adapters.capability_registry.registry import InMemoryCapabilityRegistry
from adapters.delegation.hermes_transport import HermesDelegationTransportAdapter
from adapters.hermes.bridge import HermesBridgeConfig
from adapters.model_providers.anthropic_provider import AnthropicProvider
from adapters.model_providers.mock_provider import MockLLMProvider
from adapters.model_providers.openai_provider import OpenAIProvider
from application.app_compilation.service import AgentAppService
from application.execution.service import ExecutionService
from application.workflow_resolution.service import WorkflowService
from bootstrap.settings import Settings
from domain.agent_app.service import DefaultAgentAppDomainService
from domain.agent_app.policies import ModelPolicy
from domain.capability.models import CapabilityDescriptor, CapabilityResult
from domain.memory.policy import MemoryPromotionPolicy
from domain.memory.service import DefaultMemoryDomainService
from domain.memory.models import MemoryKind, MemoryScope
from domain.session.models import AgentSession
from domain.session.service import DefaultSessionDomainService
from domain.workflow.service import DefaultWorkflowDomainService
from domain.workflow.steps import WorkflowStep
from runtime.agent_kernel import AgentKernel
from runtime.approval.gate import ApprovalGate
from runtime.approval.sandbox import SandboxGate
from runtime.capability.executor import ExecutionEngine
from runtime.context.engine import ContextEngine
from runtime.delegation.coordinator import DelegationCoordinator
from runtime.llm.runtime import LLMRuntime
from runtime.memory.summarizer import LLMMemorySummarizer
from runtime.ports import (
    ApprovalPolicyPort,
    CapabilityRegistryPort,
    DelegationTransportPort,
    SandboxPolicyPort,
)
from runtime.response.normalizer import ResponseNormalizer
from storage.artifact.store import InMemoryArtifactStore
from storage.evidence.store import InMemoryEvidenceStore, JsonlEvidenceStore
from storage.memory.store import InMemoryMemoryStore, JsonlMemoryStore
from storage.memory_dataset.store import InMemoryMemoryDatasetStore, JsonlMemoryDatasetStore
from storage.session.store import InMemorySessionStore


@dataclass(slots=True)
class PlatformContainer:
    """Fully wired default container for the v2 scaffold runtime."""

    settings: Settings
    app_api: AgentAppAPI
    workflow_api: WorkflowAPI
    runtime_api: RuntimeAPI
    capability_registry: CapabilityRegistryPort
    approval_policy: ApprovalPolicyPort
    sandbox_policy: SandboxPolicyPort
    delegation_transport: DelegationTransportPort
    model_registry: InMemoryModelRegistry
    session_store: InMemorySessionStore
    artifact_store: InMemoryArtifactStore
    memory_store: Any
    evidence_store: Any
    memory_dataset_store: Any


@dataclass(slots=True, frozen=True)
class _SystemSessionClock:
    def now(self) -> datetime:
        return datetime.now(timezone.utc)


@dataclass(slots=True, frozen=True)
class _UuidSessionIdentity:
    def new_id(self, prefix: str) -> str:
        return f"{prefix}-{uuid4()}"


def build_default_container(settings: Settings | None = None) -> PlatformContainer:
    """Creates the default in-memory container for local development and tests."""

    resolved_settings = settings or Settings.from_env()

    capability_registry = InMemoryCapabilityRegistry()
    capability_registry.register(
        CapabilityDescriptor(
            id="context.inspect",
            name="Context Inspect",
            description="Returns the current runtime context for diagnostics.",
            output_schema={"context": "dict"},
        ),
        handler=_inspect_context,
    )

    model_registry = InMemoryModelRegistry.with_defaults(
        provider=resolved_settings.default_provider,
        model=resolved_settings.default_model,
    )
    llm_runtime = LLMRuntime(
        providers={
            "mock": MockLLMProvider(),
            "openai": OpenAIProvider(),
            "anthropic": AnthropicProvider(),
        },
        default_provider=resolved_settings.default_provider,
    )
    approval_policy: ApprovalPolicyPort = ApprovalGate()
    sandbox_policy: SandboxPolicyPort = SandboxGate(
        allowed_prefixes=resolved_settings.allowed_writeset_prefixes
    )
    delegation_transport: DelegationTransportPort = DelegationCoordinator()
    bridge = (
        HermesBridgeConfig.from_repo_root(resolved_settings.hermes_repo_root)
        if resolved_settings.hermes_repo_root
        else None
    )
    configured_adapters = set(resolved_settings.hermes_enabled_adapters)
    capability_registry_port: CapabilityRegistryPort = capability_registry
    if bridge and "capability_registry" in configured_adapters:
        capability_registry_port = HermesCapabilityRegistryAdapter(
            fallback=capability_registry,
            bridge=bridge,
        )
    if bridge and "approval" in configured_adapters:
        approval_policy = HermesApprovalPolicyAdapter(
            fallback=approval_policy,
            bridge=bridge,
        )
    if bridge and "delegation" in configured_adapters:
        delegation_transport = HermesDelegationTransportAdapter(
            fallback=delegation_transport,
            bridge=bridge,
        )
    execution_engine = ExecutionEngine(
        llm_runtime=llm_runtime,
        normalizer=ResponseNormalizer(),
        approval_gate=approval_policy,
        sandbox_gate=sandbox_policy,
        capability_registry=capability_registry_port,
        model_registry=model_registry,
    )
    kernel = AgentKernel(
        context_engine=ContextEngine(),
        delegation=delegation_transport,
        execution_engine=execution_engine,
    )

    session_store = InMemorySessionStore()
    artifact_store = InMemoryArtifactStore()
    if resolved_settings.memory_store_root:
        memory_store = JsonlMemoryStore(resolved_settings.memory_store_root)
        evidence_store = JsonlEvidenceStore(resolved_settings.memory_store_root)
        memory_dataset_store = JsonlMemoryDatasetStore(resolved_settings.memory_store_root)
    else:
        memory_store = InMemoryMemoryStore()
        evidence_store = InMemoryEvidenceStore()
        memory_dataset_store = InMemoryMemoryDatasetStore()
    summarizer = None
    if resolved_settings.memory_summarizer_provider and resolved_settings.memory_summarizer_model:
        summarizer = LLMMemorySummarizer(
            llm_runtime=llm_runtime,
            summary_policy=ModelPolicy(
                provider=resolved_settings.memory_summarizer_provider,
                model=resolved_settings.memory_summarizer_model,
                max_output_tokens=256,
            ),
            extraction_policy=ModelPolicy(
                provider=resolved_settings.memory_summarizer_provider,
                model=(
                    resolved_settings.memory_summarizer_extract_model
                    or resolved_settings.memory_summarizer_model
                ),
                max_output_tokens=256,
            ),
        )
    app_domain_service = DefaultAgentAppDomainService()
    workflow_domain_service = DefaultWorkflowDomainService()
    session_domain_service = DefaultSessionDomainService(
        ledger=session_store,
        artifact_store=artifact_store,
        clock=_SystemSessionClock(),
        identity=_UuidSessionIdentity(),
    )
    memory_domain_service = DefaultMemoryDomainService(
        memory_records=memory_store,
        evidence_records=evidence_store,
        dataset_records=memory_dataset_store,
        reasoning=summarizer,
        default_project_scope_key="shanforge",
        promotion_policy=MemoryPromotionPolicy(
            default_min_confidence=resolved_settings.memory_promotion_default_min_confidence,
            min_confidence_by_kind={
                MemoryKind(kind): threshold
                for kind, threshold in (
                    resolved_settings.memory_promotion_min_confidence_by_kind.items()
                )
            },
            draft_kinds=tuple(
                MemoryKind(kind) for kind in resolved_settings.memory_promotion_draft_kinds
            ),
            allowed_scopes_by_kind={
                MemoryKind(kind): tuple(MemoryScope(scope) for scope in scopes)
                for kind, scopes in (
                    resolved_settings.memory_promotion_allowed_scopes_by_kind.items()
                )
            },
        ),
    )
    app_service = AgentAppService(domain_service=app_domain_service)
    workflow_service = WorkflowService(domain_service=workflow_domain_service)
    execution_service = ExecutionService(
        app_service=app_domain_service,
        workflow_service=workflow_domain_service,
        session_service=session_domain_service,
        memory_service=memory_domain_service,
        kernel=kernel,
    )

    return PlatformContainer(
        settings=resolved_settings,
        app_api=AgentAppAPI(service=app_service),
        workflow_api=WorkflowAPI(service=workflow_service),
        runtime_api=RuntimeAPI(service=execution_service),
        capability_registry=capability_registry_port,
        approval_policy=approval_policy,
        sandbox_policy=sandbox_policy,
        delegation_transport=delegation_transport,
        model_registry=model_registry,
        session_store=session_store,
        artifact_store=artifact_store,
        memory_store=memory_store,
        evidence_store=evidence_store,
        memory_dataset_store=memory_dataset_store,
    )


def _inspect_context(
    session: AgentSession,
    step: WorkflowStep,
    payload: dict[str, object],
) -> CapabilityResult:
    return CapabilityResult(
        capability_id=step.capability_id or "context.inspect",
        summary="Returned the current runtime context snapshot.",
        output={"context": payload, "session_id": session.id},
    )
