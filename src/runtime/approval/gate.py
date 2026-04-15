from __future__ import annotations

from dataclasses import dataclass

from domain.approval.models import ApprovalDecision
from domain.workflow.steps import WorkflowStep
from runtime.ports.approval_policy import ApprovalPolicyPort


@dataclass(slots=True)
class ApprovalGate(ApprovalPolicyPort):
    """Centralized approval boundary for high-risk steps."""

    def evaluate(
        self,
        step: WorkflowStep,
        session=None,
        capability=None,
    ) -> ApprovalDecision:
        if step.requires_approval:
            return ApprovalDecision(
                approved=False,
                reason=f"Step '{step.id}' requires explicit approval before execution.",
            )
        return ApprovalDecision(
            approved=True,
            reason=f"Step '{step.id}' does not require approval.",
        )
