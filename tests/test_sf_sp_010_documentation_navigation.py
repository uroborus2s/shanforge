from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_development_navigation_exposes_process_docs_and_test_report() -> None:
    docs_index = read("docs/index.md")
    design_index = read("docs/05-design/index.md")
    delivery_index = read("docs/06-delivery/index.md")

    nav_paths = (
        "05-design/workflow-execution-design.md",
        "06-delivery/test-plan.md",
    )

    for path in nav_paths:
        assert (REPO_ROOT / "docs" / path).is_file()

    assert "05-design/index.md" in docs_index
    assert "06-delivery/index.md" in docs_index

    navigation_links = (
        (
            design_index,
            "[workflow-execution-design.md](./workflow-execution-design.md)",
            REPO_ROOT / "docs/05-design/workflow-execution-design.md",
        ),
        (
            delivery_index,
            "[测试策略与质量门](./test-plan.md)",
            REPO_ROOT / "docs/06-delivery/test-plan.md",
        ),
    )

    for index, link, target in navigation_links:
        assert link in index
        assert target.is_file()


def test_old_process_docs_are_removed_from_current_baseline() -> None:
    removed = (
        "superpowers-workflow-integration-plan.md",
        "project-management-control-plane.md",
        "memory-governance-implementation-plan.md",
        "software-development-process.md",
        "process-workflow-contract-implementation-plan.md",
    )
    docs_index = read("docs/index.md")
    design_index = read("docs/05-design/index.md")
    contract = read("docs/05-design/workflow-execution-design.md")

    for filename in removed:
        assert filename not in docs_index
        assert filename not in design_index
        assert not (
            REPO_ROOT / "docs/04-project-development/05-development-process" / filename
        ).exists()

    assert not (REPO_ROOT / "docs/04-project-development").exists()

    for phrase in ("任务分解", "系统总设计", "模块设计", "UI 设计", "开发", "测试"):
        assert phrase in contract


def test_doc_map_tracks_navigation_plan_and_test_report_sources() -> None:
    doc_map = read(".factory/memory/doc-map.md")

    mappings = (
        (
            "docs/index.md",
            ".factory/memory/runtime-brief.md",
        ),
        (
            "docs/05-design/index.md",
            ".factory/memory/runtime-brief.md",
        ),
        (
            "docs/05-design/workflow-execution-design.md",
            ".factory/memory/tasks.summary.md",
            ".factory/memory/runtime-brief.md",
        ),
        (
            "docs/06-delivery/test-plan.md",
            ".factory/memory/tests.summary.md",
        ),
    )

    for source, *targets in mappings:
        matching_lines = [line for line in doc_map.splitlines() if source in line]
        assert matching_lines, source
        assert any(all(target in line for target in targets) for line in matching_lines)


def test_doc_factory_restructure_summary_tracks_destructive_migration() -> None:
    tasks = read(".factory/memory/tasks.summary.md")

    assert "DOC-FACTORY-RESTRUCTURE-001" in tasks
    assert "破坏性" in tasks
    assert "task-execution-contract.md" in tasks


def test_superpowers_closeout_report_tracks_completed_and_open_items() -> None:
    report = read(
        ".factory/workitems/SF-SP-010/reports/superpowers-workflow-integration-closeout-report.md"
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
    catalog = read("skills/document-templates/references/document-catalog.md")
    gates = read("skills/document-templates/references/traceability-and-gates.md")

    frontmatter = skill.split("---", 2)[1]
    assert 'description: "创建、审查、整理和升级软件项目正式文档体系。' in frontmatter
    assert "docs-stratego 的 4 大模块" in frontmatter
    assert "D3" not in frontmatter

    for phrase in (
        "新增正式文档必须在同一改动中同步 `docs/index.md` 或 `.factory/memory/doc-map.md`",
        "修改正式文档必须追加 `版本历史`",
        (
            "临时文档只能放在 `.factory/workitems/<WORKITEM-ID>/drafts/`、"
            "`evidence/`、`reports/` 或 `reviews/`"
        ),
        "只读 HTML 由项目快照 CLI 写入 `.factory/cache/site/current/`",
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
        "模板资产与输出路径",
    ):
        assert phrase in structure

    assert "默认最小文档包" not in skill
    assert "模板资产与输出路径" not in skill
    assert "文档重构 / 升级流程" not in skill
    assert "最小文档包建议" in catalog
    assert "文档重构 / 升级流程" in gates


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
