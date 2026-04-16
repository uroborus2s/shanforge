from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, TypeVar


def serialize_value(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, datetime):
        return value.isoformat()
    if is_dataclass(value):
        return {key: serialize_value(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {key: serialize_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serialize_value(item) for item in value]
    return value


def serialize_record(record: Any) -> dict[str, Any]:
    return {key: serialize_value(value) for key, value in asdict(record).items()}


def parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value)


_RecordT = TypeVar("_RecordT")


class JsonlStore:
    """Shared JSONL persistence helper."""

    def __init__(self, root: str | Path, filename: str) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.path = self.root / filename

    def read_all(self, loader: Callable[[dict[str, Any]], _RecordT]) -> list[_RecordT]:
        if not self.path.exists():
            return []
        records: list[_RecordT] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            records.append(loader(json.loads(line)))
        return records

    def replace_or_append(self, record_id: str, payload: dict[str, Any]) -> None:
        current: dict[str, dict[str, Any]] = {}
        order: list[str] = []
        if self.path.exists():
            for line in self.path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                item = json.loads(line)
                current[item["id"]] = item
                if item["id"] not in order:
                    order.append(item["id"])
        current[record_id] = payload
        if record_id not in order:
            order.append(record_id)
        content = "\n".join(json.dumps(current[item_id], ensure_ascii=True) for item_id in order) + "\n"
        self.path.write_text(content, encoding="utf-8")
