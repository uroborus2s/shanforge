from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from domain.model.models import ModelRequest, ModelResponse
from runtime.ports.llm_provider import LLMProviderPort


@dataclass(slots=True)
class LLMRuntime:
    """Chooses the provider adapter and executes normalized model requests."""

    providers: Mapping[str, LLMProviderPort]
    default_provider: str

    def invoke(self, request: ModelRequest) -> ModelResponse:
        provider_id = request.model_policy.provider or self.default_provider
        provider = self.providers.get(provider_id)
        if provider is None:
            raise KeyError(f"Provider '{provider_id}' is not registered.")
        return provider.generate(request)

