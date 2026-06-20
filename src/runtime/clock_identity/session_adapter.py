from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from domain.session.ports import SessionClockPort, SessionIdentityPort
from runtime.clock_identity.service import ClockIdentityService


@dataclass(slots=True)
class SessionClockAdapter(SessionClockPort):
    """Adapts the clock_identity capability package to the session domain clock port."""

    service: ClockIdentityService

    def now(self) -> datetime:
        return self.service.now()


@dataclass(slots=True)
class SessionIdentityAdapter(SessionIdentityPort):
    """Adapts the clock_identity capability package to the session domain identity port."""

    service: ClockIdentityService

    def new_id(self, prefix: str) -> str:
        return self.service.new_id(prefix)
