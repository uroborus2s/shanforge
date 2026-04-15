from __future__ import annotations

from typing import Protocol

from domain.approval.models import SandboxDecision
from domain.workflow.steps import WorkflowStep


class SandboxPolicyPort(Protocol):
    """Runtime-owned writeset sandbox contract."""

    def evaluate(
        self,
        step: WorkflowStep,
        writeset: tuple[str, ...],
        workspace_root: str | None = None,
    ) -> SandboxDecision: ...
