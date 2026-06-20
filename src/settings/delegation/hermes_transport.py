from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from domain.delegation.models import (
    DelegationPlan,
    DelegationResult,
    DelegationTask,
    DelegationTicket,
)
from domain.session.models import AgentSession
from domain.workflow.steps import WorkflowStep
from runtime.ports.delegation_transport import DelegationTransportPort
from settings.hermes.bridge import HermesBridgeConfig


@dataclass(slots=True)
class HermesDelegationTransportAdapter:
    """Scaffold adapter that will route delegation to Hermes while preserving current behavior."""

    REQUIRED_MODULES = ("tools/delegate_tool.py",)

    fallback: DelegationTransportPort
    bridge: HermesBridgeConfig

    def bridge_ready(self) -> bool:
        return self.bridge.has_modules(*self.REQUIRED_MODULES)

    def contract_metadata(self) -> dict[str, Any]:
        return {
            "bridge_kind": "hermes",
            "bridge_modules": self.REQUIRED_MODULES,
            "bridge_repo_root": str(self.bridge.repo_root),
            "contract_ready": self.bridge_ready(),
            "fallback_class": self.fallback.__class__.__name__,
        }

    def plan(self, step: WorkflowStep, session: AgentSession) -> DelegationPlan:
        return self.fallback.plan(step=step, session=session)

    def dispatch(self, task: DelegationTask) -> DelegationTicket:
        return self.fallback.dispatch(task)

    def collect(self, ticket: DelegationTicket) -> DelegationResult:
        return self.fallback.collect(ticket)
