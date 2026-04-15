from __future__ import annotations

import copy
from dataclasses import dataclass, field

from domain.session.models import AgentSession, SessionEvent


@dataclass(slots=True)
class InMemorySessionStore:
    """Simple in-memory session store for scaffold and tests."""

    sessions: dict[str, AgentSession] = field(default_factory=dict)
    events_by_session: dict[str, list[SessionEvent]] = field(default_factory=dict)

    def save(self, session: AgentSession) -> None:
        self.sessions[session.id] = copy.deepcopy(session)

    def load(self, session_id: str) -> AgentSession | None:
        session = self.sessions.get(session_id)
        return copy.deepcopy(session) if session is not None else None

    def save_session(self, session: AgentSession) -> None:
        self.save(session)

    def load_session(self, session_id: str) -> AgentSession | None:
        return self.load(session_id)

    def append_event(self, session_id: str, event: SessionEvent) -> None:
        self.events_by_session.setdefault(session_id, []).append(copy.deepcopy(event))

    def list_events(self, session_id: str) -> tuple[SessionEvent, ...]:
        return tuple(copy.deepcopy(self.events_by_session.get(session_id, ())))
