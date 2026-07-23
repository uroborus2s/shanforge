from __future__ import annotations

import hashlib
import json
from pathlib import Path

from domain.project_knowledge.models import AccessClass, SourceDefinition
from runtime.project_knowledge.extractors import MarkdownExtractor

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / ".factory/workitems/FLOW-CONTRACT-001/drafts/"
    "REQ-CHANGE-PROJECT-KNOWLEDGE-001.contract.R009.json"
)
PM_FIELD_MAP = (
    ROOT
    / ".factory/workitems/FLOW-CONTRACT-001/drafts/"
    "REQ-CHANGE-PROJECT-KNOWLEDGE-001.pm-field-map.R009.json"
)
FINAL_MANIFEST = (
    ROOT
    / ".factory/workitems/FLOW-CONTRACT-001/evidence/"
    "TASK-REQ-006-R009-final-candidate-manifest.json"
)
PRD = ROOT / "docs/04-product/prd.md"
REGISTRY = ROOT / ".factory/project-knowledge/source-registry.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_formal_prd_is_semantically_equal_to_frozen_r009_requirement_contract() -> None:
    assert _sha256(CONTRACT) == "53923f55c2bcc16bce6ad60ed1045c671dd490b6733885725641fe39e6859977"
    assert (
        _sha256(PM_FIELD_MAP)
        == "17af8c254017bc60eb44e73b8e61322bc57eb577ffa6baa2711f100d48251055"
    )
    assert (
        _sha256(FINAL_MANIFEST)
        == "8be9d829ea2a895eae043eaf054914cb03b7457a43d51c142cc4ad7f41f577ae"
    )

    frozen = json.loads(CONTRACT.read_text(encoding="utf-8"))
    contribution = MarkdownExtractor().extract(
        SourceDefinition(
            source_id="source:formal-prd",
            registry_source_id="SRC-DOCS",
            kind="markdown",
            relative_path="docs/04-product/prd.md",
            extractor_id="markdown-v2",
            registry_version="2",
            authority_rank=100,
            access_class=AccessClass.PUBLIC,
        ),
        PRD.read_bytes(),
    )
    entities = {item["entity_id"]: item for item in contribution["entities"]}

    assert len(frozen["requirements"]) == 16
    assert sum(len(item["acceptance_criteria"]) for item in frozen["requirements"]) == 64
    assert len(frozen["nfrs"]) == 11
    for expected in frozen["requirements"]:
        actual = entities[expected["id"]]
        assert actual["entity_kind"] == "requirement"
        assert actual["display_name"] == expected["title"]
        assert actual["priority"] == expected["priority"]
        assert actual["lifecycle_status"] == "approved"
        assert actual["details"]["normative_statements"] == expected["normative_statements"]
        assert actual["source_section_key"]
        actual_criteria = sorted(
            (
                entity
                for entity in entities.values()
                if entity["entity_kind"] == "acceptance_criterion"
                and entity["details"]["requirement_id"] == expected["id"]
            ),
            key=lambda item: int(item["entity_id"].rsplit("-AC-", 1)[1]),
        )
        assert [
            (item["entity_id"], item["details"]["statement"], item["lifecycle_status"])
            for item in actual_criteria
        ] == [
            (item["id"], item["statement"], "approved")
            for item in expected["acceptance_criteria"]
        ]

    for expected in frozen["nfrs"]:
        actual = entities[expected["id"]]
        assert actual["entity_kind"] == "non_functional_requirement"
        assert actual["display_name"] == expected["title"]
        assert actual["lifecycle_status"] == "approved"
        assert actual["details"]["metric"] == expected["metric"]
        assert actual["details"]["verification"] == expected["verification"]
        assert actual["source_section_key"]


def test_current_source_registry_retires_only_r009_requirement_contract() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    work_item_json = next(
        source
        for source in registry["sources"]
        if source["registry_source_id"] == "SRC-WORKITEM-JSON"
    )
    included = set(work_item_json["include"])
    assert (
        "FLOW-CONTRACT-001/drafts/"
        "REQ-CHANGE-PROJECT-KNOWLEDGE-001.contract.R009.json"
    ) not in included
    assert (
        "FLOW-CONTRACT-001/drafts/"
        "REQ-CHANGE-PROJECT-KNOWLEDGE-001.pm-field-map.R009.json"
    ) in included
    assert (
        "FLOW-CONTRACT-001/evidence/TASK-REQ-006-R009-final-candidate-manifest.json"
    ) in included
    assert (
        "FLOW-CONTRACT-001/evidence/TASK-REQ-002-R014-release-manifest.json"
    ) in included


def test_task_requirement_relation_declarations_have_canonical_endpoints() -> None:
    task_ids = {
        f"TASK-IMPLEMENT-003-P001-T{number:02d}" for number in range(1, 7)
    } | {f"PK-SOURCE-MIGRATION-001-T{number:02d}" for number in range(1, 4)}
    indexed_task_ids: set[str] = set()
    for task_brief in (
        ROOT / ".factory/workitems"
    ).glob("*/task-briefs/*.md"):
        relative_path = task_brief.relative_to(ROOT).as_posix()
        contribution = MarkdownExtractor().extract(
            SourceDefinition(
                source_id=f"source:task-brief:{relative_path}",
                registry_source_id="SRC-WORKITEM-BRIEF",
                kind="markdown",
                relative_path=relative_path,
                extractor_id="markdown-v2",
                registry_version="2",
                authority_rank=90,
                access_class=AccessClass.PROJECT,
            ),
            task_brief.read_bytes(),
        )
        indexed_task_ids.update(
            entity["entity_id"]
            for entity in contribution["entities"]
            if entity["entity_kind"] == "work_item"
        )
    assert task_ids <= indexed_task_ids

    prd_entities = {
        item["entity_id"]
        for item in MarkdownExtractor()
        .extract(
            SourceDefinition(
                source_id="source:formal-prd",
                registry_source_id="SRC-DOCS",
                kind="markdown",
                relative_path="docs/04-product/prd.md",
                extractor_id="markdown-v2",
                registry_version="2",
                authority_rank=100,
                access_class=AccessClass.PUBLIC,
            ),
            PRD.read_bytes(),
        )["entities"]
    }
    declarations = json.loads(
        (ROOT / ".factory/project-knowledge/relation-declarations.json").read_text(
            encoding="utf-8"
        )
    )
    task_edges = [
        edge for edge in declarations["relations"] if edge["from_entity_id"] in task_ids
    ]
    assert len(task_edges) == 88
    assert {edge["from_entity_id"] for edge in task_edges} == task_ids
    assert all(edge["to_entity_id"] in prd_entities for edge in task_edges)
    assert all(
        edge["relation_type"] == "IMPLEMENTS"
        and edge["strength"] == "strong"
        and edge["confidence"] == 1.0
        for edge in task_edges
    )
    flow_task_edges = [
        edge
        for edge in declarations["relations"]
        if edge["from_entity_id"] == "FLOW-TASK-011"
    ]
    assert flow_task_edges == [
        {
            "from_entity_id": "FLOW-TASK-011",
            "to_entity_id": "REQ-PKI-008",
            "relation_type": "IMPLEMENTS",
            "strength": "strong",
            "confidence": 1.0,
        }
    ]
