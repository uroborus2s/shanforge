from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ReasoningEffort(StrEnum):
    """Normalized reasoning budget exposed to business workflows."""

    MINIMAL = "minimal"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(slots=True, frozen=True)
class ModelFallback:
    """Fallback target used when the primary provider or model is unavailable."""

    provider: str
    model: str


@dataclass(slots=True, frozen=True)
class ModelPolicy:
    """Declarative model-selection policy consumed by the runtime."""

    provider: str
    model: str
    reasoning_effort: ReasoningEffort = ReasoningEffort.MEDIUM
    temperature: float = 0.2
    max_output_tokens: int = 2048
    fallback_chain: tuple[ModelFallback, ...] = ()
    metadata: dict[str, str] = field(default_factory=dict)

