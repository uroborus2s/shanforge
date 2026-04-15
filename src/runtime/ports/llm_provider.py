from __future__ import annotations

from typing import Protocol

from domain.model.models import ModelRequest, ModelResponse


class LLMProviderPort(Protocol):
    """Provider adapter contract implemented by infrastructure drivers."""

    provider_name: str

    def generate(self, request: ModelRequest) -> ModelResponse: ...

