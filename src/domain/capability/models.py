from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class CapabilityDescriptor:
    """Governed capability metadata used by the runtime."""

    id: str
    name: str
    description: str
    input_schema: dict[str, str] = field(default_factory=dict)
    output_schema: dict[str, str] = field(default_factory=dict)
    writeset: tuple[str, ...] = ()
    risk_level: str = "L0"


@dataclass(slots=True, frozen=True)
class CapabilityResult:
    """Structured output returned by one capability execution."""

    capability_id: str
    summary: str
    output: dict[str, Any] = field(default_factory=dict)

