from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Mapping

from domain.agent_app.policies import ModelPolicy


class ContextSegmentType(StrEnum):
    """Normalized layers available to the runtime context engine."""

    SYSTEM = "system"
    TASK = "task"
    WORKFLOW_STATE = "workflow_state"
    CONVERSATION = "conversation"
    WORKING_MEMORY = "working_memory"
    LONG_TERM_MEMORY = "long_term_memory"
    SKILL = "skill"
    EVIDENCE = "evidence"
    CURRENT_TURN = "current_turn"


class ContextPriority(StrEnum):
    """Relative importance used when the engine needs to prune context."""

    PINNED = "pinned"
    CRITICAL = "critical"
    SUPPORTING = "supporting"
    OPTIONAL = "optional"


@dataclass(slots=True, frozen=True)
class ContextRequest:
    """Platform-internal request passed into the context builder."""

    session_id: str
    app_id: str
    workflow_id: str
    current_user_input: str
    step_id: str | None = None
    step_name: str | None = None
    step_kind: str | None = None
    model_policy: ModelPolicy | None = None
    toolset: tuple[str, ...] = ()
    runtime_state: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class ContextSegment:
    """Atomic unit assembled into the model-facing context envelope."""

    id: str
    type: ContextSegmentType
    source: str
    content: Any
    token_estimate: int
    priority: ContextPriority = ContextPriority.SUPPORTING
    freshness: int = 0
    pinned: bool = False
    compressible: bool = True
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class ContextBudget:
    """Input/output token allocation for one model-facing turn."""

    model_context_window: int
    reserved_output_tokens: int
    reserved_tool_tokens: int
    max_input_tokens: int
    per_layer_budget: Mapping[str, int] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class ContextEnvelope:
    """Assembled context returned by the context engine."""

    request: ContextRequest
    budget: ContextBudget
    system_segments: tuple[ContextSegment, ...] = ()
    conversation_segments: tuple[ContextSegment, ...] = ()
    memory_segments: tuple[ContextSegment, ...] = ()
    evidence_segments: tuple[ContextSegment, ...] = ()
    tool_schemas: tuple[str, ...] = ()
    diagnostics: Mapping[str, Any] = field(default_factory=dict)
    final_messages: tuple[dict[str, str], ...] = ()
    values: Mapping[str, Any] = field(default_factory=dict)

    def all_segments(self) -> tuple[ContextSegment, ...]:
        """Returns every segment in the envelope in assembly order."""

        return (
            *self.system_segments,
            *self.evidence_segments,
            *self.memory_segments,
            *self.conversation_segments,
        )
