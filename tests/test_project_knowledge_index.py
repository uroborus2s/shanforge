from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path

import pytest

from application.project_knowledge.index_service import ProjectKnowledgeIndexService
from application.project_knowledge.query_service import ProjectKnowledgeQueryService, QueryFailure
from domain.project_knowledge.models import AccessClass, SourceDefinition, stable_id
from runtime.project_knowledge.extractors import default_extractors
from runtime.project_knowledge.site_renderer import ProjectSiteRenderer
from settings.project_knowledge.pm_projection import SQLiteSiteDataStore
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


@pytest.mark.parametrize("reference_kind", ["entity", "evidence_locator"])
def test_python_incremental_refresh_falls_back_for_foreign_key_references(
    tmp_path: Path, reference_kind: str
) -> None:
    source_root = tmp_path / "src"
    source_root.mkdir()
    python_source = source_root / "example.py"
    python_source.write_text("def run() -> int:\n    return 1\n", encoding="utf-8")
    relation_root = tmp_path / "relations"
    relation_root.mkdir()
    code_file_id = stable_id("codefile", ["src/example.py"])
    symbol_id = "py:src.example:run:function"
    python_definition = SourceDefinition(
        source_id="source:python:test",
        registry_source_id="SRC-PYTHON",
        kind="python",
        relative_path="src/example.py",
        extractor_id="python-ast-v1",
        registry_version="1",
        authority_rank=80,
        access_class=AccessClass.PROJECT,
    )
    python_contribution = default_extractors().extract(
        python_definition, python_source.read_bytes()
    )
    evidence_locator_id = str(python_contribution["locators"][0]["locator_id"])
    if reference_kind == "entity":
        relation = {
            "from_entity_id": code_file_id,
            "to_entity_id": symbol_id,
            "relation_type": "CONTAINS",
        }
        nodes: list[dict[str, str]] = []
    else:
        relation = {
            "from_entity_id": "external-source",
            "to_entity_id": "external-target",
            "relation_type": "EVIDENCES",
            "evidence_locator_id": evidence_locator_id,
        }
        nodes = [{"id": "external-source"}, {"id": "external-target"}]
    (relation_root / "code-map.json").write_text(
        json.dumps(
            {
                "schema_id": "ProjectKnowledgeRelationDeclarations/v1",
                "nodes": nodes,
                "relations": [relation],
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
                        "registry_source_id": "SRC-PYTHON",
                        "kind": "python",
                        "roots": ["src"],
                        "include": ["*.py"],
                        "exclude": [],
                        "extractor_id": "python-ast-v1",
                        "access_class": "project",
                        "authority_rank": 80,
                        "stable_id_policy": "ast-qualified-name",
                        "max_file_bytes": 100000,
                    },
                    {
                        "registry_source_id": "SRC-RELATION",
                        "kind": "json",
                        "roots": ["relations"],
                        "include": ["*.json"],
                        "exclude": [],
                        "extractor_id": "json-pointer-v1",
                        "access_class": "project",
                        "authority_rank": 100,
                        "stable_id_policy": "explicit_or_pointer",
                        "max_file_bytes": 100000,
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    indexer, database = service(tmp_path, registry_path)
    indexer.refresh(as_of="2026-07-22T00:00:00Z", git_commit="head")

    python_source.write_text("def run() -> int:\n    return 2\n", encoding="utf-8")
    refreshed = indexer.refresh(as_of="2026-07-22T00:00:01Z", git_commit="head")

    assert refreshed.parsed_count == 1
    with sqlite3.connect(database) as connection:
        assert connection.execute("SELECT COUNT(*) FROM pk_edge").fetchone()[0] == 1
        assert connection.execute(
            "SELECT COUNT(*) FROM pk_code_symbol WHERE symbol_id=?", (symbol_id,)
        ).fetchone()[0] == 1


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


def test_markdown_requirement_sections_populate_source_binding_and_criterion_status(
    tmp_path: Path,
) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "prd.md").write_text(
        """<!-- sf:document-id=PRD-1 -->
# 产品需求

<!-- sf:section-id=REQ-PKI-001 -->
## REQ-PKI-001：确定性项目快照

- 分类：项目查看与管理
- 优先级：P0
- 状态：已批准（v4.1.0）
- 用户故事：作为项目负责人，我希望快速获得当前项目快照。
- 需求规则 1：输入不变时复用最后有效站点。
- `REQ-PKI-001-AC-1`：缓存命中时不得重写 HTML。

<!-- sf:section-id=NFR-PKI-001 -->
## NFR-PKI-001：会话恢复

- 分类：性能与上下文
- 状态：已批准（v4.1.0）
- 度量目标：单记忆点不超过 8 KiB。
- 验证方式：使用事件夹具。
""",
        encoding="utf-8",
    )
    indexer, database = service(tmp_path, write_registry(tmp_path))

    indexer.refresh(as_of="2026-07-23T00:00:00Z")

    with sqlite3.connect(database) as connection:
        requirements = connection.execute(
            "SELECT requirement_id,requirement_status,source_section_key "
            "FROM pk_requirement ORDER BY requirement_id"
        ).fetchall()
        assert [row[0] for row in requirements] == ["NFR-PKI-001", "REQ-PKI-001"]
        assert all(row[1] == "approved" for row in requirements)
        assert all(str(row[2]).startswith("mdsec:") for row in requirements)
        assert connection.execute(
            "SELECT requirement_id,criterion_status FROM pk_acceptance_criterion "
            "WHERE acceptance_id='REQ-PKI-001-AC-1'"
        ).fetchone() == ("REQ-PKI-001", "approved")
        assert connection.execute(
            "SELECT s.relative_path,l.locator_kind,l.selector_json "
            "FROM pk_entity_locator el "
            "JOIN pk_locator l ON l.locator_id=el.locator_id "
            "JOIN pk_source s ON s.source_id=l.source_id "
            "WHERE el.entity_id='REQ-PKI-001' AND el.is_primary=1"
        ).fetchone() == (
            "docs/prd.md",
            "markdown_section",
            '{"block_sha256":"'
            + connection.execute(
                "SELECT block_sha256 FROM pk_document_section WHERE section_id='REQ-PKI-001'"
            ).fetchone()[0]
            + '","document_id":"PRD-1","estimated_bytes":'
            + str(
                json.loads(
                    connection.execute(
                        "SELECT l.selector_json FROM pk_entity_locator el "
                        "JOIN pk_locator l ON l.locator_id=el.locator_id "
                        "WHERE el.entity_id='REQ-PKI-001' AND el.is_primary=1"
                    ).fetchone()[0]
                )["estimated_bytes"]
            )
            + ',"kind":"markdown_section","section_id":"REQ-PKI-001"}',
        )


def test_warm_json_to_prd_migration_matches_cold_prd_rebuild(tmp_path: Path) -> None:
    legacy = tmp_path / "legacy"
    docs = tmp_path / "docs"
    legacy.mkdir()
    docs.mkdir()
    (legacy / "requirements.json").write_text(
        json.dumps(
            {
                "requirements": [
                    {
                        "id": "REQ-MIG-001",
                        "title": "迁移需求",
                        "status": "approved",
                        "priority": "P0",
                        "acceptance_criteria": [
                            {
                                "id": "REQ-MIG-001-AC-1",
                                "statement": "迁移后验收标准仍然存在。",
                                "status": "approved",
                            }
                        ],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    (docs / "prd.md").write_text(
        """<!-- sf:document-id=PRD-MIG -->
# 产品需求

<!-- sf:section-id=REQ-MIG-001 -->
## REQ-MIG-001：迁移需求

- 分类：迁移
- 优先级：P0
- 状态：已批准
- 用户故事：作为维护者，我希望迁移当前需求来源。
- 需求规则 1：当前需求必须从正式 PRD 提取。
- `REQ-MIG-001-AC-1`：迁移后验收标准仍然存在。
""",
        encoding="utf-8",
    )
    registry_path = tmp_path / "registry.json"
    legacy_registry = {
        "schema_id": "ProjectKnowledgeSourceRegistry/v1",
        "registry_version": "1",
        "sources": [
            {
                "registry_source_id": "SRC-LEGACY",
                "kind": "json",
                "roots": ["legacy"],
                "include": ["requirements.json"],
                "exclude": [],
                "extractor_id": "json-pointer-v5",
                "access_class": "project",
                "authority_rank": 90,
                "stable_id_policy": "json_pointer",
                "max_file_bytes": 100000,
            }
        ],
    }
    final_registry = {
        "schema_id": "ProjectKnowledgeSourceRegistry/v1",
        "registry_version": "2",
        "sources": [
            {
                "registry_source_id": "SRC-DOCS",
                "kind": "markdown",
                "roots": ["docs"],
                "include": ["*.md"],
                "exclude": [],
                "extractor_id": "markdown-v2",
                "access_class": "public",
                "authority_rank": 100,
                "stable_id_policy": "explicit_document_and_section_id",
                "max_file_bytes": 100000,
            }
        ],
    }
    registry_path.write_text(json.dumps(legacy_registry), encoding="utf-8")
    warm_database = tmp_path / "warm.sqlite3"

    def indexer(database: Path) -> ProjectKnowledgeIndexService:
        return ProjectKnowledgeIndexService(
            FileSourceRegistry(tmp_path, registry_path),
            SQLiteProjectKnowledgeIndex(database),
            default_extractors(),
        )

    indexer(warm_database).refresh(as_of="2026-07-23T00:00:00Z")
    registry_path.write_text(json.dumps(final_registry), encoding="utf-8")
    warm_result = indexer(warm_database).refresh(as_of="2026-07-23T00:00:01Z")
    assert warm_result.deleted_count == 1

    cold_database = tmp_path / "cold.sqlite3"
    indexer(cold_database).refresh(as_of="2026-07-23T00:00:01Z")

    semantic_queries = [
        "SELECT requirement_id,entity_id,priority,requirement_status,"
        "source_section_key FROM pk_requirement ORDER BY requirement_id",
        "SELECT acceptance_id,entity_id,requirement_id,display_order,statement,"
        "criterion_status FROM pk_acceptance_criterion ORDER BY acceptance_id",
        "SELECT document_id,section_id,parent_section_key,display_order,display_title,"
        "block_sha256 FROM pk_document_section ORDER BY document_id,display_order",
        "SELECT el.entity_id,l.locator_kind,l.selector_json,el.locator_role,el.is_primary "
        "FROM pk_entity_locator el JOIN pk_locator l ON l.locator_id=el.locator_id "
        "WHERE el.entity_id LIKE 'REQ-MIG-%' ORDER BY el.entity_id,l.locator_id",
        "SELECT from_entity_id,to_entity_id,relation_type,strength,confidence "
        "FROM pk_edge ORDER BY from_entity_id,to_entity_id,relation_type",
    ]
    with sqlite3.connect(warm_database) as warm_connection, sqlite3.connect(
        cold_database
    ) as cold_connection:
        for query in semantic_queries:
            assert warm_connection.execute(query).fetchall() == cold_connection.execute(
                query
            ).fetchall()
        assert warm_connection.execute(
            "SELECT source_section_key FROM pk_requirement "
            "WHERE requirement_id='REQ-MIG-001'"
        ).fetchone()[0]
        assert warm_connection.execute(
            "SELECT requirement_id,display_order,criterion_status "
            "FROM pk_acceptance_criterion WHERE acceptance_id='REQ-MIG-001-AC-1'"
        ).fetchone() == ("REQ-MIG-001", 1, "approved")


def test_ledger_status_and_task_brief_chinese_title_merge_by_stable_task_id(
    tmp_path: Path,
) -> None:
    work_items = tmp_path / "workitems"
    briefs = work_items / "task-briefs"
    briefs.mkdir(parents=True)
    (briefs / "TASK-1.md").write_text(
        """# PRD 与 Markdown 需求提取

## 工作项

- 任务：`TASK-1`
""",
        encoding="utf-8",
    )
    (work_items / "old-ledger.jsonl").write_text(
        '{"event":"started","task":"TASK-1","status":"in_progress",'
        '"ts":"2026-07-22T10:00:00+08:00","idempotency_key":"task-1-started"}\n',
        encoding="utf-8",
    )
    (work_items / "current-ledger.jsonl").write_text(
        '{"event":"verified","task":"TASK-1","status":"ready_for_review",'
        '"ts":"2026-07-23T10:00:00+08:00","idempotency_key":"task-1-verified"}\n',
        encoding="utf-8",
    )
    registry_path = tmp_path / "registry.json"
    registry_path.write_text(
        json.dumps(
            {
                "schema_id": "ProjectKnowledgeSourceRegistry/v1",
                "registry_version": "2",
                "sources": [
                    {
                        "registry_source_id": "SRC-WORKITEM-LEDGER",
                        "kind": "jsonl",
                        "roots": ["workitems"],
                        "include": ["*.jsonl"],
                        "exclude": [],
                        "extractor_id": "jsonl-event-v5",
                        "access_class": "project",
                        "authority_rank": 100,
                        "stable_id_policy": "task_id",
                        "max_file_bytes": 100000,
                    },
                    {
                        "registry_source_id": "SRC-WORKITEM-BRIEF",
                        "kind": "markdown",
                        "roots": ["workitems"],
                        "include": ["task-briefs/*.md"],
                        "exclude": [],
                        "extractor_id": "markdown-v2",
                        "access_class": "project",
                        "authority_rank": 90,
                        "stable_id_policy": "declared_task_id",
                        "max_file_bytes": 100000,
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    indexer, database = service(tmp_path, registry_path)

    indexer.refresh(as_of="2026-07-23T00:00:00Z")

    with sqlite3.connect(database) as connection:
        assert connection.execute(
            "SELECT display_name,lifecycle_status FROM pk_entity WHERE entity_id='TASK-1'"
        ).fetchone() == ("PRD 与 Markdown 需求提取", "ready_for_review")
        assert connection.execute(
            "SELECT task_status FROM pk_work_item WHERE work_item_id='TASK-1'"
        ).fetchone()[0] == "ready_for_review"
    pages = ProjectSiteRenderer().render(
        SQLiteSiteDataStore(database, project_root=tmp_path).load(profile="local-owner"),
        profile="local-owner",
    ).pages
    assert "PRD 与 Markdown 需求提取" in pages["tasks/index.html"]
    task_page = pages["tasks/TASK-1.html"]
    assert "<h1>PRD 与 Markdown 需求提取</h1>" in task_page
    assert "<dt>任务编号</dt><dd>TASK-1</dd>" in task_page
    assert "任务标题待补充" not in task_page


def test_jsonl_v4_to_v5_warm_migration_preserves_old_work_item_alias(
    tmp_path: Path,
) -> None:
    work_items = tmp_path / "workitems"
    work_items.mkdir()
    ledger = work_items / "ledger.jsonl"
    content = (
        '{"event":"started","task":"TASK-ALIAS-001","status":"in_progress",'
        '"ts":"2026-07-23T10:00:00+08:00","idempotency_key":"alias-started"}\n'
    ).encode()
    ledger.write_bytes(content)
    registry_path = tmp_path / "registry.json"

    def registry(extractor_id: str, registry_version: str) -> dict[str, object]:
        return {
            "schema_id": "ProjectKnowledgeSourceRegistry/v1",
            "registry_version": registry_version,
            "sources": [
                {
                    "registry_source_id": "SRC-WORKITEM-LEDGER",
                    "kind": "jsonl",
                    "roots": ["workitems"],
                    "include": ["*.jsonl"],
                    "exclude": [],
                    "extractor_id": extractor_id,
                    "access_class": "project",
                    "authority_rank": 100,
                    "stable_id_policy": "event_uid_or_task_id",
                    "max_file_bytes": 100000,
                }
            ],
        }

    registry_path.write_text(json.dumps(registry("jsonl-event-v4", "1")), encoding="utf-8")
    source_registry = FileSourceRegistry(tmp_path, registry_path)
    source_definition = source_registry.sources()[0]
    old_contribution = default_extractors().extract(source_definition, content)
    old_entity_id = stable_id(
        "workitem", [source_definition.source_id, "TASK-ALIAS-001"]
    )
    for entity in old_contribution["entities"]:
        if entity["entity_id"] == "TASK-ALIAS-001":
            entity["entity_id"] = old_entity_id
    for locator in old_contribution["locators"]:
        if locator["entity_id"] == "TASK-ALIAS-001":
            locator["entity_id"] = old_entity_id
    for search in old_contribution["search"]:
        if search["entity_id"] == "TASK-ALIAS-001":
            search["entity_id"] = old_entity_id
    old_contribution.pop("aliases", None)
    database = tmp_path / "knowledge.sqlite3"
    SQLiteProjectKnowledgeIndex(database).publish(
        sources=(source_definition,),
        contributions={source_definition.source_id: old_contribution},
        content_hashes={source_definition.source_id: hashlib.sha256(content).hexdigest()},
        stats={source_definition.source_id: source_registry.stat(source_definition)},
        as_of="2026-07-23T10:00:00+08:00",
        git_commit="legacy",
    )

    registry_path.write_text(json.dumps(registry("jsonl-event-v5", "2")), encoding="utf-8")
    refreshed = ProjectKnowledgeIndexService(
        FileSourceRegistry(tmp_path, registry_path),
        SQLiteProjectKnowledgeIndex(database),
        default_extractors(),
    ).refresh(as_of="2026-07-23T11:00:00+08:00")

    assert refreshed.parsed_count == 1
    with sqlite3.connect(database) as connection:
        assert connection.execute(
            "SELECT canonical_entity_id,reason FROM pk_entity_alias "
            "WHERE alias_entity_id=?",
            (old_entity_id,),
        ).fetchone() == (
            "TASK-ALIAS-001",
            "jsonl-v5 canonical work-item ID migration from source-scoped identity",
        )
        assert connection.execute(
            "SELECT COUNT(*) FROM pk_entity WHERE entity_id=?", (old_entity_id,)
        ).fetchone()[0] == 0
    assert (
        SQLiteKnowledgeQueryStore(database, tmp_path).resolve_alias(old_entity_id)
        == "TASK-ALIAS-001"
    )


def test_same_natural_work_item_label_in_two_ledgers_does_not_collide(
    tmp_path: Path,
) -> None:
    work_items = tmp_path / "workitems"
    work_items.mkdir()
    for name in ("a", "b"):
        (work_items / f"{name}.jsonl").write_text(
            '{"event":"started","task":"shared-label","status":"in_progress",'
            f'"idempotency_key":"{name}-started"}}\n',
            encoding="utf-8",
        )
    registry_path = tmp_path / "registry.json"
    registry_path.write_text(
        json.dumps(
            {
                "schema_id": "ProjectKnowledgeSourceRegistry/v1",
                "registry_version": "2",
                "sources": [
                    {
                        "registry_source_id": "SRC-WORKITEM-LEDGER",
                        "kind": "jsonl",
                        "roots": ["workitems"],
                        "include": ["*.jsonl"],
                        "exclude": [],
                        "extractor_id": "jsonl-event-v5",
                        "access_class": "project",
                        "authority_rank": 100,
                        "stable_id_policy": "event_uid_or_task_id",
                        "max_file_bytes": 100000,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    indexer, database = service(tmp_path, registry_path)

    indexer.refresh(as_of="2026-07-23T11:00:00+08:00")

    with sqlite3.connect(database) as connection:
        work_items = connection.execute(
            "SELECT work_item_id FROM pk_work_item ORDER BY work_item_id"
        ).fetchall()
        assert len(work_items) == 2
        assert all(str(row[0]).startswith("workitem:") for row in work_items)
