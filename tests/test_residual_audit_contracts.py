from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_residual_skill_wording_is_scoped_and_uses_acceptance_criteria() -> None:
    article = read("skills/article-writing/SKILL.md")
    frontend = read("skills/frontend-patterns/SKILL.md")

    assert "用户提供或明确授权" in article
    assert "不得自行抓取、推断或模仿未授权个人" in article
    assert "多个兄弟或下游组件共享" in frontend
    assert "多个远端组件共享" not in frontend

    for path in (
        "skills/using-shanforge/SKILL.md",
        "skills/writing-plans/SKILL.md",
        "skills/executing-plans/SKILL.md",
        "skills/subagent-driven-development/SKILL.md",
    ):
        content = read(path)
        assert "验收标准" in content
        assert "验收结果明确" not in content
        assert "缺目标、验收结果、依赖" not in content


def test_subagent_dispatch_and_result_contracts_have_one_owner() -> None:
    subagent = read("skills/subagent-driven-development/SKILL.md")
    using = read("skills/using-shanforge/SKILL.md")
    result_contract = read("skills/using-shanforge/references/work-skill-return-contract.md")

    assert "using-shanforge` 的“子代理严格派发判定”为唯一规范定义" in subagent
    assert "本 skill 内 `source_or_test_write + execution_authorized=true" not in subagent
    assert "本 skill 的 worker 路由沿用既有简写" not in subagent
    assert "工作 Skill 本职结果包：" not in using
    assert "本职结果包字段、`release_summary` 及其适用性只由" in using
    assert "release_summary:" in result_contract


def test_using_shanforge_route_fields_have_non_overlapping_chinese_groups() -> None:
    using = read("skills/using-shanforge/SKILL.md")

    expected = (
        "任务身份：`work_item_id`、`task_card_id`、`wbs_id`（来自基础 route）",
        "控制/复杂度：`control_model`、`task_complexity`、`risk_level`、`reasoning_demand`",
        "风险/范围：`execution_authorized`、`capability_source`、`route_reason`",
        "派发：`execution_model`、`dispatch_role`、`dispatch_required`、`dispatch_mode`、`requested_reasoning_effort`、`fork_turns`",
        "Gate/升级：`current_gate`、`escalation_triggers`",
    )
    for phrase in expected:
        assert phrase in using

    assert "任务身份为 `control_model`" not in using
