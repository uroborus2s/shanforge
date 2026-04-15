from __future__ import annotations

from typing import Protocol


class WorkspacePort(Protocol):
    """Reserved runtime-owned workspace bridge contract."""

    def resolve_root(self) -> str: ...
