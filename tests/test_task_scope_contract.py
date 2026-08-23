from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_writing_plans_defines_four_task_scopes_and_traceability_rules() -> None:
    skill = read("skills/writing-plans/SKILL.md")
    template = read("skills/writing-plans/references/task-brief-template.md")

    for value in ("project", "requirement", "cross_cutting", "system"):
        assert value in skill
        assert value in template

    for phrase in (
        "`requirement` 至少强关联一个 `REQ-*` 或 `NFR-*`",
        "`cross_cutting` 强关联一个或多个 `REQ-*` / `NFR-*`",
        "`project` 关联项目基线、项目章程或设计项",
        "`system` 对产品进度贡献为零",
        "不得复用 `task_kind` 表达 `task_scope`",
        "沿用现有关系图",
    ):
        assert phrase in skill

    assert "- 任务层级：`project | requirement | cross_cutting | system`" in template
    assert "- 关联目标：" in template
    assert "强关系" in template


def test_writing_plans_requires_explicit_task_priority() -> None:
    skill = read("skills/writing-plans/SKILL.md")
    template = read("skills/writing-plans/references/task-brief-template.md")

    assert "`P0 | P1 | P2`" in skill
    assert "- 优先级：`P0 | P1 | P2`" in template
