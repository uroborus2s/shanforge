from __future__ import annotations

from typing import Protocol


class EmbeddingProviderPort(Protocol):
    """Settings-provider contract owned by the basic capability layer for embeddings."""

    provider_name: str

    def embed(self, texts: tuple[str, ...], model: str | None = None) -> tuple[tuple[float, ...], ...]: ...
