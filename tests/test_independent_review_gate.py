from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def read_jsonl(path: str) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in (REPO_ROOT / path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_requesting_code_review_forbids_same_thread_approved() -> None:
    skill = read("skills/requesting-code-review/SKILL.md")

    assert "同线程作者自检只能输出 `self_check_passed`" in skill
    assert "禁止把同线程复核写成 `approved`" in skill
    assert (
        "没有真实独立 reviewer 证据时，下一 gate 状态必须是 "
        "`needs_independent_review`"
    ) in skill
    assert "需要子 agent 但用户未授权时，必须停止并请求授权" in skill
    assert (
        "approved` 必须带 `reviewer_type`、`reviewer_id` "
        "和 `reviewer_independence_evidence`"
    ) in skill
    assert "单线程 fallback" not in skill


def test_review_rubric_requires_independence_metadata_for_score() -> None:
    rubric = read("skills/requesting-code-review/references/review-score-rubric.md")
    task_template = read("skills/requesting-code-review/references/task-review-template.md")
    independent_template = read(
        "skills/requesting-code-review/references/independent-review-task-template.md"
    )

    for content in (rubric, task_template, independent_template):
        assert "reviewer_type" in content
        assert "reviewer_id" in content
        assert "reviewer_independence_evidence" in content
        assert "author_self_check_score" in content
        assert "review_score" in content
        assert "same_thread" in content
        assert "needs_independent_review" in content

    assert "same_thread` 只能写 `self_check_passed`" in rubric
    assert "没有 reviewer 独立性证据时，不得写 `review_score`" in rubric
    assert "没有 reviewer 独立性证据时，不得写 `approved`" in rubric


def test_workflow_plan_makes_independent_review_a_hard_gate() -> None:
    plan = read(
        "docs/04-project-development/05-development-process/superpowers-workflow-integration-plan.md"
    )

    assert "same_thread 只能产生 `self_check_passed`" in plan
    assert "approved 必须来自真实独立 reviewer" in plan
    assert "reviewer_type / reviewer_id / reviewer_independence_evidence" in plan
    assert "未获授权创建子 agent 时，必须停在 `needs_independent_review`" in plan
    assert "没有独立评审证据，不得进入 `pending_human_confirmation`" in plan


def test_current_sf_sp_007_latest_review_status_requires_independent_review() -> None:
    events = read_jsonl(".factory/workitems/SF-SP-007/ledger.jsonl")
    review_events = [
        event
        for event in events
        if event.get("action")
        in {"loop_iteration_completed", "review_independence_correction"}
    ]

    latest = review_events[-1]

    assert latest["action"] == "review_independence_correction"
    assert latest["status"] == "needs_independent_review"
    assert "review_score=96" in latest["invalidated_fields"]
    assert "pending_human_confirmation" in latest["invalidated_fields"]


def test_review_ledger_corrections_override_same_thread_approvals() -> None:
    events = read_jsonl(".factory/memory/review-ledger.jsonl")

    correction_by_workitem: dict[str, dict[str, object]] = {}
    independent_review_by_workitem: dict[str, dict[str, object]] = {}
    independent_rereview_by_workitem: dict[str, dict[str, object]] = {}
    review_fix_by_workitem: dict[str, dict[str, object]] = {}
    human_confirmation_by_workitem: dict[str, dict[str, object]] = {}
    latest_by_workitem: dict[str, dict[str, object]] = {}
    for event in events:
        workitem = event.get("workitem")
        if isinstance(workitem, str):
            if event.get("action") == "review_independence_correction":
                correction_by_workitem[workitem] = event
            if event.get("action") == "independent_review":
                independent_review_by_workitem[workitem] = event
            if event.get("action") == "independent_re_review":
                independent_rereview_by_workitem[workitem] = event
            if event.get("action") == "review_feedback_fixed":
                review_fix_by_workitem[workitem] = event
            if event.get("action") == "human_confirmation":
                human_confirmation_by_workitem[workitem] = event
            latest_by_workitem[workitem] = event

    assert correction_by_workitem["SF-SP-007"]["status"] == "needs_independent_review"
    assert correction_by_workitem["SF-SP-007"]["score"] is None
    assert "same-thread author self-check" in correction_by_workitem["SF-SP-007"]["reason"]

    assert independent_review_by_workitem["SF-SP-007"]["status"] == "approved"
    assert independent_review_by_workitem["SF-SP-007"]["score"] == 95
    assert independent_review_by_workitem["SF-SP-007"]["actor"] == "independent_subagent"
    assert "reviewer_agent_id" in independent_review_by_workitem["SF-SP-007"]

    assert independent_review_by_workitem["SF-SP-005"]["status"] == "changes_requested"
    assert independent_review_by_workitem["SF-SP-005"]["score"] == 78
    assert independent_review_by_workitem["SF-SP-006"]["status"] == "changes_requested"
    assert independent_review_by_workitem["SF-SP-006"]["score"] == 84

    assert review_fix_by_workitem["SF-SP-005"]["status"] == "ready_for_review"
    assert review_fix_by_workitem["SF-SP-005"]["next_status"] == "independent_re_review"
    assert review_fix_by_workitem["SF-SP-006"]["status"] == "ready_for_review"
    assert review_fix_by_workitem["SF-SP-006"]["next_status"] == "independent_re_review"

    assert independent_rereview_by_workitem["SF-SP-005"]["status"] == "approved"
    assert independent_rereview_by_workitem["SF-SP-005"]["score"] == 92
    assert (
        independent_rereview_by_workitem["SF-SP-005"]["next_status"]
        == "pending_human_confirmation"
    )
    assert independent_rereview_by_workitem["SF-SP-006"]["status"] == "approved"
    assert independent_rereview_by_workitem["SF-SP-006"]["score"] == 95
    assert (
        independent_rereview_by_workitem["SF-SP-006"]["next_status"]
        == "pending_human_confirmation"
    )

    for workitem in ("SF-SP-005", "SF-SP-006", "SF-SP-007"):
        assert human_confirmation_by_workitem[workitem]["status"] == "human_approved"
        assert human_confirmation_by_workitem[workitem]["next_status"] == "SF-SP-008"
        assert latest_by_workitem[workitem]["action"] == "human_confirmation"
