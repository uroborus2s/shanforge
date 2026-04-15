from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from domain.session.models import AgentSession, SessionArtifact, SessionEvent
from domain.session.ports import (
    SessionArtifactStorePort,
    SessionClockPort,
    SessionIdentityPort,
    SessionLedgerPort,
)


@dataclass(slots=True)
class DefaultSessionDomainService:
    """Business-domain logic for session lifecycle and artifact ownership."""

    ledger: SessionLedgerPort
    artifact_store: SessionArtifactStorePort
    clock: SessionClockPort
    identity: SessionIdentityPort

    def open_session(
        self,
        app_id: str,
        workflow_id: str,
        user_input: str,
        session_id: str | None = None,
    ) -> AgentSession:
        session = AgentSession(
            id=session_id or self.identity.new_id("session"),
            app_id=app_id,
            workflow_id=workflow_id,
            user_input=user_input,
        )
        self._append_event(
            session,
            event_type="session_opened",
            summary=f"Opened session for workflow '{workflow_id}'.",
            payload={"app_id": app_id, "workflow_id": workflow_id},
        )
        self.ledger.save_session(session)
        return session

    def complete_session(self, session: AgentSession) -> AgentSession:
        session.status = "completed"
        self._append_event(
            session,
            event_type="session_completed",
            summary=f"Completed session '{session.id}'.",
        )
        self.ledger.save_session(session)
        return session

    def fail_session(self, session: AgentSession, reason: str) -> AgentSession:
        session.status = "failed"
        self._append_event(
            session,
            event_type="session_failed",
            summary=f"Session '{session.id}' failed.",
            payload={"reason": reason},
        )
        self.ledger.save_session(session)
        return session

    def persist_session(self, session: AgentSession) -> AgentSession:
        self.ledger.save_session(session)
        return session

    def attach_artifacts(
        self,
        session: AgentSession,
        artifacts: Sequence[SessionArtifact],
    ) -> AgentSession:
        if not artifacts:
            return session
        existing_ids = {artifact.id for artifact in session.artifacts}
        for artifact in artifacts:
            if artifact.id not in existing_ids:
                session.add_artifact(artifact)
                existing_ids.add(artifact.id)
            self.artifact_store.save_artifact(session.id, artifact)
        self._append_event(
            session,
            event_type="artifacts_attached",
            summary=f"Attached {len(artifacts)} artifact(s) to session '{session.id}'.",
            payload={"artifact_count": len(artifacts)},
        )
        self.ledger.save_session(session)
        return session

    def _append_event(
        self,
        session: AgentSession,
        event_type: str,
        summary: str,
        payload: dict[str, object] | None = None,
    ) -> None:
        event = SessionEvent(
            type=event_type,
            summary=summary,
            payload=payload or {},
            created_at=self.clock.now(),
        )
        session.events.append(event)
        self.ledger.append_event(session.id, event)
