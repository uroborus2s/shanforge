from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _read_skill(skill_name: str) -> str:
    return (REPO_ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")


def test_tdd_workflow_requires_root_cause_before_bug_fix() -> None:
    content = _read_skill("tdd-workflow")

    for phrase in (
        "Bug 根因先于修复",
        "直接原因与根源原因",
        "禁止把 `try/except`、默认值、空结果、重试、忽略异常、宽松解析或“兼容一下”当作主要修复",
        "不得提交行为修复",
    ):
        assert phrase in content


def test_ai_regression_testing_rejects_fallback_only_fixes() -> None:
    content = _read_skill("ai-regression-testing")

    for phrase in (
        "Bug 根因修复门槛",
        "回归测试不是为兜底方案背书",
        "字段缺失时临时填默认值，却不修复上游 SELECT、映射、schema 或契约",
        "根因未明时用兜底、默认值、静默异常或宽松兼容声明修复完成",
    ):
        assert phrase in content


def test_ai_first_engineering_defines_team_bug_fix_discipline() -> None:
    content = _read_skill("ai-first-engineering")

    for phrase in (
        "Bug 修复纪律",
        "先定位根因，再修改实现",
        "禁止把默认值、空结果、宽松解析、吞异常、重试或额外 fallback 当作主要修复",
        "Bug 修复测试必须覆盖根因路径",
    ):
        assert phrase in content


def test_python_uv_project_applies_root_cause_rule_to_python_debugging() -> None:
    content = _read_skill("python-uv-project")

    for phrase in (
        "修 Bug 时必须先复现并定位根因",
        "禁止用宽泛 `except Exception`、返回空集合、默认成功、"
        "静默跳过、宽松解析或额外 fallback 掩盖根因",
        "直接原因、根源原因和证据",
        "防回归测试必须断言根因路径",
    ):
        assert phrase in content
