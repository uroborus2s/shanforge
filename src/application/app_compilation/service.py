from __future__ import annotations

from dataclasses import dataclass, field

from application.ports.domain_services import AgentAppDomainService
from domain.agent_app.manifest import AgentAppManifest
from domain.agent_app.models import AgentApp
from domain.agent_app.service import DefaultAgentAppDomainService


@dataclass(slots=True)
class AgentAppService:
    """Thin application facade over the Agent App domain service."""

    domain_service: AgentAppDomainService = field(default_factory=DefaultAgentAppDomainService)

    def build_from_manifest(self, manifest: AgentAppManifest) -> AgentApp:
        return self.domain_service.build_from_manifest(manifest)

    def list_required_capabilities(self, app: AgentApp) -> tuple[str, ...]:
        return self.domain_service.list_required_capabilities(app)
