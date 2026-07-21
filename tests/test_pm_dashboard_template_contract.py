from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL = REPO_ROOT / "skills/using-shanforge/SKILL.md"
RENDERING = REPO_ROOT / "skills/using-shanforge/references/pm-dashboard-rendering.md"
TEMPLATE = REPO_ROOT / "skills/using-shanforge/references/status-dashboard-template.html"

MODULES = (
    ("module-team", "项目成员", "TEAM"),
    ("module-charter", "项目策划", "CHARTER"),
    ("module-wbs", "WBS", "WBS"),
    ("module-schedule", "进度计划", "SCHEDULE"),
    ("module-risks", "风险管理", "RISKS"),
    ("module-communications", "沟通计划", "COMMUNICATIONS"),
    ("module-meetings", "会议与行动", "MEETINGS"),
    ("module-status-reports", "状态报告", "STATUS_REPORTS"),
    ("module-changes", "变更管理", "CHANGES"),
    ("module-closure", "项目总结", "CLOSURE"),
)
MODULE_SUFFIXES = (
    "COUNT",
    "MISSING_COUNT",
    "CONFLICT_COUNT",
    "AS_OF_TIME",
    "SOURCE_DIGEST_SHORT",
    "EMPTY_REASON",
    "ROWS",
    "SOURCE_DETAILS",
)
OVERVIEW_SLOTS = {
    "PROJECT_NAME",
    "PROJECT_ID",
    "STAGE_NAME",
    "AS_OF_H",
    "AS_OF_TIME",
    "PROJECT_TIMEZONE",
    "VALIDATION_STATUS",
    "VALIDATION_MESSAGE",
    "SNAPSHOT_ID",
    "SNAPSHOT_SHA256_SHORT",
    "SOURCE_ROOT_SHA256_SHORT",
    "AUTHORIZATION_DIGEST_SHORT",
    "RULE_VERSION",
    "RENDER_DISPOSITION",
    "TOTAL_TASKS",
    "COMPLETED_TASKS",
    "COMPLETION_RATE",
    "ACTIVE_TASKS",
    "PENDING_APPROVALS",
    "BLOCKED_OR_OVERDUE_TASKS",
    "DEPLOYED_DELIVERABLES",
    "STATUS_DISTRIBUTION_SEGMENTS",
    "STATUS_DISTRIBUTION_LEGEND",
    "ACTIVE_SUMMARY",
    "APPROVAL_SUMMARY",
    "RECENT_COMPLETION_SUMMARY",
    "DEPLOYMENT_SUMMARY",
    "BLOCKED_OVERDUE_SUMMARY",
    "NEXT_MILESTONE_SUMMARY",
    "ERROR_CODE",
    "AFFECTED_PATHS",
    "RECOVERY_ACTION",
    "REDACTION_NOTICE",
    "OVERVIEW_DETAIL_ROWS",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_using_shanforge_routes_status_to_one_registered_query() -> None:
    content = read(SKILL)

    assert "IntentCandidate" in content
    assert "一次已注册项目状态查询" in content
    assert "不得由 AI 临时遍历" in content
    assert "AI 专业检查" in content


def test_rendering_contract_distinguishes_all_fact_source_classes() -> None:
    content = read(RENDERING)

    for phrase in (
        "`.factory/pm/` 不是全部事实源",
        "SRC-PROJECT-MASTER-001",
        "SRC-FORMAL-DOC-MAP-001",
        "SRC-WORKITEM-LEDGER-001",
        "SRC-PM-EVENT-001",
        "SRC-TASK-EVIDENCE-001",
        "SRC-DEPLOYMENT-EVENT-001",
        "生成页不是事实源",
    ):
        assert phrase in content


def test_excel_example_is_design_time_only_and_never_a_runtime_input() -> None:
    skill = read(SKILL)
    rendering = read(RENDERING)
    template = read(TEMPLATE)

    for phrase in (
        "Excel 样例只在模板设计时读取一次",
        "运行时不得再次读取 `.xls` / `.xlsx`",
    ):
        assert phrase in skill
    for phrase in (
        "Excel 样例的一次性角色",
        "标准项目状态查询不得打开、解析或依赖原始 `.xls` / `.xlsx` 文件",
        "Excel 样例不是事实源、运行时输入、模板数据库或每次查询的前置步骤",
        "不再次读取事实或 Excel 样例",
    ):
        assert phrase in rendering
    assert "对应 Excel" not in template


def test_rendering_contract_defines_the_fixed_h_query_chain() -> None:
    content = read(RENDERING)
    flow = content.split("## 会话中的固定九步流程", 1)[1].split(
        "## AI 与代码边界", 1
    )[0]

    positions = [
        flow.index(phrase)
        for phrase in (
            "IntentCandidate",
            "ToolCallPlan/v1",
            "不可变高水位 `H`",
            "ProjectProgressSnapshot/v2",
            "AuthorizedProgressSnapshot/v1",
            "RenderManifest/v2",
            "ReconciliationResult/v2",
            "AIInspectionResult/v1",
            "SessionResponseAssembly/v1",
        )
    ]
    assert positions == sorted(positions)
    assert "标准总览最多一次主工具调用" in flow


def test_rendering_contract_keeps_ai_out_of_fact_computation() -> None:
    content = read(RENDERING)

    for phrase in (
        "AI 不计算完成率",
        "AI 不计算状态",
        "AI 不拼装 HTML",
        "AI 不覆盖代码事实",
        "事实看板",
        "AI 专业检查",
    ):
        assert phrase in content
    assert "注册工具由确定性策略系统选择和授权" in content
    assert "AI 只识别意图、选择注册工具" not in content


def test_template_has_the_exact_registered_slot_set() -> None:
    content = read(TEMPLATE)
    actual = set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", content))
    module_slots = {
        f"{prefix}_{suffix}"
        for _, _, prefix in MODULES
        for suffix in MODULE_SUFFIXES
    }

    assert actual == OVERVIEW_SLOTS | module_slots


def test_template_has_one_overview_and_ten_modules_in_excel_order() -> None:
    content = read(TEMPLATE)
    ids = re.findall(r'<(?:main|section)[^>]+id="([^"]+)"', content)
    expected = ["page-overview", *(module_id for module_id, _, _ in MODULES)]

    assert [value for value in ids if value in expected] == expected
    assert all(content.count(f'id="{value}"') == 1 for value in expected)
    assert all(label in content for _, label, _ in MODULES)


def test_template_defines_full_partial_and_error_only_without_old_values() -> None:
    rendering = read(RENDERING)
    template = read(TEMPLATE)

    for value in ("FULL", "PARTIAL", "ERROR_ONLY"):
        assert value in rendering
    assert "conflict|stale|failed" in rendering
    assert "ERROR_ONLY" in template
    assert 'data-render-disposition="{{RENDER_DISPOSITION}}"' in template
    assert ".business-content" in template
    assert "ERROR_CODE" in template
    assert "RECOVERY_ACTION" in template


def test_template_is_accessible_responsive_and_network_independent() -> None:
    content = read(TEMPLATE)

    for phrase in (
        'class="skip-link"',
        'aria-label="项目管理模块"',
        ":focus-visible",
        "data-focus-ring",
        "prefers-reduced-motion",
        "@media(max-width:768px)",
        "@media(max-width:390px)",
        'id="overview-first-screen"',
        "overflow-wrap:anywhere",
    ):
        assert phrase in content
    for forbidden in (
        "http://",
        "https://",
        "fetch(",
        "XMLHttpRequest",
        "WebSocket",
        "localStorage",
        "sessionStorage",
        ".factory/pm/",
        ".factory/workitems/",
    ):
        assert forbidden not in content


def test_template_script_is_limited_to_read_only_dom_interactions() -> None:
    content = read(TEMPLATE)

    for phrase in (
        "data-module-filter",
        "data-module-sort",
        "data-sort-value",
        "data-source-details",
        "aria-sort",
    ):
        assert phrase in content
    for forbidden in (
        "completionRate",
        "riskLevel",
        "authorizationDigest =",
        "document.cookie",
        "indexedDB",
        "navigator.sendBeacon",
    ):
        assert forbidden not in content
