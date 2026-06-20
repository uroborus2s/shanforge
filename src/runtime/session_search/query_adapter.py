from __future__ import annotations

from dataclasses import dataclass

from domain.session.archive_models import SessionArchiveHit, SessionTranscriptSlice
from domain.session.assembly_models import SessionAssemblyManifest
from domain.session.ports import (
    SessionAssemblyQueryPort,
    SessionArchiveQueryPort,
    SessionTranscriptSlicePort,
)
from runtime.capability.contracts import CapabilityInvocationContext
from runtime.session_search.service import SessionSearchService


@dataclass(slots=True)
class SessionSearchQueryAdapter(
    SessionArchiveQueryPort,
    SessionTranscriptSlicePort,
    SessionAssemblyQueryPort,
):
    """Adapter that exposes session_search capability methods as inspection query ports."""

    service: SessionSearchService
    inspection_session_id: str = "session-inspection"

    def search_session_archive(
        self,
        query: str,
        profile_id: str | None,
        limit: int = 10,
    ) -> tuple[SessionArchiveHit, ...]:
        return self.service.search_session_archive(
            query=query,
            profile_id=profile_id,
            limit=limit,
            context=CapabilityInvocationContext(session_id=self.inspection_session_id),
        )

    def get_session_summary(self, session_id: str) -> str | None:
        return self.service.get_session_summary(session_id)

    def load_session_slice(
        self,
        session_id: str,
        cursor: str | None,
        limit: int,
    ) -> SessionTranscriptSlice:
        return self.service.load_session_slice(
            session_id=session_id,
            cursor=cursor,
            limit=limit,
            context=CapabilityInvocationContext(session_id=self.inspection_session_id),
        )

    def explain_session_assembly(self, session_id: str) -> SessionAssemblyManifest:
        return self.service.explain_session_assembly(
            session_id=session_id,
            context=CapabilityInvocationContext(session_id=self.inspection_session_id),
        )
