from __future__ import annotations

from typing import Protocol

from domain.memory.models import MemoryDistillationSample


class MemoryDatasetStorePort(Protocol):
    """Runtime-owned persistence contract for memory distillation samples."""

    def save_entry(self, entry: MemoryDistillationSample) -> None: ...

    def list_by_session(self, session_id: str) -> tuple[MemoryDistillationSample, ...]: ...
