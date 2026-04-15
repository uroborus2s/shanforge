from __future__ import annotations

from typing import Any, Mapping, Protocol

from domain.model.models import ModelRequest, ModelResponse


class ModelInvocationPort(Protocol):
    """Foundation capability contract consumed by the model domain for model invocation."""

    def invoke(self, request: ModelRequest) -> ModelResponse: ...


class ModelMetadataPort(Protocol):
    """Foundation capability contract consumed by the model domain for metadata lookup."""

    def get_metadata(self, provider: str, model: str) -> Mapping[str, Any]: ...


class EmbeddingGenerationPort(Protocol):
    """Foundation capability contract consumed by the model domain for embedding generation."""

    def embed(
        self,
        texts: tuple[str, ...],
        provider: str | None = None,
        model: str | None = None,
    ) -> tuple[tuple[float, ...], ...]: ...
