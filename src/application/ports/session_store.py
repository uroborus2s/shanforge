from __future__ import annotations

from typing import Protocol

from domain.session.models import AgentSession


class SessionStorePort(Protocol):
    """Application-owned persistence contract for runtime sessions."""

    def save(self, session: AgentSession) -> None: ...

    def load(self, session_id: str) -> AgentSession | None: ...
