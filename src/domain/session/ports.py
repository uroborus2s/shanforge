from __future__ import annotations

from datetime import datetime
from typing import Protocol

from domain.session.models import AgentSession, SessionArtifact, SessionEvent


class SessionLedgerPort(Protocol):
    """Foundation capability contract consumed by the session domain for ledger persistence."""

    def save_session(self, session: AgentSession) -> None: ...

    def load_session(self, session_id: str) -> AgentSession | None: ...

    def append_event(self, session_id: str, event: SessionEvent) -> None: ...

    def list_events(self, session_id: str) -> tuple[SessionEvent, ...]: ...


class SessionArtifactStorePort(Protocol):
    """Foundation capability contract consumed by the session domain for artifact persistence."""

    def save_artifact(self, session_id: str, artifact: SessionArtifact) -> None: ...

    def load_artifact(self, artifact_id: str) -> SessionArtifact | None: ...

    def list_artifacts(self, session_id: str) -> tuple[SessionArtifact, ...]: ...


class SessionClockPort(Protocol):
    """Foundation capability contract consumed by the session domain for current time."""

    def now(self) -> datetime: ...


class SessionIdentityPort(Protocol):
    """Foundation capability contract consumed by the session domain for stable identifiers."""

    def new_id(self, prefix: str) -> str: ...
