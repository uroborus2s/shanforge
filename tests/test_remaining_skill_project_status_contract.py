from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

OWNER_SKILLS = {
    "executing-plans",
    "project-memory",
    "requesting-code-review",
    "subagent-driven-development",
    "using-shanforge",
    "verification-before-completion",
}

WORK_SKILLS = {
    "agent-harness-construction",
    "ai-first-engineering",
    "ai-regression-testing",
    "algorithmic-art",
    "api-design",
    "art-asset-pipeline",
    "article-writing",
    "brainstorming",
    "browser-control",
    "crawler4j-model-project",
    "doc-coauthoring",
    "document-templates",
    "docx",
    "frontend-patterns",
    "gitcommitzh",
    "go-developer",
    "humanizer",
    "java-developer",
    "pdf",
    "python-uv-project",
    "receiving-code-review",
    "requirements-engineering",
    "shadcn",
    "stratix-admin-web",
    "stratix-service",
    "systematic-debugging",
    "tdd-workflow",
    "ui-ux-pro-max",
    "webapp-testing",
    "writing-plans",
    "xlsx",
}

STATUS_FACTS = (
    "project_position: <第 N/TOTAL 步 / 阶段 / 当前任务>",
    "completion_level: none | task | stage | project",
    "stop_reason: none | blocker | human_gate",
    "scope_remaining: <已授权范围内剩余工作；没有则写“无”>",
)


def read_skill(name: str) -> str:
    return (REPO_ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")


def test_remaining_skill_scope_is_exactly_the_non_owner_top_level_set() -> None:
    actual = {path.parent.name for path in (REPO_ROOT / "skills").glob("*/SKILL.md")}

    assert len(actual) == 37
    assert len(WORK_SKILLS) == 31
    assert actual == OWNER_SKILLS | WORK_SKILLS
    assert not OWNER_SKILLS & WORK_SKILLS


PROJECT_CONTRACT_LINK = (
    "项目化执行时，沿用 [工作 Skill 回写契约]"
    "(../using-shanforge/references/work-skill-return-contract.md)；"
    "本 skill 的现有专业输出和失败语义不变。"
)


def test_work_skills_do_not_duplicate_project_status_envelope() -> None:
    for name in sorted(WORK_SKILLS):
        skill = read_skill(name)
        for fact in STATUS_FACTS:
            assert fact not in skill, f"skills/{name}/SKILL.md still owns {fact}"
        assert "## 项目化状态边界" not in skill, name


def test_work_skills_do_not_duplicate_the_shared_return_contract() -> None:
    for name in sorted(WORK_SKILLS):
        skill = read_skill(name)
        assert skill.count(PROJECT_CONTRACT_LINK) <= 1, name

    assert PROJECT_CONTRACT_LINK not in read_skill("stratix-service")


def test_runtime_skill_management_stays_removed() -> None:
    assert not (REPO_ROOT / "src" / "runtime" / "skills").exists()
    assert not (REPO_ROOT / "src" / "settings" / "skills").exists()
