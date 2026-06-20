from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from domain.model.models import ModelRequest, ModelResponse


@dataclass(slots=True)
class OpenAIProvider:
    """Reserved adapter for a future OpenAI SDK integration."""

    provider_name: str = "openai"

    def contract_metadata(self) -> dict[str, Any]:
        return {
            "bridge_kind": "provider",
            "contract_ready": False,
            "provider_kind": "sdk-placeholder",
        }

    def generate(self, request: ModelRequest) -> ModelResponse:
        raise NotImplementedError(
            "OpenAIProvider is a scaffold placeholder. Bind a real SDK adapter in infrastructure."
        )
