from __future__ import annotations

from dataclasses import dataclass

from application.ports.domain_services import MemoryDomainService
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
)
from domain.session.ports import SessionLedgerPort


@dataclass(slots=True)
class MemoryGovernanceService:
    """Application facade for lifecycle review and durable apply flows."""

    session_ledger: SessionLedgerPort
    memory_service: MemoryDomainService

    def review_lifecycle(self, session_id: str) -> MemoryLifecycleReviewResult:
        session = self.session_ledger.load_session(session_id)
        if session is None:
            raise KeyError(f"Unknown session: {session_id}")
        return self.memory_service.review_lifecycle(session)

    def load_lifecycle_queue(
        self,
        session_id: str,
        queue_filter: MemoryLifecycleQueueFilter | None = None,
    ) -> MemoryLifecycleQueue:
        session = self.session_ledger.load_session(session_id)
        if session is None:
            raise KeyError(f"Unknown session: {session_id}")
        return self.memory_service.load_lifecycle_queue(
            session,
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
        session = self.session_ledger.load_session(session_id)
        if session is None:
            raise KeyError(f"Unknown session: {session_id}")
        return self.memory_service.reopen_lifecycle_queue(
            session,
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
        session = self.session_ledger.load_session(session_id)
        if session is None:
            raise KeyError(f"Unknown session: {session_id}")
        return self.memory_service.load_lifecycle_audit(
            session,
            audit_filter=audit_filter,
        )

    def apply_lifecycle(
        self,
        session_id: str,
        actor: str,
        record_ids: tuple[str, ...] | None = None,
        queue_filter: MemoryLifecycleQueueFilter | None = None,
    ) -> MemoryLifecycleApplyResult:
        session = self.session_ledger.load_session(session_id)
        if session is None:
            raise KeyError(f"Unknown session: {session_id}")
        result = self.memory_service.apply_lifecycle(
            session,
            actor=actor,
            record_ids=record_ids,
            queue_filter=queue_filter,
        )
        self.session_ledger.save_session(session)
        return result

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
        session = self.session_ledger.load_session(session_id)
        if session is None:
            raise KeyError(f"Unknown session: {session_id}")
        return self.memory_service.update_lifecycle_queue(
            session,
            actor=actor,
            review_status=review_status,
            record_ids=record_ids,
            queue_filter=queue_filter,
            note=note,
            resolution=resolution,
        )
