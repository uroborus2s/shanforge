from __future__ import annotations

from typing import Protocol

from domain.agent_app.models import AgentApp
from domain.response.models import AgentResponse
from domain.session.models import AgentSession
from domain.workflow.models import WorkflowDefinition
from domain.workflow.state import WorkflowRunState


class AgentKernelPort(Protocol):
    """Application-owned execution kernel contract."""

    def run(
        self,
        app: AgentApp,
        workflow: WorkflowDefinition,
        session: AgentSession,
    ) -> tuple[AgentResponse, WorkflowRunState]: ...
