from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class BrowserSessionHandle:
    """Handle returned when one browser session is opened."""

    session_token: str
    current_url: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class BrowserObservation:
    """Observation returned by browser inspection and capture operations."""

    session_token: str
    kind: str
    value: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class BrowserActionReceipt:
    """Receipt returned by browser state-changing operations."""

    session_token: str
    action: str
    status: str = "pending"
    metadata: dict[str, Any] = field(default_factory=dict)
