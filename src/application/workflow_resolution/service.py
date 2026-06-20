from __future__ import annotations

from dataclasses import dataclass

from application.ports.domain_services import WorkflowDomainService
from domain.agent_app.models import AgentApp
from domain.workflow.models import WorkflowDefinition


@dataclass(slots=True)
class WorkflowService:
    """Thin application facade over the workflow domain service."""

    domain_service: WorkflowDomainService

    def resolve(self, app: AgentApp, workflow_id: str | None = None) -> WorkflowDefinition:
        return self.domain_service.resolve_workflow(app, workflow_id)
