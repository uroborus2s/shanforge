from __future__ import annotations

import ast
import hashlib
import json
import sqlite3
from pathlib import Path

from domain.project_knowledge.models import AccessClass, SourceDefinition
from runtime.project_knowledge.extractors import default_extractors
from runtime.project_knowledge.site_renderer import ProjectSiteRenderer
from settings.project_knowledge.pm_projection import SQLiteSiteDataStore
from settings.project_knowledge.schema import create_schema
from settings.project_knowledge.sqlite_index import SQLiteProjectKnowledgeIndex

ROOT = Path(__file__).resolve().parents[1]


def test_application_project_knowledge_has_no_concrete_runtime_or_settings_imports() -> None:
    violations: list[str] = []
    for path in sorted((ROOT / "src/application/project_knowledge").glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            module = ""
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith(("runtime.", "settings.")):
                        violations.append(f"{path.name}:{alias.name}")
            if module.startswith(("runtime.", "settings.")):
                violations.append(f"{path.name}:{module}")
    assert violations == []


def test_shared_restricted_static_model_excludes_project_and_restricted_facts(
    tmp_path: Path,
) -> None:
    database = tmp_path / "knowledge.sqlite3"
    with sqlite3.connect(database) as connection:
        create_schema(connection)
        connection.execute(
            "INSERT INTO pk_generation(generation_id,status,source_root_sha256,schema_version,"
            "created_at) VALUES('g1','current',?,1,'2026-07-22T00:00:00Z')",
            ("a" * 64,),
        )
        for source_id, access in (
            ("source-public", "public"),
            ("source-project", "project"),
            ("source-restricted", "restricted"),
        ):
            connection.execute(
                "INSERT INTO pk_source(source_id,registry_source_id,kind,relative_path,"
                "extractor_id,registry_version,authority_rank,access_class,enabled,config_json) "
                "VALUES(?,?, 'markdown', ?, 'markdown-v1','1',100,?,1,'{}')",
                (source_id, source_id, f"docs/{source_id}.md", access),
            )
            artifact_id = f"artifact-{source_id}"
            connection.execute(
                "INSERT INTO pk_artifact(artifact_id,source_id,artifact_kind,relative_path,"
                "content_sha256,semantic_sha256,access_class) VALUES(?,?, 'document', ?,?,?,?)",
                (
                    artifact_id,
                    source_id,
                    f"docs/{source_id}.md",
                    hashlib.sha256(source_id.encode()).hexdigest(),
                    hashlib.sha256(f"semantic-{source_id}".encode()).hexdigest(),
                    access,
                ),
            )
            connection.execute(
                "INSERT INTO pk_entity(entity_id,entity_kind,display_name,lifecycle_status,"
                "primary_artifact_id,semantic_sha256) VALUES(?, 'document', ?, 'active', ?, ?)",
                (
                    f"entity-{source_id}",
                    f"{access} fact",
                    artifact_id,
                    hashlib.sha256(f"entity-{source_id}".encode()).hexdigest(),
                ),
            )
    store = SQLiteSiteDataStore(database)
    owner = store.load(profile="local-owner")
    shared = store.load(profile="shared-restricted")

    assert {item["display_name"] for item in owner["entities"]} == {
        "public fact",
        "project fact",
        "restricted fact",
    }
    assert [item["display_name"] for item in shared["entities"]] == ["public fact"]
    assert shared["pm"] == {table: [] for table in shared["pm"]}
    assert shared["project"]["name"] == "受限项目视图"


def test_temporary_index_cleanup_rejects_symlink(tmp_path: Path) -> None:
    from settings.composition.project_knowledge import _clear_rebuild_family

    database = tmp_path / "project-knowledge.sqlite3"
    temporary = tmp_path / "project-knowledge.sqlite3.rebuild"
    outside = tmp_path / "outside"
    outside.write_text("do not touch", encoding="utf-8")
    temporary.symlink_to(outside)

    try:
        _clear_rebuild_family(temporary, database)
    except ValueError as error:
        assert "symlink" in str(error)
    else:  # pragma: no cover - assertion branch
        raise AssertionError("symlink rebuild target was accepted")
    assert outside.read_text(encoding="utf-8") == "do not touch"


def test_sensitive_values_never_reach_contribution_sqlite_or_html(tmp_path: Path) -> None:
    secret_token = "sk-abcdefghijklmnop1234"
    password = "never-store-me-123"
    content = (
        json.dumps(
            {
                "event_uid": "event-1",
                "work_item": "TASK-1",
                "status": "in_progress",
                "summary": f"验证凭据 {secret_token}",
                "password": password,
                "next_action": "继续验证",
            }
        )
        + "\n"
    ).encode()
    source = SourceDefinition(
        source_id="source-ledger",
        registry_source_id="SRC-WORKITEM-LEDGER",
        kind="jsonl",
        relative_path=".factory/workitems/example/ledger.jsonl",
        extractor_id="jsonl-v3",
        registry_version="1",
        authority_rank=100,
        access_class=AccessClass.PROJECT,
        config={"max_file_bytes": 100000},
    )
    contribution = default_extractors().extract(source, content)
    serialized = json.dumps(contribution, ensure_ascii=False)
    assert secret_token not in serialized
    assert password not in serialized
    assert "[REDACTED]" in serialized

    database = tmp_path / "knowledge.sqlite3"
    index = SQLiteProjectKnowledgeIndex(database)
    index.publish(
        sources=(source,),
        contributions={source.source_id: contribution},
        content_hashes={source.source_id: hashlib.sha256(content).hexdigest()},
        stats={source.source_id: (len(content), 1)},
        as_of="2026-07-22T00:00:00Z",
        git_commit="head-1",
    )
    with sqlite3.connect(database) as connection:
        dump = "\n".join(connection.iterdump())
    assert secret_token not in dump
    assert password not in dump

    model = SQLiteSiteDataStore(database).load(profile="local-owner")
    pages = ProjectSiteRenderer().render(model, profile="local-owner").pages
    html = "\n".join(pages.values())
    assert secret_token not in html
    assert password not in html
    assert "[REDACTED]" in html
