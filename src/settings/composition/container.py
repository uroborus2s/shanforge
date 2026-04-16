from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from access.api.app_api import AgentAppAPI
from access.api.runtime_api import RuntimeAPI
from access.api.workflow_api import WorkflowAPI
from settings.approval.hermes_policy import HermesApprovalPolicyAdapter
from settings.capability_registry.hermes_registry import HermesCapabilityRegistryAdapter
from settings.capability_registry.registry import InMemoryCapabilityRegistry
from settings.composition.settings import Settings
from settings.delegation.hermes_transport import HermesDelegationTransportAdapter
from settings.hermes.bridge import HermesBridgeConfig
from settings.memory import (
    InMemoryEvidenceStore,
    InMemoryMemoryDatasetStore,
    InMemoryMemoryStore,
    JsonlEvidenceStore,
    JsonlMemoryDatasetStore,
    JsonlMemoryStore,
)
from settings.model import AnthropicProvider, MockLLMProvider, OpenAIProvider
from settings.model.registry import InMemoryModelRegistry
from settings.session import (
    EmptyVectorIndexProvider,
    InMemoryArtifactStore,
    InMemorySearchIndexProvider,
    InMemorySessionArchiveProvider,
    InMemorySessionStore,
)
from settings.skills import LocalSkillCatalogProvider
from settings.workspace import LocalWorkspaceProvider
from application.app_compilation.service import AgentAppService
from application.execution.service import ExecutionService
from application.workflow_resolution.service import WorkflowService
from domain.agent_app.policies import ModelPolicy
from domain.agent_app.service import DefaultAgentAppDomainService
from domain.capability.models import CapabilityDescriptor, CapabilityResult
from domain.memory.models import MemoryKind, MemoryScope
from domain.memory.policy import MemoryPromotionPolicy
from domain.memory.service import DefaultMemoryDomainService
from domain.session.models import AgentSession
from domain.session.service import DefaultSessionDomainService
from domain.workflow.service import DefaultWorkflowDomainService
from domain.workflow.steps import WorkflowStep
from runtime.agent_kernel import AgentKernel
from runtime.approval.gate import ApprovalGate
from runtime.approval.sandbox import SandboxGate
from runtime.browser.service import BrowserService
from runtime.capability import CapabilityPackageRegistry
from runtime.capability.executor import ExecutionEngine
from runtime.clock_identity.service import ClockIdentityService
from runtime.context.engine import ContextEngine
from runtime.delegation.coordinator import DelegationCoordinator
from runtime.file_access.service import FileAccessService
from runtime.llm.runtime import LLMRuntime
from runtime.memory.summarizer import LLMMemorySummarizer
from runtime.ports import (
    ApprovalPolicyPort,
    CapabilityRegistryPort,
    DelegationTransportPort,
    SandboxPolicyPort,
)
from runtime.profile_source.service import ProfileSourceService
from runtime.response.normalizer import ResponseNormalizer
from runtime.rule_source.service import RuleSourceService
from runtime.session_search.service import SessionSearchService
from runtime.skills.service import SkillCatalogService
from runtime.terminal.service import TerminalService
from runtime.web_access.service import WebAccessService

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
    capability_packages: CapabilityPackageRegistry
    file_access: FileAccessService
    web_access: WebAccessService
    terminal: TerminalService
    browser: BrowserService
    session_search: SessionSearchService
    skills: SkillCatalogService
    rule_source: RuleSourceService
    profile_source: ProfileSourceService
    clock_identity: ClockIdentityService
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

    workspace_root = Path(
        resolved_settings.workspace_root or os.getcwd()
    ).expanduser().resolve()
    project_skills_root = Path(
        resolved_settings.project_skills_root or workspace_root / "skills"
    ).expanduser().resolve()
    codex_home = os.getenv("CODEX_HOME")
    default_global_skills_root = Path(codex_home) / "skills" if codex_home else None
    global_skills_root = (
        Path(resolved_settings.global_skills_root).expanduser().resolve()
        if resolved_settings.global_skills_root
        else default_global_skills_root.expanduser().resolve()
        if default_global_skills_root is not None
        else None
    )
    managed_skills_root = Path(
        resolved_settings.managed_skills_root or workspace_root / ".factory/runtime/skills"
    ).expanduser().resolve()
    skill_state_path = Path(
        resolved_settings.skill_state_path
        or workspace_root / ".factory/runtime/skill-state.json"
    ).expanduser().resolve()

    workspace_provider = LocalWorkspaceProvider(workspace_root=workspace_root)
    skill_provider = LocalSkillCatalogProvider(
        project_root=project_skills_root,
        global_root=global_skills_root,
        managed_root=managed_skills_root,
        state_path=skill_state_path,
    )
    session_archive_provider = InMemorySessionArchiveProvider(
        session_store=session_store,
        artifact_store=artifact_store,
    )

    capability_packages = CapabilityPackageRegistry()
    file_access = FileAccessService(
        file_provider=workspace_provider,
        workspace_provider=workspace_provider,
    )
    web_access = WebAccessService()
    terminal = TerminalService()
    browser = BrowserService()
    session_search = SessionSearchService(
        structured_store=session_archive_provider,
        search_index=InMemorySearchIndexProvider(session_archive_provider),
        vector_index=EmptyVectorIndexProvider(),
    )
    skills = SkillCatalogService(
        skill_source=skill_provider,
        skill_management=skill_provider,
    )
    rule_source = RuleSourceService()
    profile_source = ProfileSourceService()
    clock_identity = ClockIdentityService()
    for service in (
        file_access,
        web_access,
        terminal,
        browser,
        session_search,
        skills,
        rule_source,
        profile_source,
        clock_identity,
    ):
        capability_packages.register(service.describe_package(), service)
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
        capability_packages=capability_packages,
        file_access=file_access,
        web_access=web_access,
        terminal=terminal,
        browser=browser,
        session_search=session_search,
        skills=skills,
        rule_source=rule_source,
        profile_source=profile_source,
        clock_identity=clock_identity,
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
