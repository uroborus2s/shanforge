from __future__ import annotations

import json
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from domain.project_knowledge.models import (
    AccessClass,
    Locator,
    SourceDefinition,
    ValueState,
    canonical_json,
    document_section_key,
    stable_id,
)
from settings.project_knowledge.schema import validate_pm_field_map

ROOT = Path(__file__).resolve().parents[1]
FIELD_MAP = (
    ROOT / ".factory/workitems/FLOW-CONTRACT-001/drafts/"
    "REQ-CHANGE-PROJECT-KNOWLEDGE-001.pm-field-map.R009.json"
)


def test_stable_ids_use_canonical_json_and_have_no_separator_collision() -> None:
    assert canonical_json({"b": 2, "a": "值"}) == '{"a":"值","b":2}'
    assert stable_id("entity", ["a:b", "c"]) != stable_id("entity", ["a", "b:c"])
    assert document_section_key("doc:a", "b") != document_section_key("doc", "a:b")
    assert document_section_key("doc", "intro").startswith("mdsec:")
    assert len(document_section_key("doc", "intro")) == len("mdsec:") + 64


def test_source_and_locator_contracts_fail_closed() -> None:
    source = SourceDefinition(
        source_id="source:" + "a" * 64,
        registry_source_id="docs-human",
        kind="markdown",
        relative_path="docs/index.md",
        extractor_id="markdown-v1",
        registry_version="1",
        authority_rank=100,
        access_class=AccessClass.PROJECT,
    )
    with pytest.raises(FrozenInstanceError):
        source.kind = "json"  # type: ignore[misc]
    with pytest.raises(ValueError, match="relative_path"):
        SourceDefinition(
            source_id="source:" + "a" * 64,
            registry_source_id="bad",
            kind="markdown",
            relative_path="../secret.md",
            extractor_id="markdown-v1",
            registry_version="1",
            authority_rank=1,
            access_class=AccessClass.RESTRICTED,
        )
    with pytest.raises(ValueError, match="line"):
        Locator(
            locator_id="locator:" + "b" * 64,
            locator_kind="markdown_section",
            selector={"line": 42},
            source_id=source.source_id,
        )


def test_value_state_is_a_closed_four_state_contract() -> None:
    assert {state.value for state in ValueState} == {
        "known",
        "unknown",
        "not_registered",
        "not_applicable",
    }


def test_r009_pm_field_map_is_complete_and_pinned() -> None:
    result = validate_pm_field_map(FIELD_MAP)
    assert result.field_count == 137
    assert result.unique_field_count == 137
    assert result.row_model_count == 13
    assert result.source_schema_id == "ProjectProgressSnapshot/v2"
    assert result.source_contract_revision == "R014"
    assert result.release_status == "released"


def test_pm_field_map_rejects_duplicate_field_ids(tmp_path: Path) -> None:
    payload = json.loads(FIELD_MAP.read_text(encoding="utf-8"))
    payload["mappings"].append(payload["mappings"][0])
    candidate = tmp_path / "duplicate.json"
    candidate.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate field_id"):
        validate_pm_field_map(candidate)
