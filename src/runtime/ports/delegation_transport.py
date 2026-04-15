from __future__ import annotations

from typing import Protocol

from domain.delegation.models import (
    DelegationPlan,
    DelegationResult,
    DelegationTask,
    DelegationTicket,
)
from domain.session.models import AgentSession
from domain.workflow.steps import WorkflowStep


class DelegationTransportPort(Protocol):
    """Runtime-owned delegation planning and transport contract."""

    def plan(self, step: WorkflowStep, session: AgentSession) -> DelegationPlan: ...

    def dispatch(self, task: DelegationTask) -> DelegationTicket: ...

    def collect(self, ticket: DelegationTicket) -> DelegationResult: ...
