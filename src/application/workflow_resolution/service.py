from __future__ import annotations

from dataclasses import dataclass, field

from application.ports.domain_services import WorkflowDomainService
from domain.agent_app.models import AgentApp
from domain.workflow.models import WorkflowDefinition
from domain.workflow.service import DefaultWorkflowDomainService


@dataclass(slots=True)
class WorkflowService:
    """Thin application facade over the workflow domain service."""

    domain_service: WorkflowDomainService = field(default_factory=DefaultWorkflowDomainService)

    def resolve(self, app: AgentApp, workflow_id: str | None = None) -> WorkflowDefinition:
        return self.domain_service.resolve_workflow(app, workflow_id)
