from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from settings.session.archive import InMemorySearchIndexProvider as ArchiveSearchIndexProvider


@dataclass(slots=True)
class EmptySearchIndexProvider:
    """Skeleton search index until a concrete backend is selected in composition."""

    def search(
        self,
        namespace: str,
        query_text: str,
        limit: int = 20,
        filters: Mapping[str, Any] | None = None,
    ) -> tuple[Mapping[str, Any], ...]:
        return ()


InMemorySearchIndexProvider = ArchiveSearchIndexProvider

__all__ = ["EmptySearchIndexProvider", "InMemorySearchIndexProvider"]
