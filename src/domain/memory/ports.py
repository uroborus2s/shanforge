from __future__ import annotations

from typing import Any, Mapping, Protocol

from domain.memory.assembly_models import (
    MemoryProviderAugmentation,
    MemoryProviderBinding,
    RecallPlan,
)
from domain.memory.governance import (
    MemoryProviderGovernanceDecision,
    RecallGovernanceDecision,
)
from domain.memory.models import (
    CandidateDrafts,
    DistillationResult,
    EvidenceRecord,
    MemoryDistillationSample,
    MemoryLifecycleApplyResult,
    MemoryLifecycleAuditEntry,
    MemoryLifecycleQueueEntry,
    MemoryRecord,
    MemoryScope,
    MemoryStatus,
    RecallQuery,
    SummaryResult,
)
from domain.session.delegation_models import SubAgentDigest
from domain.session.models import AgentSession, SessionEvent


class MemoryRecordRepositoryPort(Protocol):
    """Foundation capability contract consumed by the memory domain for memory persistence."""

    def save_memory_record(self, record: MemoryRecord) -> None: ...

    def scan_memory_records(
        self,
        scope_filters: tuple[tuple[MemoryScope, str], ...],
        allowed_statuses: tuple[MemoryStatus, ...],
    ) -> tuple[MemoryRecord, ...]: ...

    def query_memory_records(self, query: RecallQuery) -> tuple[MemoryRecord, ...]: ...


class EvidenceRepositoryPort(Protocol):
    """Foundation capability contract consumed by the memory domain for evidence persistence."""

    def save_evidence(self, record: EvidenceRecord) -> None: ...

    def list_evidence(self, session_id: str) -> tuple[EvidenceRecord, ...]: ...


class MemoryDatasetRepositoryPort(Protocol):
    """Foundation capability contract consumed by the memory domain for dataset persistence."""

    def save_sample(self, sample: MemoryDistillationSample) -> None: ...

    def list_samples(self, session_id: str) -> tuple[MemoryDistillationSample, ...]: ...


class MemoryLifecycleQueueRepositoryPort(Protocol):
    """Foundation capability contract consumed by the memory domain for queue persistence."""

    def list_lifecycle_queue_entries(
        self,
        session_id: str,
    ) -> tuple[MemoryLifecycleQueueEntry, ...]: ...

    def replace_lifecycle_queue_entries(
        self,
        session_id: str,
        entries: tuple[MemoryLifecycleQueueEntry, ...],
    ) -> None: ...


class MemoryLifecycleAuditRepositoryPort(Protocol):
    """Foundation capability contract consumed by the memory domain for audit persistence."""

    def list_lifecycle_audit_entries(
        self,
        session_id: str,
    ) -> tuple[MemoryLifecycleAuditEntry, ...]: ...

    def append_lifecycle_audit_entries(
        self,
        session_id: str,
        entries: tuple[MemoryLifecycleAuditEntry, ...],
    ) -> None: ...


class MemoryArchiveQueryPort(Protocol):
    """Foundation capability contract consumed by the memory domain for archive inspection."""

    def search_archive(
        self,
        app_id: str,
        query_text: str,
        limit: int = 20,
    ) -> tuple[Mapping[str, Any], ...]: ...


class MemoryProfileResolverPort(Protocol):
    """Foundation capability contract consumed by the memory domain for profile resolution."""

    def resolve_profile(
        self,
        session: AgentSession,
        app_id: str,
        workflow_id: str,
    ) -> Mapping[str, Any]: ...


class MemoryRuleBundlePort(Protocol):
    """Foundation capability contract consumed by the memory domain for rule loading."""

    def load_rule_bundle(
        self,
        workspace_root: str | None,
        profile_id: str | None,
    ) -> Mapping[str, Any]: ...


class MemorySkillCatalogPort(Protocol):
    """Foundation capability contract consumed by the memory domain for skill catalog lookup."""

    def list_skill_index(
        self,
        app_id: str,
        workflow_id: str,
    ) -> tuple[Mapping[str, Any], ...]: ...


class MemoryReasoningPort(Protocol):
    """Foundation capability contract consumed by the memory domain for reasoning assistance."""

    def summarize_evidence(
        self,
        session: AgentSession,
        evidence_records: tuple[EvidenceRecord, ...],
    ) -> SummaryResult: ...

    def extract_candidates(
        self,
        session: AgentSession,
        evidence_records: tuple[EvidenceRecord, ...],
        summary: SummaryResult,
    ) -> CandidateDrafts: ...


class MemorySemanticSearchPort(Protocol):
    """Foundation capability contract consumed by the memory domain for semantic recall."""

    def semantic_search(
        self,
        namespace: str,
        query_text: str,
        limit: int = 8,
        filters: Mapping[str, Any] | None = None,
    ) -> tuple[Mapping[str, Any], ...]: ...


class MemoryProviderPort(Protocol):
    """Foundation capability contract for external recall augmentation."""

    def initialize(self, binding: MemoryProviderBinding, session_id: str) -> None: ...

    def prefetch(self, query: RecallQuery, session_id: str) -> str: ...

    def sync_turn(
        self,
        session_id: str,
        latest_events: tuple[SessionEvent, ...],
    ) -> None: ...

    def on_session_end(
        self,
        session_id: str,
        distillation_result: DistillationResult,
    ) -> None: ...

    def on_lifecycle_apply(
        self,
        session_id: str,
        apply_result: MemoryLifecycleApplyResult,
    ) -> None: ...

    def on_delegation(self, digest: SubAgentDigest) -> None: ...


class MemoryProviderManagerPort(Protocol):
    """Runtime execution contract for coordinating one active external memory provider."""

    def start_session(
        self,
        decision: MemoryProviderGovernanceDecision | None,
        query: RecallQuery,
    ) -> MemoryProviderAugmentation | None: ...

    def sync_turn(
        self,
        decision: MemoryProviderGovernanceDecision | None,
        session_id: str,
        latest_events: tuple[SessionEvent, ...],
    ) -> None: ...

    def on_session_end(
        self,
        decision: MemoryProviderGovernanceDecision | None,
        session_id: str,
        distillation_result: DistillationResult,
    ) -> None: ...

    def on_lifecycle_apply(
        self,
        decision: MemoryProviderGovernanceDecision | None,
        session_id: str,
        apply_result: MemoryLifecycleApplyResult,
    ) -> None: ...

    def on_delegation(
        self,
        decision: MemoryProviderGovernanceDecision | None,
        digest: SubAgentDigest,
    ) -> None: ...


class RecallPlannerPort(Protocol):
    """Runtime execution contract for materializing a recall plan from a domain decision."""

    def plan(self, decision: RecallGovernanceDecision) -> RecallPlan: ...


class RecallRankerPort(Protocol):
    """Runtime execution contract for ranking and trimming recall candidates."""

    def rank(
        self,
        plan: RecallPlan,
        records: tuple[MemoryRecord, ...],
        augmentation: MemoryProviderAugmentation | None = None,
    ) -> tuple[MemoryRecord, ...]: ...
