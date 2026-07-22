from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from pathlib import Path

import pytest

from application.project_knowledge.query_service import QueryFailure
from settings.composition.project_knowledge import (
    _atomic_replace_index,
    build_application,
)

ROOT = Path(__file__).resolve().parents[1]
FIELD_MAP = ROOT / (
    ".factory/workitems/FLOW-CONTRACT-001/drafts/"
    "REQ-CHANGE-PROJECT-KNOWLEDGE-001.pm-field-map.R009.json"
)


def _workspace(tmp_path: Path) -> tuple[Path, Path]:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/index.md").write_text(
        "<!-- sf:document-id=DOC-INDEX -->\n# Project index\n", encoding="utf-8"
    )
    registry = {
        "schema_id": "ProjectKnowledgeSourceRegistry/v1",
        "registry_version": "1",
        "sources": [
            {
                "registry_source_id": "SRC-DOCS",
                "kind": "markdown",
                "roots": ["docs"],
                "include": ["**/*.md"],
                "exclude": [],
                "extractor_id": "markdown-v1",
                "access_class": "public",
                "authority_rank": 100,
                "stable_id_policy": "explicit_document_and_section_id_or_path",
                "max_file_bytes": 100_000,
            }
        ],
    }
    registry_path = tmp_path / ".factory/project-knowledge/source-registry.json"
    registry_path.parent.mkdir(parents=True)
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    project_path = tmp_path / ".factory/project.json"
    project_path.write_text(
        json.dumps({"project_name": "fixture", "owner": "owner", "idea": "fixture"}),
        encoding="utf-8",
    )
    field_map = tmp_path / (
        ".factory/workitems/FLOW-CONTRACT-001/drafts/"
        "REQ-CHANGE-PROJECT-KNOWLEDGE-001.pm-field-map.R009.json"
    )
    field_map.parent.mkdir(parents=True)
    field_map.write_bytes(FIELD_MAP.read_bytes())
    git = tmp_path / ".git"
    git.mkdir()
    (git / "HEAD").write_text("fixture-head\n", encoding="utf-8")
    database = tmp_path / ".factory/index/project-knowledge.sqlite3"
    return tmp_path, database


def test_rebuild_removes_registered_stale_sidecars_and_first_read_succeeds(
    tmp_path: Path,
) -> None:
    root, database = _workspace(tmp_path)
    application = build_application(root)
    first = application.execute("index.rebuild")
    assert first["source_count"] == 1

    temporary = database.with_suffix(".sqlite3.rebuild")
    for suffix in ("", "-wal", "-shm", "-journal"):
        Path(f"{temporary}{suffix}").write_bytes(b"stale rebuild state")
    with closing(sqlite3.connect(database)) as connection:
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("CREATE TABLE IF NOT EXISTS rebuild_probe(value TEXT)")
        connection.commit()
    Path(f"{database}-wal").write_bytes(b"")
    Path(f"{database}-shm").write_bytes(b"")
    assert Path(f"{database}-wal").exists() and Path(f"{database}-shm").exists()

    rebuilt = application.execute("index.rebuild")
    assert rebuilt["source_count"] == 1
    with sqlite3.connect(database) as connection:
        assert connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        assert connection.execute("SELECT COUNT(*) FROM pm_project_profile").fetchone()[0] == 1
    assert not any(Path(f"{temporary}{suffix}").exists() for suffix in ("", "-wal", "-shm"))


def test_active_reader_fails_closed_with_exit_7_and_preserves_old_generation(
    tmp_path: Path,
) -> None:
    root, database = _workspace(tmp_path)
    application = build_application(root)
    first = application.execute("index.rebuild")
    generation = first["generation_id"]
    reader = sqlite3.connect(database)
    reader.execute("PRAGMA journal_mode=WAL")
    reader.execute("BEGIN")
    assert (
        reader.execute("SELECT generation_id FROM pk_generation WHERE status='current'").fetchone()[
            0
        ]
        == generation
    )

    with pytest.raises(QueryFailure) as raised:
        application.execute("index.rebuild")
    assert raised.value.code == "CONCURRENT_WRITER"
    assert raised.value.exit_code == 7
    assert (
        reader.execute("SELECT generation_id FROM pk_generation WHERE status='current'").fetchone()[
            0
        ]
        == generation
    )
    reader.close()


def test_failure_before_replace_keeps_the_previous_database(tmp_path: Path) -> None:
    old = tmp_path / "old.sqlite3"
    new = tmp_path / "new.sqlite3"
    for path, value in ((old, "old"), (new, "new")):
        with sqlite3.connect(path) as connection:
            connection.execute("CREATE TABLE marker(value TEXT)")
            connection.execute("INSERT INTO marker VALUES(?)", (value,))
            connection.execute("PRAGMA journal_mode=WAL")

    with pytest.raises(RuntimeError, match="injected"):
        _atomic_replace_index(new, old, fail_at="before_replace")
    with sqlite3.connect(old) as connection:
        assert connection.execute("SELECT value FROM marker").fetchone()[0] == "old"


def test_snapshot_checks_registered_sources_then_reuses_unchanged_site(tmp_path: Path) -> None:
    root, _ = _workspace(tmp_path)
    application = build_application(root)

    first = application.execute("snapshot", html=True)
    assert first["cache_hit"] is False
    assert first["index"]["changed"] is True

    document = root / "docs/index.md"
    document.write_text(document.read_text(encoding="utf-8") + "\n## 新章节\n", encoding="utf-8")
    changed = application.execute("snapshot", html=True)
    assert changed["cache_hit"] is False
    assert changed["index"]["changed"] is True
    assert changed["index"]["parsed_count"] == 1

    unchanged = application.execute("snapshot", html=True)
    assert unchanged["cache_hit"] is True
    assert unchanged["index"]["changed"] is False
    assert unchanged["rendered_pages"] == 0
