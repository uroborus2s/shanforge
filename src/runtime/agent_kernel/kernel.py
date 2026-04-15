from __future__ import annotations

from dataclasses import dataclass

from domain.agent_app.models import AgentApp
from domain.response.models import AgentResponse
from domain.session.models import AgentSession
from domain.workflow.models import WorkflowDefinition
from domain.workflow.state import StepExecutionRecord, StepExecutionStatus, WorkflowRunState
from runtime.capability.executor import ExecutionEngine
from runtime.context.engine import ContextEngine
from runtime.ports.delegation_transport import DelegationTransportPort


@dataclass(slots=True)
class AgentKernel:
    """Core runtime loop for the v2 platform.

    This is the platform's first-class execution nucleus. Inspired by Hermes'
    reusable agent loop, it owns the step-by-step workflow lifecycle:
    session start, context compilation, delegation planning, step execution,
    state accumulation, and normalized response handoff.
    """

    context_engine: ContextEngine
    delegation: DelegationTransportPort
    execution_engine: ExecutionEngine

    def run(
        self,
        app: AgentApp,
        workflow: WorkflowDefinition,
        session: AgentSession,
    ) -> tuple[AgentResponse, WorkflowRunState]:
        state = WorkflowRunState(workflow_id=workflow.id)
        latest_response = AgentResponse.empty()

        session.status = "running"
        session.add_event(
            "workflow_started",
            f"Started workflow '{workflow.id}' for app '{app.metadata.id}'.",
            {"workflow_id": workflow.id},
        )

        for step in workflow.steps:
            delegation_plan = self.delegation.plan(step=step, session=session)
            session.add_event(
                "step_planned",
                f"Planned step '{step.id}' with mode '{delegation_plan.mode.value}'.",
                {"step_id": step.id, "mode": delegation_plan.mode.value},
            )
            compiled = self.context_engine.compile_for_step(
                app=app,
                workflow=workflow,
                session=session,
                step=step,
                state=state,
            )
            working_context = dict(compiled.values)
            session.add_event(
                "context_compiled",
                f"Compiled runtime context for step '{step.id}'.",
                {
                    "step_id": step.id,
                    "segment_count": len(compiled.all_segments()),
                    "max_input_tokens": compiled.budget.max_input_tokens,
                    "token_estimate": compiled.diagnostics.get("total_token_estimate", 0),
                },
            )
            response = self.execution_engine.execute_step(
                app=app,
                session=session,
                step=step,
                context=working_context,
            )
            output_key = step.output_key or step.id
            working_context[output_key] = response.structured_output or {
                "text": response.raw_output,
            }
            session.context.update(working_context)
            session.add_event(
                "step_completed",
                f"Completed step '{step.id}'.",
                {"step_id": step.id, "output_key": output_key},
            )
            state.append(
                StepExecutionRecord(
                    step_id=step.id,
                    status=StepExecutionStatus.COMPLETED,
                    summary=response.summary,
                    output_key=output_key,
                )
            )
            latest_response = response

        session.status = "completed"
        session.add_event(
            "workflow_completed",
            f"Completed workflow '{workflow.id}'.",
            {"workflow_id": workflow.id},
        )
        return latest_response, state
