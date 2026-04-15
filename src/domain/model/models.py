from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from domain.agent_app.policies import ModelPolicy


@dataclass(slots=True, frozen=True)
class TokenUsage:
    """Token usage normalized across providers."""

    input_tokens: int = 0
    output_tokens: int = 0


@dataclass(slots=True, frozen=True)
class ModelRef:
    """Provider + model identifier pair."""

    provider: str
    model: str


@dataclass(slots=True, frozen=True)
class ModelRequest:
    """Provider-agnostic request emitted by the LLM runtime."""

    model_policy: ModelPolicy
    system_prompt: str
    user_prompt: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class ModelResponse:
    """Provider-agnostic raw model response."""

    model_ref: ModelRef
    content: str
    structured_output: dict[str, Any] = field(default_factory=dict)
    usage: TokenUsage | None = None

