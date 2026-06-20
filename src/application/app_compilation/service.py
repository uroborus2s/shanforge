from __future__ import annotations

from dataclasses import dataclass

from application.ports.domain_services import AgentAppDomainService
from domain.agent_app.manifest import AgentAppManifest
from domain.agent_app.models import AgentApp


@dataclass(slots=True)
class AgentAppService:
    """Thin application facade over the Agent App domain service."""

    domain_service: AgentAppDomainService

    def build_from_manifest(self, manifest: AgentAppManifest) -> AgentApp:
        return self.domain_service.build_from_manifest(manifest)

    def list_required_capabilities(self, app: AgentApp) -> tuple[str, ...]:
        return self.domain_service.list_required_capabilities(app)
