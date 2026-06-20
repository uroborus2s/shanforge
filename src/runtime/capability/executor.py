from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from domain.agent_app.models import AgentApp
from domain.model.models import ModelRequest
from domain.response.models import AgentResponse, ToolCallTrace
from domain.session.models import AgentSession, SessionArtifact
from domain.workflow.steps import StepKind, WorkflowStep
from runtime.llm.runtime import LLMRuntime
from runtime.ports import (
    ApprovalPolicyPort,
    CapabilityRegistryPort,
    ModelPolicyResolverPort,
    SandboxPolicyPort,
)
from runtime.response.normalizer import ResponseNormalizer


@dataclass(slots=True)
class ExecutionEngine:
    """Executes one workflow step against model or capability runtimes."""

    llm_runtime: LLMRuntime
    normalizer: ResponseNormalizer
    approval_gate: ApprovalPolicyPort
    sandbox_gate: SandboxPolicyPort
    capability_registry: CapabilityRegistryPort
    model_registry: ModelPolicyResolverPort

    def execute_step(
        self,
        app: AgentApp,
        session: AgentSession,
        step: WorkflowStep,
        context: dict[str, Any],
    ) -> AgentResponse:
        approval = self.approval_gate.evaluate(step=step, session=session)
        if not approval.approved:
            raise PermissionError(approval.reason)

        sandbox = self.sandbox_gate.evaluate(step=step, writeset=step.writeset)
        if not sandbox.allowed:
            raise PermissionError(sandbox.reason)

        if step.kind is StepKind.PROMPT:
            return self._execute_prompt_step(app=app, session=session, step=step, context=context)
        if step.kind is StepKind.CAPABILITY:
            return self._execute_capability_step(session=session, step=step, context=context)
        raise ValueError(f"Unsupported step kind: {step.kind}")

    def _execute_prompt_step(
        self,
        app: AgentApp,
        session: AgentSession,
        step: WorkflowStep,
        context: dict[str, Any],
    ) -> AgentResponse:
        effective_policy = self.model_registry.resolve(step.model_policy, app.default_model_policy)
        request = ModelRequest(
            model_policy=effective_policy,
            system_prompt=(
                f"Agent App '{app.metadata.name}' is executing workflow "
                f"'{session.workflow_id}'."
            ),
            user_prompt=self._render_prompt(step.instruction, context),
            metadata={
                "app_id": app.metadata.id,
                "workflow_id": session.workflow_id,
                "step_id": step.id,
            },
        )
        response = self.llm_runtime.invoke(request)
        model_bindings = list(session.context.get("model_bindings", ()))
        model_bindings.append(
            {
                "provider_id": response.model_ref.provider,
                "model_id": response.model_ref.model,
                "source": "execution",
                "step_id": step.id,
                "metadata": {
                    "policy_provider": effective_policy.provider,
                    "policy_model": effective_policy.model,
                },
            }
        )
        session.context["model_bindings"] = tuple(model_bindings)
        return self.normalizer.from_model_response(response)

    def _execute_capability_step(
        self,
        session: AgentSession,
        step: WorkflowStep,
        context: dict[str, Any],
    ) -> AgentResponse:
        if not step.capability_id:
            raise ValueError(f"Capability step '{step.id}' is missing capability_id.")

        result = self.capability_registry.invoke(
            capability_id=step.capability_id,
            session=session,
            step=step,
            payload=context,
        )
        artifact = SessionArtifact(
            kind="capability",
            uri=f"capability://{result.capability_id}",
            summary=result.summary,
        )
        session.add_artifact(artifact)
        return AgentResponse(
            summary=result.summary,
            raw_output=result.summary,
            structured_output=result.output,
            tool_calls=(
                ToolCallTrace(
                    tool_name=result.capability_id,
                    status="completed",
                    summary=result.summary,
                ),
            ),
            evidence=(artifact,),
        )

    @staticmethod
    def _render_prompt(instruction: str, context: dict[str, Any]) -> str:
        return "\n".join(
            [
                instruction.strip(),
                "",
                "## Context",
                *[f"- {key}: {value}" for key, value in sorted(context.items())],
            ]
        ).strip()
