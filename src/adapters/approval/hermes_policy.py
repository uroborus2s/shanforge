from __future__ import annotations

from dataclasses import dataclass

from adapters.hermes.bridge import HermesBridgeConfig
from domain.approval.models import ApprovalDecision
from domain.workflow.steps import WorkflowStep
from runtime.ports.approval_policy import ApprovalPolicyPort


@dataclass(slots=True)
class HermesApprovalPolicyAdapter:
    """Scaffold adapter that will route approval to Hermes while preserving current behavior."""

    fallback: ApprovalPolicyPort
    bridge: HermesBridgeConfig

    def bridge_ready(self) -> bool:
        return self.bridge.has_module("tools/approval.py")

    def evaluate(
        self,
        step: WorkflowStep,
        session=None,
        capability=None,
    ) -> ApprovalDecision:
        return self.fallback.evaluate(step=step, session=session, capability=capability)
