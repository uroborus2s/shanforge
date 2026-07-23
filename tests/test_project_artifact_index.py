from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path
from typing import Any

import pytest

from domain.project_knowledge.models import (
    AccessClass,
    SourceDefinition,
    canonical_json,
    stable_id,
)
from settings.composition.project_knowledge import _git_head
from settings.project_knowledge.sqlite_index import SQLiteProjectKnowledgeIndex


def _source() -> SourceDefinition:
    return SourceDefinition(
        source_id="source:test-catalog",
        registry_source_id="SRC-TEST-CASE-ARTIFACTS",
        kind="yaml",
        relative_path="tests/specifications/example.testcases.yaml",
        extractor_id="project-artifact-yaml-v1",
        registry_version="1",
        authority_rank=100,
        access_class=AccessClass.PROJECT,
        config={"max_file_bytes": 100000},
    )


def _contribution(*, code_symbol_id: str | None = None) -> dict[str, Any]:
    entity_id = "TEST-API-PROJECT-STATUS-001"
    content_sha = hashlib.sha256(b"catalog").hexdigest()
    semantic = hashlib.sha256(entity_id.encode()).hexdigest()
    return {
        "schema_id": "SourceContribution/v1",
        "source_id": "source:test-catalog",
        "registry_source_id": "SRC-TEST-CASE-ARTIFACTS",
        "source_kind": "yaml",
        "relative_path": "tests/specifications/example.testcases.yaml",
        "extractor_id": "project-artifact-yaml-v1",
        "registry_version": "1",
        "authority_rank": 100,
        "size_bytes": 7,
        "content_sha256": content_sha,
        "artifact": {
            "artifact_id": stable_id("artifact", "test-catalog"),
            "artifact_kind": "yaml",
            "relative_path": "tests/specifications/example.testcases.yaml",
            "content_sha256": content_sha,
            "semantic_sha256": semantic,
            "access_class": "project",
        },
        "entities": [
            {
                "entity_id": entity_id,
                "entity_kind": "test",
                "display_name": "项目状态接口合同校验",
                "summary": "确认接口合同和稳定追踪。",
                "lifecycle_status": "active",
                "semantic_sha256": semantic,
                "definition": True,
                "details": {"definition_status": "active"},
            }
        ],
        "locators": [],
        "search": [],
        "diagnostics": [],
        "relations": [],
        "tests": [
            {
                "test_id": entity_id,
                "entity_id": entity_id,
                "code_symbol_id": code_symbol_id,
                "framework": "catalog",
                "test_kind": "contract",
                "test_status": "definition:active",
                "last_evidence_entity_id": None,
            }
        ],
    }


def _publish(
    index: SQLiteProjectKnowledgeIndex,
    contribution: dict[str, Any],
    *,
    as_of: str,
) -> dict[str, str]:
    source = _source()
    serialized = canonical_json(contribution)
    return index.publish(
        sources=(source,),
        contributions={source.source_id: contribution},
        content_hashes={source.source_id: hashlib.sha256(serialized.encode()).hexdigest()},
        stats={source.source_id: (len(serialized), 1)},
        as_of=as_of,
        git_commit="head",
    )


def test_catalog_test_is_projected_as_definition_not_execution_result(
    tmp_path: Path,
) -> None:
    database = tmp_path / "knowledge.sqlite3"
    index = SQLiteProjectKnowledgeIndex(database)

    _publish(index, _contribution(), as_of="2026-07-23T10:00:00Z")

    with sqlite3.connect(database) as connection:
        row = connection.execute(
            "SELECT framework,test_kind,test_status,code_symbol_id,"
            "last_evidence_entity_id FROM pk_test WHERE test_id=?",
            ("TEST-API-PROJECT-STATUS-001",),
        ).fetchone()
    assert row == ("catalog", "contract", "definition:active", None, None)


def test_invalid_catalog_projection_rolls_back_generation_and_test_rows(
    tmp_path: Path,
) -> None:
    database = tmp_path / "knowledge.sqlite3"
    index = SQLiteProjectKnowledgeIndex(database)
    first = _publish(index, _contribution(), as_of="2026-07-23T10:00:00Z")

    with pytest.raises(sqlite3.IntegrityError):
        _publish(
            index,
            _contribution(code_symbol_id="missing-code-symbol"),
            as_of="2026-07-23T10:01:00Z",
        )

    with sqlite3.connect(database) as connection:
        generation = connection.execute(
            "SELECT generation_id FROM pk_generation WHERE status='current'"
        ).fetchone()[0]
        tests = connection.execute(
            "SELECT test_id,test_status FROM pk_test ORDER BY test_id"
        ).fetchall()
    assert generation == first["generation_id"]
    assert tests == [("TEST-API-PROJECT-STATUS-001", "definition:active")]


def test_git_head_reads_linked_worktree_gitdir(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    git_dir = tmp_path / "git-admin" / "worktrees" / "candidate"
    project_root.mkdir()
    git_dir.mkdir(parents=True)
    (project_root / ".git").write_text(f"gitdir: {git_dir}\n", encoding="utf-8")
    (git_dir / "HEAD").write_text("detached-candidate\n", encoding="utf-8")

    assert _git_head(project_root) == "detached-candidate"
