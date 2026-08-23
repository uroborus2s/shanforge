from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_requirements_engineering_declares_shanforge_outputs_and_gates() -> None:
    skill = read("skills/requirements-engineering/SKILL.md")
    frontmatter = skill.split("---", 2)[1]

    for phrase in (
        ".factory/workitems/<WORKITEM-ID>/brief.md",
        ".factory/workitems/<WORKITEM-ID>/ledger.jsonl",
        ".factory/memory/prd.summary.md",
        ".factory/memory/tasks.summary.md",
        "工作结果：",
        "requirements_ready",
        "needs_user_input",
        "不得把工作项写成 `approved`、`done`、`human_approved`",
        "`needs` 只是状态回写，不是下一步 skill 决策",
        "流程路由由 `using-shanforge` 判断",
    ):
        assert phrase in skill

    assert "requirements-analyst" not in frontmatter


def test_requirements_engineering_keeps_prd_template_linked() -> None:
    skill = read("skills/requirements-engineering/SKILL.md")
    template = read("skills/requirements-engineering/references/prd-template.md")

    assert "references/prd-template.md" in skill
    assert "REQ-XXX" in template
    assert "AC-1" in template
    assert "NFR-XXX" in template
    assert "INVEST 检查" in template
    assert "AC 示例" in template
    assert "NFR 示例" in template


def test_requirements_engineering_supports_flow_contract_scenarios() -> None:
    skill = read("skills/requirements-engineering/SKILL.md")

    for phrase in (
        "new_project",
        "add_requirement",
        "change_requirement",
        "fix_bug",
        "需求版本规则",
        "baseline 影响分析",
        "领域模块映射",
        "baseline 变更建议",
        "bug 需求必须先有复现和根因",
    ):
        assert phrase in skill


def test_prd_template_tracks_version_impact_domain_and_baseline() -> None:
    template = read("skills/requirements-engineering/references/prd-template.md")

    for phrase in (
        "## 版本信息",
        "## 版本历史",
        "场景：new_project | add_requirement | change_requirement | fix_bug",
        "baseline 影响：无 | 领域 | 架构 | 数据库 | API | UI",
        "领域模块映射",
        "baseline 变更建议",
    ):
        assert phrase in template
