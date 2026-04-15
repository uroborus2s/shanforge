from __future__ import annotations

from dataclasses import dataclass

from application.execution.service import ExecutionResult, ExecutionService
from domain.agent_app.manifest import AgentAppManifest
from domain.agent_app.models import AgentApp


@dataclass(slots=True)
class RuntimeAPI:
    """Adapter-facing runtime facade."""

    service: ExecutionService

    def run_manifest(
        self,
        manifest: AgentAppManifest,
        user_input: str,
        workflow_id: str | None = None,
    ) -> ExecutionResult:
        return self.service.execute_manifest(manifest=manifest, user_input=user_input, workflow_id=workflow_id)

    def run_app(self, app: AgentApp, user_input: str, workflow_id: str | None = None) -> ExecutionResult:
        return self.service.execute_app(app=app, user_input=user_input, workflow_id=workflow_id)
