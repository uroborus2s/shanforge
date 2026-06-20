from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from application.ports import AgentKernelPort
from application.ports.domain_services import (
    AgentAppDomainService,
    MemoryDomainService,
    SessionDomainService,
    WorkflowDomainService,
)
from domain.agent_app.manifest import AgentAppManifest
from domain.agent_app.models import AgentApp
from domain.response.models import AgentResponse
from domain.session.models import AgentSession
from domain.workflow.state import WorkflowRunState


@dataclass(slots=True, frozen=True)
class ExecutionResult:
    """Return envelope for one platform execution."""

    response: AgentResponse
    session: AgentSession
    state: WorkflowRunState


@dataclass(slots=True)
class ExecutionService:
    """Application use case that runs one Agent App workflow."""

    app_service: AgentAppDomainService
    workflow_service: WorkflowDomainService
    session_service: SessionDomainService
    memory_service: MemoryDomainService
    kernel: AgentKernelPort
    session_context_defaults: Mapping[str, Any] = field(default_factory=dict)

    def execute_manifest(
        self,
        manifest: AgentAppManifest,
        user_input: str,
        workflow_id: str | None = None,
        session_id: str | None = None,
    ) -> ExecutionResult:
        app = self.app_service.build_from_manifest(manifest)
        return self.execute_app(
            app=app,
            user_input=user_input,
            workflow_id=workflow_id,
            session_id=session_id,
        )

    def execute_app(
        self,
        app: AgentApp,
        user_input: str,
        workflow_id: str | None = None,
        session_id: str | None = None,
    ) -> ExecutionResult:
        workflow = self.workflow_service.resolve_workflow(app, workflow_id)
        session = self.session_service.open_session(
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            user_input=user_input,
            session_id=session_id,
        )
        session.context.update(dict(self.session_context_defaults))
        self.memory_service.prepare_session(
            session=session,
            app=app,
            workflow=workflow,
        )
        try:
            response, state = self.kernel.run(app=app, workflow=workflow, session=session)
        except Exception as exc:
            self.session_service.fail_session(session, str(exc))
            raise
        if session.artifacts:
            self.session_service.attach_artifacts(session, tuple(session.artifacts))
        self.session_service.complete_session(session)
        self.memory_service.distill_session(session)
        self.session_service.persist_session(session)
        return ExecutionResult(response=response, session=session, state=state)
