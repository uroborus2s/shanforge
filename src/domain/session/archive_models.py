from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class SessionArchiveHit:
    """Read model for one session archive search hit."""

    session_id: str
    summary: str
    profile_id: str | None = None
    score: float | None = None
    created_at: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class SessionTranscriptSlice:
    """Read model for one transcript slice returned by archive replay."""

    session_id: str
    cursor: str | None = None
    events: tuple[dict[str, Any], ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
