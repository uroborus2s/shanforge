from __future__ import annotations

from dataclasses import dataclass

from access.ports.application_use_cases import WorkflowDescriptionUseCase
from domain.agent_app.models import AgentApp
from domain.workflow.models import WorkflowDefinition


@dataclass(slots=True)
class WorkflowAPI:
    """Thin API facade around workflow selection."""

    service: WorkflowDescriptionUseCase

    def describe(self, app: AgentApp, workflow_id: str | None = None) -> WorkflowDefinition:
        return self.service.resolve(app, workflow_id)
