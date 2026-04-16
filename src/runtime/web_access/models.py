from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class WebSearchHit:
    """Normalized web search hit returned by the web access package."""

    url: str
    title: str
    snippet: str = ""
    rank: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class WebDocument:
    """Normalized web document returned by fetch and extract operations."""

    url: str
    title: str | None = None
    content: str = ""
    extracted_text: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
