from __future__ import annotations

from domain.project_knowledge.models import AccessClass, SourceDefinition
from runtime.project_knowledge.extractors import (
    JsonExtractor,
    JsonLinesExtractor,
    MarkdownExtractor,
    PythonExtractor,
)


def source(kind: str, path: str) -> SourceDefinition:
    return SourceDefinition(
        source_id=f"source:{kind}:1",
        registry_source_id=f"SRC-{kind.upper()}",
        kind=kind,
        relative_path=path,
        extractor_id=f"{kind}-v1",
        registry_version="1",
        authority_rank=100,
        access_class=AccessClass.PROJECT,
    )


def test_markdown_uses_document_and_section_identity_without_persisting_body() -> None:
    content = b"""<!-- sf:document-id=DOC-1 -->
# Project

Introductory text that is safe to summarize.

<!-- sf:section-id=SEC-DETAIL -->
## Detail

Body text.
"""
    contribution = MarkdownExtractor().extract(source("markdown", "docs/a.md"), content)
    assert contribution["schema_id"] == "SourceContribution/v1"
    assert contribution["document"]["document_id"] == "DOC-1"
    detail = contribution["sections"][1]
    assert detail["section_id"] == "SEC-DETAIL"
    assert detail["section_key"].startswith("mdsec:")
    assert detail["locator"]["selector"]["kind"] == "markdown_section"
    assert detail["locator"]["selector"]["document_id"] == "DOC-1"
    assert detail["locator"]["selector"]["section_id"] == "SEC-DETAIL"
    assert detail["locator"]["selector"]["estimated_bytes"] > 0
    assert len(detail["locator"]["selector"]["block_sha256"]) == 64
    document_locators = [
        item
        for item in contribution["locators"]
        if item["entity_id"] == "doc:DOC-1" and item["locator_role"] == "definition"
    ]
    assert len(document_locators) == 1
    assert "Body text." not in str(contribution)


def test_markdown_duplicate_fallback_headings_get_distinct_provisional_ids() -> None:
    contribution = MarkdownExtractor().extract(
        source("markdown", "docs/repeated.md"),
        b"# Notes\n\n## Item\n\n## Item\n",
    )
    section_ids = [item["section_id"] for item in contribution["sections"]]
    assert section_ids == ["heading:notes", "heading:item", "heading:item~2"]
    assert len({item["section_key"] for item in contribution["sections"]}) == 3


def test_markdown_reads_existing_document_control_table_as_stable_metadata() -> None:
    contribution = MarkdownExtractor().extract(
        source("markdown", "docs/05-design/data-design.md"),
        """# 数据与存储设计

| 项目 | 内容 |
|---|---|
| 文档 ID | `DESIGN-DATA-001` |
| 正式版本 | `v1.1.0` |
| 负责人 | `HUMAN_DATABASE_LEAD` |
| 状态 | 已批准并生效 |

- 主要读者：架构、后端、数据、测试。
""".encode(),
    )

    assert contribution["document"] == {
        "document_id": "DESIGN-DATA-001",
        "entity_id": "doc:DESIGN-DATA-001",
        "title": "数据与存储设计",
        "chinese_name": "数据与存储设计",
        "audience": "架构、后端、数据、测试",
        "owner": "HUMAN_DATABASE_LEAD",
        "doc_status": "已批准并生效",
        "doc_version": "v1.1.0",
        "semantic_sha256": contribution["document"]["semantic_sha256"],
        "artifact_id": contribution["artifact"]["artifact_id"],
    }
    assert not contribution["diagnostics"]


def test_relation_declaration_json_is_normalized_without_defining_endpoints() -> None:
    contribution = JsonExtractor().extract(
        source("json", ".factory/project-knowledge/relation-declarations.json"),
        b'{"schema_id":"ProjectKnowledgeRelationDeclarations/v1",'
        b'"relations":[{"from_entity_id":"REQ-1","to_entity_id":"doc:DESIGN-1",'
        b'"relation_type":"SATISFIES","strength":"strong","confidence":1.0}]}',
    )

    assert contribution["relations"] == [
        {
            "from_entity_id": "REQ-1",
            "to_entity_id": "doc:DESIGN-1",
            "relation_type": "SATISFIES",
            "strength": "strong",
            "confidence": 1.0,
            "evidence_locator_id": None,
        }
    ]
    assert all(
        item["entity_id"] not in {"REQ-1", "doc:DESIGN-1"} for item in contribution["entities"]
    )


def test_python_extractor_uses_ast_qualified_symbol_identity() -> None:
    content = b"""class Greeter:
    def greet(self, name: str) -> str:
        return name

async def run() -> None:
    pass
"""
    contribution = PythonExtractor().extract(source("python", "src/demo.py"), content)
    symbols = {item["qualified_name"]: item for item in contribution["symbols"]}
    assert set(symbols) == {"Greeter", "Greeter.greet", "run"}
    assert symbols["Greeter.greet"]["symbol_id"].startswith("py:src.demo:")
    assert "signature_digest" in symbols["Greeter.greet"]["locator"]["selector"]


def test_python_extractor_signature_omits_decorators_for_every_symbol_kind() -> None:
    content = b"""@factory(mode="safe")
def build(value: int) -> str:
    return str(value)

@logged
async def fetch(item: str) -> bytes:
    return item.encode()

@sealed
class Service(Base, mode="safe"):
    pass
"""
    contribution = PythonExtractor().extract(source("python", "src/decorated.py"), content)
    signatures = {
        item["qualified_name"]: item["signature_text"] for item in contribution["symbols"]
    }

    assert signatures == {
        "build": "def build(value: int) -> str:",
        "fetch": "async def fetch(item: str) -> bytes:",
        "Service": "class Service(Base, mode='safe'):",
    }


def test_json_and_jsonl_locators_are_pointer_and_event_uid_based() -> None:
    json_contribution = JsonExtractor().extract(
        source("json", ".factory/project.json"),
        b'{"project":{"id":"shanforge"},"items":[{"id":"one"}]}',
    )
    pointers = {item["pointer"] for item in json_contribution["records"]}
    assert "/project/id" in pointers
    assert "/items/0/id" in pointers
    object_entity = next(
        item for item in json_contribution["entities"] if item["entity_id"] == "one"
    )
    assert object_entity["entity_kind"] == "json_record"

    jsonl_contribution = JsonLinesExtractor().extract(
        source("jsonl", ".factory/workitems/A/ledger.jsonl"),
        b'{"event":"created","idempotency_key":"evt:1"}\n{"event":"unsafe-without-id"}\n',
    )
    assert [event["event_uid"] for event in jsonl_contribution["events"]] == ["evt:1"]
    assert jsonl_contribution["diagnostics"][0]["code"] == "JSONL_EVENT_UID_MISSING"


def test_jsonl_projects_latest_readable_work_item_without_losing_event_audit() -> None:
    contribution = JsonLinesExtractor().extract(
        source("jsonl", ".factory/workitems/A/ledger.jsonl"),
        b'{"event":"started","task":"TASK-1","status":"running","idempotency_key":"e1"}\n'
        b'{"event":"verified","task":"TASK-1","status":"ready_for_review",'
        b'"next_action":"review","idempotency_key":"e2"}\n',
    )
    work_items = [item for item in contribution["entities"] if item["entity_kind"] == "work_item"]
    assert len(work_items) == 1
    assert work_items[0]["display_name"] == "TASK-1"
    assert work_items[0]["summary"] == (
        "最近进展：验证已完成；当前状态：等待独立评审；下一步：独立评审。"
    )
    assert len(contribution["events"]) == 2
