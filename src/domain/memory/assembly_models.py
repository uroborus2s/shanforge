from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from domain.memory.models import MemoryScope, MemoryStatus, RecallBundle, RecallQuery


@dataclass(slots=True, frozen=True)
class RecallPlan:
    """Read model describing how one recall pass is budgeted and ranked."""

    scope_filters: tuple[tuple[MemoryScope, str], ...]
    allowed_statuses: tuple[MemoryStatus, ...] = (MemoryStatus.ACCEPTED,)
    total_limit: int = 8
    scope_budgets: dict[str, int] = field(default_factory=dict)
    ranking_strategy: str = "scope_confidence_recency"
    within_scope_order: tuple[str, ...] = ("confidence:desc", "created_at:asc", "id:asc")
    overflow_order: tuple[str, ...] = (
        "scope_order:asc",
        "confidence:desc",
        "created_at:asc",
        "id:asc",
    )
    overflow_fill_enabled: bool = True
    include_external_augmentation: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def budget_for(self, scope: MemoryScope, scope_key: str) -> int:
        return int(self.scope_budgets.get(f"{scope.value}:{scope_key}", 0))

    def to_mapping(self) -> dict[str, Any]:
        return {
            "scope_filters": tuple(
                (scope.value, scope_key) for scope, scope_key in self.scope_filters
            ),
            "allowed_statuses": tuple(status.value for status in self.allowed_statuses),
            "total_limit": self.total_limit,
            "scope_budgets": dict(self.scope_budgets),
            "ranking_strategy": self.ranking_strategy,
            "within_scope_order": tuple(self.within_scope_order),
            "overflow_order": tuple(self.overflow_order),
            "overflow_fill_enabled": self.overflow_fill_enabled,
            "include_external_augmentation": self.include_external_augmentation,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "RecallPlan":
        return cls(
            scope_filters=tuple(
                (MemoryScope(str(scope)), str(scope_key))
                for scope, scope_key in payload.get("scope_filters", ())
            ),
            allowed_statuses=tuple(
                MemoryStatus(str(status)) for status in payload.get("allowed_statuses", ())
            )
            or (MemoryStatus.ACCEPTED,),
            total_limit=int(payload.get("total_limit", 8) or 8),
            scope_budgets={
                str(key): int(value)
                for key, value in dict(payload.get("scope_budgets") or {}).items()
            },
            ranking_strategy=str(payload.get("ranking_strategy") or "scope_confidence_recency"),
            within_scope_order=tuple(
                str(item)
                for item in payload.get(
                    "within_scope_order",
                    ("confidence:desc", "created_at:asc", "id:asc"),
                )
            ),
            overflow_order=tuple(
                str(item)
                for item in payload.get(
                    "overflow_order",
                    ("scope_order:asc", "confidence:desc", "created_at:asc", "id:asc"),
                )
            ),
            overflow_fill_enabled=bool(payload.get("overflow_fill_enabled", True)),
            include_external_augmentation=bool(payload.get("include_external_augmentation", False)),
            metadata=dict(payload.get("metadata") or {}),
        )


@dataclass(slots=True, frozen=True)
class MemoryProviderBinding:
    """Read model describing one external memory augmentation provider binding."""

    provider_id: str
    source: str | None = None
    namespace: str | None = None
    mode: str = "augmentation"
    writable: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_mapping(self) -> dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "source": self.source,
            "namespace": self.namespace,
            "mode": self.mode,
            "writable": self.writable,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "MemoryProviderBinding":
        return cls(
            provider_id=str(
                payload.get("provider_id") or payload.get("binding_id") or payload.get("name") or ""
            ),
            source=str(payload.get("source") or "") or None,
            namespace=str(payload.get("namespace") or "") or None,
            mode=str(payload.get("mode") or "augmentation"),
            writable=bool(payload.get("writable", False)),
            metadata=dict(payload.get("metadata") or {}),
        )


@dataclass(slots=True, frozen=True)
class MemoryProviderAugmentation:
    """Runtime projection of one provider-prefetch result."""

    binding: MemoryProviderBinding
    recall_block: str | None = None
    diagnostics: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class RecallScopeBreakdown:
    """Explainability projection for one recall scope budget."""

    scope: str
    scope_key: str
    budget: int
    scanned_record_ids: tuple[str, ...] = ()
    selected_record_ids: tuple[str, ...] = ()
    overflow_record_ids: tuple[str, ...] = ()


@dataclass(slots=True, frozen=True)
class RecallRecordRanking:
    """Explainability projection for one scanned record in preview order."""

    record_id: str
    scope: str
    scope_key: str
    confidence: float
    rank_position: int
    selected: bool
    selection_reason: str
    selected_order: int | None = None


@dataclass(slots=True, frozen=True)
class RecallAugmentationPreview:
    """Explainability projection for one augmentation source in preview mode."""

    provider_id: str
    source: str | None = None
    namespace: str | None = None
    mode: str = "augmentation"
    writable: bool = False
    recall_block_source: str | None = None
    recall_block_present: bool = False
    diagnostics: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class RecallPreview:
    """Read model describing one recall preview for diagnostics and governance."""

    session_id: str
    query: RecallQuery
    plan: RecallPlan
    bundle: RecallBundle
    scope_breakdowns: tuple[RecallScopeBreakdown, ...] = ()
    record_rankings: tuple[RecallRecordRanking, ...] = ()
    augmentation_preview: RecallAugmentationPreview | None = None
    memory_provider_binding: MemoryProviderBinding | None = None
    external_recall_block: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
