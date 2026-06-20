from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from domain.model.models import ModelRequest, ModelResponse


@dataclass(slots=True)
class AnthropicProvider:
    """Reserved adapter for a future Anthropic SDK integration."""

    provider_name: str = "anthropic"

    def contract_metadata(self) -> dict[str, Any]:
        return {
            "bridge_kind": "provider",
            "contract_ready": False,
            "provider_kind": "sdk-placeholder",
        }

    def generate(self, request: ModelRequest) -> ModelResponse:
        raise NotImplementedError(
            "AnthropicProvider is a scaffold placeholder. "
            "Bind a real SDK adapter in infrastructure."
        )
