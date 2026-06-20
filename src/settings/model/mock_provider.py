from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from domain.model.models import ModelRef, ModelRequest, ModelResponse, TokenUsage


@dataclass(slots=True)
class MockLLMProvider:
    """Deterministic provider used for local scaffold validation."""

    provider_name: str = "mock"

    def contract_metadata(self) -> dict[str, Any]:
        return {
            "bridge_kind": "provider",
            "contract_ready": True,
        }

    def generate(self, request: ModelRequest) -> ModelResponse:
        step_id = str(request.metadata.get("step_id", "step"))
        content = f"[mock:{request.model_policy.model}] {request.user_prompt}"
        structured_output = {
            "summary": f"Mock response generated for '{step_id}'.",
            "echo": request.user_prompt,
        }
        if step_id == "memory_extract":
            structured_output = {
                "title": "Mock memory draft",
                "body": f"Reusable memory extracted from: {request.user_prompt}",
            }
        return ModelResponse(
            model_ref=ModelRef(provider=self.provider_name, model=request.model_policy.model),
            content=content,
            structured_output=structured_output,
            usage=TokenUsage(input_tokens=len(request.user_prompt.split()), output_tokens=16),
        )
