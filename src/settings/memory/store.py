from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from domain.memory.models import MemoryKind, MemoryRecord, MemoryScope, MemoryStatus, RecallQuery
from settings.shared.jsonl import JsonlStore, parse_datetime, serialize_record


def _rank_memory_records(records: list[MemoryRecord], limit: int) -> tuple[MemoryRecord, ...]:
    scope_rank = {
        MemoryScope.APP: 0,
        MemoryScope.PROJECT: 1,
        MemoryScope.USER: 2,
        MemoryScope.WORKSPACE: 3,
        MemoryScope.SESSION: 4,
    }
    records.sort(
        key=lambda record: (
            scope_rank.get(record.scope, 99),
            -record.confidence,
            record.created_at,
        )
    )
    return tuple(records[:limit])


def _deserialize_memory_record(payload: dict[str, object]) -> MemoryRecord:
    return MemoryRecord(
        id=str(payload["id"]),
        kind=MemoryKind(str(payload["kind"])),
        scope=MemoryScope(str(payload["scope"])),
        scope_key=str(payload["scope_key"]),
        title=str(payload["title"]),
        body=str(payload["body"]),
        status=MemoryStatus(str(payload["status"])),
        confidence=float(payload["confidence"]),
        supporting_refs=tuple(payload.get("supporting_refs", ())),
        metadata=dict(payload.get("metadata", {})),
        created_at=parse_datetime(str(payload["created_at"])),
    )


@dataclass(slots=True)
class InMemoryMemoryStore:
    """In-memory store used by scaffold tests and local runtime wiring."""

    records: list[MemoryRecord] = field(default_factory=list)

    def save(self, record: MemoryRecord) -> None:
        for index, existing in enumerate(self.records):
            if existing.id == record.id:
                self.records[index] = record
                break
        else:
            self.records.append(record)

    def list_by_scope(self, scope: MemoryScope, scope_key: str) -> tuple[MemoryRecord, ...]:
        return tuple(
            record
            for record in self.records
            if record.scope is scope and record.scope_key == scope_key
        )

    def scan_memory_records(
        self,
        scope_filters: tuple[tuple[MemoryScope, str], ...],
        allowed_statuses: tuple[MemoryStatus, ...],
    ) -> tuple[MemoryRecord, ...]:
        scope_filter_set = set(scope_filters)
        allowed_status_set = set(allowed_statuses)
        return tuple(
            record
            for record in self.records
            if (record.scope, record.scope_key) in scope_filter_set
            and record.status in allowed_status_set
        )

    def search(self, query: RecallQuery) -> tuple[MemoryRecord, ...]:
        filtered = list(self.scan_memory_records(query.scope_filters, query.allowed_statuses))
        return _rank_memory_records(filtered, query.limit)

    def save_memory_record(self, record: MemoryRecord) -> None:
        self.save(record)

    def query_memory_records(self, query: RecallQuery) -> tuple[MemoryRecord, ...]:
        return self.search(query)


class JsonlMemoryStore(JsonlStore):
    """JSONL-backed persistence adapter for memory records."""

    def __init__(self, root: str | Path) -> None:
        super().__init__(root=root, filename="memory-records.jsonl")

    def save(self, record: MemoryRecord) -> None:
        self.replace_or_append(record.id, serialize_record(record))

    def list_by_scope(self, scope: MemoryScope, scope_key: str) -> tuple[MemoryRecord, ...]:
        return tuple(
            record
            for record in self.read_all(_deserialize_memory_record)
            if record.scope is scope and record.scope_key == scope_key
        )

    def scan_memory_records(
        self,
        scope_filters: tuple[tuple[MemoryScope, str], ...],
        allowed_statuses: tuple[MemoryStatus, ...],
    ) -> tuple[MemoryRecord, ...]:
        scope_filter_set = set(scope_filters)
        allowed_status_set = set(allowed_statuses)
        return tuple(
            record
            for record in self.read_all(_deserialize_memory_record)
            if (record.scope, record.scope_key) in scope_filter_set
            and record.status in allowed_status_set
        )

    def search(self, query: RecallQuery) -> tuple[MemoryRecord, ...]:
        filtered = list(self.scan_memory_records(query.scope_filters, query.allowed_statuses))
        return _rank_memory_records(filtered, query.limit)

    def save_memory_record(self, record: MemoryRecord) -> None:
        self.save(record)

    def query_memory_records(self, query: RecallQuery) -> tuple[MemoryRecord, ...]:
        return self.search(query)
