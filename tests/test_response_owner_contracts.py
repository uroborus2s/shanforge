from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_receiving_review_owns_evidence_based_pushback_and_authorized_writes_only() -> None:
    skill = read("skills/receiving-code-review/SKILL.md")

    for phrase in (
        "基于技术证据提出异议",
        "只有 allowlist 与 `write_policy` 同时授权时才写 triage、response、ledger 或 memory",
        "triage/response 只由 receiving-code-review 在确有 review feedback 且授权时形成",
    ):
        assert phrase in skill


def test_project_memory_keeps_status_reads_non_persistent_and_explains_receipts() -> None:
    skill = read("skills/project-memory/SKILL.md")

    for phrase in (
        "读取回执（receipt）",
        "无活动 WorkItem 的纯 `SB-STATUS` / `no_project_write` 请求",
        "跳过 work-item ledger",
        "不因缺少 TaskCard/WBS 返回 `blocked`",
        "不写项目事实",
    ):
        assert phrase in skill


def test_webapp_testing_returns_browser_candidate_to_the_controller() -> None:
    skill = read("skills/webapp-testing/SKILL.md")

    assert "不得自行决定转交 `browser-control`" in skill
    assert "由 `using-shanforge` 总控路由" in skill


def test_review_requester_does_not_own_feedback_triage_or_response() -> None:
    requesting = read("skills/requesting-code-review/SKILL.md")

    assert "不写 triage 或 response" in requesting
    assert "只组织 review 与原范围整改" in requesting


def test_plan_and_session_templates_keep_recovery_and_gate_contracts() -> None:
    review = read("skills/writing-plans/references/plan-review-template.md")
    session = read("skills/project-memory/references/session-card-template.md")
    plan = read("skills/writing-plans/references/workitem-plan-template.md")

    for phrase in (
        "依赖 DAG",
        "TaskCard 生命周期词表",
        "planned | active | ready_for_review | completed | closed | blocked",
        "review_status 词表",
        "not_requested | self_check_passed | approved | changes_requested",
        "恢复字段",
    ):
        assert phrase in review
    assert "停止原因：<none 或具体原因>" in session
    for phrase in ("Gate ID", "owner", "进入条件", "evidence path"):
        assert phrase in plan


def test_harness_candidates_and_release_facts_do_not_replace_controller_response_owner() -> None:
    harness = read("skills/agent-harness-construction/SKILL.md")
    release = read("skills/release-deployment/SKILL.md")
    contract = read("skills/using-shanforge/references/work-skill-return-contract.md")

    assert "仅为内部候选" in harness
    assert "只有一个 `next_required_action`" in harness
    assert "只返回本职发布回执" in release
    assert "不拥有最终 human/progress/verification/defect/change/release 响应" in release
    for field in (
        "progress_delta",
        "verification_summary",
        "defect_summary",
        "change_locations",
        "release_summary",
    ):
        assert field in contract
    assert "唯一 `next_required_action`" in contract
