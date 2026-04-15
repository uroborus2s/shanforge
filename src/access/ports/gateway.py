from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol

from domain.gateway.models import GatewayResult, InboundRequest


class GatewayPort(Protocol):
    """Access-owned gateway binding contract."""

    def bind(self, raw_request: Mapping[str, Any]) -> InboundRequest: ...

    def emit(self, result: GatewayResult) -> Mapping[str, Any]: ...
