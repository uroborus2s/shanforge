from __future__ import annotations

from dataclasses import dataclass

from domain.agent_app.manifest import AgentAppManifest
from domain.agent_app.models import AgentApp


@dataclass(slots=True)
class DefaultAgentAppDomainService:
    """Business-domain logic for building and inspecting Agent Apps."""

    def build_from_manifest(self, manifest: AgentAppManifest) -> AgentApp:
        return manifest.to_agent_app()

    def list_required_capabilities(self, app: AgentApp) -> tuple[str, ...]:
        return app.required_capabilities
