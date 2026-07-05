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

    assert "当前不新增 `SF-SP-011`" in plan
    assert "本地闭环完成 `3 / 10`" in plan
    assert "`SF-SP-010` | 本地闭环完成" in plan
    assert "对 `SF-SP-001` 到 `SF-SP-007` 已通过的产物做范围隔离提交" in plan


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
        "本地闭环完成 | 3 | `SF-SP-008`、`SF-SP-009`、`SF-SP-010`",
        "独立评审通过，待人工确认 | 0 | 无",
        (
            "已人工确认，提交未闭环 | 7 | `SF-SP-001`、`SF-SP-002`、"
            "`SF-SP-003`、`SF-SP-004`、`SF-SP-005`、`SF-SP-006`、`SF-SP-007`"
        ),
        "未补开发或真实独立 review | 0 | 无",
        "`SF-SP-010` | 本地闭环完成 | 本地提交 `3b0e9a5`",
        "10 个任务的开发、真实独立 review 和人工确认缺口已经补齐",
    ):
        assert phrase in report
