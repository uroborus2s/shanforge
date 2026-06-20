from __future__ import annotations

from typing import Protocol

from domain.session.archive_models import SessionArchiveHit, SessionTranscriptSlice
from domain.session.assembly_models import SessionAssemblyManifest
from domain.session.models import AgentSession


class MemoryAssemblyQueryPort(Protocol):
    """Application-owned read facade for session archive and assembly explainability."""

    def get_session(self, session_id: str) -> AgentSession | None: ...

    def search_session_archive(
        self,
        query: str,
        profile_id: str | None,
        limit: int = 10,
    ) -> tuple[SessionArchiveHit, ...]: ...

    def load_session_slice(
        self,
        session_id: str,
        cursor: str | None,
        limit: int,
    ) -> SessionTranscriptSlice: ...

    def explain_session_assembly(self, session_id: str) -> SessionAssemblyManifest: ...
