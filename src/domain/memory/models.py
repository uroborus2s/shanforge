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
