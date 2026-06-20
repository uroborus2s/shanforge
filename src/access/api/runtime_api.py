from __future__ import annotations

from dataclasses import dataclass

from access.ports.application_use_cases import RuntimeExecutionResult, RuntimeExecutionUseCase
from domain.agent_app.manifest import AgentAppManifest
from domain.agent_app.models import AgentApp


@dataclass(slots=True)
class RuntimeAPI:
    """Adapter-facing runtime facade."""

    service: RuntimeExecutionUseCase

    def run_manifest(
        self,
        manifest: AgentAppManifest,
        user_input: str,
        workflow_id: str | None = None,
    ) -> RuntimeExecutionResult:
        return self.service.execute_manifest(manifest=manifest, user_input=user_input, workflow_id=workflow_id)

    def run_app(self, app: AgentApp, user_input: str, workflow_id: str | None = None) -> RuntimeExecutionResult:
        return self.service.execute_app(app=app, user_input=user_input, workflow_id=workflow_id)
