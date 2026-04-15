from __future__ import annotations

from typing import Any, Mapping, Protocol

from application.execution.service import ExecutionResult
from domain.agent_app.manifest import AgentAppManifest
from domain.agent_app.models import AgentApp
from domain.capability.models import CapabilityDescriptor
from domain.memory.models import RecallBundle, RecallQuery
from domain.session.models import AgentSession
from domain.workflow.models import WorkflowDefinition


class AgentAppMaterializationUseCase(Protocol):
    """Application use case contract consumed by access gateways for app materialization."""

    def materialize(self, manifest: AgentAppManifest) -> AgentApp: ...


class WorkflowDescriptionUseCase(Protocol):
    """Application use case contract consumed by access gateways for workflow inspection."""

    def describe(self, app: AgentApp, workflow_id: str | None = None) -> WorkflowDefinition: ...


class RuntimeExecutionUseCase(Protocol):
    """Application use case contract consumed by access gateways for runtime execution."""

    def run_manifest(
        self,
        manifest: AgentAppManifest,
        user_input: str,
        workflow_id: str | None = None,
        session_id: str | None = None,
    ) -> ExecutionResult: ...

    def run_app(
        self,
        app: AgentApp,
        user_input: str,
        workflow_id: str | None = None,
        session_id: str | None = None,
    ) -> ExecutionResult: ...


class SessionInspectionUseCase(Protocol):
    """Application use case contract for session inspection and replay entrypoints."""

    def get_session(self, session_id: str) -> AgentSession | None: ...


class MemoryInspectionUseCase(Protocol):
    """Application use case contract for memory recall and explainability queries."""

    def recall(self, query: RecallQuery) -> RecallBundle: ...


class CapabilityCatalogUseCase(Protocol):
    """Application use case contract for capability catalog exposure."""

    def list_capabilities(self, app_id: str | None = None) -> tuple[CapabilityDescriptor, ...]: ...


class PlatformHealthUseCase(Protocol):
    """Application use case contract for health and readiness checks."""

    def check(self) -> Mapping[str, Any]: ...
