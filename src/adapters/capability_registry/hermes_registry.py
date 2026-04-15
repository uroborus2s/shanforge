from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from adapters.hermes.bridge import HermesBridgeConfig
from domain.capability.models import CapabilityResult
from domain.session.models import AgentSession
from domain.workflow.steps import WorkflowStep
from runtime.ports.capability_registry import CapabilityRegistryPort


@dataclass(slots=True)
class HermesCapabilityRegistryAdapter:
    """Scaffold adapter that will route capability execution through Hermes' tool registry."""

    fallback: CapabilityRegistryPort
    bridge: HermesBridgeConfig

    def bridge_ready(self) -> bool:
        return self.bridge.has_modules("tools/registry.py", "model_tools.py")

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
