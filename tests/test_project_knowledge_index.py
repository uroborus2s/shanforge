from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from application.project_knowledge.index_service import ProjectKnowledgeIndexService
from application.project_knowledge.query_service import ProjectKnowledgeQueryService, QueryFailure
from runtime.project_knowledge.extractors import default_extractors
from settings.project_knowledge.query_store import SQLiteKnowledgeQueryStore
from settings.project_knowledge.source_registry import FileSourceRegistry
from settings.project_knowledge.sqlite_index import SQLiteProjectKnowledgeIndex


def write_registry(root: Path, *, include: str = "*.md") -> Path:
    config = {
        "schema_id": "ProjectKnowledgeSourceRegistry/v1",
        "registry_version": "1",
        "sources": [
            {
                "registry_source_id": "SRC-DOCS",
                "kind": "markdown",
                "roots": ["docs"],
                "include": [include],
                "exclude": [],
                "extractor_id": "markdown-v1",
                "access_class": "project",
                "authority_rank": 100,
                "stable_id_policy": "explicit_or_path",
                "max_file_bytes": 100000,
            }
        ],
    }
    path = root / "registry.json"
    path.write_text(json.dumps(config), encoding="utf-8")
    return path


def service(root: Path, registry_path: Path) -> tuple[ProjectKnowledgeIndexService, Path]:
    database = root / "knowledge.sqlite3"
    registry = FileSourceRegistry(root, registry_path)
    index = SQLiteProjectKnowledgeIndex(database)
    return ProjectKnowledgeIndexService(registry, index, default_extractors()), database


def test_concrete_sources_incremental_reuse_and_deleted_source_cleanup(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    body = "<!-- sf:document-id=DOC-SHARED -->\n# Shared\n\nSame definition.\n"
    (docs / "a.md").write_text(body, encoding="utf-8")
    (docs / "b.md").write_text(body, encoding="utf-8")
    indexer, database = service(tmp_path, write_registry(tmp_path))

    cold = indexer.refresh(as_of="2026-07-22T00:00:00Z")
    assert cold.source_count == 2
    assert cold.parsed_count == 2
    warm = indexer.refresh(as_of="2026-07-22T00:00:01Z")
    assert warm.source_count == 2
    assert warm.parsed_count == 0
    assert warm.reused_count == 2

    (docs / "a.md").unlink()
    after_delete = indexer.refresh(as_of="2026-07-22T00:00:02Z")
    assert after_delete.deleted_count == 1
    with sqlite3.connect(database) as connection:
        current = connection.execute(
            "SELECT generation_id FROM pk_generation WHERE status='current'"
        ).fetchone()[0]
        sources = connection.execute(
            "SELECT COUNT(*) FROM pk_generation_source WHERE generation_id=?", (current,)
        ).fetchone()[0]
        entities = connection.execute(
            "SELECT COUNT(*) FROM pk_entity WHERE entity_id LIKE 'doc:%'"
        ).fetchone()[0]
    assert sources == 1
    assert entities == 1


def test_generation_retention_keeps_only_current_and_atomic_recovery_parent(
    tmp_path: Path,
) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    document = docs / "index.md"
    document.write_text("# First\n", encoding="utf-8")
    indexer, database = service(tmp_path, write_registry(tmp_path))

    for position in range(4):
        document.write_text(f"# Revision {position}\n", encoding="utf-8")
        indexer.refresh(as_of=f"2026-07-22T00:00:0{position}Z")

    with sqlite3.connect(database) as connection:
        generations = connection.execute(
            "SELECT generation_id,parent_generation_id,status FROM pk_generation ORDER BY status"
        ).fetchall()
        contribution_generations = connection.execute(
            "SELECT COUNT(DISTINCT generation_id) FROM pk_generation_source"
        ).fetchone()[0]
    assert len(generations) == 2
    assert contribution_generations == 2
    current = next(row for row in generations if row[2] == "current")
    previous = next(row for row in generations if row[2] == "previous")
    assert current[1] == previous[0]
    assert previous[1] is None


def test_single_existing_python_source_uses_consistent_incremental_projection(
    tmp_path: Path,
) -> None:
    source_root = tmp_path / "tests"
    source_root.mkdir()
    source = source_root / "example.py"
    source.write_text("def test_value() -> int:\n    return 1\n", encoding="utf-8")
    registry_path = tmp_path / "registry.json"
    registry_path.write_text(
        json.dumps(
            {
                "schema_id": "ProjectKnowledgeSourceRegistry/v1",
                "registry_version": "1",
                "sources": [
                    {
                        "registry_source_id": "SRC-PYTHON",
                        "kind": "python",
                        "roots": ["tests"],
                        "include": ["*.py"],
                        "exclude": [],
                        "extractor_id": "python-ast-v1",
                        "access_class": "project",
                        "authority_rank": 80,
                        "stable_id_policy": "ast-qualified-name",
                        "max_file_bytes": 100000,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    indexer, database = service(tmp_path, registry_path)
    first = indexer.refresh(as_of="2026-07-22T00:00:00Z")
    source.write_text("def test_updated() -> int:\n    return 2\n", encoding="utf-8")
    second = indexer.refresh(as_of="2026-07-22T00:00:01Z")

    assert first.parsed_count == 1
    assert second.parsed_count == 1
    with sqlite3.connect(database) as connection:
        assert connection.execute("SELECT COUNT(*) FROM pk_generation").fetchone()[0] == 2
        assert connection.execute("SELECT COUNT(*) FROM pk_code_file").fetchone()[0] == 1
        assert connection.execute("SELECT COUNT(*) FROM pk_code_symbol").fetchone()[0] == 1
        assert connection.execute("SELECT COUNT(*) FROM pk_test").fetchone()[0] == 1
        assert connection.execute("SELECT COUNT(*) FROM pk_search_entry").fetchone()[0] == 1
        assert (
            connection.execute(
                "SELECT COUNT(*) FROM pk_search_fts WHERE pk_search_fts MATCH 'test_updated'"
            ).fetchone()[0]
            == 1
        )
        assert (
            connection.execute(
                "SELECT COUNT(*) FROM pk_search_fts WHERE pk_search_fts MATCH 'test_value'"
            ).fetchone()[0]
            == 0
        )


def test_failed_conflicting_generation_rolls_back_for_concurrent_reader(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "a.md").write_text(
        "<!-- sf:document-id=DOC-1 -->\n# One\n\nDefinition A.\n", encoding="utf-8"
    )
    indexer, database = service(tmp_path, write_registry(tmp_path))
    first = indexer.refresh(as_of="2026-07-22T00:00:00Z")
    reader = sqlite3.connect(database)
    reader.execute("PRAGMA journal_mode=WAL")
    assert (
        reader.execute("SELECT generation_id FROM pk_generation WHERE status='current'").fetchone()[
            0
        ]
        == first.generation_id
    )

    (docs / "b.md").write_text(
        "<!-- sf:document-id=DOC-1 -->\n# Other\n\nConflicting definition.\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="conflicting definitions"):
        indexer.refresh(as_of="2026-07-22T00:00:01Z")
    assert (
        reader.execute("SELECT generation_id FROM pk_generation WHERE status='current'").fetchone()[
            0
        ]
        == first.generation_id
    )
    reader.close()


def test_registry_rejects_path_escape_and_cold_rebuild_is_deterministic(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "index.md").write_text("# Index\n", encoding="utf-8")
    registry_path = write_registry(tmp_path)
    first, first_database = service(tmp_path, registry_path)
    result_one = first.refresh(as_of="2026-07-22T00:00:00Z")
    first_database.unlink()
    second, _ = service(tmp_path, registry_path)
    result_two = second.refresh(as_of="2026-07-22T00:00:00Z")
    assert result_one.source_root_sha256 == result_two.source_root_sha256

    payload = json.loads(registry_path.read_text(encoding="utf-8"))
    payload["sources"][0]["roots"] = ["../outside"]
    registry_path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="project root"):
        FileSourceRegistry(tmp_path, registry_path).sources()


def test_extractor_version_change_invalidates_unchanged_file_contribution(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "index.md").write_text("# Index\n", encoding="utf-8")
    registry_path = write_registry(tmp_path)
    indexer, _ = service(tmp_path, registry_path)
    indexer.refresh(as_of="2026-07-22T00:00:00Z")
    payload = json.loads(registry_path.read_text(encoding="utf-8"))
    payload["sources"][0]["extractor_id"] = "markdown-v2"
    registry_path.write_text(json.dumps(payload), encoding="utf-8")
    refreshed = indexer.refresh(as_of="2026-07-22T00:00:01Z")
    assert refreshed.parsed_count == 1
    assert refreshed.reused_count == 0


def test_discovery_cache_skips_full_scan_but_detects_changed_and_new_sources(
    tmp_path: Path,
) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    target = docs / "index.md"
    target.write_text("# Index\n", encoding="utf-8")
    registry_path = write_registry(tmp_path)
    database = tmp_path / "knowledge.sqlite3"
    cache = tmp_path / ".factory/cache/project-knowledge/source-discovery.json"

    def cached_service() -> ProjectKnowledgeIndexService:
        return ProjectKnowledgeIndexService(
            FileSourceRegistry(
                tmp_path,
                registry_path,
                discovery_cache_path=cache,
            ),
            SQLiteProjectKnowledgeIndex(database),
            default_extractors(),
        )

    first = cached_service().refresh(as_of="2026-07-22T00:00:00Z", git_commit="head-1")
    assert first.changed is True
    second = cached_service().refresh(as_of="2026-07-22T00:00:01Z", git_commit="head-1")
    assert second.changed is False
    assert second.parsed_count == 0

    target.write_text("# Changed\n", encoding="utf-8")
    changed = cached_service().refresh(as_of="2026-07-22T00:00:02Z", git_commit="head-1")
    assert changed.changed is True
    assert changed.parsed_count == 1

    (docs / "new.md").write_text("# New\n", encoding="utf-8")
    added = cached_service().refresh(as_of="2026-07-22T00:00:03Z", git_commit="head-1")
    assert added.changed is True
    assert added.source_count == 2


def test_git_head_change_publishes_a_new_generation_without_reparsing_sources(
    tmp_path: Path,
) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "index.md").write_text("# Index\n", encoding="utf-8")
    indexer, database = service(tmp_path, write_registry(tmp_path))

    first = indexer.refresh(as_of="2026-07-22T00:00:00Z", git_commit="head-a")
    second = indexer.refresh(as_of="2026-07-22T00:00:01Z", git_commit="head-b")

    assert second.changed is True
    assert second.parsed_count == 0
    assert second.generation_id != first.generation_id
    with sqlite3.connect(database) as connection:
        assert (
            connection.execute(
                "SELECT git_commit FROM pk_generation WHERE status='current'"
            ).fetchone()[0]
            == "head-b"
        )


def test_alias_module_revision_memory_and_meta_tables_have_production_writers(
    tmp_path: Path,
) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/index.md").write_text(
        "<!-- sf:document-id=DOC-1 -->\n# 项目说明\n", encoding="utf-8"
    )
    (tmp_path / "src/domain").mkdir(parents=True)
    (tmp_path / "src/domain/example.py").write_text(
        "def execute() -> None:\n    pass\n", encoding="utf-8"
    )
    (tmp_path / ".factory/memory").mkdir(parents=True)
    (tmp_path / ".factory/memory/agent-session.md").write_text(
        "# 当前记忆点\n\n只读取本卡。\n", encoding="utf-8"
    )
    (tmp_path / ".factory/project-knowledge").mkdir()
    (tmp_path / ".factory/project.json").write_text(
        json.dumps({"project_name": "sample"}), encoding="utf-8"
    )
    (tmp_path / ".factory/project-knowledge/id-aliases.json").write_text(
        json.dumps(
            {
                "schema_id": "ProjectKnowledgeIdAliases/v1",
                "aliases": [
                    {
                        "alias_entity_id": "DOC-OLD",
                        "canonical_entity_id": "doc:DOC-1",
                        "reason": "renamed",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    registry_path = tmp_path / "registry.json"
    registry_path.write_text(
        json.dumps(
            {
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
                        "stable_id_policy": "document",
                        "max_file_bytes": 100000,
                    },
                    {
                        "registry_source_id": "SRC-PYTHON",
                        "kind": "python",
                        "roots": ["src"],
                        "include": ["**/*.py"],
                        "exclude": [],
                        "extractor_id": "python-v1",
                        "access_class": "project",
                        "authority_rank": 80,
                        "stable_id_policy": "ast",
                        "max_file_bytes": 100000,
                    },
                    {
                        "registry_source_id": "SRC-MEMORY",
                        "kind": "markdown",
                        "roots": [".factory/memory"],
                        "include": ["*.md"],
                        "exclude": [],
                        "extractor_id": "markdown-v1",
                        "access_class": "restricted",
                        "authority_rank": 70,
                        "stable_id_policy": "checkpoint",
                        "max_file_bytes": 100000,
                    },
                    {
                        "registry_source_id": "SRC-PROJECT-CONFIG",
                        "kind": "json",
                        "roots": [".factory"],
                        "include": ["project.json", "project-knowledge/*.json"],
                        "exclude": [],
                        "extractor_id": "json-v1",
                        "access_class": "project",
                        "authority_rank": 100,
                        "stable_id_policy": "json-pointer",
                        "max_file_bytes": 100000,
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    indexer, database = service(tmp_path, registry_path)
    indexer.refresh(as_of="2026-07-22T00:00:00Z", git_commit="head-1")

    with sqlite3.connect(database) as connection:
        assert connection.execute("SELECT COUNT(*) FROM pk_entity_alias").fetchone()[0] == 1
        assert (
            connection.execute(
                "SELECT canonical_entity_id FROM pk_entity_alias WHERE alias_entity_id='DOC-OLD'"
            ).fetchone()[0]
            == "doc:DOC-1"
        )
        assert connection.execute(
            "SELECT layer_name,root_path FROM pk_module WHERE module_id='module:domain'"
        ).fetchone() == ("domain", "src/domain")
        assert (
            connection.execute(
                "SELECT module_id FROM pk_code_file WHERE import_name='src.domain.example'"
            ).fetchone()[0]
            == "module:domain"
        )
        assert connection.execute("SELECT COUNT(*) FROM pk_document_revision").fetchone()[0] == 2
        assert connection.execute(
            "SELECT project_id,is_current,size_bytes FROM pk_memory_checkpoint WHERE is_current=1"
        ).fetchone() == ("sample", 1, 38)
        assert connection.execute("SELECT COUNT(*) FROM pk_meta").fetchone()[0] == 2


def test_document_context_uses_section_budget_and_rejects_hash_drift(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    target = docs / "large.md"
    target.write_text(
        "<!-- sf:document-id=DOC-LARGE -->\n# Summary\n\nSmall overview.\n\n"
        "## Large appendix\n\n" + ("x" * 40_000),
        encoding="utf-8",
    )
    indexer, database = service(tmp_path, write_registry(tmp_path))
    indexer.refresh(as_of="2026-07-22T00:00:00Z")
    query = ProjectKnowledgeQueryService(SQLiteKnowledgeQueryStore(database, tmp_path))

    plan = query.context("doc:DOC-LARGE")
    assert plan["files"][0]["selector"]["section_id"] == "heading:summary"
    assert plan["total_bytes"] < target.stat().st_size

    target.write_text(
        target.read_text(encoding="utf-8").replace("Small overview.", "Changed overview."),
        encoding="utf-8",
    )
    with pytest.raises(QueryFailure) as stale:
        query.context("doc:DOC-LARGE")
    assert stale.value.code == "LOCATOR_NOT_FOUND"


def test_declared_relation_is_projected_and_rejects_missing_endpoint(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "requirement.md").write_text(
        "<!-- sf:document-id=REQ-DOC -->\n# Requirement\n", encoding="utf-8"
    )
    (docs / "design.md").write_text(
        "<!-- sf:document-id=DESIGN-DOC -->\n# Design\n", encoding="utf-8"
    )
    relations = tmp_path / "relations.json"
    relations.write_text(
        json.dumps(
            {
                "schema_id": "ProjectKnowledgeRelationDeclarations/v1",
                "relations": [
                    {
                        "from_entity_id": "doc:DESIGN-DOC",
                        "to_entity_id": "doc:REQ-DOC",
                        "relation_type": "SATISFIES",
                        "strength": "strong",
                        "confidence": 1.0,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "facts.json").write_text(
        json.dumps(
            {
                "requirements": [
                    {
                        "id": "REQ-1",
                        "title": "Indexed requirement",
                        "priority": "P0",
                        "status": "approved",
                        "acceptance_criteria": [
                            {
                                "id": "REQ-1-AC-1",
                                "statement": "Projection is queryable",
                                "status": "approved",
                            }
                        ],
                    }
                ],
                "tasks": [{"id": "TASK-1", "title": "Build index", "status": "active"}],
            }
        ),
        encoding="utf-8",
    )
    registry = {
        "schema_id": "ProjectKnowledgeSourceRegistry/v1",
        "registry_version": "1",
        "sources": [
            {
                "registry_source_id": "SRC-DOCS",
                "kind": "markdown",
                "roots": ["docs"],
                "include": ["*.md"],
                "exclude": [],
                "extractor_id": "markdown-v1",
                "access_class": "project",
                "authority_rank": 100,
                "stable_id_policy": "explicit_or_path",
                "max_file_bytes": 100000,
            },
            {
                "registry_source_id": "SRC-REL",
                "kind": "json",
                "roots": ["."],
                "include": ["relations.json", "facts.json"],
                "exclude": [],
                "extractor_id": "json-v1",
                "access_class": "project",
                "authority_rank": 100,
                "stable_id_policy": "json_pointer",
                "max_file_bytes": 100000,
            },
        ],
    }
    registry_path = tmp_path / "registry.json"
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    indexer, database = service(tmp_path, registry_path)

    indexer.refresh(as_of="2026-07-22T00:00:00Z")
    with sqlite3.connect(database) as connection:
        assert connection.execute(
            "SELECT from_entity_id,to_entity_id,relation_type,strength FROM pk_edge"
        ).fetchone() == (
            "doc:DESIGN-DOC",
            "doc:REQ-DOC",
            "SATISFIES",
            "strong",
        )
        assert connection.execute(
            "SELECT priority,requirement_status FROM pk_requirement WHERE requirement_id='REQ-1'"
        ).fetchone() == ("P0", "approved")
        assert connection.execute(
            "SELECT requirement_id,display_order FROM pk_acceptance_criterion "
            "WHERE acceptance_id='REQ-1-AC-1'"
        ).fetchone() == ("REQ-1", 1)
        assert connection.execute("SELECT COUNT(*) FROM pk_work_item").fetchone()[0] == 1

    payload = json.loads(relations.read_text(encoding="utf-8"))
    payload["relations"][0]["to_entity_id"] = "doc:MISSING"
    relations.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="missing relation endpoint"):
        indexer.refresh(as_of="2026-07-22T00:00:01Z")
