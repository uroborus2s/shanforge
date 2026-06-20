from __future__ import annotations

from dataclasses import dataclass

from application.ports.domain_services import MemoryDomainService
from domain.memory import RecallPreview
from domain.memory.models import RecallBundle, RecallQuery
from domain.session.ports import SessionLedgerPort


@dataclass(slots=True)
class MemoryInspectionService:
    """Application read facade for memory recall diagnostics and governance."""

    session_ledger: SessionLedgerPort
    memory_service: MemoryDomainService

    def recall(self, query: RecallQuery) -> RecallBundle:
        return self.memory_service.recall(query)

    def preview_recall(
        self,
        session_id: str,
        limit: int | None = None,
    ) -> RecallPreview:
        session = self.session_ledger.load_session(session_id)
        if session is None:
            raise KeyError(f"Unknown session: {session_id}")
        return self.memory_service.preview_recall(session, limit=limit)
