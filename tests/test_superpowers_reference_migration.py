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
    contract = read("docs/05-design/workflow-execution-design.md")
    tasks = read(".factory/memory/tasks.summary.md")

    for phrase in (
        "writing-plans",
        "executing-plans",
        "subagent-driven-development",
        "tdd-workflow",
    ):
        assert phrase in contract

    assert "DOC-FACTORY-RESTRUCTURE-001" in tasks
    assert "破坏性" in tasks
    assert not (
        REPO_ROOT / "docs/04-project-development/05-development-process/"
        "superpowers-workflow-integration-plan.md"
    ).exists()


def test_downstream_workflow_reference_paths_exist_and_helper_scope_is_tracked() -> None:
    contract = read("docs/05-design/workflow-execution-design.md")
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
        assert (REPO_ROOT / path).is_file()

    for phrase in (
        "任务分解",
        "开发",
        "测试",
        "review input package",
        "ledger event",
    ):
        assert phrase in contract


def test_superpowers_plan_defines_memory_layers_and_human_confirmation_gate() -> None:
    contract = read("docs/05-design/workflow-execution-design.md")

    for phrase in (
        "Review 不能替代 verification",
        "Verification 不能替代 human confirmation",
        "pending_human_confirmation",
        "作者只能推进到 `ready_for_review`",
        "不得自批 `approved`",
    ):
        assert phrase in contract
