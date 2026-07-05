from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_subagent_driven_development_skill_is_shanforge_localized() -> None:
    skill = read("skills/subagent-driven-development/SKILL.md")

    assert "name: subagent-driven-development" in skill
    assert "独立任务" in skill
    assert ".factory/workitems/<WORKITEM-ID>/plan.md" in skill
    assert ".factory/workitems/<WORKITEM-ID>/task-briefs/" in skill
    assert ".factory/workitems/<WORKITEM-ID>/ledger.jsonl" in skill
    assert "不要让子 agent 自己读完整 plan" in skill
    assert "本 skill 只准备评审输入" in skill
    assert "实现者只能进入 `ready_for_review`" in skill
    assert "DONE_WITH_CONCERNS" in skill
    assert "NEEDS_CONTEXT" in skill
    assert "BLOCKED" in skill
    assert "禁止并行派发多个实现子 agent" in skill
    assert "工作结果：" in skill
    assert "needs:" in skill
    assert "本 skill 不决定完成后交给谁" in skill
    assert "只写状态、产物、证据和 `needs`" in skill
    assert "docs/superpowers" not in skill
    assert "finishing-a-development-branch" not in skill
    assert "## 与其他 skill 的关系" not in skill
    assert "requesting-code-review" not in skill
    assert "verification-before-completion" not in skill
    assert "gitcommitzh" not in skill


def test_subagent_references_define_handoff_and_review_templates() -> None:
    expected = {
        "skills/subagent-driven-development/references/implementer-task-template.md": (
            "Implementer Task",
            "完整 task brief",
            "Work item",
            "DONE",
            "DONE_WITH_CONCERNS",
            "BLOCKED",
            "NEEDS_CONTEXT",
            "evidence",
            "implementer report",
        ),
        "skills/subagent-driven-development/references/spec-review-template.md": (
            "Spec Review",
            "不要相信实现报告",
            "读取实际 diff",
            "缺失需求",
            "额外工作",
            "file:line",
        ),
        "skills/subagent-driven-development/references/quality-review-template.md": (
            "Quality Review",
            "只在 Spec Review 通过后执行",
            "Critical",
            "Important",
            "Minor",
            "分层",
            "Assessment",
        ),
        "skills/subagent-driven-development/references/status-handling-checklist.md": (
            "DONE_WITH_CONCERNS",
            "NEEDS_CONTEXT",
            "BLOCKED",
            "review input package",
            "needs: review",
        ),
    }

    for path, phrases in expected.items():
        content = read(path)
        for phrase in phrases:
            assert phrase in content

    status_checklist = read(
        "skills/subagent-driven-development/references/status-handling-checklist.md"
    )
    assert "进入 Spec Review" not in status_checklist
    assert "Review 状态回流" not in status_checklist
    assert "收到 Spec Review" not in status_checklist
    assert "收到 Quality Review" not in status_checklist
    assert "收到 reviewer `approved`" not in status_checklist


def test_execution_workflow_docs_do_not_keep_stale_review_state() -> None:
    plan = read(
        "docs/04-project-development/05-development-process/"
        "superpowers-workflow-integration-plan.md"
    )
    codex_tools = read("skills/using-shanforge/references/codex-tools.md")

    assert "| `SF-SP-005` | 功能评审通过，提交未闭环 |" in plan
    assert "iteration-3 独立复审 `approved / 92`" in plan
    assert not re.search(
        r"`SF-SP-005`.*human_approved.*可以进入 `SF-SP-006`",
        plan,
    )
    assert "finishing-a-development-branch" not in plan
    assert "finishing-a-development-branch" not in codex_tools
    assert "gitcommitzh" in codex_tools


def test_executing_plans_skill_is_inline_fallback() -> None:
    skill = read("skills/executing-plans/SKILL.md")

    assert "name: executing-plans" in skill
    assert "written implementation plan" in skill
    assert ".factory/workitems/<WORKITEM-ID>/plan.md" in skill
    assert ".factory/workitems/<WORKITEM-ID>/ledger.jsonl" in skill
    assert "先批判性 review plan" in skill
    assert "逐步执行" in skill
    assert "每个任务后写 evidence" in skill
    assert "review checkpoint" in skill
    assert "工作结果：" in skill
    assert "needs:" in skill
    assert "本 skill 不决定完成后交给谁" in skill
    assert "只写状态、产物、证据和 `needs`" in skill
    assert "STOP" in skill
    assert "BLOCKED" in skill
    assert "禁止猜测" in skill
    assert "docs/superpowers" not in skill
    assert "finishing-a-development-branch" not in skill
    assert "## 与其他 skill 的关系" not in skill
    assert "requesting-code-review" not in skill
    assert "verification-before-completion" not in skill
    assert "receiving-code-review" not in skill
    assert "gitcommitzh" not in skill


def test_using_shanforge_is_flow_controller_and_owns_skill_routing() -> None:
    skill = read("skills/using-shanforge/SKILL.md")
    metadata = read("skills/using-shanforge/agents/openai.yaml")

    for phrase in (
        "流程总控 / CTO",
        "选择唯一下一步 skill",
        "工作 skill 不决定前置、后置或下一步 skill",
        "路由表",
        "pending_human_confirmation",
        "工作 skill 状态回写协议",
        "工作 skill 完成时只返回状态包，不写下一步 skill",
        "人工确认门",
    ):
        assert phrase in skill

    for phrase in (
        "作为 Shanforge 流程总控判断当前环节",
        "选择唯一下一步 skill",
        "工作 skill 只产出状态、证据和 needs",
    ):
        assert phrase in metadata


def test_execution_workflow_openai_metadata_is_chinese() -> None:
    subagent_metadata = read("skills/subagent-driven-development/agents/openai.yaml")
    executing_metadata = read("skills/executing-plans/agents/openai.yaml")

    assert 'display_name: "子代理驱动开发"' in subagent_metadata
    assert "work item plan" in subagent_metadata
    assert "状态回写" in subagent_metadata
    assert "不决定下一步 skill" in subagent_metadata

    assert 'display_name: "执行实施计划"' in executing_metadata
    assert "written implementation plan" in executing_metadata
    assert "状态回写" in executing_metadata
    assert "不决定下一步 skill" in executing_metadata
