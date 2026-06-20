from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

from runtime.ports.execution_backends import ClockProviderPort, IdGeneratorProviderPort


@dataclass(slots=True, frozen=True)
class SystemClockProvider(ClockProviderPort):
    """System UTC clock provider for runtime services."""

    def now(self) -> datetime:
        return datetime.now(timezone.utc)


@dataclass(slots=True, frozen=True)
class UuidIdGeneratorProvider(IdGeneratorProviderPort):
    """UUID-backed identifier generator for runtime services."""

    def new_id(self, prefix: str) -> str:
        normalized_prefix = prefix.strip() or "id"
        return f"{normalized_prefix}-{uuid4()}"
