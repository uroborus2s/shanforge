from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path

import pytest

from application.project_knowledge.query_service import (
    ProjectKnowledgeQueryService,
    QueryFailure,
)
from settings.project_knowledge.query_store import SQLiteKnowledgeQueryStore
from settings.project_knowledge.schema import create_schema


def database(tmp_path: Path) -> tuple[Path, sqlite3.Connection]:
    path = tmp_path / "knowledge.sqlite3"
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys=ON")
    create_schema(connection)
    connection.execute(
        "INSERT INTO pk_generation(generation_id,status,schema_version,created_at) "
        "VALUES ('g1','current',1,'2026-07-22T00:00:00Z')"
    )
    return path, connection


def add_entity(connection: sqlite3.Connection, entity_id: str, name: str) -> None:
    connection.execute(
        "INSERT INTO pk_entity(entity_id,entity_kind,display_name,lifecycle_status) "
        "VALUES (?,?,?,?)",
        (entity_id, "requirement", name, "active"),
    )
    search_id = f"search:{entity_id}"
    cursor = connection.execute(
        "INSERT INTO pk_search_entry("
        "search_id,entity_id,title,summary,tags,access_class,content_sha256) "
        "VALUES (?,?,?,?,?,?,?)",
        (search_id, entity_id, name, "Project requirement", "requirement", "project", "a" * 64),
    )
    rowid = cursor.lastrowid
    connection.execute(
        "INSERT INTO pk_search_fts(rowid,search_id,title,summary,tags) VALUES (?,?,?,?,?)",
        (rowid, search_id, name, "Project requirement", "requirement"),
    )
    connection.execute(
        "INSERT INTO pk_search_tri(rowid,search_id,title,summary,tags) VALUES (?,?,?,?,?)",
        (rowid, search_id, name, "Project requirement", "requirement"),
    )


def test_find_show_trace_preserve_alias_and_multi_source_edges(tmp_path: Path) -> None:
    path, connection = database(tmp_path)
    add_entity(connection, "REQ-1", "项目知识索引")
    add_entity(connection, "TASK-1", "实现索引")
    connection.execute(
        "INSERT INTO pk_source("
        "source_id,registry_source_id,kind,relative_path,extractor_id,registry_version,"
        "authority_rank,access_class,enabled) VALUES (?,?,?,?,?,?,?,?,1)",
        ("s1", "R1", "json", "a.json", "json-v1", "1", 10, "project"),
    )
    connection.execute(
        "INSERT INTO pk_source("
        "source_id,registry_source_id,kind,relative_path,extractor_id,registry_version,"
        "authority_rank,access_class,enabled) VALUES (?,?,?,?,?,?,?,?,1)",
        ("s2", "R2", "json", "b.json", "json-v1", "1", 10, "project"),
    )
    connection.execute(
        "INSERT INTO pk_relation_type("
        "relation_type,strength_policy,is_transitive,description) "
        "VALUES ('IMPLEMENTS','formal',0,'x')"
    )
    for source_id in ("s1", "s2"):
        connection.execute(
            "INSERT INTO pk_edge("
            "edge_id,from_entity_id,to_entity_id,relation_type,source_id,strength,"
            "confidence,semantic_sha256) VALUES (?,?,?,?,?,?,?,?)",
            (
                f"edge:{source_id}",
                "TASK-1",
                "REQ-1",
                "IMPLEMENTS",
                source_id,
                "strong",
                1.0,
                "b" * 64,
            ),
        )
    connection.execute(
        "INSERT INTO pk_entity_alias(alias_entity_id,canonical_entity_id,reason) "
        "VALUES ('REQ-OLD','REQ-1','renamed')"
    )
    connection.commit()
    service = ProjectKnowledgeQueryService(SQLiteKnowledgeQueryStore(path, tmp_path))

    found = service.find("知识索引")
    assert found["items"][0]["entity_id"] == "REQ-1"
    shown = service.show("REQ-OLD")
    assert shown["entity"]["entity_id"] == "REQ-1"
    traced = service.trace("TASK-1", depth=2)
    assert len(traced["edges"]) == 2
    assert {edge["source_id"] for edge in traced["edges"]} == {"s1", "s2"}


def test_alias_cycle_and_ambiguous_locator_fail_with_exit_four(tmp_path: Path) -> None:
    path, connection = database(tmp_path)
    add_entity(connection, "A", "A")
    add_entity(connection, "B", "B")
    connection.execute(
        "INSERT INTO pk_entity_alias(alias_entity_id,canonical_entity_id,reason) "
        "VALUES ('A','B','loop')"
    )
    connection.execute(
        "INSERT INTO pk_entity_alias(alias_entity_id,canonical_entity_id,reason) "
        "VALUES ('B','A','loop')"
    )
    docs = tmp_path / "docs"
    docs.mkdir()
    source_path = docs / "ambiguous.md"
    source_path.write_text(
        "<!-- sf:section-id=SEC-1 -->\n# First\n\n<!-- sf:section-id=SEC-1 -->\n## Second\n",
        encoding="utf-8",
    )
    connection.execute(
        "INSERT INTO pk_source("
        "source_id,registry_source_id,kind,relative_path,extractor_id,registry_version,"
        "authority_rank,access_class,enabled) VALUES (?,?,?,?,?,?,?,?,1)",
        ("source-doc", "DOC", "markdown", "docs/ambiguous.md", "markdown-v1", "1", 1, "project"),
    )
    connection.execute(
        "INSERT INTO pk_source_state(source_id,size_bytes,mtime_ns,parse_status) VALUES (?,?,?,?)",
        ("source-doc", source_path.stat().st_size, source_path.stat().st_mtime_ns, "parsed"),
    )
    selector = {"kind": "markdown_section", "document_id": "DOC-1", "section_id": "SEC-1"}
    selector_json = json.dumps(selector, sort_keys=True, separators=(",", ":"))
    connection.execute(
        "INSERT INTO pk_locator("
        "locator_id,locator_kind,selector_json,selector_sha256,source_id,validation_state) "
        "VALUES (?,?,?,?,?,'valid')",
        (
            "locator-1",
            "markdown_section",
            selector_json,
            hashlib.sha256(selector_json.encode()).hexdigest(),
            "source-doc",
        ),
    )
    connection.execute(
        "INSERT INTO pk_entity_locator(entity_id,locator_id,locator_role,confidence,is_primary) "
        "VALUES ('A','locator-1','definition',1,1)"
    )
    connection.commit()
    service = ProjectKnowledgeQueryService(SQLiteKnowledgeQueryStore(path, tmp_path))

    with pytest.raises(QueryFailure) as alias_error:
        service.show("A")
    assert alias_error.value.exit_code == 4
    connection.execute("DELETE FROM pk_entity_alias")
    connection.commit()
    with pytest.raises(QueryFailure) as locator_error:
        service.context("A")
    assert locator_error.value.exit_code == 4
    assert locator_error.value.code == "LOCATOR_AMBIGUOUS"


def test_context_returns_a_bounded_read_plan_without_body(tmp_path: Path) -> None:
    path, connection = database(tmp_path)
    add_entity(connection, "E", "Entity")
    for index in range(5):
        relative = f"docs/{index}.md"
        target = tmp_path / relative
        target.parent.mkdir(exist_ok=True)
        target.write_text(f"<!-- sf:section-id=root -->\n# File {index}\n", encoding="utf-8")
        source_id = f"s{index}"
        connection.execute(
            "INSERT INTO pk_source("
            "source_id,registry_source_id,kind,relative_path,extractor_id,registry_version,"
            "authority_rank,access_class,enabled) VALUES (?,?,?,?,?,?,?,?,1)",
            (source_id, "DOC", "markdown", relative, "markdown-v1", "1", 1, "project"),
        )
        connection.execute(
            "INSERT INTO pk_source_state(source_id,size_bytes,mtime_ns,parse_status) "
            "VALUES (?,?,0,'parsed')",
            (source_id, target.stat().st_size),
        )
        selector = {"kind": "markdown_section", "document_id": f"D{index}", "section_id": "root"}
        encoded = json.dumps(selector, sort_keys=True, separators=(",", ":"))
        locator_id = f"l{index}"
        connection.execute(
            "INSERT INTO pk_locator("
            "locator_id,locator_kind,selector_json,selector_sha256,source_id,validation_state) "
            "VALUES (?,?,?,?,?,'valid')",
            (
                locator_id,
                "markdown_section",
                encoded,
                hashlib.sha256(encoded.encode()).hexdigest(),
                source_id,
            ),
        )
        connection.execute(
            "INSERT INTO pk_entity_locator("
            "entity_id,locator_id,locator_role,confidence,is_primary) "
            "VALUES (?,?,?,?,?)",
            ("E", locator_id, f"evidence-{index}", 1.0, 0),
        )
    connection.commit()
    service = ProjectKnowledgeQueryService(SQLiteKnowledgeQueryStore(path, tmp_path))
    plan = service.context("E")
    assert len(plan["files"]) == 4
    assert plan["total_bytes"] <= 32 * 1024
    assert "# File" not in json.dumps(plan)
