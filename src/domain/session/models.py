from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any
from uuid import uuid4

if TYPE_CHECKING:
    from domain.memory.models import MemoryCandidate, MemoryRecord, PromotionDecision


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(slots=True, frozen=True)
class SessionArtifact:
    """Runtime evidence emitted by the platform."""

    kind: str
    uri: str
    summary: str
    id: str = field(default_factory=lambda: f"artifact-{uuid4()}")
    created_at: datetime = field(default_factory=_utcnow)


@dataclass(slots=True, frozen=True)
class SessionEvent:
    """Structured event appended to a session timeline."""

    type: str
    summary: str
    payload: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: f"event-{uuid4()}")
    created_at: datetime = field(default_factory=_utcnow)


@dataclass(slots=True)
class AgentSession:
    """A single execution session for one workflow invocation."""

    id: str
    app_id: str
    workflow_id: str
    user_input: str
    context: dict[str, Any] = field(default_factory=dict)
    events: list[SessionEvent] = field(default_factory=list)
    artifacts: list[SessionArtifact] = field(default_factory=list)
    recalled_memories: list["MemoryRecord"] = field(default_factory=list)
    memory_candidates: list["MemoryCandidate"] = field(default_factory=list)
    promotion_decisions: list["PromotionDecision"] = field(default_factory=list)
    status: str = "pending"

    def add_event(
        self,
        event_type: str,
        summary: str,
        payload: dict[str, Any] | None = None,
    ) -> None:
        self.events.append(SessionEvent(type=event_type, summary=summary, payload=payload or {}))

    def add_artifact(self, artifact: SessionArtifact) -> None:
        self.artifacts.append(artifact)
