from __future__ import annotations

import hashlib
import json
from pathlib import Path

from settings.project_knowledge.migration import ProjectKnowledgeMigrationPreparer


def _write(root: Path, relative: str, text: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_migration_prepare_accounts_every_exact_legacy_source_without_deleting(
    tmp_path: Path,
) -> None:
    sources = {
        "docs/05-design/ai-sdlc-catalog.source.json": '{"schema_id":"catalog"}',
        "docs/05-design/ai-sdlc-catalog.manifest.json": '{"schema_id":"manifest"}',
        ".factory/pm/README.md": "# PM",
        ".factory/pm/project-brief.md": "# Brief",
        ".factory/pm/team-raci.md": "# RACI",
        ".factory/pm/milestones.md": "# Milestones",
        ".factory/pm/wbs.md": "# WBS",
        ".factory/pm/risk-register.jsonl": '{"id":"risk-1"}\n',
        ".factory/pm/communication-plan.md": "# Communication",
        ".factory/pm/meeting-notes/one.md": "# Meeting",
        ".factory/pm/status-reports/one.md": "# Status",
        ".factory/pm/change-register.jsonl": '{"id":"change-1"}\n',
        ".factory/pm/closure-report.md": "# Closure",
        ".factory/pm/dashboard.md": "# Derived dashboard",
    }
    for relative, content in sources.items():
        _write(tmp_path, relative, content)
    _write(
        tmp_path,
        ".factory/project-knowledge/relation-declarations.json",
        json.dumps({"relations": [{"strength": "strong"}, {"strength": "weak"}]}),
    )
    preparer = ProjectKnowledgeMigrationPreparer(tmp_path)

    dry_run = preparer.prepare(job_id="migration-001", apply=False)
    assert dry_run.written is False
    assert not (tmp_path / ".factory/cache/project-knowledge/migration").exists()

    receipt = preparer.prepare(job_id="migration-001", apply=True)
    assert receipt.written is True
    assert receipt.legacy_delete_count == 0
    assert receipt.strong_relations_before == receipt.strong_relations_after == 1
    assert {item.source for item in receipt.items} == set(sources)
    for item in receipt.items:
        source = tmp_path / item.source
        assert source.exists()
        assert item.before_sha256 == hashlib.sha256(source.read_bytes()).hexdigest()
        assert item.target
        assert item.rollback_path
        assert (tmp_path / item.rollback_path).is_file()

    package = tmp_path / receipt.package_path
    manifest = json.loads((package / "migration-plan.json").read_text(encoding="utf-8"))
    assert manifest["legacy_delete_count"] == 0
    assert manifest["strong_relation_loss"] == 0
    assert not (tmp_path / ".factory/catalog/ai-sdlc-catalog.source.json").exists()
