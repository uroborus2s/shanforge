"""Versioned SQLite schema and R009 PM field-map validation."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any

CORE_TABLES = (
    "pk_meta",
    "pk_source",
    "pk_source_state",
    "pk_generation",
    "pk_generation_source",
    "pk_artifact",
    "pk_entity",
    "pk_entity_alias",
    "pk_locator",
    "pk_entity_locator",
    "pk_relation_type",
    "pk_edge",
    "pk_document",
    "pk_document_section",
    "pk_document_revision",
    "pk_module",
    "pk_code_file",
    "pk_code_symbol",
    "pk_requirement",
    "pk_acceptance_criterion",
    "pk_work_item",
    "pk_test",
    "pk_memory_checkpoint",
    "pk_search_entry",
    "pk_search_fts",
    "pk_search_tri",
    "pk_diagnostic",
    "pk_cache_entry",
    "pk_render_view",
)

FTS_TABLES = ("pk_search_fts", "pk_search_tri")

PM_TABLES = (
    "pm_project_profile",
    "pm_party",
    "pm_work_plan",
    "pm_risk",
    "pm_communication",
    "pm_meeting",
    "pm_action_item",
    "pm_status_report",
    "pm_change_request",
    "pm_project_summary",
)

_PM_COMMON = """
    generation_id TEXT,
    source_manifest_sha256 TEXT,
    row_sha256 TEXT,
    field_values_json TEXT NOT NULL DEFAULT '{}'
"""


DDL = f"""
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS pk_generation (
    generation_id TEXT PRIMARY KEY,
    parent_generation_id TEXT REFERENCES pk_generation(generation_id),
    status TEXT NOT NULL CHECK(status IN ('building','current','previous','failed')),
    source_root_sha256 TEXT,
    facts_high_watermark INTEGER,
    git_commit TEXT,
    as_of TEXT,
    schema_version INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    published_at TEXT
);
CREATE UNIQUE INDEX IF NOT EXISTS pk_generation_one_current
    ON pk_generation(status) WHERE status = 'current';
CREATE TABLE IF NOT EXISTS pk_meta (
    meta_key TEXT PRIMARY KEY,
    value_json TEXT NOT NULL,
    value_sha256 TEXT NOT NULL,
    updated_generation_id TEXT REFERENCES pk_generation(generation_id)
);
CREATE TABLE IF NOT EXISTS pk_source (
    source_id TEXT PRIMARY KEY,
    registry_source_id TEXT NOT NULL,
    kind TEXT NOT NULL,
    relative_path TEXT NOT NULL,
    extractor_id TEXT NOT NULL,
    registry_version TEXT NOT NULL,
    authority_rank INTEGER NOT NULL CHECK(authority_rank >= 0),
    access_class TEXT NOT NULL CHECK(access_class IN ('public','project','restricted')),
    enabled INTEGER NOT NULL DEFAULT 1 CHECK(enabled IN (0,1)),
    config_json TEXT NOT NULL DEFAULT '{{}}',
    UNIQUE(registry_source_id, relative_path)
);
CREATE INDEX IF NOT EXISTS pk_source_kind_enabled ON pk_source(enabled, kind);
CREATE TABLE IF NOT EXISTS pk_source_state (
    source_id TEXT PRIMARY KEY REFERENCES pk_source(source_id),
    content_sha256 TEXT,
    size_bytes INTEGER NOT NULL CHECK(size_bytes >= 0),
    mtime_ns INTEGER NOT NULL CHECK(mtime_ns >= 0),
    parse_status TEXT NOT NULL,
    last_generation_id TEXT REFERENCES pk_generation(generation_id),
    error_digest TEXT
);
CREATE TABLE IF NOT EXISTS pk_generation_source (
    generation_id TEXT NOT NULL REFERENCES pk_generation(generation_id),
    source_id TEXT NOT NULL REFERENCES pk_source(source_id),
    content_sha256 TEXT NOT NULL,
    contribution_sha256 TEXT NOT NULL,
    contribution_json TEXT NOT NULL,
    parse_status TEXT NOT NULL,
    PRIMARY KEY(generation_id, source_id)
);
CREATE INDEX IF NOT EXISTS pk_generation_source_lookup
    ON pk_generation_source(source_id, generation_id);
CREATE TABLE IF NOT EXISTS pk_artifact (
    artifact_id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL REFERENCES pk_source(source_id),
    artifact_kind TEXT NOT NULL,
    relative_path TEXT NOT NULL,
    content_sha256 TEXT NOT NULL,
    semantic_sha256 TEXT NOT NULL,
    access_class TEXT NOT NULL,
    revision_ref TEXT,
    UNIQUE(source_id, relative_path)
);
CREATE TABLE IF NOT EXISTS pk_entity (
    entity_id TEXT PRIMARY KEY,
    entity_kind TEXT NOT NULL,
    display_name TEXT NOT NULL,
    summary TEXT,
    lifecycle_status TEXT NOT NULL,
    primary_artifact_id TEXT REFERENCES pk_artifact(artifact_id),
    semantic_sha256 TEXT,
    detail_json TEXT NOT NULL DEFAULT '{{}}'
);
CREATE INDEX IF NOT EXISTS pk_entity_lookup
    ON pk_entity(entity_kind, lifecycle_status, display_name);
CREATE TABLE IF NOT EXISTS pk_entity_alias (
    alias_entity_id TEXT PRIMARY KEY,
    canonical_entity_id TEXT NOT NULL REFERENCES pk_entity(entity_id),
    reason TEXT NOT NULL,
    source_id TEXT REFERENCES pk_source(source_id),
    created_generation_id TEXT REFERENCES pk_generation(generation_id),
    CHECK(alias_entity_id <> canonical_entity_id)
);
CREATE TABLE IF NOT EXISTS pk_locator (
    locator_id TEXT PRIMARY KEY,
    locator_kind TEXT NOT NULL,
    selector_json TEXT NOT NULL,
    selector_sha256 TEXT NOT NULL,
    source_id TEXT NOT NULL REFERENCES pk_source(source_id),
    validation_state TEXT NOT NULL,
    UNIQUE(locator_kind, selector_sha256)
);
CREATE TABLE IF NOT EXISTS pk_entity_locator (
    entity_id TEXT NOT NULL REFERENCES pk_entity(entity_id),
    locator_id TEXT NOT NULL REFERENCES pk_locator(locator_id),
    locator_role TEXT NOT NULL,
    confidence REAL NOT NULL CHECK(confidence >= 0 AND confidence <= 1),
    is_primary INTEGER NOT NULL CHECK(is_primary IN (0,1)),
    PRIMARY KEY(entity_id, locator_id, locator_role)
);
CREATE UNIQUE INDEX IF NOT EXISTS pk_entity_locator_one_primary
    ON pk_entity_locator(entity_id, locator_role) WHERE is_primary = 1;
CREATE TABLE IF NOT EXISTS pk_relation_type (
    relation_type TEXT PRIMARY KEY,
    inverse_type TEXT REFERENCES pk_relation_type(relation_type),
    strength_policy TEXT NOT NULL,
    is_transitive INTEGER NOT NULL CHECK(is_transitive IN (0,1)),
    description TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS pk_edge (
    edge_id TEXT PRIMARY KEY,
    from_entity_id TEXT NOT NULL REFERENCES pk_entity(entity_id),
    to_entity_id TEXT NOT NULL REFERENCES pk_entity(entity_id),
    relation_type TEXT NOT NULL REFERENCES pk_relation_type(relation_type),
    source_id TEXT NOT NULL REFERENCES pk_source(source_id),
    strength TEXT NOT NULL CHECK(strength IN ('strong','weak')),
    confidence REAL NOT NULL CHECK(confidence >= 0 AND confidence <= 1),
    evidence_locator_id TEXT REFERENCES pk_locator(locator_id),
    semantic_sha256 TEXT NOT NULL,
    UNIQUE(from_entity_id,to_entity_id,relation_type,source_id,evidence_locator_id)
);
CREATE TABLE IF NOT EXISTS pk_document (
    document_id TEXT PRIMARY KEY,
    entity_id TEXT NOT NULL UNIQUE REFERENCES pk_entity(entity_id),
    artifact_id TEXT NOT NULL UNIQUE REFERENCES pk_artifact(artifact_id),
    title TEXT NOT NULL,
    chinese_name TEXT,
    audience TEXT,
    owner TEXT,
    doc_status TEXT NOT NULL,
    doc_version TEXT
);
CREATE TABLE IF NOT EXISTS pk_document_section (
    section_key TEXT PRIMARY KEY,
    document_id TEXT NOT NULL REFERENCES pk_document(document_id),
    section_id TEXT NOT NULL,
    entity_id TEXT NOT NULL UNIQUE REFERENCES pk_entity(entity_id),
    parent_section_key TEXT REFERENCES pk_document_section(section_key),
    source_id TEXT NOT NULL REFERENCES pk_source(source_id),
    display_title TEXT NOT NULL,
    display_order INTEGER NOT NULL,
    block_sha256 TEXT NOT NULL,
    safe_excerpt TEXT,
    UNIQUE(document_id, section_id)
);
CREATE TABLE IF NOT EXISTS pk_document_revision (
    document_id TEXT NOT NULL REFERENCES pk_document(document_id),
    git_commit TEXT NOT NULL,
    blob_sha256 TEXT NOT NULL,
    content_sha256 TEXT NOT NULL,
    doc_version TEXT,
    observed_generation_id TEXT REFERENCES pk_generation(generation_id),
    PRIMARY KEY(document_id, git_commit)
);
CREATE TABLE IF NOT EXISTS pk_module (
    module_id TEXT PRIMARY KEY,
    entity_id TEXT NOT NULL UNIQUE REFERENCES pk_entity(entity_id),
    layer_name TEXT NOT NULL
        CHECK(layer_name IN ('access','application','domain','runtime','settings')),
    root_path TEXT NOT NULL UNIQUE,
    owner TEXT,
    boundary_sha256 TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS pk_code_file (
    code_file_id TEXT PRIMARY KEY,
    entity_id TEXT NOT NULL UNIQUE REFERENCES pk_entity(entity_id),
    artifact_id TEXT NOT NULL UNIQUE REFERENCES pk_artifact(artifact_id),
    module_id TEXT REFERENCES pk_module(module_id),
    language TEXT NOT NULL,
    import_name TEXT
);
CREATE TABLE IF NOT EXISTS pk_code_symbol (
    symbol_id TEXT PRIMARY KEY,
    entity_id TEXT NOT NULL UNIQUE REFERENCES pk_entity(entity_id),
    code_file_id TEXT NOT NULL REFERENCES pk_code_file(code_file_id),
    symbol_kind TEXT NOT NULL,
    qualified_name TEXT NOT NULL,
    signature_text TEXT,
    visibility TEXT NOT NULL,
    semantic_sha256 TEXT NOT NULL,
    UNIQUE(code_file_id, qualified_name, symbol_kind)
);
CREATE TABLE IF NOT EXISTS pk_requirement (
    requirement_id TEXT PRIMARY KEY,
    entity_id TEXT NOT NULL UNIQUE REFERENCES pk_entity(entity_id),
    priority TEXT,
    requirement_status TEXT NOT NULL,
    owner TEXT,
    source_section_key TEXT REFERENCES pk_document_section(section_key)
);
CREATE TABLE IF NOT EXISTS pk_acceptance_criterion (
    acceptance_id TEXT PRIMARY KEY,
    entity_id TEXT NOT NULL UNIQUE REFERENCES pk_entity(entity_id),
    requirement_id TEXT NOT NULL REFERENCES pk_requirement(requirement_id),
    display_order INTEGER NOT NULL,
    statement TEXT NOT NULL,
    criterion_status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS pk_work_item (
    work_item_id TEXT PRIMARY KEY,
    entity_id TEXT NOT NULL UNIQUE REFERENCES pk_entity(entity_id),
    parent_work_item_id TEXT REFERENCES pk_work_item(work_item_id),
    task_kind TEXT NOT NULL,
    task_status TEXT NOT NULL,
    completion_level TEXT,
    ledger_locator_id TEXT REFERENCES pk_locator(locator_id),
    CHECK(parent_work_item_id IS NULL OR parent_work_item_id <> work_item_id)
);
CREATE TABLE IF NOT EXISTS pk_test (
    test_id TEXT PRIMARY KEY,
    entity_id TEXT NOT NULL UNIQUE REFERENCES pk_entity(entity_id),
    code_symbol_id TEXT REFERENCES pk_code_symbol(symbol_id),
    framework TEXT NOT NULL,
    test_kind TEXT NOT NULL,
    test_status TEXT NOT NULL,
    last_evidence_entity_id TEXT REFERENCES pk_entity(entity_id)
);
CREATE TABLE IF NOT EXISTS pk_memory_checkpoint (
    checkpoint_id TEXT PRIMARY KEY,
    entity_id TEXT REFERENCES pk_entity(entity_id),
    project_id TEXT NOT NULL,
    task_id TEXT,
    gate_id TEXT,
    facts_high_watermark INTEGER NOT NULL,
    schema_id TEXT NOT NULL,
    size_bytes INTEGER NOT NULL CHECK(size_bytes >= 0),
    content_sha256 TEXT NOT NULL,
    is_current INTEGER NOT NULL CHECK(is_current IN (0,1)),
    CHECK(is_current = 0 OR size_bytes <= 8192)
);
CREATE UNIQUE INDEX IF NOT EXISTS pk_memory_one_current
    ON pk_memory_checkpoint(project_id) WHERE is_current = 1;
CREATE TABLE IF NOT EXISTS pk_search_entry (
    search_id TEXT PRIMARY KEY,
    entity_id TEXT NOT NULL UNIQUE REFERENCES pk_entity(entity_id),
    title TEXT NOT NULL,
    summary TEXT,
    tags TEXT,
    access_class TEXT NOT NULL,
    content_sha256 TEXT NOT NULL
);
CREATE VIRTUAL TABLE IF NOT EXISTS pk_search_fts USING fts5(
    search_id UNINDEXED, title, summary, tags, content=''
);
CREATE VIRTUAL TABLE IF NOT EXISTS pk_search_tri USING fts5(
    search_id UNINDEXED, title, summary, tags, content='', tokenize='trigram'
);
CREATE TABLE IF NOT EXISTS pk_diagnostic (
    diagnostic_id TEXT PRIMARY KEY,
    generation_id TEXT REFERENCES pk_generation(generation_id),
    source_id TEXT REFERENCES pk_source(source_id),
    entity_id TEXT REFERENCES pk_entity(entity_id),
    severity TEXT NOT NULL CHECK(severity IN ('info','warning','error','fatal')),
    code TEXT NOT NULL,
    safe_message TEXT NOT NULL,
    locator_id TEXT REFERENCES pk_locator(locator_id),
    diagnostic_status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS pk_cache_entry (
    cache_key TEXT PRIMARY KEY,
    cache_kind TEXT NOT NULL,
    relative_path TEXT NOT NULL,
    size_bytes INTEGER NOT NULL CHECK(size_bytes >= 0),
    created_at TEXT NOT NULL,
    expires_at TEXT,
    generation_id TEXT REFERENCES pk_generation(generation_id),
    authorization_digest TEXT NOT NULL,
    content_sha256 TEXT NOT NULL,
    legal_hold INTEGER NOT NULL DEFAULT 0 CHECK(legal_hold IN (0,1))
);
CREATE TABLE IF NOT EXISTS pk_render_view (
    view_id TEXT PRIMARY KEY,
    view_kind TEXT NOT NULL,
    subject_id TEXT NOT NULL,
    profile TEXT NOT NULL,
    locale TEXT NOT NULL,
    authorization_digest TEXT NOT NULL,
    generation_id TEXT NOT NULL REFERENCES pk_generation(generation_id),
    input_fingerprint TEXT NOT NULL,
    output_path TEXT NOT NULL,
    content_sha256 TEXT NOT NULL,
    render_status TEXT NOT NULL,
    as_of TEXT NOT NULL,
    manifest_sha256 TEXT NOT NULL,
    UNIQUE(view_kind,subject_id,profile,locale,authorization_digest,generation_id)
);

CREATE TABLE IF NOT EXISTS pm_project_profile (
    project_id TEXT PRIMARY KEY, project_name TEXT, project_status TEXT,
    manager_party_id TEXT, planned_start TEXT, planned_end TEXT, actual_start TEXT,
    actual_end TEXT, completion_ratio REAL, facts_high_watermark INTEGER, {_PM_COMMON}
);
CREATE TABLE IF NOT EXISTS pm_party (
    party_id TEXT PRIMARY KEY, project_id TEXT, party_kind TEXT, display_name TEXT,
    role_name TEXT, department TEXT, responsibility TEXT, engagement_level TEXT,
    {_PM_COMMON}, FOREIGN KEY(project_id) REFERENCES pm_project_profile(project_id)
);
CREATE TABLE IF NOT EXISTS pm_work_plan (
    plan_item_id TEXT PRIMARY KEY, project_id TEXT, parent_plan_item_id TEXT,
    plan_kind TEXT, title TEXT, owner_party_id TEXT, task_status TEXT,
    planned_start TEXT, planned_end TEXT, actual_start TEXT, actual_end TEXT,
    completion_ratio REAL, schedule_variance REAL, {_PM_COMMON},
    FOREIGN KEY(project_id) REFERENCES pm_project_profile(project_id),
    FOREIGN KEY(parent_plan_item_id) REFERENCES pm_work_plan(plan_item_id),
    FOREIGN KEY(owner_party_id) REFERENCES pm_party(party_id)
);
CREATE TABLE IF NOT EXISTS pm_risk (
    risk_id TEXT PRIMARY KEY, project_id TEXT, title TEXT, description TEXT,
    probability REAL, impact REAL, risk_level TEXT, owner_party_id TEXT,
    response_strategy TEXT, risk_status TEXT, due_at TEXT, {_PM_COMMON},
    FOREIGN KEY(project_id) REFERENCES pm_project_profile(project_id),
    FOREIGN KEY(owner_party_id) REFERENCES pm_party(party_id)
);
CREATE TABLE IF NOT EXISTS pm_communication (
    communication_id TEXT PRIMARY KEY, project_id TEXT, stakeholder_party_id TEXT,
    information_need TEXT, frequency TEXT, channel TEXT, owner_party_id TEXT,
    next_at TEXT, communication_status TEXT, {_PM_COMMON},
    FOREIGN KEY(project_id) REFERENCES pm_project_profile(project_id),
    FOREIGN KEY(stakeholder_party_id) REFERENCES pm_party(party_id),
    FOREIGN KEY(owner_party_id) REFERENCES pm_party(party_id)
);
CREATE TABLE IF NOT EXISTS pm_meeting (
    meeting_id TEXT PRIMARY KEY, project_id TEXT, title TEXT, meeting_type TEXT,
    scheduled_at TEXT, chair_party_id TEXT, decision_summary TEXT, meeting_status TEXT,
    {_PM_COMMON}, FOREIGN KEY(project_id) REFERENCES pm_project_profile(project_id),
    FOREIGN KEY(chair_party_id) REFERENCES pm_party(party_id)
);
CREATE TABLE IF NOT EXISTS pm_action_item (
    action_item_id TEXT PRIMARY KEY, project_id TEXT, meeting_id TEXT, title TEXT,
    owner_party_id TEXT, due_at TEXT, action_status TEXT, completion_note TEXT,
    {_PM_COMMON}, FOREIGN KEY(project_id) REFERENCES pm_project_profile(project_id),
    FOREIGN KEY(meeting_id) REFERENCES pm_meeting(meeting_id),
    FOREIGN KEY(owner_party_id) REFERENCES pm_party(party_id)
);
CREATE TABLE IF NOT EXISTS pm_status_report (
    status_report_id TEXT PRIMARY KEY, project_id TEXT, period_start TEXT, period_end TEXT,
    overall_status TEXT, completion_ratio REAL, highlights TEXT, next_steps TEXT,
    help_needed TEXT, {_PM_COMMON},
    FOREIGN KEY(project_id) REFERENCES pm_project_profile(project_id),
    UNIQUE(project_id,period_start,period_end)
);
CREATE TABLE IF NOT EXISTS pm_change_request (
    change_request_id TEXT PRIMARY KEY, project_id TEXT, title TEXT, change_type TEXT,
    reason TEXT, impact_summary TEXT, requester_party_id TEXT, approver_party_id TEXT,
    decision TEXT, change_status TEXT, requested_at TEXT, decided_at TEXT, {_PM_COMMON},
    FOREIGN KEY(project_id) REFERENCES pm_project_profile(project_id),
    FOREIGN KEY(requester_party_id) REFERENCES pm_party(party_id),
    FOREIGN KEY(approver_party_id) REFERENCES pm_party(party_id)
);
CREATE TABLE IF NOT EXISTS pm_project_summary (
    summary_id TEXT PRIMARY KEY, project_id TEXT NOT NULL UNIQUE, summary_status TEXT,
    scope_result TEXT, schedule_result TEXT, cost_result TEXT, quality_result TEXT,
    delivery_result TEXT, lessons_learned TEXT, closure_eligibility TEXT, closed_at TEXT,
    {_PM_COMMON}, FOREIGN KEY(project_id) REFERENCES pm_project_profile(project_id)
);
"""


@dataclass(frozen=True, slots=True)
class SchemaReport:
    core_tables: tuple[str, ...]
    pm_tables: tuple[str, ...]
    fts_tables: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class FieldMapReport:
    field_count: int
    unique_field_count: int
    row_model_count: int
    source_schema_id: str
    source_contract_revision: str
    release_status: str


def create_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(DDL)
    entity_columns = {
        str(row[1]) for row in connection.execute("PRAGMA table_info(pk_entity)").fetchall()
    }
    if "detail_json" not in entity_columns:
        connection.execute(
            "ALTER TABLE pk_entity ADD COLUMN detail_json TEXT NOT NULL DEFAULT '{}'"
        )


def validate_schema(connection: sqlite3.Connection) -> SchemaReport:
    rows = connection.execute(
        "SELECT name FROM sqlite_master WHERE type IN ('table','view')"
    ).fetchall()
    existing = {str(row[0]) for row in rows}
    expected = set(CORE_TABLES) | set(PM_TABLES)
    missing = sorted(expected - existing)
    if missing:
        raise ValueError(f"project-knowledge schema missing tables: {', '.join(missing)}")
    foreign_key_violations = connection.execute("PRAGMA foreign_key_check").fetchall()
    if foreign_key_violations:
        raise ValueError(f"project-knowledge schema has FK violations: {foreign_key_violations!r}")
    return SchemaReport(CORE_TABLES, PM_TABLES, FTS_TABLES)


def _require_mapping_keys(mapping: dict[str, Any], field_id: str) -> None:
    required = {
        "field_id",
        "source_snapshot_path",
        "source_type",
        "row_model",
        "target_kind",
        "value_owner",
        "history_policy",
        "row_identity_owner",
        "target_key_formula",
        "source_nullable",
    }
    missing = sorted(required - mapping.keys())
    if missing:
        raise ValueError(f"field {field_id!r} missing keys: {', '.join(missing)}")
    if mapping["target_kind"] == "sqlite_projection":
        if not mapping.get("target_table") or not mapping.get("target_column"):
            raise ValueError(f"field {field_id!r} is missing SQLite target")
    elif mapping["target_kind"] == "render_dto":
        if not mapping.get("target_dto") or not mapping.get("target_field"):
            raise ValueError(f"field {field_id!r} is missing DTO target")
    else:
        raise ValueError(f"field {field_id!r} has unsupported target_kind")


def validate_pm_field_map(path: Path) -> FieldMapReport:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_id") != "ProjectKnowledgePmFieldMap/R009/v1":
        raise ValueError("unexpected PM field-map schema_id")
    source = payload.get("source_contract")
    if not isinstance(source, dict):
        raise ValueError("source_contract must be an object")
    pins = {
        "revision": "R014",
        "whole_file_sha256": "836fadc2c214ef2f56b2a21ef2fb705445a58ca7ddb0047f3b638292ba578d33",
        "field_catalog_sha256": "658f8d805ce423e46b686e7e6da2de22d0d7e874817a153bffefdf8c0d604313",
        "release_manifest_sha256": (
            "ea84805f62b9c20d17f625e0e4f68efcd510c19897cc1b5c8ebacf70a5bdef4e"
        ),
        "release_status": "released",
        "human_approval_ledger_key": (
            "FLOW-CONTRACT-001:TASK-REQ-002:R014:human-formalization-approved:v1"
        ),
    }
    for key, expected in pins.items():
        if source.get(key) != expected:
            raise ValueError(f"source_contract.{key} does not match the released R014 pin")
    projection = payload.get("projection_contract")
    if not isinstance(projection, dict):
        raise ValueError("projection_contract must be an object")
    snapshot = projection.get("project_progress_snapshot")
    if not isinstance(snapshot, dict) or snapshot.get("schema_id") != "ProjectProgressSnapshot/v2":
        raise ValueError("PM field map must project ProjectProgressSnapshot/v2")
    row_models = payload.get("row_models")
    if not isinstance(row_models, dict) or len(row_models) != 13:
        raise ValueError("PM field map must declare exactly 13 row models")
    for model_id, model in row_models.items():
        if not isinstance(model, dict):
            raise ValueError(f"row model {model_id!r} must be an object")
        for key in (
            "target_kind",
            "primary_key",
            "cardinality",
            "source_collection_path",
            "source_record_id_path",
            "target_key_formula",
            "parent_keys",
            "reducer_id",
            "history_policy",
        ):
            if key not in model:
                raise ValueError(f"row model {model_id!r} missing {key}")
    mappings = payload.get("mappings")
    if not isinstance(mappings, list):
        raise ValueError("mappings must be a list")
    field_ids: list[str] = []
    for raw_mapping in mappings:
        if not isinstance(raw_mapping, dict):
            raise ValueError("every mapping must be an object")
        field_id = raw_mapping.get("field_id")
        if not isinstance(field_id, str) or not field_id:
            raise ValueError("every mapping must have a field_id")
        if field_id in field_ids:
            raise ValueError(f"duplicate field_id: {field_id}")
        field_ids.append(field_id)
        _require_mapping_keys(raw_mapping, field_id)
        if raw_mapping["row_model"] not in row_models:
            raise ValueError(f"field {field_id!r} references an unknown row model")
    if len(mappings) != 137:
        raise ValueError("PM field map must contain exactly 137 mappings")
    return FieldMapReport(
        field_count=len(mappings),
        unique_field_count=len(set(field_ids)),
        row_model_count=len(row_models),
        source_schema_id=snapshot["schema_id"],
        source_contract_revision=source["revision"],
        release_status=source["release_status"],
    )
