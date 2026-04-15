from __future__ import annotations

import unittest

from domain.agent_app.models import AgentApp, AgentAppMetadata
from domain.agent_app.policies import ModelPolicy
from domain.context.models import ContextSegmentType
from domain.memory.models import MemoryKind, MemoryRecord, MemoryScope, MemoryStatus
from domain.session.models import AgentSession
from domain.workflow.models import WorkflowDefinition
from domain.workflow.state import StepExecutionRecord, StepExecutionStatus, WorkflowRunState
from domain.workflow.steps import StepKind, WorkflowStep
from runtime.context.engine import ContextEngine


def _build_app() -> AgentApp:
    workflow = WorkflowDefinition(
        id="default",
        name="Default Workflow",
        description="Build a layered context envelope.",
        steps=(
            WorkflowStep(
                id="draft",
                name="Draft",
                kind=StepKind.PROMPT,
                instruction="Draft a response from the runtime context.",
                output_key="draft",
            ),
        ),
    )
    return AgentApp(
        metadata=AgentAppMetadata(
            id="demo.context",
            name="Context Demo",
            domain="demo",
            description="Test fixture for the context engine.",
        ),
        workflows={workflow.id: workflow},
        default_workflow_id=workflow.id,
        default_model_policy=ModelPolicy(
            provider="mock",
            model="mock-default",
            max_output_tokens=512,
            metadata={"context_window": "4096"},
        ),
    )


class ContextEngineTests(unittest.TestCase):
    def test_compile_builds_layered_context_envelope(self) -> None:
        app = _build_app()
        workflow = app.resolve_workflow()
        session = AgentSession(
            id="session-1",
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            user_input="Explain the first runtime step.",
            context={
                "project": "shanforge",
                "goal": "implement the v2 core runtime",
            },
        )

        envelope = ContextEngine().compile(app=app, workflow=workflow, session=session)

        self.assertEqual(envelope.request.session_id, "session-1")
        self.assertEqual(envelope.request.app_id, app.metadata.id)
        self.assertEqual(envelope.budget.model_context_window, 4096)
        self.assertEqual(envelope.budget.reserved_output_tokens, 512)
        self.assertGreater(envelope.budget.max_input_tokens, 0)
        self.assertEqual(envelope.values["project"], "shanforge")
        self.assertEqual(envelope.values["user_input"], "Explain the first runtime step.")

        segment_types = [segment.type for segment in envelope.all_segments()]
        self.assertIn(ContextSegmentType.SYSTEM, segment_types)
        self.assertIn(ContextSegmentType.TASK, segment_types)
        self.assertIn(ContextSegmentType.WORKING_MEMORY, segment_types)
        self.assertIn(ContextSegmentType.CURRENT_TURN, segment_types)

        self.assertEqual(envelope.final_messages[0]["role"], "system")
        self.assertEqual(envelope.final_messages[-1]["content"], "Explain the first runtime step.")
        self.assertEqual(
            envelope.diagnostics["segment_count"],
            len(envelope.all_segments()),
        )

    def test_compile_for_step_adds_step_state_and_completed_outputs(self) -> None:
        workflow = WorkflowDefinition(
            id="writer",
            name="Writer Workflow",
            description="Run draft and review as separate steps.",
            steps=(
                WorkflowStep(
                    id="draft",
                    name="Draft",
                    kind=StepKind.PROMPT,
                    instruction="Write the first draft.",
                    output_key="draft",
                ),
                WorkflowStep(
                    id="review",
                    name="Review",
                    kind=StepKind.PROMPT,
                    instruction="Review the draft using current context.",
                    output_key="review",
                ),
            ),
        )
        app = AgentApp(
            metadata=AgentAppMetadata(
                id="demo.writer",
                name="Writer Demo",
                domain="demo",
            ),
            workflows={workflow.id: workflow},
            default_workflow_id=workflow.id,
            default_model_policy=ModelPolicy(
                provider="mock",
                model="mock-default",
                max_output_tokens=256,
            ),
        )
        session = AgentSession(
            id="session-2",
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            user_input="Review the drafted response.",
            context={
                "draft": {
                    "summary": "Mock response generated for 'draft'.",
                    "echo": "First draft body",
                }
            },
        )
        state = WorkflowRunState(workflow_id=workflow.id)
        state.append(
            StepExecutionRecord(
                step_id="draft",
                status=StepExecutionStatus.COMPLETED,
                summary="Draft complete.",
                output_key="draft",
            )
        )

        envelope = ContextEngine().compile_for_step(
            app=app,
            workflow=workflow,
            session=session,
            step=workflow.steps[1],
            state=state,
        )

        self.assertEqual(envelope.request.step_id, "review")
        self.assertEqual(envelope.request.step_kind, StepKind.PROMPT.value)
        self.assertEqual(envelope.values["step_id"], "review")
        self.assertEqual(envelope.values["completed_steps"], ["draft"])
        self.assertIn("draft", envelope.values)
        self.assertIn(
            ContextSegmentType.WORKFLOW_STATE,
            [segment.type for segment in envelope.all_segments()],
        )
        self.assertEqual(envelope.diagnostics["step_id"], "review")
        self.assertIn("Current step 'Review'", envelope.final_messages[2]["content"])

    def test_compile_includes_recalled_long_term_memory_segments(self) -> None:
        app = _build_app()
        workflow = app.resolve_workflow()
        session = AgentSession(
            id="session-3",
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            user_input="Continue the platform design.",
            context={"draft": "Current working draft"},
            recalled_memories=[
                MemoryRecord(
                    id="memory-1",
                    kind=MemoryKind.EPISODIC,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Prior Session",
                    body="The last run completed the first runtime scaffold.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.82,
                    supporting_refs=("event://workflow_completed", "evidence://artifact"),
                )
            ],
        )

        envelope = ContextEngine().compile(app=app, workflow=workflow, session=session)

        segment_types = [segment.type for segment in envelope.all_segments()]
        self.assertIn(ContextSegmentType.LONG_TERM_MEMORY, segment_types)
        memory_segment = next(
            segment
            for segment in envelope.all_segments()
            if segment.type is ContextSegmentType.LONG_TERM_MEMORY
        )
        self.assertIn("Prior Session", memory_segment.content)


if __name__ == "__main__":
    unittest.main()
