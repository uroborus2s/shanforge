from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class RuleBundle:
    """Normalized workspace rule bundle."""

    workspace_root: str | None
    profile_id: str | None
    values: dict[str, Any] = field(default_factory=dict)
