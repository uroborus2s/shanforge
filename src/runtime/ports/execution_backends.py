from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping, Protocol


class ToolExecutionProviderPort(Protocol):
    """Settings-provider contract owned by the basic capability layer for generic tool execution."""

    def execute(
        self,
        tool_name: str,
        payload: Mapping[str, Any],
    ) -> Mapping[str, Any]: ...


class WorkspaceProviderPort(Protocol):
    """Settings-provider contract owned by the basic capability layer for workspace access."""

    def resolve_root(self) -> str: ...

    def read_text(self, path: str) -> str: ...

    def list_paths(self, root: str, pattern: str | None = None) -> tuple[str, ...]: ...


class HttpClientProviderPort(Protocol):
    """Settings-provider contract owned by the basic capability layer for outbound HTTP."""

    def request(
        self,
        method: str,
        url: str,
        payload: Mapping[str, Any] | None = None,
        options: Mapping[str, Any] | None = None,
    ) -> Mapping[str, Any]: ...


class WebSearchProviderPort(Protocol):
    """Settings-provider contract owned by the basic capability layer for web search."""

    def search(
        self,
        query: str,
        limit: int = 10,
        filters: Mapping[str, Any] | None = None,
    ) -> tuple[Mapping[str, Any], ...]: ...


class WebDocumentProviderPort(Protocol):
    """Settings-provider contract owned by the basic capability layer for web documents."""

    def fetch(self, url: str) -> Mapping[str, Any]: ...

    def extract(self, url: str, mode: str = "readable") -> Mapping[str, Any]: ...


class ShellCommandProviderPort(Protocol):
    """Settings-provider contract owned by the basic capability layer for shell commands."""

    def run(
        self,
        argv: tuple[str, ...],
        cwd: str | None = None,
    ) -> Mapping[str, Any]: ...


class GitProviderPort(Protocol):
    """Settings-provider contract owned by the basic capability layer for git access."""

    def run_git(self, cwd: str, argv: tuple[str, ...]) -> Mapping[str, Any]: ...


class BrowserAutomationProviderPort(Protocol):
    """Settings-provider contract owned by the basic capability layer for browser automation."""

    def open_page(
        self,
        url: str,
        session_id: str | None = None,
    ) -> Mapping[str, Any]: ...

    def inspect_dom(
        self,
        session_token: str,
        selector: str | None = None,
    ) -> Mapping[str, Any]: ...

    def click(
        self,
        session_token: str,
        target: str,
    ) -> Mapping[str, Any]: ...

    def type_text(
        self,
        session_token: str,
        target: str,
        value: str,
    ) -> Mapping[str, Any]: ...

    def wait_for(
        self,
        session_token: str,
        condition: Mapping[str, Any],
    ) -> Mapping[str, Any]: ...

    def capture_screenshot(
        self,
        session_token: str,
        label: str | None = None,
    ) -> Mapping[str, Any]: ...


class ApprovalBackendPort(Protocol):
    """Settings-provider contract owned by the basic capability layer for approval backends."""

    def request_approval(self, payload: Mapping[str, Any]) -> Mapping[str, Any]: ...

    def get_decision(self, approval_id: str) -> Mapping[str, Any] | None: ...


class DelegationBackendPort(Protocol):
    """Settings-provider contract owned by the basic capability layer for delegation backends."""

    def dispatch(self, payload: Mapping[str, Any]) -> Mapping[str, Any]: ...

    def collect(self, ticket_id: str) -> Mapping[str, Any]: ...


class ClockProviderPort(Protocol):
    """Settings-provider contract owned by the basic capability layer for time."""

    def now(self) -> datetime: ...


class IdGeneratorProviderPort(Protocol):
    """Settings-provider contract owned by the basic capability layer for IDs."""

    def new_id(self, prefix: str) -> str: ...
