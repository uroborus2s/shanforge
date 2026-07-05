from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_existing_skills_have_migrated_reference_templates() -> None:
    expected = {
        "skills/requirements-engineering/references/prd-template.md": (
            "REQ-XXX",
            "AC-1",
            "NFR-XXX",
            ".factory/workitems/<WORKITEM-ID>/brief.md",
            ".factory/memory/prd.summary.md",
        ),
        "skills/document-templates/references/technical-design-template.md": (
            "分层和接口边界",
            "影响文件",
            "测试策略",
            ".factory/memory/",
            "不得引入新的中心脚本主控",
        ),
        "skills/tdd-workflow/references/root-cause-checklist.md": (
            "Bug 症状",
            "复现步骤",
            "直接原因",
            "根源原因",
            "禁止用未验证兜底替代根因修复",
        ),
        "skills/tdd-workflow/references/evidence-report-template.md": (
            "Red",
            "Green",
            "验证命令",
            "真实结果",
            "偏离",
        ),
        "skills/gitcommitzh/references/commit-message-rubric.md": (
            "提交范围",
            "变更概览",
            "风险与影响",
            "验证情况",
            "禁止把无关改动混入同一提交",
        ),
    }

    for path, phrases in expected.items():
        content = read(path)
        for phrase in phrases:
            assert phrase in content


def test_workflow_template_migration_progress_is_tracked() -> None:
    plan = read(
        "docs/04-project-development/05-development-process/superpowers-workflow-integration-plan.md"
    )
    tasks = read(".factory/memory/tasks.summary.md")

    for phrase in (
        "writing-plans",
        "requesting-code-review",
        "verification-before-completion",
        "systematic-debugging",
    ):
        assert phrase in plan

    assert "`SF-SP-008` 已提交为 `e048784`" in tasks
    assert "`SF-SP-009` 已提交为 `9296f58`" in tasks
    assert "`SF-SP-010` 已提交为 `3b0e9a5`" in tasks
    assert "`SF-SP-001/002/003/004/005/006/007` 已人工确认" in tasks
    assert "当前不新增 `SF-SP-011`" in tasks
    assert (
        "详细报告见 `.factory/workitems/SF-SP-010/reports/"
        "superpowers-workflow-integration-closeout-report.md`"
        in tasks
    )
    assert "review、完成验证、独立调试等后续 workflow skill 的 references 仍未完成" not in plan
    assert "剩余 workflow skill 的 references 仍待随对应 skill 创建迁移" not in tasks
    assert "整体流程集成当前只剩 `SF-SP-010` 文档、导航、memory 同步收口" not in tasks
    assert (
        "requesting-code-review / verification-before-completion / systematic-debugging"
        not in tasks
    )


def test_downstream_workflow_reference_paths_exist_and_helper_scope_is_tracked() -> None:
    plan = read(
        "docs/04-project-development/05-development-process/superpowers-workflow-integration-plan.md"
    )
    expected_paths = (
        "skills/project-memory/references/session-start-checklist.md",
        "skills/writing-plans/references/workitem-plan-template.md",
        "skills/writing-plans/references/task-brief-template.md",
        "skills/writing-plans/references/plan-review-template.md",
        "skills/requesting-code-review/references/task-review-template.md",
        "skills/requesting-code-review/references/pr-review-template.md",
        "skills/requesting-code-review/references/independent-review-task-template.md",
        "skills/receiving-code-review/references/feedback-triage-template.md",
        "skills/receiving-code-review/references/review-response-template.md",
        "skills/systematic-debugging/references/root-cause-investigation-template.md",
        "skills/verification-before-completion/references/completion-evidence-template.md",
        "skills/gitcommitzh/references/commit-message-rubric.md",
    )

    for path in expected_paths:
        assert path in plan
        assert (REPO_ROOT / path).is_file()

    assert "SF-SP-003 helper code 迁移结论" in plan
    assert "没有新增必须迁出的全局 helper code" in plan
    assert "skills/systematic-debugging/references/root-cause-checklist.md" not in plan
    assert (
        "skills/verification-before-completion/references/evidence-report-template.md"
        not in plan
    )


def test_superpowers_plan_defines_memory_layers_and_human_confirmation_gate() -> None:
    plan = read(
        "docs/04-project-development/05-development-process/superpowers-workflow-integration-plan.md"
    )

    for phrase in (
        "### 4.1 记忆分层",
        "`using-shanforge` 是唯一的流程路由 owner",
        "工作 skill 的边界固定为",
        "不写“与其他 skill 的关系”",
        "不决定下一步 skill",
        "入口压缩层",
        "主题摘要层",
        "Work item 执行层",
        "Ledger 审计层",
        "正式文档层",
        "### 7.8 Loop 结束人工确认门",
        "pending_human_confirmation",
        "human_approved | human_changes_requested",
        "本轮执行完成，等待人工确认",
        "把 reviewer 的 `approved` 当成人工 `human_approved`",
        "human_confirmation_status: pending | human_approved | human_changes_requested",
        "approved` 和 `human_approved` 是两个不同状态",
    ):
        assert phrase in plan
