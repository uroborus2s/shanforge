from __future__ import annotations

import unittest
from dataclasses import dataclass, field

from application.execution.service import ExecutionService
from domain.agent_app.manifest import AgentAppManifest
from domain.agent_app.models import AgentAppMetadata
from domain.agent_app.service import DefaultAgentAppDomainService
from domain.memory.models import DistillationResult, RecallBundle
from domain.response.models import AgentResponse
from domain.session.models import AgentSession, SessionArtifact
from domain.workflow.models import WorkflowDefinition
from domain.workflow.service import DefaultWorkflowDomainService
from domain.workflow.state import WorkflowRunState
from domain.workflow.steps import StepKind, WorkflowStep


def _build_manifest() -> AgentAppManifest:
    workflow = WorkflowDefinition(
        id="compose",
        name="Compose",
        description="Draft a response.",
        steps=(
            WorkflowStep(
                id="draft",
                name="Draft",
                kind=StepKind.PROMPT,
                instruction="Create a draft.",
                output_key="draft",
            ),
        ),
    )
    return AgentAppManifest(
        metadata=AgentAppMetadata(
            id="demo.writer",
            name="Writer",
            domain="demo",
        ),
        workflows=(workflow,),
        default_workflow_id=workflow.id,
    )


@dataclass(slots=True)
class _SessionService:
    opened: list[tuple[str, str, str, str | None]] = field(default_factory=list)
    attached: list[tuple[str, tuple[str, ...]]] = field(default_factory=list)
    completed: list[str] = field(default_factory=list)
    failed: list[tuple[str, str]] = field(default_factory=list)
    persisted: list[str] = field(default_factory=list)

    def open_session(
        self,
        app_id: str,
        workflow_id: str,
        user_input: str,
        session_id: str | None = None,
    ) -> AgentSession:
        self.opened.append((app_id, workflow_id, user_input, session_id))
        return AgentSession(
            id=session_id or "session-001",
            app_id=app_id,
            workflow_id=workflow_id,
            user_input=user_input,
        )

    def complete_session(self, session: AgentSession) -> AgentSession:
        session.status = "completed"
        self.completed.append(session.id)
        return session

    def fail_session(self, session: AgentSession, reason: str) -> AgentSession:
        session.status = "failed"
        self.failed.append((session.id, reason))
        return session

    def persist_session(self, session: AgentSession) -> AgentSession:
        self.persisted.append(session.id)
        return session

    def attach_artifacts(
        self,
        session: AgentSession,
        artifacts: tuple[SessionArtifact, ...],
    ) -> AgentSession:
        self.attached.append((session.id, tuple(artifact.id for artifact in artifacts)))
        return session


@dataclass(slots=True)
class _MemoryService:
    prepared: list[tuple[str, str, str]] = field(default_factory=list)
    distilled: list[str] = field(default_factory=list)

    def prepare_session(self, session: AgentSession, app: object, workflow: object) -> RecallBundle:
        self.prepared.append((session.id, app.metadata.id, workflow.id))
        return RecallBundle()

    def recall(self, query: object) -> RecallBundle:
        return RecallBundle()

    def distill_session(self, session: AgentSession) -> DistillationResult:
        self.distilled.append(session.id)
        return DistillationResult()

    def explain_session_memory(self, session: AgentSession) -> dict[str, object]:
        return {"session_id": session.id}


@dataclass(slots=True)
class _Kernel:
    should_fail: bool = False

    def run(self, app: object, workflow: object, session: AgentSession) -> tuple[AgentResponse, WorkflowRunState]:
        if self.should_fail:
            raise RuntimeError("kernel exploded")
        session.add_artifact(
            SessionArtifact(
                kind="note",
                uri="memory://artifact-1",
                summary="Generated one note.",
                id="artifact-1",
            )
        )
        return (
            AgentResponse(summary="ok", raw_output="done"),
            WorkflowRunState(workflow_id=workflow.id),
        )


class ApplicationExecutionTests(unittest.TestCase):
    def test_execution_service_runs_through_domain_services(self) -> None:
        manifest = _build_manifest()
        session_service = _SessionService()
        memory_service = _MemoryService()
        service = ExecutionService(
            app_service=DefaultAgentAppDomainService(),
            workflow_service=DefaultWorkflowDomainService(),
            session_service=session_service,
            memory_service=memory_service,
            kernel=_Kernel(),
        )

        result = service.execute_manifest(
            manifest=manifest,
            user_input="Write the first draft.",
            session_id="session-fixed",
        )

        self.assertEqual(result.response.summary, "ok")
        self.assertEqual(result.session.id, "session-fixed")
        self.assertEqual(result.session.status, "completed")
        self.assertEqual(session_service.opened, [("demo.writer", "compose", "Write the first draft.", "session-fixed")])
        self.assertEqual(session_service.attached, [("session-fixed", ("artifact-1",))])
        self.assertEqual(session_service.completed, ["session-fixed"])
        self.assertEqual(session_service.persisted, ["session-fixed"])
        self.assertEqual(memory_service.prepared, [("session-fixed", "demo.writer", "compose")])
        self.assertEqual(memory_service.distilled, ["session-fixed"])

    def test_execution_service_marks_failed_session_when_kernel_raises(self) -> None:
        manifest = _build_manifest()
        session_service = _SessionService()
        memory_service = _MemoryService()
        service = ExecutionService(
            app_service=DefaultAgentAppDomainService(),
            workflow_service=DefaultWorkflowDomainService(),
            session_service=session_service,
            memory_service=memory_service,
            kernel=_Kernel(should_fail=True),
        )

        with self.assertRaisesRegex(RuntimeError, "kernel exploded"):
            service.execute_manifest(
                manifest=manifest,
                user_input="Write the first draft.",
                session_id="session-failed",
            )

        self.assertEqual(session_service.failed, [("session-failed", "kernel exploded")])
        self.assertEqual(session_service.completed, [])
        self.assertEqual(session_service.persisted, [])
        self.assertEqual(memory_service.distilled, [])


if __name__ == "__main__":
    unittest.main()
