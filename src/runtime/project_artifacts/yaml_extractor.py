"""YAML extraction for design, OpenAPI, and test artifact contracts."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping, Sequence
from typing import Any

import yaml

from domain.project_artifacts.validation import (
    validate_design_manifest,
    validate_openapi,
    validate_test_case_catalog,
)
from domain.project_knowledge.models import SourceDefinition, canonical_json, stable_id
from runtime.project_knowledge.extractors import (
    ExtractorRegistry,
    GitExtractor,
    JsonExtractor,
    JsonLinesExtractor,
    MarkdownExtractor,
    PythonExtractor,
)

_HTTP_METHODS = frozenset({"get", "post", "put", "patch", "delete", "head", "options", "trace"})


def _sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _sha256_json(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _mapping(value: object) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _string_list(value: object) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        return []
    return [str(item) for item in value if isinstance(item, str) and item]


def _base(source: SourceDefinition, content: bytes) -> dict[str, Any]:
    content_sha256 = _sha256_bytes(content)
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
        "content_sha256": content_sha256,
        "artifact": {
            "artifact_id": stable_id("artifact", [source.source_id, source.relative_path]),
            "artifact_kind": source.kind,
            "relative_path": source.relative_path,
            "content_sha256": content_sha256,
            "access_class": source.access_class.value,
        },
        "entities": [],
        "locators": [],
        "search": [],
        "diagnostics": [],
        "relations": [],
    }


def _locator(entity_id: str, path: list[str | int]) -> dict[str, Any]:
    selector = {"kind": "yaml_path", "path": path}
    return {
        "locator_id": stable_id("locator", selector),
        "locator_kind": "yaml_path",
        "selector": selector,
        "entity_id": entity_id,
        "locator_role": "definition",
    }


def _relation(
    from_entity_id: str,
    to_entity_id: str,
    relation_type: str,
) -> dict[str, Any]:
    return {
        "from_entity_id": from_entity_id,
        "to_entity_id": to_entity_id,
        "relation_type": relation_type,
        "strength": "strong",
        "confidence": 1.0,
        "evidence_locator_id": None,
    }


def _entity(
    *,
    entity_id: str,
    entity_kind: str,
    display_name: str,
    summary: str,
    lifecycle_status: str,
    details: Mapping[str, Any],
) -> dict[str, Any]:
    semantic = {
        "entity_id": entity_id,
        "entity_kind": entity_kind,
        "display_name": display_name,
        "summary": summary,
        "lifecycle_status": lifecycle_status,
        "details": dict(details),
    }
    return {
        **semantic,
        "semantic_sha256": _sha256_json(semantic),
        "definition": True,
    }


class YamlProjectArtifactExtractor:
    """Project typed YAML contracts into stable entities without line locators."""

    kind = "yaml"

    def __init__(
        self,
        *,
        expected_routes: set[tuple[str, str]] | frozenset[tuple[str, str]] | None = None,
        available_design_paths: set[str] | frozenset[str] = frozenset(),
    ) -> None:
        self._expected_routes = frozenset(expected_routes) if expected_routes is not None else None
        self._available_design_paths = frozenset(available_design_paths)

    def extract(self, source: SourceDefinition, content: bytes) -> dict[str, Any]:
        payload = yaml.safe_load(content.decode("utf-8"))
        if not isinstance(payload, Mapping):
            raise ValueError("project artifact YAML root must be an object")
        if payload.get("schema_id") == "DesignArtifactManifest/v1":
            self._require_valid(
                validate_design_manifest(
                    payload,
                    available_paths=self._available_design_paths,
                )
            )
            contribution = self._design_manifest(source, content, payload)
        elif str(payload.get("openapi") or "").startswith("3.1."):
            self._require_valid(validate_openapi(payload, expected_routes=self._expected_routes))
            contribution = self._openapi(source, content, payload)
        elif payload.get("schema_id") == "TestCaseCatalog/v1":
            self._require_valid(validate_test_case_catalog(payload))
            contribution = self._test_catalog(source, content, payload)
        else:
            raise ValueError(f"unsupported project artifact YAML schema: {source.relative_path}")
        contribution["artifact"]["semantic_sha256"] = _sha256_json(
            {
                "entities": contribution["entities"],
                "relations": contribution["relations"],
            }
        )
        return contribution

    @staticmethod
    def _require_valid(report: object) -> None:
        if not getattr(report, "valid", False):
            codes = ",".join(str(issue.code) for issue in getattr(report, "issues", ()))
            raise ValueError(f"project artifact contract validation failed: {codes}")

    def _design_manifest(
        self,
        source: SourceDefinition,
        content: bytes,
        payload: Mapping[str, Any],
    ) -> dict[str, Any]:
        contribution = _base(source, content)
        root_id = str(payload["id"])
        document_id = str(payload["document_id"])
        title = str(payload["title"])
        status = str(payload["status"])
        source_details = _mapping(payload.get("source"))
        root_details = {
            "document_id": document_id,
            "source_format": source_details.get("format"),
            "source_file": source_details.get("file"),
            "connection_required": source_details.get("connection_required"),
            "tokens_file": payload.get("tokens_file"),
            "export_count": len(payload.get("exports") or []),
        }
        contribution["entities"].append(
            _entity(
                entity_id=root_id,
                entity_kind="design_asset",
                display_name=title,
                summary=(
                    "等待连接真实 Penpot 文件"
                    if status == "awaiting_penpot_connection"
                    else f"设计资产状态：{status}"
                ),
                lifecycle_status=status,
                details=root_details,
            )
        )
        contribution["locators"].append(_locator(root_id, []))
        contribution["search"].append(
            {
                "entity_id": root_id,
                "title": title,
                "summary": str(contribution["entities"][-1]["summary"]),
                "tags": "设计 UX UI Penpot",
            }
        )
        contribution["relations"].append(_relation(f"doc:{document_id}", root_id, "CONTAINS"))
        for collection, entity_kind in (
            ("pages", "ui_page"),
            ("components", "ui_component"),
        ):
            for index, raw_item in enumerate(payload.get(collection) or []):
                item = _mapping(raw_item)
                entity_id = str(item["id"])
                item_title = str(item["title"])
                purpose = str(item["purpose"])
                details: dict[str, Any] = {"purpose": purpose}
                if collection == "components":
                    details["states"] = _string_list(item.get("states"))
                contribution["entities"].append(
                    _entity(
                        entity_id=entity_id,
                        entity_kind=entity_kind,
                        display_name=item_title,
                        summary=purpose,
                        lifecycle_status=status,
                        details=details,
                    )
                )
                contribution["locators"].append(_locator(entity_id, [collection, index]))
                contribution["search"].append(
                    {
                        "entity_id": entity_id,
                        "title": item_title,
                        "summary": purpose,
                        "tags": "UX UI 页面" if collection == "pages" else "UI 组件 状态",
                    }
                )
                contribution["relations"].append(_relation(root_id, entity_id, "CONTAINS"))
        return contribution

    def _openapi(
        self,
        source: SourceDefinition,
        content: bytes,
        payload: Mapping[str, Any],
    ) -> dict[str, Any]:
        contribution = _base(source, content)
        document_id = str(payload.get("x-shanforge-document-id") or "DESIGN-API-001")
        for route_path, raw_path_item in _mapping(payload.get("paths")).items():
            for method, raw_operation in _mapping(raw_path_item).items():
                if str(method).casefold() not in _HTTP_METHODS:
                    continue
                operation = _mapping(raw_operation)
                entity_id = str(operation["x-shanforge-id"])
                title = str(operation["summary"])
                description = str(operation["description"])
                requirements = _string_list(operation.get("x-shanforge-requirements"))
                details: dict[str, Any] = {
                    "method": str(method).upper(),
                    "path": str(route_path),
                    "operation_id": operation.get("operationId"),
                    "owner": operation.get("x-shanforge-owner"),
                    "requirements": requirements,
                    "tests": _string_list(operation.get("x-shanforge-tests")),
                }
                contribution["entities"].append(
                    _entity(
                        entity_id=entity_id,
                        entity_kind="api_operation",
                        display_name=title,
                        summary=description,
                        lifecycle_status="active",
                        details=details,
                    )
                )
                contribution["locators"].append(
                    _locator(entity_id, ["paths", str(route_path), str(method)])
                )
                contribution["search"].append(
                    {
                        "entity_id": entity_id,
                        "title": title,
                        "summary": description,
                        "tags": (
                            f"API {str(method).upper()} {route_path} "
                            f"{operation.get('operationId', '')}"
                        ),
                    }
                )
                contribution["relations"].append(
                    _relation(f"doc:{document_id}", entity_id, "CONTAINS")
                )
                for requirement_id in requirements:
                    contribution["relations"].append(
                        _relation(entity_id, requirement_id, "SATISFIES")
                    )
        return contribution

    def _test_catalog(
        self,
        source: SourceDefinition,
        content: bytes,
        payload: Mapping[str, Any],
    ) -> dict[str, Any]:
        contribution = _base(source, content)
        for index, raw_case in enumerate(payload.get("cases") or []):
            case = _mapping(raw_case)
            entity_id = str(case["id"])
            title = str(case["title"])
            objective = str(case["objective"])
            contribution["entities"].append(
                _entity(
                    entity_id=entity_id,
                    entity_kind="test",
                    display_name=title,
                    summary=objective,
                    lifecycle_status=str(case["definition_status"]),
                    details={
                        "version": case.get("version"),
                        "type": case.get("type"),
                        "level": case.get("level"),
                        "priority": case.get("priority"),
                        "risk": case.get("risk"),
                        "owner": case.get("owner"),
                        "definition_status": case.get("definition_status"),
                        "traceability": dict(_mapping(case.get("traceability"))),
                    },
                )
            )
            contribution["locators"].append(_locator(entity_id, ["cases", index]))
            contribution["search"].append(
                {
                    "entity_id": entity_id,
                    "title": title,
                    "summary": objective,
                    "tags": f"测试 {case.get('type', '')} {case.get('level', '')}",
                }
            )
            traceability = _mapping(case.get("traceability"))
            for trace_kind, raw_targets in traceability.items():
                for target_id in _string_list(raw_targets):
                    relation_target = f"doc:{target_id}" if trace_kind == "designs" else target_id
                    contribution["relations"].append(
                        _relation(entity_id, relation_target, "VERIFIES")
                    )
            contribution.setdefault("tests", []).append(
                {
                    "test_id": entity_id,
                    "entity_id": entity_id,
                    "framework": "catalog",
                    "test_kind": str(case.get("type") or "manual"),
                    "test_status": f"definition:{case.get('definition_status')}",
                    "code_symbol_id": None,
                    "last_evidence_entity_id": None,
                }
            )
        return contribution


def project_artifact_extractors(
    *,
    expected_routes: set[tuple[str, str]] | frozenset[tuple[str, str]] | None = None,
    available_design_paths: set[str] | frozenset[str] = frozenset(),
) -> ExtractorRegistry:
    """Return the existing extractor set plus typed YAML project artifacts."""

    return ExtractorRegistry(
        (
            MarkdownExtractor(),
            JsonExtractor(),
            JsonLinesExtractor(),
            PythonExtractor(),
            GitExtractor(),
            YamlProjectArtifactExtractor(
                expected_routes=expected_routes,
                available_design_paths=available_design_paths,
            ),
        )
    )
