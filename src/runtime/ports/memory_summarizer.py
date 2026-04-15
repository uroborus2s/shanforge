from __future__ import annotations

from typing import Protocol

from domain.memory.models import CandidateDrafts, EvidenceRecord, SummaryResult
from domain.session.models import AgentSession


class MemorySummarizerPort(Protocol):
    """Runtime-owned optional memory summarizer contract."""

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
