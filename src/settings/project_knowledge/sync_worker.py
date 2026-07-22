"""Isolated worker orchestration for the project-state sync queue."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from application.project_knowledge.sync_service import (
    ProjectStateSyncQueuePort,
    ProjectStateSyncRequest,
    SyncEvent,
    SyncState,
)


class ProjectStateSyncStages(Protocol):
    def project(self, request: ProjectStateSyncRequest) -> None: ...

    def update_memory(self, request: ProjectStateSyncRequest) -> None: ...

    def publish_html(self, request: ProjectStateSyncRequest) -> None: ...

    def has_maintenance_diff(self, request: ProjectStateSyncRequest) -> bool: ...

    def commit_maintenance(self, request: ProjectStateSyncRequest) -> None: ...

    def integrate(self, request: ProjectStateSyncRequest) -> bool: ...

    def receipt_matches(self, request: ProjectStateSyncRequest) -> bool: ...


@dataclass(frozen=True, slots=True)
class SyncWorkerReceipt:
    schema_id: str
    job_id: str
    final_state: SyncState
    visited_states: tuple[SyncState, ...]


class ProjectStateSyncWorker:
    def __init__(self, queue: ProjectStateSyncQueuePort, stages: ProjectStateSyncStages) -> None:
        self._queue = queue
        self._stages = stages

    def run_once(self, *, worker_id: str, now: datetime) -> SyncWorkerReceipt | None:
        claim = self._queue.claim(worker_id=worker_id, now=now, lease_seconds=300)
        if claim is None:
            return None
        request = claim.request
        visited: list[SyncState] = [SyncState.RUNNING]

        def event(value: SyncEvent) -> SyncState:
            state = self._queue.apply_event(
                claim.job_id,
                value,
                worker_id=worker_id,
                fencing_token=claim.fencing_token,
                now=now,
            )
            visited.append(state)
            return state

        try:
            self._stages.project(request)
            event(SyncEvent.STAGE_SUCCEEDED)
            self._stages.update_memory(request)
            event(SyncEvent.STAGE_SUCCEEDED)
            self._stages.publish_html(request)
            event(SyncEvent.STAGE_SUCCEEDED)
            if not self._stages.has_maintenance_diff(request):
                event(SyncEvent.NO_MAINTENANCE_DIFF)
            elif request.commit_authorized:
                self._stages.commit_maintenance(request)
                event(SyncEvent.COMMIT_AUTHORIZED_WITH_DIFF)
                event(
                    SyncEvent.INTEGRATION_SUCCEEDED
                    if self._stages.integrate(request)
                    else SyncEvent.INTEGRATION_REQUIRES_MANUAL
                )
            else:
                event(SyncEvent.COMMIT_NOT_AUTHORIZED_WITH_DIFF)
                event(
                    SyncEvent.INTEGRATION_SUCCEEDED
                    if self._stages.integrate(request)
                    else SyncEvent.INTEGRATION_REQUIRES_MANUAL
                )
            if visited[-1] is SyncState.INTEGRATED:
                event(
                    SyncEvent.RECEIPT_MATCH
                    if self._stages.receipt_matches(request)
                    else SyncEvent.RECEIPT_PERMANENT_MISMATCH
                )
        except OSError, TimeoutError:
            event(SyncEvent.TRANSIENT_FAILURE)
            visited.append(self._queue.schedule_retry(claim.job_id, now=now))
        except Exception:
            event(SyncEvent.PERMANENT_FAILURE)
        return SyncWorkerReceipt(
            "ProjectStateSyncWorkerReceipt/v1",
            claim.job_id,
            visited[-1],
            tuple(visited),
        )
