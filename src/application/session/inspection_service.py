from __future__ import annotations

from dataclasses import dataclass

from domain.session.archive_models import SessionArchiveHit, SessionTranscriptSlice
from domain.session.assembly_models import SessionAssemblyManifest
from domain.session.models import AgentSession
from domain.session.ports import (
    SessionAssemblyQueryPort,
    SessionArchiveQueryPort,
    SessionLedgerPort,
    SessionTranscriptSlicePort,
)


@dataclass(slots=True)
class SessionInspectionService:
    """Application read facade for archive replay and session assembly explainability."""

    session_ledger: SessionLedgerPort
    archive_query: SessionArchiveQueryPort
    transcript_query: SessionTranscriptSlicePort
    assembly_query: SessionAssemblyQueryPort

    def get_session(self, session_id: str) -> AgentSession | None:
        return self.session_ledger.load_session(session_id)

    def search_session_archive(
        self,
        query: str,
        profile_id: str | None,
        limit: int = 10,
    ) -> tuple[SessionArchiveHit, ...]:
        return self.archive_query.search_session_archive(query, profile_id, limit)

    def load_session_slice(
        self,
        session_id: str,
        cursor: str | None,
        limit: int,
    ) -> SessionTranscriptSlice:
        return self.transcript_query.load_session_slice(session_id, cursor, limit)

    def explain_session_assembly(self, session_id: str) -> SessionAssemblyManifest:
        return self.assembly_query.explain_session_assembly(session_id)
