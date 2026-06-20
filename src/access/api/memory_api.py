from __future__ import annotations

from dataclasses import dataclass

from access.ports.application_use_cases import (
    MemoryGovernanceUseCase,
    MemoryInspectionUseCase,
    SessionInspectionUseCase,
)
from domain.memory import RecallPreview
from domain.memory.models import (
    MemoryLifecycleApplyResult,
    MemoryLifecycleAuditFilter,
    MemoryLifecycleAuditLog,
    MemoryLifecycleQueue,
    MemoryLifecycleQueueFilter,
    MemoryLifecycleReviewResolution,
    MemoryLifecycleQueueReviewStatus,
    MemoryLifecycleQueueUpdateResult,
    MemoryLifecycleReviewResult,
    RecallBundle,
    RecallQuery,
)
from domain.session.archive_models import SessionArchiveHit, SessionTranscriptSlice
from domain.session.assembly_models import SessionAssemblyManifest
from domain.session.models import AgentSession


@dataclass(slots=True)
class MemoryAPI:
    """Adapter-facing diagnostics facade for session archive and assembly inspection."""

    session_service: SessionInspectionUseCase
    memory_service: MemoryInspectionUseCase
    memory_governance_service: MemoryGovernanceUseCase

    def get_session(self, session_id: str) -> AgentSession | None:
        return self.session_service.get_session(session_id)

    def search_session_archive(
        self,
        query: str,
        profile_id: str | None,
        limit: int = 10,
    ) -> tuple[SessionArchiveHit, ...]:
        return self.session_service.search_session_archive(query, profile_id, limit)

    def load_session_slice(
        self,
        session_id: str,
        cursor: str | None = None,
        limit: int = 50,
    ) -> SessionTranscriptSlice:
        return self.session_service.load_session_slice(session_id, cursor, limit)

    def explain_session_assembly(self, session_id: str) -> SessionAssemblyManifest:
        return self.session_service.explain_session_assembly(session_id)

    def recall(self, query: RecallQuery) -> RecallBundle:
        return self.memory_service.recall(query)

    def preview_recall(
        self,
        session_id: str,
        limit: int | None = None,
    ) -> RecallPreview:
        return self.memory_service.preview_recall(session_id, limit=limit)

    def review_lifecycle(self, session_id: str) -> MemoryLifecycleReviewResult:
        return self.memory_governance_service.review_lifecycle(session_id)

    def load_lifecycle_queue(
        self,
        session_id: str,
        queue_filter: MemoryLifecycleQueueFilter | None = None,
    ) -> MemoryLifecycleQueue:
        return self.memory_governance_service.load_lifecycle_queue(
            session_id,
            queue_filter=queue_filter,
        )

    def reopen_lifecycle_queue(
        self,
        session_id: str,
        actor: str,
        record_ids: tuple[str, ...] | None = None,
        queue_filter: MemoryLifecycleQueueFilter | None = None,
        note: str | None = None,
    ) -> MemoryLifecycleQueueUpdateResult:
        return self.memory_governance_service.reopen_lifecycle_queue(
            session_id,
            actor=actor,
            record_ids=record_ids,
            queue_filter=queue_filter,
            note=note,
        )

    def load_lifecycle_audit(
        self,
        session_id: str,
        audit_filter: MemoryLifecycleAuditFilter | None = None,
    ) -> MemoryLifecycleAuditLog:
        return self.memory_governance_service.load_lifecycle_audit(
            session_id,
            audit_filter=audit_filter,
        )

    def apply_lifecycle(
        self,
        session_id: str,
        actor: str,
        record_ids: tuple[str, ...] | None = None,
        queue_filter: MemoryLifecycleQueueFilter | None = None,
    ) -> MemoryLifecycleApplyResult:
        return self.memory_governance_service.apply_lifecycle(
            session_id,
            actor=actor,
            record_ids=record_ids,
            queue_filter=queue_filter,
        )

    def update_lifecycle_queue(
        self,
        session_id: str,
        actor: str,
        review_status: MemoryLifecycleQueueReviewStatus,
        record_ids: tuple[str, ...] | None = None,
        queue_filter: MemoryLifecycleQueueFilter | None = None,
        note: str | None = None,
        resolution: MemoryLifecycleReviewResolution | None = None,
    ) -> MemoryLifecycleQueueUpdateResult:
        return self.memory_governance_service.update_lifecycle_queue(
            session_id,
            actor=actor,
            review_status=review_status,
            record_ids=record_ids,
            queue_filter=queue_filter,
            note=note,
            resolution=resolution,
        )
