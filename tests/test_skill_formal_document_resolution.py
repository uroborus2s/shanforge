from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_work_skills_resolve_registered_formal_documents_instead_of_hardcoding_layout() -> None:
    for path in (
        "skills/brainstorming/SKILL.md",
        "skills/requirements-engineering/SKILL.md",
    ):
        skill = read(path)
        assert ".factory/memory/doc-map.md" in skill
        assert "docs/04-project-development/" not in skill


def test_document_templates_preserve_registered_layout_and_only_fallback_for_new_projects() -> None:
    skill = read("skills/document-templates/SKILL.md")
    workflow = skill.split("## 默认工作流", 1)[1].split("\n## ", 1)[0]
    registered = next(line for line in workflow.splitlines() if line.startswith("2. "))
    fallback = next(line for line in workflow.splitlines() if line.startswith("4. "))

    assert ".factory/memory/doc-map.md" in registered
    assert "保持当前布局" in registered
    assert "未登记的新项目" in fallback
    assert "回退布局" in fallback
    assert workflow.index(registered) < workflow.index(fallback)
