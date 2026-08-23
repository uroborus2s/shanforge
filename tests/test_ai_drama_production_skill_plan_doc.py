from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LEGACY_PATH = "docs/04-project-development/04-design/ai-drama-production-skill-system.md"


def load_disposition() -> dict[str, object]:
    ia = json.loads(
        (
            REPO_ROOT / ".factory/workitems/FLOW-CONTRACT-001/drafts/"
            "docs-information-architecture.R019.json"
        ).read_text(encoding="utf-8")
    )
    return next(entry for entry in ia["dispositions"] if entry["source_path"] == LEGACY_PATH)


def test_unowned_ai_drama_topic_is_not_a_formal_document() -> None:
    assert not (REPO_ROOT / LEGACY_PATH).exists()


def test_unowned_ai_drama_topic_is_not_in_the_design_navigation() -> None:
    design_index = (REPO_ROOT / "docs/05-design/index.md").read_text(encoding="utf-8")
    assert "ai-drama-production-skill-system.md" not in design_index


def test_document_index_records_the_ai_drama_retirement() -> None:
    document_index = (REPO_ROOT / "docs/document-index.md").read_text(encoding="utf-8")
    assert LEGACY_PATH in document_index
    assert "专题业务方案不属于当前 shanforge 核心正式基线，无活跃 owner" in document_index


def test_ai_drama_disposition_has_no_formal_successor() -> None:
    assert load_disposition()["target_paths"] == []


def test_ai_drama_disposition_uses_the_unowned_topic_reason() -> None:
    assert load_disposition()["reason_code"] == "unowned_topic_design"


def test_ai_drama_disposition_requires_integrated_release_before_retirement() -> None:
    disposition = load_disposition()
    assert disposition["disposition"] == "conditional_retire_after_integrated_formal_release"
    assert "generation_CAS" in disposition["release_preconditions"]


def test_ai_drama_disposition_retains_its_frozen_source_identity() -> None:
    disposition = load_disposition()
    assert disposition["source_sha256"] == (
        "0b255e45780f681c9b36af125f9f4b9ea75f9e6c2cab63c1439c72e8b0a319ab"
    )
    assert disposition["source_preimage_disposition_ref"] == "SPD-R017-012"


def test_ai_drama_disposition_has_no_active_owner_transfer() -> None:
    disposition = load_disposition()
    assert disposition["mode"] == "baseline_reachable"
    assert "applicable_human_approval" in disposition["release_preconditions"]
