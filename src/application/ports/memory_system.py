from __future__ import annotations

from typing import Any, Mapping, Protocol

from domain.agent_app.models import AgentApp
from domain.memory.models import DistillationResult, RecallBundle, RecallQuery
from domain.session.models import AgentSession
from domain.workflow.models import WorkflowDefinition


class MemorySystemPort(Protocol):
    """Application-owned memory subsystem facade."""

    def prepare_session(
        self,
        session: AgentSession,
        app: AgentApp,
        workflow: WorkflowDefinition,
    ) -> RecallBundle: ...

    def recall(self, query: RecallQuery) -> RecallBundle: ...

    def distill_session(self, session: AgentSession) -> DistillationResult: ...

    def explain_session_memory(self, session: AgentSession) -> Mapping[str, Any]: ...
