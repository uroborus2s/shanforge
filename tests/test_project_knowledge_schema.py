from __future__ import annotations

import sqlite3

import pytest

from settings.project_knowledge.schema import (
    CORE_TABLES,
    FTS_TABLES,
    PM_TABLES,
    create_schema,
    validate_schema,
)


def memory_database() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.execute("PRAGMA foreign_keys = ON")
    create_schema(connection)
    return connection


def test_schema_declares_exactly_29_core_10_pm_and_2_fts_tables() -> None:
    assert len(CORE_TABLES) == 29
    assert len(PM_TABLES) == 10
    assert len(FTS_TABLES) == 2
    assert len(set(CORE_TABLES) | set(PM_TABLES)) == 39
    assert FTS_TABLES == ("pk_search_fts", "pk_search_tri")
    report = validate_schema(memory_database())
    assert report.core_tables == CORE_TABLES
    assert report.pm_tables == PM_TABLES
    assert report.fts_tables == FTS_TABLES


def test_schema_enforces_foreign_keys_and_single_current_generation() -> None:
    connection = memory_database()
    with pytest.raises(sqlite3.IntegrityError):
        connection.execute(
            "INSERT INTO pk_source_state(source_id,size_bytes,mtime_ns,parse_status) "
            "VALUES ('missing',0,0,'parsed')"
        )
    connection.execute(
        "INSERT INTO pk_generation(generation_id,status,schema_version,created_at) "
        "VALUES ('g1','current',1,'2026-07-22T00:00:00Z')"
    )
    with pytest.raises(sqlite3.IntegrityError):
        connection.execute(
            "INSERT INTO pk_generation(generation_id,status,schema_version,created_at) "
            "VALUES ('g2','current',1,'2026-07-22T00:00:01Z')"
        )


def test_schema_rejects_invalid_alias_and_oversized_current_memory() -> None:
    connection = memory_database()
    with pytest.raises(sqlite3.IntegrityError):
        connection.execute(
            "INSERT INTO pk_entity_alias(alias_entity_id,canonical_entity_id,reason) "
            "VALUES ('same','same','invalid')"
        )
    with pytest.raises(sqlite3.IntegrityError):
        connection.execute(
            "INSERT INTO pk_memory_checkpoint("
            "checkpoint_id,project_id,facts_high_watermark,schema_id,size_bytes,"
            "content_sha256,is_current) VALUES (?,?,?,?,?,?,?)",
            ("memory:1", "shanforge", 1, "MemoryCheckpoint/v1", 8193, "a" * 64, 1),
        )


def test_requirement_section_reference_uses_hashed_section_key() -> None:
    connection = memory_database()
    connection.execute(
        "INSERT INTO pk_entity(entity_id,entity_kind,display_name,lifecycle_status) "
        "VALUES ('entity:req','requirement','Requirement','active')"
    )
    with pytest.raises(sqlite3.IntegrityError):
        connection.execute(
            "INSERT INTO pk_requirement("
            "requirement_id,entity_id,requirement_status,source_section_key) "
            "VALUES ('REQ-1','entity:req','approved','mdsec:missing')"
        )
