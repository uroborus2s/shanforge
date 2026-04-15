from __future__ import annotations

from typing import Protocol

from domain.memory.models import MemoryRecord, MemoryScope, RecallQuery


class MemoryStorePort(Protocol):
    """Runtime-owned persistence contract for promoted memory records."""

    def save(self, record: MemoryRecord) -> None: ...

    def list_by_scope(self, scope: MemoryScope, scope_key: str) -> tuple[MemoryRecord, ...]: ...

    def search(self, query: RecallQuery) -> tuple[MemoryRecord, ...]: ...
