from __future__ import annotations

from dataclasses import dataclass

from domain.delegation.models import (
    DelegationMode,
    DelegationPlan,
    DelegationResult,
    DelegationStatus,
    DelegationTask,
    DelegationTicket,
)
from domain.session.models import AgentSession
from domain.workflow.steps import WorkflowStep
from runtime.ports.delegation_transport import DelegationTransportPort


@dataclass(slots=True)
class DelegationCoordinator(DelegationTransportPort):
    """Chooses where each workflow step should run."""

    def plan(self, step: WorkflowStep, session: AgentSession) -> DelegationPlan:
        return DelegationPlan(
            mode=DelegationMode.LOCAL,
            reason=f"Step '{step.id}' runs in the local orchestrator by default.",
        )

    def plan_for(self, step: WorkflowStep, session: AgentSession) -> DelegationPlan:
        return self.plan(step=step, session=session)

    def dispatch(self, task: DelegationTask) -> DelegationTicket:
        return DelegationTicket(task_id=task.id, backend="local")

    def collect(self, ticket: DelegationTicket) -> DelegationResult:
        return DelegationResult(
            task_id=ticket.task_id,
            status=DelegationStatus.COMPLETED,
            summary="Delegation task completed in the local coordinator scaffold.",
        )
