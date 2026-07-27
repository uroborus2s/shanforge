from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_controller_exposes_project_position_before_internal_routing() -> None:
    controller = read("skills/using-shanforge/SKILL.md")

    for phrase in (
        "项目位置快照",
        "项目整体进度",
        "当前任务",
        "已完成",
        "正在执行",
        "停止原因",
        "唯一下一动作",
        "用户可见的下一动作必须描述项目动作",
        "不得只写调用某个 skill",
    ):
        assert phrase in controller


def test_controller_distinguishes_internal_actions_from_true_human_gates() -> None:
    controller = read("skills/using-shanforge/SKILL.md")

    for phrase in (
        "真实人工 Gate",
        "内部动作不是人工 Gate",
        "实现、验证、独立只读评审、同范围整改和 memory sync",
        "reviewer `approved` 不自动等于 `pending_human_confirmation`",
        "产品或需求取舍",
        "风险接受",
        "扩大授权范围",
        "破坏性或外部动作",
        "精确候选哈希批准或正式发布",
    ):
        assert phrase in controller

    assert "reviewer 已 approved | 无工作 skill | 必须进入人工确认" not in controller


def test_execution_skills_continue_only_inside_authorized_envelope() -> None:
    for path in (
        "skills/executing-plans/SKILL.md",
        "skills/subagent-driven-development/SKILL.md",
    ):
        skill = read(path)
        for phrase in (
            "授权执行包",
            "不要逐项请求继续",
            "普通 task checkpoint 不是人工 Gate",
            "授权范围不得扩大",
            "需要人类产品决策",
            "超出允许文件范围",
            "破坏性或外部动作",
            "stop_reason",
        ):
            assert phrase in skill, f"{path} missing {phrase}"

    subagent = read("skills/subagent-driven-development/SKILL.md")
    assert "只有 `human_confirmation_required: true` 且有完整 `gate_reason` 时" in subagent
    assert "普通授权任务不得额外制造人工 Gate" in subagent
    assert "`approved` 和 `done` 由流程总控、独立评审、验证和人工确认共同决定" not in subagent


def test_readonly_review_and_same_scope_remediation_are_internal_actions() -> None:
    review = read("skills/requesting-code-review/SKILL.md")

    for phrase in (
        "只读独立评审是已授权任务的内部质量动作",
        "无需为只读派发单独请求人工授权",
        "同范围整改循环",
        "changes_requested",
        "不扩大原授权范围",
        "human_confirmation_required",
        "只有真实人工 Gate 才写 `pending_human_confirmation`",
    ):
        assert phrase in review

    assert "loop 结束必须进入 `pending_human_confirmation`" not in review
    assert "需要子 agent 但用户未授权时，必须停止并请求授权" not in review


def test_memory_recovery_prefers_current_header_over_historical_gates() -> None:
    memory = read("skills/project-memory/SKILL.md")

    for phrase in (
        "当前状态头部优先于历史条目",
        "历史条目中的“当前”“下一步”不得覆盖头部",
        "项目整体进度",
        "当前任务",
        "停止原因",
        "唯一下一动作",
        "不得恢复已撤销、已取代或已关闭的 Gate",
    ):
        assert phrase in memory


def test_completion_evidence_declares_scope_level_and_remaining_work() -> None:
    verification = read("skills/verification-before-completion/SKILL.md")

    for phrase in (
        "完成层级",
        "completion_level: task | stage | project",
        "任务完成不等于项目完成",
        "scope_remaining",
        "project_position",
        "stop_reason",
    ):
        assert phrase in verification


def test_runtime_skill_management_is_not_reintroduced() -> None:
    assert not (REPO_ROOT / "src" / "runtime" / "skills").exists()
    assert not (REPO_ROOT / "src" / "settings" / "skills").exists()
