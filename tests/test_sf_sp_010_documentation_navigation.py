from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_development_navigation_exposes_process_docs_and_test_report() -> None:
    docs_index = read("docs/index.md")
    process_index = read("docs/04-project-development/05-development-process/index.md")

    nav_paths = (
        "04-project-development/05-development-process/superpowers-workflow-integration-plan.md",
        "04-project-development/05-development-process/project-management-control-plane.md",
        "04-project-development/05-development-process/memory-governance-implementation-plan.md",
        "04-project-development/06-testing-verification/test-report.md",
    )

    for path in nav_paths:
        assert path in docs_index
        assert (REPO_ROOT / "docs" / path).is_file()

    process_links = (
        (
            "[Superpowers 流程集成实施方案](./superpowers-workflow-integration-plan.md)",
            "superpowers-workflow-integration-plan.md",
        ),
        (
            "[项目管理控制面集成方案](./project-management-control-plane.md)",
            "project-management-control-plane.md",
        ),
        (
            "[记忆治理专项实施计划](./memory-governance-implementation-plan.md)",
            "memory-governance-implementation-plan.md",
        ),
        (
            "[测试报告](../06-testing-verification/test-report.md)",
            "../06-testing-verification/test-report.md",
        ),
    )

    process_dir = REPO_ROOT / "docs/04-project-development/05-development-process"
    for link, target in process_links:
        assert link in process_index
        assert (process_dir / target).resolve().is_file()


def test_superpowers_plan_next_steps_are_current() -> None:
    plan = read(
        "docs/04-project-development/05-development-process/superpowers-workflow-integration-plan.md"
    )

    for stale in (
        "review、完成验证、独立调试等后续 workflow skill 的 references 仍未完成",
        "推荐先执行：",
        "这三项完成后，再拷贝改造 Superpowers 的计划、执行、评审和验证类 skill",
        "当前只剩 `SF-SP-010` 文档、导航、memory 同步收口",
        "目标文档必须一并纳入同一可审阅提交范围",
    ):
        assert stale not in plan

    for stale in (
        "本地闭环完成 `3 / 10`",
        "已人工确认但提交未闭环 `7 / 10`",
        "不能声明整个 Superpowers 流程集成计划已完成",
        "对 `SF-SP-001` 到 `SF-SP-007` 已通过的产物做范围隔离提交",
    ):
        assert stale not in plan

    assert "当前不新增 `SF-SP-011`" in plan
    assert "本地闭环完成 `10 / 10`" in plan
    assert "`SF-SP-001` | 本地闭环完成" in plan
    assert "`SF-SP-010` | 本地闭环完成" in plan
    assert "`efac627`" in plan


def test_doc_map_tracks_navigation_plan_and_test_report_sources() -> None:
    doc_map = read(".factory/memory/doc-map.md")

    mappings = (
        (
            "docs/index.md",
            ".factory/memory/runtime-brief.md",
        ),
        (
            "docs/04-project-development/05-development-process/index.md",
            ".factory/memory/runtime-brief.md",
        ),
        (
            "docs/04-project-development/05-development-process/superpowers-workflow-integration-plan.md",
            ".factory/memory/tasks.summary.md",
            ".factory/memory/skill-updates.summary.md",
            ".factory/memory/runtime-brief.md",
        ),
        (
            "docs/04-project-development/05-development-process/project-management-control-plane.md",
            ".factory/memory/tasks.summary.md",
            ".factory/memory/current-state.md",
        ),
        (
            "docs/04-project-development/05-development-process/memory-governance-implementation-plan.md",
            ".factory/memory/tasks.summary.md",
            ".factory/memory/runtime-brief.md",
        ),
        (
            "docs/04-project-development/06-testing-verification/test-report.md",
            ".factory/memory/tests.summary.md",
        ),
    )

    for source, *targets in mappings:
        mapping = f"`{source}` -> {', '.join(f'`{target}`' for target in targets)}"
        assert mapping in doc_map


def test_sf_sp_010_closeout_replaces_stale_progress_language() -> None:
    plan = read(
        "docs/04-project-development/05-development-process/superpowers-workflow-integration-plan.md"
    )
    tasks = read(".factory/memory/tasks.summary.md")
    current_state = read(".factory/memory/current-state.md")

    for content in (tasks, current_state):
        assert "`SF-SP-009` 已提交为 `9296f58`" in content
        assert "`SF-SP-010`" in content
        assert "3b0e9a5" in content

    assert "本地提交 `9296f58`" in plan
    assert "本地提交 `3b0e9a5`" in plan

    assert "整体流程集成仍需 `SF-SP-009` 和 `SF-SP-010` 收口" not in tasks
    assert "`SF-SP-009`：当前已进入黑盒流程 eval 开发" not in plan
    assert "`SF-SP-010` 已进入文档、导航、memory 同步开发" not in plan


def test_superpowers_closeout_report_tracks_completed_and_open_items() -> None:
    report = read(
        ".factory/workitems/SF-SP-010/reports/"
        "superpowers-workflow-integration-closeout-report.md"
    )

    for phrase in (
        (
            "本地闭环完成 | 10 | `SF-SP-001`、`SF-SP-002`、`SF-SP-003`、"
            "`SF-SP-004`、`SF-SP-005`、`SF-SP-006`、`SF-SP-007`、"
            "`SF-SP-008`、`SF-SP-009`、`SF-SP-010`"
        ),
        "独立评审通过，待人工确认 | 0 | 无",
        "已人工确认，提交未闭环 | 0 | 无",
        "未补开发或真实独立 review | 0 | 无",
        "`SF-SP-001` | 本地闭环完成 | 本地提交 `efac627`",
        "`SF-SP-010` | 本地闭环完成 | 本地提交 `3b0e9a5`",
        "10 个任务的开发、真实独立 review、人工确认和本地提交闭环已经补齐",
    ):
        assert phrase in report


def test_active_runtime_entries_do_not_recommend_center_scripts() -> None:
    for path in (
        "AGENTS.md",
        ".factory/memory/runtime-brief.md",
        ".factory/memory/agent-session.md",
    ):
        content = read(path)
        assert "python3 scripts/factory-dispatch" not in content
        assert "factory-agent-session --help" not in content
        assert "命令执行统一走 `factory-dispatch`" not in content


def test_document_templates_register_formal_docs_and_keep_temporary_docs_out() -> None:
    skill = read("skills/document-templates/SKILL.md")
    structure = read("skills/document-templates/references/repository-structure.md")

    frontmatter = skill.split("---", 2)[1]
    assert "description: \"创建、审查、整理和升级软件项目正式文档体系。" in frontmatter
    assert "docs-stratego 的 4 大模块" in frontmatter
    assert "D3" not in frontmatter

    for phrase in (
        "新增正式文档必须在同一改动中同步 `docs/index.md` 或 `.factory/memory/doc-map.md`",
        "修改正式文档必须追加 `版本历史`",
        (
            "临时文档只能放在 `.factory/workitems/<WORKITEM-ID>/evidence/`、"
            "`reports/`、`reviews/` 或 `.factory/pm/generated/`"
        ),
        "工作结果：",
        "- work_item: <WORKITEM-ID>",
        "- skill: document-templates",
        "- status: ready_for_review | blocked | needs_user_input",
        "- ledger_event: <event id or none>",
        "`needs_user_input` 用于必须由用户决定的文档范围",
    ):
        assert phrase in skill

    for phrase in (
        "新增正式页面后，同步根 `docs/index.md`；需要 AI 恢复时同步 `.factory/memory/doc-map.md`",
        "临时过程材料不得放入 `docs/`",
    ):
        assert phrase in structure


def test_formal_document_template_has_chinese_version_metadata() -> None:
    template = read("skills/document-templates/references/formal-document-template.md")

    for phrase in (
        "## 版本信息",
        "| 文档编号 |  |",
        "| 文档类型 |  |",
        "| 当前版本 | `0.1.0` |",
        "| 当前状态 | 草稿 |",
        "| 最近更新 |  |",
        "## 版本历史",
        "| 版本 | 修改内容 | 日期 | 修改人 | 审核 | 批准 |",
    ):
        assert phrase in template


def test_baseline_design_templates_exist_and_have_required_sections() -> None:
    expected = {
        "skills/document-templates/references/project-baseline-template.md": (
            "项目级 Baseline 模板",
            "领域划分",
            "后端模块",
            "数据库基线",
            "API 基线",
            "前端 UI",
        ),
        "skills/document-templates/references/backend-module-design-template.md": (
            "后端模块设计模板",
            "微服务边界",
            "模块职责",
            "接口契约",
        ),
        "skills/document-templates/references/database-design-template.md": (
            "数据库设计模板",
            "ERD",
            "实体",
            "迁移策略",
        ),
        "skills/document-templates/references/api-design-template.md": (
            "API 设计模板",
            "openapi.yaml",
            "接口清单",
            "错误响应",
        ),
        "skills/document-templates/references/frontend-ui-design-template.md": (
            "前端 UI 设计模板",
            "信息架构",
            "页面清单",
            "组件",
            "可访问性",
        ),
    }

    required_metadata = (
        "## 版本信息",
        "| 文档编号 |  |",
        "| 文档类型 |  |",
        "| 当前版本 | `0.1.0` |",
        "## 版本历史",
        "| 版本 | 修改内容 | 日期 | 修改人 | 审核 | 批准 |",
    )

    for path, phrases in expected.items():
        template = read(path)
        for phrase in (*required_metadata, *phrases):
            assert phrase in template
