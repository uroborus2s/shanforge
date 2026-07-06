from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_project_management_control_plane_doc_defines_boundaries() -> None:
    doc = read(
        "docs/04-project-development/05-development-process/"
        "project-management-control-plane.md"
    )

    for phrase in (
        "项目管理 Excel 模板不应被当作新事实源",
        "PM 控制面",
        "AI 执行闭环",
        "两层通过 `work_item_id` 连接",
        "`using-shanforge` 的项目恢复顺序",
        "`.factory/pm/dashboard.md`",
        "`.factory/pm/generated/status-dashboard.html`",
        "不作为事实源",
        "不新增单独的 `project-management` skill",
        "skills/using-shanforge/references/status-dashboard-template.html",
    ):
        assert phrase in doc


def test_pm_dashboard_files_support_human_and_ai_views() -> None:
    dashboard = read(".factory/pm/dashboard.md")
    html = read(".factory/pm/generated/status-dashboard.html")
    pm_details = read(".factory/pm/generated/pm-details.html")
    workitems = read(".factory/pm/generated/workitems.html")
    lifecycle = read(".factory/pm/generated/requirements-lifecycle.html")
    readme = read(".factory/pm/README.md")
    rendering = read("skills/using-shanforge/references/pm-dashboard-rendering.md")
    template = read("skills/using-shanforge/references/status-dashboard-template.html")

    assert "PM 控制面负责目标、WBS、状态、风险、变更和人类查看" in dashboard
    assert "generated/status-dashboard.html` 作为人类查看层，不作为事实源" in dashboard
    assert "AI 默认不读取 `generated/status-dashboard.html`" in readme
    assert "<title>shanforge PM Dashboard</title>" in html
    assert "按需生成页面，不作为事实源" in html
    assert "项目甘特图" in html
    assert "项目任务看板" in html
    assert "<h3>未开始任务</h3>" in html
    assert "<h3>正在进行</h3>" in html
    assert "<h3>已完成</h3>" in html
    assert "<h3>已经审批</h3>" in html
    assert "评审链路总览" in html
    assert "WBS / Work Item" in html
    assert "需求实时跟踪表" in html
    assert "当前流程集成需求" in html
    assert 'class="requirements-table"' in html
    assert 'class="task-status-table"' in html
    assert "FLOW-CONTRACT-001（待人工确认）" in html
    assert "SKILL-FLOW-AUDIT-001（待修复）" in html
    assert "SF-SP-001..010（本地闭环）" in html
    assert ".requirements-table col:nth-child(1){width:16%}" in html
    assert ".requirements-table col:nth-child(5){width:9%}" in html
    assert ".requirements-table col:nth-child(6){width:10%}" in html
    assert ".task-status-table col:nth-child(1){width:14%}" in html
    assert 'href="#task-flow-contract-001"' in html
    assert 'href="#task-skill-flow-audit-001"' in html
    assert 'href="#task-sf-sp-bundle"' in html
    assert 'id="task-flow-contract-001"' in html
    assert 'id="task-skill-flow-audit-001"' in html
    assert 'id="task-sf-sp-bundle"' in html
    assert "本地闭环完成" in html
    assert "未进入实施" in html
    assert "开放风险" in html
    assert 'href="requirements-lifecycle.html"' in html
    assert 'href="workitems.html#flow-contract-review-1"' in html
    assert 'href="workitems.html#skill-flow-review-3"' in html
    assert 'href="pm-details.html#team-raci"' in html
    assert 'href="pm-details.html#project-brief"' in html
    assert 'href="pm-details.html#wbs"' in html
    assert 'href="pm-details.html#milestones"' in html
    assert 'href="pm-details.html#risks"' in html
    assert 'href="pm-details.html#communication"' in html
    assert 'href="pm-details.html#meeting-notes"' in html
    assert 'href="pm-details.html#status-report"' in html
    assert 'href="pm-details.html#changes"' in html
    assert 'href="pm-details.html#closure"' in html
    assert 'href="workitems.html#sf-sp-bundle"' in html
    assert ".jsonl\"" not in html
    assert "../" not in html
    assert "完整项目进度入口" in pm_details
    assert "01 项目组成员 / RACI" in pm_details
    assert "05 风险管理" in pm_details
    assert "PM-RISK-001" in pm_details
    assert "FLOW-CONTRACT-001" in pm_details
    assert "SKILL-FLOW-AUDIT-001" in pm_details
    assert "local_commit_closed" in pm_details
    assert "FLOW-CONTRACT-001：流程契约实施前 gate" in workitems
    assert "SKILL-FLOW-AUDIT-001：skill flow 审计" in workitems
    assert "任务详情与评审链路" in workitems
    assert 'id="sf-sp-005-review-2"' in workitems
    assert 'id="sf-sp-005-review-3"' in workitems
    assert 'id="sf-sp-006-review-1"' in workitems
    assert 'id="sf-sp-006-review-2"' in workitems
    assert 'id="sf-sp-007-review-1"' in workitems
    assert 'id="sf-sp-008-review-pending"' in workitems
    assert "SF-SP-001..010：Superpowers workflow cleanup" in workitems
    assert "changes_requested" in workitems
    assert "approved" in workitems
    assert "pending_human_confirmation" in workitems
    assert "local_commit_closed" in workitems
    assert "<title>shanforge Requirements Lifecycle</title>" in lifecycle
    assert "需求生命周期总览" in lifecycle
    assert "REQ-006" in lifecycle
    assert "Session、Memory 与 Context Engine" in lifecycle
    assert "当前流程集成需求" in lifecycle
    assert 'id="task-flow-contract-001"' in lifecycle
    assert 'id="task-skill-flow-audit-001"' in lifecycle
    assert 'id="task-sf-sp-bundle"' in lifecycle
    assert "本地闭环完成" in lifecycle
    assert "需求未关闭" in lifecycle
    assert ".jsonl\"" not in lifecycle
    assert "generated/requirements-lifecycle.html" in readme
    assert "不新增独立 `project-management` skill" in rendering
    assert ".factory/pm/generated/requirements-lifecycle.html" in rendering
    assert "首页链接必须指向渲染后的 HTML 视图" in rendering
    assert "首页必须直接包含需求实时跟踪表" in rendering
    assert "需求生命周期页" in rendering
    assert "项目甘特图" in rendering
    assert "项目任务看板" in rendering
    assert "未开始任务、正在进行、已完成、已经审批" in rendering
    assert "每一轮评审结果必须有人能读懂" in rendering
    assert "{{PROJECT_NAME}}" in template
    assert "{{WBS_ROWS}}" in template
    assert "a{color:#1d4ed8" in template


def test_pm_control_plane_uses_existing_using_shanforge_skill() -> None:
    assert not (REPO_ROOT / "skills/project-management/SKILL.md").exists()

    using_shanforge = read("skills/using-shanforge/SKILL.md")
    assert "当人类要求查看项目状态时，按需渲染 PM 状态页" in using_shanforge
    assert "不新增单独的 `project-management` skill" in using_shanforge

    for relative_path in (
        ".factory/pm/team-raci.md",
        ".factory/pm/project-brief.md",
        ".factory/pm/wbs.md",
        ".factory/pm/milestones.md",
        ".factory/pm/risk-register.jsonl",
        ".factory/pm/communication-plan.md",
        ".factory/pm/meeting-notes/2026-07-05-pm-control-plane.md",
        ".factory/pm/status-reports/2026-07-05.md",
        ".factory/pm/change-register.jsonl",
        ".factory/pm/closure-report.md",
    ):
        assert (REPO_ROOT / relative_path).exists()


def test_pm_jsonl_registers_are_parseable() -> None:
    for relative_path in (
        ".factory/pm/risk-register.jsonl",
        ".factory/pm/change-register.jsonl",
    ):
        path = REPO_ROOT / relative_path
        records = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        assert records


def test_generated_pm_html_links_resolve_to_rendered_pages() -> None:
    for relative_path in (
        ".factory/pm/generated/status-dashboard.html",
        ".factory/pm/generated/pm-details.html",
        ".factory/pm/generated/workitems.html",
        ".factory/pm/generated/requirements-lifecycle.html",
    ):
        html_path = REPO_ROOT / relative_path
        html = html_path.read_text(encoding="utf-8")
        hrefs = re.findall(r'href="([^"]+)"', html)
        assert hrefs
        for href in hrefs:
            target, _, fragment = href.partition("#")
            if not target:
                if fragment:
                    assert f'id="{fragment}"' in html, href
                continue
            assert not target.endswith((".md", ".jsonl"))
            target_path = (html_path.parent / target).resolve()
            assert target_path.exists(), href
            if fragment:
                target_html = target_path.read_text(encoding="utf-8")
                assert f'id="{fragment}"' in target_html, href
