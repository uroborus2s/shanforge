from __future__ import annotations

from typing import Any, Mapping, Protocol

from domain.delegation.models import DelegationResult, DelegationTask, DelegationTicket


class DelegationWorkerDispatchPort(Protocol):
    """Foundation capability contract consumed by the delegation domain for worker dispatch."""

    def dispatch(self, task: DelegationTask) -> DelegationTicket: ...


class DelegationResultCollectionPort(Protocol):
    """Foundation capability contract consumed by the delegation domain for result collection."""

    def collect(self, ticket: DelegationTicket) -> DelegationResult: ...


class DelegationWorkspacePort(Protocol):
    """Foundation capability contract consumed by the delegation domain for workspace allocation."""

    def allocate(self, task_id: str) -> Mapping[str, Any]: ...
