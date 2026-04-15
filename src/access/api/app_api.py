from __future__ import annotations

from dataclasses import dataclass

from application.app_compilation.service import AgentAppService
from domain.agent_app.manifest import AgentAppManifest
from domain.agent_app.models import AgentApp


@dataclass(slots=True)
class AgentAppAPI:
    """Thin API facade around Agent App compilation."""

    service: AgentAppService

    def materialize(self, manifest: AgentAppManifest) -> AgentApp:
        return self.service.build_from_manifest(manifest)

