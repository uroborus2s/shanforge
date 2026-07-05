from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def scenario_bodies(reference: str) -> dict[str, str]:
    matches = re.finditer(
        r"^### (SF-SP-009-S\d)：.*?\n(?P<body>.*?)(?=^### SF-SP-009-S\d：|\Z)",
        reference,
        re.MULTILINE | re.DOTALL,
    )
    return {match.group(1): match.group("body") for match in matches}


def test_black_box_flow_eval_reference_covers_required_scenarios() -> None:
    reference = read("skills/using-shanforge/references/black-box-flow-eval.md")

    expected_scenarios = {
        "SF-SP-009-S1": ("一句话需求", "帮我加一个导出按钮"),
        "SF-SP-009-S2": ("Bug 修复", "这个测试失败了，修一下"),
        "SF-SP-009-S3": ("Review 反馈", "按 reviewer 的 1-6 条修改"),
        "SF-SP-009-S4": ("压缩恢复", "中断后继续同一 work item"),
        "SF-SP-009-S5": ("完成声明", "现在完成了吗"),
        "SF-SP-009-S6": ("自评隔离", "我检查过了，可以完成"),
    }

    for scenario_id, phrases in expected_scenarios.items():
        assert scenario_id in reference
        for phrase in phrases:
            assert phrase in reference

    assert len(re.findall(r"^### SF-SP-009-S\d", reference, re.MULTILINE)) == 6


def test_black_box_flow_eval_defines_scoring_and_failure_gates() -> None:
    reference = read("skills/using-shanforge/references/black-box-flow-eval.md")

    for phrase in (
        "fast smoke",
        "full regression",
        "评分断言",
        "2 分",
        "1 分",
        "0 分",
        "总分必须 >= 90",
        "最高可能得分 = 纳入场景的 critical assertion 总数 * 2",
        "总分 = round(实际得分 / 最高可能得分 * 100)",
        "每个场景默认同权",
        "任一 critical assertion 为 0 分则失败",
        "不得读取实现 diff",
        "不得调用中心脚本",
        "不得把实现者自检写成 approved",
        "不得在没有根因和回归测试时声明 bug 修复完成",
    ):
        assert phrase in reference


def test_black_box_flow_eval_scenarios_have_scored_critical_assertions() -> None:
    reference = read("skills/using-shanforge/references/black-box-flow-eval.md")

    for scenario_id, body in scenario_bodies(reference).items():
        assert "期望行为：" in body, scenario_id
        assert "critical assertions：" in body, scenario_id
        assert "评分：" in body, scenario_id
        assert "每条 critical assertion 单独按 `2/1/0` 计分" in body, scenario_id
        critical_block = body.split("critical assertions：", 1)[1].split("评分：", 1)[0]
        assert len(re.findall(r"^- ", critical_block, re.MULTILINE)) >= 3, scenario_id


def test_black_box_flow_eval_evidence_format_is_complete() -> None:
    reference = read("skills/using-shanforge/references/black-box-flow-eval.md")

    for field in (
        "Scenario:",
        "Input:",
        "Allowed context:",
        "Observed actions:",
        "Files read:",
        "Files written:",
        "Commands run:",
        "Critical assertions:",
        "Actual score:",
        "Max score:",
        "Normalized score:",
        "Failure reason:",
    ):
        assert field in reference


def test_flow_controller_links_sf_sp_009_eval_without_script_gate() -> None:
    skill = read("skills/using-shanforge/SKILL.md")
    reference = read("skills/using-shanforge/references/black-box-flow-eval.md")

    assert "SF-SP-009" in skill
    assert "references/black-box-flow-eval.md" in skill
    assert "黑盒流程评估" in skill

    forbidden = (
        "factory-dispatch loop-gate",
        "factory-workitem-loop-gate",
        "scripts/factory-workitem-loop-gate",
    )
    for phrase in forbidden:
        assert phrase not in reference
        assert phrase not in skill


def test_workflow_plan_tracks_sf_sp_009_development_scope() -> None:
    plan = read(
        "docs/04-project-development/05-development-process/"
        "superpowers-workflow-integration-plan.md"
    )

    assert "`SF-SP-009`：当前已进入黑盒流程 eval 开发" in plan
    assert "一句话需求、bug 修复、review 反馈、压缩恢复、完成声明和自评隔离" in plan
    assert "不新增中心脚本 gate" in plan
