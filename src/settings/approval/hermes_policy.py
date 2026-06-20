from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from domain.approval.models import ApprovalDecision
from domain.workflow.steps import WorkflowStep
from runtime.ports.approval_policy import ApprovalPolicyPort
from settings.hermes.bridge import HermesBridgeConfig


@dataclass(slots=True)
class HermesApprovalPolicyAdapter:
    """Scaffold adapter that will route approval to Hermes while preserving current behavior."""

    REQUIRED_MODULES = ("tools/approval.py",)

    fallback: ApprovalPolicyPort
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

    def evaluate(
        self,
        step: WorkflowStep,
        session=None,
        capability=None,
    ) -> ApprovalDecision:
        return self.fallback.evaluate(step=step, session=session, capability=capability)
