#!/usr/bin/env python3
"""Build a small, deterministic PM snapshot from a project's .factory facts."""

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
            return match.group(1).strip().strip("*` ")
    return ""


def _title(text: str, fallback: str) -> str:
    match = re.search(r"(?m)^#\s+(.+?)\s*$", text)
    title = match.group(1).strip() if match else fallback
    return re.sub(rf"^{re.escape(fallback)}\s*[：:—-]\s*", "", title).strip() or fallback


def _section_text(text: str, *names: str) -> str:
    names_pattern = "|".join(re.escape(name) for name in names)
    match = re.search(
        rf"(?ms)^##+\s+(?:\d+\.\s*)?(?:{names_pattern})\s*$\n+(.+?)(?=^##+\s|\Z)",
        text,
    )
    if not match:
        return ""
    for paragraph in re.split(r"\n\s*\n", match.group(1)):
        value = " ".join(line.strip().strip("-* ") for line in paragraph.splitlines()).strip()
        if value and not value.startswith("```"):
            return value
    return ""


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


def _task_brief(directory: Path, task_id: str) -> dict[str, str]:
    task_root = directory / "task-briefs"
    if not task_id or not task_root.is_dir():
        return {}
    for path in sorted(task_root.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        declared_id = _text_field(text, "任务", "Task")
        heading = re.search(r"(?m)^#\s+([A-Za-z0-9._~-]+)", text)
        if task_id not in {path.stem, declared_id, heading.group(1) if heading else ""}:
            continue
        return {
            "title": _title(text, task_id),
            "goal": _summary(text, "目标", "任务目标", "目标和口径"),
            "priority": _text_field(text, "优先级"),
            "scope": _text_field(text, "任务层级", "层级", "类型"),
            "relations": _text_field(text, "关联目标", "关联需求", "追踪目标"),
            "verification": _summary(text, "验证", "验证命令", "完成口径"),
        }
    return {}


def _work_items(root: Path) -> list[dict[str, str]]:
    work_items_root = root / ".factory" / "workitems"
    if not work_items_root.exists():
        return []
    items: list[dict[str, str]] = []
    for directory in sorted(path for path in work_items_root.iterdir() if path.is_dir()):
        brief_path = directory / "brief.md"
        ledger_path = directory / "ledger.jsonl"
        if not brief_path.is_file() and not ledger_path.is_file():
            continue
        brief = brief_path.read_text(encoding="utf-8") if brief_path.exists() else ""
        events = _events(ledger_path)
        event = events[-1] if events else {}
        status = str(event.get("status") or _text_field(brief, "状态") or "unknown")
        category = _category(status)
        task_id = str(event.get("task_id") or event.get("task_card_id") or "")
        task = _task_brief(directory, task_id)
        task_title = str(event.get("task_title") or task.get("title") or "")
        raw_next_action = str(
            event.get("next_required_action")
            or event.get("next_action")
            or _text_field(brief, "唯一下一动作", "下一动作")
            or ""
        )
        relations = task.get("relations") or event.get("traceability_targets") or ""
        if isinstance(relations, list):
            relations = "、".join(str(value) for value in relations)
        items.append(
            {
                "id": directory.name,
                "title": _title(brief, directory.name),
                "status": status,
                "status_label": _status_label(status, category),
                "next_action": _next_step(status, category, raw_next_action, task_title),
                "category": category,
                "purpose": _summary(brief, "用户目标", "目标", "用户意图", "问题"),
                "task_id": task_id,
                "task_title": task_title,
                "task_goal": task.get("goal", ""),
                "priority": task.get("priority", ""),
                "scope": task.get("scope", ""),
                "relations": str(relations),
                "verification": task.get("verification", ""),
                "updated_at": str(
                    event.get("ts")
                    or event.get("time")
                    or event.get("updated_at")
                    or event.get("created_at")
                    or ""
                ),
            }
        )
    order = {"attention": 0, "active": 1, "backlog": 2, "completed": 3}
    items.sort(key=lambda item: item["id"])
    items.sort(key=lambda item: item["updated_at"], reverse=True)
    items.sort(key=lambda item: order[item["category"]])
    return items


def _project_name(root: Path) -> str:
    project_file = root / ".factory" / "project.json"
    if not project_file.exists():
        return root.name
    try:
        value = json.loads(project_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise SnapshotError(f"{project_file}: invalid JSON: {error.msg}") from error
    if not isinstance(value, dict):
        raise SnapshotError(f"{project_file}: project metadata must be an object")
    return str(
        value.get("name") or value.get("project_name") or value.get("project_id") or root.name
    )


def _session(root: Path) -> dict[str, str]:
    path = root / ".factory" / "memory" / "agent-session.md"
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    return {
        key: value
        for key, value in {
            "阶段": _text_field(text, "项目整体进度", "当前阶段", "阶段"),
            "当前任务": _text_field(text, "当前任务", "Work item"),
            "状态": _text_field(text, "当前状态", "状态"),
            "停止原因": _text_field(text, "停止原因"),
            "唯一下一动作": _text_field(text, "唯一下一动作", "下一动作"),
        }.items()
        if value
    }


def _sources(root: Path) -> list[Path]:
    paths = [
        root / ".factory" / "project.json",
        root / ".factory" / "memory" / "agent-session.md",
    ]
    work_items_root = root / ".factory" / "workitems"
    if work_items_root.exists():
        for directory in sorted(path for path in work_items_root.iterdir() if path.is_dir()):
            paths.extend((directory / "brief.md", directory / "ledger.jsonl"))
            task_root = directory / "task-briefs"
            if task_root.is_dir():
                paths.extend(sorted(task_root.glob("*.md")))
    return [path for path in paths if path.is_file()]


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


def _card(item: dict[str, str]) -> str:
    task = ""
    if item["task_title"]:
        metadata = "".join(
            f"<span>{html.escape(value)}</span>"
            for value in (
                item["priority"],
                _scope_label(item["scope"]),
            )
            if value
        )
        task = (
            '<div class="task">'
            '<p class="label">当前任务</p>'
            f"<h4>{html.escape(item['task_title'])}</h4>"
            f'<div class="task-meta">{metadata}</div>'
            + (
                f"<p><strong>任务目标：</strong>{html.escape(item['task_goal'])}</p>"
                if item["task_goal"]
                else ""
            )
            + (
                f"<p><strong>关联需求：</strong>{html.escape(item['relations'])}</p>"
                if item["relations"]
                else '<p class="muted">关联需求尚未登记。</p>'
            )
            + (
                f"<p><strong>完成标准：</strong>{html.escape(item['verification'])}</p>"
                if item["verification"]
                else ""
            )
            + "</div>"
        )
    return (
        f'<article class="work-card work-card--{html.escape(item["category"])}">'
        '<div class="card-heading"><div>'
        f"<h3>{html.escape(item['title'])}</h3>"
        f'<p class="work-id">{html.escape(item["id"])}</p></div>'
        f'<span class="status">{html.escape(item["status_label"])}</span></div>'
        f'<p class="purpose"><strong>为什么做：</strong>'
        f"{html.escape(item['purpose'] or '工作项目标尚未登记。')}</p>"
        + task
        + f'<p class="next"><strong>下一步：{html.escape(item["next_action"])}</strong></p>'
        '<details class="technical"><summary>查看技术状态</summary><dl>'
        f"<dt>工作项 ID</dt><dd><code>{html.escape(item['id'])}</code></dd>"
        f"<dt>原始状态</dt><dd><code>{html.escape(item['status'])}</code></dd>"
        + (
            f"<dt>任务 ID</dt><dd><code>{html.escape(item['task_id'])}</code></dd>"
            if item["task_id"]
            else ""
        )
        + (
            f"<dt>最近更新</dt><dd>{html.escape(item['updated_at'])}</dd>"
            if item["updated_at"]
            else ""
        )
        + "</dl></details></article>"
    )


def _render(project: str, session: dict[str, str], items: list[dict[str, str]]) -> str:
    counts = {
        category: sum(item["category"] == category for item in items)
        for category in ("attention", "active", "backlog", "completed")
    }
    labels = {
        "attention": "需要关注",
        "active": "正在推进",
        "backlog": "后续待办",
        "completed": "已完成",
    }
    session_html = "".join(
        f"<dt>{html.escape(key)}</dt><dd>{html.escape(value)}</dd>"
        for key, value in session.items()
    )
    grouped = {
        category: [item for item in items if item["category"] == category] for category in labels
    }
    focus = next(iter(grouped["active"]), None) or next(iter(grouped["attention"]), None)
    focus_html = (
        '<section class="focus" aria-labelledby="focus-title">'
        '<p class="eyebrow">当前重点</p><h2 id="focus-title">'
        f"{html.escape(focus['title'])}</h2>"
        f"<p>{html.escape(focus['purpose'] or '工作项目标尚未登记。')}</p>"
        + (
            f"<p><strong>当前任务：</strong>{html.escape(focus['task_title'])}</p>"
            if focus["task_title"]
            else ""
        )
        + f'<p class="next"><strong>下一步：{html.escape(focus["next_action"])}</strong></p>'
        "</section>"
        if focus
        else ""
    )
    groups: list[str] = []
    for category in ("attention", "active", "backlog"):
        if grouped[category]:
            groups.append(
                f'<section class="work-group work-group--{category}">'
                f"<h2>{labels[category]}（{counts[category]}）</h2>"
                f'<div class="cards">{"".join(_card(item) for item in grouped[category])}</div>'
                "</section>"
            )
    if grouped["completed"]:
        groups.append(
            '<details class="archive"><summary>'
            f"{labels['completed']}（{counts['completed']}）</summary>"
            f'<div class="cards">{"".join(_card(item) for item in grouped["completed"])}</div>'
            "</details>"
        )
    session_details = (
        f'<details class="archive"><summary>查看会话记录</summary><dl>{session_html}</dl></details>'
        if session_html
        else ""
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(project)} · 项目快照</title>
<style>
:root {{
  color-scheme: light dark; font-family: system-ui,sans-serif;
  --bg:#f5f7fb;--surface:#fff;--text:#172033;--muted:#647086;
  --line:#d9dfeb;--accent:#2359d6;--accent-soft:#eaf0ff;
  --attention:#9a3412;--attention-soft:#fff1e8;--radius:14px;
}}
@media (prefers-color-scheme:dark) {{
  :root {{ --bg:#0f1420;--surface:#171e2c;--text:#eef3ff;--muted:#a7b2c8;
    --line:#344056;--accent:#8db0ff;--accent-soft:#1d315e;
    --attention:#ffb38a;--attention-soft:#402619; }}
}}
* {{ box-sizing:border-box; }}
html {{ scroll-behavior:smooth; }}
body {{ margin:0;background:var(--bg);color:var(--text);line-height:1.6; }}
header,main {{ width:min(1120px,calc(100% - 32px));margin:auto; }}
header {{ padding:48px 0 24px; }}
main {{ padding-bottom:56px; }}
.skip-link {{ position:absolute;left:12px;top:-60px;background:var(--surface);
  color:var(--text);padding:10px 14px;border-radius:8px;z-index:2; }}
.skip-link:focus {{ top:12px; }}
.eyebrow,.label {{ margin:0;color:var(--accent);font-size:.82rem;font-weight:800;
  letter-spacing:.08em;text-transform:uppercase; }}
h1,h2,h3,h4 {{ line-height:1.25;overflow-wrap:anywhere; }}
h1 {{ margin:.2rem 0;font-size:clamp(2rem,5vw,3.4rem); }}
h2 {{ margin-top:36px; }}
.intro,.muted,.work-id,small {{ color:var(--muted); }}
.summary,.cards {{ display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px; }}
.summary {{ margin:24px 0;grid-template-columns:repeat(4,minmax(0,1fr)); }}
.metric,.work-card,.focus,.archive {{ border:1px solid var(--line);
  border-radius:var(--radius);background:var(--surface); }}
.metric {{ padding:18px; }}
.metric strong {{ display:block;font-size:1.7rem; }}
.focus {{ padding:24px;border-color:var(--accent);background:var(--accent-soft); }}
.focus h2 {{ margin:.3rem 0; }}
.card-heading {{ display:flex;justify-content:space-between;align-items:flex-start;gap:14px; }}
.work-card {{ padding:20px;min-width:0; }}
.work-card h3 {{ margin:0; }}
.work-id {{ margin:.3rem 0;font-size:.84rem; }}
.status {{ flex:none;border:1px solid currentColor;border-radius:999px;padding:3px 9px;
  color:var(--accent);font-size:.82rem;font-weight:750; }}
.work-card--attention .status {{ color:var(--attention); }}
.purpose {{ margin:18px 0; }}
.task {{ border-left:3px solid var(--accent);padding:4px 0 4px 14px; }}
.task h4 {{ margin:.25rem 0; }}
.task-meta {{ display:flex;flex-wrap:wrap;gap:8px;margin:8px 0; }}
.task-meta span {{ border-radius:999px;background:var(--accent-soft);padding:2px 8px;
  color:var(--accent);font-size:.8rem;font-weight:750; }}
.next {{ margin:18px 0 0; }}
.technical {{ margin-top:16px;color:var(--muted); }}
summary {{ cursor:pointer;font-weight:750; }}
summary:hover {{ color:var(--accent); }}
a:focus-visible,summary:focus-visible {{ outline:3px solid var(--accent);outline-offset:4px; }}
dl {{ display:grid;grid-template-columns:max-content 1fr;gap:6px 14px; }}
dt {{ font-weight:700; }} dd {{ margin:0;overflow-wrap:anywhere; }}
code {{ overflow-wrap:anywhere; }}
.archive {{ margin-top:36px;padding:18px; }}
.archive>summary {{ font-size:1.35rem; }}
.archive>.cards {{ margin-top:18px; }}
@media (max-width:760px) {{
  header,main {{ width:min(100% - 24px,1120px); }}
  header {{ padding-top:28px; }}
  .summary,.cards {{ grid-template-columns:1fr; }}
  .summary {{ grid-template-columns:repeat(2,minmax(0,1fr)); }}
  .card-heading {{ display:block; }}
  .status {{ display:inline-block;margin-top:8px; }}
  dl {{ grid-template-columns:1fr;gap:2px; }}
  dd {{ margin-bottom:8px; }}
}}
</style>
</head>
<body>
<a class="skip-link" href="#main">跳到主要内容</a>
<header><h1>{html.escape(project)} · 项目快照</h1>
<p class="intro">先看正在做什么、为什么做、是否需要你处理，再按需展开技术状态。</p>
<p><small>工作项统计，不等于产品功能完成率。页面由项目事实确定性生成。</small></p></header>
<main id="main">
<div class="summary">
<div class="metric"><strong>{len(items)}</strong>工作项</div>
<div class="metric"><strong>{counts["active"]}</strong>正在推进</div>
<div class="metric"><strong>{counts["attention"]}</strong>需要关注</div>
<div class="metric"><strong>{counts["completed"]}</strong>已完成</div>
</div>
{focus_html}
{"".join(groups) or "<p>尚未登记工作项。</p>"}
{session_details}
</main>
</body>
</html>
"""


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
    if output.exists() and metadata.exists():
        try:
            previous = json.loads(metadata.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            previous = {}
        if not isinstance(previous, dict):
            raise SnapshotError(f"{metadata}: metadata must be an object")
        if previous.get("generation_id") == generation_id:
            return _receipt(root, output, generation_id, True, len(sources), relative_paths)

    items = _work_items(root)
    page = _render(_project_name(root), _session(root), items)
    output_dir.mkdir(parents=True, exist_ok=True)
    _atomic_write(output, page)
    _atomic_write(
        metadata,
        json.dumps(
            {"generation_id": generation_id, "source_count": len(sources)},
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
