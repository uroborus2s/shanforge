"""Deterministic, side-effect-free source extractors."""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import re
from collections.abc import Mapping
from typing import Any, Protocol

from domain.project_knowledge.models import (
    SourceDefinition,
    canonical_json,
    document_section_key,
    stable_id,
)
from domain.project_knowledge.sensitive_values import sanitize_value


def _sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _sha256_json(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _base(source: SourceDefinition, content: bytes) -> dict[str, Any]:
    return {
        "schema_id": "SourceContribution/v1",
        "source_id": source.source_id,
        "registry_source_id": source.registry_source_id,
        "source_kind": source.kind,
        "relative_path": source.relative_path,
        "extractor_id": source.extractor_id,
        "registry_version": source.registry_version,
        "authority_rank": source.authority_rank,
        "size_bytes": len(content),
        "content_sha256": _sha256_bytes(content),
        "artifact": {
            "artifact_id": stable_id("artifact", [source.source_id, source.relative_path]),
            "artifact_kind": source.kind,
            "relative_path": source.relative_path,
            "content_sha256": _sha256_bytes(content),
            "access_class": source.access_class.value,
        },
        "entities": [],
        "locators": [],
        "search": [],
        "diagnostics": [],
    }


class Extractor(Protocol):
    kind: str

    def extract(self, source: SourceDefinition, content: bytes) -> dict[str, Any]: ...


_DOCUMENT_ID = re.compile(r"<!--\s*sf:document-id=([^\s]+)\s*-->")
_SECTION_ID = re.compile(r"<!--\s*sf:section-id=([^\s]+)\s*-->")
_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
_TABLE_ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$")
_AUDIENCE_LINE = re.compile(r"^(?:[-*]\s*)?(?:\*\*)?主要读者(?:\*\*)?[：:]\s*(.+?)\s*$")
_TASK_BRIEF_TITLE_LINE = re.compile(
    r"^\s*[-*]\s*任务[：:]\s*`[^`]+`\s+(.+?)\s*$"
)


def _metadata_value(value: str) -> str:
    return value.strip().strip("`").strip().rstrip("。；;")


def _markdown_metadata(lines: list[str]) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in lines:
        table_row = _TABLE_ROW.match(line)
        if table_row:
            key = _metadata_value(table_row.group(1))
            value = _metadata_value(table_row.group(2))
            if key not in {"项目", "内容", "---"}:
                metadata.setdefault(key, value)
        audience = _AUDIENCE_LINE.match(line.strip())
        if audience:
            metadata.setdefault("主要读者", _metadata_value(audience.group(1)))
    return metadata


def _slug(title: str) -> str:
    normalized = re.sub(r"[^\w\-\u4e00-\u9fff]+", "-", title.strip().lower()).strip("-")
    return normalized or _sha256_json(title)[:16]


class MarkdownExtractor:
    kind = "markdown"

    def extract(self, source: SourceDefinition, content: bytes) -> dict[str, Any]:
        text = content.decode("utf-8")
        contribution = _base(source, content)
        document_match = _DOCUMENT_ID.search(text)
        lines = text.splitlines()
        metadata = _markdown_metadata(lines)
        declared_document_id = metadata.get("文档 ID") or metadata.get("文档编号")
        document_id = (
            document_match.group(1)
            if document_match
            else declared_document_id
            or stable_id("document", [source.registry_source_id, source.relative_path])
        )
        document_entity_id = f"doc:{document_id}"
        raw_headings: list[tuple[int, str, str | None, int, int]] = []
        pending_section_id: str | None = None
        for index, line in enumerate(lines):
            marker = _SECTION_ID.fullmatch(line.strip())
            if marker:
                pending_section_id = marker.group(1)
                continue
            heading = _HEADING.match(line)
            if not heading:
                continue
            level = len(heading.group(1))
            title = heading.group(2).strip()
            raw_headings.append((level, title, pending_section_id, index, len(lines)))
            pending_section_id = None
        heading_counts: dict[str, int] = {}
        headings: list[tuple[int, str, str, int, int]] = []
        for position, (level, heading_title, explicit_id, start, _) in enumerate(raw_headings):
            end = raw_headings[position + 1][3] if position + 1 < len(raw_headings) else len(lines)
            if explicit_id is None:
                slug = _slug(heading_title)
                heading_counts[slug] = heading_counts.get(slug, 0) + 1
                occurrence = heading_counts[slug]
                section_id = (
                    f"heading:{slug}" if occurrence == 1 else f"heading:{slug}~{occurrence}"
                )
            else:
                section_id = explicit_id
            headings.append((level, heading_title, section_id, start, end))
        title = headings[0][1] if headings else source.relative_path.rsplit("/", 1)[-1]
        if title.strip() in {"任务简报", "实施任务简报"} and "/task-briefs/" in (
            f"/{source.relative_path}"
        ):
            declared_title = next(
                (
                    match.group(1).strip()
                    for line in lines
                    if (match := _TASK_BRIEF_TITLE_LINE.match(line)) is not None
                ),
                None,
            )
            if declared_title:
                title = declared_title
        document_metadata = {
            "chinese_name": title,
            "audience": metadata.get("主要读者"),
            "owner": metadata.get("负责人"),
            "doc_status": metadata.get("状态") or metadata.get("当前状态") or "active",
            "doc_version": metadata.get("正式版本") or metadata.get("当前正式版本"),
        }
        semantic = _sha256_json(
            {
                "document_id": document_id,
                "headings": [(h[0], h[1], h[2]) for h in headings],
                "metadata": document_metadata,
            }
        )
        artifact = contribution["artifact"]
        artifact["semantic_sha256"] = semantic
        document = {
            "document_id": document_id,
            "entity_id": document_entity_id,
            "title": title,
            **document_metadata,
            "semantic_sha256": semantic,
            "artifact_id": artifact["artifact_id"],
        }
        contribution["document"] = document
        contribution["entities"].append(
            {
                "entity_id": document_entity_id,
                "entity_kind": "document",
                "display_name": title,
                "summary": "",
                "lifecycle_status": "active",
                "semantic_sha256": semantic,
                "definition": True,
            }
        )
        contribution["search"].append(
            {"entity_id": document_entity_id, "title": title, "summary": "", "tags": "document"}
        )
        sections: list[dict[str, Any]] = []
        parent_stack: list[tuple[int, str]] = []
        for order, (level, heading_title, section_id, start, end) in enumerate(headings):
            while parent_stack and parent_stack[-1][0] >= level:
                parent_stack.pop()
            parent_key = parent_stack[-1][1] if parent_stack else None
            section_key = document_section_key(document_id, section_id)
            block = "\n".join(lines[start:end])
            block_hash = _sha256_bytes(block.encode("utf-8"))
            selector = {
                "kind": "markdown_section",
                "document_id": document_id,
                "section_id": section_id,
                "block_sha256": block_hash,
                "estimated_bytes": len(block.encode("utf-8")),
            }
            locator_id = stable_id("locator", selector)
            section = {
                "section_key": section_key,
                "section_id": section_id,
                "document_id": document_id,
                "entity_id": section_key,
                "parent_section_key": parent_key,
                "display_title": heading_title,
                "display_order": order,
                "block_sha256": block_hash,
                "safe_excerpt": "",
                "semantic_sha256": _sha256_json(
                    [document_id, section_id, heading_title, block_hash]
                ),
                "locator": {"locator_id": locator_id, "selector": selector},
            }
            sections.append(section)
            contribution["entities"].append(
                {
                    "entity_id": section_key,
                    "entity_kind": "document_section",
                    "display_name": heading_title,
                    "summary": "",
                    "lifecycle_status": "active",
                    "semantic_sha256": section["semantic_sha256"],
                    "definition": True,
                }
            )
            contribution["locators"].append(
                {
                    "locator_id": locator_id,
                    "locator_kind": "markdown_section",
                    "selector": selector,
                    "entity_id": section_key,
                    "locator_role": "definition",
                }
            )
            if order == 0:
                contribution["locators"].append(
                    {
                        "locator_id": locator_id,
                        "locator_kind": "markdown_section",
                        "selector": selector,
                        "entity_id": document_entity_id,
                        "locator_role": "definition",
                    }
                )
            contribution["search"].append(
                {
                    "entity_id": section_key,
                    "title": heading_title,
                    "summary": "",
                    "tags": f"section {document_id}",
                }
            )
            parent_stack.append((level, section_key))
        contribution["sections"] = sections
        if document_match is None and declared_document_id is None:
            contribution["diagnostics"].append(
                {
                    "code": "DOCUMENT_ID_PROVISIONAL",
                    "severity": "info",
                    "safe_message": "document uses a registry/path-derived identity",
                }
            )
        return contribution


def _signature_digest(node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) -> str:
    if isinstance(node, ast.ClassDef):
        shape: object = {"kind": "class", "bases": [ast.unparse(base) for base in node.bases]}
    else:
        shape = {
            "kind": "async" if isinstance(node, ast.AsyncFunctionDef) else "function",
            "args": [argument.arg for argument in node.args.args],
            "returns": ast.unparse(node.returns) if node.returns else None,
        }
    return _sha256_json(shape)


def _signature_text(node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) -> str:
    definition = copy.copy(node)
    definition.decorator_list = []
    definition.body = [ast.Pass()]
    return ast.unparse(definition).split("\n", 1)[0]


class _SymbolVisitor(ast.NodeVisitor):
    def __init__(self, module: str) -> None:
        self.module = module
        self.stack: list[str] = []
        self.symbols: list[dict[str, Any]] = []

    def _visit_symbol(self, node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) -> None:
        qualified_name = ".".join([*self.stack, node.name])
        if isinstance(node, ast.ClassDef):
            kind = "class"
        elif isinstance(node, ast.AsyncFunctionDef):
            kind = "async_function"
        else:
            kind = "function"
        symbol_id = f"py:{self.module}:{qualified_name}:{kind}"
        signature_digest = _signature_digest(node)
        selector = {
            "kind": "python_symbol",
            "module": self.module,
            "qualified_name": qualified_name,
            "symbol_kind": kind,
            "signature_digest": signature_digest,
        }
        self.symbols.append(
            {
                "symbol_id": symbol_id,
                "entity_id": symbol_id,
                "symbol_kind": kind,
                "qualified_name": qualified_name,
                "signature_text": _signature_text(node),
                "visibility": "private" if node.name.startswith("_") else "public",
                "semantic_sha256": _sha256_json(
                    [self.module, qualified_name, kind, signature_digest]
                ),
                "locator": {
                    "locator_id": stable_id("locator", selector),
                    "selector": selector,
                },
            }
        )
        self.stack.append(node.name)
        self.generic_visit(node)
        self.stack.pop()

    visit_ClassDef = _visit_symbol
    visit_FunctionDef = _visit_symbol
    visit_AsyncFunctionDef = _visit_symbol


class PythonExtractor:
    kind = "python"

    def extract(self, source: SourceDefinition, content: bytes) -> dict[str, Any]:
        text = content.decode("utf-8")
        tree = ast.parse(text, filename=source.relative_path)
        module = source.relative_path.removesuffix(".py").replace("/", ".")
        if module.endswith(".__init__"):
            module = module[: -len(".__init__")]
        visitor = _SymbolVisitor(module)
        visitor.visit(tree)
        contribution = _base(source, content)
        artifact = contribution["artifact"]
        file_entity_id = stable_id("codefile", [source.relative_path])
        semantic = _sha256_json(
            [[item["symbol_id"], item["semantic_sha256"]] for item in visitor.symbols]
        )
        artifact["semantic_sha256"] = semantic
        contribution["code_file"] = {
            "code_file_id": file_entity_id,
            "entity_id": file_entity_id,
            "artifact_id": artifact["artifact_id"],
            "language": "python",
            "import_name": module,
        }
        contribution["entities"].append(
            {
                "entity_id": file_entity_id,
                "entity_kind": "code_file",
                "display_name": source.relative_path,
                "summary": "",
                "lifecycle_status": "active",
                "semantic_sha256": semantic,
                "definition": True,
            }
        )
        contribution["symbols"] = visitor.symbols
        for symbol in visitor.symbols:
            contribution["entities"].append(
                {
                    "entity_id": symbol["entity_id"],
                    "entity_kind": "code_symbol",
                    "display_name": symbol["qualified_name"],
                    "summary": symbol["signature_text"],
                    "lifecycle_status": "active",
                    "semantic_sha256": symbol["semantic_sha256"],
                    "definition": True,
                }
            )
            contribution["locators"].append(
                {
                    "locator_id": symbol["locator"]["locator_id"],
                    "locator_kind": "python_symbol",
                    "selector": symbol["locator"]["selector"],
                    "entity_id": symbol["entity_id"],
                    "locator_role": "definition",
                }
            )
            contribution["search"].append(
                {
                    "entity_id": symbol["entity_id"],
                    "title": symbol["qualified_name"],
                    "summary": symbol["signature_text"],
                    "tags": f"python {symbol['symbol_kind']}",
                }
            )
        return contribution


def _pointer_token(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


_INDEXED_JSON_KEYS = {
    "id",
    "schema_id",
    "status",
    "event",
    "event_uid",
    "idempotency_key",
    "work_item",
    "work_item_id",
    "task",
    "task_id",
    "requirement_id",
    "field_id",
    "entity_id",
    "source_id",
    "project_id",
    "generation_id",
}

_DETAIL_KEYS = {
    "acceptance_criteria",
    "activities",
    "activity",
    "actual",
    "background",
    "blockers",
    "code",
    "completion_conditions",
    "context",
    "dependencies",
    "description",
    "design",
    "done_definition",
    "expected",
    "expected_result",
    "goal",
    "implementation",
    "next",
    "next_action",
    "non_goals",
    "objective",
    "out_of_scope",
    "outcome",
    "owner",
    "priority",
    "problem",
    "reason",
    "release",
    "result",
    "scope",
    "statement",
    "summary",
    "tasks",
    "tests",
    "user_scenario",
    "user_scenarios",
    "why",
}


def _bounded_detail(value: Any, *, depth: int = 0) -> Any:
    if depth >= 4:
        return "[内容层级已截断]"
    if isinstance(value, dict):
        return {
            str(key): _bounded_detail(item, depth=depth + 1)
            for key, item in list(value.items())[:40]
        }
    if isinstance(value, list):
        return [_bounded_detail(item, depth=depth + 1) for item in value[:25]]
    if isinstance(value, str):
        return value[:4000]
    return value


def _business_details(value: Mapping[str, Any]) -> dict[str, Any]:
    return {
        str(key): _bounded_detail(item)
        for key, item in value.items()
        if str(key).casefold() in _DETAIL_KEYS
    }


def _json_records(value: object, pointer: str = "") -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key in sorted(value):
            records.extend(_json_records(value[key], f"{pointer}/{_pointer_token(str(key))}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            records.extend(_json_records(item, f"{pointer}/{index}"))
    else:
        final_token = pointer.rsplit("/", 1)[-1].replace("~1", "/").replace("~0", "~")
        if final_token not in _INDEXED_JSON_KEYS and not final_token.endswith("_id"):
            return records
        records.append(
            {
                "pointer": pointer or "",
                "value_type": type(value).__name__,
                "value_sha256": _sha256_json(value),
            }
        )
    return records


def _json_objects(value: object, pointer: str = "") -> list[dict[str, Any]]:
    objects: list[dict[str, Any]] = []
    if isinstance(value, dict):
        record_id = value.get("id")
        if isinstance(record_id, str) and record_id:
            title_value = value.get("title") or value.get("label") or value.get("statement")
            title = str(title_value) if title_value is not None else record_id
            status_value = value.get("status")
            objects.append(
                {
                    "pointer": pointer or "",
                    "record_id": record_id,
                    "title": title[:500],
                    "status": str(status_value) if status_value is not None else "unknown",
                    "priority": value.get("priority"),
                    "details": _business_details(value),
                    "semantic_sha256": _sha256_json(value),
                }
            )
        for key in sorted(value):
            objects.extend(_json_objects(value[key], f"{pointer}/{_pointer_token(str(key))}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            objects.extend(_json_objects(item, f"{pointer}/{index}"))
    return objects


def _json_entity_kind(record_id: str) -> str:
    if "-AC-" in record_id:
        return "acceptance_criterion"
    if record_id.startswith("REQ-"):
        return "requirement"
    if record_id.startswith("NFR-"):
        return "non_functional_requirement"
    if record_id.startswith("TASK-"):
        return "work_item"
    return "json_record"


_HUMAN_LABELS = {
    "active": "进行中",
    "approved": "已批准",
    "approved_ready_for_commit": "已批准，等待本地提交",
    "changes_requested": "需要修改",
    "commit": "本地提交",
    "committed": "已本地提交",
    "done": "已完成",
    "human_approved": "人工已确认",
    "human_confirmation": "人工确认",
    "in_progress": "进行中",
    "independent_re_review": "独立复审",
    "independent_review": "独立评审",
    "pending_human_confirmation": "等待人工确认",
    "ready_for_review": "等待独立评审",
    "review": "独立评审",
    "review_feedback_fixed": "评审意见已修复",
    "task_started": "任务已开始",
    "verified": "验证已完成",
    "workitem_created": "工作项已创建",
}

_HUMAN_WORDS = {
    "destructive": "破坏性",
    "doc": "文档",
    "factory": "体系",
    "full": "完整",
    "implement": "实施",
    "migration": "迁移",
    "project": "项目",
    "rebuild": "重建",
    "sync": "同步",
    "validate": "验证",
}


def _human_label(value: object) -> str:
    token = str(value or "未登记").strip()
    normalized = token.casefold()
    if normalized in _HUMAN_LABELS:
        return _HUMAN_LABELS[normalized]
    parts = normalized.split("_")
    if any(part in _HUMAN_WORDS for part in parts):
        return " ".join(_HUMAN_WORDS.get(part, part) for part in parts)
    return token.replace("_", " ").lower()


def _work_item_summary(event: Mapping[str, Any]) -> str:
    status = _human_label(event.get("status"))
    next_value = event.get("next_action") or event.get("next_required_action") or event.get("next")
    next_action = _human_label(next_value) if next_value else "未登记"
    explicit = event.get("summary") or event.get("feedback") or event.get("reason")
    if explicit:
        return f"{str(explicit).strip()} 当前状态：{status}；下一步：{next_action}。"[:1000]
    event_name = (
        event.get("event") or event.get("event_type") or event.get("action") or "状态已更新"
    )
    return (f"最近进展：{_human_label(event_name)}；当前状态：{status}；下一步：{next_action}。")[
        :1000
    ]


class JsonExtractor:
    kind = "json"

    def extract(self, source: SourceDefinition, content: bytes) -> dict[str, Any]:
        payload = json.loads(content)
        contribution = _base(source, content)
        if (
            isinstance(payload, dict)
            and payload.get("schema_id") == "ProjectKnowledgeRelationDeclarations/v1"
        ):
            raw_relations = payload.get("relations")
            if not isinstance(raw_relations, list):
                raise ValueError("relation declarations must contain a relations array")
            relations: list[dict[str, Any]] = []
            for raw_relation in raw_relations:
                if not isinstance(raw_relation, dict):
                    raise ValueError("relation declaration must be an object")
                confidence = float(raw_relation.get("confidence", 1.0))
                if confidence < 0 or confidence > 1:
                    raise ValueError("relation confidence must be between zero and one")
                strength = str(raw_relation.get("strength", "strong"))
                if strength not in {"strong", "weak"}:
                    raise ValueError("relation strength must be strong or weak")
                relations.append(
                    {
                        "from_entity_id": str(raw_relation["from_entity_id"]),
                        "to_entity_id": str(raw_relation["to_entity_id"]),
                        "relation_type": str(raw_relation["relation_type"]).upper(),
                        "strength": strength,
                        "confidence": confidence,
                        "evidence_locator_id": raw_relation.get("evidence_locator_id"),
                    }
                )
            contribution["relations"] = relations
        if isinstance(payload, dict) and payload.get("schema_id") == "ProjectKnowledgeIdAliases/v1":
            raw_aliases = payload.get("aliases")
            if not isinstance(raw_aliases, list):
                raise ValueError("id aliases must contain an aliases array")
            aliases: list[dict[str, str]] = []
            for raw_alias in raw_aliases:
                if not isinstance(raw_alias, dict):
                    raise ValueError("id alias must be an object")
                alias_id = str(raw_alias.get("alias_entity_id") or raw_alias.get("alias") or "")
                canonical_id = str(
                    raw_alias.get("canonical_entity_id") or raw_alias.get("canonical") or ""
                )
                if not alias_id or not canonical_id or alias_id == canonical_id:
                    raise ValueError("id alias requires different alias and canonical entity IDs")
                aliases.append(
                    {
                        "alias_entity_id": alias_id,
                        "canonical_entity_id": canonical_id,
                        "reason": str(raw_alias.get("reason") or "declared alias"),
                    }
                )
            contribution["aliases"] = aliases
        if isinstance(payload, dict) and source.relative_path.endswith(".factory/project.json"):
            project_id = payload.get("project_id") or payload.get("project_name")
            if isinstance(project_id, str) and project_id:
                contribution["project_id"] = project_id
        records = _json_records(payload)
        objects = _json_objects(payload)
        contribution["records"] = records
        contribution["objects"] = objects
        contribution["artifact"]["semantic_sha256"] = _sha256_json(
            [records, objects, contribution.get("relations", [])]
        )
        for record in objects:
            selector = {
                "kind": "json_pointer",
                "source_id": source.source_id,
                "pointer": record["pointer"],
            }
            entity_id = str(record["record_id"])
            contribution["entities"].append(
                {
                    "entity_id": entity_id,
                    "entity_kind": _json_entity_kind(entity_id),
                    "display_name": record["title"],
                    "summary": record["status"],
                    "lifecycle_status": record["status"],
                    "semantic_sha256": record["semantic_sha256"],
                    "definition": True,
                    "priority": record.get("priority"),
                    "details": record.get("details", {}),
                }
            )
            contribution["locators"].append(
                {
                    "locator_id": stable_id("locator", selector),
                    "locator_kind": "json_pointer",
                    "selector": selector,
                    "entity_id": entity_id,
                    "locator_role": "definition",
                }
            )
            contribution["search"].append(
                {
                    "entity_id": entity_id,
                    "title": record["title"],
                    "summary": record["status"],
                    "tags": _json_entity_kind(entity_id),
                }
            )
        for record in records:
            selector = {
                "kind": "json_pointer",
                "source_id": source.source_id,
                "pointer": record["pointer"],
            }
            entity_id = stable_id("json", [source.source_id, record["pointer"]])
            contribution["entities"].append(
                {
                    "entity_id": entity_id,
                    "entity_kind": "json_value",
                    "display_name": record["pointer"] or "/",
                    "summary": record["value_type"],
                    "lifecycle_status": "active",
                    "semantic_sha256": record["value_sha256"],
                    "definition": True,
                }
            )
            contribution["locators"].append(
                {
                    "locator_id": stable_id("locator", [source.source_id, selector]),
                    "locator_kind": "json_pointer",
                    "selector": selector,
                    "entity_id": entity_id,
                    "locator_role": "definition",
                }
            )
        return contribution


class JsonLinesExtractor:
    kind = "jsonl"

    def extract(self, source: SourceDefinition, content: bytes) -> dict[str, Any]:
        contribution = _base(source, content)
        events: list[dict[str, Any]] = []
        latest_work_items: dict[str, dict[str, Any]] = {}
        missing_event_uid_count = 0
        derived_uid_occurrences: dict[str, int] = {}
        for raw_line in content.decode("utf-8").splitlines():
            if not raw_line.strip():
                continue
            event = json.loads(raw_line)
            semantic = _sha256_json(event)
            event_uid = (
                event.get("event_uid") or event.get("idempotency_key") or event.get("action_key")
            )
            if not isinstance(event_uid, str) or not event_uid:
                missing_event_uid_count += 1
                occurrence = derived_uid_occurrences.get(semantic, 0) + 1
                derived_uid_occurrences[semantic] = occurrence
                event_uid = f"derived:{semantic}:{occurrence}"
            work_item = event.get("task") or event.get("work_item") or event.get("workitem")
            display_name = str(work_item or event_uid)
            safe_summary = _work_item_summary(event)
            safe_details = _business_details(event)
            updated_at = event.get("ts") or event.get("timestamp") or event.get("updated_at")
            if isinstance(updated_at, str) and updated_at:
                safe_details["updated_at"] = updated_at
            task_title = event.get("task_title") or event.get("title")
            if isinstance(task_title, str) and task_title.strip():
                safe_details["task_title"] = task_title.strip()
            events.append(
                {
                    "event_uid": event_uid,
                    "event_type": str(
                        event.get("event")
                        or event.get("event_type")
                        or event.get("action")
                        or event.get("type")
                        or "event"
                    ),
                    "work_item": display_name,
                    "safe_summary": safe_summary,
                    "semantic_sha256": semantic,
                    "details": safe_details,
                }
            )
            if work_item:
                latest_work_items[display_name] = {
                    "summary": safe_summary,
                    "status": str(event.get("status") or "unknown"),
                    "semantic_sha256": semantic,
                    "event_uid": event_uid,
                    "details": safe_details,
                }
            entity_id = stable_id("event", [source.source_id, event_uid])
            contribution["entities"].append(
                {
                    "entity_id": entity_id,
                    "entity_kind": "event",
                    "display_name": display_name,
                    "summary": safe_summary,
                    "lifecycle_status": "observed",
                    "semantic_sha256": semantic,
                    "definition": True,
                    "details": safe_details,
                }
            )
            contribution["search"].append(
                {
                    "entity_id": entity_id,
                    "title": display_name,
                    "summary": safe_summary,
                    "tags": "work-item ledger event",
                }
            )
        for work_item, latest in latest_work_items.items():
            entity_id = stable_id("workitem", [source.source_id, work_item])
            selector = {
                "kind": "jsonl_event",
                "source_id": source.source_id,
                "event_uid": latest["event_uid"],
            }
            contribution["entities"].append(
                {
                    "entity_id": entity_id,
                    "entity_kind": "work_item",
                    "display_name": work_item,
                    "summary": latest["summary"],
                    "lifecycle_status": latest["status"],
                    "semantic_sha256": latest["semantic_sha256"],
                    "definition": True,
                    "details": latest["details"],
                }
            )
            contribution["locators"].append(
                {
                    "locator_id": stable_id("locator", selector),
                    "locator_kind": "jsonl_event",
                    "selector": selector,
                    "entity_id": entity_id,
                    "locator_role": "definition",
                }
            )
            contribution["search"].append(
                {
                    "entity_id": entity_id,
                    "title": work_item,
                    "summary": latest["summary"],
                    "tags": "work-item current ledger",
                }
            )
        contribution["events"] = events
        if missing_event_uid_count:
            contribution["diagnostics"].append(
                {
                    "code": "JSONL_EVENT_UID_MISSING",
                    "severity": "warning",
                    "safe_message": (
                        f"{missing_event_uid_count} JSONL events use a deterministic derived UID; "
                        "new events should provide an explicit stable UID"
                    ),
                }
            )
        contribution["artifact"]["semantic_sha256"] = _sha256_json(events)
        return contribution


class GitExtractor:
    """Extract pre-normalized git facts supplied as JSON without reading git itself."""

    kind = "git"

    def extract(self, source: SourceDefinition, content: bytes) -> dict[str, Any]:
        payload = json.loads(content)
        commits = payload if isinstance(payload, list) else [payload]
        normalized: list[dict[str, str]] = []
        for commit in commits:
            if not isinstance(commit, Mapping):
                raise ValueError("git fact must be an object")
            normalized.append(
                {
                    "commit": str(commit["commit"]),
                    "blob": str(commit["blob"]),
                    "path": str(commit["path"]),
                }
            )
        contribution = _base(source, content)
        contribution["revisions"] = normalized
        contribution["artifact"]["semantic_sha256"] = _sha256_json(normalized)
        return contribution


class ExtractorRegistry:
    def __init__(self, extractors: tuple[Extractor, ...]) -> None:
        self._extractors = {extractor.kind: extractor for extractor in extractors}

    def extract(self, source: SourceDefinition, content: bytes) -> dict[str, Any]:
        extractor = self._extractors.get(source.kind)
        if extractor is None:
            raise ValueError(f"no extractor registered for source kind {source.kind!r}")
        contribution = extractor.extract(source, content)
        if contribution.get("schema_id") != "SourceContribution/v1":
            raise ValueError("extractor returned an unsupported contribution schema")
        sanitized = sanitize_value(contribution)
        if not isinstance(sanitized, dict):  # pragma: no cover - structural invariant
            raise TypeError("sanitized contribution must remain an object")
        return sanitized


def default_extractors() -> ExtractorRegistry:
    return ExtractorRegistry(
        (
            MarkdownExtractor(),
            JsonExtractor(),
            JsonLinesExtractor(),
            PythonExtractor(),
            GitExtractor(),
        )
    )
