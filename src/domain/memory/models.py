from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any, Mapping
from uuid import uuid4


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class MemoryKind(StrEnum):
    """Canonical memory categories available to the runtime."""

    EPISODIC = "episodic"
    DECLARATIVE = "declarative"
    PROCEDURAL = "procedural"
    REFLECTIVE = "reflective"


class MemoryScope(StrEnum):
    """Visibility boundary of one memory record."""

    SESSION = "session"
    APP = "app"
    PROJECT = "project"
    USER = "user"
    WORKSPACE = "workspace"


class MemoryStatus(StrEnum):
    """Lifecycle state of one memory candidate or record."""

    DRAFT = "draft"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"
    FORGOTTEN = "forgotten"


class MemoryLifecycleQueueReviewStatus(StrEnum):
    """Human review state carried by one durable lifecycle queue entry."""

    PENDING = "pending"
    DISMISSED = "dismissed"
    APPLIED = "applied"


class MemoryLifecycleReviewResolution(StrEnum):
    """Reviewer-facing taxonomy used to explain why a lifecycle item was triaged."""

    DEFERRED = "deferred"
    KEEP_CURRENT = "keep_current"
    CONFLICT_CONFIRMED = "conflict_confirmed"
    STALE_SIGNAL = "stale_signal"
    MANUAL_OVERRIDE = "manual_override"


class MemoryLifecycleAuditAction(StrEnum):
    """Canonical audit actions emitted by lifecycle review and apply flows."""

    REVIEW_STATUS_UPDATED = "review_status_updated"
    REVIEW_NOTE_UPDATED = "review_note_updated"
    REVIEW_REOPENED = "review_reopened"
    LIFECYCLE_APPLIED = "lifecycle_applied"


@dataclass(slots=True, frozen=True)
class EvidenceRecord:
    """Projection of one session event or artifact into the evidence index."""

    session_id: str
    source_kind: str
    source_id: str
    source_ref: str
    summary: str
    payload: Mapping[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: f"evidence-{uuid4()}")
    created_at: datetime = field(default_factory=_utcnow)


@dataclass(slots=True, frozen=True)
class MemoryCandidate:
    """Candidate memory extracted from ledger facts and evidence."""

    kind: MemoryKind
    scope: MemoryScope
    scope_key: str
    title: str
    body: str
    source_event_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    confidence: float
    metadata: Mapping[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: f"candidate-{uuid4()}")
    created_at: datetime = field(default_factory=_utcnow)


@dataclass(slots=True, frozen=True)
class PromotionDecision:
    """Decision emitted by the promotion gate for one candidate."""

    candidate_id: str
    status: MemoryStatus
    reason: str
    supporting_refs: tuple[str, ...] = ()
    decided_at: datetime = field(default_factory=_utcnow)


@dataclass(slots=True, frozen=True)
class MemoryRecord:
    """Persisted memory asset recalled by future sessions."""

    kind: MemoryKind
    scope: MemoryScope
    scope_key: str
    title: str
    body: str
    status: MemoryStatus
    confidence: float
    supporting_refs: tuple[str, ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: f"memory-{uuid4()}")
    created_at: datetime = field(default_factory=_utcnow)


@dataclass(slots=True, frozen=True)
class RecallQuery:
    """Stable query passed into the memory store and runtime."""

    session_id: str
    app_id: str
    workflow_id: str
    scope_filters: tuple[tuple[MemoryScope, str], ...]
    allowed_statuses: tuple[MemoryStatus, ...] = (MemoryStatus.ACCEPTED,)
    limit: int = 8
    query_text: str | None = None


@dataclass(slots=True, frozen=True)
class RecallBundle:
    """Recall output consumed by the execution service and context engine."""

    pinned_records: tuple[MemoryRecord, ...] = ()
    retrieved_records: tuple[MemoryRecord, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    diagnostics: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class DistillationResult:
    """Artifacts emitted by one session distillation pass."""

    evidence_records: tuple[EvidenceRecord, ...] = ()
    candidates: tuple[MemoryCandidate, ...] = ()
    promotion_decisions: tuple[PromotionDecision, ...] = ()
    promoted_records: tuple[MemoryRecord, ...] = ()


@dataclass(slots=True, frozen=True)
class MemoryLifecycleEvaluation:
    """Lifecycle review projection for one persisted memory record."""

    record_id: str
    scope: MemoryScope
    scope_key: str
    current_status: MemoryStatus
    effective_status: MemoryStatus
    reason: str
    allowed: bool
    hidden: bool
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class MemoryLifecycleQueueFilter:
    """Stable filter used to project a product-facing lifecycle review queue."""

    actionable_only: bool = True
    include_hidden: bool = True
    reasons: tuple[str, ...] = ()
    effective_statuses: tuple[MemoryStatus, ...] = ()
    current_statuses: tuple[MemoryStatus, ...] = ()
    review_statuses: tuple[MemoryLifecycleQueueReviewStatus, ...] = (
        MemoryLifecycleQueueReviewStatus.PENDING,
    )
    review_resolutions: tuple[MemoryLifecycleReviewResolution, ...] = ()
    limit: int | None = None


@dataclass(slots=True, frozen=True)
class MemoryLifecycleResolutionOption:
    """Reviewer-facing guidance for one available lifecycle resolution choice."""

    resolution: MemoryLifecycleReviewResolution
    description: str
    suggested_note: str | None = None


@dataclass(slots=True, frozen=True)
class MemoryLifecycleQueueEntry:
    """Durable queue entry persisted for one session-scoped lifecycle review item."""

    id: str
    session_id: str
    record_id: str
    scope: MemoryScope
    scope_key: str
    current_status: MemoryStatus
    effective_status: MemoryStatus
    reason: str
    allowed: bool
    hidden: bool
    action_required: bool
    selected_by_default: bool
    review_status: MemoryLifecycleQueueReviewStatus = MemoryLifecycleQueueReviewStatus.PENDING
    review_resolution: MemoryLifecycleReviewResolution | None = None
    reviewed_by: str | None = None
    reviewed_at: datetime | None = None
    review_note: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class MemoryLifecycleQueueItem:
    """One actionable or inspectable item projected into the lifecycle queue."""

    record_id: str
    scope: MemoryScope
    scope_key: str
    current_status: MemoryStatus
    effective_status: MemoryStatus
    reason: str
    allowed: bool
    hidden: bool
    action_required: bool
    selected_by_default: bool
    review_status: MemoryLifecycleQueueReviewStatus = MemoryLifecycleQueueReviewStatus.PENDING
    review_resolution: MemoryLifecycleReviewResolution | None = None
    resolution_required: bool = False
    resolution_options: tuple[MemoryLifecycleResolutionOption, ...] = ()
    reviewed_by: str | None = None
    reviewed_at: datetime | None = None
    review_note: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class MemoryLifecycleQueue:
    """Product-facing lifecycle review queue derived from a review pass."""

    session_id: str
    scope_filters: tuple[tuple[MemoryScope, str], ...]
    queue_filter: MemoryLifecycleQueueFilter = field(
        default_factory=MemoryLifecycleQueueFilter
    )
    items: tuple[MemoryLifecycleQueueItem, ...] = ()
    selected_record_ids: tuple[str, ...] = ()
    total_evaluation_count: int = 0
    actionable_count: int = 0
    hidden_count: int = 0
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class MemoryLifecycleReviewResult:
    """Lifecycle review result for one session-scoped governance pass."""

    session_id: str
    scope_filters: tuple[tuple[MemoryScope, str], ...]
    evaluations: tuple[MemoryLifecycleEvaluation, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class MemoryLifecycleApplyResult:
    """Durable result of applying reviewed lifecycle decisions."""

    session_id: str
    actor: str
    queue_filter: MemoryLifecycleQueueFilter | None = None
    selected_record_ids: tuple[str, ...] = ()
    applied_record_ids: tuple[str, ...] = ()
    skipped_record_ids: tuple[str, ...] = ()
    updated_records: tuple[MemoryRecord, ...] = ()
    evaluations: tuple[MemoryLifecycleEvaluation, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class MemoryLifecycleQueueUpdateResult:
    """Result of updating durable lifecycle queue review state."""

    session_id: str
    actor: str
    review_status: MemoryLifecycleQueueReviewStatus
    resolution: MemoryLifecycleReviewResolution | None = None
    queue_filter: MemoryLifecycleQueueFilter | None = None
    requested_record_ids: tuple[str, ...] = ()
    updated_record_ids: tuple[str, ...] = ()
    missing_record_ids: tuple[str, ...] = ()
    queue: MemoryLifecycleQueue | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class MemoryLifecycleAuditFilter:
    """Stable filter used to read lifecycle audit history for one session."""

    actions: tuple[MemoryLifecycleAuditAction, ...] = ()
    record_ids: tuple[str, ...] = ()
    actors: tuple[str, ...] = ()
    queue_review_statuses: tuple[MemoryLifecycleQueueReviewStatus, ...] = ()
    resolutions: tuple[MemoryLifecycleReviewResolution, ...] = ()
    latest_per_record_only: bool = False
    limit: int | None = None


@dataclass(slots=True, frozen=True)
class MemoryLifecycleAuditEntry:
    """Durable audit event for one lifecycle review or apply action."""

    id: str
    session_id: str
    record_id: str
    actor: str
    action: MemoryLifecycleAuditAction
    current_status: MemoryStatus
    effective_status: MemoryStatus
    created_at: datetime = field(default_factory=_utcnow)
    queue_review_status: MemoryLifecycleQueueReviewStatus | None = None
    resolution: MemoryLifecycleReviewResolution | None = None
    reason: str | None = None
    note: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class MemoryLifecycleAuditLog:
    """Product-facing audit log for lifecycle queue review and apply actions."""

    session_id: str
    audit_filter: MemoryLifecycleAuditFilter = field(
        default_factory=MemoryLifecycleAuditFilter
    )
    entries: tuple[MemoryLifecycleAuditEntry, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class SummaryResult:
    """Summary payload returned by a memory summarizer implementation."""

    episode_summary: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class CandidateDrafts:
    """Candidate drafts proposed by a summarizer before promotion gate."""

    candidates: tuple[MemoryCandidate, ...] = ()


@dataclass(slots=True, frozen=True)
class MemoryDistillationSample:
    """Labeled sample emitted for future memory-model training."""

    session_id: str
    candidate_id: str
    candidate_kind: MemoryKind
    candidate_scope: MemoryScope
    candidate_scope_key: str
    decision_status: MemoryStatus
    decision_reason: str
    supporting_refs: tuple[str, ...]
    promoted_record_id: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: f"sample-{uuid4()}")
    created_at: datetime = field(default_factory=_utcnow)
