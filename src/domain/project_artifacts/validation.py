"""Pure validation rules for repository-owned project artifacts."""

from __future__ import annotations

import math
import re
from collections import Counter
from collections.abc import Iterable, Mapping, Set
from datetime import datetime
from pathlib import PurePosixPath
from typing import Any

from domain.project_artifacts.models import (
    ArtifactValidationIssue,
    ArtifactValidationReport,
    ValidatedTestResult,
)

_HTTP_METHODS = frozenset({"get", "post", "put", "patch", "delete", "head", "options", "trace"})
_TEST_RESULT_STATUSES = frozenset(
    {"passed", "failed", "error", "blocked", "skipped", "not_run", "cancelled"}
)
_TEST_TYPES = frozenset(
    {
        "unit",
        "contract",
        "integration",
        "system",
        "acceptance",
        "usability",
        "accessibility",
        "security",
        "performance",
        "regression",
    }
)
_TEST_LEVELS = frozenset({"unit", "component", "integration", "system", "acceptance"})
_TEST_PRIORITIES = frozenset({"P0", "P1", "P2", "P3"})
_TEST_RISKS = frozenset({"low", "medium", "high", "critical"})
_DEFINITION_STATUSES = frozenset({"draft", "active", "deprecated", "retired"})
_AUTOMATION_STATUSES = frozenset({"manual", "planned", "automated", "partial"})
_DESIGN_STATES = frozenset(
    {
        "default",
        "loading",
        "empty",
        "error",
        "disabled",
        "focus",
        "hover",
        "pressed",
        "success",
        "blocked",
    }
)
_DESIGN_EXPORT_FORMATS = frozenset({"svg", "png", "webp", "pdf"})
_DESIGN_EXPORT_KINDS = frozenset({"page", "component", "asset"})
_DESIGN_ROOT_FIELDS = frozenset(
    {
        "schema_id",
        "id",
        "title",
        "status",
        "document_id",
        "source",
        "pages",
        "components",
        "tokens_file",
        "exports",
    }
)


class _Issues:
    def __init__(self) -> None:
        self._values: list[ArtifactValidationIssue] = []

    def add(self, code: str, path: str, message: str) -> None:
        self._values.append(ArtifactValidationIssue(code=code, path=path, message=message))

    def require_text(
        self,
        value: object,
        *,
        code: str,
        path: str,
        message: str,
        min_length: int = 1,
    ) -> str:
        text = str(value).strip() if isinstance(value, str) else ""
        if len(text) < min_length:
            self.add(code, path, message)
        return text

    def report(self, *, artifact_kind: str, subject_count: int) -> ArtifactValidationReport:
        ordered = tuple(sorted(self._values, key=lambda item: (item.path, item.code, item.message)))
        return ArtifactValidationReport(
            schema_id="ArtifactValidationReport/v1",
            artifact_kind=artifact_kind,
            valid=not ordered,
            subject_count=subject_count,
            issues=ordered,
        )


def _is_repository_path(value: object, *, prefix: str | None = None) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "." in path.parts:
        return False
    normalized = path.as_posix()
    return prefix is None or normalized == prefix or normalized.startswith(f"{prefix}/")


def _has_chinese(value: object) -> bool:
    return isinstance(value, str) and bool(re.search(r"[\u3400-\u9fff]", value))


def _mapping(value: object) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _list(value: object) -> list[Any]:
    return list(value) if isinstance(value, list) else []


def _nonempty_string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _duplicate_values(values: Iterable[str]) -> set[str]:
    counts = Counter(values)
    return {value for value, count in counts.items() if count > 1}


def _require_mapping(
    issues: _Issues,
    payload: Mapping[str, Any],
    field: str,
    *,
    path: str,
) -> Mapping[str, Any]:
    value = payload.get(field)
    if not isinstance(value, Mapping):
        issues.add("OBJECT_REQUIRED", path, f"{field} 必须是对象。")
        return {}
    return value


def _require_list(
    issues: _Issues,
    payload: Mapping[str, Any],
    field: str,
    *,
    path: str,
) -> list[Any]:
    value = payload.get(field)
    if not isinstance(value, list):
        issues.add("ARRAY_REQUIRED", path, f"{field} 必须是数组。")
        return []
    return value


def _reject_unknown_fields(
    issues: _Issues,
    payload: Mapping[str, Any],
    allowed: Set[str] | frozenset[str],
    *,
    path: str,
) -> None:
    for field in sorted(set(payload) - set(allowed)):
        issues.add(
            "UNKNOWN_FIELD",
            f"{path}/{field}" if path else f"/{field}",
            f"不支持字段 {field}。",
        )


def validate_design_manifest(
    payload: Mapping[str, Any],
    *,
    available_paths: Set[str] | set[str] | frozenset[str],
) -> ArtifactValidationReport:
    issues = _Issues()
    _reject_unknown_fields(issues, payload, _DESIGN_ROOT_FIELDS, path="")
    if payload.get("schema_id") != "DesignArtifactManifest/v1":
        issues.add(
            "UNSUPPORTED_SCHEMA",
            "/schema_id",
            "设计资产必须使用 DesignArtifactManifest/v1。",
        )
    design_id = issues.require_text(
        payload.get("id"),
        code="DESIGN_ID_REQUIRED",
        path="/id",
        message="设计资产必须有稳定 ID。",
    )
    if design_id and re.fullmatch(r"^DESIGN-ASSET-[A-Z0-9-]+$", design_id) is None:
        issues.add("INVALID_DESIGN_ID", "/id", "设计资产 ID 不符合稳定前缀规则。")
    title = issues.require_text(
        payload.get("title"),
        code="DESIGN_TITLE_REQUIRED",
        path="/title",
        message="设计资产必须有人类可读标题。",
    )
    if title and not _has_chinese(title):
        issues.add("CHINESE_TITLE_REQUIRED", "/title", "设计资产标题必须包含中文。")
    document_id = issues.require_text(
        payload.get("document_id"),
        code="DOCUMENT_ID_REQUIRED",
        path="/document_id",
        message="设计资产必须绑定正式 UX/UI 文档。",
    )
    if document_id and re.fullmatch(r"^DESIGN-[A-Z0-9-]+$", document_id) is None:
        issues.add("INVALID_DOCUMENT_ID", "/document_id", "设计文档 ID 不符合稳定前缀规则。")
    status = str(payload.get("status") or "")
    if status not in {"awaiting_penpot_connection", "draft", "ready", "deprecated"}:
        issues.add("INVALID_DESIGN_STATUS", "/status", "设计资产状态不受支持。")

    source = _require_mapping(issues, payload, "source", path="/source")
    _reject_unknown_fields(
        issues,
        source,
        frozenset({"format", "file", "connection_required"}),
        path="/source",
    )
    for field in ("format", "file", "connection_required"):
        if field not in source:
            issues.add(
                "REQUIRED_FIELD_MISSING",
                f"/source/{field}",
                f"设计源必须声明 {field}。",
            )
    if source.get("format") != "penpot":
        issues.add("PENPOT_FORMAT_REQUIRED", "/source/format", "设计源格式必须是 penpot。")
    source_file = source.get("file")
    if source_file is not None and not isinstance(source_file, str):
        issues.add("INVALID_SOURCE_FILE", "/source/file", "设计源文件必须是字符串或 null。")
    elif source_file is not None:
        if not _is_repository_path(source_file, prefix="design/ux-ui"):
            issues.add(
                "UNSAFE_REPOSITORY_PATH",
                "/source/file",
                "Penpot 源文件必须位于 design/ux-ui 且不能越出仓库。",
            )
        if not str(source_file).endswith(".penpot"):
            issues.add("PENPOT_EXTENSION_REQUIRED", "/source/file", "设计源必须是 .penpot。")
        if str(source_file) not in available_paths:
            issues.add(
                "PENPOT_SOURCE_NOT_FOUND",
                "/source/file",
                "manifest 声明的 Penpot 源文件不存在。",
            )
    elif status in {"ready", "deprecated"}:
        issues.add(
            "PENPOT_SOURCE_NOT_FOUND",
            "/source/file",
            "ready 或 deprecated 状态必须绑定真实 .penpot 文件。",
        )
    if status == "awaiting_penpot_connection":
        if source_file is not None or source.get("connection_required") is not True:
            issues.add(
                "INVALID_UNCONNECTED_STATE",
                "/source",
                "等待连接状态不能声称已有源文件，且必须标明 connection_required。",
            )
    elif status in {"ready", "deprecated"} and source.get("connection_required") is not False:
        issues.add(
            "INVALID_CONNECTED_STATE",
            "/source/connection_required",
            "已有真实 Penpot 源的状态必须标明无需连接。",
        )
    if not isinstance(source.get("connection_required"), bool):
        issues.add(
            "CONNECTION_FLAG_REQUIRED",
            "/source/connection_required",
            "connection_required 必须是布尔值。",
        )

    tokens_file = payload.get("tokens_file")
    if not _is_repository_path(tokens_file, prefix="design/ux-ui"):
        issues.add(
            "UNSAFE_REPOSITORY_PATH",
            "/tokens_file",
            "Token 文件必须位于 design/ux-ui。",
        )
    elif str(tokens_file) not in available_paths:
        issues.add("TOKENS_FILE_NOT_FOUND", "/tokens_file", "Token 文件不存在。")

    subject_ids: list[str] = []
    for collection_name in ("pages", "components"):
        values = _require_list(
            issues,
            payload,
            collection_name,
            path=f"/{collection_name}",
        )
        for index, raw in enumerate(values):
            item = _mapping(raw)
            base = f"/{collection_name}/{index}"
            allowed = (
                frozenset({"id", "title", "purpose"})
                if collection_name == "pages"
                else frozenset({"id", "title", "purpose", "states"})
            )
            _reject_unknown_fields(issues, item, allowed, path=base)
            item_id = issues.require_text(
                item.get("id"),
                code="DESIGN_SUBJECT_ID_REQUIRED",
                path=f"{base}/id",
                message="设计页面和组件必须有稳定 ID。",
            )
            if item_id:
                subject_ids.append(item_id)
                expected_pattern = (
                    r"^UI-PAGE-[A-Z0-9-]+$"
                    if collection_name == "pages"
                    else r"^UI-COMPONENT-[A-Z0-9-]+$"
                )
                if re.fullmatch(expected_pattern, item_id) is None:
                    issues.add(
                        "INVALID_DESIGN_SUBJECT_ID",
                        f"{base}/id",
                        "设计对象 ID 不符合稳定前缀规则。",
                    )
            item_title = issues.require_text(
                item.get("title"),
                code="DESIGN_SUBJECT_TITLE_REQUIRED",
                path=f"{base}/title",
                message="设计页面和组件必须有人类可读标题。",
            )
            if item_title and not _has_chinese(item_title):
                issues.add(
                    "CHINESE_TITLE_REQUIRED",
                    f"{base}/title",
                    "设计页面和组件标题必须包含中文。",
                )
            issues.require_text(
                item.get("purpose"),
                code="DESIGN_SUBJECT_PURPOSE_REQUIRED",
                path=f"{base}/purpose",
                message="设计页面和组件必须说明用途。",
            )
            if collection_name == "components":
                raw_states = item.get("states")
                if not isinstance(raw_states, list):
                    issues.add(
                        "COMPONENT_STATES_REQUIRED",
                        f"{base}/states",
                        "设计组件必须声明状态数组。",
                    )
                    states: list[str] = []
                else:
                    states = _nonempty_string_list(raw_states)
                    if len(states) != len(raw_states):
                        issues.add(
                            "INVALID_COMPONENT_STATE",
                            f"{base}/states",
                            "设计组件状态必须是非空字符串。",
                        )
                if not states:
                    issues.add(
                        "COMPONENT_STATES_REQUIRED",
                        f"{base}/states",
                        "设计组件必须声明至少一个状态。",
                    )
                unsupported_states = sorted(set(states) - _DESIGN_STATES)
                if unsupported_states:
                    issues.add(
                        "INVALID_COMPONENT_STATE",
                        f"{base}/states",
                        f"设计组件包含不受支持的状态：{unsupported_states}。",
                    )
                duplicate_states = sorted(_duplicate_values(states))
                if duplicate_states:
                    issues.add(
                        "DUPLICATE_COMPONENT_STATE",
                        f"{base}/states",
                        f"设计组件状态不能重复：{duplicate_states}。",
                    )
    for duplicate in sorted(_duplicate_values(subject_ids)):
        issues.add(
            "DUPLICATE_DESIGN_SUBJECT_ID",
            "/pages|components",
            f"设计对象 ID 重复：{duplicate}。",
        )

    for index, raw in enumerate(_require_list(issues, payload, "exports", path="/exports")):
        item = _mapping(raw)
        base = f"/exports/{index}"
        _reject_unknown_fields(
            issues,
            item,
            frozenset({"id", "kind", "subject_id", "file", "format", "purpose"}),
            path=base,
        )
        for field in ("id", "subject_id", "purpose"):
            issues.require_text(
                item.get(field),
                code=f"DESIGN_EXPORT_{field.upper()}_REQUIRED",
                path=f"{base}/{field}",
                message=f"设计导出资源必须声明 {field}。",
            )
        if str(item.get("kind") or "") not in _DESIGN_EXPORT_KINDS:
            issues.add("INVALID_EXPORT_KIND", f"{base}/kind", "设计导出资源 kind 不受支持。")
        if str(item.get("format") or "") not in _DESIGN_EXPORT_FORMATS:
            issues.add(
                "INVALID_EXPORT_FORMAT",
                f"{base}/format",
                "设计导出资源 format 不受支持。",
            )
        if str(item.get("subject_id") or "") not in set(subject_ids):
            issues.add(
                "EXPORT_SUBJECT_NOT_FOUND",
                f"{base}/subject_id",
                "设计导出资源必须引用同一 manifest 的页面或组件。",
            )
        export_path = item.get("file")
        if not _is_repository_path(export_path, prefix="design/ux-ui/exports"):
            issues.add(
                "UNSAFE_REPOSITORY_PATH",
                f"{base}/file",
                "导出资源必须位于 design/ux-ui/exports。",
            )
        elif str(export_path) not in available_paths:
            issues.add(
                "EXPORT_FILE_NOT_FOUND",
                f"{base}/file",
                "manifest 声明的导出资源不存在。",
            )
    return issues.report(artifact_kind="design", subject_count=len(subject_ids))


def validate_design_tokens(payload: Mapping[str, Any]) -> ArtifactValidationReport:
    issues = _Issues()
    allowed = frozenset(
        {
            "schema_id",
            "id",
            "title",
            "version",
            "color",
            "typography",
            "space",
            "radius",
            "motion",
        }
    )
    _reject_unknown_fields(issues, payload, allowed, path="")
    if payload.get("schema_id") != "DesignTokens/v1":
        issues.add("UNSUPPORTED_SCHEMA", "/schema_id", "设计 Token 必须使用 DesignTokens/v1。")
    token_id = issues.require_text(
        payload.get("id"),
        code="TOKEN_ID_REQUIRED",
        path="/id",
        message="设计 Token 必须有稳定 ID。",
    )
    if token_id and re.fullmatch(r"^DESIGN-TOKENS-[A-Z0-9-]+$", token_id) is None:
        issues.add("INVALID_TOKEN_ID", "/id", "设计 Token ID 不符合稳定前缀规则。")
    title = issues.require_text(
        payload.get("title"),
        code="TOKEN_TITLE_REQUIRED",
        path="/title",
        message="设计 Token 必须有人类可读标题。",
    )
    if title and not _has_chinese(title):
        issues.add("CHINESE_TITLE_REQUIRED", "/title", "设计 Token 标题必须包含中文。")
    issues.require_text(
        payload.get("version"),
        code="TOKEN_VERSION_REQUIRED",
        path="/version",
        message="设计 Token 必须声明版本。",
    )
    for field in ("color", "typography", "space", "radius", "motion"):
        values = _require_mapping(issues, payload, field, path=f"/{field}")
        if not values:
            issues.add("TOKEN_GROUP_EMPTY", f"/{field}", f"Token 分组 {field} 不能为空。")
    return issues.report(artifact_kind="design_tokens", subject_count=1)


def _validate_schema_descriptions(
    issues: _Issues,
    schema: Mapping[str, Any],
    *,
    path: str,
) -> None:
    if not _has_chinese(schema.get("description")):
        issues.add(
            "SCHEMA_DESCRIPTION_REQUIRED",
            f"{path}/description",
            "Schema 及字段必须有中文说明。",
        )
    for name, raw_property in _mapping(schema.get("properties")).items():
        _validate_schema_descriptions(
            issues,
            _mapping(raw_property),
            path=f"{path}/properties/{name}",
        )
    items = schema.get("items")
    if isinstance(items, Mapping):
        _validate_schema_descriptions(issues, items, path=f"{path}/items")


def _validate_media_content(issues: _Issues, content: object, *, path: str) -> None:
    media_types = _mapping(content)
    if not media_types:
        issues.add("CONTENT_REQUIRED", path, "请求或响应必须声明媒体类型内容。")
        return
    for media_type, raw_media in media_types.items():
        media = _mapping(raw_media)
        schema = _mapping(media.get("schema"))
        if not schema:
            issues.add("SCHEMA_REQUIRED", f"{path}/{media_type}/schema", "媒体类型必须有 Schema。")
        else:
            _validate_schema_descriptions(
                issues,
                schema,
                path=f"{path}/{media_type}/schema",
            )
        if "example" not in media and "examples" not in media:
            issues.add(
                "EXAMPLE_REQUIRED",
                f"{path}/{media_type}",
                "请求或响应必须提供示例。",
            )


def validate_openapi(
    payload: Mapping[str, Any],
    *,
    expected_routes: set[tuple[str, str]] | frozenset[tuple[str, str]] | None = None,
) -> ArtifactValidationReport:
    issues = _Issues()
    if not str(payload.get("openapi") or "").startswith("3.1."):
        issues.add("OPENAPI_31_REQUIRED", "/openapi", "接口合同必须使用 OpenAPI 3.1。")
    info = _mapping(payload.get("info"))
    if not _has_chinese(info.get("description")):
        issues.add(
            "CHINESE_DESCRIPTION_REQUIRED",
            "/info/description",
            "API 总说明必须包含中文并解释用途。",
        )
    paths = _mapping(payload.get("paths"))
    component_schemas = _mapping(_mapping(payload.get("components")).get("schemas"))
    for schema_name, raw_schema in component_schemas.items():
        _validate_schema_descriptions(
            issues,
            _mapping(raw_schema),
            path=f"/components/schemas/{schema_name}",
        )
    actual_routes: set[tuple[str, str]] = set()
    operation_ids: list[str] = []
    stable_api_ids: list[str] = []
    operation_count = 0
    for route, raw_path_item in paths.items():
        path_item = _mapping(raw_path_item)
        for method, raw_operation in path_item.items():
            normalized_method = str(method).casefold()
            if normalized_method not in _HTTP_METHODS:
                continue
            operation_count += 1
            actual_routes.add((normalized_method.upper(), str(route)))
            operation = _mapping(raw_operation)
            base = f"/paths/{route}/{normalized_method}"
            operation_id = issues.require_text(
                operation.get("operationId"),
                code="OPERATION_ID_REQUIRED",
                path=f"{base}/operationId",
                message="每个 HTTP 操作必须有稳定 operationId。",
            )
            if operation_id:
                operation_ids.append(operation_id)
            if not _has_chinese(operation.get("summary")):
                issues.add(
                    "CHINESE_SUMMARY_REQUIRED",
                    f"{base}/summary",
                    "每个 HTTP 操作必须有中文摘要。",
                )
            description = operation.get("description")
            if not _has_chinese(description) or len(str(description or "").strip()) < 20:
                issues.add(
                    "CHINESE_DESCRIPTION_REQUIRED",
                    f"{base}/description",
                    "每个 HTTP 操作必须用中文详细说明用途和边界。",
                )
            stable_api_id = issues.require_text(
                operation.get("x-shanforge-id"),
                code="STABLE_API_ID_REQUIRED",
                path=f"{base}/x-shanforge-id",
                message="每个 HTTP 操作必须有稳定 Shanforge API ID。",
            )
            if stable_api_id:
                stable_api_ids.append(stable_api_id)
                if re.fullmatch(r"^API-[A-Z0-9-]+$", stable_api_id) is None:
                    issues.add(
                        "INVALID_STABLE_API_ID",
                        f"{base}/x-shanforge-id",
                        "Shanforge API ID 不符合稳定前缀规则。",
                    )
            raw_requirements = operation.get("x-shanforge-requirements")
            requirements = _nonempty_string_list(raw_requirements)
            if not requirements:
                issues.add(
                    "REQUIREMENT_TRACE_REQUIRED",
                    f"{base}/x-shanforge-requirements",
                    "每个 HTTP 操作必须追踪至少一个需求。",
                )
            if (
                not isinstance(raw_requirements, list)
                or len(requirements) != len(raw_requirements)
                or any(
                    re.fullmatch(r"^(?:REQ|NFR)-[A-Z0-9-]+$", item) is None for item in requirements
                )
            ):
                issues.add(
                    "INVALID_REQUIREMENT_TRACE",
                    f"{base}/x-shanforge-requirements",
                    "需求追踪必须是稳定 REQ/NFR ID 数组。",
                )
            if _duplicate_values(requirements):
                issues.add(
                    "DUPLICATE_REQUIREMENT_TRACE",
                    f"{base}/x-shanforge-requirements",
                    "需求追踪不能包含重复 ID。",
                )
            raw_tests = operation.get("x-shanforge-tests")
            tests = _nonempty_string_list(raw_tests)
            if not tests:
                issues.add(
                    "TEST_TRACE_REQUIRED",
                    f"{base}/x-shanforge-tests",
                    "每个 HTTP 操作必须追踪至少一个稳定测试 ID。",
                )
            if (
                not isinstance(raw_tests, list)
                or len(tests) != len(raw_tests)
                or any(re.fullmatch(r"^TEST-[A-Z0-9-]+$", item) is None for item in tests)
            ):
                issues.add(
                    "INVALID_TEST_TRACE",
                    f"{base}/x-shanforge-tests",
                    "测试追踪必须是稳定 TEST ID 数组。",
                )
            if _duplicate_values(tests):
                issues.add(
                    "DUPLICATE_TEST_TRACE",
                    f"{base}/x-shanforge-tests",
                    "测试追踪不能包含重复 ID。",
                )
            issues.require_text(
                operation.get("x-shanforge-owner"),
                code="API_OWNER_REQUIRED",
                path=f"{base}/x-shanforge-owner",
                message="每个 HTTP 操作必须声明 owner。",
            )
            for index, raw_parameter in enumerate(_list(operation.get("parameters"))):
                parameter = _mapping(raw_parameter)
                parameter_path = f"{base}/parameters/{index}"
                if not _has_chinese(parameter.get("description")):
                    issues.add(
                        "PARAMETER_DESCRIPTION_REQUIRED",
                        f"{parameter_path}/description",
                        "参数必须有中文说明。",
                    )
                schema = _mapping(parameter.get("schema"))
                if schema:
                    _validate_schema_descriptions(
                        issues,
                        schema,
                        path=f"{parameter_path}/schema",
                    )
                if "example" not in parameter and "examples" not in parameter:
                    issues.add(
                        "EXAMPLE_REQUIRED",
                        parameter_path,
                        "参数必须提供示例。",
                    )
            request_body = _mapping(operation.get("requestBody"))
            if request_body:
                if not _has_chinese(request_body.get("description")):
                    issues.add(
                        "REQUEST_DESCRIPTION_REQUIRED",
                        f"{base}/requestBody/description",
                        "请求体必须有中文说明。",
                    )
                _validate_media_content(
                    issues,
                    request_body.get("content"),
                    path=f"{base}/requestBody/content",
                )
            responses = _mapping(operation.get("responses"))
            invalid_response_codes = [
                str(code)
                for code in responses
                if re.fullmatch(r"(?:[1-5][0-9]{2}|default)", str(code)) is None
            ]
            if invalid_response_codes:
                issues.add(
                    "INVALID_RESPONSE_STATUS_CODE",
                    f"{base}/responses",
                    "响应键必须是 100-599 的三位状态码或 default。",
                )
            success_codes = [
                str(code)
                for code in responses
                if re.fullmatch(r"[23][0-9]{2}", str(code)) is not None
            ]
            error_codes = [
                str(code)
                for code in responses
                if re.fullmatch(r"[45][0-9]{2}", str(code)) is not None
            ]
            if not success_codes:
                issues.add("SUCCESS_RESPONSE_REQUIRED", f"{base}/responses", "必须声明成功响应。")
            if not error_codes:
                issues.add("ERROR_RESPONSE_REQUIRED", f"{base}/responses", "必须声明错误响应。")
            for status_code, raw_response in responses.items():
                response = _mapping(raw_response)
                response_path = f"{base}/responses/{status_code}"
                if not _has_chinese(response.get("description")):
                    issues.add(
                        "RESPONSE_DESCRIPTION_REQUIRED",
                        f"{response_path}/description",
                        "响应必须有中文说明。",
                    )
                _validate_media_content(
                    issues,
                    response.get("content"),
                    path=f"{response_path}/content",
                )
    for duplicate in sorted(_duplicate_values(operation_ids)):
        issues.add("DUPLICATE_OPERATION_ID", "/paths", f"operationId 重复：{duplicate}。")
    for duplicate in sorted(_duplicate_values(stable_api_ids)):
        issues.add(
            "DUPLICATE_STABLE_API_ID",
            "/paths",
            f"Shanforge API ID 重复：{duplicate}。",
        )
    if expected_routes is not None:
        missing = sorted(expected_routes - actual_routes)
        extra = sorted(actual_routes - expected_routes)
        if missing:
            issues.add(
                "ROUTE_MISSING_FROM_OPENAPI",
                "/paths",
                f"代码路由未进入 OpenAPI：{missing}。",
            )
        if extra:
            issues.add(
                "OPENAPI_ROUTE_NOT_IMPLEMENTED",
                "/paths",
                f"OpenAPI 声明了代码中不存在的路由：{extra}。",
            )
    return issues.report(artifact_kind="openapi", subject_count=operation_count)


def _validate_string_array(
    issues: _Issues,
    value: object,
    *,
    path: str,
    pattern: str | None = None,
) -> list[str]:
    values = _nonempty_string_list(value)
    if not isinstance(value, list) or len(values) != len(value):
        issues.add("INVALID_STRING_ARRAY", path, "该字段必须是非空字符串数组。")
    if pattern is not None and any(re.fullmatch(pattern, item) is None for item in values):
        issues.add("INVALID_STABLE_REFERENCE", path, "数组包含不符合规则的稳定 ID。")
    if _duplicate_values(values):
        issues.add("DUPLICATE_REFERENCE", path, "数组不能包含重复值。")
    return values


_TRACE_PATTERNS = {
    "requirements": r"^(?:REQ|NFR)-[A-Z0-9-]+$",
    "acceptance_criteria": r"^(?:REQ|NFR)-[A-Z0-9-]+-AC-\d+$",
    "designs": r"^DESIGN-[A-Z0-9-]+$",
    "ui_pages": r"^UI-PAGE-[A-Z0-9-]+$",
    "api_operations": r"^API-[A-Z0-9-]+$",
    "tasks": r"^[A-Z][A-Z0-9]*(?:-[A-Za-z0-9]+)+$",
}


def _is_json_value(
    value: object,
    *,
    allow_array: bool,
    active_ids: set[int] | None = None,
    depth: int = 0,
) -> bool:
    if depth > 64:
        return False
    if value is None or isinstance(value, (str, bool, int)):
        return True
    if isinstance(value, float):
        return math.isfinite(value)
    if not isinstance(value, (Mapping, list)):
        return False
    if isinstance(value, list) and not allow_array:
        return False
    identities = active_ids if active_ids is not None else set()
    identity = id(value)
    if identity in identities:
        return False
    identities.add(identity)
    try:
        if isinstance(value, Mapping):
            return all(
                isinstance(key, str)
                and _is_json_value(
                    item,
                    allow_array=True,
                    active_ids=identities,
                    depth=depth + 1,
                )
                for key, item in value.items()
            )
        return all(
            _is_json_value(
                item,
                allow_array=True,
                active_ids=identities,
                depth=depth + 1,
            )
            for item in value
        )
    finally:
        identities.remove(identity)


def validate_test_case_catalog(payload: Mapping[str, Any]) -> ArtifactValidationReport:
    issues = _Issues()
    _reject_unknown_fields(
        issues,
        payload,
        frozenset({"schema_id", "id", "title", "version", "status", "cases"}),
        path="",
    )
    if payload.get("schema_id") != "TestCaseCatalog/v1":
        issues.add(
            "UNSUPPORTED_SCHEMA",
            "/schema_id",
            "测试案例目录必须使用 TestCaseCatalog/v1。",
        )
    for field in ("id", "title", "version", "status"):
        value = issues.require_text(
            payload.get(field),
            code=f"CATALOG_{field.upper()}_REQUIRED",
            path=f"/{field}",
            message=f"测试案例目录必须声明 {field}。",
        )
        if field == "title" and value and not _has_chinese(value):
            issues.add(
                "CHINESE_TEST_DESCRIPTION_REQUIRED",
                "/title",
                "测试案例目录标题必须包含中文。",
            )
        if field == "id" and value and re.fullmatch(r"^TEST-CATALOG-[A-Z0-9-]+$", value) is None:
            issues.add(
                "INVALID_TEST_CATALOG_ID",
                "/id",
                "测试案例目录 ID 不符合稳定前缀规则。",
            )
    if str(payload.get("status") or "") not in _DEFINITION_STATUSES:
        issues.add("INVALID_CATALOG_STATUS", "/status", "测试案例目录状态不受支持。")
    cases = _require_list(issues, payload, "cases", path="/cases")
    case_ids: list[str] = []
    required_fields = (
        "version",
        "title",
        "objective",
        "type",
        "level",
        "priority",
        "risk",
        "owner",
        "environment",
    )
    for index, raw_case in enumerate(cases):
        case = _mapping(raw_case)
        base = f"/cases/{index}"
        _reject_unknown_fields(
            issues,
            case,
            frozenset(
                {
                    "id",
                    "version",
                    "title",
                    "definition_status",
                    "objective",
                    "type",
                    "level",
                    "priority",
                    "risk",
                    "owner",
                    "traceability",
                    "preconditions",
                    "test_data",
                    "steps",
                    "postconditions",
                    "environment",
                    "automation",
                    "tags",
                }
            ),
            path=base,
        )
        case_id = issues.require_text(
            case.get("id"),
            code="TEST_CASE_ID_REQUIRED",
            path=f"{base}/id",
            message="测试案例必须有稳定 ID。",
        )
        if case_id:
            case_ids.append(case_id)
            if re.fullmatch(r"^TEST-[A-Z0-9-]+$", case_id) is None:
                issues.add("INVALID_TEST_CASE_ID", f"{base}/id", "测试案例 ID 不符合规则。")
        for field in required_fields:
            value = issues.require_text(
                case.get(field),
                code=f"TEST_CASE_{field.upper()}_REQUIRED",
                path=f"{base}/{field}",
                message=f"测试案例必须声明 {field}。",
            )
            if field in {"title", "objective"} and value and not _has_chinese(value):
                issues.add(
                    "CHINESE_TEST_DESCRIPTION_REQUIRED",
                    f"{base}/{field}",
                    "测试标题和目标必须包含中文。",
                )
        if str(case.get("definition_status") or "") not in _DEFINITION_STATUSES:
            issues.add(
                "INVALID_DEFINITION_STATUS",
                f"{base}/definition_status",
                "测试定义状态必须是 draft、active、deprecated 或 retired。",
            )
        if str(case.get("type") or "") not in _TEST_TYPES:
            issues.add("INVALID_TEST_TYPE", f"{base}/type", "测试类型不受支持。")
        if str(case.get("level") or "") not in _TEST_LEVELS:
            issues.add("INVALID_TEST_LEVEL", f"{base}/level", "测试层级不受支持。")
        if str(case.get("priority") or "") not in _TEST_PRIORITIES:
            issues.add("INVALID_TEST_PRIORITY", f"{base}/priority", "测试优先级不受支持。")
        if str(case.get("risk") or "") not in _TEST_RISKS:
            issues.add("INVALID_TEST_RISK", f"{base}/risk", "测试风险等级不受支持。")
        traceability = _require_mapping(
            issues,
            case,
            "traceability",
            path=f"{base}/traceability",
        )
        _reject_unknown_fields(
            issues,
            traceability,
            frozenset(_TRACE_PATTERNS),
            path=f"{base}/traceability",
        )
        traces = {
            field: _validate_string_array(
                issues,
                traceability.get(field),
                path=f"{base}/traceability/{field}",
                pattern=pattern,
            )
            for field, pattern in _TRACE_PATTERNS.items()
        }
        if not traces["requirements"]:
            issues.add(
                "REQUIREMENT_TRACE_REQUIRED",
                f"{base}/traceability/requirements",
                "测试案例必须追踪至少一个需求。",
            )
        if not any(
            traces[key]
            for key in ("acceptance_criteria", "designs", "ui_pages", "api_operations", "tasks")
        ):
            issues.add(
                "DELIVERY_TRACE_REQUIRED",
                f"{base}/traceability",
                "测试案例还必须追踪验收、设计、UI、API 或任务中的至少一种。",
            )
        for field in ("preconditions", "postconditions", "tags"):
            _validate_string_array(
                issues,
                case.get(field),
                path=f"{base}/{field}",
            )
        test_data = _require_list(
            issues,
            case,
            "test_data",
            path=f"{base}/test_data",
        )
        for data_index, raw_data in enumerate(test_data):
            data = _mapping(raw_data)
            data_base = f"{base}/test_data/{data_index}"
            _reject_unknown_fields(
                issues,
                data,
                frozenset({"name", "value", "sensitive"}),
                path=data_base,
            )
            issues.require_text(
                data.get("name"),
                code="TEST_DATA_NAME_REQUIRED",
                path=f"{data_base}/name",
                message="测试数据必须声明名称。",
            )
            if "value" not in data:
                issues.add("TEST_DATA_VALUE_REQUIRED", f"{data_base}/value", "测试数据缺少值。")
            elif not _is_json_value(data.get("value"), allow_array=False):
                issues.add(
                    "INVALID_TEST_DATA_VALUE",
                    f"{data_base}/value",
                    "测试数据值只能是可无损序列化的 JSON 标量或字符串键对象。",
                )
            if not isinstance(data.get("sensitive"), bool):
                issues.add(
                    "TEST_DATA_SENSITIVE_REQUIRED",
                    f"{data_base}/sensitive",
                    "测试数据必须明确 sensitive 布尔值。",
                )
        steps = _require_list(issues, case, "steps", path=f"{base}/steps")
        if not steps:
            issues.add("TEST_STEPS_REQUIRED", f"{base}/steps", "测试案例必须有执行步骤。")
        for step_index, raw_step in enumerate(steps):
            step = _mapping(raw_step)
            step_base = f"{base}/steps/{step_index}"
            _reject_unknown_fields(
                issues,
                step,
                frozenset({"action", "expected"}),
                path=step_base,
            )
            issues.require_text(
                step.get("action"),
                code="TEST_ACTION_REQUIRED",
                path=f"{step_base}/action",
                message="每个测试步骤必须说明操作。",
            )
            issues.require_text(
                step.get("expected"),
                code="EXPECTED_RESULT_REQUIRED",
                path=f"{step_base}/expected",
                message="每个测试步骤必须说明预期结果。",
            )
        automation = _require_mapping(
            issues,
            case,
            "automation",
            path=f"{base}/automation",
        )
        _reject_unknown_fields(
            issues,
            automation,
            frozenset({"status", "entrypoint"}),
            path=f"{base}/automation",
        )
        automation_status = str(automation.get("status") or "")
        if automation_status not in _AUTOMATION_STATUSES:
            issues.add(
                "INVALID_AUTOMATION_STATUS",
                f"{base}/automation/status",
                "自动化状态不受支持。",
            )
        entrypoint = automation.get("entrypoint")
        if automation_status in {"automated", "partial"}:
            issues.require_text(
                entrypoint,
                code="AUTOMATION_ENTRYPOINT_REQUIRED",
                path=f"{base}/automation/entrypoint",
                message="已自动化或部分自动化的案例必须声明入口。",
            )
        elif entrypoint is not None and not isinstance(entrypoint, str):
            issues.add(
                "INVALID_AUTOMATION_ENTRYPOINT",
                f"{base}/automation/entrypoint",
                "手工或计划自动化入口必须是字符串或 null。",
            )
        if "result" in case or "run_status" in case:
            issues.add(
                "RUN_RESULT_NOT_ALLOWED_IN_DEFINITION",
                base,
                "稳定测试定义不能保存单次运行结果。",
            )
    for duplicate in sorted(_duplicate_values(case_ids)):
        issues.add("DUPLICATE_TEST_CASE_ID", "/cases", f"测试案例 ID 重复：{duplicate}。")
    return issues.report(artifact_kind="test_cases", subject_count=len(cases))


def _parse_timestamp(
    issues: _Issues,
    value: object,
    *,
    path: str,
) -> datetime | None:
    if not isinstance(value, str):
        issues.add("TIMESTAMP_REQUIRED", path, "时间必须是带时区的 ISO 8601 字符串。")
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        issues.add("INVALID_TIMESTAMP", path, "时间不是合法 ISO 8601。")
        return None
    if parsed.tzinfo is None:
        issues.add("TIMEZONE_REQUIRED", path, "时间必须包含时区。")
        return None
    return parsed


def validate_test_run_result(
    payload: Mapping[str, Any],
    *,
    evidence_root: str,
) -> ArtifactValidationReport:
    issues = _Issues()
    _reject_unknown_fields(
        issues,
        payload,
        frozenset(
            {
                "schema_id",
                "id",
                "run_id",
                "test_case_id",
                "test_case_version",
                "status",
                "started_at",
                "finished_at",
                "environment",
                "step_results",
                "evidence",
            }
        ),
        path="",
    )
    if payload.get("schema_id") != "TestRunResult/v1":
        issues.add("UNSUPPORTED_SCHEMA", "/schema_id", "测试结果必须使用 TestRunResult/v1。")
    for field in ("id", "run_id", "test_case_id", "test_case_version"):
        issues.require_text(
            payload.get(field),
            code=f"TEST_RESULT_{field.upper()}_REQUIRED",
            path=f"/{field}",
            message=f"测试结果必须声明 {field}。",
        )
    for field, pattern in (
        ("id", r"^RUN-RESULT-[A-Z0-9-]+$"),
        ("run_id", r"^RUN-[A-Z0-9-]+$"),
        ("test_case_id", r"^TEST-[A-Z0-9-]+$"),
    ):
        value = str(payload.get(field) or "")
        if value and re.fullmatch(pattern, value) is None:
            issues.add(
                "INVALID_TEST_RESULT_ID",
                f"/{field}",
                f"{field} 不符合稳定 ID 规则。",
            )
    status = str(payload.get("status") or "")
    if status not in _TEST_RESULT_STATUSES:
        issues.add(
            "INVALID_TEST_RESULT_STATUS",
            "/status",
            "测试结果状态必须使用七态枚举。",
        )
    started_at = _parse_timestamp(issues, payload.get("started_at"), path="/started_at")
    finished_at = _parse_timestamp(issues, payload.get("finished_at"), path="/finished_at")
    if started_at is not None and finished_at is not None and finished_at < started_at:
        issues.add("INVALID_TIME_RANGE", "/finished_at", "结束时间不能早于开始时间。")
    environment = _require_mapping(
        issues,
        payload,
        "environment",
        path="/environment",
    )
    _reject_unknown_fields(
        issues,
        environment,
        frozenset({"id", "git_commit", "runtime"}),
        path="/environment",
    )
    for field in ("id", "git_commit", "runtime"):
        issues.require_text(
            environment.get(field),
            code=f"TEST_ENVIRONMENT_{field.upper()}_REQUIRED",
            path=f"/environment/{field}",
            message=f"测试环境必须声明 {field}。",
        )
    git_commit = str(environment.get("git_commit") or "")
    if git_commit and re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", git_commit) is None:
        issues.add(
            "INVALID_GIT_COMMIT",
            "/environment/git_commit",
            "git_commit 必须是 40 或 64 位小写十六进制。",
        )
    step_results = _require_list(
        issues,
        payload,
        "step_results",
        path="/step_results",
    )
    observed_steps: list[int] = []
    observed_statuses: list[str] = []
    step_evidence_counts: list[int] = []
    referenced_evidence: set[str] = set()
    for index, raw_step in enumerate(step_results):
        step = _mapping(raw_step)
        base = f"/step_results/{index}"
        _reject_unknown_fields(
            issues,
            step,
            frozenset({"step", "status", "actual", "evidence_refs"}),
            path=base,
        )
        step_number = step.get("step")
        if type(step_number) is not int or int(step_number) < 1:
            issues.add("INVALID_STEP_NUMBER", f"{base}/step", "步骤编号必须是正整数。")
        else:
            observed_steps.append(int(step_number))
        step_status = str(step.get("status") or "")
        if step_status not in _TEST_RESULT_STATUSES:
            issues.add("INVALID_TEST_RESULT_STATUS", f"{base}/status", "步骤状态不受支持。")
        else:
            observed_statuses.append(step_status)
        issues.require_text(
            step.get("actual"),
            code="STEP_ACTUAL_REQUIRED",
            path=f"{base}/actual",
            message="步骤结果必须说明实际结果。",
        )
        step_evidence = _validate_string_array(
            issues,
            step.get("evidence_refs"),
            path=f"{base}/evidence_refs",
        )
        step_evidence_counts.append(len(step_evidence))
        referenced_evidence.update(step_evidence)
    if observed_steps != list(range(1, len(step_results) + 1)):
        issues.add(
            "NON_CONTIGUOUS_STEP_RESULTS",
            "/step_results",
            "步骤结果必须从 1 开始连续递增。",
        )
    evidence = _require_list(issues, payload, "evidence", path="/evidence")
    evidence_ids: list[str] = []
    evidence_root_path = PurePosixPath(evidence_root)
    if (
        evidence_root_path.is_absolute()
        or ".." in evidence_root_path.parts
        or "." in evidence_root_path.parts
    ):
        issues.add("INVALID_EVIDENCE_ROOT", "/evidence", "evidence_root 必须是仓库相对路径。")
    for index, raw_evidence in enumerate(evidence):
        item = _mapping(raw_evidence)
        base = f"/evidence/{index}"
        _reject_unknown_fields(
            issues,
            item,
            frozenset({"id", "kind", "path", "sha256"}),
            path=base,
        )
        evidence_id = issues.require_text(
            item.get("id"),
            code="EVIDENCE_ID_REQUIRED",
            path=f"{base}/id",
            message="证据必须有稳定 ID。",
        )
        if evidence_id:
            evidence_ids.append(evidence_id)
        issues.require_text(
            item.get("kind"),
            code="EVIDENCE_KIND_REQUIRED",
            path=f"{base}/kind",
            message="证据必须声明类型。",
        )
        evidence_path = item.get("path")
        if (
            not _is_repository_path(evidence_path, prefix=evidence_root)
            or str(evidence_path) == evidence_root
        ):
            issues.add(
                "EVIDENCE_PATH_OUTSIDE_ROOT",
                f"{base}/path",
                "证据路径必须位于当前 work item evidence 目录。",
            )
        if re.fullmatch(r"[0-9a-f]{64}", str(item.get("sha256") or "")) is None:
            issues.add(
                "INVALID_EVIDENCE_SHA256",
                f"{base}/sha256",
                "证据 sha256 必须是 64 位小写十六进制。",
            )
    for duplicate in sorted(_duplicate_values(evidence_ids)):
        issues.add("DUPLICATE_EVIDENCE_ID", "/evidence", f"证据 ID 重复：{duplicate}。")
    missing_evidence = sorted(referenced_evidence - set(evidence_ids))
    if missing_evidence:
        issues.add(
            "EVIDENCE_REFERENCE_NOT_FOUND",
            "/step_results",
            f"步骤引用了未登记证据：{missing_evidence}。",
        )
    aggregate_status: str | None = None
    for candidate in ("error", "failed", "blocked", "cancelled"):
        if candidate in observed_statuses:
            aggregate_status = candidate
            break
    if aggregate_status is None and observed_statuses:
        if all(value == "passed" for value in observed_statuses):
            aggregate_status = "passed"
        elif all(value == "skipped" for value in observed_statuses):
            aggregate_status = "skipped"
        elif all(value == "not_run" for value in observed_statuses):
            aggregate_status = "not_run"
    if aggregate_status != status:
        issues.add(
            "TEST_RESULT_STATUS_MISMATCH",
            "/status",
            "整体状态必须由逐步结果按 error、failed、blocked、cancelled 优先级确定。",
        )
    if status == "passed" and (
        not step_results
        or not evidence_ids
        or not referenced_evidence
        or any(count == 0 for count in step_evidence_counts)
    ):
        issues.add(
            "PASSED_RESULT_EVIDENCE_REQUIRED",
            "/evidence",
            "通过结果必须有逐步结果，并由步骤引用至少一条证据。",
        )
    return issues.report(artifact_kind="test_run_result", subject_count=1)


def validate_test_report(
    payload: Mapping[str, Any],
    *,
    validated_results_by_id: Mapping[str, ValidatedTestResult],
) -> ArtifactValidationReport:
    issues = _Issues()
    _reject_unknown_fields(
        issues,
        payload,
        frozenset(
            {
                "schema_id",
                "id",
                "run_id",
                "title",
                "generated_at",
                "result_refs",
                "summary",
            }
        ),
        path="",
    )
    if payload.get("schema_id") != "TestReport/v1":
        issues.add("UNSUPPORTED_SCHEMA", "/schema_id", "测试报告必须使用 TestReport/v1。")
    for field in ("id", "run_id", "title"):
        issues.require_text(
            payload.get(field),
            code=f"TEST_REPORT_{field.upper()}_REQUIRED",
            path=f"/{field}",
            message=f"测试报告必须声明 {field}。",
        )
    for field, pattern in (
        ("id", r"^TEST-REPORT-[A-Z0-9-]+$"),
        ("run_id", r"^RUN-[A-Z0-9-]+$"),
    ):
        value = str(payload.get(field) or "")
        if value and re.fullmatch(pattern, value) is None:
            issues.add(
                "INVALID_TEST_REPORT_ID",
                f"/{field}",
                f"{field} 不符合稳定 ID 规则。",
            )
    _parse_timestamp(issues, payload.get("generated_at"), path="/generated_at")
    report_run_id = str(payload.get("run_id") or "")
    refs = _require_list(issues, payload, "result_refs", path="/result_refs")
    result_ids: list[str] = []
    statuses: list[str] = []
    for index, raw_ref in enumerate(refs):
        ref = _mapping(raw_ref)
        base = f"/result_refs/{index}"
        _reject_unknown_fields(
            issues,
            ref,
            frozenset({"result_id", "test_case_id", "status", "evidence_path", "sha256"}),
            path=base,
        )
        for field in ("result_id", "test_case_id", "status", "evidence_path", "sha256"):
            issues.require_text(
                ref.get(field),
                code=f"RESULT_REF_{field.upper()}_REQUIRED",
                path=f"{base}/{field}",
                message=f"结果引用必须声明 {field}。",
            )
        result_id = str(ref.get("result_id") or "")
        status = str(ref.get("status") or "")
        if result_id:
            result_ids.append(result_id)
        if status in _TEST_RESULT_STATUSES:
            statuses.append(status)
        else:
            issues.add("INVALID_TEST_RESULT_STATUS", f"{base}/status", "结果状态不受支持。")
        if re.fullmatch(r"^RUN-RESULT-[A-Z0-9-]+$", result_id) is None:
            issues.add(
                "INVALID_RESULT_REFERENCE_ID",
                f"{base}/result_id",
                "result_id 不符合稳定 ID 规则。",
            )
        if (
            re.fullmatch(
                r"^TEST-[A-Z0-9-]+$",
                str(ref.get("test_case_id") or ""),
            )
            is None
        ):
            issues.add(
                "INVALID_TEST_CASE_REFERENCE_ID",
                f"{base}/test_case_id",
                "test_case_id 不符合稳定 ID 规则。",
            )
        if re.fullmatch(r"[0-9a-f]{64}", str(ref.get("sha256") or "")) is None:
            issues.add(
                "INVALID_EVIDENCE_SHA256",
                f"{base}/sha256",
                "证据 sha256 必须是 64 位小写十六进制。",
            )
        validated = validated_results_by_id.get(result_id)
        evidence_pair = (
            str(ref.get("evidence_path") or ""),
            str(ref.get("sha256") or ""),
        )
        if (
            validated is None
            or validated.result_id != result_id
            or validated.run_id != report_run_id
            or validated.test_case_id != str(ref.get("test_case_id") or "")
            or validated.status != status
            or evidence_pair not in validated.evidence
        ):
            issues.add(
                "REPORT_RESULT_MISMATCH",
                base,
                "结果引用必须与已验证结果的案例、状态和证据精确一致。",
            )
    for duplicate in sorted(_duplicate_values(result_ids)):
        issues.add(
            "DUPLICATE_RESULT_REFERENCE",
            "/result_refs",
            f"结果引用重复：{duplicate}。",
        )
    summary = _require_mapping(issues, payload, "summary", path="/summary")
    _reject_unknown_fields(
        issues,
        summary,
        frozenset({"total", *_TEST_RESULT_STATUSES}),
        path="/summary",
    )
    actual = Counter(statuses)
    mismatch = summary.get("total") != len(refs)
    for status in _TEST_RESULT_STATUSES:
        summary_count = summary.get(status)
        if (
            type(summary_count) is not int
            or int(summary_count) < 0
            or summary_count != actual.get(status, 0)
        ):
            mismatch = True
    if mismatch:
        issues.add(
            "REPORT_COUNT_MISMATCH",
            "/summary",
            "报告汇总必须与唯一结果引用的七态计数逐项一致。",
        )
    return issues.report(artifact_kind="test_report", subject_count=len(refs))
