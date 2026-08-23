#!/usr/bin/env python3
# ruff: noqa: E501
"""Build a deterministic project-management snapshot from .factory facts."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
from pathlib import Path
from typing import Any

FINAL_MARKERS = ("closed", "committed", "completed", "done", "passed", "superseded")
ATTENTION_MARKERS = (
    "blocked",
    "failed",
    "changes_requested",
    "needs_user",
    "pending",
    "waiting",
    "awaiting",
)
ACTIVE_MARKERS = ("in_progress", "ready_for", "execut", "review", "verify")
VIEW_LINKS = (
    ("overview", "index.html", "项目总览"),
    ("roadmap", "roadmap.html", "路线图"),
    ("work", "work.html", "当前工作"),
    ("decisions", "decisions.html", "阻塞与决策"),
    ("readiness", "readiness.html", "交付就绪"),
    ("documents", "documents.html", "文档与审计"),
)
BOARD_COLUMNS = (
    "待开始",
    "进行中",
    "测试中",
    "待评审",
    "待确认 / 阻塞",
    "已完成",
)


class SnapshotError(Exception):
    pass


def _assert_within(root: Path, path: Path) -> None:
    if not path.resolve(strict=False).is_relative_to(root):
        raise SnapshotError(f"path resolves outside project root: {path}")


def _text_field(text: str, *names: str) -> str:
    for name in names:
        match = re.search(
            rf"(?m)^(?:[-*]\s*)?(?:\*\*)?{re.escape(name)}(?:\*\*)?\s*[：:]\s*(.+?)\s*$",
            text,
        )
        if match:
            return match.group(1).replace("`", "").strip().strip("* ")
    return ""


def _title(text: str, fallback: str) -> str:
    match = re.search(r"(?m)^#\s+(.+?)\s*$", text)
    title = match.group(1).strip() if match else fallback
    return re.sub(rf"^{re.escape(fallback)}\s*[：:—-]\s*", "", title).strip() or fallback


def _section_paragraphs(text: str, *names: str) -> list[str]:
    names_pattern = "|".join(re.escape(name) for name in names)
    match = re.search(
        rf"(?ms)^##+\s+(?:\d+\.\s*)?(?:{names_pattern})\s*$\n+(.+?)(?=^##+\s|\Z)",
        text,
    )
    if not match:
        return []
    values: list[str] = []
    for paragraph in re.split(r"\n\s*\n", match.group(1)):
        lines = [line.strip() for line in paragraph.splitlines() if line.strip()]
        if not lines or lines[0].startswith("```"):
            continue
        if all(line.startswith("|") for line in lines):
            cells = [
                [cell.strip().replace("`", "") for cell in line.strip("|").split("|")]
                for line in lines
                if not re.fullmatch(r"\|?[\s|:?-]+\|?", line)
            ]
            values.append("；".join(row[-1] for row in cells[1:] if len(row) > 1))
            continue
        bullets = all(re.match(r"^[-*]\s+", line) for line in lines)
        separator = "；" if bullets else " "
        parts = [line.lstrip("-* ").replace("`", "") for line in lines]
        value = separator.join(part.rstrip("。；") if bullets else part for part in parts).strip(
            "； "
        )
        if bullets and value:
            value += "。"
        if value:
            values.append(value)
    return values


def _section_text(text: str, *names: str) -> str:
    paragraphs = _section_paragraphs(text, *names)
    return paragraphs[0] if paragraphs else ""


def _summary(text: str, *names: str) -> str:
    return _text_field(text, *names) or _section_text(text, *names)


def _events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    if not path.exists():
        return events
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            raise SnapshotError(f"{path}:{number}: invalid JSONL: {error.msg}") from error
        if not isinstance(value, dict):
            raise SnapshotError(f"{path}:{number}: ledger event must be an object")
        events.append(value)
    return events


def _category(status: str) -> str:
    normalized = status.lower()
    if any(marker in normalized for marker in ATTENTION_MARKERS):
        return "attention"
    if any(marker in normalized for marker in FINAL_MARKERS):
        return "completed"
    if any(marker in normalized for marker in ACTIVE_MARKERS):
        return "active"
    return "backlog"


def _effective_event(
    events: list[dict[str, Any]],
    *,
    work_item: bool = False,
) -> dict[str, Any]:
    terminal: dict[str, Any] | None = None
    for event in events:
        event_type = str(event.get("event_type") or event.get("event") or "").lower()
        marker = f"{event_type} {event.get('status', '')}".lower()
        if "reopen" in marker or any(
            value in marker
            for value in ("changes_requested", "changes-requested", "changes requested")
        ):
            terminal = None
        elif any(
            value in str(event.get("status") or "").lower()
            for value in ("closed", "committed", "completed", "done", "superseded")
        ) and (
            not work_item
            or str(event.get("completion_level") or "").lower() == "work_item"
            or "work_item_closed" in event_type
            or "workitem_closed" in event_type
            or not _event_task_id(event)
        ):
            terminal = event
    return terminal or (events[-1] if events else {})


def _status_label(status: str, category: str) -> str:
    normalized = status.lower()
    if category == "attention":
        if "changes_requested" in normalized:
            return "评审要求修改"
        if "blocked" in normalized or "failed" in normalized:
            return "存在阻塞"
        return "等待你的确认"
    if category == "active":
        if "ready_for" in normalized and "review" in normalized:
            return "等待独立评审"
        if "commit" in normalized:
            return "等待本地提交"
        if "verify" in normalized or "test" in normalized:
            return "正在验证"
        return "正在进行"
    if category == "completed":
        if "superseded" in normalized:
            return "已由新方案替代"
        if "committed" in normalized:
            return "已完成并提交"
        return "已完成"
    if status.lower() in {"", "unknown", "not_registered"}:
        return "状态未登记"
    return "已登记待办"


def _next_step(status: str, category: str, raw: str, task_title: str) -> str:
    if raw and re.search(r"[\u3400-\u9fff]", raw):
        return raw
    normalized = status.lower()
    if category == "completed":
        return "无"
    if "changes_requested" in normalized:
        return "修复评审发现的问题"
    if category == "attention":
        return "等待人工确认"
    if "review" in normalized:
        return "完成独立评审"
    if "commit" in normalized:
        return "完成本地提交"
    if "verify" in normalized or "test" in normalized:
        return "完成验证"
    if task_title:
        return f"完成「{task_title}」"
    return "继续当前工作项"


def _event_task_id(event: dict[str, Any]) -> str:
    return str(event.get("task_card_id") or event.get("task_id") or event.get("task") or "")


def _event_time(event: dict[str, Any]) -> str:
    return str(
        event.get("ts")
        or event.get("time")
        or event.get("updated_at")
        or event.get("created_at")
        or ""
    )


def _values(events: list[dict[str, Any]], *keys: str) -> list[str]:
    values: list[str] = []
    for event in reversed(events):
        for key in keys:
            value = event.get(key)
            candidates = value if isinstance(value, list) else [value]
            for candidate in candidates:
                if isinstance(candidate, str) and candidate and candidate not in values:
                    values.append(candidate)
    return values


def _requirements(text: str) -> list[dict[str, str]]:
    matches = list(
        re.finditer(
            r"(?m)^###\s+([A-Za-z][A-Za-z0-9._~-]*REQ[A-Za-z0-9._~-]*|REQ-[A-Za-z0-9._~-]+)"
            r"\s*[：:—-]?\s*(.*?)\s*$",
            text,
        )
    )
    requirements: list[dict[str, str]] = []
    for index, match in enumerate(matches):
        body = text[match.end() : matches[index + 1].start() if index + 1 < len(matches) else None]
        requirements.append(
            {
                "id": match.group(1),
                "title": match.group(2).strip() or "需求名称尚未登记",
                "body": body.strip(),
            }
        )
    return requirements


def _plan_stages(text: str) -> list[dict[str, Any]]:
    section = re.search(
        r"(?ms)^##\s+Work Breakdown\s*$\n(.*?)(?=^##\s|\Z)",
        text,
    )
    if not section:
        return []
    lines = section.group(1).splitlines()
    header_index = next(
        (
            index
            for index, line in enumerate(lines)
            if [cell.strip().lower() for cell in line.strip().strip("|").split("|")]
            == ["id", "parent_id", "title", "status"]
        ),
        None,
    )
    if header_index is None or header_index + 1 >= len(lines):
        raise SnapshotError("Work Breakdown must contain an id | parent_id | title | status table")
    separator = [cell.strip() for cell in lines[header_index + 1].strip().strip("|").split("|")]
    if len(separator) != 4 or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator):
        raise SnapshotError("Work Breakdown route table has an invalid separator row")

    stages: list[dict[str, Any]] = []
    nodes_by_id: dict[str, dict[str, Any]] = {}
    for line in lines[header_index + 2 :]:
        if not line.strip():
            continue
        if not line.lstrip().startswith("|"):
            break
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 4:
            raise SnapshotError("Work Breakdown route rows must contain exactly four columns")
        node_id, parent_id, title, status = cells
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._~-]*", node_id):
            raise SnapshotError(f"invalid route id: {node_id or '<empty>'}")
        if node_id in nodes_by_id:
            raise SnapshotError(f"duplicate route id: {node_id}")
        if not status:
            status = "unknown"
            state = "missing"
            label = "状态未登记"
        else:
            normalized = status.lower()
            if normalized == "approved" or any(
                marker in normalized for marker in ("completed", "closed", "done")
            ):
                state = "completed"
                label = "已完成"
            elif "approved_pending" in normalized or any(
                marker in normalized
                for marker in (
                    "review",
                    "confirm",
                    "blocked",
                    "pending",
                    "current",
                    "in_progress",
                    "active",
                )
            ):
                state = "current"
                label = "当前 / 待处理"
            else:
                state = "planned"
                label = "未开始"
        node = {
            "id": node_id,
            "title": title or "路线名称尚未登记",
            "status": status,
            "state": state,
            "label": label,
            "parent_id": parent_id or None,
            "children": [],
            "depth": 0,
        }
        stages.append(node)
        nodes_by_id[node_id] = node

    for node in stages:
        parent_id = node["parent_id"]
        if not parent_id:
            continue
        if parent_id == node["id"]:
            raise SnapshotError(f"route {node['id']} cannot be its own parent")
        if parent_id not in nodes_by_id:
            raise SnapshotError(f"missing parent {parent_id} for route {node['id']}")

    for node in stages:
        seen: set[str] = set()
        cursor = node
        while cursor["parent_id"]:
            if cursor["id"] in seen:
                raise SnapshotError(f"route parent cycle detected at {cursor['id']}")
            seen.add(cursor["id"])
            cursor = nodes_by_id[cursor["parent_id"]]

    for node in stages:
        if node["parent_id"]:
            nodes_by_id[node["parent_id"]]["children"].append(node["id"])
            cursor = node
            while cursor["parent_id"]:
                node["depth"] += 1
                cursor = nodes_by_id[cursor["parent_id"]]
    return stages


def _relation_ids(value: str) -> list[str]:
    return list(dict.fromkeys(re.findall(r"\bREQ-[A-Za-z0-9._~-]+\b", value)))


def _task_briefs(
    directory: Path,
    events: list[dict[str, Any]],
    parent: dict[str, Any],
) -> list[dict[str, Any]]:
    task_root = directory / "task-briefs"
    tasks: list[dict[str, Any]] = []
    if not task_root.is_dir():
        return tasks
    for path in sorted(task_root.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        declared_id = _text_field(text, "任务", "Task")
        task_id = declared_id.split(maxsplit=1)[0] if declared_id else path.stem
        task_events = [event for event in events if _event_task_id(event) == task_id]
        latest = _effective_event(task_events)
        brief_status = _text_field(text, "状态")
        if parent["category"] == "completed":
            status = parent["status"]
        elif task_id == parent["task_id"]:
            status = parent["status"]
        else:
            historical_status = str(latest.get("status") or brief_status or "")
            status = (
                historical_status
                if _category(historical_status) == "completed"
                else "registered_backlog"
            )
        category = _category(status)
        raw_next_action = str(
            latest.get("next_required_action")
            or latest.get("next_action")
            or _text_field(text, "唯一下一动作", "下一动作")
            or ""
        )
        relations: Any = (
            _text_field(text, "关联需求", "关联目标", "追踪目标")
            or latest.get("traceability_targets")
            or ""
        )
        if isinstance(relations, list):
            relations = "、".join(str(value) for value in relations)
        tasks.append(
            {
                "id": task_id,
                "is_current": task_id == parent["task_id"],
                "brief_status": brief_status,
                "title": _title(text, task_id),
                "status": status,
                "status_label": _status_label(status, category),
                "category": category,
                "next_action": _next_step(
                    status,
                    category,
                    raw_next_action,
                    _title(text, task_id),
                ),
                "goal": _summary(text, "目标", "任务目标", "目标和口径"),
                "priority": _text_field(text, "优先级"),
                "scope": _text_field(text, "任务层级", "层级"),
                "task_type": _text_field(text, "类型", "task_type") or "任务类型未登记",
                "module": (
                    _text_field(text, "需求模块", "业务模块", "领域模块")
                    or parent["module"]
                    or "需求模块未登记"
                ),
                "relations": str(relations),
                "verification": _summary(
                    text,
                    "验证",
                    "验证命令",
                    "完成口径",
                    "验收标准",
                ),
                "outputs": _values(task_events, "outputs", "output"),
                "evidence": _values(
                    task_events,
                    "evidence",
                    "evidences",
                    "report",
                    "review",
                ),
                "commits": _values(
                    task_events,
                    "commits",
                    "commit",
                    "commit_sha",
                    "local_commit",
                ),
                "updated_at": _event_time(latest),
                "work_item_id": parent["id"],
                "work_item_title": parent["title"],
                "work_item_purpose": parent["purpose"],
                "stage": parent["stage"],
                "gate_reason": parent["gate_reason"],
                "human_confirmation_required": parent["human_confirmation_required"],
                "owner": parent["owner"],
                "target_date": parent["target_date"],
                "stop_reason": str(
                    latest.get("stop_reason")
                    or latest.get("blocked_reason")
                    or latest.get("blocker")
                    or ""
                ),
                "events": task_events,
                "work_item_has_plan": parent["plan_path"].is_file(),
            }
        )
    return tasks


def _synthetic_task(
    parent: dict[str, Any],
    event: dict[str, Any],
    events: list[dict[str, Any]],
) -> dict[str, Any]:
    task_id = _event_task_id(event) or parent["id"]
    title = str(event.get("task_title") or parent["title"])
    return {
        "id": task_id,
        "is_current": True,
        "brief_status": "",
        "title": title,
        "status": parent["status"],
        "status_label": parent["status_label"],
        "category": parent["category"],
        "next_action": parent["next_action"],
        "goal": parent["purpose"],
        "priority": "",
        "scope": "",
        "task_type": "任务类型未登记",
        "module": parent["module"] or "需求模块未登记",
        "relations": "",
        "verification": "",
        "outputs": _values(events, "outputs", "output"),
        "evidence": _values(events, "evidence", "evidences", "report", "review"),
        "commits": _values(
            events,
            "commits",
            "commit",
            "commit_sha",
            "local_commit",
        ),
        "updated_at": parent["updated_at"],
        "work_item_id": parent["id"],
        "work_item_title": parent["title"],
        "work_item_purpose": parent["purpose"],
        "stage": parent["stage"],
        "gate_reason": parent["gate_reason"],
        "human_confirmation_required": parent["human_confirmation_required"],
        "owner": parent["owner"],
        "target_date": parent["target_date"],
        "stop_reason": parent["stop_reason"],
        "events": events,
        "work_item_has_plan": parent["plan_path"].is_file(),
    }


def _work_items(root: Path) -> list[dict[str, Any]]:
    work_items_root = root / ".factory" / "workitems"
    if not work_items_root.exists():
        return []
    items: list[dict[str, Any]] = []
    for directory in sorted(path for path in work_items_root.iterdir() if path.is_dir()):
        brief_path = directory / "brief.md"
        ledger_path = directory / "ledger.jsonl"
        plan_path = directory / "plan.md"
        if not brief_path.is_file() and not ledger_path.is_file():
            continue
        brief = brief_path.read_text(encoding="utf-8") if brief_path.exists() else ""
        events = _events(ledger_path)
        event = _effective_event(events, work_item=True)
        status = str(event.get("status") or _text_field(brief, "状态") or "unknown")
        category = _category(status)
        task_id = _event_task_id(event)
        task_title = str(event.get("task_title") or "")
        raw_next_action = str(
            event.get("next_required_action")
            or event.get("next_action")
            or _text_field(brief, "唯一下一动作", "下一动作")
            or ""
        )
        parent_title = _title(brief, directory.name)
        if parent_title == directory.name:
            parent_title = _text_field(brief, "名称") or parent_title
        parent: dict[str, Any] = {
            "id": directory.name,
            "title": parent_title,
            "status": status,
            "status_label": _status_label(status, category),
            "next_action": _next_step(status, category, raw_next_action, task_title),
            "category": category,
            "purpose": _summary(brief, "用户目标", "目标", "用户意图", "问题"),
            "stage": _text_field(brief, "阶段") or "阶段未登记",
            "module": _text_field(brief, "需求模块", "业务模块"),
            "milestone": _text_field(brief, "里程碑", "下一里程碑"),
            "target_date": _text_field(
                brief,
                "目标日期",
                "计划日期",
                "截止日期",
                "完成日期",
            ),
            "task_id": task_id,
            "task_title": task_title,
            "updated_at": _event_time(event),
            "stop_reason": str(
                event.get("stop_reason")
                or event.get("blocked_reason")
                or event.get("blocker")
                or _text_field(brief, "停止原因", "阻塞")
                or ""
            ),
            "gate_reason": str(event.get("gate_reason") or ""),
            "human_confirmation_required": bool(event.get("human_confirmation_required")),
            "review_score": event.get("review_score"),
            "owner": str(event.get("owner") or event.get("actor") or ""),
            "outputs": _values(events, "outputs", "output"),
            "evidence": _values(
                events,
                "evidence",
                "evidences",
                "report",
                "review",
            ),
            "commits": _values(
                events,
                "commits",
                "commit",
                "commit_sha",
                "local_commit",
            ),
            "events": events,
            "requirements": _requirements(brief),
            "plan_path": plan_path,
            "plan_title": "",
            "plan_stages": [],
            "plan_nodes": [],
        }
        if plan_path.is_file():
            plan_text = plan_path.read_text(encoding="utf-8")
            parent["plan_title"] = _title(plan_text, f"{directory.name} 计划")
            parent["plan_nodes"] = _plan_stages(plan_text)
            parent["plan_stages"] = [
                node for node in parent["plan_nodes"] if node["parent_id"] is None
            ]
        tasks = _task_briefs(directory, events, parent)
        if not tasks:
            tasks = [_synthetic_task(parent, event, events)]
        current_task = next((task for task in tasks if task["id"] == task_id), None)
        if current_task:
            parent["task_title"] = current_task["title"]
            parent["priority"] = current_task["priority"]
            parent["scope"] = current_task["scope"]
            parent["relations"] = current_task["relations"]
            parent["task_goal"] = current_task["goal"]
            parent["verification"] = current_task["verification"]
            if not parent["module"] and current_task["module"] != "需求模块未登记":
                parent["module"] = current_task["module"]
        else:
            parent.update(
                {
                    "priority": "",
                    "scope": "",
                    "relations": "",
                    "task_goal": "",
                    "verification": "",
                }
            )
        parent["tasks"] = tasks
        items.append(parent)
    category_order = {"attention": 0, "active": 1, "backlog": 2, "completed": 3}
    items.sort(key=lambda item: item["id"])
    items.sort(key=lambda item: item["updated_at"], reverse=True)
    items.sort(key=lambda item: category_order[item["category"]])
    task_id_counts: dict[str, int] = {}
    for item in items:
        for task in item["tasks"]:
            task_id_counts[task["id"]] = task_id_counts.get(task["id"], 0) + 1
    for item in items:
        for task in item["tasks"]:
            task["route"] = (
                task["id"]
                if task_id_counts[task["id"]] == 1
                else f"{task['work_item_id']}--{task['id']}"
            )
    return items


def _project(root: Path) -> dict[str, str]:
    project_file = root / ".factory" / "project.json"
    if not project_file.exists():
        value: dict[str, Any] = {}
    else:
        try:
            loaded = json.loads(project_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise SnapshotError(f"{project_file}: invalid JSON: {error.msg}") from error
        if not isinstance(loaded, dict):
            raise SnapshotError(f"{project_file}: project metadata must be an object")
        value = loaded
    architecture = root / "docs" / "05-design" / "system-architecture.md"
    architecture_text = architecture.read_text(encoding="utf-8") if architecture.is_file() else ""
    overview = root / "docs" / "01-getting-started" / "project-overview.md"
    overview_text = overview.read_text(encoding="utf-8") if overview.is_file() else ""
    positioning = _section_paragraphs(overview_text, "项目定位")
    definition = _section_text(architecture_text, "架构结论")
    delivery = _section_text(architecture_text, "交付单元")
    return {
        "name": str(
            value.get("name") or value.get("project_name") or value.get("project_id") or root.name
        ),
        "idea": str(value.get("idea") or value.get("description") or ""),
        "owner": str(value.get("owner") or ""),
        "stage": str(value.get("stage") or ""),
        "definition": definition,
        "delivery": delivery,
        "problem": positioning[1] if len(positioning) > 1 else "",
    }


def _session(root: Path) -> dict[str, str]:
    path = root / ".factory" / "memory" / "agent-session.md"
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    position = _text_field(text, "项目整体进度", "当前阶段", "阶段")
    identifiers = re.findall(r"[A-Za-z0-9][A-Za-z0-9._~-]*", position)
    values = {
        "位置": position,
        "工作项": identifiers[0] if "/" in position and identifiers else "",
        "任务": identifiers[1] if "/" in position and len(identifiers) > 1 else "",
        "阶段": _text_field(text, "阶段"),
        "状态": _text_field(text, "当前状态", "状态"),
        "当前焦点": _text_field(text, "当前焦点"),
        "停止原因": _text_field(text, "停止原因"),
        "唯一下一动作": _text_field(text, "唯一下一动作", "下一动作"),
        "Gate": _text_field(text, "Gate"),
        "确认事项": _text_field(text, "人工确认", "确认事项"),
    }
    return {key: value for key, value in values.items() if value}


def _document_label(path: str) -> str:
    labels = {
        "prd": "产品需求（PRD）",
        "requirements-matrix": "需求追踪矩阵",
        "project-overview": "项目说明",
        "solution-overview": "解决方案总览",
        "system-architecture": "系统架构",
        "module-domain-design": "模块与领域设计",
        "data-design": "数据设计",
        "frontend-design": "前端设计",
        "ux-ui-design": "UI/UX 设计",
        "api-design": "API 设计",
        "technical-selection": "技术选型",
        "application-development": "应用开发指南",
        "interface-reference": "接口参考",
        "test-plan": "测试计划",
        "test-cases": "测试用例",
        "test-report": "测试报告",
        "release-notes": "发布说明",
        "delivery-package": "交付包",
        "deployment-guide": "部署指南",
        "user-guide": "用户指南",
    }
    stem = Path(path).stem
    return labels.get(stem, stem.replace("-", " ").replace("_", " "))


def _document_category(path: str) -> str:
    normalized = path.casefold()
    if any(value in normalized for value in ("test-", "/tests/", "testing")):
        return "测试文档"
    if any(value in normalized for value in ("04-product", "requirement", "/prd.")):
        return "需求文档"
    if any(value in normalized for value in ("05-design", "/design/", "-design.")):
        return "设计文档"
    if "03-developer-guide" in normalized or "developer" in normalized:
        return "开发文档"
    if any(
        value in normalized
        for value in ("06-delivery", "release", "deployment", "operations", "maintenance")
    ):
        return "发布与运维"
    return "项目说明"


def _documents(root: Path) -> list[dict[str, str]]:
    candidates: set[str] = set()
    project_file = root / ".factory" / "project.json"
    if project_file.is_file():
        try:
            project = json.loads(project_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            project = {}
        if isinstance(project, dict):
            for key in ("human_workflow_docs", "workflow_docs"):
                values = project.get(key)
                if isinstance(values, list):
                    candidates.update(value for value in values if isinstance(value, str))
    doc_map = root / ".factory" / "memory" / "doc-map.md"
    if doc_map.is_file():
        candidates.update(
            match for match in re.findall(r"`(docs/[^`]+)`", doc_map.read_text(encoding="utf-8"))
        )
    paths: set[Path] = set()
    for candidate in candidates:
        if any(character in candidate for character in "*?["):
            paths.update(path for path in root.glob(candidate) if path.is_file())
        else:
            path = root / candidate
            if path.is_file():
                paths.add(path)
    category_order = {
        "需求文档": 0,
        "设计文档": 1,
        "开发文档": 2,
        "测试文档": 3,
        "发布与运维": 4,
        "项目说明": 5,
    }
    document_priority = {
        "prd": 0,
        "requirements-matrix": 1,
        "solution-overview": 0,
        "system-architecture": 1,
        "ux-ui-design": 2,
        "module-domain-design": 3,
        "data-design": 4,
        "api-design": 5,
        "frontend-design": 6,
        "technical-selection": 7,
        "application-development": 0,
        "interface-reference": 1,
        "test-plan": 0,
        "test-cases": 1,
        "test-report": 2,
        "release-notes": 0,
        "deployment-guide": 1,
        "operations-runbook": 2,
        "project-overview": 0,
        "project-charter": 1,
        "user-guide": 2,
        "index": 99,
    }
    documents = []
    for path in paths:
        relative_path = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        match = re.search(
            r"(?mi)^\|\s*(?:文档\s*ID|Document\s*ID)\s*\|\s*`?([A-Za-z0-9._~-]+)`?\s*\|",
            text,
        )
        document_id = (
            match.group(1)
            if match
            else f"DOC-{hashlib.sha1(relative_path.encode()).hexdigest()[:10].upper()}"
        )
        documents.append(
            {
                "id": document_id,
                "path": relative_path,
                "label": _document_label(path.as_posix()),
                "title": _title(text, _document_label(path.as_posix())),
                "category": _document_category(path.as_posix()),
            }
        )
    documents.sort(
        key=lambda document: (
            category_order[document["category"]],
            document_priority.get(Path(document["path"]).stem, 50),
            document["path"],
        )
    )
    return documents


def _sources(root: Path) -> list[Path]:
    paths = [
        root / ".factory" / "project.json",
        root / ".factory" / "memory" / "agent-session.md",
        root / ".factory" / "memory" / "doc-map.md",
    ]
    work_items_root = root / ".factory" / "workitems"
    if work_items_root.exists():
        for directory in sorted(path for path in work_items_root.iterdir() if path.is_dir()):
            paths.extend(
                (directory / "brief.md", directory / "plan.md", directory / "ledger.jsonl")
            )
            task_root = directory / "task-briefs"
            if task_root.is_dir():
                paths.extend(sorted(task_root.glob("*.md")))
    paths.extend(root / document["path"] for document in _documents(root))
    return sorted({path for path in paths if path.is_file()})


def _fingerprint(root: Path, sources: list[Path]) -> str:
    digest = hashlib.sha256()
    digest.update(Path(__file__).read_bytes())
    for path in sources:
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _scope_label(value: str) -> str:
    return {
        "project": "项目级任务",
        "requirement": "需求任务",
        "cross_cutting": "跨领域任务",
        "system": "系统任务",
    }.get(value.lower(), value or "层级未登记")


def _task_type_label(value: str) -> str:
    return {
        "process_design": "流程与治理设计",
        "requirements": "需求设计",
        "implementation": "开发实现",
        "verification": "验证",
    }.get(value.lower(), value or "任务类型未登记")


def _task_nature(task: dict[str, Any]) -> str:
    scope = str(task.get("scope") or "").lower()
    if scope in {"project", "requirement", "cross_cutting", "system"}:
        return scope
    return "requirement" if _relation_ids(str(task.get("relations") or "")) else "project"


def _task_category_label(value: str, status: str = "") -> str:
    normalized = value.lower()
    if not value or "未登记" in value:
        normalized_status = status.lower()
        if "commit" in normalized_status or "closeout" in normalized_status:
            return "提交与收尾"
        if "review" in normalized_status:
            return "评审"
        if any(marker in normalized_status for marker in ("test", "verify")):
            return "测试"
        if any(marker in normalized_status for marker in ("progress", "execut", "implement")):
            return "实施"
        return "其他"
    if any(marker in normalized for marker in ("test", "verification", "测试", "验收", "验证")):
        return "测试"
    if any(marker in normalized for marker in ("review", "评审", "审查")):
        return "评审"
    if any(
        marker in normalized
        for marker in ("implement", "develop", "correction", "fix", "开发", "实现", "修复")
    ):
        return "开发"
    if any(marker in normalized for marker in ("design", "设计", "架构")):
        return "设计"
    if any(marker in normalized for marker in ("requirement", "需求", "分析")):
        return "需求"
    return "其他"


def _empty(message: str) -> str:
    return f'<p class="empty">{html.escape(message)}</p>'


def _display_title(value: str, fallback: str) -> str:
    if not value or re.fullmatch(r"[A-Z0-9._~-]+", value):
        return fallback or value or "标题尚未登记"
    title = re.sub(r"^[A-Z][A-Z0-9._~-]*\s*[：:—-]?\s+", "", value).strip()
    if title.casefold() in {"brief", "task brief", "work item brief"}:
        return fallback
    return title or fallback


def _compact(value: str, limit: int = 180) -> str:
    normalized = " ".join(value.split())
    first_sentence = re.split(r"(?<=[。！？])\s*", normalized, maxsplit=1)[0]
    candidate = first_sentence or normalized
    return candidate if len(candidate) <= limit else f"{candidate[: limit - 1]}…"


def _board_column(task: dict[str, Any]) -> str:
    normalized = str(task["status"]).lower()
    if task["category"] == "completed":
        return "已完成"
    if any(marker in normalized for marker in ("blocked", "changes_requested", "needs_user")):
        return "待确认 / 阻塞"
    if any(marker in normalized for marker in ("test", "verify", "verification")):
        return "测试中"
    if any(marker in normalized for marker in ("review", "confirm", "pending_customer")):
        return "待评审" if "review" in normalized else "待确认 / 阻塞"
    if task["category"] == "attention":
        return "待确认 / 阻塞"
    if task["category"] == "active":
        return "进行中"
    return "待开始"


def _requirement_link(
    requirement_id: str,
    requirements: dict[str, dict[str, str]],
    prefix: str = "",
) -> str:
    requirement = requirements.get(requirement_id, {})
    label = requirement.get("title") or "需求说明待补齐"
    return (
        f'<a class="requirement-link" '
        f'href="{prefix}requirements/{html.escape(requirement_id, quote=True)}.html">'
        f"{html.escape(label)} <small>{html.escape(requirement_id)}</small></a>"
    )


def _requirement_links(
    task: dict[str, Any],
    requirements: dict[str, dict[str, str]],
    prefix: str = "",
) -> str:
    relation_ids = _relation_ids(task["relations"])
    if not relation_ids:
        nature = _task_nature(task)
        if nature in {"project", "system"}:
            return f'<span class="muted">{html.escape(_scope_label(nature))}，不按需求分组</span>'
        return '<span class="muted">需求关系待补录</span>'
    return "、".join(
        _requirement_link(requirement_id, requirements, prefix) for requirement_id in relation_ids
    )


def _board_card(
    task: dict[str, Any],
    requirements: dict[str, dict[str, str]],
) -> str:
    title = _display_title(
        task["title"],
        task["goal"] or task["work_item_title"] or task["work_item_purpose"],
    )
    facts = " · ".join(
        value
        for value in (
            task["module"] if "未登记" not in task["module"] else "",
            _task_type_label(task["task_type"]) if "未登记" not in task["task_type"] else "",
            task["priority"],
        )
        if value
    )
    route = html.escape(task["route"], quote=True)
    return (
        f'<article class="board-card" data-task-id="{html.escape(task["id"], quote=True)}">'
        f'<a class="board-card__title" href="tasks/{route}.html">'
        f"{html.escape(_compact(title, 64))}</a>"
        f'<span class="status">{html.escape(task["status_label"])}</span>'
        f'<div class="board-card__tags tags"><span>{html.escape(_scope_label(_task_nature(task)))}</span>'
        f"<span>{html.escape(_task_category_label(task['task_type'], task['status']))}</span></div>"
        + (f"<small>{html.escape(facts)}</small>" if facts else "")
        + f'<div class="board-card__next"><strong>下一步：{html.escape(task["next_action"])}</strong></div>'
        + f'<a class="board-card__action" href="tasks/{route}.html">查看任务详情 →</a>'
        + "</article>"
    )


def _grouped_board_cards(
    tasks: list[dict[str, Any]],
    requirements: dict[str, dict[str, str]],
) -> str:
    groups: dict[str, list[dict[str, Any]]] = {}
    for task in tasks:
        nature = _task_nature(task)
        requirement_ids = _relation_ids(task["relations"])
        key = (
            f"REQUIREMENT:{requirement_ids[0]}"
            if nature in {"requirement", "cross_cutting"} and requirement_ids
            else f"WORKITEM:{task['work_item_id']}"
        )
        groups.setdefault(key, []).append(task)

    rendered_groups: list[str] = []
    for key, group_tasks in sorted(groups.items(), key=lambda entry: entry[0]):
        if key.startswith("REQUIREMENT:"):
            requirement_id = key.removeprefix("REQUIREMENT:")
            heading = _requirement_link(requirement_id, requirements)
            group_attributes = (
                'class="board-swimlane requirement-group" '
                f'data-requirement-id="{html.escape(requirement_id, quote=True)}"'
            )
        else:
            item_label = _display_title(
                group_tasks[0]["work_item_title"],
                _compact(group_tasks[0]["work_item_purpose"], 42),
            )
            if group_tasks[0]["work_item_has_plan"]:
                group_href = f"plans/{html.escape(group_tasks[0]['work_item_id'], quote=True)}.html"
            else:
                group_task = next(
                    (task for task in group_tasks if task.get("is_current")),
                    group_tasks[0],
                )
                group_href = f"tasks/{html.escape(group_task['route'], quote=True)}.html"
            heading = f'<a href="{group_href}">{html.escape(item_label)}</a>'
            group_attributes = (
                'class="board-swimlane work-item-group" '
                f'data-work-item-id="{html.escape(group_tasks[0]["work_item_id"], quote=True)}"'
            )

        open_attribute = (
            " open"
            if any(
                task.get("is_current") or task["category"] in {"active", "attention"}
                for task in group_tasks
            )
            else ""
        )
        completed = sum(task["category"] == "completed" for task in group_tasks)
        cells = []
        for column in BOARD_COLUMNS:
            column_tasks = sorted(
                (task for task in group_tasks if _board_column(task) == column),
                key=lambda value: (value["updated_at"], value["id"]),
                reverse=True,
            )
            if not column_tasks:
                continue
            cards = "".join(_board_card(task, requirements) for task in column_tasks)
            cells.append(
                '<section class="swimlane-column" '
                f'data-board-column="{html.escape(column, quote=True)}">'
                f"<h4>{html.escape(column)} <span>{len(column_tasks)}</span></h4>"
                f'<div class="board-cards">{cards}</div>'
                "</section>"
            )
        rendered_groups.append(
            f"<details {group_attributes}{open_attribute}>"
            f'<summary class="board-swimlane__heading"><strong>{heading}</strong>'
            f"<span>{completed} / {len(group_tasks)} 已完成</span></summary>"
            f'<div class="swimlane-grid">{"".join(cells)}</div></details>'
        )
    return "".join(rendered_groups)


def _inline_markdown(value: str) -> str:
    rendered = html.escape(value)
    rendered = re.sub(r"`([^`]+)`", r"<code>\1</code>", rendered)
    rendered = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", rendered)

    def link(match: re.Match[str]) -> str:
        label, target = match.groups()
        if target.strip().lower().startswith(("javascript:", "data:")):
            return label
        return f'<a href="{html.escape(target, quote=True)}">{label}</a>'

    return re.sub(r"\[([^\]]+)]\(([^)]+)\)", link, rendered)


def _markdown(text: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    paragraph: list[str] = []
    index = 0

    def flush_paragraph() -> None:
        if paragraph:
            output.append(f"<p>{_inline_markdown(' '.join(paragraph))}</p>")
            paragraph.clear()

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if stripped.startswith("```"):
            flush_paragraph()
            language = stripped[3:].strip()
            code: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code.append(lines[index])
                index += 1
            output.append(
                f'<pre><code class="language-{html.escape(language, quote=True)}">'
                f"{html.escape(chr(10).join(code))}</code></pre>"
            )
        elif (
            "|" in stripped
            and index + 1 < len(lines)
            and re.match(r"^\s*\|?(?:\s*:?-+:?\s*\|)+\s*:?-+:?\s*\|?\s*$", lines[index + 1])
        ):
            flush_paragraph()

            def cells(row: str) -> list[str]:
                return [cell.strip() for cell in row.strip().strip("|").split("|")]

            headers = cells(line)
            index += 2
            rows: list[list[str]] = []
            while index < len(lines) and "|" in lines[index] and lines[index].strip():
                rows.append(cells(lines[index]))
                index += 1
            output.append(
                '<div class="table-scroll"><table><thead><tr>'
                + "".join(f"<th>{_inline_markdown(cell)}</th>" for cell in headers)
                + "</tr></thead><tbody>"
                + "".join(
                    "<tr>" + "".join(f"<td>{_inline_markdown(cell)}</td>" for cell in row) + "</tr>"
                    for row in rows
                )
                + "</tbody></table></div>"
            )
            continue
        elif match := re.match(r"^(#{1,6})\s+(.+)$", stripped):
            flush_paragraph()
            level = len(match.group(1))
            output.append(f"<h{level}>{_inline_markdown(match.group(2))}</h{level}>")
        elif re.match(r"^[-*]\s+", stripped):
            flush_paragraph()
            values = []
            while index < len(lines) and re.match(r"^\s*[-*]\s+", lines[index]):
                values.append(re.sub(r"^\s*[-*]\s+", "", lines[index]).strip())
                index += 1
            output.append(
                "<ul>"
                + "".join(f"<li>{_inline_markdown(value)}</li>" for value in values)
                + "</ul>"
            )
            continue
        elif re.match(r"^\d+\.\s+", stripped):
            flush_paragraph()
            values = []
            while index < len(lines) and re.match(r"^\s*\d+\.\s+", lines[index]):
                values.append(re.sub(r"^\s*\d+\.\s+", "", lines[index]).strip())
                index += 1
            output.append(
                "<ol>"
                + "".join(f"<li>{_inline_markdown(value)}</li>" for value in values)
                + "</ol>"
            )
            continue
        elif stripped.startswith(">"):
            flush_paragraph()
            output.append(f"<blockquote>{_inline_markdown(stripped.lstrip('> '))}</blockquote>")
        elif not stripped:
            flush_paragraph()
        else:
            paragraph.append(stripped)
        index += 1
    flush_paragraph()
    return "\n".join(output)


def _navigation(prefix: str = "", active: str = "") -> str:
    links = "".join(
        f'<li><a href="{prefix}{filename}"'
        + (' aria-current="page"' if view == active else "")
        + f">{label}</a></li>"
        for view, filename, label in VIEW_LINKS
    )
    return f'<span class="sr-only">负责人视图（6 项）</span><ul class="nav-tabs">{links}</ul>'


def _detail_page(
    title: str,
    subtitle: str,
    content: str,
    return_page: str,
    active_view: str,
) -> str:
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<style>
:root{{font-family:Inter,"PingFang SC","Microsoft YaHei",system-ui,sans-serif;color:#18202f;background:#f3f5f8}}
*{{box-sizing:border-box}}body{{margin:0;line-height:1.7}}header,main{{width:min(920px,calc(100% - 28px));margin:auto}}
header{{padding-top:18px}}main{{margin-top:18px;margin-bottom:64px;
background:#fff;border:1px solid #d9dee8;border-radius:16px;padding:clamp(20px,4vw,46px)}}
a{{color:#2855d9}}nav{{overflow-x:auto;border:1px solid #d9dee8;border-radius:14px;background:#fff}}nav ul{{display:flex;
flex-wrap:nowrap;min-width:max-content;gap:4px;margin:0;padding:8px;list-style:none}}nav a{{display:block;padding:7px 10px;border-radius:9px;
text-decoration:none;font-size:.88rem;font-weight:720;white-space:nowrap}}nav a[aria-current="page"]{{background:#edf2ff;color:#2855d9}}
.sr-only{{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);
white-space:nowrap;border:0}}.back{{display:inline-block;margin-bottom:20px;text-decoration:none;font-weight:750}}
.subtitle{{color:#657085}}h1,h2,h3{{line-height:1.3}}code{{overflow-wrap:anywhere}}pre{{overflow:auto;padding:16px;
background:#f3f5f8;border-radius:10px}}blockquote{{margin-left:0;padding-left:16px;border-left:4px solid #2855d9;color:#657085}}
.table-scroll{{max-width:100%;overflow-x:auto}}table{{width:100%;border-collapse:collapse;min-width:560px}}
th,td{{padding:10px;text-align:left;vertical-align:top;border:1px solid #d9dee8}}th{{background:#f3f5f8}}
.facts{{display:grid;grid-template-columns:max-content 1fr;gap:6px 16px}}dt{{font-weight:750}}dd{{margin:0}}
.plan-outline{{display:grid;gap:9px;padding:0;list-style:none}}.plan-outline li,.daily-progress{{
padding:12px;border:1px solid #d9dee8;border-radius:10px}}.plan-outline li span,.plan-outline li small{{
display:block;color:#657085}}.daily-progress h3{{margin-top:0}}
.route-tree{{padding-left:1.3rem}}.route-tree li{{margin:8px 0;padding:9px 11px;
border-left:3px solid #d9dee8;background:#f8f9fb}}.route-tree li.current{{border-left-color:#2855d9}}
.route-tree small{{display:block;color:#657085}}
@media(max-width:520px){{main{{margin-top:10px}}.facts{{grid-template-columns:1fr;gap:2px}}dd{{margin-bottom:8px}}}}
</style></head><body><header><nav aria-label="项目快照导航">{_navigation("../", active_view)}</nav></header>
<main><a class="back" href="../{return_page}">← 返回{dict((view, label) for view, _, label in VIEW_LINKS)[active_view]}</a>
<p class="subtitle">{html.escape(subtitle)}</p>{content}</main></body></html>"""


def _status_counts(records: list[dict[str, Any]]) -> dict[str, int]:
    return {
        category: sum(record["category"] == category for record in records)
        for category in ("attention", "active", "backlog", "completed")
    }


def _render(
    project: dict[str, str],
    session: dict[str, str],
    items: list[dict[str, Any]],
    documents: list[dict[str, str]],
) -> str:
    item_counts = _status_counts(items)
    primary_id = session.get("工作项", "")
    focus = next((item for item in items if item["id"] == primary_id), None)
    focus = focus or next((item for item in items if item["category"] == "active"), None)
    focus = focus or next((item for item in items if item["category"] == "attention"), None)
    primary_task_id = session.get("任务") or str((focus or {}).get("task_id") or "")
    primary_task = next(
        (task for task in (focus or {}).get("tasks", []) if task["id"] == primary_task_id),
        None,
    )
    active_items = [item for item in items if item["category"] in {"attention", "active"}]
    current_stage = str(
        project.get("stage") or (focus or {}).get("stage") or session.get("阶段") or "阶段尚未登记"
    )
    current_task = _display_title(
        str(
            (primary_task or {}).get("title")
            or (focus or {}).get("task_title")
            or (focus or {}).get("title")
            or "当前任务尚未登记"
        ),
        str(
            (primary_task or {}).get("goal")
            or (focus or {}).get("purpose")
            or session.get("当前焦点")
            or "当前任务尚未登记"
        ),
    )
    current_focus = session.get("当前焦点") or str(
        (focus or {}).get("purpose") or "当前焦点尚未登记"
    )
    confirmation = session.get("确认事项", "")
    stop_reason = str((focus or {}).get("stop_reason") or "")
    if not stop_reason and (focus or {}).get("human_confirmation_required"):
        stop_reason = (
            f"等待人工确认：{confirmation or (focus or {}).get('gate_reason') or '确认事项未登记'}"
        )
    stop_reason = stop_reason or session.get("停止原因") or "无"
    next_action = str((focus or {}).get("next_action") or "")
    if next_action == "等待人工确认" and confirmation:
        next_action = f"确认{confirmation}"
    next_action = next_action or session.get("唯一下一动作") or "下一步尚未登记"
    current_position = str(
        session.get("位置")
        or (f"{(focus or {}).get('id')} / {primary_task_id}" if focus else "尚未登记")
    )
    mainline_status = str((focus or {}).get("status_label") or "状态尚未登记")
    parallel_candidates = sorted(
        (item for item in active_items if item is not focus),
        key=lambda item: item["updated_at"],
        reverse=True,
    )
    parallel_items = parallel_candidates[:1]
    paused_items = parallel_candidates[1:] + [
        item for item in items if item["category"] == "backlog"
    ]
    visible_work_items = ([focus] if focus else []) + parallel_items
    tasks = [
        task
        for item in visible_work_items
        for task in item["tasks"]
        if task["category"] in {"attention", "active"}
    ]
    planned_markers = ("planned", "not_started", "todo", "backlog")
    board_tasks = [
        task
        for item in visible_work_items
        for task in item["tasks"]
        if task["is_current"]
        or task["category"] == "completed"
        or any(marker in task["brief_status"].lower() for marker in planned_markers)
    ]
    history_tasks = [
        task for item in items if item["category"] == "completed" for task in item["tasks"]
    ]
    requirements = {
        requirement["id"]: requirement for item in items for requirement in item["requirements"]
    }
    product_goal = _compact(
        str((focus or {}).get("purpose") or project.get("idea") or "项目目标尚未登记。")
    )
    project_definition = _compact(
        str(project.get("definition") or project.get("idea") or "项目定义尚未登记。"),
        260,
    )
    project_problem = _compact(
        str(project.get("problem") or project.get("idea") or product_goal),
        220,
    )
    project_delivery = _compact(
        str(project.get("delivery") or "交付范围尚未在正式架构文档中登记。"),
        220,
    )
    current_task_goal = _compact(str((primary_task or {}).get("goal") or product_goal))
    current_work_type = _task_type_label(str((primary_task or {}).get("task_type") or ""))

    stage_labels = (
        ("BRAINSTORM", "意图与立项"),
        ("REQUIREMENTS", "需求"),
        ("ANALYSIS", "分析"),
        ("DESIGN", "设计"),
        ("PLAN", "计划"),
        ("IMPLEMENTATION", "开发实现"),
        ("TESTING", "测试"),
        ("ACCEPTANCE", "验收"),
        ("RELEASE", "发布"),
        ("MAINTENANCE", "维护"),
    )
    current_stage_label = dict(stage_labels).get(
        current_stage.upper(),
        current_stage,
    )
    roadmap_tasks = (focus or {}).get("plan_stages", [])
    roadmap_nodes = (focus or {}).get("plan_nodes", [])
    roadmap_nodes_by_id = {node["id"]: node for node in roadmap_nodes}
    stage_cards = [
        f'<li class="stage-card{" current" if task["state"] == "current" else ""}">'
        f'<a class="stage-card__link" href="stages/{html.escape(task["id"], quote=True)}.html">'
        f'<span class="stage-index">{index:02d}</span>'
        f"<strong>{html.escape(task['title'])}</strong>"
        f"<small>{html.escape(task['label'])} · "
        f"{len(roadmap_nodes_by_id.get(task['id'], {}).get('children', []))} 个直接子步骤"
        "</small></a></li>"
        for index, task in enumerate(roadmap_tasks, 1)
    ]
    completed_stages = sum(stage["state"] == "completed" for stage in roadmap_tasks)
    planned_stages = sum(stage["state"] == "planned" for stage in roadmap_tasks)
    roadmap_summary = (
        f"当前主线完成 {completed_stages} / {len(roadmap_tasks)} 步"
        if roadmap_tasks
        else "主线计划尚未登记"
    )

    def item_route_task(item: dict[str, Any]) -> dict[str, Any]:
        return next(
            (task for task in item["tasks"] if task["id"] == item["task_id"]),
            next((task for task in item["tasks"] if task["is_current"]), item["tasks"][0]),
        )

    def roadmap_action(item: dict[str, Any]) -> str:
        if item["plan_stages"]:
            href = f"plans/{html.escape(item['id'], quote=True)}.html"
            label = "查看计划"
        else:
            href = f"tasks/{html.escape(item_route_task(item)['route'], quote=True)}.html"
            label = "查看任务路线"
        return f'<a class="roadmap-card__action" href="{href}">{label} →</a>'

    roadmap_items_html = "".join(
        '<article class="list-card">'
        + (
            f'<h3><a href="plans/{html.escape(item["id"], quote=True)}.html">'
            f"{html.escape(_compact(_display_title(item['title'], item['purpose']), 80))}</a></h3>"
            if item["plan_stages"]
            else f"<h3>{html.escape(_compact(_display_title(item['title'], item['purpose']), 80))}</h3>"
        )
        + f"<p><strong>状态：</strong>{html.escape(item['status_label'])}</p>"
        f"<p><strong>计划层级：</strong>{len(item['plan_stages'])} 个阶段 · {len(item['tasks'])} 个任务</p>"
        f"<p><strong>最近进展：</strong>{html.escape(item['updated_at'][:10] or '日期未登记')}</p>"
        + roadmap_action(item)
        + "</article>"
        for item in visible_work_items
    )
    roadmap_other_html = "".join(
        '<article class="list-card">'
        f"<h3>{html.escape(_compact(_display_title(item['title'], item['purpose']), 64))}</h3>"
        f"<p><strong>状态：</strong>{html.escape(item['status_label'])}</p>"
        f"<p><strong>下一步：</strong>{html.escape(item['next_action'])}</p>"
        + roadmap_action(item)
        + "</article>"
        for item in paused_items
        if item["category"] in {"attention", "active"}
    )
    board_html = _grouped_board_cards(board_tasks, requirements)
    board_status_summary = "".join(
        f'<span tabindex="0" data-board-summary="{html.escape(column, quote=True)}">'
        f"<strong>{sum(_board_column(task) == column for task in board_tasks)}</strong>"
        f"{html.escape(column)}</span>"
        for column in BOARD_COLUMNS
    )
    history_html = "".join(
        "<li>"
        f'<a href="tasks/{html.escape(task["route"], quote=True)}.html">'
        f"{html.escape(_compact(_display_title(task['title'], task['goal']), 80))}</a>"
        f"<small>{html.escape(task['work_item_id'])} · {html.escape(task['status_label'])}</small>"
        "</li>"
        for task in sorted(
            history_tasks,
            key=lambda task: (task["updated_at"], task["id"]),
            reverse=True,
        )
    )
    milestone_rows = [
        item for item in visible_work_items if item["milestone"] or item["target_date"]
    ]
    milestones_html = "".join(
        '<article class="list-card">'
        f"<h3>{html.escape(item['milestone'] or item['title'])}</h3>"
        f"<p>{html.escape(item['title'])}</p>"
        f"<p><strong>目标日期：</strong>{html.escape(item['target_date'] or '尚未登记')}</p>"
        f"<p><strong>状态：</strong>{html.escape(item['status_label'])}</p>"
        + roadmap_action(item)
        + "</article>"
        for item in milestone_rows
    )

    attention_items = [item for item in visible_work_items if item["category"] == "attention"]
    risk_cards = []
    for item in attention_items:
        title = _display_title(
            str(item.get("task_title") or item["title"]),
            str(item.get("task_goal") or item["title"] or item["purpose"]),
        )
        owner = (
            "人工确认方尚未登记"
            if item.get("human_confirmation_required")
            else item["owner"] or "责任人尚未登记"
        )
        reason = item["stop_reason"] or item["status_label"]
        if item is focus and confirmation:
            reason = f"等待确认：{confirmation}"
        item_next_action = next_action if item is focus else item["next_action"]
        risk_cards.append(
            '<article class="list-card list-card--attention">'
            f"<h3>{html.escape(title)}</h3>"
            f"<p><strong>原因：</strong>{html.escape(reason)}</p>"
            f"<p><strong>影响：</strong>未处理前，依赖该事项的后续工作保持暂停。</p>"
            f"<p><strong>需求模块：</strong>{html.escape(item['module'] or '需求模块未登记')}</p>"
            f"<p><strong>责任人：</strong>{html.escape(owner)}</p>"
            f"<p><strong>截止日期：</strong>{html.escape(item['target_date'] or '未排期')}</p>"
            f"<p><strong>下一步：</strong>{html.escape(item_next_action)}</p>"
            "</article>"
        )
    risk_html = "".join(risk_cards)
    decision_records: list[dict[str, str]] = []
    quality_records: list[dict[str, str]] = []
    deliverables: list[dict[str, str]] = []
    versions: list[dict[str, str]] = []
    for item in items:
        seen_outputs: set[str] = set()
        seen_commits: set[str] = set()
        for event in reversed(item["events"]):
            event_type = str(event.get("event_type") or event.get("event") or "")
            normalized = f"{event_type} {event.get('status', '')}".lower()
            record = {
                "item": item["title"],
                "time": _event_time(event),
                "event": event_type or "事件类型未登记",
                "status": str(event.get("status") or "状态未登记"),
                "actor": str(event.get("actor") or "责任人未登记"),
            }
            if str(event.get("actor_type") or "").lower() == "human" or any(
                marker in normalized
                for marker in ("decision", "confirm", "approve", "reopen", "supersed", "change")
            ):
                decision_records.append(record)
            if any(marker in normalized for marker in ("review", "verif", "test")):
                evidence = _values(
                    [event],
                    "evidence",
                    "evidences",
                    "report",
                    "review",
                )
                record["evidence"] = evidence[0] if evidence else ""
                quality_records.append(record)
            for output in _values([event], "outputs", "output"):
                if output not in seen_outputs:
                    deliverables.append(
                        {"item": item["title"], "path": output, "time": _event_time(event)}
                    )
                    seen_outputs.add(output)
            for commit in _values(
                [event],
                "commits",
                "commit",
                "commit_sha",
                "local_commit",
            ):
                if commit not in seen_commits:
                    versions.append(
                        {"item": item["title"], "commit": commit, "time": _event_time(event)}
                    )
                    seen_commits.add(commit)
    decision_records.sort(key=lambda record: record["time"], reverse=True)
    quality_records.sort(key=lambda record: record["time"], reverse=True)
    deliverables.sort(key=lambda record: record["time"], reverse=True)
    versions.sort(key=lambda record: record["time"], reverse=True)

    decisions_html = "".join(
        "<li><strong>"
        f"{html.escape(record['item'])}</strong> · {html.escape(record['event'])}"
        f" · {html.escape(record['actor'])}"
        + (f"<small>{html.escape(record['time'])}</small>" if record["time"] else "")
        + "</li>"
        for record in decision_records[:12]
    )
    quality_html = "".join(
        "<li><strong>"
        f"{html.escape(record['item'])}</strong> · {html.escape(record['status'])}"
        + (f"<br><code>{html.escape(record['evidence'])}</code>" if record.get("evidence") else "")
        + "</li>"
        for record in quality_records[:12]
    )
    deliverables_html = "".join(
        "<li><strong>"
        f"{html.escape(record['item'])}</strong><br>"
        f"<code>{html.escape(record['path'])}</code></li>"
        for record in deliverables[:20]
    )
    versions_html = "".join(
        "<li><strong>"
        f"{html.escape(record['item'])}</strong> · "
        f"<code>{html.escape(record['commit'])}</code>"
        + (f"<small>{html.escape(record['time'])}</small>" if record["time"] else "")
        + "</li>"
        for record in versions[:20]
    )

    trace_rows = "".join(
        "<tr>"
        f"<td>{html.escape(task['module'])}</td>"
        f"<td>{html.escape(task['relations'] or '尚未登记')}</td>"
        f"<td>{html.escape(task['title'])}<small>{html.escape(task['id'])}</small></td>"
        f"<td>{html.escape(task['outputs'][0] if task['outputs'] else '尚未登记')}</td>"
        f"<td>{html.escape(task['evidence'][0] if task['evidence'] else '尚未登记')}</td>"
        f"<td>{html.escape(task['commits'][0] if task['commits'] else '尚未登记')}</td>"
        "</tr>"
        for task in tasks
    )

    focus_label = (
        _compact(_display_title(focus["title"], focus["purpose"]), 80) if focus else "尚未登记"
    )
    parallel_label = (
        _compact(_display_title(parallel_items[0]["title"], parallel_items[0]["purpose"]), 80)
        if parallel_items
        else "无"
    )
    paused_html = "".join(
        "<li><strong>"
        f"{html.escape(_compact(_display_title(item['title'], item['purpose']), 80))}</strong>"
        f" · {html.escape(item['status_label'])}" + roadmap_action(item) + "</li>"
        for item in paused_items
    )

    primary_quality = [
        event
        for event in (focus or {}).get("events", [])
        if any(
            marker
            in f"{event.get('event_type', '')} {event.get('event', '')} {event.get('status', '')}".lower()
            for marker in ("review", "verif", "test")
        )
    ]
    document_counts = {
        category: sum(document["category"] == category for document in documents)
        for category in (
            "需求文档",
            "设计文档",
            "开发文档",
            "测试文档",
            "发布与运维",
        )
    }
    verification_summary = "尚未登记当前主线验证"
    if primary_quality:
        latest_quality = primary_quality[-1]
        verification = latest_quality.get("verification")
        if isinstance(verification, dict) and verification.get("status") == "passed":
            verification_summary = "验证已通过"
        elif latest_quality.get("review_score") is not None:
            verification_summary = f"独立评审 {latest_quality['review_score']} / 100"
        else:
            quality_status = str(latest_quality.get("status") or "")
            verification_summary = _status_label(
                quality_status,
                _category(quality_status),
            )
    readiness_rows = (
        (
            "需求",
            f"{document_counts['需求文档']} 份正式文档"
            if document_counts["需求文档"]
            else "尚未登记需求文档",
            "ok" if document_counts["需求文档"] else "attention",
        ),
        (
            "设计",
            f"{document_counts['设计文档']} 份正式文档"
            if document_counts["设计文档"]
            else "尚未登记设计文档",
            "ok" if document_counts["设计文档"] else "attention",
        ),
        (
            "实现",
            mainline_status,
            "attention" if (focus or {}).get("category") == "attention" else "active",
        ),
        (
            "验证",
            verification_summary,
            "ok" if primary_quality else "attention",
        ),
        (
            "审批",
            "等待人工确认"
            if (focus or {}).get("human_confirmation_required")
            else "未登记人工 Gate",
            "attention" if (focus or {}).get("human_confirmation_required") else "neutral",
        ),
        (
            "发布",
            "已有版本证据，未声明发布就绪" if (focus or {}).get("commits") else "尚未登记发布结论",
            "neutral",
        ),
    )
    readiness_html = "".join(
        f'<article class="readiness-card readiness-card--{state}">'
        f"<span>{html.escape(name)}</span><strong>{html.escape(value)}</strong></article>"
        for name, value, state in readiness_rows
    )

    document_categories = (
        "需求文档",
        "设计文档",
        "开发文档",
        "测试文档",
        "发布与运维",
        "项目说明",
    )
    document_groups = []
    for category in document_categories:
        category_documents = [
            document for document in documents if document["category"] == category
        ]
        links = "".join(
            '<a class="doc-link" '
            f'href="documents/{html.escape(document["id"], quote=True)}.html">'
            f"<strong>{html.escape(document['label'])}</strong>"
            f"<small>{html.escape(document['path'])}</small></a>"
            for document in category_documents[:6]
        )
        more = "".join(
            '<a class="doc-link" '
            f'href="documents/{html.escape(document["id"], quote=True)}.html">'
            f"<strong>{html.escape(document['label'])}</strong>"
            f"<small>{html.escape(document['path'])}</small></a>"
            for document in category_documents[6:]
        )
        document_groups.append(
            '<article class="document-group">'
            f"<h3>{category} <small>{len(category_documents)} 份</small></h3>"
            f'<div class="doc-links">{links or _empty("尚未登记")}</div>'
            + (
                f'<details class="technical"><summary>更多文档（{len(category_documents) - 6}）</summary>'
                f'<div class="doc-links">{more}</div></details>'
                if more
                else ""
            )
            + "</article>"
        )
    documents_html = "".join(document_groups)

    content_domains = (
        "项目总览",
        "阶段",
        "需求",
        "任务",
        "里程碑",
        "风险与决策",
        "质量",
        "交付物",
        "追踪链",
        "版本变更",
    )
    domain_html = "".join(f"<span>{value}</span>" for value in content_domains)
    nav_html = _navigation()
    session_html = "".join(
        f"<dt>{html.escape(key)}</dt><dd>{html.escape(value)}</dd>"
        for key, value in session.items()
        if key != "唯一下一动作" or value == next_action
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(project["name"])} · 项目实时看板</title>
<style>
:root {{
  color-scheme:light dark;font-family:Inter,"PingFang SC","Microsoft YaHei",system-ui,sans-serif;
  --bg:#f3f5f8;--surface:#fff;--surface-2:#f8f9fb;--text:#18202f;--muted:#657085;
  --line:#d9dee8;--accent:#2855d9;--accent-soft:#edf2ff;--attention:#a63b18;
  --attention-soft:#fff1e9;--success:#13795b;--radius:16px;--shadow:0 8px 28px #17203312;
}}
@media(prefers-color-scheme:dark) {{
  :root{{--bg:#0d1119;--surface:#151b26;--surface-2:#1b2330;--text:#eef3ff;--muted:#aab5c8;
  --line:#344055;--accent:#94b2ff;--accent-soft:#1e315d;--attention:#ffb18b;
  --attention-soft:#42271d;--success:#7bd9b8;--shadow:none;}}
}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth;scroll-padding-top:88px}}
body{{margin:0;background:var(--bg);color:var(--text);line-height:1.65;overflow-wrap:anywhere}}
a{{color:inherit}}code{{overflow-wrap:anywhere}}h1,h2,h3,h4{{line-height:1.25;overflow-wrap:anywhere}}
header,main{{width:min(1400px,calc(100% - 32px));margin:auto}}
header{{padding:28px 0 18px}}main{{padding-bottom:64px}}
.skip-link{{position:absolute;left:12px;top:-64px;background:var(--surface);padding:10px 14px;
  border-radius:10px;z-index:4}}.skip-link:focus{{top:12px}}
.brand{{display:flex;align-items:center;gap:12px;font-weight:850;font-size:1.15rem}}
.brand-mark{{display:grid;place-items:center;width:36px;height:36px;border-radius:11px;
  background:var(--accent);color:#fff}}nav{{margin-top:18px;border:1px solid var(--line);
  border-radius:14px;background:var(--surface);box-shadow:var(--shadow);overflow-x:auto}}
nav ul{{display:flex;flex-wrap:nowrap;min-width:max-content;gap:4px;margin:0;padding:8px;list-style:none}}
nav a{{display:block;padding:7px 10px;border-radius:9px;text-decoration:none;font-size:.88rem;font-weight:720;white-space:nowrap}}
nav a:hover,nav a[aria-current="page"]{{background:var(--accent-soft);color:var(--accent)}}
a:focus-visible,summary:focus-visible{{outline:3px solid var(--accent);outline-offset:3px}}
.sr-only{{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;
  clip:rect(0,0,0,0);white-space:nowrap;border:0}}
.panel,.hero{{margin-top:22px;border:1px solid var(--line);border-radius:var(--radius);
  background:var(--surface);box-shadow:var(--shadow)}}
.panel{{padding:26px}}.hero{{padding:clamp(24px,4vw,44px);background:
  linear-gradient(135deg,var(--surface),var(--accent-soft))}}
.eyebrow{{margin:0;color:var(--accent);font-size:.78rem;font-weight:850;letter-spacing:.1em}}
.hero h1{{margin:.25rem 0;font-size:clamp(2rem,5vw,3.7rem)}}.hero h2{{margin:1.5rem 0 .5rem}}
.lede,.muted,.work-id,small{{color:var(--muted)}}small{{display:block;font-size:.78rem}}
.hero-grid,.intro-grid,.metrics,.cards,.module-grid,.list-grid,.lane-grid,.readiness-grid,
.document-grid,.doc-links{{display:grid;gap:14px}}
.intro-grid{{grid-template-columns:repeat(2,minmax(0,1fr));margin:20px 0}}
.intro-card{{min-width:0;border-left:4px solid var(--accent);padding:4px 16px}}
.intro-card h2{{margin:0 0 4px;font-size:1rem}}.intro-card p{{margin:0}}
.hero-grid{{grid-template-columns:minmax(0,1.5fr) minmax(260px,.8fr);margin-top:24px}}
.focus-box,.position-box,.metric,.module-card,.task-card,.list-card,.next-card{{
  min-width:0;border:1px solid var(--line);border-radius:14px;background:var(--surface);padding:18px}}
.focus-box{{border-color:var(--accent)}}.position-box dl{{margin:0}}
.metrics{{grid-template-columns:repeat(5,minmax(0,1fr));margin-top:14px}}
.metric strong{{display:block;font-size:1.65rem}}.metric span{{color:var(--muted);font-size:.84rem}}
.section-heading{{display:flex;justify-content:space-between;align-items:end;gap:20px;margin-bottom:18px}}
.section-heading h2{{margin:0}}.section-heading p{{max-width:680px;margin:0;color:var(--muted)}}
.section-action,.roadmap-card__action,.board-card__action{{display:inline-block;
  margin-top:10px;color:var(--accent);font-weight:800;text-decoration:underline;text-underline-offset:3px}}
.stage-list{{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;padding:0;list-style:none}}
.stage-card{{border:1px solid var(--line);border-radius:12px;background:var(--surface-2);
  overflow:hidden}}.stage-card__link{{display:flex;min-height:100%;flex-direction:column;gap:4px;
  padding:14px;color:inherit;text-decoration:none}}.stage-card:hover{{border-color:var(--accent)}}
.stage-card.current{{border-color:var(--accent);
  box-shadow:inset 0 0 0 1px var(--accent)}}.stage-index{{color:var(--accent);font-weight:850}}
.module-grid,.list-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}
.lane-grid,.document-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}
.readiness-card,.document-group{{min-width:0;border:1px solid var(--line);
  border-radius:14px;background:var(--surface-2);padding:18px}}
.paused,.audit{{margin-top:18px;border-top:1px solid var(--line);padding-top:16px}}
.paused>summary,.audit>summary{{font-weight:850;font-size:1.05rem}}
.scope-summary{{display:flex;flex-wrap:wrap;gap:10px 22px;padding:12px 0;
  border-block:1px solid var(--line)}}.scope-summary span{{color:var(--muted)}}
.scope-summary strong{{margin-right:6px;color:var(--text)}}.scope-list{{padding-left:1.2rem}}
.scope-list li{{margin:8px 0}}.scope-list .roadmap-card__action{{margin:0 0 0 8px}}
.summary-strip{{display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px;
  margin-bottom:16px;padding:12px 14px;border-radius:12px;background:var(--surface-2)}}
.readiness-grid{{grid-template-columns:repeat(3,minmax(0,1fr))}}
.readiness-card span{{display:block;color:var(--muted);font-size:.82rem}}
.readiness-card strong{{display:block;margin-top:5px}}.readiness-card--attention{{border-color:var(--attention)}}
.readiness-card--ok{{border-color:var(--success)}}.doc-links{{gap:8px}}
.doc-link{{display:block;padding:11px 12px;border:1px solid var(--line);border-radius:10px;
  text-decoration:none;background:var(--surface)}}.doc-link:hover{{border-color:var(--accent);
  color:var(--accent)}}.document-group h3{{margin-top:0}}.domain-list{{display:flex;
  flex-wrap:wrap;gap:8px;margin:16px 0}}.domain-list span{{padding:4px 9px;border-radius:999px;
  background:var(--accent-soft);color:var(--accent);font-size:.8rem;font-weight:800}}
.module-card h3,.list-card h3,.next-card h3{{margin:.15rem 0 .45rem}}
.legend,.tags{{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}}
.legend span,.tags span,.status{{display:inline-block;border-radius:999px;padding:3px 9px;
  background:var(--accent-soft);color:var(--accent);font-size:.78rem;font-weight:800}}
.module-tasks{{margin-top:12px;border:1px solid var(--line);border-radius:14px;padding:16px}}
.module-tasks>summary{{font-size:1.1rem;font-weight:850;cursor:pointer}}
.type-group{{margin-top:18px}}.type-group h4{{margin:.25rem 0 10px}}
.cards{{grid-template-columns:repeat(2,minmax(0,1fr))}}.card-heading{{display:flex;
  justify-content:space-between;align-items:flex-start;gap:12px}}.task-card h4{{margin:0}}
.task-card--attention,.list-card--attention{{border-color:var(--attention);
  background:var(--attention-soft)}}.task-card--attention .status{{color:var(--attention);
  background:transparent;border:1px solid currentColor}}.attention-text{{color:var(--attention)}}
.next{{margin-top:16px}}.technical{{margin-top:14px;color:var(--muted)}}
summary{{cursor:pointer}}dl{{display:grid;grid-template-columns:max-content 1fr;gap:6px 14px}}
dt{{font-weight:750}}dd{{margin:0;overflow-wrap:anywhere}}ul.record-list{{padding-left:1.2rem}}
.record-list li{{margin:10px 0}}.empty{{margin:0;padding:18px;border:1px dashed var(--line);
  border-radius:12px;color:var(--muted);background:var(--surface-2)}}
.table-scroll{{max-width:100%;overflow-x:auto;border:1px solid var(--line);border-radius:12px}}
table{{width:100%;min-width:900px;border-collapse:collapse}}th,td{{padding:12px;text-align:left;
  vertical-align:top;border-bottom:1px solid var(--line)}}th{{background:var(--surface-2)}}
.source-note{{margin-top:18px;padding-top:16px;border-top:1px solid var(--line);color:var(--muted)}}
.board-summary{{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:8px;
  margin:12px 0 18px}}.board-summary span{{padding:8px 10px;border-radius:10px;
  background:var(--surface-2);color:var(--muted);font-size:.78rem}}
.board-summary strong{{display:block;color:var(--text);font-size:1.05rem}}
.swimlane-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:0 18px}}
.board-swimlane{{border-bottom:1px solid var(--line)}}
.board-swimlane__heading{{display:flex;align-items:center;justify-content:space-between;gap:12px;
  padding:13px 12px;background:var(--surface)}}.board-swimlane__heading strong{{min-width:0}}
.board-swimlane__heading strong a{{color:var(--accent);text-decoration:underline}}
.board-swimlane__heading>span{{flex:0 0 auto;color:var(--muted);font-size:.78rem}}
.swimlane-column{{min-width:0;padding:0 12px 10px}}
.swimlane-column h4{{display:flex;justify-content:space-between;margin:10px 0 0;font-size:.84rem}}
.board-cards{{display:grid}}.board-card{{min-width:0;padding:12px 0;border-bottom:1px solid var(--line)}}
.board-card:last-child{{border-bottom:0}}.board-card__title{{display:block;font-weight:850;
  line-height:1.35;text-decoration:none}}.board-card__title:hover{{color:var(--accent)}}
.board-card .status{{margin:7px 0}}.board-card small{{margin-top:5px}}
.board-card__next{{margin-top:8px;font-size:.82rem}}.board-history{{margin-top:18px}}
.history-list{{columns:2;padding-left:1.2rem}}.history-list li{{break-inside:avoid;margin:8px 0}}
@media(prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
@media(max-width:820px){{.metrics{{grid-template-columns:repeat(2,minmax(0,1fr))}}
  .stage-list{{grid-template-columns:repeat(2,minmax(0,1fr))}}.hero-grid,.intro-grid,.cards,.module-grid,
  .list-grid,.lane-grid,.document-grid{{grid-template-columns:1fr}}
  .readiness-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}
  .board-summary{{grid-template-columns:repeat(3,minmax(0,1fr))}}
  .swimlane-grid{{grid-template-columns:1fr}}
  .history-list{{columns:1}}}}
@media(max-width:480px){{header,main{{width:min(100% - 20px,1400px)}}header{{padding-top:18px}}
  .panel,.hero{{padding:18px}}nav a{{padding:8px}}.metrics,.stage-list,.readiness-grid,
  .board-summary{{grid-template-columns:1fr}}.section-heading,.card-heading{{
  display:block}}.status{{margin-top:8px}}dl{{grid-template-columns:1fr;gap:2px}}dd{{margin-bottom:8px}}
  .board-swimlane__heading{{align-items:flex-start}}}}
</style>
</head>
<body>
<a class="skip-link" href="#main">跳到主要内容</a>
<header>
<div class="brand"><span class="brand-mark">S</span>{html.escape(project["name"])} · 实时看板</div>
<nav aria-label="项目快照导航">{nav_html}</nav>
</header>
<main id="main">
<!-- VIEW:overview -->
<section id="overview" class="hero" aria-labelledby="overview-title">
<p class="eyebrow">30 秒接手摘要</p>
<h1 id="overview-title">{html.escape(project["name"])}</h1>
<p class="lede">{html.escape(project_definition)}</p>
<div class="intro-grid">
<article class="intro-card"><h2>要解决什么</h2><p>{html.escape(project_problem)}</p></article>
<article class="intro-card"><h2>会交付什么</h2><p>{html.escape(project_delivery)}</p></article>
</div>
<div class="hero-grid">
<div class="focus-box"><p class="eyebrow">产品主线</p><h2>{html.escape(current_focus)}</h2>
<p><strong>主线目标：</strong>{html.escape(product_goal)}</p>
<p><strong>本步验收：</strong>{html.escape(current_task_goal)}</p>
<p><strong>当前任务：</strong>{html.escape(current_task)}</p>
<p class="next"><strong>唯一下一动作：{html.escape(next_action)}</strong></p></div>
<div class="position-box"><p class="eyebrow">项目位置</p><dl>
<dt>项目生命周期阶段</dt><dd>{html.escape(current_stage_label)}</dd>
<dt>当前工作类型</dt><dd>{html.escape(current_work_type)}</dd>
<dt>当前里程碑</dt><dd>{html.escape(current_position)}</dd>
<dt>主线状态</dt><dd>{html.escape(mainline_status)}</dd>
<dt>停止原因</dt><dd>{html.escape(stop_reason)}</dd>
<dt>项目负责人</dt><dd>{html.escape(project["owner"] or "尚未登记")}</dd>
</dl></div></div>
<div class="metrics">
<div class="metric"><strong>{len(parallel_items)}</strong><span>可并行工作</span></div>
<div class="metric"><strong>{len(attention_items)}</strong><span>待处理阻塞与决策</span></div>
<div class="metric"><strong>{len(paused_items)}</strong><span>未纳入当前会话 / 后续</span></div>
<div class="metric"><strong>{item_counts["completed"]}</strong><span>有完成记录的工作项</span></div>
<div class="metric"><strong>—</strong><span>产品完成率暂不可计算</span></div>
</div>
<p class="source-note">主线身份来自当前会话卡，状态、Gate 和下一动作以该工作项最新 ledger 为准；看板维护只作为并行工作展示。</p>
</section>
<!-- VIEW:roadmap -->
<section id="roadmap" class="panel" aria-labelledby="roadmap-title">
<div class="section-heading"><div><p class="eyebrow">阶段 + 里程碑</p><h2 id="roadmap-title">路线图</h2></div>
<p>先看产品主线已经完成什么、当前在哪个 Gate，再看有明确日期的里程碑。</p></div>
<div class="summary-strip"><strong>{html.escape(roadmap_summary)}</strong>
<span>{planned_stages} 步未开始</span>
{(f'<a href="plans/{html.escape(str(focus["id"]), quote=True)}.html">打开完整主线计划</a>') if focus and focus.get("plan_stages") else ""}</div>
<ol class="stage-list">{"".join(stage_cards) or "<li class='stage-card'>尚未登记主线路线图。</li>"}</ol>
<h3>项目主线与工作项</h3>
<div class="list-grid">{roadmap_items_html or _empty("尚未登记可下钻的工作项计划。")}</div>
<details class="paused"><summary>其他已登记工作路线（{sum(item["category"] in {"attention", "active"} for item in paused_items)}）</summary>
<div class="list-grid">{roadmap_other_html or _empty("当前没有其他活动工作路线。")}</div></details>
<h3>已登记里程碑</h3>
<div class="list-grid">{milestones_html or _empty("尚未登记里程碑或目标日期。")}</div></section>
<!-- VIEW:work -->
<section id="work" class="panel" aria-labelledby="work-title">
<div class="section-heading"><div><p class="eyebrow">主线 / 并行 / 暂停</p><h2 id="work-title">当前工作</h2></div>
<div><p>只把当前有效工作放在负责人视图；历史任务不再铺满页面。</p>
<a class="section-action" href="roadmap.html">查看分层路线图 →</a></div></div>
<h3>负责人当前范围</h3>
<div class="scope-summary">
<span><strong>产品主线</strong>{html.escape(focus_label)}</span>
<span><strong>主线 Gate</strong>{html.escape(mainline_status)}</span>
<span><strong>并行范围</strong>{html.escape(parallel_label)}</span>
<span><strong>主板任务</strong>{len(board_tasks)} 项</span>
</div>
<details class="paused"><summary>未纳入当前会话 / 后续工作（{len(paused_items)}）</summary>
<ul class="scope-list">{paused_html or "<li>尚未登记其他工作。</li>"}</ul></details>
<h3>敏捷任务看板</h3>
<p class="muted">六种状态统一汇总一次；业务分组内只显示实际存在的状态，设计、开发、测试等专业类型使用标签区分。</p>
<div class="board-summary" aria-label="主板状态汇总">{board_status_summary}</div>
<div id="agile-board" class="swimlane-board" aria-label="敏捷任务看板">
{board_html or _empty("当前没有有效任务。")}</div>
<details class="board-history"><summary>历史完成任务（{len(history_tasks)}）</summary>
<ul class="history-list">{history_html or "<li>暂无历史任务。</li>"}</ul></details></section>
<!-- VIEW:decisions -->
<section id="decisions" class="panel" aria-labelledby="decisions-title">
<div class="section-heading"><div><p class="eyebrow">现在需要谁处理什么</p><h2 id="decisions-title">阻塞与决策</h2></div>
<p>每项只展示原因、责任人、日期和下一动作；内部事件名称下沉审计。</p></div>
<div class="list-grid">{risk_html or _empty("当前没有已登记的阻塞或人工确认。")}</div></section>
<!-- VIEW:readiness -->
<section id="readiness" class="panel" aria-labelledby="readiness-title">
<div class="section-heading"><div><p class="eyebrow">需求到发布</p><h2 id="readiness-title">交付就绪</h2></div>
<p>状态表示已登记事实，不用事件数或工作项关闭率冒充产品完成度。</p></div>
<div class="readiness-grid">{readiness_html}</div>
<p class="source-note"><strong>产品完成率暂不可计算。</strong> 当前只说明需求、设计、实现、验证、审批和发布证据是否已登记。</p></section>
<!-- VIEW:documents -->
<section id="documents" class="panel" aria-labelledby="documents-title">
<div class="section-heading"><div><p class="eyebrow">正式文档快速入口</p><h2 id="documents-title">文档与审计</h2></div>
<p>先按类别打开正式技术文档；需要追责或复核时，再展开底部审计信息。</p></div>
<div class="document-grid">{documents_html}</div>
<details class="audit"><summary>查看 10 类底层内容与审计详情</summary>
<div class="domain-list">{domain_html}</div>
<h3>质量记录</h3><ul class="record-list">{quality_html or "<li>尚未登记测试、验证或评审证据。</li>"}</ul>
<h3>交付物</h3><ul class="record-list">{deliverables_html or "<li>尚未登记交付物。</li>"}</ul>
<h3>当前追踪链</h3>
{("<div class='table-scroll'><table><thead><tr><th>需求模块</th><th>关联需求</th><th>任务</th><th>交付物</th><th>证据</th><th>版本</th></tr></thead><tbody>" + trace_rows + "</tbody></table></div>") if tasks else _empty("尚未登记当前任务追踪链。")}
<h3>版本变更</h3><ul class="record-list">{versions_html or "<li>尚未登记版本提交。</li>"}</ul>
<h3>治理决策</h3><ul class="record-list">{decisions_html or "<li>尚未登记决策记录。</li>"}</ul>
<details class="technical"><summary>项目定义原文</summary><p>{html.escape(project["idea"] or "尚未登记")}</p></details>
{('<details class="technical"><summary>会话卡定位信息（动作以最新 ledger 为准）</summary><dl>' + session_html + "</dl></details>") if session_html else ""}
</details></section>
<!-- VIEW:END -->
</main>
</body>
</html>
"""


def _view_pages(page: str) -> dict[str, str]:
    main_open = '<main id="main">'
    main_start = page.index(main_open) + len(main_open)
    main_end = page.index("</main>", main_start)
    pages: dict[str, str] = {}
    for view, filename, _ in VIEW_LINKS:
        marker = f"<!-- VIEW:{view} -->"
        start = page.index(marker, main_start) + len(marker)
        next_markers = [
            position
            for candidate, _, _ in VIEW_LINKS
            if (position := page.find(f"<!-- VIEW:{candidate} -->", start)) >= 0
        ]
        end_marker = page.index("<!-- VIEW:END -->", start)
        end = min(next_markers + [end_marker])
        content = page[start:end].strip()
        rendered = page[:main_start] + "\n" + content + "\n" + page[main_end:]
        rendered = rendered.replace(
            f'<a href="{filename}">',
            f'<a href="{filename}" aria-current="page">',
        )
        pages[filename] = rendered
    return pages


def _event_label(event: dict[str, Any]) -> str:
    event_type = str(event.get("event_type") or event.get("event") or "").lower()
    if "start" in event_type:
        return "启动任务"
    if "changes_requested" in event_type:
        return "评审要求修改"
    if any(marker in event_type for marker in ("remediat", "finding_fixed", "findings_fixed")):
        return "完成评审整改"
    if "review" in event_type and any(
        marker in event_type for marker in ("approved", "rereview", "passed")
    ):
        return "独立评审通过"
    if "review" in event_type:
        return "提交独立评审"
    if any(marker in event_type for marker in ("verif", "test")):
        return "完成验证"
    if "commit" in event_type:
        return "完成本地提交"
    if any(marker in event_type for marker in ("human", "confirm", "decision")):
        return "人工确认或决策"
    status = str(event.get("status") or "")
    return _status_label(status, _category(status))


def _daily_progress(task: dict[str, Any]) -> str:
    dated: dict[str, list[dict[str, Any]]] = {}
    for event in task["events"]:
        timestamp = _event_time(event)
        day = timestamp[:10] if len(timestamp) >= 10 else "日期未登记"
        dated.setdefault(day, []).append(event)
    if not dated:
        return _empty("尚未登记任务日计划或 ledger 进展。")
    days = []
    for day, events in sorted(dated.items(), reverse=True):
        rows = []
        for event in reversed(events):
            status = str(event.get("status") or "状态未登记")
            raw_next_action = str(
                event.get("next_required_action") or event.get("next_action") or ""
            )
            next_action = _next_step(status, _category(status), raw_next_action, "")
            rows.append(
                "<li>"
                f"<strong>{html.escape(_event_label(event))}</strong>"
                f" · {html.escape(_status_label(status, _category(status)))}"
                + (
                    f"<br><span>后续路线：{html.escape(next_action)}</span>"
                    if next_action and next_action != "无"
                    else ""
                )
                + "</li>"
            )
        days.append(
            '<section class="daily-progress">'
            f"<h3>{html.escape(day)}</h3><ul>{''.join(rows)}</ul></section>"
        )
    return (
        '<p class="subtitle">正式日计划未登记时，以下仅显示 ledger 已发生事实和事件登记的后续路线。</p>'
        + "".join(days)
    )


def _route_tree(
    item: dict[str, Any],
    root_ids: list[str],
    include_descendants: bool = True,
) -> str:
    nodes = {node["id"]: node for node in item["plan_nodes"]}
    tasks = {task["id"]: task for task in item["tasks"]}

    def render(node_id: str, include_descendants: bool = True) -> str:
        node = nodes[node_id]
        task = tasks.get(node_id)
        stage_link = (
            f'<a href="../stages/{html.escape(node_id, quote=True)}.html">'
            f"{html.escape(node['title'])}</a>"
        )
        task_link = (
            f'<a class="route-task-link" '
            f'href="../tasks/{html.escape(task["route"], quote=True)}.html">查看任务详情 →</a>'
            if task
            else ""
        )
        task_status = " · 任务尚未拆分" if node["parent_id"] is None and not task else ""
        children = (
            "".join(render(child_id) for child_id in node["children"])
            if include_descendants
            else ""
        )
        return (
            f'<li id="stage-{html.escape(node_id, quote=True)}" '
            f'class="{html.escape(node["state"], quote=True)}" '
            f'data-route-id="{html.escape(node_id, quote=True)}">'
            f"<strong>{stage_link}</strong>"
            f"<small>{html.escape(node['label'])} · {html.escape(node['status'])}"
            f"{task_status}</small>"
            + task_link
            + (f'<ol class="route-tree">{children}</ol>' if children else "")
            + "</li>"
        )

    return (
        '<ol class="route-tree">'
        f"{''.join(render(node_id, include_descendants) for node_id in root_ids)}</ol>"
    )


def _task_stage(item: dict[str, Any], task_id: str) -> dict[str, Any] | None:
    nodes = {node["id"]: node for node in item["plan_nodes"]}
    node = nodes.get(task_id)
    while node and node["parent_id"]:
        node = nodes.get(node["parent_id"])
    return node if node and node["parent_id"] is None else None


def _plan_outline(item: dict[str, Any]) -> str:
    linked = {node["id"] for node in item["plan_nodes"]}
    unlinked = [task for task in item["tasks"] if task["id"] not in linked]
    unlinked_html = "".join(
        "<li>"
        f'<a href="../tasks/{html.escape(task["route"], quote=True)}.html">'
        f"{html.escape(_display_title(task['title'], task['goal']))}</a>"
        f"<small>{html.escape(task['status_label'])}</small></li>"
        for task in unlinked
    )
    return (
        "<h2>计划阶段与任务</h2>"
        + (
            _route_tree(item, [stage["id"] for stage in item["plan_stages"]])
            if item["plan_stages"]
            else '<ol class="plan-outline"><li>计划阶段尚未登记。</li></ol>'
        )
        + (f"<h2>尚未写入计划阶段的任务</h2><ul>{unlinked_html}</ul>" if unlinked_html else "")
    )


def _detail_pages(
    root: Path,
    items: list[dict[str, Any]],
    documents: list[dict[str, str]],
    session: dict[str, str],
) -> dict[str, str]:
    pages: dict[str, str] = {}
    requirements: dict[str, dict[str, str]] = {}
    requirement_owner: dict[str, str] = {}
    for item in items:
        for requirement in item["requirements"]:
            requirements[requirement["id"]] = requirement
            requirement_owner[requirement["id"]] = item["title"]
        for task in item["tasks"]:
            for requirement_id in _relation_ids(task["relations"]):
                requirements.setdefault(
                    requirement_id,
                    {
                        "id": requirement_id,
                        "title": "需求说明待补齐",
                        "body": "该需求已被任务引用，但正式需求说明尚未登记。",
                    },
                )
                requirement_owner.setdefault(requirement_id, item["title"])
    for item in items:
        plan_link = (
            f'<p><a href="../plans/{html.escape(item["id"], quote=True)}.html">'
            "查看所属工作项完整计划</a></p>"
            if item["plan_stages"]
            else ""
        )
        for task in item["tasks"]:
            title = _display_title(
                task["title"],
                task["goal"] or task["work_item_title"] or task["work_item_purpose"],
            )
            work_item_label = _display_title(
                task["work_item_title"],
                _compact(task["work_item_purpose"], 42),
            )
            is_focus = task["work_item_id"] == session.get("工作项") and task["id"] == session.get(
                "任务"
            )
            confirmation = session.get("确认事项", "") if is_focus else ""
            gate_reason = task["gate_reason"] or (session.get("Gate", "") if is_focus else "")
            if "customer" in gate_reason.lower():
                gate_label = "客户岗位授权与职责分离确认"
                confirmation_party = "客户授权代表（具体人员未登记）"
            else:
                gate_label = gate_reason or "人工确认"
                confirmation_party = task["owner"] or "人工确认方尚未登记"
            next_action = f"确认{confirmation}" if confirmation else task["next_action"]
            route_stage = _task_stage(item, task["id"])
            route_link = (
                f'<p><a href="../stages/{html.escape(route_stage["id"], quote=True)}.html">'
                f"查看所属路线阶段：{html.escape(route_stage['title'])}</a></p>"
                if route_stage
                else ""
            )
            gate_rows = ""
            if task["human_confirmation_required"] or confirmation:
                gate_rows = (
                    f"<dt>当前 Gate</dt><dd>{html.escape(gate_label)}</dd>"
                    f"<dt>确认事项</dt><dd>{html.escape(confirmation or '具体确认项尚未登记')}</dd>"
                    f"<dt>确认方</dt><dd>{html.escape(confirmation_party)}</dd>"
                    f"<dt>截止日期</dt><dd>{html.escape(task['target_date'] or '未排期')}</dd>"
                )
            content = (
                f"<h1>{html.escape(title)}</h1>"
                f"<p>{html.escape(task['goal'] or task['work_item_title'] or task['work_item_purpose'] or '任务目标尚未登记。')}</p>"
                '<dl class="facts">'
                f"<dt>所属工作项</dt><dd>{html.escape(work_item_label)}</dd>"
                f"<dt>当前状态</dt><dd>{html.escape(task['status_label'])}</dd>"
                f"<dt>需求模块</dt><dd>{html.escape(task['module'])}</dd>"
                f"<dt>任务类型</dt><dd>{html.escape(_task_type_label(task['task_type']))}</dd>"
                f"<dt>关联需求</dt><dd>{_requirement_links(task, requirements, '../')}</dd>"
                f"{gate_rows}"
                f"<dt>下一步</dt><dd>{html.escape(next_action)}</dd>"
                f"<dt>验收标准</dt><dd>{html.escape(task['verification'] or '尚未登记')}</dd>"
                "</dl>" + route_link + plan_link + "<h2>每日路线与进展</h2>" + _daily_progress(task)
            )
            pages[f"tasks/{task['route']}.html"] = _detail_page(
                title,
                f"任务详情 · {work_item_label}",
                content,
                "work.html",
                "work",
            )
        node_by_id = {node["id"]: node for node in item["plan_nodes"]}
        task_by_id = {task["id"]: task for task in item["tasks"]}
        for stage in item["plan_nodes"]:
            descendant_ids: list[str] = []
            pending = list(stage["children"])
            while pending:
                descendant_id = pending.pop(0)
                descendant_ids.append(descendant_id)
                pending.extend(node_by_id[descendant_id]["children"])
            descendants = [node_by_id[node_id] for node_id in descendant_ids]
            counts = {
                state: sum(node["state"] == state for node in descendants)
                for state in ("completed", "current", "planned")
            }
            stage_task = task_by_id.get(stage["id"])
            task_link = (
                f'<p><a href="../tasks/{html.escape(stage_task["route"], quote=True)}.html">'
                "查看本阶段任务详情与每日进展 →</a></p>"
                if stage_task
                else ""
            )
            route = (
                _route_tree(item, stage["children"], include_descendants=False)
                if stage["children"]
                else _empty("本阶段尚未拆分子步骤。")
            )
            content = (
                f"<h1>{html.escape(stage['title'])}</h1>"
                '<dl class="facts">'
                f"<dt>阶段状态</dt><dd>{html.escape(stage['label'])}</dd>"
                f"<dt>直接子步骤</dt><dd>{len(stage['children'])} 个直接子步骤</dd>"
                f"<dt>全部子步骤</dt><dd>{len(descendants)}</dd>"
                f"<dt>子步骤进度</dt><dd>{counts['completed']} 已完成 · "
                f"{counts['current']} 当前 · {counts['planned']} 未开始</dd>"
                "</dl>" + task_link + "<h2>本阶段细化路线</h2>" + route
            )
            pages[f"stages/{stage['id']}.html"] = _detail_page(
                stage["title"],
                f"路线阶段 · {_display_title(item['title'], item['purpose'])} · {stage['id']}",
                content,
                "roadmap.html",
                "roadmap",
            )
        if item["plan_path"].is_file():
            plan_text = item["plan_path"].read_text(encoding="utf-8")
            pages[f"plans/{item['id']}.html"] = _detail_page(
                item["plan_title"],
                f"主线计划 · {item['title']}",
                _plan_outline(item) + "<h2>完整计划文档</h2>" + _markdown(plan_text),
                "roadmap.html",
                "roadmap",
            )
    for requirement_id, requirement in requirements.items():
        content = (
            f"<h1>{html.escape(requirement['title'])}</h1>"
            f"<p><code>{html.escape(requirement_id)}</code></p>"
            f"{_markdown(requirement['body'])}"
        )
        pages[f"requirements/{requirement_id}.html"] = _detail_page(
            requirement["title"],
            f"需求详情 · {requirement_owner.get(requirement_id, '所属工作项尚未登记')}",
            content,
            "work.html",
            "work",
        )
    for document in documents:
        text = (root / document["path"]).read_text(encoding="utf-8")
        pages[f"documents/{document['id']}.html"] = _detail_page(
            document["title"],
            f"{document['category']} · {document['path']}",
            _markdown(text),
            "documents.html",
            "documents",
        )
    return pages


def snapshot(project_root: Path, relative_paths: bool) -> dict[str, Any]:
    root = project_root.expanduser().resolve()
    if not root.is_dir():
        raise SnapshotError(f"project root does not exist: {root}")
    factory = root / ".factory"
    if not factory.is_dir():
        raise SnapshotError(f"project has no .factory directory: {root}")
    _assert_within(root, factory)

    output_dir = factory / "cache" / "site" / "current"
    _assert_within(root, output_dir)
    output = output_dir / "index.html"
    metadata = output_dir / "snapshot.json"
    sources = _sources(root)
    for source in sources:
        _assert_within(root, source)
    generation_id = _fingerprint(root, sources)
    items = _work_items(root)
    documents = _documents(root)
    project = _project(root)
    session = _session(root)
    details = _detail_pages(root, items, documents, session)
    views = _view_pages(_render(project, session, items, documents))
    pages = {**views, **details}
    expected_outputs = sorted(pages)
    if output.exists() and metadata.exists():
        try:
            previous = json.loads(metadata.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            previous = {}
        if not isinstance(previous, dict):
            raise SnapshotError(f"{metadata}: metadata must be an object")
        if previous.get("generation_id") == generation_id and all(
            (output_dir / relative_path).is_file() for relative_path in expected_outputs
        ):
            return _receipt(root, output, generation_id, True, len(sources), relative_paths)

    output_dir.mkdir(parents=True, exist_ok=True)
    for relative_path, content in pages.items():
        detail_path = output_dir / relative_path
        _assert_within(root, detail_path)
        detail_path.parent.mkdir(parents=True, exist_ok=True)
        _atomic_write(detail_path, content)
    _atomic_write(
        metadata,
        json.dumps(
            {
                "generation_id": generation_id,
                "source_count": len(sources),
                "outputs": expected_outputs,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
        + "\n",
    )
    return _receipt(root, output, generation_id, False, len(sources), relative_paths)


def _atomic_write(path: Path, content: str) -> None:
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(content, encoding="utf-8")
    os.replace(temporary, path)


def _receipt(
    root: Path,
    output: Path,
    generation_id: str,
    cache_hit: bool,
    source_count: int,
    relative_paths: bool,
) -> dict[str, Any]:
    rendered_path = output.relative_to(root).as_posix() if relative_paths else str(output)
    return {
        "schema_id": "SkillProjectSnapshotReceipt/v1",
        "status": "success",
        "cache_hit": cache_hit,
        "generation_id": generation_id,
        "source_count": source_count,
        "relative_paths": relative_paths,
        "read_only_facts": True,
        "html_path": rendered_path,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--relative-paths", action="store_true")
    arguments = parser.parse_args(argv)
    try:
        receipt = snapshot(Path(arguments.project_root), arguments.relative_paths)
    except (SnapshotError, OSError, UnicodeError) as error:
        print(
            json.dumps(
                {
                    "schema_id": "SkillProjectSnapshotReceipt/v1",
                    "status": "failed",
                    "error": str(error),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 2
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
