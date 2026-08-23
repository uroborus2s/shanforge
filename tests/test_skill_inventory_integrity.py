from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_skill_directories_are_the_inventory_source() -> None:
    names = []
    for path in sorted((REPO_ROOT / "skills").glob("*/SKILL.md")):
        match = re.search(r"^name:\s*[\"']?([^\"'\n]+)", path.read_text(), re.MULTILINE)
        assert match, path
        name = match.group(1).strip()
        assert name == path.parent.name
        names.append(name)

    assert names
    assert len(names) == len(set(names))


def test_formal_design_does_not_freeze_a_skill_count_or_removed_runtime() -> None:
    for path in (REPO_ROOT / "docs" / "05-design").glob("*.md"):
        content = path.read_text(encoding="utf-8")
        assert not re.search(r"系统扫描仓内 \d+ 个 `skills/\*/SKILL\.md`", content), path

    workflow = (REPO_ROOT / "docs/05-design/workflow-execution-design.md").read_text()
    for removed_runtime in (
        "domain.session.models",
        "DefaultMemoryDomainService",
        "EvidenceRepositoryPort",
    ):
        assert removed_runtime not in workflow


def test_current_project_document_routes_resolve_to_registered_files() -> None:
    for config_path in (
        "config/software-factory.defaults.json",
        ".factory/project.json",
    ):
        config = json.loads((REPO_ROOT / config_path).read_text())
        for key in ("human_workflow_docs", "workflow_docs"):
            for path in config[key]:
                assert (REPO_ROOT / path).is_file(), f"{config_path}: {key}: {path}"

    project = json.loads((REPO_ROOT / ".factory/project.json").read_text())
    for role in project["roles"]:
        for path in role["docs"]:
            assert (REPO_ROOT / path).is_file(), f"{role['id']}: {path}"
