from __future__ import annotations

from datetime import datetime
from typing import Protocol

from domain.session.archive_models import SessionArchiveHit, SessionTranscriptSlice
from domain.session.assembly_models import SessionAssemblyManifest
from domain.session.delegation_models import SubAgentDigest
from domain.session.models import AgentSession, SessionArtifact, SessionEvent


class SessionLedgerPort(Protocol):
    """Foundation capability contract consumed by the session domain for ledger persistence."""

    def save_session(self, session: AgentSession) -> None: ...

    def load_session(self, session_id: str) -> AgentSession | None: ...

    def append_event(self, session_id: str, event: SessionEvent) -> None: ...

    def list_events(self, session_id: str) -> tuple[SessionEvent, ...]: ...


class SessionArtifactStorePort(Protocol):
    """Foundation capability contract consumed by the session domain for artifact persistence."""

    def save_artifact(self, session_id: str, artifact: SessionArtifact) -> None: ...

    def load_artifact(self, artifact_id: str) -> SessionArtifact | None: ...

    def list_artifacts(self, session_id: str) -> tuple[SessionArtifact, ...]: ...


class SessionClockPort(Protocol):
    """Foundation capability contract consumed by the session domain for current time."""

    def now(self) -> datetime: ...


class SessionIdentityPort(Protocol):
    """Foundation capability contract consumed by the session domain for stable identifiers."""

    def new_id(self, prefix: str) -> str: ...


class SessionAssemblyStorePort(Protocol):
    """Foundation capability contract consumed for durable session assembly snapshots."""

    def save(self, manifest: SessionAssemblyManifest) -> None: ...

    def get(self, session_id: str) -> SessionAssemblyManifest | None: ...


class DelegationDigestStorePort(Protocol):
    """Foundation capability contract consumed for child-session digest persistence."""

    def save(self, digest: SubAgentDigest) -> None: ...

    def list_by_session(self, session_id: str) -> tuple[SubAgentDigest, ...]: ...


class SessionArchiveQueryPort(Protocol):
    """Foundation capability contract consumed by inspection flows for archive search."""

    def search_session_archive(
        self,
        query: str,
        profile_id: str | None,
        limit: int = 10,
    ) -> tuple[SessionArchiveHit, ...]: ...

    def get_session_summary(self, session_id: str) -> str | None: ...


class SessionTranscriptSlicePort(Protocol):
    """Foundation capability contract consumed by inspection flows for transcript replay."""

    def load_session_slice(
        self,
        session_id: str,
        cursor: str | None,
        limit: int,
    ) -> SessionTranscriptSlice: ...


class SessionAssemblyQueryPort(Protocol):
    """Foundation capability contract consumed by inspection flows for assembly explainability."""

    def explain_session_assembly(self, session_id: str) -> SessionAssemblyManifest: ...
