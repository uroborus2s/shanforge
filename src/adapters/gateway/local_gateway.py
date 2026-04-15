from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from domain.gateway.models import GatewayContext, GatewayResult, InboundRequest


@dataclass(slots=True)
class InMemoryGatewayAdapter:
    """Minimal gateway adapter used by tests and local access scaffolds."""

    channel: str

    def bind(self, raw_request: dict[str, Any]) -> InboundRequest:
        metadata = dict(raw_request.get("metadata", {}))
        session_id = str(raw_request.get("session_id") or f"{self.channel}-session-{uuid4()}")
        correlation_id = raw_request.get("correlation_id")
        return InboundRequest(
            context=GatewayContext(
                channel=self.channel,
                session_id=session_id,
                metadata=metadata,
                correlation_id=correlation_id,
            ),
            user_input=str(raw_request.get("user_input", "")),
            raw_request=dict(raw_request),
        )

    def emit(self, result: GatewayResult) -> dict[str, Any]:
        return {
            "channel": result.channel,
            "session_id": result.session_id,
            "summary": result.summary,
            "payload": dict(result.payload),
        }
