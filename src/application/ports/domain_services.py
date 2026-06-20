from __future__ import annotations

from typing import Any, Mapping, Protocol, Sequence

from domain.agent_app.manifest import AgentAppManifest
from domain.agent_app.models import AgentApp
from domain.agent_app.policies import ModelPolicy
from domain.approval.models import ApprovalDecision, SandboxDecision
from domain.capability.models import CapabilityDescriptor, CapabilityResult
from domain.context.models import ContextEnvelope
from domain.delegation.models import (
    DelegationPlan,
    DelegationResult,
    DelegationTask,
    DelegationTicket,
)
from domain.memory import RecallPreview
from domain.memory.models import (
    DistillationResult,
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
from domain.model.models import ModelResponse
from domain.response.models import AgentResponse
from domain.session.models import AgentSession, SessionArtifact
from domain.workflow.models import WorkflowDefinition
from domain.workflow.state import WorkflowRunState
from domain.workflow.steps import WorkflowStep


class AgentAppDomainService(Protocol):
    """Business-domain contract owned by the application layer for app assembly."""

    def build_from_manifest(self, manifest: AgentAppManifest) -> AgentApp: ...

    def list_required_capabilities(self, app: AgentApp) -> tuple[str, ...]: ...


class WorkflowDomainService(Protocol):
    """Business-domain contract owned by the application layer for workflow decisions."""

    def resolve_workflow(
        self,
        app: AgentApp,
        workflow_id: str | None = None,
    ) -> WorkflowDefinition: ...

    def open_run_state(self, workflow: WorkflowDefinition) -> WorkflowRunState: ...


class SessionDomainService(Protocol):
    """Business-domain contract owned by the application layer for session lifecycle."""

    def open_session(
        self,
        app_id: str,
        workflow_id: str,
        user_input: str,
        session_id: str | None = None,
    ) -> AgentSession: ...

    def complete_session(self, session: AgentSession) -> AgentSession: ...

    def fail_session(self, session: AgentSession, reason: str) -> AgentSession: ...

    def persist_session(self, session: AgentSession) -> AgentSession: ...

    def attach_artifacts(
        self,
        session: AgentSession,
        artifacts: Sequence[SessionArtifact],
    ) -> AgentSession: ...


class MemoryDomainService(Protocol):
    """Business-domain contract owned by the application layer for memory logic."""

    def prepare_session(
        self,
        session: AgentSession,
        app: AgentApp,
        workflow: WorkflowDefinition,
    ) -> RecallBundle: ...

    def recall(self, query: RecallQuery) -> RecallBundle: ...

    def preview_recall(
        self,
        session: AgentSession,
        limit: int | None = None,
    ) -> RecallPreview: ...

    def distill_session(self, session: AgentSession) -> DistillationResult: ...

    def explain_session_memory(self, session: AgentSession) -> Mapping[str, Any]: ...

    def review_lifecycle(self, session: AgentSession) -> MemoryLifecycleReviewResult: ...

    def load_lifecycle_queue(
        self,
        session: AgentSession,
        queue_filter: MemoryLifecycleQueueFilter | None = None,
    ) -> MemoryLifecycleQueue: ...

    def reopen_lifecycle_queue(
        self,
        session: AgentSession,
        actor: str,
        record_ids: tuple[str, ...] | None = None,
        queue_filter: MemoryLifecycleQueueFilter | None = None,
        note: str | None = None,
    ) -> MemoryLifecycleQueueUpdateResult: ...

    def load_lifecycle_audit(
        self,
        session: AgentSession,
        audit_filter: MemoryLifecycleAuditFilter | None = None,
    ) -> MemoryLifecycleAuditLog: ...

    def apply_lifecycle(
        self,
        session: AgentSession,
        actor: str,
        record_ids: tuple[str, ...] | None = None,
        queue_filter: MemoryLifecycleQueueFilter | None = None,
    ) -> MemoryLifecycleApplyResult: ...

    def update_lifecycle_queue(
        self,
        session: AgentSession,
        actor: str,
        review_status: MemoryLifecycleQueueReviewStatus,
        record_ids: tuple[str, ...] | None = None,
        queue_filter: MemoryLifecycleQueueFilter | None = None,
        note: str | None = None,
        resolution: MemoryLifecycleReviewResolution | None = None,
    ) -> MemoryLifecycleQueueUpdateResult: ...


class ContextDomainService(Protocol):
    """Business-domain contract owned by the application layer for context logic."""

    def compile_context(
        self,
        app: AgentApp,
        workflow: WorkflowDefinition,
        session: AgentSession,
        step: WorkflowStep | None = None,
        state: WorkflowRunState | None = None,
    ) -> ContextEnvelope: ...


class ModelDomainService(Protocol):
    """Business-domain contract owned by the application layer for model policy logic."""

    def resolve_policy(
        self,
        step_policy: ModelPolicy | None,
        app_policy: ModelPolicy | None,
    ) -> ModelPolicy: ...


class CapabilityDomainService(Protocol):
    """Business-domain contract owned by the application layer for capability logic."""

    def describe_capabilities(self, app: AgentApp) -> tuple[CapabilityDescriptor, ...]: ...

    def invoke_capability(
        self,
        capability_id: str,
        session: AgentSession,
        step: WorkflowStep,
        payload: Mapping[str, Any],
    ) -> CapabilityResult: ...


class ApprovalDomainService(Protocol):
    """Business-domain contract owned by the application layer for approval logic."""

    def evaluate_step(
        self,
        step: WorkflowStep,
        session: AgentSession | None = None,
        capability: CapabilityDescriptor | None = None,
    ) -> ApprovalDecision: ...

    def evaluate_writeset(
        self,
        step: WorkflowStep,
        writeset: tuple[str, ...],
        workspace_root: str | None = None,
    ) -> SandboxDecision: ...


class DelegationDomainService(Protocol):
    """Business-domain contract owned by the application layer for delegation logic."""

    def plan(
        self,
        step: WorkflowStep,
        session: AgentSession,
    ) -> DelegationPlan: ...

    def dispatch(self, task: DelegationTask) -> DelegationTicket: ...

    def collect(self, ticket: DelegationTicket) -> DelegationResult: ...


class ResponseDomainService(Protocol):
    """Business-domain contract owned by the application layer for response logic."""

    def normalize_model_response(self, response: ModelResponse) -> AgentResponse: ...

    def normalize_capability_result(
        self,
        result: CapabilityResult,
        session: AgentSession | None = None,
    ) -> AgentResponse: ...
