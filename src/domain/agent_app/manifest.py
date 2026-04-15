from __future__ import annotations

from dataclasses import dataclass

from .models import AgentApp, AgentAppMetadata
from .policies import ModelPolicy
from domain.workflow.models import WorkflowDefinition


@dataclass(slots=True, frozen=True)
class AgentAppManifest:
    """Source manifest used by business teams to declare an Agent App."""

    metadata: AgentAppMetadata
    workflows: tuple[WorkflowDefinition, ...]
    default_workflow_id: str
    required_capabilities: tuple[str, ...] = ()
    default_model_policy: ModelPolicy | None = None

    def to_agent_app(self) -> AgentApp:
        return AgentApp(
            metadata=self.metadata,
            workflows={workflow.id: workflow for workflow in self.workflows},
            default_workflow_id=self.default_workflow_id,
            required_capabilities=self.required_capabilities,
            default_model_policy=self.default_model_policy,
        )

