from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class FileReadResult:
    """Normalized text resource returned by the file access package."""

    path: str
    content: str
    exists: bool = True
    media_type: str = "text/plain"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class FileWritePlan:
    """Governed write plan generated before file mutation happens."""

    path: str
    content: str
    mode: str = "overwrite"
    reason: str | None = None
    requires_approval: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class PathMatch:
    """One matched path returned by workspace listing or searching."""

    path: str
    is_dir: bool = False
    score: float | None = None


@dataclass(slots=True, frozen=True)
class WorkspaceSnapshot:
    """Snapshot returned by file and workspace discovery operations."""

    root: str
    cwd: str | None = None
    matches: tuple[PathMatch, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
