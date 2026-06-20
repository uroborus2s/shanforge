from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class NullEmbeddingProvider:
    """Reserved skeleton provider for future embedding backends."""

    provider_name: str = "null-embedding"

    def embed(
        self,
        texts: tuple[str, ...],
        model: str | None = None,
    ) -> tuple[tuple[float, ...], ...]:
        raise NotImplementedError(
            "NullEmbeddingProvider is a settings-layer skeleton. "
            "Bind a real embedding backend before use."
        )
