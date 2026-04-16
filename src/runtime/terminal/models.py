from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class CommandExecutionRequest:
    """Governed command request handled by the terminal package."""

    argv: tuple[str, ...]
    cwd: str | None = None
    timeout_seconds: int | None = None
    environment: dict[str, str] = field(default_factory=dict)
    capture_output: bool = True


@dataclass(slots=True, frozen=True)
class CommandExecutionResult:
    """Normalized command result emitted by the terminal package."""

    argv: tuple[str, ...]
    cwd: str | None
    exit_code: int | None = None
    stdout: str = ""
    stderr: str = ""
    duration_ms: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class WriteSetAudit:
    """Structured write-set summary derived from one command execution."""

    touched_paths: tuple[str, ...] = ()
    created_paths: tuple[str, ...] = ()
    deleted_paths: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
