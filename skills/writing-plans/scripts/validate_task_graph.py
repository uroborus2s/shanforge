#!/usr/bin/env python3
"""Validate owner and dependency DAG fields in plan and TaskCard Markdown."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    arguments = parser.parse_args()
    tasks: dict[str, tuple[str, list[str]]] = {}
    errors: list[str] = []
    for path in arguments.paths:
        record: dict[str, str] = {}
        for line in path.read_text(encoding="utf-8").splitlines() + ["- task_card_id:"]:
            if not line.startswith("- ") or ":" not in line:
                continue
            field, value = (part.strip().strip("`") for part in line[2:].split(":", 1))
            if field == "task_card_id":
                if record:
                    task_id = record.get("task_card_id", "")
                    owner = record.get("owner", "")
                    depends_on = [
                        item.strip()
                        for item in record.get("depends_on", "").split(",")
                        if item.strip() and item.strip() != "none"
                    ]
                    if not task_id:
                        errors.append(f"{path}: missing task_card_id")
                    elif task_id in tasks and "owner" not in record and "depends_on" not in record:
                        continue
                    elif not owner:
                        errors.append(f"{task_id}: missing owner")
                    elif "depends_on" not in record:
                        errors.append(f"{task_id}: missing depends_on")
                    elif task_id in tasks and tasks[task_id] != (owner, depends_on):
                        errors.append(f"{task_id}: inconsistent owner or depends_on")
                    else:
                        tasks[task_id] = (owner, depends_on)
                record = {"task_card_id": value}
            elif field in {"owner", "depends_on"}:
                record[field] = value
    for task_id, (_, dependencies) in tasks.items():
        for dependency in dependencies:
            if dependency == task_id:
                errors.append(f"{task_id}: self dependency")
            elif dependency not in tasks:
                errors.append(f"{task_id}: unknown dependency {dependency}")
    states = {task_id: 0 for task_id in tasks}
    for task_id in tasks:
        if states[task_id]:
            continue
        stack = [(task_id, False)]
        while stack:
            current, leaving = stack.pop()
            if leaving:
                states[current] = 2
            elif states[current] == 1:
                errors.append(f"{current}: dependency cycle")
            elif not states[current]:
                states[current] = 1
                stack.append((current, True))
                stack.extend(
                    (dependency, False)
                    for dependency in tasks[current][1]
                    if dependency in tasks
                )
    if errors:
        print("\n".join(dict.fromkeys(errors)))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
