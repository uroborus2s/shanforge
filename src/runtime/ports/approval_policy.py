from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from domain.approval.models import ApprovalDecision
from domain.workflow.steps import WorkflowStep

if TYPE_CHECKING:
    from domain.capability.models import CapabilityDescriptor
    from domain.session.models import AgentSession


class ApprovalPolicyPort(Protocol):
    """Runtime-owned approval evaluation contract."""

    def evaluate(
        self,
        step: WorkflowStep,
        session: AgentSession | None = None,
        capability: CapabilityDescriptor | None = None,
    ) -> ApprovalDecision: ...
