from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from domain.memory.models import MemoryDistillationSample, MemoryKind, MemoryScope, MemoryStatus
from storage.runtime_resource.jsonl import JsonlStore, parse_datetime, serialize_record


def _deserialize_sample(payload: dict[str, object]) -> MemoryDistillationSample:
    return MemoryDistillationSample(
        id=str(payload["id"]),
        session_id=str(payload["session_id"]),
        candidate_id=str(payload["candidate_id"]),
        candidate_kind=MemoryKind(str(payload["candidate_kind"])),
        candidate_scope=MemoryScope(str(payload["candidate_scope"])),
        candidate_scope_key=str(payload["candidate_scope_key"]),
        decision_status=MemoryStatus(str(payload["decision_status"])),
        decision_reason=str(payload["decision_reason"]),
        supporting_refs=tuple(payload.get("supporting_refs", ())),
        promoted_record_id=payload.get("promoted_record_id"),
        metadata=dict(payload.get("metadata", {})),
        created_at=parse_datetime(str(payload["created_at"])),
    )


@dataclass(slots=True)
class InMemoryMemoryDatasetStore:
    """In-memory labeled dataset store for distillation samples."""

    entries: list[MemoryDistillationSample] = field(default_factory=list)

    def save_entry(self, entry: MemoryDistillationSample) -> None:
        for index, existing in enumerate(self.entries):
            if existing.id == entry.id:
                self.entries[index] = entry
                break
        else:
            self.entries.append(entry)

    def list_by_session(self, session_id: str) -> tuple[MemoryDistillationSample, ...]:
        return tuple(entry for entry in self.entries if entry.session_id == session_id)

    def save_sample(self, sample: MemoryDistillationSample) -> None:
        self.save_entry(sample)

    def list_samples(self, session_id: str) -> tuple[MemoryDistillationSample, ...]:
        return self.list_by_session(session_id)


class JsonlMemoryDatasetStore(JsonlStore):
    """JSONL-backed labeled dataset store for memory distillation samples."""

    def __init__(self, root: str | Path) -> None:
        super().__init__(root=root, filename="memory-dataset.jsonl")

    def save_entry(self, entry: MemoryDistillationSample) -> None:
        self.replace_or_append(entry.id, serialize_record(entry))

    def list_by_session(self, session_id: str) -> tuple[MemoryDistillationSample, ...]:
        return tuple(
            entry
            for entry in self.read_all(_deserialize_sample)
            if entry.session_id == session_id
        )

    def save_sample(self, sample: MemoryDistillationSample) -> None:
        self.save_entry(sample)

    def list_samples(self, session_id: str) -> tuple[MemoryDistillationSample, ...]:
        return self.list_by_session(session_id)
