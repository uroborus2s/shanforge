from __future__ import annotations

from typing import Any, Protocol

from domain.capability.models import CapabilityResult
from domain.session.models import AgentSession
from domain.workflow.steps import WorkflowStep


class CapabilityRegistryPort(Protocol):
    """Runtime-owned capability invocation contract."""

    def invoke(
        self,
        capability_id: str,
        session: AgentSession,
        step: WorkflowStep,
        payload: dict[str, Any],
    ) -> CapabilityResult: ...
