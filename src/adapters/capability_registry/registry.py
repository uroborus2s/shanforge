from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from domain.capability.models import CapabilityDescriptor, CapabilityResult
from domain.session.models import AgentSession
from domain.workflow.steps import WorkflowStep

CapabilityHandler = Callable[[AgentSession, WorkflowStep, dict[str, Any]], CapabilityResult]


@dataclass(slots=True)
class InMemoryCapabilityRegistry:
    """Simple capability registry with optional local handlers."""

    descriptors: dict[str, CapabilityDescriptor] = field(default_factory=dict)
    handlers: dict[str, CapabilityHandler] = field(default_factory=dict)

    def register(
        self,
        descriptor: CapabilityDescriptor,
        handler: CapabilityHandler | None = None,
    ) -> None:
        self.descriptors[descriptor.id] = descriptor
        if handler is not None:
            self.handlers[descriptor.id] = handler

    def describe(self, capability_id: str) -> CapabilityDescriptor:
        return self.descriptors[capability_id]

    def invoke(
        self,
        capability_id: str,
        session: AgentSession,
        step: WorkflowStep,
        payload: dict[str, Any],
    ) -> CapabilityResult:
        descriptor = self.describe(capability_id)
        handler = self.handlers.get(capability_id)
        if handler is None:
            return CapabilityResult(
                capability_id=descriptor.id,
                summary=f"Capability '{descriptor.id}' is declared but has no runtime handler yet.",
                output={"declared": True, "implemented": False},
            )
        return handler(session, step, payload)

