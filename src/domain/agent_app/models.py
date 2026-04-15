from __future__ import annotations

from dataclasses import dataclass

from domain.agent_app.policies import ModelPolicy
from domain.workflow.models import WorkflowDefinition


@dataclass(slots=True, frozen=True)
class AgentAppMetadata:
    """Human-facing identity of a business Agent App."""

    id: str
    name: str
    domain: str
    description: str = ""


@dataclass(slots=True, frozen=True)
class AgentApp:
    """Compiled business app contract consumed by the runtime."""

    metadata: AgentAppMetadata
    workflows: dict[str, WorkflowDefinition]
    default_workflow_id: str
    required_capabilities: tuple[str, ...] = ()
    default_model_policy: ModelPolicy | None = None

    def resolve_workflow(self, workflow_id: str | None = None) -> WorkflowDefinition:
        selected_id = workflow_id or self.default_workflow_id
        try:
            return self.workflows[selected_id]
        except KeyError as exc:
            raise KeyError(
                f"Workflow '{selected_id}' is not registered in app '{self.metadata.id}'."
            ) from exc

