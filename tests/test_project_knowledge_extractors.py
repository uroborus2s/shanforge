from __future__ import annotations

from pathlib import Path

import pytest

from domain.project_knowledge.models import AccessClass, SourceDefinition, stable_id
from runtime.project_knowledge.extractors import (
    JsonExtractor,
    JsonLinesExtractor,
    MarkdownExtractor,
    PythonExtractor,
)
from settings.project_knowledge.source_registry import FileSourceRegistry


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


def test_markdown_projects_requirements_acceptance_and_nfr_from_stable_sections() -> None:
    contribution = MarkdownExtractor().extract(
        source("markdown", "docs/04-product/prd.md"),
        """<!-- sf:document-id=PRD-1 -->
# 产品需求

<!-- sf:section-id=REQ-PKI-001 -->
## REQ-PKI-001：确定性项目快照

- 分类：项目查看与管理
- 优先级：P0
- 状态：已批准（v4.1.0）
- 用户故事：作为项目负责人，我希望快速获得当前项目快照，以便直接判断下一步。
- 需求规则 1：输入不变时复用最后有效站点。
- 需求规则 2：输入变化时只刷新受影响页面。
- `REQ-PKI-001-AC-1`：缓存命中时不得重写 HTML。
- `REQ-PKI-001-AC-2`：刷新失败时保留上一有效站点。

<!-- sf:section-id=NFR-PKI-001 -->
## NFR-PKI-001：会话恢复

- 分类：性能与上下文
- 状态：已批准（v4.1.0）
- 度量目标：单记忆点不超过 8 KiB。
- 验证方式：使用 0、1、50 和 200 条事件夹具。
""".encode(),
    )

    entities = {item["entity_id"]: item for item in contribution["entities"]}
    requirement = entities["REQ-PKI-001"]
    assert requirement["entity_kind"] == "requirement"
    assert requirement["display_name"] == "确定性项目快照"
    assert requirement["lifecycle_status"] == "approved"
    assert requirement["priority"] == "P0"
    assert requirement["details"]["category"] == "项目查看与管理"
    assert requirement["details"]["user_scenario"].startswith("作为项目负责人")
    assert requirement["details"]["expected_result"] == [
        "输入不变时复用最后有效站点。",
        "输入变化时只刷新受影响页面。",
    ]
    assert requirement["source_section_key"].startswith("mdsec:")

    criterion = entities["REQ-PKI-001-AC-1"]
    assert criterion["entity_kind"] == "acceptance_criterion"
    assert criterion["lifecycle_status"] == "approved"
    assert criterion["details"]["statement"] == "缓存命中时不得重写 HTML。"
    assert entities["NFR-PKI-001"]["entity_kind"] == "non_functional_requirement"
    assert entities["NFR-PKI-001"]["details"]["metric"] == "单记忆点不超过 8 KiB。"
    assert entities["NFR-PKI-001"]["details"]["verification"].startswith("使用 0、1")

    requirement_locator = next(
        item
        for item in contribution["locators"]
        if item["entity_id"] == "REQ-PKI-001" and item["locator_role"] == "definition"
    )
    assert requirement_locator["locator_kind"] == "markdown_section"
    assert requirement_locator["selector"]["section_id"] == "REQ-PKI-001"
    assert {
        (item["from_entity_id"], item["to_entity_id"], item["relation_type"])
        for item in contribution["relations"]
    } == {
        ("REQ-PKI-001", "REQ-PKI-001-AC-1", "CONTAINS"),
        ("REQ-PKI-001", "REQ-PKI-001-AC-2", "CONTAINS"),
    }


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
    event_uids = [event["event_uid"] for event in jsonl_contribution["events"]]
    assert event_uids[0] == "evt:1"
    assert event_uids[1].startswith("derived:")
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
    assert work_items[0]["entity_id"] == "TASK-1"
    assert work_items[0]["display_name"] == "TASK-1"
    assert work_items[0]["summary"] == (
        "最近进展：验证已完成；当前状态：等待独立评审；下一步：独立评审。"
    )
    assert len(contribution["events"]) == 2
    assert contribution["aliases"] == [
        {
            "alias_entity_id": stable_id("workitem", ["source:jsonl:1", "TASK-1"]),
            "canonical_entity_id": "TASK-1",
            "reason": ("jsonl-v5 canonical work-item ID migration from source-scoped identity"),
        }
    ]


def test_jsonl_legacy_event_without_uid_updates_current_task_instead_of_being_dropped() -> None:
    contribution = JsonLinesExtractor().extract(
        source("jsonl", ".factory/workitems/A/ledger.jsonl"),
        b'{"event":"implemented","task":"TASK-1","status":"ready_for_review",'
        b'"ts":"2026-07-01T10:00:00+08:00","idempotency_key":"e1"}\n'
        b'{"event":"human_confirmation","task":"TASK-1","status":"human_approved",'
        b'"ts":"2026-07-01T11:00:00+08:00","next_required_action":"none"}\n',
    )

    work_item = next(
        item for item in contribution["entities"] if item["entity_kind"] == "work_item"
    )
    assert work_item["lifecycle_status"] == "human_approved"
    assert work_item["details"]["updated_at"] == "2026-07-01T11:00:00+08:00"
    assert len(contribution["events"]) == 2
    assert contribution["events"][1]["event_uid"].startswith("derived:")


def test_jsonl_natural_labels_remain_source_scoped_and_do_not_become_global_ids() -> None:
    first_source = source("jsonl", ".factory/workitems/A/ledger.jsonl")
    second_source = SourceDefinition(
        source_id="source:jsonl:2",
        registry_source_id="SRC-JSONL",
        kind="jsonl",
        relative_path=".factory/workitems/B/ledger.jsonl",
        extractor_id="jsonl-v5",
        registry_version="2",
        authority_rank=100,
        access_class=AccessClass.PROJECT,
    )
    content = (
        b'{"event":"started","task":"shared-label","status":"in_progress","idempotency_key":"e1"}\n'
    )

    first = JsonLinesExtractor().extract(first_source, content)
    second = JsonLinesExtractor().extract(second_source, content)
    first_item = next(item for item in first["entities"] if item["entity_kind"] == "work_item")
    second_item = next(item for item in second["entities"] if item["entity_kind"] == "work_item")
    assert first_item["entity_id"].startswith("workitem:")
    assert second_item["entity_id"].startswith("workitem:")
    assert first_item["entity_id"] != second_item["entity_id"]
    assert first.get("aliases", []) == []
    assert second.get("aliases", []) == []


def test_markdown_task_brief_uses_declared_task_name_when_heading_is_generic() -> None:
    contribution = MarkdownExtractor().extract(
        source(
            "markdown",
            ".factory/workitems/PM-DASHBOARD-002/task-briefs/PM-DASHBOARD-002-T01.md",
        ),
        """# 任务简报

## 工作项

- 任务：`PM-DASHBOARD-002-T01` Excel 十模块项目状态查看契约
""".encode(),
    )

    assert contribution["document"]["title"] == "Excel 十模块项目状态查看契约"
    assert contribution["document"]["chinese_name"] == "Excel 十模块项目状态查看契约"
    work_item = next(
        item for item in contribution["entities"] if item["entity_kind"] == "work_item"
    )
    assert work_item["entity_id"] == "PM-DASHBOARD-002-T01"
    assert work_item["display_name"] == "Excel 十模块项目状态查看契约"
    assert work_item["lifecycle_status"] == "planned"


def test_markdown_task_brief_uses_heading_when_declared_task_has_no_inline_title() -> None:
    contribution = MarkdownExtractor().extract(
        source(
            "markdown",
            ".factory/workitems/FLOW-CONTRACT-001/task-briefs/TASK-1.md",
        ),
        """# T05 异步同步、有界维护与资料迁移

## 工作项

- 任务：`TASK-IMPLEMENT-003-P001-T05`
- 状态：`ready_for_review`
""".encode(),
    )

    work_item = next(
        item for item in contribution["entities"] if item["entity_kind"] == "work_item"
    )
    assert work_item["entity_id"] == "TASK-IMPLEMENT-003-P001-T05"
    assert work_item["display_name"] == "T05 异步同步、有界维护与资料迁移"
    assert work_item["lifecycle_status"] == "ready_for_review"


def test_markdown_task_brief_projects_human_readable_execution_fields() -> None:
    contribution = MarkdownExtractor().extract(
        source(
            "markdown",
            ".factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-011.md",
        ),
        """# FLOW-TASK-011 升级项目管理视图

## 工作项

- 任务：`FLOW-TASK-011`
- 状态：`in_progress`
- 设计：将任务详情拆成目的、具体工作和交付结果。
- UI：把需求按产品、业务域、需求和验收标准逐层展示。
- 完成条件：用户无需理解内部编号即可说明任务目的和验收结果。

## 目标

让项目成员快速看懂每项任务为什么做、具体做什么、完成后得到什么。

## 允许修改

- 任务简报提取器与 SQLite 投影。
- 只读站点渲染器和对应测试。

## 交付结果

- 可读的任务详情页。
- 可展开的需求树。

## 验证命令

`pytest tests/test_project_site_renderer.py`
""".encode(),
    )

    work_item = next(
        item for item in contribution["entities"] if item["entity_kind"] == "work_item"
    )
    assert work_item["details"] == {
        "task_id": "FLOW-TASK-011",
        "task_title": "FLOW-TASK-011 升级项目管理视图",
        "task_status": "in_progress",
        "source_document_id": contribution["document"]["document_id"],
        "goal": "让项目成员快速看懂每项任务为什么做、具体做什么、完成后得到什么。",
        "work_items": [
            "将任务详情拆成目的、具体工作和交付结果。",
            "把需求按产品、业务域、需求和验收标准逐层展示。",
        ],
        "scope": [
            "任务简报提取器与 SQLite 投影。",
            "只读站点渲染器和对应测试。",
        ],
        "deliverables": ["可读的任务详情页。", "可展开的需求树。"],
        "completion_conditions": "用户无需理解内部编号即可说明任务目的和验收结果。",
        "verification": "`pytest tests/test_project_site_renderer.py`",
    }


def test_markdown_task_brief_projects_declared_task_scope_and_targets() -> None:
    contribution = MarkdownExtractor().extract(
        source(
            "markdown",
            ".factory/workitems/DEMO-001/task-briefs/DEMO-001-T06.md",
        ),
        """# DEMO-001-T06 横切需求实现

## 工作项

- 任务：`DEMO-001-T06`
- 任务层级：`cross_cutting`
- 关联目标：
  - `REQ-001`
  - `NFR-001`
""".encode(),
    )

    work_item = next(
        item for item in contribution["entities"] if item["entity_kind"] == "work_item"
    )
    assert work_item["details"]["task_scope"] == "cross_cutting"
    assert work_item["details"]["traceability_targets"] == ["REQ-001", "NFR-001"]


def test_markdown_task_brief_rejects_unknown_task_scope() -> None:
    with pytest.raises(ValueError, match="unsupported task_scope: feature"):
        MarkdownExtractor().extract(
            source(
                "markdown",
                ".factory/workitems/DEMO-001/task-briefs/DEMO-001-T07.md",
            ),
            b"# DEMO-001-T07\n\n- Task scope: `feature`\n",
        )


def test_markdown_task_brief_supports_english_and_numbered_semantic_sections() -> None:
    contribution = MarkdownExtractor().extract(
        source(
            "markdown",
            ".factory/workitems/DEMO-001/task-briefs/EAD-TASK-001-demo.md",
        ),
        """# EAD-TASK-001 Capability assessment

## Goal

Explain whether the current product can close an enterprise delivery loop.

## 8. 开发实现

- Build a readable capability matrix.
- Link each gap to a delivery task.

## Required Outputs

- A capability assessment.
- A prioritized product backlog.

## Acceptance Criteria

- The result answers what the system does and why it matters.

## Verification

- Check the generated read-only task page.
""".encode(),
    )

    work_item = next(
        item for item in contribution["entities"] if item["entity_kind"] == "work_item"
    )
    assert work_item["entity_id"] == "EAD-TASK-001"
    assert work_item["details"]["goal"] == (
        "Explain whether the current product can close an enterprise delivery loop."
    )
    assert work_item["details"]["work_items"] == [
        "Build a readable capability matrix.",
        "Link each gap to a delivery task.",
    ]
    assert work_item["details"]["deliverables"] == [
        "A capability assessment.",
        "A prioritized product backlog.",
    ]
    assert work_item["details"]["completion_conditions"] == (
        "The result answers what the system does and why it matters."
    )
    assert work_item["details"]["verification"] == ("Check the generated read-only task page.")


def test_markdown_task_brief_task_heading_remains_a_semantic_goal() -> None:
    contribution = MarkdownExtractor().extract(
        source(
            "markdown",
            ".factory/workitems/DEMO-001/task-briefs/DEMO-001-T05.md",
        ),
        b"# DEMO-001-T05\n\n## Task\n\nExplain the human goal.\n",
    )

    work_item = next(
        item for item in contribution["entities"] if item["entity_kind"] == "work_item"
    )
    assert work_item["details"]["goal"] == "Explain the human goal."


def test_markdown_task_brief_supports_inline_semantic_aliases() -> None:
    contribution = MarkdownExtractor().extract(
        source(
            "markdown",
            ".factory/workitems/DEMO-001/task-briefs/DEMO-001-T01.md",
        ),
        """# DEMO-001-T01

- 目的：让成员看懂任务。
- 本轮交付：可验收的任务详情。
- 决策：复用现有详情字段。
""".encode(),
    )

    work_item = next(
        item for item in contribution["entities"] if item["entity_kind"] == "work_item"
    )
    assert work_item["details"]["goal"] == "让成员看懂任务。"
    assert work_item["details"]["deliverables"] == "可验收的任务详情。"
    assert work_item["details"]["work_items"] == "复用现有详情字段。"


def test_markdown_task_brief_supports_empty_inline_field_with_indented_list() -> None:
    contribution = MarkdownExtractor().extract(
        source(
            "markdown",
            ".factory/workitems/DEMO-001/task-briefs/DEMO-001-T02.md",
        ),
        """# DEMO-001-T02

- 目标：
  - 退役旧入口。
  - 保留稳定链接。
- 状态：`in_progress`
""".encode(),
    )

    work_item = next(
        item for item in contribution["entities"] if item["entity_kind"] == "work_item"
    )
    assert work_item["details"]["goal"] == ["退役旧入口。", "保留稳定链接。"]


def test_markdown_task_brief_unknown_inline_fields_do_not_invent_semantics() -> None:
    contribution = MarkdownExtractor().extract(
        source(
            "markdown",
            ".factory/workitems/DEMO-001/task-briefs/DEMO-001-T03.md",
        ),
        b"# DEMO-001-T03\n\n- Platform: iOS\n- Status: in_progress\n",
    )

    work_item = next(
        item for item in contribution["entities"] if item["entity_kind"] == "work_item"
    )
    semantic_keys = {
        "goal",
        "work_items",
        "deliverables",
        "completion_conditions",
        "verification",
    }
    assert semantic_keys.isdisjoint(work_item["details"])


def test_markdown_task_brief_identity_fields_do_not_satisfy_semantic_gate() -> None:
    contribution = MarkdownExtractor().extract(
        source(
            "markdown",
            ".factory/workitems/DEMO-001/task-briefs/DEMO-001-T04.md",
        ),
        b"# DEMO-001-T04\n\n- Task: DEMO-001-T04\n- Status: in_progress\n",
    )

    work_item = next(
        item for item in contribution["entities"] if item["entity_kind"] == "work_item"
    )
    assert not any(
        work_item["details"].get(key)
        for key in (
            "goal",
            "work_items",
            "deliverables",
            "completion_conditions",
            "verification",
        )
    )


def test_all_registered_task_briefs_project_a_work_item_entity() -> None:
    project_root = Path(__file__).resolve().parents[1]
    registry = FileSourceRegistry(
        project_root,
        project_root / ".factory/project-knowledge/source-registry.json",
    )
    task_briefs = [
        definition
        for definition in registry.sources()
        if definition.registry_source_id == "SRC-WORKITEM-BRIEF"
    ]
    assert task_briefs

    entity_ids: list[str] = []
    missing: list[str] = []
    missing_semantics: list[str] = []
    for definition in task_briefs:
        contribution = MarkdownExtractor().extract(
            definition,
            registry.read_bytes(definition),
        )
        work_items = [
            entity for entity in contribution["entities"] if entity["entity_kind"] == "work_item"
        ]
        if not work_items:
            missing.append(definition.relative_path)
            continue
        work_item = work_items[0]
        entity_ids.append(str(work_item["entity_id"]))
        details = work_item.get("details") or {}
        if not any(
            details.get(key)
            for key in (
                "goal",
                "work_items",
                "deliverables",
                "completion_conditions",
                "verification",
            )
        ):
            missing_semantics.append(definition.relative_path)

    assert missing == []
    assert missing_semantics == []
    assert len(entity_ids) == len(set(entity_ids)), (
        "registered task briefs must project globally unique work-item identities"
    )


def test_local_task_numbers_are_scoped_by_parent_work_item() -> None:
    ui = MarkdownExtractor().extract(
        source(
            "markdown",
            ".factory/workitems/UI-DESIGN-SKILL-001/task-briefs/TASK-SKILL-001.md",
        ),
        b"# TASK-SKILL-001 UI design skill\n\n## Goal\n\nImprove UI design.\n",
    )
    backend = MarkdownExtractor().extract(
        source(
            "markdown",
            ".factory/workitems/GO-BACKEND-SKILL-001/task-briefs/TASK-SKILL-001.md",
        ),
        b"# TASK-SKILL-001 Go backend skill\n\n## Goal\n\nImprove Go delivery.\n",
    )

    ui_task = next(entity for entity in ui["entities"] if entity["entity_kind"] == "work_item")
    backend_task = next(
        entity for entity in backend["entities"] if entity["entity_kind"] == "work_item"
    )
    assert ui_task["entity_id"] == "UI-DESIGN-SKILL-001-TASK-SKILL-001"
    assert backend_task["entity_id"] == "GO-BACKEND-SKILL-001-TASK-SKILL-001"
