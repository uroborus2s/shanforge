from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from domain.memory.models import (
    MemoryLifecycleQueueEntry,
    MemoryLifecycleQueueReviewStatus,
    MemoryLifecycleReviewResolution,
    MemoryScope,
    MemoryStatus,
)
from settings.shared.jsonl import JsonlStore, parse_datetime, serialize_record


def _deserialize_lifecycle_queue_entry(payload: dict[str, object]) -> MemoryLifecycleQueueEntry:
    reviewed_at = payload.get("reviewed_at")
    review_resolution = payload.get("review_resolution")
    return MemoryLifecycleQueueEntry(
        id=str(payload["id"]),
        session_id=str(payload["session_id"]),
        record_id=str(payload["record_id"]),
        scope=MemoryScope(str(payload["scope"])),
        scope_key=str(payload["scope_key"]),
        current_status=MemoryStatus(str(payload["current_status"])),
        effective_status=MemoryStatus(str(payload["effective_status"])),
        reason=str(payload["reason"]),
        allowed=bool(payload["allowed"]),
        hidden=bool(payload["hidden"]),
        action_required=bool(payload["action_required"]),
        selected_by_default=bool(payload["selected_by_default"]),
        review_status=MemoryLifecycleQueueReviewStatus(str(payload["review_status"])),
        reviewed_by=(
            str(payload["reviewed_by"])
            if payload.get("reviewed_by") not in (None, "")
            else None
        ),
        reviewed_at=(
            parse_datetime(str(reviewed_at))
            if reviewed_at not in (None, "")
            else None
        ),
        review_note=(
            str(payload["review_note"])
            if payload.get("review_note") not in (None, "")
            else None
        ),
        review_resolution=(
            MemoryLifecycleReviewResolution(str(review_resolution))
            if review_resolution not in (None, "")
            else None
        ),
        metadata=dict(payload.get("metadata", {})),
    )


@dataclass(slots=True)
class InMemoryMemoryLifecycleQueueStore:
    """In-memory lifecycle queue persistence for tests and local wiring."""

    entries: list[MemoryLifecycleQueueEntry] = field(default_factory=list)

    def list_lifecycle_queue_entries(
        self,
        session_id: str,
    ) -> tuple[MemoryLifecycleQueueEntry, ...]:
        return tuple(entry for entry in self.entries if entry.session_id == session_id)

    def replace_lifecycle_queue_entries(
        self,
        session_id: str,
        entries: tuple[MemoryLifecycleQueueEntry, ...],
    ) -> None:
        retained = [entry for entry in self.entries if entry.session_id != session_id]
        self.entries = [*retained, *entries]


class JsonlMemoryLifecycleQueueStore(JsonlStore):
    """JSONL-backed persistence adapter for durable lifecycle queue entries."""

    def __init__(self, root: str | Path) -> None:
        super().__init__(root=root, filename="memory-lifecycle-queue.jsonl")

    def list_lifecycle_queue_entries(
        self,
        session_id: str,
    ) -> tuple[MemoryLifecycleQueueEntry, ...]:
        return tuple(
            entry
            for entry in self.read_all(_deserialize_lifecycle_queue_entry)
            if entry.session_id == session_id
        )

    def replace_lifecycle_queue_entries(
        self,
        session_id: str,
        entries: tuple[MemoryLifecycleQueueEntry, ...],
    ) -> None:
        retained = [
            entry
            for entry in self.read_all(_deserialize_lifecycle_queue_entry)
            if entry.session_id != session_id
        ]
        ordered_entries = (*retained, *entries)
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
