from __future__ import annotations

from typing import Any, Mapping, Protocol

from domain.memory.models import (
    CandidateDrafts,
    EvidenceRecord,
    MemoryDistillationSample,
    MemoryRecord,
    RecallQuery,
    SummaryResult,
)
from domain.session.models import AgentSession


class MemoryRecordRepositoryPort(Protocol):
    """Foundation capability contract consumed by the memory domain for memory persistence."""

    def save_memory_record(self, record: MemoryRecord) -> None: ...

    def query_memory_records(self, query: RecallQuery) -> tuple[MemoryRecord, ...]: ...


class EvidenceRepositoryPort(Protocol):
    """Foundation capability contract consumed by the memory domain for evidence persistence."""

    def save_evidence(self, record: EvidenceRecord) -> None: ...

    def list_evidence(self, session_id: str) -> tuple[EvidenceRecord, ...]: ...


class MemoryDatasetRepositoryPort(Protocol):
    """Foundation capability contract consumed by the memory domain for dataset persistence."""

    def save_sample(self, sample: MemoryDistillationSample) -> None: ...

    def list_samples(self, session_id: str) -> tuple[MemoryDistillationSample, ...]: ...


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
