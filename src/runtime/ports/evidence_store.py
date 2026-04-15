from __future__ import annotations

from typing import Protocol

from domain.memory.models import EvidenceRecord


class EvidenceStorePort(Protocol):
    """Runtime-owned persistence contract for evidence projections."""

    def save_evidence(self, record: EvidenceRecord) -> None: ...

    def list_by_session(self, session_id: str) -> tuple[EvidenceRecord, ...]: ...
