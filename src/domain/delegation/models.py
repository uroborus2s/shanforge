from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any
from uuid import uuid4


class DelegationMode(StrEnum):
    """Execution ownership for one workflow step."""

    LOCAL = "local"
    SUBAGENT = "subagent"


class DelegationStatus(StrEnum):
    """Lifecycle state for delegated work."""

    SUBMITTED = "submitted"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(slots=True, frozen=True)
class DelegationPlan:
    """Delegation decision for a workflow step."""

    mode: DelegationMode
    reason: str


@dataclass(slots=True, frozen=True)
class DelegationTask:
    """A unit of delegated execution."""

    step_id: str
    session_id: str
    mode: DelegationMode
    payload: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: f"delegation-task-{uuid4()}")


@dataclass(slots=True, frozen=True)
class DelegationTicket:
    """Handle used to collect delegation results later."""

    task_id: str
    backend: str
    status: DelegationStatus = DelegationStatus.SUBMITTED


@dataclass(slots=True, frozen=True)
class DelegationResult:
    """Normalized outcome of delegated execution."""

    task_id: str
    status: DelegationStatus
    summary: str
    output: dict[str, Any] = field(default_factory=dict)
