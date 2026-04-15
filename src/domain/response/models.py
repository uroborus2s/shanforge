from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from domain.model.models import TokenUsage
from domain.session.models import SessionArtifact


@dataclass(slots=True, frozen=True)
class ToolCallTrace:
    """Audit entry for one capability invocation."""

    tool_name: str
    status: str
    summary: str


@dataclass(slots=True, frozen=True)
class AgentResponse:
    """Platform-normalized response returned to adapters."""

    summary: str
    raw_output: str
    structured_output: dict[str, Any] = field(default_factory=dict)
    tool_calls: tuple[ToolCallTrace, ...] = ()
    evidence: tuple[SessionArtifact, ...] = ()
    next_actions: tuple[str, ...] = ()
    usage: TokenUsage | None = None

    @classmethod
    def empty(cls) -> "AgentResponse":
        return cls(summary="", raw_output="")

