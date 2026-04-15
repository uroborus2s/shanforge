from __future__ import annotations

from dataclasses import dataclass

from application.workflow_resolution.service import WorkflowService
from domain.agent_app.models import AgentApp
from domain.workflow.models import WorkflowDefinition


@dataclass(slots=True)
class WorkflowAPI:
    """Thin API facade around workflow selection."""

    service: WorkflowService

    def describe(self, app: AgentApp, workflow_id: str | None = None) -> WorkflowDefinition:
        return self.service.resolve(app, workflow_id)

