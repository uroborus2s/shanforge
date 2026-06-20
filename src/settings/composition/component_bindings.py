from __future__ import annotations

import sys

from shanforge_di import DependencyRef, ServiceContainer, factory

from runtime.approval.gate import ApprovalGate
from runtime.delegation.coordinator import DelegationCoordinator
from settings.approval.hermes_policy import HermesApprovalPolicyAdapter
from settings.capability_registry.hermes_registry import HermesCapabilityRegistryAdapter
from settings.capability_registry.registry import InMemoryCapabilityRegistry
from settings.delegation.hermes_transport import HermesDelegationTransportAdapter
from settings.gateway.http_client import LocalHttpClientProvider
from settings.memory.dataset_store import InMemoryMemoryDatasetStore, JsonlMemoryDatasetStore
from settings.memory.evidence_store import InMemoryEvidenceStore, JsonlEvidenceStore
from settings.memory.lifecycle_audit_store import (
    InMemoryMemoryLifecycleAuditStore,
    JsonlMemoryLifecycleAuditStore,
)
from settings.memory.lifecycle_queue_store import (
    InMemoryMemoryLifecycleQueueStore,
    JsonlMemoryLifecycleQueueStore,
)
from settings.memory.provider import (
    InMemoryAugmentationMemoryProvider,
    JsonlAugmentationMemoryProvider,
    JsonlVectorAugmentationMemoryProvider,
    NullMemoryProvider,
    RemoteAugmentationMemoryProvider,
)
from settings.memory.store import InMemoryMemoryStore, JsonlMemoryStore
from settings.model.anthropic_provider import AnthropicProvider
from settings.model.embedding_provider import NullEmbeddingProvider
from settings.model.mock_provider import MockLLMProvider
from settings.model.openai_provider import OpenAIProvider
from settings.session.blob_store import InMemoryBlobStore
from settings.session.search_index import EmptySearchIndexProvider
from settings.session.vector_index import EmptyVectorIndexProvider
from settings.shared import (
    InMemoryBrowserAutomationProvider,
    InMemoryWebSearchProvider,
    LocalWebDocumentProvider,
)
from settings.workspace import (
    LocalGitProvider,
    LocalSecretCatalogProvider,
    LocalShellCommandProvider,
)


@factory(family="llm_provider", name="mock", default=True)
def build_mock_llm_provider() -> MockLLMProvider:
    return MockLLMProvider()


@factory(family="llm_provider", name="openai")
def build_openai_llm_provider() -> OpenAIProvider:
    return OpenAIProvider()


@factory(family="llm_provider", name="anthropic")
def build_anthropic_llm_provider() -> AnthropicProvider:
    return AnthropicProvider()


@factory(family="embedding_provider", name="null", default=True)
def build_null_embedding_provider() -> NullEmbeddingProvider:
    return NullEmbeddingProvider()


@factory(family="memory_store", name="in_memory", default=True)
def build_in_memory_memory_store() -> InMemoryMemoryStore:
    return InMemoryMemoryStore()


@factory(family="memory_store", name="jsonl", lifecycle="transient")
def build_jsonl_memory_store(root: str) -> JsonlMemoryStore:
    return JsonlMemoryStore(root)


@factory(family="evidence_store", name="in_memory", default=True)
def build_in_memory_evidence_store() -> InMemoryEvidenceStore:
    return InMemoryEvidenceStore()


@factory(family="evidence_store", name="jsonl", lifecycle="transient")
def build_jsonl_evidence_store(root: str) -> JsonlEvidenceStore:
    return JsonlEvidenceStore(root)


@factory(family="memory_dataset_store", name="in_memory", default=True)
def build_in_memory_memory_dataset_store() -> InMemoryMemoryDatasetStore:
    return InMemoryMemoryDatasetStore()


@factory(family="memory_dataset_store", name="jsonl", lifecycle="transient")
def build_jsonl_memory_dataset_store(root: str) -> JsonlMemoryDatasetStore:
    return JsonlMemoryDatasetStore(root)


@factory(family="memory_lifecycle_queue_store", name="in_memory", default=True)
def build_in_memory_memory_lifecycle_queue_store() -> InMemoryMemoryLifecycleQueueStore:
    return InMemoryMemoryLifecycleQueueStore()


@factory(family="memory_lifecycle_queue_store", name="jsonl", lifecycle="transient")
def build_jsonl_memory_lifecycle_queue_store(root: str) -> JsonlMemoryLifecycleQueueStore:
    return JsonlMemoryLifecycleQueueStore(root)


@factory(family="memory_lifecycle_audit_store", name="in_memory", default=True)
def build_in_memory_memory_lifecycle_audit_store() -> InMemoryMemoryLifecycleAuditStore:
    return InMemoryMemoryLifecycleAuditStore()


@factory(family="memory_lifecycle_audit_store", name="jsonl", lifecycle="transient")
def build_jsonl_memory_lifecycle_audit_store(root: str) -> JsonlMemoryLifecycleAuditStore:
    return JsonlMemoryLifecycleAuditStore(root)


@factory(family="memory_provider", name="none", default=True)
def build_null_memory_provider() -> NullMemoryProvider:
    return NullMemoryProvider()


@factory(family="memory_provider", name="in_memory")
def build_in_memory_memory_provider() -> InMemoryAugmentationMemoryProvider:
    return InMemoryAugmentationMemoryProvider()


@factory(family="memory_provider", name="jsonl", lifecycle="transient")
def build_jsonl_memory_provider(root: str) -> JsonlAugmentationMemoryProvider:
    return JsonlAugmentationMemoryProvider(root=root)


@factory(family="memory_provider", name="jsonl_vector", lifecycle="transient")
def build_jsonl_vector_memory_provider(root: str) -> JsonlVectorAugmentationMemoryProvider:
    return JsonlVectorAugmentationMemoryProvider(root=root)


@factory(
    family="memory_provider",
    name="remote_http",
    lifecycle="transient",
    dependencies={
        "http_client": DependencyRef("http_client", "local"),
        "secret_catalog_provider": DependencyRef("secret_catalog", "local"),
    },
)
def build_remote_http_memory_provider(
    http_client,
    secret_catalog_provider,
) -> RemoteAugmentationMemoryProvider:
    return RemoteAugmentationMemoryProvider(
        http_client=http_client,
        secret_catalog_provider=secret_catalog_provider,
    )


@factory(family="blob_store", name="in_memory", default=True)
def build_in_memory_blob_store() -> InMemoryBlobStore:
    return InMemoryBlobStore()


@factory(family="capability_registry", name="local", default=True)
def build_local_capability_registry() -> InMemoryCapabilityRegistry:
    return InMemoryCapabilityRegistry()


@factory(family="capability_registry", name="hermes", lifecycle="transient")
def build_hermes_capability_registry(
    fallback,
    bridge,
) -> HermesCapabilityRegistryAdapter:
    return HermesCapabilityRegistryAdapter(
        fallback=fallback,
        bridge=bridge,
    )


@factory(family="approval_policy", name="local", default=True)
def build_local_approval_policy() -> ApprovalGate:
    return ApprovalGate()


@factory(family="approval_policy", name="hermes", lifecycle="transient")
def build_hermes_approval_policy(
    fallback,
    bridge,
) -> HermesApprovalPolicyAdapter:
    return HermesApprovalPolicyAdapter(
        fallback=fallback,
        bridge=bridge,
    )


@factory(family="delegation_transport", name="local", default=True)
def build_local_delegation_transport() -> DelegationCoordinator:
    return DelegationCoordinator()


@factory(family="delegation_transport", name="hermes", lifecycle="transient")
def build_hermes_delegation_transport(
    fallback,
    bridge,
) -> HermesDelegationTransportAdapter:
    return HermesDelegationTransportAdapter(
        fallback=fallback,
        bridge=bridge,
    )


@factory(family="web_search", name="local", default=True)
def build_local_web_search_provider() -> InMemoryWebSearchProvider:
    return InMemoryWebSearchProvider()


@factory(family="web_document", name="local", default=True)
def build_local_web_document_provider() -> LocalWebDocumentProvider:
    return LocalWebDocumentProvider()


@factory(family="http_client", name="local", default=True)
def build_local_http_client_provider() -> LocalHttpClientProvider:
    return LocalHttpClientProvider()


@factory(family="shell_command", name="local", default=True)
def build_local_shell_command_provider() -> LocalShellCommandProvider:
    return LocalShellCommandProvider()


@factory(family="git", name="local", default=True)
def build_local_git_provider() -> LocalGitProvider:
    return LocalGitProvider()


@factory(family="secret_catalog", name="local", default=True)
def build_local_secret_catalog_provider() -> LocalSecretCatalogProvider:
    return LocalSecretCatalogProvider()


@factory(family="browser_automation", name="local", default=True)
def build_local_browser_automation_provider() -> InMemoryBrowserAutomationProvider:
    return InMemoryBrowserAutomationProvider()


@factory(family="search_index", name="empty", default=True)
def build_empty_search_index_provider() -> EmptySearchIndexProvider:
    return EmptySearchIndexProvider()


@factory(family="vector_index", name="empty", default=True)
def build_empty_vector_index_provider() -> EmptyVectorIndexProvider:
    return EmptyVectorIndexProvider()


def build_component_container() -> ServiceContainer:
    """Builds the local business binding layer on top of the external shanforge-di kernel."""

    container = ServiceContainer()
    container.register_module(sys.modules[__name__])
    return container
