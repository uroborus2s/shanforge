from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class SessionArchiveHit:
    """Search hit returned by session archive queries."""

    session_id: str
    summary: str
    profile_id: str | None = None
    score: float | None = None
    created_at: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class SessionTranscriptSlice:
    """Transcript slice returned by session replay queries."""

    session_id: str
    cursor: str | None = None
    events: tuple[dict[str, Any], ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class SessionAssemblyExplanation:
    """Assembly explanation returned for one session."""

    session_id: str
    profile_id: str | None = None
    workspace_root: str | None = None
    sources: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
