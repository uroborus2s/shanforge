from __future__ import annotations

from typing import Protocol

from domain.agent_app.manifest import AgentAppManifest


class AgentAppCatalogPort(Protocol):
    """Foundation capability contract consumed by the agent_app domain for manifest lookup."""

    def load_manifest(self, app_id: str) -> AgentAppManifest | None: ...

    def list_manifests(self) -> tuple[AgentAppManifest, ...]: ...


class AgentAppSchemaValidationPort(Protocol):
    """Foundation capability contract consumed by the agent_app domain for manifest validation."""

    def validate_manifest(self, manifest: AgentAppManifest) -> tuple[bool, tuple[str, ...]]: ...
