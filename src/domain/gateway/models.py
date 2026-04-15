from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class GatewayContext:
    """Normalized gateway session context."""

    channel: str
    session_id: str
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: str | None = None


@dataclass(slots=True, frozen=True)
class InboundRequest:
    """Normalized inbound request bound by an access adapter."""

    context: GatewayContext
    user_input: str
    raw_request: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class GatewayResult:
    """Normalized outbound result emitted by a gateway adapter."""

    channel: str
    session_id: str
    summary: str
    payload: dict[str, Any] = field(default_factory=dict)
