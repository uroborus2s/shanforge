from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from domain.memory.models import MemoryCandidate, MemoryKind, MemoryScope, MemoryStatus


@dataclass(slots=True, frozen=True)
class MemoryPromotionPolicy:
    """Configurable promotion rules for candidate acceptance and drafting."""

    default_min_confidence: float = 0.6
    min_confidence_by_kind: Mapping[MemoryKind, float] = field(default_factory=dict)
    draft_kinds: tuple[MemoryKind, ...] = (MemoryKind.PROCEDURAL, MemoryKind.REFLECTIVE)
    allowed_scopes_by_kind: Mapping[MemoryKind, tuple[MemoryScope, ...]] = field(
        default_factory=dict
    )

    def evaluate(self, candidate: MemoryCandidate) -> tuple[MemoryStatus, str]:
        allowed_scopes = self.allowed_scopes_by_kind.get(candidate.kind)
        if allowed_scopes is not None and candidate.scope not in allowed_scopes:
            return (
                MemoryStatus.REJECTED,
                (
                    f"Scope '{candidate.scope.value}' is not allowed "
                    f"for {candidate.kind.value} memory."
                ),
            )

        threshold = self.min_confidence_by_kind.get(candidate.kind, self.default_min_confidence)
        if candidate.confidence < threshold:
            return (
                MemoryStatus.REJECTED,
                (
                    f"Candidate confidence {candidate.confidence:.2f} is below the "
                    f"{candidate.kind.value} threshold {threshold:.2f}."
                ),
            )

        if candidate.kind in self.draft_kinds:
            return (
                MemoryStatus.DRAFT,
                (
                    f"{candidate.kind.value.capitalize()} memory remains draft "
                    "until additional review."
                ),
            )

        return (
            MemoryStatus.ACCEPTED,
            "Candidate satisfied configurable promotion policy.",
        )
