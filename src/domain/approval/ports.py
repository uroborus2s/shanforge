from __future__ import annotations

from typing import Any, Mapping, Protocol

from domain.workflow.steps import WorkflowStep


class ApprovalRequestPort(Protocol):
    """Foundation capability contract consumed by the approval domain for approval requests."""

    def request_approval(
        self,
        step: WorkflowStep,
        payload: Mapping[str, Any],
    ) -> Mapping[str, Any]: ...


class ApprovalDecisionQueryPort(Protocol):
    """Foundation capability contract consumed by the approval domain for decision lookup."""

    def get_decision(self, approval_id: str) -> Mapping[str, Any] | None: ...


class ApprovalAuditPort(Protocol):
    """Foundation capability contract consumed by the approval domain for audit persistence."""

    def record_audit_event(
        self,
        event_type: str,
        payload: Mapping[str, Any],
    ) -> None: ...
