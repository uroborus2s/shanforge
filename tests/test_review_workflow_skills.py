from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_requesting_code_review_skill_is_shanforge_localized() -> None:
    skill = read("skills/requesting-code-review/SKILL.md")

    assert "name: requesting-code-review" in skill
    assert "任务级 review" in skill
    assert "PR review" in skill
    assert ".factory/workitems/<WORKITEM-ID>/reviews/" in skill
    assert ".factory/workitems/<WORKITEM-ID>/ledger.jsonl" in skill
    assert ".factory/memory/review-ledger.jsonl" in skill
    assert "Spec Review" in skill
    assert "Quality Review" in skill
    assert "Critical" in skill
    assert "Important" in skill
    assert "pending_human_confirmation" in skill
    assert "不能把 reviewer approved 当成人工确认" in skill
    assert "同线程作者自检的 review 输出状态只能是 `self_check_passed`" in skill
    assert "同线程作者自检后的下一 gate 状态必须是 `needs_independent_review`" in skill
    assert "禁止把 `needs_independent_review` 写成 review 通过结论" in skill
    assert "工作结果：" in skill
    assert "- work_item: <WORKITEM-ID>" in skill
    assert "- skill: requesting-code-review" in skill
    assert (
        "- status: approved | changes_requested | self_check_passed | blocked | needs_user_input"
        in skill
    )
    assert "- ledger_event: <review ledger event id or none>" in skill
    assert "`blocked` 用于缺 task brief" in skill
    assert "`needs_user_input` 用于 review 类型" in skill
    assert "与其他 skill 的关系" not in skill
    assert "subagent-driven-development" not in skill
    assert "executing-plans" not in skill
    assert "verification-before-completion" not in skill
    assert "gitcommitzh" not in skill
    assert "requesting-code-review/code-reviewer.md" not in skill
    assert "docs/superpowers" not in skill


def test_requesting_code_review_references_define_review_packages() -> None:
    expected = {
        "skills/requesting-code-review/references/task-review-template.md": (
            "Task Review",
            "task brief",
            "implementer report",
            "verification evidence",
            "Spec Review",
            "Quality Review",
            "approved",
            "changes_requested",
        ),
        "skills/requesting-code-review/references/pr-review-template.md": (
            "PR Review",
            "Base",
            "Head",
            "diff package",
            "Ready to merge",
            "Critical",
            "Important",
            "Minor",
        ),
        "skills/requesting-code-review/references/independent-review-task-template.md": (
            "Independent Review Task",
            "不要读取实现者会话历史",
            "重新读取输入包",
            "review score",
            "pending_human_confirmation",
        ),
        "skills/requesting-code-review/references/review-score-rubric.md": (
            "需求符合度",
            "架构一致性",
            "测试充分性",
            "代码质量",
            "文档与记忆同步",
            "100",
        ),
    }

    for path, phrases in expected.items():
        content = read(path)
        for phrase in phrases:
            assert phrase in content


def test_review_gate_rejects_self_approval_and_requires_reviewer_na_decision() -> None:
    skill = read("skills/requesting-code-review/SKILL.md")

    for phrase in (
        "作者自检不能 `approved`",
        "N/A 必须由 reviewer 明确接受或拒绝",
        "未被 reviewer 接受的 N/A 不得通过 review",
    ):
        assert phrase in skill


def test_receiving_code_review_skill_requires_verification_before_changes() -> None:
    skill = read("skills/receiving-code-review/SKILL.md")

    assert "name: receiving-code-review" in skill
    assert "先核实反馈再修改" in skill
    assert "禁止表演式同意" in skill
    assert "禁止盲改" in skill
    assert "不清楚就先问" in skill
    assert "一次处理一个反馈项" in skill
    assert "Critical" in skill
    assert "Important" in skill
    assert "Minor" in skill
    assert ".factory/workitems/<WORKITEM-ID>/reviews/" in skill
    assert ".factory/workitems/<WORKITEM-ID>/reports/" in skill
    assert ".factory/memory/review-ledger.jsonl" in skill
    assert ".factory/memory/tasks.summary.md" in skill
    assert "memory sync" in skill
    assert "receiving-code-review" in skill
    assert "工作结果：" in skill
    assert "- work_item: <WORKITEM-ID>" in skill
    assert "- skill: receiving-code-review" in skill
    assert "- status: ready_for_review | blocked | needs_user_input" in skill
    assert "- ledger_event: <work item ledger event id or none>" in skill
    assert "`blocked` 用于 feedback 来源缺失" in skill
    assert "`needs_user_input` 用于 feedback 不清楚" in skill
    assert "requesting-code-review" not in skill
    assert "You're absolutely right" not in skill
    assert "Great point" not in skill


def test_receiving_code_review_references_define_triage_and_response() -> None:
    expected = {
        "skills/receiving-code-review/references/feedback-triage-template.md": (
            "Review Feedback Triage",
            "反馈来源",
            "是否清楚",
            "是否技术正确",
            "是否与用户决策冲突",
            "处理决定",
        ),
        "skills/receiving-code-review/references/review-response-template.md": (
            "Review Response",
            "Fixed",
            "Verified",
            "Pushback",
            "Needs clarification",
            "验证命令",
        ),
    }

    for path, phrases in expected.items():
        content = read(path)
        for phrase in phrases:
            assert phrase in content


def test_review_workflow_openai_metadata_is_chinese() -> None:
    requesting_metadata = read("skills/requesting-code-review/agents/openai.yaml")
    receiving_metadata = read("skills/receiving-code-review/agents/openai.yaml")

    assert 'display_name: "请求代码评审"' in requesting_metadata
    assert "task review" in requesting_metadata
    assert "PR review" in requesting_metadata
    assert "仅真实独立 review 输出 review_score" in requesting_metadata
    assert "同线程只输出 author_self_check_score" in requesting_metadata

    assert 'display_name: "处理代码评审反馈"' in receiving_metadata
    assert "review feedback" in receiving_metadata
    assert "先核实" in receiving_metadata
