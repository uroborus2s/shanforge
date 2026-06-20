from __future__ import annotations

from typing import Any, Mapping, Protocol

from domain.agent_app.manifest import AgentAppManifest
from domain.agent_app.models import AgentApp
from domain.capability.models import CapabilityDescriptor
from domain.memory import RecallPreview
from domain.memory.models import (
    MemoryLifecycleApplyResult,
    MemoryLifecycleAuditFilter,
    MemoryLifecycleAuditLog,
    MemoryLifecycleQueue,
    MemoryLifecycleQueueFilter,
    MemoryLifecycleReviewResolution,
    MemoryLifecycleQueueReviewStatus,
    MemoryLifecycleQueueUpdateResult,
    MemoryLifecycleReviewResult,
    RecallBundle,
    RecallQuery,
)
from domain.response.models import AgentResponse
from domain.session.archive_models import SessionArchiveHit, SessionTranscriptSlice
from domain.session.assembly_models import SessionAssemblyManifest
from domain.session.models import AgentSession
from domain.workflow.models import WorkflowDefinition
from domain.workflow.state import WorkflowRunState


class AgentAppMaterializationUseCase(Protocol):
    """Application use case contract consumed by access gateways for app materialization."""

    def build_from_manifest(self, manifest: AgentAppManifest) -> AgentApp: ...


class WorkflowDescriptionUseCase(Protocol):
    """Application use case contract consumed by access gateways for workflow inspection."""

    def resolve(self, app: AgentApp, workflow_id: str | None = None) -> WorkflowDefinition: ...


class RuntimeExecutionUseCase(Protocol):
    """Application use case contract consumed by access gateways for runtime execution."""

    def execute_manifest(
        self,
        manifest: AgentAppManifest,
        user_input: str,
        workflow_id: str | None = None,
        session_id: str | None = None,
    ) -> RuntimeExecutionResult: ...

    def execute_app(
        self,
        app: AgentApp,
        user_input: str,
        workflow_id: str | None = None,
        session_id: str | None = None,
    ) -> RuntimeExecutionResult: ...


class RuntimeExecutionResult(Protocol):
    """Structural result envelope returned by runtime execution use cases."""

    response: AgentResponse
    session: AgentSession
    state: WorkflowRunState


class SessionInspectionUseCase(Protocol):
    """Application use case contract for session inspection and replay entrypoints."""

    def get_session(self, session_id: str) -> AgentSession | None: ...

    def search_session_archive(
        self,
        query: str,
        profile_id: str | None,
        limit: int = 10,
    ) -> tuple[SessionArchiveHit, ...]: ...

    def load_session_slice(
        self,
        session_id: str,
        cursor: str | None,
        limit: int,
    ) -> SessionTranscriptSlice: ...

    def explain_session_assembly(self, session_id: str) -> SessionAssemblyManifest: ...


class MemoryInspectionUseCase(Protocol):
    """Application use case contract for memory recall and explainability queries."""

    def recall(self, query: RecallQuery) -> RecallBundle: ...

    def preview_recall(
        self,
        session_id: str,
        limit: int | None = None,
    ) -> RecallPreview: ...


class MemoryGovernanceUseCase(Protocol):
    """Application use case contract for lifecycle review and apply entrypoints."""

    def review_lifecycle(self, session_id: str) -> MemoryLifecycleReviewResult: ...

    def load_lifecycle_queue(
        self,
        session_id: str,
        queue_filter: MemoryLifecycleQueueFilter | None = None,
    ) -> MemoryLifecycleQueue: ...

    def reopen_lifecycle_queue(
        self,
        session_id: str,
        actor: str,
        record_ids: tuple[str, ...] | None = None,
        queue_filter: MemoryLifecycleQueueFilter | None = None,
        note: str | None = None,
    ) -> MemoryLifecycleQueueUpdateResult: ...

    def load_lifecycle_audit(
        self,
        session_id: str,
        audit_filter: MemoryLifecycleAuditFilter | None = None,
    ) -> MemoryLifecycleAuditLog: ...

    def apply_lifecycle(
        self,
        session_id: str,
        actor: str,
        record_ids: tuple[str, ...] | None = None,
        queue_filter: MemoryLifecycleQueueFilter | None = None,
    ) -> MemoryLifecycleApplyResult: ...

    def update_lifecycle_queue(
        self,
        session_id: str,
        actor: str,
        review_status: MemoryLifecycleQueueReviewStatus,
        record_ids: tuple[str, ...] | None = None,
        queue_filter: MemoryLifecycleQueueFilter | None = None,
        note: str | None = None,
        resolution: MemoryLifecycleReviewResolution | None = None,
    ) -> MemoryLifecycleQueueUpdateResult: ...


class CapabilityCatalogUseCase(Protocol):
    """Application use case contract for capability catalog exposure."""

    def list_capabilities(self, app_id: str | None = None) -> tuple[CapabilityDescriptor, ...]: ...


class PlatformHealthUseCase(Protocol):
    """Application use case contract for health and readiness checks."""

    def check(self) -> Mapping[str, Any]: ...
