from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from domain.capability.models import CapabilityResult
from domain.session.models import AgentSession
from domain.workflow.steps import WorkflowStep
from runtime.ports.capability_registry import CapabilityRegistryPort
from settings.hermes.bridge import HermesBridgeConfig


@dataclass(slots=True)
class HermesCapabilityRegistryAdapter:
    """Scaffold adapter that will route capability execution through Hermes' tool registry."""

    REQUIRED_MODULES = ("tools/registry.py", "model_tools.py")

    fallback: CapabilityRegistryPort
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

    def invoke(
        self,
        capability_id: str,
        session: AgentSession,
        step: WorkflowStep,
        payload: dict[str, Any],
    ) -> CapabilityResult:
        return self.fallback.invoke(
            capability_id=capability_id,
            session=session,
            step=step,
            payload=payload,
        )
