from __future__ import annotations

from dataclasses import dataclass, field

from .steps import WorkflowStep


@dataclass(slots=True, frozen=True)
class WorkflowDefinition:
    """Declarative workflow definition attached to an Agent App."""

    id: str
    name: str
    description: str
    steps: tuple[WorkflowStep, ...]
    input_schema: dict[str, str] = field(default_factory=dict)
    output_schema: dict[str, str] = field(default_factory=dict)
    retry_budget: int = 0

