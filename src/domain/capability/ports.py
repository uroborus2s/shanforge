from __future__ import annotations

from typing import Any, Mapping, Protocol

from domain.capability.models import CapabilityDescriptor, CapabilityResult
from domain.session.models import AgentSession
from domain.workflow.steps import WorkflowStep


class CapabilityCatalogPort(Protocol):
    """Foundation capability contract consumed by the capability domain for catalog lookup."""

    def describe_capability(self, capability_id: str) -> CapabilityDescriptor: ...

    def list_capabilities(self) -> tuple[CapabilityDescriptor, ...]: ...


class CapabilityExecutionPort(Protocol):
    """Foundation capability contract consumed by the capability domain for execution."""

    def execute_capability(
        self,
        capability_id: str,
        session: AgentSession,
        step: WorkflowStep,
        payload: Mapping[str, Any],
    ) -> CapabilityResult: ...


class CapabilityWorkspacePort(Protocol):
    """Foundation capability contract consumed by the capability domain for workspace access."""

    def resolve_root(self) -> str: ...

    def read_text(self, path: str) -> str: ...

    def list_paths(self, root: str, pattern: str | None = None) -> tuple[str, ...]: ...


class CapabilityHttpPort(Protocol):
    """Foundation capability contract consumed by the capability domain for outbound HTTP calls."""

    def request(
        self,
        method: str,
        url: str,
        payload: Mapping[str, Any] | None = None,
    ) -> Mapping[str, Any]: ...


class CapabilityShellPort(Protocol):
    """Foundation capability contract consumed by the capability domain for shell execution."""

    def run_command(
        self,
        argv: tuple[str, ...],
        cwd: str | None = None,
    ) -> Mapping[str, Any]: ...


class CapabilityGitPort(Protocol):
    """Foundation capability contract consumed by the capability domain for git operations."""

    def inspect(self, cwd: str, argv: tuple[str, ...]) -> Mapping[str, Any]: ...
