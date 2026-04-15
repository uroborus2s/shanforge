from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from access.ports.gateway import GatewayPort
from adapters.hermes.bridge import HermesBridgeConfig
from domain.gateway.models import GatewayResult, InboundRequest


@dataclass(slots=True)
class HermesGatewayAdapter:
    """Scaffold adapter that will route gateway binding through Hermes session/gateway modules."""

    fallback: GatewayPort
    bridge: HermesBridgeConfig

    def bridge_ready(self) -> bool:
        return self.bridge.has_modules(
            "gateway/platforms/base.py",
            "gateway/session.py",
            "gateway/session_context.py",
        )

    def bind(self, raw_request: dict[str, Any]) -> InboundRequest:
        return self.fallback.bind(raw_request)

    def emit(self, result: GatewayResult) -> dict[str, Any]:
        return dict(self.fallback.emit(result))
