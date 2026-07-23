from __future__ import annotations

import os
import re
import sqlite3
from pathlib import Path

import pytest

from application.project_knowledge.site_service import ProjectSiteService
from domain.project_knowledge.models import AccessClass, SourceDefinition
from runtime.project_knowledge.extractors import PythonExtractor
from runtime.project_knowledge.site_renderer import ProjectSiteRenderer
from settings.project_knowledge.schema import create_schema
from settings.project_knowledge.site_publisher import AtomicSitePublisher


def site_model() -> dict[str, object]:
    entities = [
        {
            "entity_id": "REQ-1",
            "entity_kind": "requirement",
            "display_name": "<script>alert(1)</script> 快速快照",
            "summary": "用固定命令查看项目。",
            "lifecycle_status": "approved",
            "details": {
                "background": "项目事实分散，查看成本高。",
                "user_scenarios": ["项目负责人在会话中请求查看当前进度。"],
                "expected_result": "返回最后有效的只读项目站点。",
                "scope": "需求、设计、任务、代码和质量视图。",
                "non_goals": "不在页面中编辑事实。",
                "release": "通过固定 CLI 发布静态快照。",
            },
            "requirement": {
                "acceptance_criteria": [
                    {
                        "acceptance_id": "REQ-1-AC-1",
                        "statement": "输入未变化时复用最后站点。",
                        "criterion_status": "approved",
                    }
                ]
            },
            "relations": [
                {
                    "relation_type": "IMPLEMENTS",
                    "entity_id": "TASK-1",
                    "display_name": "实现项目索引",
                }
            ],
            "locators": [
                {
                    "relative_path": "requirements.json",
                    "locator_kind": "json_pointer",
                    "selector": {"pointer": "/requirements/0"},
                }
            ],
        },
        {
            "entity_id": "TASK-1",
            "entity_kind": "work_item",
            "display_name": "实现项目索引",
            "summary": "目标：快速查看。完成条件：测试通过。",
            "lifecycle_status": "in_progress",
            "details": {
                "goal": "让用户快速理解项目当前状态。",
                "reason": "避免 AI 每次重新扫描和计算。",
                "scope": "索引与静态站点。",
                "out_of_scope": "页面编辑。",
                "completion_conditions": ["测试通过", "独立评审批准"],
                "blockers": [],
                "next_action": "完成独立评审。",
            },
            "work_item": {"task_status": "in_progress"},
            "relations": [],
            "locators": [],
        },
        {
            "entity_id": "py:demo:file",
            "entity_kind": "code_file",
            "display_name": "demo.py",
            "summary": "演示项目快照入口。",
            "lifecycle_status": "active",
            "code_file": {"language": "python", "import_name": "demo"},
            "symbols": [
                {
                    "entity_id": "py:demo:run:function",
                    "display_name": "run",
                    "qualified_name": "demo.run",
                    "symbol_kind": "function",
                    "signature_text": "def run() -> None",
                    "lifecycle_status": "active",
                }
            ],
        },
        {
            "entity_id": "py:demo:run:function",
            "entity_kind": "code_symbol",
            "display_name": "run",
            "summary": "def run() -> None",
            "lifecycle_status": "active",
        },
        {
            "entity_id": "TEST-1",
            "entity_kind": "test",
            "display_name": "test_snapshot",
            "summary": "快照回归测试",
            "lifecycle_status": "passed",
        },
    ]
    pm = {
        table: [
            {
                "record_id": f"{table}:1",
                "field_values": {
                    f"{table}.field": {
                        "state": state,
                        "value": "值" if state == "known" else None,
                        "source_path": "/source",
                    }
                },
            }
        ]
        for table, state in zip(
            (
                "pm_project_profile",
                "pm_party",
                "pm_work_plan",
                "pm_risk",
                "pm_communication",
                "pm_meeting",
                "pm_action_item",
                "pm_status_report",
                "pm_change_request",
                "pm_project_summary",
            ),
            (
                "known",
                "unknown",
                "not_registered",
                "not_applicable",
                "known",
                "known",
                "known",
                "known",
                "known",
                "known",
            ),
            strict=True,
        )
    }
    return {
        "project": {"name": "Shanforge", "status": "in_progress", "completion": 42},
        "generation": {
            "generation_id": "g1",
            "git_commit": "abc123",
            "facts_high_watermark": 42,
            "as_of": "2026-07-22T00:00:00Z",
            "source_manifest_sha256": "a" * 64,
        },
        "entities": entities,
        "edges": [],
        "documents": [
            {
                "document_id": "DOC-DESIGN",
                "title": "系统架构设计",
                "chinese_name": "系统架构设计",
                "audience": "架构师、开发者",
                "owner": "Architecture",
                "doc_status": "active",
                "relative_path": "docs/05-design/system-architecture.md",
                "sections": [{"display_title": "架构边界", "section_id": "SEC-1"}],
            }
        ],
        "diagnostics": [
            {
                "diagnostic_id": "D-1",
                "severity": "warning",
                "code": "LINK_STALE",
                "safe_message": "链接需要刷新",
            }
        ],
        "versions": [{"generation_id": "g1", "status": "current", "as_of": "2026-07-22"}],
        "pm": pm,
    }


def test_renderer_creates_commercial_readonly_multi_page_information_architecture() -> None:
    rendered = ProjectSiteRenderer().render(site_model(), profile="local-owner")
    required = {
        "index.html",
        "requirements/index.html",
        "requirements/REQ-1.html",
        "design/index.html",
        "design/DOC-DESIGN.html",
        "plans/index.html",
        "execution/index.html",
        "tasks/TASK-1.html",
        "defects/index.html",
        "quality/index.html",
        "quality/TEST-1.html",
        "documents/index.html",
        "documents/DOC-DESIGN.html",
        "code/index.html",
        "versions/index.html",
        "versions/g1.html",
        "project-management/index.html",
        "reports/index.html",
        "assets/styles.css",
        "assets/snapshot.js",
    }
    assert required <= set(rendered.pages)
    code_details = [
        route
        for route in rendered.pages
        if route.startswith("code/") and route != "code/index.html"
    ]
    assert len(code_details) == 1
    assert code_details[0].startswith("code/py-demo-file-")
    assert "%" not in code_details[0]
    assert 'id="symbol-py-demo-run-function-' in rendered.pages[code_details[0]]
    assert "def run() -&gt; None" in rendered.pages[code_details[0]]
    assert (
        'role="region" tabindex="0" aria-label="AST 符号索引表"' in rendered.pages[code_details[0]]
    )
    for route, page in rendered.pages.items():
        if route.endswith(".html") and route != "index.html" and not route.endswith("/index.html"):
            assert "← 返回" in page
    combined = "\n".join(rendered.pages.values())
    assert "drawer" not in combined.lower()
    assert "<dialog" not in combined.lower()
    assert "<script>alert(1)</script>" not in combined
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in combined
    assert "@media print" in rendered.pages["assets/styles.css"]
    assert "@media (max-width: 768px)" in rendered.pages["assets/styles.css"]
    assert ":focus-visible" in rendered.pages["assets/styles.css"]
    assert "overflow-wrap:anywhere" in rendered.pages["assets/styles.css"]
    assert (
        ".nested-definition dd,.nested-definition p,.breadcrumb"
        in rendered.pages["assets/styles.css"]
    )
    assert "font-size:clamp(1.7rem,3vw,2.6rem)" in rendered.pages["assets/styles.css"]
    assert "#315fc0" in rendered.pages["assets/styles.css"]
    assert "#4c7df0" not in rendered.pages["assets/styles.css"]
    assert "编辑" not in rendered.pages["index.html"]
    assert "稳定 ID" in rendered.pages["tasks/TASK-1.html"]
    assert "进行中" in rendered.pages["tasks/TASK-1.html"]
    assert "执行任务" in rendered.pages["tasks/TASK-1.html"]
    assert ">in_progress<" not in rendered.pages["tasks/TASK-1.html"]
    requirement_page = rendered.pages["requirements/REQ-1.html"]
    for heading in (
        "背景、问题与目标",
        "使用场景与预期结果",
        "范围与非目标",
        "验收条件",
        "设计、任务、代码与测试",
        "发布与活动",
    ):
        assert heading in requirement_page
    task_page = rendered.pages["tasks/TASK-1.html"]
    for heading in (
        "任务目标与原因",
        "范围与非范围",
        "完成条件",
        "当前进度、阻塞与下一步",
        "关联需求",
        "相关设计",
        "代码、测试与交付",
    ):
        assert heading in task_page
    assert "让用户快速理解项目当前状态" in task_page
    assert "定向来源" not in requirement_page
    assert "定向来源" not in task_page
    assert "block_sha256" not in requirement_page
    assert "document_id" not in task_page
    assert "related_requirements" not in task_page
    assert "related_designs" not in task_page


def test_renderer_translates_unknown_business_values_to_explicit_missing_state() -> None:
    model = site_model()
    requirement = model["entities"][0]  # type: ignore[index]
    requirement["summary"] = "unknown"
    requirement["details"] = {}  # type: ignore[index]
    page = (
        ProjectSiteRenderer().render(model, profile="local-owner").pages["requirements/REQ-1.html"]
    )
    assert "当前暂无可展示的正式数据。" in page
    assert "<dd>待补充</dd>" in page
    assert (
        '<h2>背景、问题与目标</h2><p class="missing-state">当前暂无可展示的正式数据。</p>'
        in page
    )


def test_renderer_groups_requirements_links_relations_and_renders_full_document_body() -> None:
    model = site_model()
    requirement = model["entities"][0]  # type: ignore[index]
    requirement["details"]["category"] = "项目查看与管理"  # type: ignore[index]
    requirement["relations"] = [  # type: ignore[index]
        {
            "relation_type": "IMPLEMENTS",
            "entity_id": "TASK-1",
            "entity_kind": "work_item",
            "display_name": "实现项目索引",
            "strength": "strong",
        },
        {
            "relation_type": "CONTAINS",
            "entity_id": "REQ-1-AC-1",
            "entity_kind": "acceptance_criterion",
            "display_name": "缓存命中时不重写 HTML",
            "strength": "strong",
        },
        {
            "relation_type": "IMPLEMENTS",
            "entity_id": "py:demo:run:function",
            "entity_kind": "code_symbol",
            "route_entity_id": "py:demo:file",
            "route_fragment": "symbol-py-demo-run-function",
            "display_name": "demo.run",
            "strength": "strong",
        },
        {
            "direction": "incoming",
            "relation_type": "SATISFIES",
            "entity_id": "doc:DOC-DESIGN",
            "entity_kind": "document",
            "display_name": "系统架构设计",
            "strength": "strong",
        },
    ]
    task = model["entities"][1]  # type: ignore[index]
    task["relations"] = [  # type: ignore[index]
        {
            "direction": "outgoing",
            "relation_type": "IMPLEMENTS",
            "entity_id": "REQ-1",
            "entity_kind": "requirement",
            "display_name": "快速快照",
            "strength": "strong",
        },
        {
            "direction": "outgoing",
            "relation_type": "IMPLEMENTS",
            "entity_id": "REQ-WEAK",
            "entity_kind": "requirement",
            "display_name": "弱关系需求不应展示",
            "strength": "weak",
        },
        {
            "direction": "outgoing",
            "relation_type": "IMPLEMENTS",
            "entity_id": "doc:DOC-DIRECT",
            "entity_kind": "document",
            "display_name": "直接任务设计不应展示",
            "strength": "strong",
        },
    ]
    model["entities"].append(  # type: ignore[union-attr]
        {
            "entity_id": "REQ-1-AC-1",
            "entity_kind": "acceptance_criterion",
            "display_name": "缓存命中时不重写 HTML",
            "summary": "approved",
            "lifecycle_status": "approved",
            "details": {"statement": "缓存命中时不重写 HTML。"},
            "relations": [],
            "locators": [],
        }
    )
    model["entities"].append(  # type: ignore[union-attr]
        {
            "entity_id": "REQ-WEAK",
            "entity_kind": "requirement",
            "display_name": "弱关系需求不应展示",
            "summary": "只用于负例。",
            "lifecycle_status": "approved",
            "details": {},
            "requirement": {"acceptance_criteria": []},
            "relations": [
                {
                    "direction": "incoming",
                    "relation_type": "SATISFIES",
                    "entity_id": "doc:DOC-WEAK-DESIGN",
                    "entity_kind": "document",
                    "display_name": "弱关系派生设计不应展示",
                    "strength": "strong",
                }
            ],
            "locators": [],
        }
    )
    requirement["relations"].append(  # type: ignore[union-attr]
        {
            "direction": "incoming",
            "relation_type": "MENTIONS",
            "entity_id": "doc:DOC-NON-SATISFIES",
            "entity_kind": "document",
            "display_name": "非满足关系设计不应展示",
            "strength": "strong",
        }
    )
    model["documents"].extend(  # type: ignore[union-attr]
        [
            {
                "document_id": "DOC-WEAK-DESIGN",
                "title": "弱关系派生设计不应展示",
                "relative_path": "docs/05-design/weak.md",
                "sections": [],
            },
            {
                "document_id": "DOC-NON-SATISFIES",
                "title": "非满足关系设计不应展示",
                "relative_path": "docs/05-design/mentioned.md",
                "sections": [],
            },
            {
                "document_id": "DOC-DIRECT",
                "title": "直接任务设计不应展示",
                "relative_path": "docs/05-design/direct.md",
                "sections": [],
            },
        ]
    )
    document = model["documents"][0]  # type: ignore[index]
    document["content_markdown"] = (
        "# 系统架构设计\n\n这里是完整正文。\n\n"
        "- 第一项\n- 第二项\n\n`inline_code`\n\n<script>alert(1)</script>\n\n"
        "[危险链接](javascript:alert(1))"
    )

    pages = ProjectSiteRenderer().render(model, profile="local-owner").pages

    requirements_index = pages["requirements/index.html"]
    assert "项目查看与管理" in requirements_index
    assert "REQ-1-AC-1" not in requirements_index
    assert "../tasks/TASK-1.html" in pages["requirements/REQ-1.html"]
    assert (
        "../requirements/REQ-1.html#acceptance-REQ-1-AC-1"
        in pages["requirements/REQ-1.html"]
    )
    assert 'id="acceptance-REQ-1-AC-1"' in pages["requirements/REQ-1.html"]
    assert (
        "../code/py-demo-file-273556e6d64265a0.html#symbol-py-demo-run-function"
        in pages["requirements/REQ-1.html"]
    )
    assert "../requirements/REQ-1.html" in pages["tasks/TASK-1.html"]
    assert "<h2>关联需求</h2>" in pages["tasks/TASK-1.html"]
    assert "<h2>相关设计</h2>" in pages["tasks/TASK-1.html"]
    assert "../design/DOC-DESIGN.html" in pages["tasks/TASK-1.html"]
    assert "通过需求“快速快照”关联" in pages["tasks/TASK-1.html"]
    assert "定向来源" not in pages["tasks/TASK-1.html"]
    assert "related_requirements" not in pages["tasks/TASK-1.html"]
    assert "related_designs" not in pages["tasks/TASK-1.html"]
    assert "json_pointer" not in pages["requirements/REQ-1.html"]
    assert "弱关系需求不应展示" not in pages["tasks/TASK-1.html"]
    assert "弱关系派生设计不应展示" not in pages["tasks/TASK-1.html"]
    assert "非满足关系设计不应展示" not in pages["tasks/TASK-1.html"]
    assert "直接任务设计不应展示" not in pages["tasks/TASK-1.html"]
    document_page = pages["documents/DOC-DESIGN.html"]
    assert "<h1>系统架构设计</h1>" in document_page
    assert "这里是完整正文。" in document_page
    assert "<li>第一项</li>" in document_page
    assert "<code>inline_code</code>" in document_page
    assert "<script>alert(1)</script>" not in document_page
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in document_page
    assert 'href="javascript:' not in document_page
    assert "[危险链接](javascript:alert(1))" in document_page
    assert '<details class="snapshot-details">' in pages["requirements/REQ-1.html"]


def test_overview_is_a_recent_chinese_task_kanban_with_parent_completion_rollup() -> None:
    model = site_model()
    entities = list(model["entities"])  # type: ignore[arg-type]
    entities.extend(
        [
            {
                "entity_id": "task-parent",
                "entity_kind": "work_item",
                "display_name": "TASK-IMPLEMENT-003-P001",
                "summary": "项目知识索引与只读站点已经完成。",
                "lifecycle_status": "completed_local_commit_created",
                "details": {
                    "task_id": "TASK-IMPLEMENT-003-P001",
                    "updated_at": "2026-07-23T00:32:00+08:00",
                },
                "work_item": {"task_status": "completed_local_commit_created"},
                "relations": [],
                "locators": [],
            },
            {
                "entity_id": "task-parent-stale-duplicate",
                "entity_kind": "work_item",
                "display_name": "TASK-IMPLEMENT-003-P001",
                "summary": "旧记录仍在实施中。",
                "lifecycle_status": "in_progress",
                "details": {
                    "task_id": "TASK-IMPLEMENT-003-P001",
                    "updated_at": "2026-07-22T00:00:00+08:00",
                },
                "work_item": {"task_status": "in_progress"},
                "relations": [],
                "locators": [],
            },
            {
                "entity_id": "task-child",
                "entity_kind": "work_item",
                "display_name": "TASK-IMPLEMENT-003-P001-T01",
                "summary": "合同与数据结构已交付。",
                "lifecycle_status": "ready_for_review",
                "details": {
                    "task_id": "TASK-IMPLEMENT-003-P001-T01",
                    "updated_at": "2026-07-22T17:55:00+08:00",
                },
                "work_item": {"task_status": "ready_for_review"},
                "relations": [],
                "locators": [],
            },
            {
                "entity_id": "task-testing",
                "entity_kind": "work_item",
                "display_name": "验证项目快照",
                "summary": "正在运行浏览器回归。",
                "lifecycle_status": "verification_in_progress",
                "details": {"updated_at": "2026-07-23T00:31:00+08:00"},
                "work_item": {"task_status": "verification_in_progress"},
                "relations": [],
                "locators": [],
            },
            {
                "entity_id": "task-parent-without-time",
                "entity_kind": "work_item",
                "display_name": "NO-DATE-PARENT",
                "summary": "无时间父任务已完成。",
                "lifecycle_status": "done",
                "details": {"task_id": "NO-DATE-PARENT"},
                "work_item": {"task_status": "done"},
                "relations": [],
                "locators": [],
            },
            {
                "entity_id": "task-child-without-time",
                "entity_kind": "work_item",
                "display_name": "NO-DATE-PARENT-T01",
                "summary": "无时间子任务等待评审。",
                "lifecycle_status": "ready_for_review",
                "details": {"task_id": "NO-DATE-PARENT-T01"},
                "work_item": {"task_status": "ready_for_review"},
                "relations": [],
                "locators": [],
            },
            {
                "entity_id": "task-offset-parent",
                "entity_kind": "work_item",
                "display_name": "OFFSET-PARENT",
                "summary": "跨时区父任务已完成。",
                "lifecycle_status": "done",
                "details": {
                    "task_id": "OFFSET-PARENT",
                    "updated_at": "2026-07-23T00:00:00+08:00",
                },
                "work_item": {"task_status": "done"},
                "relations": [],
                "locators": [],
            },
            {
                "entity_id": "task-offset-child",
                "entity_kind": "work_item",
                "display_name": "OFFSET-PARENT-T01",
                "summary": "跨时区子任务等待评审。",
                "lifecycle_status": "ready_for_review",
                "details": {
                    "task_id": "OFFSET-PARENT-T01",
                    "updated_at": "2026-07-22T17:00:00Z",
                },
                "work_item": {"task_status": "ready_for_review"},
                "relations": [],
                "locators": [],
            },
            {
                "entity_id": "task-timezone-duplicate-old",
                "entity_kind": "work_item",
                "display_name": "TIMEZONE-DUPLICATE",
                "summary": "跨时区重复任务旧状态。",
                "lifecycle_status": "done",
                "details": {
                    "task_id": "TIMEZONE-DUPLICATE",
                    "updated_at": "2026-07-23T00:00:00+08:00",
                },
                "work_item": {"task_status": "done"},
                "relations": [],
                "locators": [],
            },
            {
                "entity_id": "task-timezone-duplicate-new",
                "entity_kind": "work_item",
                "display_name": "TIMEZONE-DUPLICATE",
                "summary": "跨时区重复任务正在执行。",
                "lifecycle_status": "in_progress",
                "details": {
                    "task_id": "TIMEZONE-DUPLICATE",
                    "updated_at": "2026-07-22T17:00:00Z",
                },
                "work_item": {"task_status": "in_progress"},
                "relations": [],
                "locators": [],
            },
            {
                "entity_id": "task-unknown-slug",
                "entity_kind": "work_item",
                "display_name": "TASK-QUALITY-999-remove-graphql-skill",
                "summary": "清理旧查询接口。",
                "lifecycle_status": "done",
                "details": {
                    "task_id": "TASK-QUALITY-999-remove-graphql-skill",
                    "updated_at": "2026-07-22T18:00:00Z",
                },
                "work_item": {"task_status": "done"},
                "relations": [],
                "locators": [],
            },
            {
                "entity_id": "task-fast-path",
                "entity_kind": "work_item",
                "display_name": "TASK-SKILL-003-simple-task-fast-path",
                "summary": "快速通道已完成。",
                "lifecycle_status": "done",
                "details": {
                    "task_id": "TASK-SKILL-003-simple-task-fast-path",
                    "updated_at": "2026-07-22T12:00:00+08:00",
                },
                "work_item": {"task_status": "done"},
                "relations": [],
                "locators": [],
            },
        ]
    )
    for index in range(12):
        entities.append(
            {
                "entity_id": f"task-complete-{index}",
                "entity_kind": "work_item",
                "display_name": f"完成任务{index + 1}",
                "summary": "已完成。",
                "lifecycle_status": "done",
                "details": {"updated_at": f"2026-07-{index + 1:02d}T10:00:00+08:00"},
                "work_item": {"task_status": "done"},
                "relations": [],
                "locators": [],
            }
        )
    model["entities"] = entities
    documents = list(model["documents"])  # type: ignore[arg-type]
    documents.extend(
        [
            {
                "document_id": "BRIEF-PARENT",
                "title": "TASK-IMPLEMENT-003-P001 项目知识索引与只读站点",
                "relative_path": (
                    ".factory/workitems/FLOW-CONTRACT-001/task-briefs/"
                    "TASK-IMPLEMENT-003-P001.md"
                ),
                "doc_status": "active",
                "sections": [],
            },
            {
                "document_id": "BRIEF-T01",
                "title": "T01 合同内核与 39 表 Schema",
                "relative_path": (
                    ".factory/workitems/FLOW-CONTRACT-001/task-briefs/"
                    "TASK-IMPLEMENT-003-P001-T01-contract-and-schema.md"
                ),
                "doc_status": "active",
                "sections": [],
            },
        ]
    )
    model["documents"] = documents

    rendered = ProjectSiteRenderer().render(model, profile="local-owner")
    overview = rendered.pages["index.html"]
    tasks_page = rendered.pages["tasks/index.html"]

    for label in ("待开始", "进行中", "测试中", "待评审", "待确认 / 阻塞", "已完成"):
        assert label in overview
    assert 'class="kanban-board"' in overview
    assert "合同内核与 39 表数据结构" in overview
    assert "简单任务快速通道" in overview
    assert "TASK-IMPLEMENT-003-P001-T01" not in overview
    assert "TASK-SKILL-003-simple-task-fast-path" not in overview
    assert overview.count("项目知识索引与只读站点") == 1
    assert ">项目任务<" not in overview
    assert ">等待独立评审<" not in overview
    assert '<details class="kanban-more">' in overview
    assert re.search(r"<summary>更多（\d+）</summary>", overview)
    assert overview.count('class="kanban-card kanban-card--visible"') <= 60
    assert 'data-kanban-status="testing"' in overview
    completed_column = re.search(
        r'<section class="kanban-column" data-kanban-status="done">(.*?)</section>',
        overview,
        re.DOTALL,
    )
    assert completed_column is not None
    assert "合同内核与 39 表数据结构" in completed_column.group(1)
    assert "等待独立评审" not in completed_column.group(1)
    review_column = re.search(
        r'<section class="kanban-column" data-kanban-status="review">(.*?)</section>',
        overview,
        re.DOTALL,
    )
    assert review_column is not None
    assert "无时间子任务等待评审" in review_column.group(1)
    assert "无时间子任务等待评审" not in completed_column.group(1)
    assert "跨时区子任务等待评审" in review_column.group(1)
    assert "跨时区子任务等待评审" not in completed_column.group(1)
    in_progress_column = re.search(
        r'<section class="kanban-column" data-kanban-status="in_progress">(.*?)</section>',
        overview,
        re.DOTALL,
    )
    assert in_progress_column is not None
    assert "跨时区重复任务正在执行" in in_progress_column.group(1)
    assert "跨时区重复任务旧状态" not in completed_column.group(1)
    assert "清理旧查询接口" in completed_column.group(1)
    assert ">技能<" not in overview
    assert 'class="kanban-board"' in tasks_page
    assert "中文任务标题" in tasks_page
    assert "TASK-IMPLEMENT-003-P001-T01" in rendered.pages["tasks/task-child.html"]
    card_titles = re.findall(r'class="kanban-card[^>]*>([^<]+)</a>', overview)
    assert card_titles
    assert all(re.search(r"[\u4e00-\u9fff]", title) for title in card_titles)
    assert all(not re.search(r"[A-Za-z]", title) for title in card_titles)


def test_overview_with_only_todo_tasks_reports_todo_instead_of_completed() -> None:
    model = site_model()
    model["entities"] = [
        {
            "entity_id": "task-todo-only",
            "entity_kind": "work_item",
            "display_name": "UNMAPPED-001",
            "summary": "同步订单状态。",
            "lifecycle_status": "todo",
            "details": {"task_title": "接入 FooBar 订单同步"},
            "work_item": {"task_status": "todo"},
            "relations": [],
            "locators": [],
        }
    ]

    overview = ProjectSiteRenderer().render(model, profile="local-owner").pages["index.html"]

    hero = re.search(r'<section class="hero">(.*?)</section>', overview, re.DOTALL)
    assert hero is not None
    assert '<span class="status-chip">待开始</span>' in hero.group(1)
    assert '<span class="status-chip">已完成</span>' not in hero.group(1)
    assert "接入 FooBar 订单同步" in overview
    assert "任务标题待补充" not in overview
    assert "接入 订单同步" not in overview


def test_code_detail_renders_real_decorated_symbol_definition_signatures() -> None:
    source = SourceDefinition(
        source_id="source:decorated",
        registry_source_id="SRC-PYTHON",
        kind="python",
        relative_path="src/decorated.py",
        extractor_id="python-ast-v1",
        registry_version="1",
        authority_rank=80,
        access_class=AccessClass.PROJECT,
    )
    contribution = PythonExtractor().extract(
        source,
        b"@wrapped\ndef build(value: int) -> str:\n    return str(value)\n",
    )
    file_entity = next(
        dict(item) for item in contribution["entities"] if item["entity_kind"] == "code_file"
    )
    file_entity["code_file"] = contribution["code_file"]
    file_entity["symbols"] = contribution["symbols"]
    model = site_model()
    model["entities"] = [file_entity]

    rendered = ProjectSiteRenderer().render(model, profile="local-owner")
    code_route = next(
        route
        for route in rendered.pages
        if route.startswith("code/") and route != "code/index.html"
    )
    page = rendered.pages[code_route]
    assert "def build(value: int) -&gt; str:" in page
    assert "@wrapped" not in page


def test_pm_records_have_full_detail_pages_and_preserve_four_states() -> None:
    rendered = ProjectSiteRenderer().render(site_model(), profile="local-owner")
    modules = [route for route in rendered.pages if route.startswith("project-management/")]
    assert len([route for route in modules if route.count("/") == 1]) == 11
    details = [route for route in modules if route.count("/") == 2]
    assert len(details) == 10
    combined = "\n".join(rendered.pages[route] for route in details)
    for state in ("known", "unknown", "not_registered", "not_applicable"):
        assert f'data-value-state="{state}"' in combined
    assert "← 返回" in combined
    assert "字段中文名" in combined
    assert "source_manifest_sha256" not in combined
    assert "row_sha256" not in combined
    assert "generation_id" not in combined
    assert "暂无数据源" in combined
    assert "当前项目尚未登记这个字段的数据来源" in rendered.pages[
        "project-management/index.html"
    ]


def test_atomic_publisher_cache_hit_minimal_redraw_and_old_site_survives_failure(
    tmp_path: Path,
) -> None:
    renderer = ProjectSiteRenderer()
    publisher = AtomicSitePublisher(tmp_path / "site")
    first_render = renderer.render(site_model(), profile="local-owner")
    first = publisher.publish(first_render, profile="local-owner", built_at="2026-07-22T00:00:00Z")
    assert first.cache_hit is False
    current = tmp_path / "site/current"
    first_index = current / "index.html"
    first_mtime = first_index.stat().st_mtime_ns
    assert oct(first_index.stat().st_mode & 0o777) == "0o600"
    assert oct(current.resolve().stat().st_mode & 0o777) == "0o700"

    cached = publisher.publish(first_render, profile="local-owner", built_at="2026-07-22T00:00:01Z")
    assert cached.cache_hit is True
    assert first_index.stat().st_mtime_ns == first_mtime

    changed_model = site_model()
    changed_task = changed_model["entities"][1]  # type: ignore[index]
    changed_task["lifecycle_status"] = "verification_in_progress"
    changed_task["work_item"]["task_status"] = "verification_in_progress"
    changed_task["details"]["updated_at"] = "2026-07-22T00:00:02Z"
    changed_render = renderer.render(
        changed_model,
        profile="local-owner",
        previous=publisher.render_cache(profile="local-owner"),
    )
    assert "requirements/REQ-1.html" not in changed_render.pages
    assert "requirements/REQ-1.html" in changed_render.page_fingerprints
    old_build = current.resolve()
    old_requirement = old_build / "requirements/REQ-1.html"
    old_requirement_ctime = old_requirement.stat().st_ctime_ns
    old_requirement_content = old_requirement.read_text(encoding="utf-8")
    changed = publisher.publish(
        changed_render, profile="local-owner", built_at="2026-07-22T00:00:02Z"
    )
    assert changed.cache_hit is False
    assert changed.reused_pages > 0
    assert (current / "requirements/REQ-1.html").read_text(
        encoding="utf-8"
    ) == old_requirement_content
    assert old_requirement.stat().st_ctime_ns == old_requirement_ctime

    old_target = os.readlink(current)
    failed_model = site_model()
    failed_model["project"]["completion"] = 44  # type: ignore[index]
    with pytest.raises(RuntimeError, match="injected"):
        publisher.publish(
            renderer.render(failed_model, profile="local-owner"),
            profile="local-owner",
            built_at="2026-07-22T00:00:03Z",
            fail_at="before_pointer_replace",
        )
    assert os.readlink(current) == old_target
    assert (current / "index.html").is_file()


def test_atomic_publisher_accepts_internal_fragments_and_rejects_unsafe_schemes() -> None:
    AtomicSitePublisher._validate_routes_and_links(
        {
            "index.html": '<a href="details.html#acceptance-1">详情</a>',
            "details.html": '<div id="acceptance-1">验收标准</div>',
        }
    )
    with pytest.raises(ValueError, match="unsafe external link"):
        AtomicSitePublisher._validate_routes_and_links(
            {"index.html": '<a href="javascript:alert(1)">危险</a>'}
        )


def test_atomic_publisher_rejects_tampered_cached_entry_content(tmp_path: Path) -> None:
    renderer = ProjectSiteRenderer()
    publisher = AtomicSitePublisher(tmp_path / "site")
    rendered = renderer.render(site_model(), profile="local-owner")
    publisher.publish(rendered, profile="local-owner", built_at="2026-07-22T00:00:00Z")

    (tmp_path / "site/current/index.html").write_text("tampered", encoding="utf-8")

    with pytest.raises(RuntimeError, match="content hash"):
        publisher.lookup(input_token=rendered.input_token, profile="local-owner")


def test_atomic_publisher_validates_every_manifest_page_on_cache_hit(tmp_path: Path) -> None:
    renderer = ProjectSiteRenderer()
    publisher = AtomicSitePublisher(tmp_path / "site")
    rendered = renderer.render(site_model(), profile="local-owner")
    publisher.publish(rendered, profile="local-owner", built_at="2026-07-22T00:00:00Z")

    (tmp_path / "site/current/tasks/TASK-1.html").write_text("tampered", encoding="utf-8")
    with pytest.raises(RuntimeError, match="page content hash"):
        publisher.lookup(input_token=rendered.input_token, profile="local-owner")

    (tmp_path / "site/current/tasks/TASK-1.html").unlink()
    with pytest.raises(RuntimeError, match="page manifest"):
        publisher.lookup(input_token=rendered.input_token, profile="local-owner")


def test_atomic_publisher_rejects_page_tamper_with_preserved_size_and_mtime(
    tmp_path: Path,
) -> None:
    renderer = ProjectSiteRenderer()
    publisher = AtomicSitePublisher(tmp_path / "site")
    rendered = renderer.render(site_model(), profile="local-owner")
    publisher.publish(rendered, profile="local-owner", built_at="2026-07-22T00:00:00Z")

    target = tmp_path / "site/current/tasks/TASK-1.html"
    metadata = target.stat()
    original = target.read_bytes()
    replacement = bytearray(original)
    replacement[-1] = ord(" ") if replacement[-1] != ord(" ") else ord("\n")
    target.write_bytes(replacement)
    os.utime(target, ns=(metadata.st_atime_ns, metadata.st_mtime_ns))

    with pytest.raises(RuntimeError, match="page content hash"):
        publisher.lookup(input_token=rendered.input_token, profile="local-owner")


def test_site_publication_registers_current_render_views_and_cache_entries(
    tmp_path: Path,
) -> None:
    database = tmp_path / "knowledge.sqlite3"
    with sqlite3.connect(database) as connection:
        create_schema(connection)
        connection.execute(
            "INSERT INTO pk_generation(generation_id,status,source_root_sha256,schema_version,"
            "created_at) VALUES('g1','current',?,1,'2026-07-22T00:00:00Z')",
            ("a" * 64,),
        )
    rendered = ProjectSiteRenderer().render(site_model(), profile="local-owner")
    publisher = AtomicSitePublisher(tmp_path / "site", database_path=database)
    publisher.publish(rendered, profile="local-owner", built_at="2026-07-22T00:00:00Z")

    with sqlite3.connect(database) as connection:
        assert connection.execute("SELECT COUNT(*) FROM pk_render_view").fetchone()[0] == len(
            rendered.pages
        )
        assert connection.execute(
            "SELECT COUNT(*) FROM pk_cache_entry WHERE cache_kind='site-page'"
        ).fetchone()[0] == len(rendered.pages)
        assert (
            connection.execute(
                "SELECT content_sha256 FROM pk_render_view WHERE output_path='current/index.html'"
            ).fetchone()[0]
            == rendered.page_fingerprints["index.html"]
        )


def test_atomic_publisher_rejects_unsafe_cached_entry_acl_and_symlink(tmp_path: Path) -> None:
    renderer = ProjectSiteRenderer()
    rendered = renderer.render(site_model(), profile="local-owner")

    acl_root = tmp_path / "acl-site"
    acl_publisher = AtomicSitePublisher(acl_root)
    acl_publisher.publish(rendered, profile="local-owner", built_at="2026-07-22T00:00:00Z")
    os.chmod(acl_root / "current/index.html", 0o644)
    with pytest.raises(RuntimeError, match="mode"):
        acl_publisher.lookup(input_token=rendered.input_token, profile="local-owner")

    link_root = tmp_path / "link-site"
    link_publisher = AtomicSitePublisher(link_root)
    link_publisher.publish(rendered, profile="local-owner", built_at="2026-07-22T00:00:00Z")
    outside = tmp_path / "outside.html"
    outside.write_text("outside", encoding="utf-8")
    entry = link_root / "current/index.html"
    entry.unlink()
    entry.symlink_to(outside)
    with pytest.raises(RuntimeError, match="regular file"):
        link_publisher.lookup(input_token=rendered.input_token, profile="local-owner")


def test_site_service_returns_current_entry_without_loading_or_rendering_on_cache_hit(
    tmp_path: Path,
) -> None:
    model = site_model()

    class Data:
        loads = 0

        def current_input_token(self, *, profile: str) -> str:
            from runtime.project_knowledge.site_renderer import site_input_token

            return site_input_token(model["generation"], profile)  # type: ignore[arg-type]

        def load(self, *, profile: str = "local-owner") -> dict[str, object]:
            assert profile == "local-owner"
            self.loads += 1
            return model

    data = Data()
    service = ProjectSiteService(
        data, ProjectSiteRenderer(), AtomicSitePublisher(tmp_path / "site")
    )
    first = service.snapshot(profile="local-owner", built_at="2026-07-22T00:00:00Z")
    second = service.snapshot(profile="local-owner", built_at="2026-07-22T00:00:01Z")
    assert first["cache_hit"] is False
    assert second["cache_hit"] is True
    assert data.loads == 1
