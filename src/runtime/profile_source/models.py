from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class ResolvedProfile:
    """Normalized profile resolution result."""

    profile_id: str
    label: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
