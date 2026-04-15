from __future__ import annotations

from typing import Any, Mapping, Protocol

from domain.workflow.models import WorkflowDefinition
from domain.workflow.steps import WorkflowStep


class WorkflowDefinitionCatalogPort(Protocol):
    """Foundation capability contract consumed by the workflow domain for workflow lookup."""

    def load_workflow(
        self,
        app_id: str,
        workflow_id: str,
    ) -> WorkflowDefinition | None: ...

    def list_workflows(self, app_id: str) -> tuple[WorkflowDefinition, ...]: ...


class WorkflowRuleEvaluationPort(Protocol):
    """Foundation capability contract consumed by the workflow domain for guard evaluation."""

    def evaluate_rule(self, rule_id: str, payload: Mapping[str, Any]) -> bool: ...


class WorkflowInstructionRenderPort(Protocol):
    """Foundation capability contract consumed by the workflow domain for step rendering."""

    def render_instruction(
        self,
        step: WorkflowStep,
        context: Mapping[str, Any],
    ) -> str: ...
