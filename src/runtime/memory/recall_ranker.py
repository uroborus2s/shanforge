from __future__ import annotations

from dataclasses import dataclass

from domain.memory.assembly_models import MemoryProviderAugmentation, RecallPlan
from domain.memory.models import MemoryRecord
from domain.memory.ports import RecallRankerPort


@dataclass(slots=True)
class DefaultRecallRanker(RecallRankerPort):
    """Ranks scanned memory records without delegating sorting or budgets to the store."""

    def rank(
        self,
        plan: RecallPlan,
        records: tuple[MemoryRecord, ...],
        augmentation: MemoryProviderAugmentation | None = None,
    ) -> tuple[MemoryRecord, ...]:
        del augmentation
        grouped: dict[tuple[object, str], list[MemoryRecord]] = {
            scope_filter: [] for scope_filter in plan.scope_filters
        }
        for record in records:
            scope_filter = (record.scope, record.scope_key)
            if scope_filter not in grouped:
                continue
            grouped[scope_filter].append(record)

        for bucket in grouped.values():
            self._sort_bucket(bucket, plan.within_scope_order)

        selected: list[MemoryRecord] = []
        leftovers: list[tuple[int, MemoryRecord]] = []
        for index, scope_filter in enumerate(plan.scope_filters):
            scope, scope_key = scope_filter
            bucket = grouped.get(scope_filter, [])
            budget = max(0, int(plan.budget_for(scope, scope_key)))
            selected.extend(bucket[:budget])
            leftovers.extend((index, record) for record in bucket[budget:])

        if len(selected) < plan.total_limit and leftovers and plan.overflow_fill_enabled:
            self._sort_overflow(leftovers, plan.overflow_order)
            remaining = plan.total_limit - len(selected)
            selected.extend(record for _, record in leftovers[:remaining])

        return tuple(selected[: plan.total_limit])

    @classmethod
    def _sort_bucket(
        cls,
        bucket: list[MemoryRecord],
        order: tuple[str, ...],
    ) -> None:
        for token in reversed(order):
            field_name, reverse = cls._parse_sort_token(token)
            bucket.sort(
                key=lambda record: cls._record_field_value(record, field_name, 0),
                reverse=reverse,
            )

    @classmethod
    def _sort_overflow(
        cls,
        leftovers: list[tuple[int, MemoryRecord]],
        order: tuple[str, ...],
    ) -> None:
        for token in reversed(order):
            field_name, reverse = cls._parse_sort_token(token)
            leftovers.sort(
                key=lambda item: cls._record_field_value(item[1], field_name, item[0]),
                reverse=reverse,
            )

    @staticmethod
    def _parse_sort_token(token: str) -> tuple[str, bool]:
        field_name, _, direction = str(token).partition(":")
        normalized_field = field_name.strip() or "id"
        normalized_direction = direction.strip().lower() or "asc"
        return normalized_field, normalized_direction == "desc"

    @staticmethod
    def _record_field_value(
        record: MemoryRecord,
        field_name: str,
        scope_order: int,
    ) -> object:
        if field_name == "scope_order":
            return scope_order
        if field_name == "confidence":
            return record.confidence
        if field_name == "created_at":
            return record.created_at
        if field_name == "title":
            return record.title
        return record.id
