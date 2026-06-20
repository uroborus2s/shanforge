from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from domain.memory.models import (
    MemoryLifecycleAuditAction,
    MemoryLifecycleAuditEntry,
    MemoryLifecycleQueueReviewStatus,
    MemoryLifecycleReviewResolution,
    MemoryStatus,
)
from settings.shared.jsonl import JsonlStore, parse_datetime, serialize_record


def _deserialize_lifecycle_audit_entry(payload: dict[str, object]) -> MemoryLifecycleAuditEntry:
    queue_review_status = payload.get("queue_review_status")
    resolution = payload.get("resolution")
    created_at = payload.get("created_at")
    return MemoryLifecycleAuditEntry(
        id=str(payload["id"]),
        session_id=str(payload["session_id"]),
        record_id=str(payload["record_id"]),
        actor=str(payload["actor"]),
        action=MemoryLifecycleAuditAction(str(payload["action"])),
        current_status=MemoryStatus(str(payload["current_status"])),
        effective_status=MemoryStatus(str(payload["effective_status"])),
        created_at=(
            parse_datetime(str(created_at))
            if created_at not in (None, "")
            else datetime.now(timezone.utc)
        ),
        queue_review_status=(
            MemoryLifecycleQueueReviewStatus(str(queue_review_status))
            if queue_review_status not in (None, "")
            else None
        ),
        resolution=(
            MemoryLifecycleReviewResolution(str(resolution))
            if resolution not in (None, "")
            else None
        ),
        reason=str(payload["reason"]) if payload.get("reason") not in (None, "") else None,
        note=str(payload["note"]) if payload.get("note") not in (None, "") else None,
        metadata=dict(payload.get("metadata", {})),
    )


@dataclass(slots=True)
class InMemoryMemoryLifecycleAuditStore:
    """In-memory lifecycle audit persistence for tests and local wiring."""

    entries: list[MemoryLifecycleAuditEntry] = field(default_factory=list)

    def list_lifecycle_audit_entries(
        self,
        session_id: str,
    ) -> tuple[MemoryLifecycleAuditEntry, ...]:
        return tuple(entry for entry in self.entries if entry.session_id == session_id)

    def append_lifecycle_audit_entries(
        self,
        session_id: str,
        entries: tuple[MemoryLifecycleAuditEntry, ...],
    ) -> None:
        del session_id
        self.entries.extend(entries)


class JsonlMemoryLifecycleAuditStore(JsonlStore):
    """JSONL-backed persistence adapter for durable lifecycle audit entries."""

    def __init__(self, root: str | Path) -> None:
        super().__init__(root=root, filename="memory-lifecycle-audit.jsonl")

    def list_lifecycle_audit_entries(
        self,
        session_id: str,
    ) -> tuple[MemoryLifecycleAuditEntry, ...]:
        return tuple(
            entry
            for entry in self.read_all(_deserialize_lifecycle_audit_entry)
            if entry.session_id == session_id
        )

    def append_lifecycle_audit_entries(
        self,
        session_id: str,
        entries: tuple[MemoryLifecycleAuditEntry, ...],
    ) -> None:
        del session_id
        existing_entries = list(self.read_all(_deserialize_lifecycle_audit_entry))
        ordered_entries = (*existing_entries, *entries)
        if not ordered_entries:
            self.path.write_text("", encoding="utf-8")
            return
        self.path.write_text(
            "\n".join(
                json.dumps(serialize_record(entry), ensure_ascii=True)
                for entry in ordered_entries
            )
            + "\n",
            encoding="utf-8",
        )
