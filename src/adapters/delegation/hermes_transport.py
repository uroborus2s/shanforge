from __future__ import annotations

from dataclasses import dataclass

from adapters.hermes.bridge import HermesBridgeConfig
from domain.delegation.models import (
    DelegationPlan,
    DelegationResult,
    DelegationTask,
    DelegationTicket,
)
from domain.session.models import AgentSession
from domain.workflow.steps import WorkflowStep
from runtime.ports.delegation_transport import DelegationTransportPort


@dataclass(slots=True)
class HermesDelegationTransportAdapter:
    """Scaffold adapter that will route delegation to Hermes while preserving current behavior."""

    fallback: DelegationTransportPort
    bridge: HermesBridgeConfig

    def bridge_ready(self) -> bool:
        return self.bridge.has_module("tools/delegate_tool.py")

    def plan(self, step: WorkflowStep, session: AgentSession) -> DelegationPlan:
        return self.fallback.plan(step=step, session=session)

    def dispatch(self, task: DelegationTask) -> DelegationTicket:
        return self.fallback.dispatch(task)

    def collect(self, ticket: DelegationTicket) -> DelegationResult:
        return self.fallback.collect(ticket)
