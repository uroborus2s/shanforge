from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from domain.agent_app.models import AgentApp
from domain.context.models import (
    ContextBudget,
    ContextEnvelope,
    ContextPriority,
    ContextRequest,
    ContextSegment,
    ContextSegmentType,
)
from domain.session.models import AgentSession
from domain.workflow.models import WorkflowDefinition
from domain.workflow.state import WorkflowRunState
from domain.workflow.steps import WorkflowStep


@dataclass(slots=True)
class ContextBuilder:
    """Builds a step-aware context envelope for one model-facing turn."""

    default_context_window: int = 8192
    default_reserved_output_tokens: int = 1024
    default_reserved_tool_tokens: int = 512

    def build(
        self,
        app: AgentApp,
        workflow: WorkflowDefinition,
        session: AgentSession,
        step: WorkflowStep | None = None,
        state: WorkflowRunState | None = None,
    ) -> ContextEnvelope:
        request = self.build_request(
            app=app,
            workflow=workflow,
            session=session,
            step=step,
            state=state,
        )
        budget = self.build_budget(request)
        system_segments = self._build_system_segments(app=app, workflow=workflow, request=request)
        evidence_segments = self._build_evidence_segments(
            workflow=workflow,
            step=step,
            state=state,
        )
        memory_segments = self._build_memory_segments(session=session)
        conversation_segments = self._build_conversation_segments(session=session)
        all_segments = (
            *system_segments,
            *evidence_segments,
            *memory_segments,
            *conversation_segments,
        )
        diagnostics = {
            "segment_count": len(all_segments),
            "total_token_estimate": sum(segment.token_estimate for segment in all_segments),
            "max_input_tokens": budget.max_input_tokens,
            "step_id": request.step_id,
        }
        return ContextEnvelope(
            request=request,
            budget=budget,
            system_segments=system_segments,
            conversation_segments=conversation_segments,
            memory_segments=memory_segments,
            evidence_segments=evidence_segments,
            diagnostics=diagnostics,
            final_messages=self._assemble_messages(all_segments),
            values=self._build_values(
                app=app,
                workflow=workflow,
                session=session,
                step=step,
                state=state,
            ),
        )

    def build_request(
        self,
        app: AgentApp,
        workflow: WorkflowDefinition,
        session: AgentSession,
        step: WorkflowStep | None = None,
        state: WorkflowRunState | None = None,
    ) -> ContextRequest:
        policy = (
            step.model_policy
            if step is not None and step.model_policy is not None
            else app.default_model_policy
            or next(
                (
                    candidate.model_policy
                    for candidate in workflow.steps
                    if candidate.model_policy
                ),
                None,
            )
        )
        return ContextRequest(
            session_id=session.id,
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            current_user_input=session.user_input,
            step_id=step.id if step is not None else None,
            step_name=step.name if step is not None else None,
            step_kind=step.kind.value if step is not None else None,
            model_policy=policy,
            runtime_state={
                "workflow_retry_budget": workflow.retry_budget,
                "existing_context_keys": tuple(sorted(session.context.keys())),
                "completed_step_ids": tuple(record.step_id for record in state.step_records)
                if state is not None
                else (),
            },
        )

    def build_budget(self, request: ContextRequest) -> ContextBudget:
        policy = request.model_policy
        metadata = policy.metadata if policy is not None else {}
        context_window = self._int_or_default(
            metadata.get("context_window"),
            default=self.default_context_window,
        )
        reserved_output_tokens = (
            policy.max_output_tokens if policy is not None else self.default_reserved_output_tokens
        )
        reserved_output_tokens = min(reserved_output_tokens, max(256, context_window // 2))
        reserved_tool_tokens = min(self.default_reserved_tool_tokens, max(256, context_window // 8))
        max_input_tokens = max(
            1024,
            context_window - reserved_output_tokens - reserved_tool_tokens,
        )
        return ContextBudget(
            model_context_window=context_window,
            reserved_output_tokens=reserved_output_tokens,
            reserved_tool_tokens=reserved_tool_tokens,
            max_input_tokens=max_input_tokens,
            per_layer_budget={
                "system": min(1024, max_input_tokens // 4),
                "memory": min(2048, max_input_tokens // 3),
                "conversation": min(2048, max_input_tokens // 3),
                "evidence": min(1024, max_input_tokens // 4),
            },
        )

    def _build_system_segments(
        self,
        app: AgentApp,
        workflow: WorkflowDefinition,
        request: ContextRequest,
    ) -> tuple[ContextSegment, ...]:
        content = (
            f"You are executing Agent App '{app.metadata.name}' in workflow "
            f"'{workflow.name}'. Keep responses aligned with the active workflow."
        )
        return (
            ContextSegment(
                id="system.runtime",
                type=ContextSegmentType.SYSTEM,
                source="runtime",
                content=content,
                token_estimate=self._estimate_tokens(content),
                priority=ContextPriority.PINNED,
                pinned=True,
                compressible=False,
                metadata={"app_id": request.app_id, "workflow_id": request.workflow_id},
            ),
        )

    def _build_evidence_segments(
        self,
        workflow: WorkflowDefinition,
        step: WorkflowStep | None,
        state: WorkflowRunState | None,
    ) -> tuple[ContextSegment, ...]:
        segments = [
            ContextSegment(
                id="task.workflow",
                type=ContextSegmentType.TASK,
                source="workflow",
                content=(
                    f"Workflow '{workflow.name}' contains {len(workflow.steps)} step(s) and is "
                    f"described as: {workflow.description}"
                ),
                token_estimate=self._estimate_tokens(workflow.description),
                priority=ContextPriority.CRITICAL,
                pinned=True,
                compressible=False,
            )
        ]
        if step is not None:
            completed = len(state.step_records) if state is not None else 0
            position = next(
                index
                for index, candidate in enumerate(workflow.steps, start=1)
                if candidate.id == step.id
            )
            step_state = (
                f"Current step '{step.name}' ({position}/{len(workflow.steps)}) is of type "
                f"'{step.kind.value}'. Completed steps before this turn: {completed}. "
                f"Instruction: {step.instruction}"
            )
            segments.append(
                ContextSegment(
                    id=f"workflow_state.{step.id}",
                    type=ContextSegmentType.WORKFLOW_STATE,
                    source="workflow.step",
                    content=step_state,
                    token_estimate=self._estimate_tokens(step_state),
                    priority=ContextPriority.CRITICAL,
                    pinned=True,
                    compressible=False,
                )
            )
        return tuple(segments)

    def _build_memory_segments(self, session: AgentSession) -> tuple[ContextSegment, ...]:
        segments: list[ContextSegment] = []
        for key, value in sorted(session.context.items()):
            content = f"{key}: {value}"
            segments.append(
                ContextSegment(
                    id=f"memory.{key}",
                    type=ContextSegmentType.WORKING_MEMORY,
                    source="session.context",
                    content=content,
                    token_estimate=self._estimate_tokens(content),
                    priority=ContextPriority.SUPPORTING,
                    freshness=1,
                )
            )
        for record in session.recalled_memories:
            content = f"{record.title}: {record.body}"
            segments.append(
                ContextSegment(
                    id=f"memory.long_term.{record.id}",
                    type=ContextSegmentType.LONG_TERM_MEMORY,
                    source="memory.runtime",
                    content=content,
                    token_estimate=self._estimate_tokens(content),
                    priority=ContextPriority.CRITICAL,
                    freshness=max(1, int(record.confidence * 10)),
                    pinned=record.scope.value == "project",
                    metadata={
                        "memory_id": record.id,
                        "memory_kind": record.kind.value,
                        "memory_scope": record.scope.value,
                    },
                )
            )
        return tuple(segments)

    def _build_conversation_segments(self, session: AgentSession) -> tuple[ContextSegment, ...]:
        content = session.user_input.strip()
        return (
            ContextSegment(
                id="turn.current",
                type=ContextSegmentType.CURRENT_TURN,
                source="user",
                content=content,
                token_estimate=self._estimate_tokens(content),
                priority=ContextPriority.CRITICAL,
                freshness=10,
                pinned=True,
                compressible=False,
            ),
        )

    def _build_values(
        self,
        app: AgentApp,
        workflow: WorkflowDefinition,
        session: AgentSession,
        step: WorkflowStep | None,
        state: WorkflowRunState | None,
    ) -> dict[str, Any]:
        values: dict[str, Any] = {
            "session_id": session.id,
            "app_id": app.metadata.id,
            "app_name": app.metadata.name,
            "workflow_id": workflow.id,
            "workflow_name": workflow.name,
            "user_input": session.user_input,
            "completed_steps": [record.step_id for record in state.step_records] if state else [],
            **session.context,
        }
        if session.recalled_memories:
            values["long_term_memory"] = tuple(
                f"{record.title}: {record.body}" for record in session.recalled_memories
            )
        if step is not None:
            values.update(
                {
                    "step_id": step.id,
                    "step_name": step.name,
                    "step_kind": step.kind.value,
                    "step_instruction": step.instruction,
                    "step_output_key": step.output_key or step.id,
                }
            )
        return values

    def _assemble_messages(
        self,
        segments: tuple[ContextSegment, ...],
    ) -> tuple[dict[str, str], ...]:
        messages: list[dict[str, str]] = []
        for segment in segments:
            role = "system" if segment.type is ContextSegmentType.SYSTEM else "user"
            messages.append({"role": role, "content": str(segment.content)})
        return tuple(messages)

    @staticmethod
    def _estimate_tokens(content: Any) -> int:
        text = str(content)
        return max(1, (len(text) // 4) + 1)

    @staticmethod
    def _int_or_default(value: Any, default: int) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default


@dataclass(slots=True)
class ContextEngine:
    """Facade that exposes workflow-level and step-level context compilation."""

    builder: ContextBuilder = field(default_factory=ContextBuilder)

    def compile(
        self,
        app: AgentApp,
        workflow: WorkflowDefinition,
        session: AgentSession,
    ) -> ContextEnvelope:
        return self.builder.build(app=app, workflow=workflow, session=session)

    def compile_for_step(
        self,
        app: AgentApp,
        workflow: WorkflowDefinition,
        session: AgentSession,
        step: WorkflowStep,
        state: WorkflowRunState,
    ) -> ContextEnvelope:
        return self.builder.build(
            app=app,
            workflow=workflow,
            session=session,
            step=step,
            state=state,
        )
