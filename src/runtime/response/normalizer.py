from __future__ import annotations

from dataclasses import dataclass

from domain.model.models import ModelResponse
from domain.response.models import AgentResponse


@dataclass(slots=True)
class ResponseNormalizer:
    """Converts raw provider output into the platform response contract."""

    def from_model_response(self, response: ModelResponse) -> AgentResponse:
        summary = response.structured_output.get("summary") or response.content
        return AgentResponse(
            summary=str(summary),
            raw_output=response.content,
            structured_output=response.structured_output,
            usage=response.usage,
        )

