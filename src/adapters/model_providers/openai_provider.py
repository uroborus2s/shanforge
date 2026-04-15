from __future__ import annotations

from dataclasses import dataclass

from domain.model.models import ModelRequest, ModelResponse


@dataclass(slots=True)
class OpenAIProvider:
    """Reserved adapter for a future OpenAI SDK integration."""

    provider_name: str = "openai"

    def generate(self, request: ModelRequest) -> ModelResponse:
        raise NotImplementedError(
            "OpenAIProvider is a scaffold placeholder. Bind a real SDK adapter in infrastructure."
        )

