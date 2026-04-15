from __future__ import annotations

from dataclasses import dataclass

from domain.agent_app.models import AgentApp
from domain.workflow.models import WorkflowDefinition
from domain.workflow.state import WorkflowRunState


@dataclass(slots=True)
class DefaultWorkflowDomainService:
    """Business-domain logic for workflow selection and runtime state creation."""

    def resolve_workflow(
        self,
        app: AgentApp,
        workflow_id: str | None = None,
    ) -> WorkflowDefinition:
        return app.resolve_workflow(workflow_id)

    def open_run_state(self, workflow: WorkflowDefinition) -> WorkflowRunState:
        return WorkflowRunState(workflow_id=workflow.id)
