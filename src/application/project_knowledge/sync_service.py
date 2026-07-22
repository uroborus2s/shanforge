"""Application contract and state model for asynchronous project-state refresh."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Protocol


class SyncState(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    PROJECTION_READY = "projection_ready"
    MEMORY_READY = "memory_ready"
    HTML_PUBLISHED = "html_published"
    MAINTENANCE_COMMITTED = "maintenance_committed"
    COMMIT_NOT_AUTHORIZED = "commit_not_authorized"
    READY_TO_INTEGRATE = "ready_to_integrate"
    RETRYABLE_FAILED = "retryable_failed"
    INTEGRATED = "integrated"
    DONE = "done"
    SUPERSEDED = "superseded"
    NEEDS_ATTENTION = "needs_attention"


class SyncEvent(StrEnum):
    DISPATCHED = "DISPATCHED"
    INPUT_SUPERSEDED = "INPUT_SUPERSEDED"
    PERMANENT_FAILURE = "PERMANENT_FAILURE"
    STAGE_SUCCEEDED = "STAGE_SUCCEEDED"
    TRANSIENT_FAILURE = "TRANSIENT_FAILURE"
    LEASE_LOST = "LEASE_LOST"
    COMMIT_AUTHORIZED_WITH_DIFF = "COMMIT_AUTHORIZED_WITH_DIFF"
    COMMIT_NOT_AUTHORIZED_WITH_DIFF = "COMMIT_NOT_AUTHORIZED_WITH_DIFF"
    NO_MAINTENANCE_DIFF = "NO_MAINTENANCE_DIFF"
    INTEGRATION_SUCCEEDED = "INTEGRATION_SUCCEEDED"
    INTEGRATION_REQUIRES_MANUAL = "INTEGRATION_REQUIRES_MANUAL"
    NEWER_JOB_INTEGRATED = "NEWER_JOB_INTEGRATED"
    RETRY_BUDGET_AVAILABLE = "RETRY_BUDGET_AVAILABLE"
    RETRY_BUDGET_EXHAUSTED = "RETRY_BUDGET_EXHAUSTED"
    RECEIPT_MATCH = "RECEIPT_MATCH"
    RECEIPT_TRANSIENT_MISMATCH = "RECEIPT_TRANSIENT_MISMATCH"
    RECEIPT_PERMANENT_MISMATCH = "RECEIPT_PERMANENT_MISMATCH"


@dataclass(frozen=True, slots=True)
class SyncTransition:
    from_state: SyncState
    event: SyncEvent
    to_state: SyncState
    precondition: str


def _build_transitions() -> tuple[SyncTransition, ...]:
    classifier = "event_classifier_proved"
    success = "input_current_and_lease_valid_and_fencing_token_matches"
    rows: list[SyncTransition] = []

    def add(
        state: SyncState,
        mappings: tuple[tuple[SyncEvent, SyncState, str], ...],
    ) -> None:
        rows.extend(
            SyncTransition(state, event, target, condition) for event, target, condition in mappings
        )

    add(
        SyncState.QUEUED,
        (
            (SyncEvent.DISPATCHED, SyncState.RUNNING, classifier),
            (SyncEvent.INPUT_SUPERSEDED, SyncState.SUPERSEDED, classifier),
            (SyncEvent.PERMANENT_FAILURE, SyncState.NEEDS_ATTENTION, classifier),
        ),
    )
    for state, target in (
        (SyncState.RUNNING, SyncState.PROJECTION_READY),
        (SyncState.PROJECTION_READY, SyncState.MEMORY_READY),
        (SyncState.MEMORY_READY, SyncState.HTML_PUBLISHED),
    ):
        add(
            state,
            (
                (SyncEvent.STAGE_SUCCEEDED, target, success),
                (SyncEvent.TRANSIENT_FAILURE, SyncState.RETRYABLE_FAILED, classifier),
                (SyncEvent.PERMANENT_FAILURE, SyncState.NEEDS_ATTENTION, classifier),
                (SyncEvent.LEASE_LOST, SyncState.RETRYABLE_FAILED, classifier),
                (SyncEvent.INPUT_SUPERSEDED, SyncState.SUPERSEDED, classifier),
            ),
        )
    add(
        SyncState.HTML_PUBLISHED,
        (
            (SyncEvent.COMMIT_AUTHORIZED_WITH_DIFF, SyncState.MAINTENANCE_COMMITTED, success),
            (SyncEvent.COMMIT_NOT_AUTHORIZED_WITH_DIFF, SyncState.COMMIT_NOT_AUTHORIZED, success),
            (SyncEvent.NO_MAINTENANCE_DIFF, SyncState.INTEGRATED, success),
            (SyncEvent.TRANSIENT_FAILURE, SyncState.RETRYABLE_FAILED, classifier),
            (SyncEvent.PERMANENT_FAILURE, SyncState.NEEDS_ATTENTION, classifier),
            (SyncEvent.LEASE_LOST, SyncState.RETRYABLE_FAILED, classifier),
            (SyncEvent.INPUT_SUPERSEDED, SyncState.SUPERSEDED, classifier),
        ),
    )
    for state in (SyncState.MAINTENANCE_COMMITTED, SyncState.COMMIT_NOT_AUTHORIZED):
        add(
            state,
            (
                (SyncEvent.INTEGRATION_SUCCEEDED, SyncState.INTEGRATED, success),
                (SyncEvent.INTEGRATION_REQUIRES_MANUAL, SyncState.READY_TO_INTEGRATE, classifier),
                (SyncEvent.TRANSIENT_FAILURE, SyncState.RETRYABLE_FAILED, classifier),
                (SyncEvent.PERMANENT_FAILURE, SyncState.NEEDS_ATTENTION, classifier),
                (SyncEvent.LEASE_LOST, SyncState.RETRYABLE_FAILED, classifier),
                (SyncEvent.INPUT_SUPERSEDED, SyncState.SUPERSEDED, classifier),
            ),
        )
    add(
        SyncState.READY_TO_INTEGRATE,
        (
            (SyncEvent.INTEGRATION_SUCCEEDED, SyncState.INTEGRATED, success),
            (SyncEvent.NEWER_JOB_INTEGRATED, SyncState.SUPERSEDED, classifier),
            (SyncEvent.TRANSIENT_FAILURE, SyncState.RETRYABLE_FAILED, classifier),
            (SyncEvent.PERMANENT_FAILURE, SyncState.NEEDS_ATTENTION, classifier),
            (SyncEvent.LEASE_LOST, SyncState.RETRYABLE_FAILED, classifier),
            (SyncEvent.INPUT_SUPERSEDED, SyncState.SUPERSEDED, classifier),
        ),
    )
    add(
        SyncState.RETRYABLE_FAILED,
        (
            (SyncEvent.RETRY_BUDGET_AVAILABLE, SyncState.QUEUED, classifier),
            (SyncEvent.RETRY_BUDGET_EXHAUSTED, SyncState.NEEDS_ATTENTION, classifier),
            (SyncEvent.INPUT_SUPERSEDED, SyncState.SUPERSEDED, classifier),
        ),
    )
    add(
        SyncState.INTEGRATED,
        (
            (SyncEvent.RECEIPT_MATCH, SyncState.DONE, classifier),
            (SyncEvent.RECEIPT_TRANSIENT_MISMATCH, SyncState.RETRYABLE_FAILED, classifier),
            (SyncEvent.RECEIPT_PERMANENT_MISMATCH, SyncState.NEEDS_ATTENTION, classifier),
            (SyncEvent.INPUT_SUPERSEDED, SyncState.SUPERSEDED, classifier),
        ),
    )
    return tuple(rows)


PROJECT_STATE_SYNC_TRANSITIONS = _build_transitions()
TRANSITION_BY_STATE_EVENT = {
    (row.from_state, row.event): row for row in PROJECT_STATE_SYNC_TRANSITIONS
}
LEASED_STATES = frozenset(
    {
        SyncState.RUNNING,
        SyncState.PROJECTION_READY,
        SyncState.MEMORY_READY,
        SyncState.HTML_PUBLISHED,
        SyncState.MAINTENANCE_COMMITTED,
        SyncState.COMMIT_NOT_AUTHORIZED,
        SyncState.READY_TO_INTEGRATE,
    }
)
TERMINAL_STATES = frozenset({SyncState.DONE, SyncState.SUPERSEDED, SyncState.NEEDS_ATTENTION})


def _utc(value: datetime) -> str:
    if value.tzinfo is None:
        raise ValueError("datetime must be timezone-aware")
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True, slots=True)
class ProjectStateSyncRequest:
    schema_id: str
    fact_high_watermark: str
    source_scope: str
    authorization_profile: str
    generator_version: str
    commit_authorized: bool
    requested_at: str
    idempotency_key: str

    @classmethod
    def create(
        cls,
        *,
        fact_high_watermark: str,
        source_scope: str,
        authorization_profile: str,
        generator_version: str,
        commit_authorized: bool,
        requested_at: datetime,
    ) -> ProjectStateSyncRequest:
        values = (
            fact_high_watermark,
            source_scope,
            authorization_profile,
            generator_version,
        )
        if any(not value or value.strip() != value for value in values):
            raise ValueError("sync identity values must be non-empty trimmed strings")
        identity = json.dumps(values, ensure_ascii=False, separators=(",", ":"))
        key = hashlib.sha256(identity.encode("utf-8")).hexdigest()
        return cls(
            schema_id="ProjectStateSyncRequest/v1",
            fact_high_watermark=fact_high_watermark,
            source_scope=source_scope,
            authorization_profile=authorization_profile,
            generator_version=generator_version,
            commit_authorized=commit_authorized,
            requested_at=_utc(requested_at),
            idempotency_key=key,
        )

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, separators=(",", ":"), sort_keys=True)


@dataclass(frozen=True, slots=True)
class SyncEnqueueReceipt:
    schema_id: str
    job_id: str
    state: SyncState
    coalesced: bool


@dataclass(frozen=True, slots=True)
class SyncJob:
    job_id: str
    request: ProjectStateSyncRequest
    state: SyncState
    attempt: int
    fencing_token: int


@dataclass(frozen=True, slots=True)
class SyncClaim:
    job_id: str
    request: ProjectStateSyncRequest
    attempt: int
    fencing_token: int


class ProjectStateSyncQueuePort(Protocol):
    def enqueue(self, request: ProjectStateSyncRequest, *, now: datetime) -> SyncEnqueueReceipt: ...

    def claim(self, *, worker_id: str, now: datetime, lease_seconds: int) -> SyncClaim | None: ...

    def apply_event(
        self,
        job_id: str,
        event: SyncEvent,
        *,
        now: datetime,
        worker_id: str | None = None,
        fencing_token: int | None = None,
    ) -> SyncState: ...

    def schedule_retry(self, job_id: str, *, now: datetime) -> SyncState: ...

    def get(self, job_id: str) -> SyncJob: ...
