from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from access.api.app_api import AgentAppAPI
from access.api.memory_api import MemoryAPI
from access.api.runtime_api import RuntimeAPI
from access.api.workflow_api import WorkflowAPI
from application.app_compilation.service import AgentAppService
from application.execution.service import ExecutionService
from application.memory.governance_service import MemoryGovernanceService
from application.memory.inspection_service import MemoryInspectionService
from application.session.inspection_service import SessionInspectionService
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
from runtime.approval.sandbox import SandboxGate
from runtime.browser.service import BrowserService
from runtime.capability import CapabilityPackageRegistry
from runtime.capability.executor import ExecutionEngine
from runtime.clock_identity.service import ClockIdentityService
from runtime.clock_identity.session_adapter import SessionClockAdapter, SessionIdentityAdapter
from runtime.context.engine import ContextEngine
from runtime.file_access.service import FileAccessService
from runtime.llm.runtime import LLMRuntime
from runtime.memory.provider_manager import DefaultMemoryProviderManager
from runtime.memory.recall_planner import DefaultRecallPlanner
from runtime.memory.recall_ranker import DefaultRecallRanker
from runtime.memory.summarizer import LLMMemorySummarizer
from runtime.ports import (
    ApprovalPolicyPort,
    CapabilityRegistryPort,
    DelegationTransportPort,
    SandboxPolicyPort,
)
from runtime.profile_source.memory_adapter import MemoryProfileResolverAdapter
from runtime.profile_source.service import ProfileSourceService
from runtime.response.normalizer import ResponseNormalizer
from runtime.rule_source.memory_adapter import MemoryRuleBundleAdapter
from runtime.rule_source.service import RuleSourceService
from runtime.session_search import SessionSearchQueryAdapter
from runtime.session_search.service import SessionSearchService
from runtime.skills.memory_adapter import MemorySkillCatalogAdapter
from runtime.skills.service import SkillCatalogService
from runtime.terminal.service import TerminalService
from runtime.web_access.service import WebAccessService
from settings.composition.component_bindings import build_component_container
from settings.composition.provider_manager import DefaultProviderManager
from settings.composition.settings import Settings
from settings.delegation import InMemoryDelegationDigestStore, JsonlDelegationDigestStore
from settings.hermes.bridge import HermesBridgeConfig
from settings.model.registry import InMemoryModelRegistry
from settings.session import (
    EmptyVectorIndexProvider,
    InMemoryArtifactStore,
    InMemorySearchIndexProvider,
    InMemorySessionArchiveProvider,
    InMemorySessionAssemblyStore,
    InMemorySessionStore,
    JsonlSessionAssemblyStore,
)
from settings.shared import SystemClockProvider, UuidIdGeneratorProvider
from settings.skills import LocalSkillCatalogProvider
from settings.workspace import (
    LocalProfileSourceProvider,
    LocalRuleSourceProvider,
    LocalWorkspaceProvider,
)


@dataclass(slots=True)
class PlatformContainer:
    """Fully wired default container for the v2 scaffold runtime."""

    settings: Settings
    app_api: AgentAppAPI
    workflow_api: WorkflowAPI
    runtime_api: RuntimeAPI
    memory_api: MemoryAPI
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
    assembly_store: Any
    digest_store: Any
    memory_store: Any
    evidence_store: Any
    memory_dataset_store: Any
    memory_lifecycle_audit_store: Any
    memory_lifecycle_queue_store: Any
    memory_provider: Any


def _first_non_empty(*values: object) -> str | None:
    for value in values:
        if value is None:
            continue
        normalized = str(value).strip()
        if normalized:
            return normalized
    return None


def _normalize_backend_ids(payload: dict[str, Any]) -> dict[str, str]:
    raw_backend_ids = payload.get("backend_ids")
    if not isinstance(raw_backend_ids, dict):
        return {}
    normalized: dict[str, str] = {}
    for family, choice in raw_backend_ids.items():
        family_text = str(family).strip()
        choice_text = str(choice).strip()
        if family_text and choice_text:
            normalized[family_text] = choice_text
    return normalized


def _normalize_backend_binding_metadata(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw_metadata = payload.get("backend_binding_metadata")
    if not isinstance(raw_metadata, dict):
        return {}
    normalized: dict[str, dict[str, Any]] = {}
    for family, metadata in raw_metadata.items():
        family_text = str(family).strip()
        if not family_text or not isinstance(metadata, dict):
            continue
        normalized[family_text] = dict(metadata)
    return normalized


def _normalize_provider_binding_metadata(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw_metadata = payload.get("provider_binding_metadata")
    if not isinstance(raw_metadata, dict):
        return {}
    normalized: dict[str, dict[str, Any]] = {}
    for family, metadata in raw_metadata.items():
        family_text = str(family).strip()
        if not family_text or not isinstance(metadata, dict):
            continue
        normalized[family_text] = dict(metadata)
    return normalized


def _memory_provider_source_metadata(payload: object) -> dict[str, Any]:
    if isinstance(payload, dict):
        return dict(payload)
    return {}


def _build_backend_binding_metadata(
    component: object,
    binding_id: str,
    *,
    source_metadata: dict[str, Any] | None = None,
    requested_binding_id: str | None = None,
    default_source: str = "runtime-resolved",
) -> dict[str, Any]:
    metadata: dict[str, Any] = dict(source_metadata or {})
    metadata["binding_id"] = binding_id
    metadata["implementation_class"] = component.__class__.__name__
    if requested_binding_id and requested_binding_id != binding_id:
        metadata["requested_binding_id"] = requested_binding_id
        metadata.setdefault("resolution", "fallback")
    contract_metadata = getattr(component, "contract_metadata", None)
    if callable(contract_metadata):
        payload = contract_metadata()
        if isinstance(payload, dict):
            metadata.update(payload)
    else:
        metadata.setdefault("bridge_kind", "local")
        metadata.setdefault("contract_ready", True)
    metadata.setdefault("binding_source", default_source)
    return metadata


def _provider_contract_ready(provider: object) -> bool:
    contract_metadata = getattr(provider, "contract_metadata", None)
    if not callable(contract_metadata):
        return True
    payload = contract_metadata()
    if not isinstance(payload, dict):
        return True
    return bool(payload.get("contract_ready", True))


def _resolve_governance_binding_choice(
    family: str,
    requested_backend_ids: dict[str, str],
    configured_adapters: set[str],
    *,
    aliases: tuple[str, ...],
) -> str:
    requested_binding_id = requested_backend_ids.get(family)
    if requested_binding_id is not None:
        normalized = requested_binding_id.strip()
        if normalized:
            return normalized
    if any(alias in configured_adapters for alias in aliases):
        return "hermes"
    return "local"


def _resolve_governance_component(
    *,
    family: str,
    requested_binding_id: str,
    local_component: object,
    bridge: HermesBridgeConfig | None,
    component_container: Any,
) -> tuple[object, str]:
    if requested_binding_id != "hermes":
        return local_component, "local"
    if bridge is None:
        return local_component, "local"
    return (
        component_container.resolve(
            family,
            "hermes",
            fallback=local_component,
            bridge=bridge,
        ),
        "hermes",
    )


def build_default_container(settings: Settings | None = None) -> PlatformContainer:
    """Creates the default in-memory container for local development and tests."""

    resolved_settings = settings or Settings.from_env()
    workspace_root = Path(
        resolved_settings.workspace_root or os.getcwd()
    ).expanduser().resolve()
    component_container = build_component_container()
    profile_catalog_path = (
        Path(resolved_settings.profile_catalog_path).expanduser().resolve()
        if resolved_settings.profile_catalog_path
        else None
    )
    provider_catalog_path = (
        Path(resolved_settings.provider_catalog_path).expanduser().resolve()
        if resolved_settings.provider_catalog_path
        else None
    )
    backend_catalog_path = (
        Path(resolved_settings.backend_catalog_path).expanduser().resolve()
        if resolved_settings.backend_catalog_path
        else None
    )
    profile_provider = LocalProfileSourceProvider(
        default_profile_id=resolved_settings.default_profile_id,
        default_workspace_root=workspace_root,
        catalog_path=profile_catalog_path,
        backend_catalog_path=backend_catalog_path,
        provider_catalog_path=provider_catalog_path,
    )
    resolved_profile_payload = dict(
        profile_provider.resolve_profile({"workspace_root": str(workspace_root)}) or {}
    )
    resolved_profile_backend_ids = _normalize_backend_ids(resolved_profile_payload)
    resolved_profile_binding_metadata = _normalize_backend_binding_metadata(
        resolved_profile_payload
    )
    store_default_choice = "jsonl" if resolved_settings.memory_store_root else "in_memory"
    binding_source = "profile" if resolved_profile_payload else "settings-default"
    capability_registry = component_container.resolve("capability_registry", "local")
    capability_registry.register(
        CapabilityDescriptor(
            id="context.inspect",
            name="Context Inspect",
            description="Returns the current runtime context for diagnostics.",
            output_schema={"context": "dict"},
        ),
        handler=_inspect_context,
    )

    providers = {
        provider_id: component_container.resolve("llm_provider", provider_id)
        for provider_id in component_container.registry.names("llm_provider")
    }
    ready_provider_ids = tuple(
        provider_id
        for provider_id, provider in sorted(providers.items())
        if _provider_contract_ready(provider)
    )
    provider_manager = DefaultProviderManager(
        available_llm_providers=tuple(sorted(providers)),
        ready_llm_providers=ready_provider_ids,
        default_provider=resolved_settings.default_provider,
        default_model=resolved_settings.default_model,
    )
    provider_selection = provider_manager.resolve_llm_selection(resolved_profile_payload)
    resolved_provider_id = provider_selection.provider_id
    resolved_model = provider_selection.model_id
    resolved_provider_binding_metadata = _normalize_provider_binding_metadata(
        resolved_profile_payload
    )

    def binding_choice(family: str, default: str) -> str:
        return resolved_profile_backend_ids.get(family, default)

    resolved_backend_ids = {
        "llm_provider": resolved_provider_id,
        "memory_provider": binding_choice("memory_provider", "none"),
        "memory_store": binding_choice("memory_store", store_default_choice),
        "evidence_store": binding_choice("evidence_store", store_default_choice),
        "memory_dataset_store": binding_choice("memory_dataset_store", store_default_choice),
        "memory_lifecycle_audit_store": binding_choice(
            "memory_lifecycle_audit_store",
            store_default_choice,
        ),
        "memory_lifecycle_queue_store": binding_choice(
            "memory_lifecycle_queue_store",
            store_default_choice,
        ),
        "web_search": binding_choice("web_search", "local"),
        "web_document": binding_choice("web_document", "local"),
        "shell_command": binding_choice("shell_command", "local"),
        "git": binding_choice("git", "local"),
        "browser_automation": binding_choice("browser_automation", "local"),
    }
    model_registry = InMemoryModelRegistry.with_defaults(
        provider=resolved_provider_id,
        model=resolved_model,
    )
    llm_runtime = LLMRuntime(
        providers=providers,
        default_provider=resolved_provider_id,
    )
    approval_policy: ApprovalPolicyPort = component_container.resolve("approval_policy", "local")
    sandbox_policy: SandboxPolicyPort = SandboxGate(
        allowed_prefixes=resolved_settings.allowed_writeset_prefixes
    )
    delegation_transport: DelegationTransportPort = component_container.resolve(
        "delegation_transport",
        "local",
    )
    bridge = (
        HermesBridgeConfig.from_repo_root(resolved_settings.hermes_repo_root)
        if resolved_settings.hermes_repo_root
        else None
    )
    configured_adapters = set(resolved_settings.hermes_enabled_adapters)
    requested_backend_ids = dict(resolved_backend_ids)
    requested_backend_ids.update(
        {
            "capability_registry": _resolve_governance_binding_choice(
                "capability_registry",
                resolved_profile_backend_ids,
                configured_adapters,
                aliases=("capability_registry",),
            ),
            "approval_policy": _resolve_governance_binding_choice(
                "approval_policy",
                resolved_profile_backend_ids,
                configured_adapters,
                aliases=("approval", "approval_policy"),
            ),
            "delegation_transport": _resolve_governance_binding_choice(
                "delegation_transport",
                resolved_profile_backend_ids,
                configured_adapters,
                aliases=("delegation", "delegation_transport"),
            ),
        }
    )
    capability_registry_port, capability_registry_binding_id = _resolve_governance_component(
        family="capability_registry",
        requested_binding_id=requested_backend_ids["capability_registry"],
        local_component=capability_registry,
        bridge=bridge,
        component_container=component_container,
    )
    approval_policy, approval_policy_binding_id = _resolve_governance_component(
        family="approval_policy",
        requested_binding_id=requested_backend_ids["approval_policy"],
        local_component=approval_policy,
        bridge=bridge,
        component_container=component_container,
    )
    delegation_transport, delegation_transport_binding_id = _resolve_governance_component(
        family="delegation_transport",
        requested_binding_id=requested_backend_ids["delegation_transport"],
        local_component=delegation_transport,
        bridge=bridge,
        component_container=component_container,
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

    selected_store_choices = {
        binding_choice("memory_store", store_default_choice),
        binding_choice("evidence_store", store_default_choice),
        binding_choice("memory_dataset_store", store_default_choice),
        binding_choice("memory_lifecycle_audit_store", store_default_choice),
        binding_choice("memory_lifecycle_queue_store", store_default_choice),
    }
    profile_scoped_store_root = resolved_settings.memory_store_root or (
        str(
            workspace_root
            / ".factory"
            / "runtime"
            / "profiles"
            / str(
                resolved_profile_payload.get("profile_id")
                or resolved_settings.default_profile_id
            )
            / "stores"
        )
        if selected_store_choices != {"in_memory"}
        else None
    )

    session_store = InMemorySessionStore()
    artifact_store = InMemoryArtifactStore()
    if profile_scoped_store_root:
        assembly_store = JsonlSessionAssemblyStore(profile_scoped_store_root)
        digest_store = JsonlDelegationDigestStore(profile_scoped_store_root)
    else:
        assembly_store = InMemorySessionAssemblyStore()
        digest_store = InMemoryDelegationDigestStore()

    default_memory_provider_root = str(
        workspace_root
        / ".factory"
        / "runtime"
        / "profiles"
        / str(resolved_profile_payload.get("profile_id") or resolved_settings.default_profile_id)
        / "memory-provider"
    )

    def resolve_store_component(family: str):
        choice = binding_choice(family, store_default_choice)
        if choice == "jsonl":
            if profile_scoped_store_root is None:
                raise ValueError(f"{family} is configured as jsonl without a root.")
            return component_container.resolve(
                family,
                choice,
                root=profile_scoped_store_root,
            )
        return component_container.resolve(family, choice)

    memory_store = resolve_store_component("memory_store")
    evidence_store = resolve_store_component("evidence_store")
    memory_dataset_store = resolve_store_component("memory_dataset_store")
    memory_lifecycle_audit_store = resolve_store_component("memory_lifecycle_audit_store")
    memory_lifecycle_queue_store = resolve_store_component("memory_lifecycle_queue_store")
    memory_provider_choice = binding_choice("memory_provider", "none")
    memory_provider_source_metadata = resolved_profile_binding_metadata.get("memory_provider")
    memory_provider_root = _first_non_empty(
        memory_provider_source_metadata.get("state_root")
        if isinstance(memory_provider_source_metadata, dict)
        else None,
        resolved_settings.memory_provider_root,
        default_memory_provider_root,
    )
    if memory_provider_choice in {"jsonl", "jsonl_vector"}:
        memory_provider = component_container.resolve(
            "memory_provider",
            memory_provider_choice,
            root=memory_provider_root,
        )
    else:
        memory_provider = component_container.resolve(
            "memory_provider",
            memory_provider_choice,
        )

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
    rule_provider = LocalRuleSourceProvider(
        default_workspace_root=workspace_root,
        catalog_path=profile_catalog_path,
    )
    skill_provider = LocalSkillCatalogProvider(
        project_root=project_skills_root,
        global_root=global_skills_root,
        managed_root=managed_skills_root,
        state_path=skill_state_path,
    )
    session_archive_provider = InMemorySessionArchiveProvider(
        session_store=session_store,
        artifact_store=artifact_store,
        assembly_store=assembly_store,
    )

    capability_packages = CapabilityPackageRegistry()
    file_access = FileAccessService(
        file_provider=workspace_provider,
        workspace_provider=workspace_provider,
    )
    web_access = WebAccessService(
        search_provider=component_container.resolve(
            "web_search",
            binding_choice("web_search", "local"),
        ),
        document_provider=component_container.resolve(
            "web_document",
            binding_choice("web_document", "local"),
        ),
    )
    terminal = TerminalService(
        shell_provider=component_container.resolve(
            "shell_command",
            binding_choice("shell_command", "local"),
        ),
        git_provider=component_container.resolve(
            "git",
            binding_choice("git", "local"),
        ),
    )
    browser = BrowserService(
        browser_provider=component_container.resolve(
            "browser_automation",
            binding_choice("browser_automation", "local"),
        ),
    )
    session_search = SessionSearchService(
        structured_store=session_archive_provider,
        search_index=InMemorySearchIndexProvider(session_archive_provider),
        vector_index=EmptyVectorIndexProvider(),
    )
    session_query_adapter = SessionSearchQueryAdapter(service=session_search)
    skills = SkillCatalogService(
        skill_source=skill_provider,
        skill_management=skill_provider,
    )
    rule_source = RuleSourceService(rule_source=rule_provider)
    profile_source = ProfileSourceService(
        profile_source=profile_provider,
        default_profile_id=resolved_settings.default_profile_id,
    )
    clock_identity = ClockIdentityService(
        clock_provider=SystemClockProvider(),
        id_provider=UuidIdGeneratorProvider(),
    )
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
    resolved_backend_ids.update(
        {
            "capability_registry": capability_registry_binding_id,
            "approval_policy": approval_policy_binding_id,
            "delegation_transport": delegation_transport_binding_id,
        }
    )
    session_context_defaults = {
        "backend_ids": resolved_backend_ids,
        "backend_binding_metadata": {
            "llm_provider": {
                **resolved_provider_binding_metadata.get("llm_provider", {}),
                "binding_id": resolved_provider_id,
                "implementation_class": providers[resolved_provider_id].__class__.__name__,
                "bridge_kind": "provider",
                "contract_ready": True,
                "binding_source": provider_selection.source,
                **(
                    {
                        "requested_binding_id": provider_selection.requested_provider_id,
                        "resolution": "fallback",
                    }
                    if provider_selection.requested_provider_id != resolved_provider_id
                    else {}
                ),
            },
            "memory_store": _build_backend_binding_metadata(
                memory_store,
                resolved_backend_ids["memory_store"],
                source_metadata=resolved_profile_binding_metadata.get("memory_store"),
                requested_binding_id=requested_backend_ids.get("memory_store"),
                default_source=binding_source,
            ),
            "evidence_store": _build_backend_binding_metadata(
                evidence_store,
                resolved_backend_ids["evidence_store"],
                source_metadata=resolved_profile_binding_metadata.get("evidence_store"),
                requested_binding_id=requested_backend_ids.get("evidence_store"),
                default_source=binding_source,
            ),
            "memory_dataset_store": _build_backend_binding_metadata(
                memory_dataset_store,
                resolved_backend_ids["memory_dataset_store"],
                source_metadata=resolved_profile_binding_metadata.get("memory_dataset_store"),
                requested_binding_id=requested_backend_ids.get("memory_dataset_store"),
                default_source=binding_source,
            ),
            "memory_lifecycle_audit_store": _build_backend_binding_metadata(
                memory_lifecycle_audit_store,
                resolved_backend_ids["memory_lifecycle_audit_store"],
                source_metadata=resolved_profile_binding_metadata.get(
                    "memory_lifecycle_audit_store"
                ),
                requested_binding_id=requested_backend_ids.get(
                    "memory_lifecycle_audit_store"
                ),
                default_source=binding_source,
            ),
            "memory_lifecycle_queue_store": _build_backend_binding_metadata(
                memory_lifecycle_queue_store,
                resolved_backend_ids["memory_lifecycle_queue_store"],
                source_metadata=resolved_profile_binding_metadata.get(
                    "memory_lifecycle_queue_store"
                ),
                requested_binding_id=requested_backend_ids.get(
                    "memory_lifecycle_queue_store"
                ),
                default_source=binding_source,
            ),
            "memory_provider": _build_backend_binding_metadata(
                memory_provider,
                resolved_backend_ids["memory_provider"],
                source_metadata={
                    **_memory_provider_source_metadata(
                        resolved_profile_binding_metadata.get("memory_provider"),
                    ),
                    **(
                        {"state_root": memory_provider_root}
                        if memory_provider_choice in {"jsonl", "jsonl_vector"}
                        else {}
                    ),
                },
                requested_binding_id=requested_backend_ids.get("memory_provider"),
                default_source=binding_source,
            ),
            "web_search": _build_backend_binding_metadata(
                web_access.search_provider,
                resolved_backend_ids["web_search"],
                source_metadata=resolved_profile_binding_metadata.get("web_search"),
                requested_binding_id=requested_backend_ids.get("web_search"),
                default_source=binding_source,
            ),
            "web_document": _build_backend_binding_metadata(
                web_access.document_provider,
                resolved_backend_ids["web_document"],
                source_metadata=resolved_profile_binding_metadata.get("web_document"),
                requested_binding_id=requested_backend_ids.get("web_document"),
                default_source=binding_source,
            ),
            "shell_command": _build_backend_binding_metadata(
                terminal.shell_provider,
                resolved_backend_ids["shell_command"],
                source_metadata=resolved_profile_binding_metadata.get("shell_command"),
                requested_binding_id=requested_backend_ids.get("shell_command"),
                default_source=binding_source,
            ),
            "git": _build_backend_binding_metadata(
                terminal.git_provider,
                resolved_backend_ids["git"],
                source_metadata=resolved_profile_binding_metadata.get("git"),
                requested_binding_id=requested_backend_ids.get("git"),
                default_source=binding_source,
            ),
            "browser_automation": _build_backend_binding_metadata(
                browser.browser_provider,
                resolved_backend_ids["browser_automation"],
                source_metadata=resolved_profile_binding_metadata.get("browser_automation"),
                requested_binding_id=requested_backend_ids.get("browser_automation"),
                default_source=binding_source,
            ),
            "capability_registry": _build_backend_binding_metadata(
                capability_registry_port,
                resolved_backend_ids["capability_registry"],
                source_metadata=resolved_profile_binding_metadata.get("capability_registry"),
                requested_binding_id=requested_backend_ids.get("capability_registry"),
                default_source=binding_source,
            ),
            "approval_policy": _build_backend_binding_metadata(
                approval_policy,
                resolved_backend_ids["approval_policy"],
                source_metadata=resolved_profile_binding_metadata.get("approval_policy"),
                requested_binding_id=requested_backend_ids.get("approval_policy"),
                default_source=binding_source,
            ),
            "delegation_transport": _build_backend_binding_metadata(
                delegation_transport,
                resolved_backend_ids["delegation_transport"],
                source_metadata=resolved_profile_binding_metadata.get("delegation_transport"),
                requested_binding_id=requested_backend_ids.get("delegation_transport"),
                default_source=binding_source,
            ),
        },
        "provider_bindings": (
            provider_selection.provider_bindings
            + (
                (f"memory_provider:{resolved_backend_ids['memory_provider']}",)
                if resolved_backend_ids["memory_provider"] != "none"
                else ()
            )
        ),
        "provider_binding_metadata": {
            "llm_provider": dict(provider_selection.metadata),
        },
        "selected_model_binding": {
            "provider_id": resolved_provider_id,
            "model_id": resolved_model,
            "source": provider_selection.source,
            "metadata": {
                **dict(provider_selection.metadata),
                "profile_id": resolved_profile_payload.get("profile_id"),
            },
        },
    }
    if resolved_backend_ids["memory_provider"] != "none":
        memory_provider_metadata = dict(
            session_context_defaults["backend_binding_metadata"].get("memory_provider", {})
        )
        session_context_defaults["memory_provider_binding"] = {
            "provider_id": resolved_backend_ids["memory_provider"],
            "source": str(memory_provider_metadata.get("binding_source") or binding_source),
            "namespace": _first_non_empty(
                memory_provider_metadata.get("namespace"),
                resolved_profile_payload.get("profile_id"),
            ),
            "mode": str(memory_provider_metadata.get("mode") or "augmentation"),
            "writable": bool(memory_provider_metadata.get("writable", False)),
            "metadata": memory_provider_metadata,
        }
    session_domain_service = DefaultSessionDomainService(
        ledger=session_store,
        artifact_store=artifact_store,
        clock=SessionClockAdapter(clock_identity),
        identity=SessionIdentityAdapter(clock_identity),
    )
    memory_domain_service = DefaultMemoryDomainService(
        memory_records=memory_store,
        evidence_records=evidence_store,
        dataset_records=memory_dataset_store,
        lifecycle_audit_records=memory_lifecycle_audit_store,
        lifecycle_queue_records=memory_lifecycle_queue_store,
        assembly_store=assembly_store,
        digest_store=digest_store,
        profile_resolver=MemoryProfileResolverAdapter(profile_source),
        rule_bundle=MemoryRuleBundleAdapter(rule_source),
        skill_catalog=MemorySkillCatalogAdapter(skills),
        reasoning=summarizer,
        memory_provider_manager=DefaultMemoryProviderManager(provider=memory_provider),
        recall_planner=DefaultRecallPlanner(),
        recall_ranker=DefaultRecallRanker(),
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
        session_context_defaults=session_context_defaults,
    )
    inspection_service = SessionInspectionService(
        session_ledger=session_store,
        archive_query=session_query_adapter,
        transcript_query=session_query_adapter,
        assembly_query=session_query_adapter,
    )
    memory_inspection_service = MemoryInspectionService(
        session_ledger=session_store,
        memory_service=memory_domain_service,
    )
    memory_governance_service = MemoryGovernanceService(
        session_ledger=session_store,
        memory_service=memory_domain_service,
    )

    return PlatformContainer(
        settings=resolved_settings,
        app_api=AgentAppAPI(service=app_service),
        workflow_api=WorkflowAPI(service=workflow_service),
        runtime_api=RuntimeAPI(service=execution_service),
        memory_api=MemoryAPI(
            session_service=inspection_service,
            memory_service=memory_inspection_service,
            memory_governance_service=memory_governance_service,
        ),
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
        assembly_store=assembly_store,
        digest_store=digest_store,
        memory_store=memory_store,
        evidence_store=evidence_store,
        memory_dataset_store=memory_dataset_store,
        memory_lifecycle_audit_store=memory_lifecycle_audit_store,
        memory_lifecycle_queue_store=memory_lifecycle_queue_store,
        memory_provider=memory_provider,
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
