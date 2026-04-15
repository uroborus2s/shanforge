from __future__ import annotations

from dataclasses import dataclass, field

from domain.approval.models import SandboxDecision
from domain.workflow.steps import WorkflowStep
from runtime.ports.sandbox_policy import SandboxPolicyPort


@dataclass(slots=True)
class SandboxGate(SandboxPolicyPort):
    """Simple writeset sandbox for the scaffold runtime."""

    allowed_prefixes: tuple[str, ...] = field(default_factory=tuple)

    def evaluate(
        self,
        step: WorkflowStep,
        writeset: tuple[str, ...],
        workspace_root: str | None = None,
    ) -> SandboxDecision:
        if not writeset or not self.allowed_prefixes:
            return SandboxDecision(allowed=True, reason="No sandbox restriction matched this step.")
        denied = [item for item in writeset if not item.startswith(self.allowed_prefixes)]
        if denied:
            return SandboxDecision(
                allowed=False,
                reason=f"Writeset {denied} is outside the allowed sandbox prefixes.",
                denied_writeset=tuple(denied),
            )
        return SandboxDecision(
            allowed=True,
            reason="Writeset is within the allowed sandbox prefixes.",
        )
