from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from domain.agent_app.policies import ModelPolicy


class StepKind(StrEnum):
    """The minimal execution primitives exposed by the platform kernel."""

    PROMPT = "prompt"
    CAPABILITY = "capability"


@dataclass(slots=True, frozen=True)
class WorkflowStep:
    """A single runtime step inside an Agent App workflow."""

    id: str
    name: str
    kind: StepKind
    instruction: str
    capability_id: str | None = None
    model_policy: ModelPolicy | None = None
    requires_approval: bool = False
    writeset: tuple[str, ...] = ()
    output_key: str | None = None

