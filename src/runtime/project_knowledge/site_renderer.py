"""Pure, framework-free renderer for the read-only project site."""

# ruff: noqa: E501

from __future__ import annotations

import hashlib
import html
import json
import re
from datetime import datetime
from pathlib import PurePosixPath
from typing import Any

from application.project_knowledge.site_service import RenderedSite
from domain.project_knowledge.models import canonical_json
from domain.project_knowledge.sensitive_values import redact_text

RENDERER_VERSION = "ProjectSiteRenderer/v6"


_NAVIGATION = (
    ("index.html", "任务看板"),
    ("requirements/index.html", "需求"),
    ("design/index.html", "设计"),
    ("plans/index.html", "计划"),
    ("execution/index.html", "执行"),
    ("quality/index.html", "质量"),
    ("documents/index.html", "文档"),
    ("code/index.html", "代码"),
    ("versions/index.html", "版本"),
    ("project-management/index.html", "项目管理"),
    ("reports/index.html", "报告"),
)

_PM_MODULES = (
    ("pm_project_profile", "project-profile", "项目章程"),
    ("pm_party", "team-stakeholders", "团队与干系人"),
    ("pm_work_plan", "work-plan", "范围、WBS 与进度"),
    ("pm_risk", "risks", "风险管理"),
    ("pm_communication", "communications", "沟通管理"),
    ("pm_meeting", "meetings", "会议与决策"),
    ("pm_action_item", "actions", "行动项"),
    ("pm_status_report", "status-reports", "进度报告"),
    ("pm_change_request", "changes", "变更管理"),
    ("pm_project_summary", "summary", "交付与收尾"),
)


def _escape(value: Any) -> str:
    return html.escape(redact_text("" if value is None else str(value)), quote=True)


def _display_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )


_RENDER_INTERNAL_FIELDS = {
    "generation_id",
    "source_manifest_sha256",
    "row_sha256",
}


def _render_input(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            str(key): _render_input(item)
            for key, item in value.items()
            if str(key) not in _RENDER_INTERNAL_FIELDS
        }
    if isinstance(value, list):
        return [_render_input(item) for item in value]
    return value


def _route_id(value: Any) -> str:
    raw = str(value)
    if re.fullmatch(r"[A-Za-z0-9._~-]{1,120}", raw):
        return raw
    readable = re.sub(r"[^A-Za-z0-9._~-]+", "-", raw).strip("-")[:72] or "entity"
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
    return f"{readable}-{digest}"


def _prefix(route: str) -> str:
    return "../" * (len(PurePosixPath(route).parts) - 1)


def site_input_token(generation: dict[str, Any], profile: str) -> str:
    return hashlib.sha256(
        canonical_json(
            {
                "renderer": RENDERER_VERSION,
                "profile": profile,
                "generation_id": generation.get("generation_id"),
                "source_manifest_sha256": generation.get("source_manifest_sha256")
                or generation.get("source_root_sha256"),
                "pm_projection_sha256": generation.get("pm_projection_sha256"),
            }
        ).encode("utf-8")
    ).hexdigest()


def _status_label(value: Any) -> str:
    labels = {
        "active": "进行中",
        "approved": "已批准",
        "changes_requested": "需要修改",
        "closed": "已关闭",
        "committed": "已本地提交",
        "current": "当前版本",
        "done": "已完成",
        "failed": "失败",
        "in_progress": "进行中",
        "open": "待处理",
        "passed": "已通过",
        "pending_human_confirmation": "等待人工确认",
        "ready_for_review": "等待独立评审",
        "review": "待评审",
        "testing": "测试中",
        "todo": "待开始",
        "blocked": "待确认 / 阻塞",
        "unknown": "待补充",
        "not_registered": "暂无数据源",
        "warning": "警告",
    }
    raw = str(value or "unknown")
    return labels.get(raw, raw.replace("_", " "))


def _status(value: Any) -> str:
    safe = _escape(_status_label(value))
    return f'<span class="status-chip">{safe}</span>'


def _definition_value(key: str, value: Any) -> Any:
    if str(value).casefold() == "unknown":
        return "待补充"
    if str(value).casefold() == "not_registered":
        return "暂无数据源"
    if key in {"lifecycle_status", "doc_status", "status", "severity"}:
        return _status_label(value)
    if key == "entity_kind":
        return {
            "acceptance_criterion": "验收条件",
            "code_file": "代码文件",
            "code_symbol": "代码符号",
            "non_functional_requirement": "非功能需求",
            "requirement": "需求",
            "test": "测试",
            "work_item": "执行任务",
            "work_item_event": "任务事件",
        }.get(str(value), str(value).replace("_", " "))
    return value


def _summary_cards(cards: list[tuple[str, Any, str]]) -> str:
    return (
        '<div class="metric-grid">'
        + "".join(
            '<article class="metric"><p class="metric-label">'
            f'{_escape(label)}</p><p class="metric-value">{_escape(value)}</p>'
            f'<p class="metric-note">{_escape(note)}</p></article>'
            for label, value, note in cards
        )
        + "</div>"
    )


def _list_items(items: list[dict[str, Any]], route_template: str) -> str:
    if not items:
        return '<div class="empty"><strong>当前没有已登记记录</strong><p>页面不会根据缺失信息猜测状态。</p></div>'
    rows = []
    for item in items:
        entity_id = item.get("entity_id") or item.get("record_id") or item.get("diagnostic_id")
        route = route_template.format(id=_route_id(entity_id))
        rows.append(
            '<li class="record-row"><div><a class="record-link" href="'
            f'{_escape(route)}">{_escape(item.get("display_name") or entity_id)}</a>'
            f"<p>{_escape(item.get('summary') or item.get('safe_message') or '暂无说明')}</p></div>"
            f"{_status(item.get('lifecycle_status') or item.get('status') or item.get('severity'))}</li>"
        )
    return '<ul class="record-list">' + "".join(rows) + "</ul>"


_KANBAN_COLUMNS = (
    ("todo", "待开始"),
    ("in_progress", "进行中"),
    ("testing", "测试中"),
    ("review", "待评审"),
    ("blocked", "待确认 / 阻塞"),
    ("done", "已完成"),
)

_TASK_SLUG_TITLES = {
    "artifact-retention-and-ephemeral-evidence-policy": "制品保留与临时证据策略",
    "project-execution-position-and-stop-visibility": "项目执行位置与停止原因可见性",
    "project-knowledge-index-and-deterministic-docs": "项目知识索引与确定性文档",
    "project-knowledge-index-and-readonly-site": "项目知识索引与只读站点",
    "progress-visibility-and-continuous-execution": "进度可见与连续执行",
    "remaining-skill-project-status-contract": "剩余技能项目状态契约",
    "simple-task-fast-path": "简单任务快速通道",
    "work-skill-status-envelope-owner": "工作技能状态信封归属",
}

_TASK_ID_TITLES = {
    "DOC-FACTORY-RESTRUCTURE-001": "文档与项目记忆结构重整",
    "FLOW-CONTRACT-001": "智能开发流程契约治理",
    "GO-BACKEND-SKILL-001": "后端开发技能建设",
    "PM-DASHBOARD-002-T01": "项目状态十模块查看契约",
    "PM-DASHBOARD-003": "项目状态仪表盘原型",
    "SF-SP-001": "移除旧中心脚本流程入口",
    "SF-SP-002": "建立项目记忆工作流",
    "SF-SP-003": "迁移需求工程参考资料",
    "SF-SP-004": "建立计划编写工作流",
    "SF-SP-005": "建立任务执行工作流",
    "SF-SP-006": "建立独立评审工作流",
    "SF-SP-007": "建立调试与完成验证工作流",
    "SF-SP-008": "建立提交与交付门禁",
    "SF-SP-009": "建立黑盒流程评估",
    "SF-SP-010": "完成工作流集成收尾",
    "TASK-001-destructive-full-doc-migration": "文档体系完整迁移",
    "TASK-002-docs-memory-structure-redesign": "文档与项目记忆结构重构",
    "TASK-DESIGN-001-ai-collaboration-workflow-design": "智能协作工作流设计",
    "TASK-DELIVERY-001-r002-delivery-and-closeout": "交付与项目收尾",
    "TASK-IMPLEMENT-001-ai-workflow-platform-implementation": "智能协作工作流平台实施",
    "TASK-IMPLEMENT-003-P001": "项目知识索引与只读站点实施",
    "TASK-IMPLEMENT-003-P001-T01": "合同内核与 39 表数据结构",
    "TASK-IMPLEMENT-003-P001-T02": "来源登记、提取器与增量索引",
    "TASK-IMPLEMENT-003-P001-T03": "稳定定位、关系图与命令行查询",
    "TASK-IMPLEMENT-003-P001-T04": "137 字段项目管理投影与只读站点",
    "TASK-IMPLEMENT-003-P001-T05": "异步同步、有界维护与资料迁移",
    "TASK-IMPLEMENT-003-P001-T06": "装配、正式文档与整体资格化",
    "TASK-PRD-001-ai-collaboration-workflow-prd": "智能协作工作流产品需求",
    "TASK-QUALITY-002-remove-unused-runtime-skill-management": "移除未使用的技能管理链路",
    "TASK-REQ-001-ai-collaboration-workflow-requirements": "智能协作工作流需求",
    "TASK-REQ-002-project-progress-snapshot-requirement-change": "项目进度快照需求变更",
    "TASK-REQ-003-main-task-projection-decoupling-and-risk-based-verification": (
        "主任务投影解耦与风险分级验证"
    ),
    "TASK-WORKFLOW-SEMANTICS-001": "任务工作流语义治理",
    "TASK-WF-PRD-001-requirement-clarification-to-prd-workflow": (
        "需求澄清到产品需求工作流"
    ),
    "UI-DESIGN-SKILL-001": "全平台界面体验与动效设计技能",
    "FLOW-TASK-008": "升级任务执行流程",
    "FLOW-TASK-009": "升级独立评审与完成验证流程",
    "FLOW-TASK-010": "增加项目基线设计模板",
}

_TASK_WORDS = {
    "ai": "智能协作",
    "artifact": "制品",
    "collaboration": "协作",
    "continuous": "连续",
    "delivery": "交付",
    "design": "设计",
    "deterministic": "确定性",
    "docs": "文档",
    "execution": "执行",
    "fast": "快速",
    "foundation": "基础",
    "implementation": "实施",
    "index": "索引",
    "knowledge": "知识",
    "memory": "记忆",
    "policy": "策略",
    "position": "位置",
    "progress": "进度",
    "project": "项目",
    "readonly": "只读",
    "requirement": "需求",
    "requirements": "需求",
    "simple": "简单",
    "skill": "技能",
    "status": "状态",
    "stop": "停止",
    "system": "系统",
    "task": "任务",
    "visibility": "可见性",
    "workflow": "工作流",
}


def _clean_chinese_title(value: Any) -> str:
    title = str(value or "").strip().lstrip("#").strip()
    title = re.sub(
        r"^(?:[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+|T\d+)\s*[|｜:：-]*\s*",
        "",
        title,
    )
    replacements = (
        (r"document-templates", "文档模板"),
        (r"requesting-code-review", "发起独立评审"),
        (r"receiving-code-review", "处理评审反馈"),
        (r"React Native", "跨平台移动端"),
        (r"UI/UX", "界面体验"),
        (r"SQLite", "本地索引"),
        (r"Schema", "数据结构"),
        (r"HTML", "网页"),
        (r"Excel", "电子表格"),
        (r"CLI", "命令行"),
        (r"PM", "项目管理"),
        (r"API", "接口"),
        (r"AST", "代码符号"),
        (r"TDD", "测试驱动开发"),
        (r"review", "评审"),
        (r"verification", "完成验证"),
        (r"baseline", "基线"),
        (r"eval", "评估"),
        (r"skill", "技能"),
    )
    for pattern, replacement in replacements:
        title = re.sub(pattern, replacement, title, flags=re.IGNORECASE)
    if re.search(r"[A-Za-z]", title):
        return ""
    title = re.sub(r"\s+", " ", title).strip(" -—_|｜:：,，;；。")
    title = re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])", "", title)
    title = title.replace("表 数据结构", "表数据结构")
    title = title.replace("智能协作协作", "智能协作")
    return title


def _slug_title(task_id: str) -> str | None:
    match = re.search(r"-(?=[a-z])([a-z0-9-]+)$", task_id)
    if match is None:
        return None
    slug = match.group(1)
    if slug in _TASK_SLUG_TITLES:
        return _TASK_SLUG_TITLES[slug]
    translated = [_TASK_WORDS.get(token) for token in slug.split("-")]
    if any(token is None for token in translated):
        return None
    return "".join(str(token) for token in translated)


def _timestamp(value: Any) -> float | None:
    raw = str(value or "").strip()
    if not raw:
        return None
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.timestamp()


def _brief_title(task_id: str, documents: list[dict[str, Any]]) -> str | None:
    matches: list[tuple[int, str]] = []
    work_item_matches: list[str] = []
    for document in documents:
        relative_path = str(document.get("relative_path") or "")
        if "/task-briefs/" not in f"/{relative_path}":
            continue
        parts = PurePosixPath(relative_path).parts
        try:
            work_item_id = parts[parts.index("workitems") + 1]
        except (ValueError, IndexError):
            work_item_id = ""
        stem = PurePosixPath(relative_path).stem
        if stem == task_id:
            score = 3
        elif stem.startswith(task_id + "-"):
            score = 2
        elif task_id.startswith(stem + "-"):
            score = 1
        else:
            continue
        title = _clean_chinese_title(document.get("chinese_name") or document.get("title"))
        if title and title not in {"任务简报", "实施任务简报", "工作项"}:
            matches.append((score, title))
            if task_id == work_item_id:
                work_item_matches.append(title)
    if matches:
        return max(matches)[1]
    if len(set(work_item_matches)) == 1:
        return work_item_matches[0]
    return None


def _summary_title(summary: Any) -> str | None:
    text = str(summary or "")
    if not re.search(r"[\u4e00-\u9fff]", text):
        return None
    match = re.search(r"[：:]\s*([^，；。]{2,60})", text)
    candidate = match.group(1) if match else re.split(r"[，；。]", text, maxsplit=1)[0]
    candidate = re.sub(r"^(?:按用户|按顺序|最近进展|当前状态)\s*", "", candidate)
    cleaned = _clean_chinese_title(candidate)
    return cleaned if len(re.findall(r"[\u4e00-\u9fff]", cleaned)) >= 3 else None


def _task_title(item: dict[str, Any], documents: list[dict[str, Any]]) -> str:
    task_id = str(item.get("display_name") or item.get("entity_id") or "")
    details = dict(item.get("details") or {})
    explicit = _clean_chinese_title(details.get("task_title"))
    if explicit:
        return explicit
    mapped = _TASK_ID_TITLES.get(task_id)
    if mapped:
        return mapped
    brief = _brief_title(task_id, documents)
    if brief:
        return brief
    if re.search(r"[\u4e00-\u9fff]", task_id):
        readable = _clean_chinese_title(task_id)
        if readable:
            return readable
    return _slug_title(task_id) or _summary_title(item.get("summary")) or "任务标题待补充"


def _kanban_status(item: dict[str, Any]) -> str:
    work_item = dict(item.get("work_item") or {})
    raw = str(work_item.get("task_status") or item.get("lifecycle_status") or "")
    details = dict(item.get("details") or {})
    next_action = str(details.get("next_action") or details.get("next") or "")
    normalized = f"{raw} {next_action}".casefold().replace("-", "_").replace(" ", "_")
    if any(
        marker in normalized
        for marker in (
            "blocked",
            "failed",
            "needs_user_input",
            "pending_human",
            "awaiting_exact",
            "human_confirmation",
            "pause",
            "reject",
        )
    ):
        return "blocked"
    if any(
        marker in raw.casefold()
        for marker in (
            "completed",
            "complete",
            "closed",
            "committed",
            "formalized",
            "human_approved",
            "released",
            "stage_complete",
        )
    ) or raw.casefold() in {"approved", "done", "passed"}:
        return "done"
    if "review" in next_action.casefold() or any(
        marker in normalized
        for marker in ("ready_for_review", "changes_requested", "requirements_ready")
    ):
        return "review"
    if any(marker in normalized for marker in ("test", "verify", "verification", "quality")):
        return "testing"
    if any(marker in normalized for marker in ("todo", "draft", "planned", "queued", "backlog")):
        return "todo"
    return "in_progress"


def _readable_task_summary(summary: Any, title: str) -> str:
    text = str(summary or "").strip()
    chinese_count = len(re.findall(r"[\u4e00-\u9fff]", text))
    latin_count = len(re.findall(r"\b[A-Za-z][A-Za-z0-9_-]*\b", text))
    if chinese_count >= 12 and latin_count <= chinese_count:
        return text
    return f"“{title}”的执行状态已从权威任务记录同步。"


def _prepare_tasks(
    raw_tasks: list[dict[str, Any]], documents: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for raw in raw_tasks:
        task = dict(raw)
        machine_id = str(task.get("display_name") or task.get("entity_id") or "")
        title = _task_title(task, documents)
        status = _kanban_status(task)
        details = dict(task.get("details") or {})
        task["task_id"] = machine_id
        task["display_name"] = title
        task["summary"] = _readable_task_summary(task.get("summary"), title)
        task["_raw_status"] = str(task.get("lifecycle_status") or "")
        task["_kanban_status"] = status
        task["lifecycle_status"] = status
        if status == "done":
            details["next_action"] = "已完成，无需继续操作。"
        task["details"] = details
        work_item = dict(task.get("work_item") or {})
        work_item["task_status"] = status
        task["work_item"] = work_item
        tasks.append(task)
    status_priority = {
        "todo": 0,
        "in_progress": 1,
        "testing": 2,
        "review": 3,
        "blocked": 4,
        "done": 5,
    }
    canonical: dict[str, dict[str, Any]] = {}
    for task in tasks:
        task_id = str(task["task_id"])
        current = canonical.get(task_id)
        updated_at = _timestamp(dict(task.get("details") or {}).get("updated_at"))
        score = (
            int(updated_at is not None),
            updated_at if updated_at is not None else float("-inf"),
            status_priority.get(str(task.get("_kanban_status") or ""), -1),
            int(task.get("display_name") != "任务标题待补充"),
        )
        current_updated_at = (
            _timestamp(dict(current.get("details") or {}).get("updated_at"))
            if current is not None
            else None
        )
        current_score = (
            int(current_updated_at is not None),
            current_updated_at if current_updated_at is not None else float("-inf"),
            status_priority.get(str(current.get("_kanban_status") or ""), -1),
            int(current.get("display_name") != "任务标题待补充"),
        ) if current is not None else (0, float("-inf"), -1, 0)
        if current is None or score > current_score:
            canonical[task_id] = task
    tasks = list(canonical.values())
    by_machine_id = {str(task["task_id"]): task for task in tasks}
    for task in tasks:
        if task["_kanban_status"] == "done":
            continue
        task_id = str(task["task_id"])
        ancestors = [
            parent
            for parent_id, parent in by_machine_id.items()
            if task_id.startswith(parent_id + "-")
        ]
        if not ancestors:
            continue
        parent = max(ancestors, key=lambda item: len(str(item["task_id"])))
        child_at = _timestamp(dict(task.get("details") or {}).get("updated_at"))
        parent_at = _timestamp(dict(parent.get("details") or {}).get("updated_at"))
        if (
            parent["_kanban_status"] == "done"
            and parent_at is not None
            and child_at is not None
            and parent_at >= child_at
        ):
            task["_kanban_status"] = "done"
            task["lifecycle_status"] = "done"
            task["work_item"]["task_status"] = "done"
            task["details"]["next_action"] = "父任务已完成，本子任务同步归档。"
    return sorted(
        tasks,
        key=lambda item: (
            _timestamp(dict(item.get("details") or {}).get("updated_at"))
            or float("-inf"),
            str(item.get("display_name") or ""),
        ),
        reverse=True,
    )


def _kanban_board(tasks: list[dict[str, Any]], route_template: str, *, limit: int = 10) -> str:
    columns = []
    for status, label in _KANBAN_COLUMNS:
        matches = [task for task in tasks if task.get("_kanban_status") == status]

        def card(task: dict[str, Any], modifier: str) -> str:
            entity_id = task.get("entity_id") or task.get("record_id")
            route = route_template.format(id=_route_id(entity_id))
            return (
                f'<a class="kanban-card kanban-card--{modifier}" href="{_escape(route)}">'
                f'{_escape(task.get("display_name") or "任务标题待补充")}</a>'
            )

        visible = "".join(card(task, "visible") for task in matches[:limit])
        remaining = matches[limit:]
        more = (
            '<details class="kanban-more"><summary>'
            f"更多（{len(remaining)}）</summary><div>"
            + "".join(card(task, "additional") for task in remaining)
            + "</div></details>"
            if remaining
            else ""
        )
        empty = '<p class="kanban-empty">暂无任务</p>' if not matches else ""
        columns.append(
            f'<section class="kanban-column" data-kanban-status="{_escape(status)}">'
            f'<header><h2>{_escape(label)}</h2><span>{len(matches)}</span></header>'
            f'<div class="kanban-cards">{visible}{more}{empty}</div></section>'
        )
    return '<div class="kanban-board">' + "".join(columns) + "</div>"


def _definition_list(values: dict[str, Any]) -> str:
    labels = {
        "entity_id": "稳定 ID",
        "entity_kind": "内容类型",
        "display_name": "名称",
        "task_id": "任务编号",
        "summary": "说明",
        "lifecycle_status": "当前状态",
        "primary_artifact_id": "主要来源制品",
        "semantic_sha256": "语义摘要",
        "document_id": "文档 ID",
        "title": "标题",
        "chinese_name": "中文名称",
        "doc_status": "文档状态",
        "audience": "主要读者",
        "owner": "负责人",
        "relative_path": "文件路径",
        "version": "当前版本",
    }
    rows = []
    for key, value in values.items():
        if key.startswith("_"):
            continue
        if key in {
            "acceptance_criteria",
            "code_symbol",
            "details",
            "field_values",
            "locators",
            "relations",
            "requirement",
            "sections",
            "symbols",
            "test",
            "work_item",
            *_RENDER_INTERNAL_FIELDS,
        }:
            continue
        rows.append(
            f"<dt>{_escape(labels.get(key, key))}</dt>"
            f"<dd>{_escape(_definition_value(key, value))}</dd>"
        )
    return '<dl class="definition-grid">' + "".join(rows) + "</dl>"


def _readable(value: Any) -> str:
    if value is None or value == "" or value == [] or value == {}:
        return '<p class="missing-state">当前暂无可展示的正式数据。</p>'
    if isinstance(value, str) and value.casefold() in {"unknown", "not_registered"}:
        return '<p class="missing-state">当前暂无可展示的正式数据。</p>'
    if isinstance(value, dict):
        rows = "".join(
            f"<dt>{_escape(key)}</dt><dd>{_readable(item)}</dd>" for key, item in value.items()
        )
        return f'<dl class="nested-definition">{rows}</dl>'
    if isinstance(value, list):
        return "<ul>" + "".join(f"<li>{_readable(item)}</li>" for item in value) + "</ul>"
    return f"<p>{_escape(value)}</p>"


def _first_detail(details: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = details.get(key)
        if value not in (None, "", [], {}):
            return value
    return None


def _relation_summary(relations: list[dict[str, Any]]) -> str:
    if not relations:
        return '<p class="missing-state">当前索引没有登记关联对象。</p>'
    return (
        '<ul class="relation-list">'
        + "".join(
            "<li><strong>"
            + _escape(relation.get("relation_type"))
            + "</strong> · "
            + _escape(relation.get("display_name") or relation.get("entity_id"))
            + " <code>"
            + _escape(relation.get("entity_id"))
            + "</code></li>"
            for relation in relations
        )
        + "</ul>"
    )


def _source_summary(item: dict[str, Any]) -> str:
    locators = list(item.get("locators") or [])
    if not locators:
        return '<p class="missing-state">当前索引没有登记可定向读取的来源。</p>'
    return (
        '<ul class="source-list">'
        + "".join(
            f"<li><code>{_escape(locator.get('relative_path'))}</code> · "
            f"{_escape(locator.get('locator_kind'))}<br>"
            f"<code>{_escape(_display_json(locator.get('selector') or {}))}</code></li>"
            for locator in locators
        )
        + "</ul>"
    )


def _snapshot_script(generation: dict[str, Any], profile: str) -> str:
    payload = canonical_json(
        {
            "generation": generation.get("generation_id") or "unknown",
            "git": generation.get("git_commit") or "unknown",
            "high_watermark": generation.get("facts_high_watermark") or "unknown",
            "as_of": generation.get("as_of") or "unknown",
            "renderer": RENDERER_VERSION,
            "profile": profile,
        }
    )
    return (
        "(()=>{const snapshot="
        + payload
        + ";document.querySelectorAll('[data-snapshot-field]').forEach((node)=>{"
        + "const value=snapshot[node.dataset.snapshotField];"
        + "node.textContent=value===undefined?'unknown':String(value);});})();"
    )


def _business_detail_sections(item: dict[str, Any]) -> str:
    kind = str(item.get("entity_kind") or "")
    details = dict(item.get("details") or {})
    relations = [dict(value) for value in item.get("relations") or []]
    summary = item.get("summary")
    if kind in {"requirement", "non_functional_requirement", "acceptance_criterion"}:
        requirement = dict(item.get("requirement") or {})
        criteria = list(requirement.get("acceptance_criteria") or [])
        criteria_html = (
            "<ol>"
            + "".join(
                f"<li>{_escape(criterion.get('statement'))} "
                f"{_status(criterion.get('criterion_status'))}</li>"
                for criterion in criteria
            )
            + "</ol>"
            if criteria
            else '<p class="missing-state">当前需求未登记独立验收条件。</p>'
        )
        return (
            "<section><h2>背景、问题与目标</h2>"
            + _readable(
                _first_detail(details, "background", "context", "problem", "goal", "objective")
                or summary
            )
            + "</section><section><h2>使用场景与预期结果</h2>"
            + _readable(
                _first_detail(
                    details,
                    "user_scenarios",
                    "user_scenario",
                    "expected_result",
                    "expected",
                    "outcome",
                    "result",
                )
            )
            + "</section><section><h2>范围与非目标</h2>"
            + _readable(
                {
                    "范围": _first_detail(details, "scope"),
                    "非目标": _first_detail(details, "non_goals", "out_of_scope"),
                }
            )
            + "</section><section><h2>验收条件</h2>"
            + criteria_html
            + "</section><section><h2>设计、任务、代码与测试</h2>"
            + _relation_summary(relations)
            + "</section><section><h2>发布与活动</h2>"
            + _readable(_first_detail(details, "release", "activities", "activity"))
            + "</section>"
        )
    if kind in {"work_item", "work_item_event"}:
        work_item = dict(item.get("work_item") or {})
        return (
            "<section><h2>任务目标与原因</h2>"
            + _readable(_first_detail(details, "goal", "objective", "why", "reason") or summary)
            + "</section><section><h2>范围与非范围</h2>"
            + _readable(
                {
                    "范围": _first_detail(details, "scope"),
                    "非范围": _first_detail(details, "out_of_scope", "non_goals"),
                }
            )
            + "</section><section><h2>完成条件</h2>"
            + _readable(
                _first_detail(
                    details, "completion_conditions", "done_definition", "acceptance_criteria"
                )
            )
            + "</section><section><h2>当前进度、阻塞与下一步</h2>"
            + _readable(
                {
                    "当前状态": _status_label(
                        work_item.get("task_status") or item.get("lifecycle_status")
                    ),
                    "最近进展": summary,
                    "阻塞": _first_detail(details, "blockers"),
                    "下一步": _first_detail(details, "next_action", "next"),
                }
            )
            + "</section><section><h2>代码、测试与交付关系</h2>"
            + _relation_summary(relations)
            + "</section>"
        )
    if kind in {"code_file", "code_symbol"}:
        symbols = list(item.get("symbols") or [])
        symbols_html = (
            '<div class="table-scroll" role="region" tabindex="0" aria-label="AST 符号索引表">'
            "<table><thead><tr><th>符号</th><th>类型</th>"
            "<th>签名</th><th>状态</th></tr></thead><tbody>"
            + "".join(
                f'<tr id="symbol-{_escape(_route_id(symbol.get("entity_id")))}">'
                f"<td><strong>{_escape(symbol.get('qualified_name') or symbol.get('display_name'))}</strong>"
                f"<br><code>{_escape(symbol.get('entity_id'))}</code></td>"
                f"<td>{_escape(symbol.get('symbol_kind'))}</td>"
                f"<td><code>{_escape(symbol.get('signature_text'))}</code></td>"
                f"<td>{_status(symbol.get('lifecycle_status'))}</td></tr>"
                for symbol in symbols
            )
            + "</tbody></table></div>"
            if symbols
            else '<p class="missing-state">当前代码文件未登记 AST 符号。</p>'
        )
        return (
            "<section><h2>代码职责与文件信息</h2>"
            + _readable(item.get("code_file") or item.get("code_symbol") or summary)
            + "</section><section><h2>AST 符号索引</h2>"
            + symbols_html
            + "</section><section><h2>实现与验证关系</h2>"
            + _relation_summary(relations)
            + "</section>"
        )
    if kind == "test":
        return (
            "<section><h2>验证目标与执行状态</h2>"
            + _readable(item.get("test") or summary)
            + "</section><section><h2>覆盖关系</h2>"
            + _relation_summary(relations)
            + "</section>"
        )
    return (
        "<section><h2>目标与说明</h2>"
        + _readable(summary)
        + "</section><section><h2>关联对象</h2>"
        + _relation_summary(relations)
        + "</section>"
    )


def _field_values(values: dict[str, Any]) -> str:
    if not values:
        return '<div class="empty"><p>当前没有可展示的字段数据。</p></div>'
    rows = []
    state_labels = {
        "known": "已知",
        "unknown": "待补充",
        "not_registered": "暂无数据源",
        "not_applicable": "不适用",
    }
    for field_id, field in sorted(values.items()):
        state = str(field.get("state", "unknown"))
        value = field.get("value") if state == "known" else state_labels.get(state, state)
        field_label = field.get("label") or field_id
        rows.append(
            f'<tr data-value-state="{_escape(state)}"><th scope="row">'
            f"{_escape(field_label)}<br><code>{_escape(field_id)}</code></th>"
            f'<td><span class="value-state value-state--{_escape(state)}">'
            f"{_escape(state_labels.get(state, state))}</span></td><td>{_escape(value)}</td>"
            f"<td><code>{_escape(field.get('source_path'))}</code></td></tr>"
        )
    return (
        '<div class="table-scroll" role="region" tabindex="0" aria-label="项目管理字段表">'
        "<table><thead><tr><th>字段中文名</th><th>状态</th>"
        "<th>值</th><th>来源</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>"
    )


class ProjectSiteRenderer:
    def __init__(self) -> None:
        self._previous_page_inputs: dict[str, str] = {}
        self._previous_page_fingerprints: dict[str, str] = {}
        self._page_input_fingerprints: dict[str, str] = {}
        self._reused_page_fingerprints: dict[str, str] = {}

    def render(
        self,
        model: dict[str, Any],
        *,
        profile: str,
        previous: dict[str, object] | None = None,
    ) -> RenderedSite:
        previous = previous or {}
        raw_previous_inputs = previous.get("page_inputs")
        previous_inputs = raw_previous_inputs if isinstance(raw_previous_inputs, dict) else {}
        raw_previous_pages = previous.get("pages")
        previous_pages = raw_previous_pages if isinstance(raw_previous_pages, dict) else {}
        self._previous_page_inputs = {
            str(route): str(fingerprint) for route, fingerprint in previous_inputs.items()
        }
        self._previous_page_fingerprints = {
            str(route): str(fingerprint) for route, fingerprint in previous_pages.items()
        }
        self._page_input_fingerprints = {}
        self._reused_page_fingerprints = {}
        pages: dict[str, str] = {"assets/styles.css": _STYLES}
        project = dict(model.get("project") or {})
        generation = dict(model.get("generation") or {})
        pages["assets/snapshot.js"] = _snapshot_script(generation, profile)
        entities = [dict(item) for item in model.get("entities", [])]
        documents = [dict(item) for item in model.get("documents", [])]
        diagnostics = [dict(item) for item in model.get("diagnostics", [])]
        versions = [dict(item) for item in model.get("versions", [])]
        pm = dict(model.get("pm") or {})
        requirements = [
            item
            for item in entities
            if item.get("entity_kind")
            in {"requirement", "non_functional_requirement", "acceptance_criterion"}
        ]
        raw_tasks = [
            item for item in entities if item.get("entity_kind") in {"work_item", "work_item_event"}
        ]
        tasks = _prepare_tasks(raw_tasks, documents)
        code_files = [item for item in entities if item.get("entity_kind") == "code_file"]
        code_symbols = [item for item in entities if item.get("entity_kind") == "code_symbol"]
        code = code_files or code_symbols
        tests = [item for item in entities if item.get("entity_kind") == "test"]
        human_documents = [
            item for item in documents if str(item.get("relative_path") or "").startswith("docs/")
        ]
        design_documents = [
            item
            for item in human_documents
            if "/05-design/" in f"/{item.get('relative_path', '')}"
        ]
        task_counts = {
            status: sum(task.get("_kanban_status") == status for task in tasks)
            for status, _ in _KANBAN_COLUMNS
        }
        completed_ratio = round(task_counts["done"] * 100 / len(tasks)) if tasks else 0
        cards = [
            ("任务总数", len(tasks), "来自当前有效任务事实"),
            ("正在执行", task_counts["in_progress"], "不包含历史已完成任务"),
            ("测试与评审", task_counts["testing"] + task_counts["review"], "内部步骤自动连续执行"),
            ("已经完成", task_counts["done"], f"当前完成比例 {completed_ratio}%"),
        ]
        if any(task_counts[key] for key in ("in_progress", "testing", "review")):
            project_status = "进行中"
        elif task_counts["blocked"]:
            project_status = "待确认 / 阻塞"
        elif task_counts["todo"]:
            project_status = "待开始"
        else:
            project_status = "已完成"
        overview = (
            '<section class="hero"><p class="eyebrow">项目实时任务快照</p>'
            f"<h1>{_escape(project.get('name') or 'Project')} 任务看板</h1>"
            '<p class="hero-copy">按真实任务状态展示当前工作；卡片只显示中文标题，点击进入完整详情。'
            '</p><div class="hero-status">'
            f"{_status(project_status)}<span>已完成 {task_counts['done']} / {len(tasks)}</span>"
            "</div></section>"
            + '<section class="kanban-section"><div class="section-heading"><div><p class="eyebrow">敏捷开发</p>'
            '<h2>任务看板</h2></div><a href="tasks/index.html">打开任务看板</a></div>'
            + _kanban_board(tasks, "tasks/{id}.html")
            + "</section>"
            + _summary_cards(cards)
        )
        pages["index.html"] = self._page(
            "项目总览", overview, route="index.html", generation=generation, profile=profile
        )
        self._entity_section(
            pages,
            title="需求与验收",
            intro="说清为什么做、做到什么程度，以及如何验收。",
            list_route="requirements/index.html",
            detail_root="requirements",
            items=requirements,
            generation=generation,
            profile=profile,
        )
        self._document_section(
            pages,
            list_route="design/index.html",
            detail_root="design",
            title="设计与模块边界",
            documents=design_documents,
            generation=generation,
            profile=profile,
        )
        self._entity_section(
            pages,
            title="计划与里程碑",
            intro="以当前有效任务事实展示顺序、条件和下一动作。",
            list_route="plans/index.html",
            detail_root="plans",
            items=tasks,
            generation=generation,
            profile=profile,
        )
        pages["tasks/index.html"] = self._page(
            "任务看板",
            '<section class="page-heading"><p class="eyebrow">当前有效视图</p><h1>任务看板</h1>'
            "<p>每张卡片只显示中文任务标题；点击后查看任务编号、目标、状态、完成条件和来源。</p></section>"
            + _kanban_board(tasks, "{id}.html"),
            route="tasks/index.html",
            generation=generation,
            profile=profile,
        )
        for item in tasks:
            self._entity_detail(pages, item, "tasks", "tasks/index.html", generation, profile)
        defect_items = diagnostics
        pages["defects/index.html"] = self._page(
            "缺陷与异常",
            '<section class="page-heading"><p class="eyebrow">问题管理</p><h1>缺陷与异常</h1>'
            "<p>只展示已有诊断，不从缺失信息推导缺陷。</p></section>"
            + _list_items(defect_items, "{id}.html"),
            route="defects/index.html",
            generation=generation,
            profile=profile,
        )
        for item in defect_items:
            self._diagnostic_detail(
                pages, item, "defects", "defects/index.html", generation, profile
            )
        pages["execution/index.html"] = self._page(
            "执行中心",
            '<section class="page-heading"><p class="eyebrow">交付执行</p><h1>执行中心</h1>'
            f"<p>当前有 {len(tasks)} 条任务事实、{len(defect_items)} 条诊断。</p></section>"
            '<div class="action-grid"><a class="action-card" href="../tasks/index.html">任务列表</a>'
            '<a class="action-card" href="../defects/index.html">缺陷列表</a></div>',
            route="execution/index.html",
            generation=generation,
            profile=profile,
        )
        quality_items = [*tests, *diagnostics]
        pages["quality/index.html"] = self._page(
            "质量与可追溯性",
            '<section class="page-heading"><p class="eyebrow">证据与风险</p><h1>质量与可追溯性</h1>'
            "<p>集中展示测试、评审、断链和安全诊断。</p></section>"
            + _list_items(quality_items, "{id}.html"),
            route="quality/index.html",
            generation=generation,
            profile=profile,
        )
        for item in tests:
            self._entity_detail(pages, item, "quality", "quality/index.html", generation, profile)
        for item in diagnostics:
            self._diagnostic_detail(
                pages, item, "quality", "quality/index.html", generation, profile
            )
        self._document_section(
            pages,
            list_route="documents/index.html",
            detail_root="documents",
            title="人类文档目录",
            documents=human_documents,
            generation=generation,
            profile=profile,
        )
        self._entity_section(
            pages,
            title="代码地图",
            intro="按模块、文件和 AST 符号稳定定位，不以行号作为身份。",
            list_route="code/index.html",
            detail_root="code",
            items=code,
            generation=generation,
            profile=profile,
        )
        self._version_section(pages, versions, generation, profile)
        self._pm_section(pages, pm, generation, profile)
        self._reports_section(pages, pm, generation, profile)
        fingerprints = {
            route: hashlib.sha256(content.encode("utf-8")).hexdigest()
            for route, content in pages.items()
        }
        fingerprints = {**self._reused_page_fingerprints, **fingerprints}
        site_fingerprint = hashlib.sha256(
            canonical_json(
                {
                    "renderer": RENDERER_VERSION,
                    "profile": profile,
                    "pages": sorted(fingerprints.items()),
                }
            ).encode("utf-8")
        ).hexdigest()
        return RenderedSite(
            pages,
            fingerprints,
            self._page_input_fingerprints,
            site_fingerprint,
            site_input_token(generation, profile),
            str(generation.get("generation_id") or ""),
        )

    def _reuse_detail(self, route: str, item: dict[str, Any], *, profile: str) -> bool:
        input_fingerprint = hashlib.sha256(
            _display_json(
                {
                    "renderer": RENDERER_VERSION,
                    "profile": profile,
                    "route": route,
                    "item": _render_input(item),
                }
            ).encode("utf-8")
        ).hexdigest()
        self._page_input_fingerprints[route] = input_fingerprint
        previous_page = self._previous_page_fingerprints.get(route)
        if previous_page is not None and self._previous_page_inputs.get(route) == input_fingerprint:
            self._reused_page_fingerprints[route] = previous_page
            return True
        return False

    def _page(
        self,
        title: str,
        content: str,
        *,
        route: str,
        generation: dict[str, Any],
        profile: str,
    ) -> str:
        prefix = _prefix(route)
        navigation = "".join(
            f'<a href="{_escape(prefix + href)}">{_escape(label)}</a>'
            for href, label in _NAVIGATION
        )
        footer = (
            "<footer><div><strong>可追溯快照</strong><p>"
            'Generation <span data-snapshot-field="generation">unknown</span> · '
            'Git <span data-snapshot-field="git">unknown</span> · '
            'H <span data-snapshot-field="high_watermark">unknown</span></p></div>'
            '<div><p>as_of <span data-snapshot-field="as_of">unknown</span></p>'
            '<p><span data-snapshot-field="renderer">unknown</span> · '
            '<span data-snapshot-field="profile">unknown</span></p></div></footer>'
        )
        return (
            '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f"<title>{_escape(title)} · Shanforge</title>"
            f'<link rel="stylesheet" href="{_escape(prefix)}assets/styles.css"></head><body>'
            '<a class="skip-link" href="#main">跳到主内容</a>'
            '<header class="site-header"><a class="brand" href="'
            f'{_escape(prefix)}index.html"><span class="brand-mark">S</span><span>Shanforge</span></a>'
            f'<nav aria-label="主导航">{navigation}</nav></header><main id="main">{content}</main>{footer}'
            f'<script defer src="{_escape(prefix)}assets/snapshot.js"></script></body></html>'
        )

    def _entity_section(
        self,
        pages: dict[str, str],
        *,
        title: str,
        intro: str,
        list_route: str,
        detail_root: str,
        items: list[dict[str, Any]],
        generation: dict[str, Any],
        profile: str,
    ) -> None:
        pages[list_route] = self._page(
            title,
            f'<section class="page-heading"><p class="eyebrow">当前有效视图</p><h1>{_escape(title)}</h1>'
            f"<p>{_escape(intro)}</p></section>" + _list_items(items, "{id}.html"),
            route=list_route,
            generation=generation,
            profile=profile,
        )
        for item in items:
            self._entity_detail(pages, item, detail_root, list_route, generation, profile)

    def _entity_detail(
        self,
        pages: dict[str, str],
        item: dict[str, Any],
        detail_root: str,
        back_route: str,
        generation: dict[str, Any],
        profile: str,
    ) -> None:
        entity_id = item.get("entity_id") or item.get("record_id")
        route = f"{detail_root}/{_route_id(entity_id)}.html"
        if self._reuse_detail(route, item, profile=profile):
            return
        content = (
            f'<a class="back-link" href="{_escape(_prefix(route) + back_route)}">← 返回上一列表</a>'
            '<nav class="breadcrumb" aria-label="面包屑">Shanforge / '
            f"{_escape(detail_root)} / {_escape(entity_id)}</nav>"
            '<article class="detail"><p class="eyebrow">详情页</p>'
            f"<h1>{_escape(item.get('display_name') or entity_id)}</h1>"
            f'<div class="detail-status">{_status(item.get("lifecycle_status") or item.get("status"))}</div>'
            + _business_detail_sections(item)
            + "<section><h2>身份与当前状态</h2>"
            + _definition_list(item)
            + "</section><section><h2>定向来源</h2>"
            + _source_summary(item)
            + "</section></article>"
        )
        pages[route] = self._page(
            str(item.get("display_name") or entity_id),
            content,
            route=route,
            generation=generation,
            profile=profile,
        )

    def _diagnostic_detail(
        self,
        pages: dict[str, str],
        item: dict[str, Any],
        detail_root: str,
        back_route: str,
        generation: dict[str, Any],
        profile: str,
    ) -> None:
        adapted = dict(item)
        adapted["entity_id"] = item.get("diagnostic_id")
        adapted["display_name"] = item.get("code")
        adapted["summary"] = item.get("safe_message")
        adapted["lifecycle_status"] = item.get("severity")
        self._entity_detail(pages, adapted, detail_root, back_route, generation, profile)

    def _document_section(
        self,
        pages: dict[str, str],
        *,
        list_route: str,
        detail_root: str,
        title: str,
        documents: list[dict[str, Any]],
        generation: dict[str, Any],
        profile: str,
    ) -> None:
        list_items = [
            {
                "entity_id": document.get("document_id"),
                "display_name": document.get("chinese_name") or document.get("title"),
                "summary": f"读者：{document.get('audience') or '未登记'} · Owner：{document.get('owner') or '未登记'}",
                "lifecycle_status": document.get("doc_status"),
            }
            for document in documents
        ]
        pages[list_route] = self._page(
            title,
            f'<section class="page-heading"><p class="eyebrow">文档导航</p><h1>{_escape(title)}</h1>'
            "<p>每份文档都显示中文名称、读者、Owner、用途和章节索引。</p></section>"
            + _list_items(list_items, "{id}.html"),
            route=list_route,
            generation=generation,
            profile=profile,
        )
        for document in documents:
            document_id = document.get("document_id")
            route = f"{detail_root}/{_route_id(document_id)}.html"
            if self._reuse_detail(route, document, profile=profile):
                continue
            sections = (
                "".join(
                    f"<li><strong>{_escape(section.get('display_title'))}</strong> "
                    f"<code>{_escape(section.get('section_id'))}</code></li>"
                    for section in document.get("sections", [])
                )
                or "<li>当前没有章节索引</li>"
            )
            content = (
                f'<a class="back-link" href="{_escape(_prefix(route) + list_route)}">← 返回上一列表</a>'
                '<article class="detail"><p class="eyebrow">文档详情</p>'
                f"<h1>{_escape(document.get('chinese_name') or document.get('title'))}</h1>"
                + _definition_list(document)
                + f'<section><h2>章节索引</h2><ol class="section-list">{sections}</ol></section>'
                "</article>"
            )
            pages[route] = self._page(
                str(document.get("title")),
                content,
                route=route,
                generation=generation,
                profile=profile,
            )

    def _version_section(
        self,
        pages: dict[str, str],
        versions: list[dict[str, Any]],
        generation: dict[str, Any],
        profile: str,
    ) -> None:
        items = [
            {
                "record_id": item.get("generation_id"),
                "display_name": item.get("generation_id"),
                "summary": f"as_of {item.get('as_of') or '未知'}",
                "status": item.get("status"),
            }
            for item in versions
        ]
        pages["versions/index.html"] = self._page(
            "版本与发布",
            '<section class="page-heading"><p class="eyebrow">当前与上一代</p><h1>版本与发布</h1>'
            "<p>SQLite 只保留当前投影所需代次，完整历史仍由 Git 与 Ledger 保存。</p></section>"
            + _list_items(items, "{id}.html"),
            route="versions/index.html",
            generation=generation,
            profile=profile,
        )
        for source, item in zip(versions, items, strict=True):
            detail = dict(source)
            detail["entity_id"] = item["record_id"]
            detail["display_name"] = item["display_name"]
            detail["summary"] = item["summary"]
            detail["lifecycle_status"] = item["status"]
            self._entity_detail(
                pages, detail, "versions", "versions/index.html", generation, profile
            )

    def _pm_section(
        self,
        pages: dict[str, str],
        pm: dict[str, Any],
        generation: dict[str, Any],
        profile: str,
    ) -> None:
        module_cards = []
        for table, slug, title in _PM_MODULES:
            records = [dict(item) for item in pm.get(table, [])]
            module_cards.append(
                f'<a class="module-card" href="{_escape(slug)}.html"><span>{_escape(title)}</span>'
                f"<strong>{len(records)}</strong><small>条当前记录</small></a>"
            )
            list_items = [
                {
                    "record_id": record.get("record_id"),
                    "display_name": record.get("title") or record.get("record_id"),
                    "summary": "字段状态来自 PM 投影，页面不二次推导。",
                    "status": record.get("summary_status") or record.get("project_status"),
                }
                for record in records
            ]
            module_route = f"project-management/{slug}.html"
            pages[module_route] = self._page(
                title,
                f'<a class="back-link" href="../project-management/index.html">← 返回项目管理总览</a>'
                f'<section class="page-heading"><p class="eyebrow">PM 模块</p><h1>{_escape(title)}</h1>'
                "<p>记录为当前投影；历史从 Git 与权威 Ledger 查询。</p></section>"
                + _list_items(list_items, f"{slug}/{{id}}.html"),
                route=module_route,
                generation=generation,
                profile=profile,
            )
            for record in records:
                record_id = record.get("record_id")
                detail_route = f"project-management/{slug}/{_route_id(record_id)}.html"
                if self._reuse_detail(detail_route, record, profile=profile):
                    continue
                content = (
                    f'<a class="back-link" href="{_escape(_prefix(detail_route) + module_route)}">← 返回上一列表</a>'
                    f'<article class="detail"><p class="eyebrow">{_escape(title)}记录</p>'
                    f"<h1>{_escape(record_id)}</h1><section><h2>投影字段</h2>"
                    + _field_values(dict(record.get("field_values") or {}))
                    + "</section><section><h2>行身份与来源</h2>"
                    + _definition_list(record)
                    + "</section></article>"
                )
                pages[detail_route] = self._page(
                    str(record_id),
                    content,
                    route=detail_route,
                    generation=generation,
                    profile=profile,
                )
        pages["project-management/index.html"] = self._page(
            "项目管理十要素",
            '<section class="page-heading"><p class="eyebrow">项目经理视图</p><h1>项目管理十要素</h1>'
            "<p>章程、团队、范围进度、风险、沟通、会议、行动、状态、变更和收尾统一追溯。</p></section>"
            '<section class="state-guide" aria-labelledby="state-guide-title"><h2 id="state-guide-title">字段状态说明</h2>'
            '<dl><div><dt>已有数据</dt><dd>索引已经找到正式来源和值。</dd></div>'
            '<div><dt>待补充</dt><dd>字段适用于当前项目，但正式来源暂时没有有效值。</dd></div>'
            '<div><dt>暂无数据源</dt><dd>当前项目尚未登记这个字段的数据来源，不代表任务被阻塞。</dd></div>'
            '<div><dt>不适用</dt><dd>项目已明确确认该字段不适用。</dd></div></dl></section>'
            '<div class="module-grid">' + "".join(module_cards) + "</div>",
            route="project-management/index.html",
            generation=generation,
            profile=profile,
        )

    def _reports_section(
        self,
        pages: dict[str, str],
        pm: dict[str, Any],
        generation: dict[str, Any],
        profile: str,
    ) -> None:
        reports = [dict(item) for item in pm.get("pm_status_report", [])]
        current = {
            "entity_id": "current",
            "display_name": "当前项目快照",
            "summary": f"Generation {generation.get('generation_id', 'unknown')}",
            "lifecycle_status": "current",
        }
        items = [current] + [
            {
                "entity_id": report.get("record_id"),
                "display_name": report.get("record_id"),
                "summary": "已登记进度报告",
                "lifecycle_status": report.get("overall_status"),
            }
            for report in reports
        ]
        pages["reports/index.html"] = self._page(
            "项目报告",
            '<section class="page-heading"><p class="eyebrow">只读报告中心</p><h1>项目报告</h1>'
            "<p>快照和状态报告均可独立打开、打印和深链。</p></section>"
            + _list_items(items, "{id}.html"),
            route="reports/index.html",
            generation=generation,
            profile=profile,
        )
        self._entity_detail(pages, current, "reports", "reports/index.html", generation, profile)
        for report, item in zip(reports, items[1:], strict=True):
            detail = dict(report)
            detail.update(item)
            self._entity_detail(pages, detail, "reports", "reports/index.html", generation, profile)


_STYLES = """
:root{color-scheme:light;--blue:#2457d6;--blue-dark:#183b91;--ink:#172033;--muted:#5d6678;--line:#dfe4ec;--surface:#f5f7fb;--success:#177245;--warning:#9a5b00;--radius:14px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif}
*{box-sizing:border-box}body{margin:0;color:var(--ink);background:#fff;line-height:1.6}.skip-link{position:absolute;left:-9999px}.skip-link:focus{left:16px;top:12px;z-index:10;background:#fff;padding:10px;border:2px solid var(--blue)}
.site-header{position:sticky;top:0;z-index:5;display:flex;align-items:center;gap:24px;padding:12px 28px;border-bottom:1px solid var(--line);background:rgba(255,255,255,.96);backdrop-filter:blur(12px)}.brand{display:flex;align-items:center;gap:9px;color:var(--ink);font-weight:800;text-decoration:none}.brand-mark{display:grid;place-items:center;width:30px;height:30px;border-radius:9px;background:var(--blue);color:#fff}.site-header nav{display:flex;gap:4px;overflow:auto}.site-header nav a{white-space:nowrap;color:var(--muted);text-decoration:none;padding:7px 10px;border-radius:8px}.site-header nav a:hover{background:var(--surface);color:var(--blue-dark)}
main{width:min(1220px,calc(100% - 40px));margin:0 auto;padding:38px 0 72px}.hero{padding:42px;border-radius:22px;color:#fff;background:linear-gradient(125deg,#173679,#2457d6 62%,#315fc0)}.hero h1,.page-heading h1{margin:.1em 0 .25em;font-size:clamp(2rem,4vw,3.4rem);line-height:1.15}.detail h1{margin:.1em 0 .25em;font-size:clamp(1.7rem,3vw,2.6rem);line-height:1.18}.hero-copy{max-width:760px;font-size:1.08rem}.hero-status{display:flex;gap:14px;align-items:center;margin-top:24px}.eyebrow{text-transform:uppercase;letter-spacing:.12em;font-size:.76rem;font-weight:800;color:var(--blue)}.hero .eyebrow{color:#dbe6ff}.status-chip{display:inline-flex;align-items:center;padding:3px 9px;border-radius:999px;background:#e9efff;color:var(--blue-dark);font-size:.78rem;font-weight:750}
.metric-grid,.module-grid,.action-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin:22px 0}.metric,.panel,.module-card,.action-card,.detail,.state-guide{border:1px solid var(--line);border-radius:var(--radius);background:#fff;box-shadow:0 8px 28px rgba(34,50,84,.06)}.metric{padding:20px}.metric-label,.metric-note{margin:0;color:var(--muted)}.metric-value{font-size:2rem;font-weight:800;margin:.15em 0}.panel,.detail,.state-guide{padding:28px;margin-top:24px}.section-heading{display:flex;justify-content:space-between;align-items:end;gap:20px}.section-heading h2{margin:0}.section-heading a,.back-link{color:var(--blue);font-weight:700}.page-heading{max-width:850px;margin-bottom:24px}.page-heading p{color:var(--muted);font-size:1.04rem}.record-list{list-style:none;padding:0;margin:0;border-top:1px solid var(--line)}.record-row{display:flex;justify-content:space-between;gap:20px;padding:17px 4px;border-bottom:1px solid var(--line)}.record-row p{margin:.25em 0 0;color:var(--muted)}.record-link{color:var(--ink);font-size:1.02rem;font-weight:760;text-decoration:none}.record-link:hover{color:var(--blue);text-decoration:underline}.empty{padding:30px;border:1px dashed #bbc4d2;border-radius:var(--radius);background:var(--surface);color:var(--muted)}
.kanban-section{margin-top:30px}.kanban-board{display:grid;grid-template-columns:repeat(6,minmax(230px,1fr));gap:14px;margin-top:16px;overflow-x:auto;padding:2px 2px 14px;scrollbar-gutter:stable}.kanban-column{min-width:230px;padding:14px;border:1px solid var(--line);border-radius:var(--radius);background:var(--surface)}.kanban-column header{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:12px}.kanban-column h2{margin:0;font-size:1rem}.kanban-column header span{display:grid;place-items:center;min-width:28px;height:28px;padding:0 7px;border-radius:999px;background:#fff;color:var(--muted);font-size:.8rem;font-weight:800}.kanban-cards{display:grid;gap:9px}.kanban-card{display:block;padding:13px 14px;border:1px solid #d9e0eb;border-radius:11px;background:#fff;color:var(--ink);font-weight:760;line-height:1.45;text-decoration:none;box-shadow:0 3px 12px rgba(34,50,84,.05);overflow-wrap:anywhere}.kanban-card:hover{border-color:var(--blue);color:var(--blue-dark)}.kanban-more summary{cursor:pointer;padding:9px 4px;color:var(--blue);font-weight:750}.kanban-more>div{display:grid;gap:9px;margin-top:8px}.kanban-empty{margin:4px 0;color:var(--muted);font-size:.9rem}.state-guide h2{margin-top:0}.state-guide dl{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:0}.state-guide dl div{padding:14px;border-radius:10px;background:var(--surface)}.state-guide dt{font-weight:800}.state-guide dd{margin:5px 0 0;color:var(--muted)}
.module-grid{grid-template-columns:repeat(3,minmax(0,1fr))}.module-card,.action-card{display:flex;flex-direction:column;padding:22px;text-decoration:none;color:var(--ink)}.module-card strong{font-size:2rem;color:var(--blue)}.module-card small{color:var(--muted)}.module-card:hover,.action-card:hover{border-color:var(--blue);transform:translateY(-1px)}.breadcrumb{margin:12px 0;color:var(--muted);font-size:.88rem}.detail{max-width:980px}.detail section{margin-top:30px}.lead{font-size:1.08rem;color:#34405a}.definition-grid{display:grid;grid-template-columns:minmax(160px,240px) 1fr;border-top:1px solid var(--line)}.definition-grid dt,.definition-grid dd{margin:0;padding:10px;border-bottom:1px solid var(--line)}.definition-grid dt{font-weight:700;background:var(--surface)}.section-list{padding-left:22px}.section-list li{margin:8px 0}.table-scroll{overflow:auto}table{width:100%;border-collapse:collapse;font-size:.9rem}th,td{padding:10px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}thead{background:var(--surface)}code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.85em;word-break:break-all}.value-state{display:inline-flex;padding:2px 7px;border-radius:999px;font-size:.76rem;font-weight:700}.value-state--known{color:var(--success);background:#e6f6ee}.value-state--unknown{color:var(--warning);background:#fff3dc}.value-state--not_registered{color:#6b7280;background:#eef0f3}.value-state--not_applicable{color:#475569;background:#e8edf5}
footer{display:flex;justify-content:space-between;gap:24px;padding:24px 28px;border-top:1px solid var(--line);background:var(--surface);color:var(--muted);font-size:.82rem}footer p{margin:.2em 0}.detail h1,.record-link,.definition-grid dd,footer p,.nested-definition dd,.nested-definition p,.breadcrumb{overflow-wrap:anywhere;word-break:break-word}a:focus-visible,button:focus-visible{outline:3px solid #f2a900;outline-offset:3px}@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important}}
@media (max-width: 1024px){.metric-grid{grid-template-columns:repeat(2,1fr)}.module-grid{grid-template-columns:repeat(2,1fr)}.state-guide dl{grid-template-columns:repeat(2,1fr)}}
@media (max-width: 768px){.site-header{position:static;display:block;padding:12px 16px}.site-header nav{margin-top:10px}.site-header nav a{min-height:44px;display:flex;align-items:center}main{width:min(100% - 28px,720px);padding-top:24px}.hero{padding:28px}.metric-grid,.module-grid,.action-grid,.state-guide dl{grid-template-columns:1fr}.record-row,.section-heading,footer{align-items:flex-start;flex-direction:column}.definition-grid{grid-template-columns:1fr}.definition-grid dd{padding-top:3px}.definition-grid dt{border-bottom:0}.detail,.panel,.state-guide{padding:20px}.kanban-board{grid-template-columns:repeat(6,minmax(82vw,1fr));scroll-snap-type:x proximity}.kanban-column{scroll-snap-align:start}}
@media print{.site-header,.skip-link,.back-link{display:none!important}body{font-size:10pt;color:#000}.hero{color:#000;background:#fff;border:1px solid #999}.metric,.panel,.detail,.module-card{box-shadow:none;break-inside:avoid}main{width:100%;padding:0}footer{background:#fff}}
""".strip()
