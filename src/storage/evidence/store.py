from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from domain.memory.models import EvidenceRecord
from domain.session.models import SessionArtifact
from storage.runtime_resource.jsonl import JsonlStore, parse_datetime, serialize_record


def _deserialize_evidence_record(payload: dict[str, object]) -> EvidenceRecord:
    return EvidenceRecord(
        id=str(payload["id"]),
        session_id=str(payload["session_id"]),
        source_kind=str(payload["source_kind"]),
        source_id=str(payload["source_id"]),
        source_ref=str(payload["source_ref"]),
        summary=str(payload["summary"]),
        payload=dict(payload.get("payload", {})),
        created_at=parse_datetime(str(payload["created_at"])),
    )


@dataclass(slots=True)
class InMemoryEvidenceStore:
    """In-memory evidence index used by the memory runtime."""

    records: list[EvidenceRecord] = field(default_factory=list)

    def save_evidence(self, record: EvidenceRecord) -> None:
        for index, existing in enumerate(self.records):
            if existing.id == record.id:
                self.records[index] = record
                break
        else:
            self.records.append(record)

    def save_evidence_from_artifact(
        self,
        session_id: str,
        artifact: SessionArtifact,
    ) -> EvidenceRecord:
        record = EvidenceRecord(
            session_id=session_id,
            source_kind="artifact",
            source_id=artifact.id,
            source_ref=f"artifact://{artifact.id}",
            summary=artifact.summary,
            payload={"kind": artifact.kind, "uri": artifact.uri},
        )
        self.save_evidence(record)
        return record

    def list_by_session(self, session_id: str) -> tuple[EvidenceRecord, ...]:
        return tuple(record for record in self.records if record.session_id == session_id)

    def list_evidence(self, session_id: str) -> tuple[EvidenceRecord, ...]:
        return self.list_by_session(session_id)


class JsonlEvidenceStore(JsonlStore):
    """JSONL-backed persistence adapter for evidence records."""

    def __init__(self, root: str | Path) -> None:
        super().__init__(root=root, filename="evidence-records.jsonl")

    def save_evidence(self, record: EvidenceRecord) -> None:
        self.replace_or_append(record.id, serialize_record(record))

    def save_evidence_from_artifact(
        self,
        session_id: str,
        artifact: SessionArtifact,
    ) -> EvidenceRecord:
        record = EvidenceRecord(
            session_id=session_id,
            source_kind="artifact",
            source_id=artifact.id,
            source_ref=f"artifact://{artifact.id}",
            summary=artifact.summary,
            payload={"kind": artifact.kind, "uri": artifact.uri},
        )
        self.save_evidence(record)
        return record

    def list_by_session(self, session_id: str) -> tuple[EvidenceRecord, ...]:
        return tuple(
            record
            for record in self.read_all(_deserialize_evidence_record)
            if record.session_id == session_id
        )

    def list_evidence(self, session_id: str) -> tuple[EvidenceRecord, ...]:
        return self.list_by_session(session_id)
