from __future__ import annotations

import io
import json
import re
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from access.http.routes import build_runtime_routes
from access.project_cli import run
from application.project_artifacts.service import ProjectArtifactValidationService
from domain.project_artifacts.models import ValidatedTestResult
from domain.project_artifacts.validation import (
    validate_design_manifest,
    validate_design_tokens,
    validate_openapi,
    validate_test_case_catalog,
    validate_test_report,
    validate_test_run_result,
)
from settings.project_artifacts.local_repository import LocalProjectArtifactRepository


def _valid_design_manifest() -> dict[str, Any]:
    return {
        "schema_id": "DesignArtifactManifest/v1",
        "id": "DESIGN-ASSET-UX-UI-001",
        "title": "项目知识只读站点 UX/UI 设计资产",
        "status": "awaiting_penpot_connection",
        "document_id": "DESIGN-UX-UI-001",
        "source": {
            "format": "penpot",
            "file": None,
            "connection_required": True,
        },
        "pages": [
            {
                "id": "UI-PAGE-PROJECT-DASHBOARD",
                "title": "项目任务看板",
                "purpose": "让项目负责人快速查看当前任务状态并进入详情。",
            }
        ],
        "components": [
            {
                "id": "UI-COMPONENT-TASK-CARD",
                "title": "任务卡片",
                "purpose": "展示中文任务标题并进入任务详情。",
                "states": ["default", "focus", "blocked"],
            }
        ],
        "tokens_file": "design/ux-ui/tokens.json",
        "exports": [],
    }


def _valid_design_tokens() -> dict[str, Any]:
    return {
        "schema_id": "DesignTokens/v1",
        "id": "DESIGN-TOKENS-PROJECT-SITE-001",
        "title": "项目站点设计 Token",
        "version": "1.0.0",
        "color": {"content.primary": "#172033"},
        "typography": {"family.sans": "sans-serif"},
        "space": {"1": "4px"},
        "radius": {"small": "8px"},
        "motion": {"duration.fast": "120ms"},
    }


def _valid_openapi() -> dict[str, Any]:
    return {
        "openapi": "3.1.0",
        "info": {
            "title": "Shanforge HTTP API",
            "version": "0.2.0",
            "description": "为 Agent App 执行和项目状态查询提供稳定的 HTTP 边界。",
        },
        "paths": {
            "/projects/{project_id}/status": {
                "get": {
                    "operationId": "getProjectStatus",
                    "summary": "查询项目状态",
                    "description": ("读取指定项目的当前任务、进度和阻塞摘要，供只读项目视图使用。"),
                    "parameters": [
                        {
                            "name": "project_id",
                            "in": "path",
                            "required": True,
                            "description": "要查询的稳定项目标识。",
                            "schema": {"type": "string", "description": "稳定项目标识。"},
                            "example": "shanforge",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "成功返回项目当前状态。",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "description": "项目当前状态响应。",
                                        "properties": {
                                            "project_id": {
                                                "type": "string",
                                                "description": "项目稳定标识。",
                                            }
                                        },
                                    },
                                    "example": {"project_id": "shanforge"},
                                }
                            },
                        },
                        "404": {
                            "description": "项目不存在或当前调用方不可访问。",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "description": "稳定错误响应。",
                                        "properties": {
                                            "code": {
                                                "type": "string",
                                                "description": "稳定错误代码。",
                                            }
                                        },
                                    },
                                    "example": {"code": "PROJECT_NOT_FOUND"},
                                }
                            },
                        },
                    },
                    "x-shanforge-id": "API-HTTP-PROJECT-STATUS",
                    "x-shanforge-requirements": ["REQ-PKI-008"],
                    "x-shanforge-tests": ["TEST-API-PROJECT-STATUS-001"],
                    "x-shanforge-owner": "access",
                }
            }
        },
    }


def _valid_test_catalog() -> dict[str, Any]:
    return {
        "schema_id": "TestCaseCatalog/v1",
        "id": "TEST-CATALOG-PROJECT-ARTIFACTS",
        "title": "项目资产合同测试案例",
        "version": "1.0.0",
        "status": "active",
        "cases": [
            {
                "id": "TEST-API-PROJECT-STATUS-001",
                "version": "1.0.0",
                "title": "项目状态接口合同校验",
                "definition_status": "active",
                "objective": "确认项目状态接口具备完整中文说明和稳定追踪。",
                "type": "contract",
                "level": "integration",
                "priority": "P1",
                "risk": "medium",
                "owner": "HUMAN_QUALITY_SECURITY_LEAD",
                "traceability": {
                    "requirements": ["REQ-PKI-008"],
                    "acceptance_criteria": ["REQ-PKI-008-AC-1"],
                    "designs": ["DESIGN-API-001"],
                    "ui_pages": [],
                    "api_operations": ["API-HTTP-PROJECT-STATUS"],
                    "tasks": ["PROJECT-ARTIFACTS-001-T02"],
                },
                "preconditions": ["OpenAPI 文件可读取。"],
                "test_data": [
                    {
                        "name": "project_id",
                        "value": "shanforge",
                        "sensitive": False,
                    }
                ],
                "steps": [
                    {
                        "action": "运行 API 合同校验命令。",
                        "expected": "命令成功并报告全部操作通过。",
                    }
                ],
                "postconditions": ["未修改正式 API 文件。"],
                "environment": "TEST-ENV-PYTEST",
                "automation": {
                    "status": "automated",
                    "entrypoint": (
                        "tests/test_project_artifact_contracts.py"
                        "::test_repository_and_service_validate_all_artifacts"
                    ),
                },
                "tags": ["api", "contract"],
            }
        ],
    }


def test_design_manifest_allows_explicit_unconnected_state_without_fake_penpot() -> None:
    report = validate_design_manifest(
        _valid_design_manifest(),
        available_paths={"design/ux-ui/tokens.json"},
    )

    assert report.valid is True
    assert report.subject_count == 2
    assert report.issues == ()


def test_design_manifest_rejects_ready_state_without_real_penpot_and_path_escape() -> None:
    payload = _valid_design_manifest()
    payload["status"] = "ready"
    payload["source"]["file"] = "../fake.penpot"

    report = validate_design_manifest(payload, available_paths={"design/ux-ui/tokens.json"})

    assert report.valid is False
    assert {issue.code for issue in report.issues} >= {
        "UNSAFE_REPOSITORY_PATH",
        "PENPOT_SOURCE_NOT_FOUND",
    }


def test_design_schema_required_fields_and_enums_match_domain_contract() -> None:
    root = Path(__file__).resolve().parents[1]
    schema = json.loads(
        (root / "contracts/schemas/design-artifact-manifest.schema.json").read_text(
            encoding="utf-8"
        )
    )

    assert set(schema["required"]) == {
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
    assert set(schema["properties"]["status"]["enum"]) == {
        "awaiting_penpot_connection",
        "draft",
        "ready",
        "deprecated",
    }
    assert set(schema["$defs"]["component"]["properties"]["states"]["items"]["enum"]) == {
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
    assert len(schema["allOf"]) == 2


@pytest.mark.parametrize(
    "mutate",
    [
        lambda payload: payload.pop("pages"),
        lambda payload: payload.pop("components"),
        lambda payload: payload.pop("exports"),
        lambda payload: payload.__setitem__("id", "wrong"),
        lambda payload: payload.__setitem__("document_id", "wrong"),
        lambda payload: payload["source"].pop("file"),
        lambda payload: payload["source"].pop("connection_required"),
    ],
)
def test_design_manifest_rejects_values_forbidden_by_the_schema(mutate: Any) -> None:
    payload = _valid_design_manifest()
    payload["status"] = "draft"
    mutate(payload)

    report = validate_design_manifest(
        payload,
        available_paths={"design/ux-ui/tokens.json"},
    )

    assert report.valid is False


@pytest.mark.parametrize("states", [["default", "default"], ["default", 123]])
def test_design_manifest_rejects_schema_invalid_component_states(
    states: list[object],
) -> None:
    payload = _valid_design_manifest()
    payload["components"][0]["states"] = states

    report = validate_design_manifest(
        payload,
        available_paths={"design/ux-ui/tokens.json"},
    )

    assert report.valid is False


def test_design_schema_paths_reject_dot_segments() -> None:
    root = Path(__file__).resolve().parents[1]
    schema = json.loads(
        (root / "contracts/schemas/design-artifact-manifest.schema.json").read_text(
            encoding="utf-8"
        )
    )
    patterns = [
        schema["properties"]["source"]["properties"]["file"]["pattern"],
        schema["properties"]["tokens_file"]["pattern"],
        schema["$defs"]["export"]["properties"]["file"]["pattern"],
    ]

    assert all(
        re.fullmatch(pattern, "design/ux-ui/../outside.penpot") is None for pattern in patterns
    )


def test_repository_rejects_internal_symlink_and_invalid_tokens(tmp_path: Path) -> None:
    design_root = tmp_path / "design/ux-ui"
    design_root.mkdir(parents=True)
    (design_root / "real-tokens.json").write_text("{}\n", encoding="utf-8")
    (design_root / "tokens.json").symlink_to(design_root / "real-tokens.json")
    repository = LocalProjectArtifactRepository(tmp_path)

    with pytest.raises(ValueError, match="symlink"):
        repository.design_tokens("design/ux-ui/tokens.json")

    (design_root / "tokens.json").unlink()
    (design_root / "tokens.json").write_text("{not-json}\n", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        repository.design_tokens("design/ux-ui/tokens.json")


def test_repository_rejects_oversized_tokens(tmp_path: Path) -> None:
    design_root = tmp_path / "design/ux-ui"
    design_root.mkdir(parents=True)
    (design_root / "tokens.json").write_bytes(b"x" * (4 * 1024 * 1024 + 1))

    with pytest.raises(ValueError, match="size limit"):
        LocalProjectArtifactRepository(tmp_path).design_tokens("design/ux-ui/tokens.json")


def test_design_tokens_are_validated_as_an_independent_contract() -> None:
    report = validate_design_tokens(
        {
            "schema_id": "DesignTokens/v1",
            "id": "bad-id",
            "title": "Project tokens",
            "version": "1.0.0",
            "color": {},
            "typography": {},
            "space": {},
            "radius": {},
            "motion": {},
        }
    )

    assert report.valid is False
    assert {issue.code for issue in report.issues} >= {
        "INVALID_TOKEN_ID",
        "CHINESE_TITLE_REQUIRED",
        "TOKEN_GROUP_EMPTY",
    }


def test_openapi_requires_detailed_chinese_contract_and_traceability() -> None:
    report = validate_openapi(
        _valid_openapi(),
        expected_routes={("GET", "/projects/{project_id}/status")},
    )
    assert report.valid is True
    assert report.subject_count == 1

    invalid = _valid_openapi()
    operation = invalid["paths"]["/projects/{project_id}/status"]["get"]
    operation["summary"] = "Get status"
    operation.pop("x-shanforge-tests")
    operation["responses"].pop("404")
    report = validate_openapi(
        invalid,
        expected_routes={("GET", "/projects/{project_id}/status")},
    )

    assert report.valid is False
    assert {issue.code for issue in report.issues} >= {
        "CHINESE_SUMMARY_REQUIRED",
        "TEST_TRACE_REQUIRED",
        "ERROR_RESPONSE_REQUIRED",
    }


@pytest.mark.parametrize(
    ("field", "value", "expected_code"),
    [
        ("x-shanforge-id", "wrong", "INVALID_STABLE_API_ID"),
        (
            "x-shanforge-requirements",
            ["REQ-PKI-008", "REQ-PKI-008"],
            "DUPLICATE_REQUIREMENT_TRACE",
        ),
        (
            "x-shanforge-requirements",
            ["REQ-PKI-008", 123],
            "INVALID_REQUIREMENT_TRACE",
        ),
        (
            "x-shanforge-tests",
            ["TEST-API-PROJECT-STATUS-001", "bad"],
            "INVALID_TEST_TRACE",
        ),
    ],
)
def test_openapi_rejects_schema_invalid_stable_trace_fields(
    field: str,
    value: object,
    expected_code: str,
) -> None:
    payload = _valid_openapi()
    payload["paths"]["/projects/{project_id}/status"]["get"][field] = value

    report = validate_openapi(
        payload,
        expected_routes={("GET", "/projects/{project_id}/status")},
    )

    assert report.valid is False
    assert expected_code in {issue.code for issue in report.issues}


def test_openapi_rejects_missing_and_extra_runtime_routes() -> None:
    payload = _valid_openapi()

    report = validate_openapi(
        payload,
        expected_routes={
            ("GET", "/projects/{project_id}/status"),
            ("POST", "/manifests/run"),
        },
    )
    assert "ROUTE_MISSING_FROM_OPENAPI" in {issue.code for issue in report.issues}

    report = validate_openapi(payload, expected_routes=set())
    assert "OPENAPI_ROUTE_NOT_IMPLEMENTED" in {issue.code for issue in report.issues}


def test_repository_openapi_matches_all_declared_runtime_routes() -> None:
    root = Path(__file__).resolve().parents[1]
    repository = LocalProjectArtifactRepository(root)

    report = validate_openapi(
        repository.openapi_contract(),
        expected_routes={(route.method, route.path) for route in build_runtime_routes()},
    )

    assert report.valid is True
    assert report.subject_count == 4
    assert report.issues == ()


def test_openapi_extension_schema_required_fields_match_domain_contract() -> None:
    root = Path(__file__).resolve().parents[1]
    schema = json.loads(
        (root / "contracts/schemas/openapi-shanforge-rules.schema.json").read_text(encoding="utf-8")
    )

    assert set(schema["required"]) == {
        "operationId",
        "summary",
        "description",
        "responses",
        "x-shanforge-id",
        "x-shanforge-requirements",
        "x-shanforge-tests",
        "x-shanforge-owner",
    }
    assert "\\u3400-\\u9fff" in schema["properties"]["summary"]["pattern"]
    assert schema["properties"]["description"]["minLength"] == 20
    assert schema["properties"]["description"]["allOf"][1]["pattern"].startswith("^\\s*")
    assert schema["properties"]["x-shanforge-requirements"]["items"]["pattern"].startswith(
        "^(REQ|NFR)-"
    )
    assert len(schema["properties"]["responses"]["allOf"]) == 2


def test_openapi_extension_schema_and_domain_accept_the_same_boundary_samples() -> None:
    root = Path(__file__).resolve().parents[1]
    schema = json.loads(
        (root / "contracts/schemas/openapi-shanforge-rules.schema.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema)
    payload = _valid_openapi()
    operation = payload["paths"]["/projects/{project_id}/status"]["get"]
    success = operation["responses"].pop("200")
    error = operation["responses"].pop("404")
    operation["responses"]["206"] = success
    operation["responses"]["418"] = error

    assert list(validator.iter_errors(operation)) == []
    assert validate_openapi(
        payload,
        expected_routes={("GET", "/projects/{project_id}/status")},
    ).valid

    operation["description"] = "中" + (" " * 19)

    assert list(validator.iter_errors(operation))
    assert not validate_openapi(
        payload,
        expected_routes={("GET", "/projects/{project_id}/status")},
    ).valid


@pytest.mark.parametrize(
    "responses",
    [
        {"206": {"description": "成功返回项目当前状态。"}},
        {"418": {"description": "调用请求不符合接口约束。"}},
    ],
)
def test_openapi_extension_schema_and_domain_both_require_success_and_error(
    responses: dict[str, Any],
) -> None:
    root = Path(__file__).resolve().parents[1]
    schema = json.loads(
        (root / "contracts/schemas/openapi-shanforge-rules.schema.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema)
    payload = _valid_openapi()
    operation = payload["paths"]["/projects/{project_id}/status"]["get"]
    operation["responses"] = responses

    assert list(validator.iter_errors(operation))
    assert not validate_openapi(
        payload,
        expected_routes={("GET", "/projects/{project_id}/status")},
    ).valid


@pytest.mark.parametrize("invalid_status_code", ["2XX", "600"])
def test_openapi_extension_schema_and_domain_both_reject_extra_invalid_status_codes(
    invalid_status_code: str,
) -> None:
    root = Path(__file__).resolve().parents[1]
    schema = json.loads(
        (root / "contracts/schemas/openapi-shanforge-rules.schema.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema)
    payload = _valid_openapi()
    operation = payload["paths"]["/projects/{project_id}/status"]["get"]
    operation["responses"][invalid_status_code] = {
        "description": "不符合正式响应状态码规则的响应。"
    }

    assert list(validator.iter_errors(operation))
    report = validate_openapi(
        payload,
        expected_routes={("GET", "/projects/{project_id}/status")},
    )
    assert not report.valid
    assert "INVALID_RESPONSE_STATUS_CODE" in {issue.code for issue in report.issues}


def test_test_case_catalog_requires_traceability_and_action_expected_steps() -> None:
    report = validate_test_case_catalog(_valid_test_catalog())
    assert report.valid is True
    assert report.subject_count == 1

    invalid = _valid_test_catalog()
    invalid_case = invalid["cases"][0]
    invalid_case["traceability"] = {}
    invalid_case["steps"] = [{"action": "运行命令。"}]
    report = validate_test_case_catalog(invalid)

    assert report.valid is False
    assert {issue.code for issue in report.issues} >= {
        "REQUIREMENT_TRACE_REQUIRED",
        "EXPECTED_RESULT_REQUIRED",
    }


@pytest.mark.parametrize(
    "mutate",
    [
        lambda payload: payload.update({"id": "bad"}),
        lambda payload: payload["cases"][0]["test_data"][0].update({"value": [1, 2]}),
    ],
)
def test_test_catalog_schema_and_domain_reject_the_same_invalid_samples(
    mutate: Any,
) -> None:
    root = Path(__file__).resolve().parents[1]
    schema = json.loads(
        (root / "contracts/schemas/test-case-catalog.schema.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema)
    payload = _valid_test_catalog()
    mutate(payload)

    assert list(validator.iter_errors(payload))
    assert not validate_test_case_catalog(payload).valid


@pytest.mark.parametrize(
    "invalid_value",
    [
        float("nan"),
        float("inf"),
        {1: "value"},
        {"nested": {"not-json"}},
    ],
)
def test_test_catalog_domain_rejects_yaml_values_that_are_not_json(
    invalid_value: Any,
) -> None:
    payload = _valid_test_catalog()
    payload["cases"][0]["test_data"][0]["value"] = invalid_value

    validation = validate_test_case_catalog(payload)

    assert not validation.valid
    assert "INVALID_TEST_DATA_VALUE" in {issue.code for issue in validation.issues}


def test_test_catalog_accepts_nested_json_arrays_inside_an_object() -> None:
    payload = _valid_test_catalog()
    payload["cases"][0]["test_data"][0]["value"] = {"items": [1, 2, {"ok": True}]}

    assert validate_test_case_catalog(payload).valid


def test_test_catalog_rejects_a_cyclic_yaml_value_without_recursion_error() -> None:
    payload = _valid_test_catalog()
    cyclic: dict[str, Any] = {}
    cyclic["self"] = cyclic
    payload["cases"][0]["test_data"][0]["value"] = cyclic

    validation = validate_test_case_catalog(payload)

    assert not validation.valid
    assert "INVALID_TEST_DATA_VALUE" in {issue.code for issue in validation.issues}


def _valid_test_result(status: str = "passed") -> dict[str, Any]:
    return {
        "schema_id": "TestRunResult/v1",
        "id": f"RUN-RESULT-{status.upper().replace('_', '-')}",
        "run_id": "RUN-20260723-001",
        "test_case_id": "TEST-API-PROJECT-STATUS-001",
        "test_case_version": "1.0.0",
        "status": status,
        "started_at": "2026-07-23T17:00:00+08:00",
        "finished_at": "2026-07-23T17:00:01+08:00",
        "environment": {
            "id": "TEST-ENV-PYTEST",
            "git_commit": "a" * 40,
            "runtime": "python-3.14",
        },
        "step_results": [
            {
                "step": 1,
                "status": status,
                "actual": "合同校验返回预期结果。",
                "evidence_refs": ["EVIDENCE-PYTEST-001"],
            }
        ],
        "evidence": [
            {
                "id": "EVIDENCE-PYTEST-001",
                "kind": "pytest_log",
                "path": (
                    ".factory/workitems/PROJECT-ARTIFACTS-001/evidence/test-results/pytest.log"
                ),
                "sha256": "a" * 64,
            }
        ],
    }


@pytest.mark.parametrize(
    "status",
    ["passed", "failed", "error", "blocked", "skipped", "not_run", "cancelled"],
)
def test_test_run_result_accepts_the_seven_explicit_statuses(status: str) -> None:
    assert (
        validate_test_run_result(
            _valid_test_result(status),
            evidence_root=".factory/workitems/PROJECT-ARTIFACTS-001/evidence",
        ).valid
        is True
    )


def test_test_run_result_rejects_non_contiguous_steps_and_unsafe_evidence() -> None:
    payload = _valid_test_result()
    payload["step_results"][0]["step"] = 2
    payload["evidence"][0]["path"] = "../outside.log"

    validation = validate_test_run_result(
        payload,
        evidence_root=".factory/workitems/PROJECT-ARTIFACTS-001/evidence",
    )

    assert validation.valid is False
    assert {issue.code for issue in validation.issues} >= {
        "NON_CONTIGUOUS_STEP_RESULTS",
        "EVIDENCE_PATH_OUTSIDE_ROOT",
    }


@pytest.mark.parametrize(
    "mutation",
    ["failed_step", "empty_execution"],
)
def test_test_result_schema_and_domain_reject_false_passes(mutation: str) -> None:
    root = Path(__file__).resolve().parents[1]
    schema = json.loads(
        (root / "contracts/schemas/test-run-result.schema.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    payload = _valid_test_result()
    if mutation == "failed_step":
        payload["step_results"][0]["status"] = "failed"
    else:
        payload["step_results"] = []
        payload["evidence"] = []

    assert list(validator.iter_errors(payload))
    validation = validate_test_run_result(
        payload,
        evidence_root=".factory/workitems/PROJECT-ARTIFACTS-001/evidence",
    )
    assert not validation.valid
    assert {issue.code for issue in validation.issues} & {
        "TEST_RESULT_STATUS_MISMATCH",
        "PASSED_RESULT_EVIDENCE_REQUIRED",
    }


def _valid_test_report() -> dict[str, Any]:
    return {
        "schema_id": "TestReport/v1",
        "id": "TEST-REPORT-20260723-001",
        "run_id": "RUN-20260723-001",
        "title": "项目资产合同测试报告",
        "generated_at": "2026-07-23T17:00:02+08:00",
        "result_refs": [
            {
                "result_id": "RUN-RESULT-PASSED",
                "test_case_id": "TEST-API-PROJECT-STATUS-001",
                "status": "passed",
                "evidence_path": (
                    ".factory/workitems/PROJECT-ARTIFACTS-001/evidence/test-results/pytest.log"
                ),
                "sha256": "a" * 64,
            }
        ],
        "summary": {
            "total": 1,
            "passed": 1,
            "failed": 0,
            "error": 0,
            "blocked": 0,
            "skipped": 0,
            "not_run": 0,
            "cancelled": 0,
        },
    }


def _validated_passed_result() -> ValidatedTestResult:
    return ValidatedTestResult(
        result_id="RUN-RESULT-PASSED",
        run_id="RUN-20260723-001",
        test_case_id="TEST-API-PROJECT-STATUS-001",
        status="passed",
        evidence=(
            (
                ".factory/workitems/PROJECT-ARTIFACTS-001/evidence/test-results/pytest.log",
                "a" * 64,
            ),
        ),
    )


def test_test_report_rejects_counts_that_do_not_match_results() -> None:
    report = _valid_test_report()
    report["summary"]["total"] = 2
    report["summary"]["passed"] = 2

    validation = validate_test_report(
        report,
        validated_results_by_id={"RUN-RESULT-PASSED": _validated_passed_result()},
    )

    assert validation.valid is False
    assert {issue.code for issue in validation.issues} == {"REPORT_COUNT_MISMATCH"}


def test_test_report_rejects_a_valid_result_from_a_different_run() -> None:
    report = _valid_test_report()
    report["run_id"] = "RUN-DIFFERENT"

    validation = validate_test_report(
        report,
        validated_results_by_id={"RUN-RESULT-PASSED": _validated_passed_result()},
    )

    assert not validation.valid
    assert "REPORT_RESULT_MISMATCH" in {issue.code for issue in validation.issues}


@pytest.mark.parametrize(
    ("field", "value", "expected_code"),
    [
        ("status", "unknown", "INVALID_TEST_RESULT_STATUS"),
        ("sha256", "invalid", "INVALID_EVIDENCE_SHA256"),
        ("unexpected", True, "UNKNOWN_FIELD"),
    ],
)
def test_test_report_schema_and_domain_reject_the_same_structural_sample(
    field: str,
    value: Any,
    expected_code: str,
) -> None:
    root = Path(__file__).resolve().parents[1]
    schema = json.loads(
        (root / "contracts/schemas/test-report.schema.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    report = _valid_test_report()
    if field == "unexpected":
        report[field] = value
    else:
        report["result_refs"][0][field] = value

    assert list(validator.iter_errors(report))
    validation = validate_test_report(
        report,
        validated_results_by_id={"RUN-RESULT-PASSED": _validated_passed_result()},
    )
    assert not validation.valid
    assert expected_code in {issue.code for issue in validation.issues}


def test_test_schemas_and_domain_accept_the_same_valid_samples() -> None:
    root = Path(__file__).resolve().parents[1]
    catalog_schema = json.loads(
        (root / "contracts/schemas/test-case-catalog.schema.json").read_text(encoding="utf-8")
    )
    result_schema = json.loads(
        (root / "contracts/schemas/test-run-result.schema.json").read_text(encoding="utf-8")
    )
    report_schema = json.loads(
        (root / "contracts/schemas/test-report.schema.json").read_text(encoding="utf-8")
    )
    catalog = _valid_test_catalog()
    result = _valid_test_result()
    report = _valid_test_report()

    assert list(Draft202012Validator(catalog_schema).iter_errors(catalog)) == []
    assert validate_test_case_catalog(catalog).valid
    assert (
        list(
            Draft202012Validator(
                result_schema,
                format_checker=FormatChecker(),
            ).iter_errors(result)
        )
        == []
    )
    assert validate_test_run_result(
        result,
        evidence_root=".factory/workitems/PROJECT-ARTIFACTS-001/evidence",
    ).valid
    assert (
        list(
            Draft202012Validator(
                report_schema,
                format_checker=FormatChecker(),
            ).iter_errors(report)
        )
        == []
    )
    assert validate_test_report(
        report,
        validated_results_by_id={"RUN-RESULT-PASSED": _validated_passed_result()},
    ).valid


def test_test_contract_schemas_match_required_fields_and_statuses() -> None:
    root = Path(__file__).resolve().parents[1]
    catalog = json.loads(
        (root / "contracts/schemas/test-case-catalog.schema.json").read_text(encoding="utf-8")
    )
    result = json.loads(
        (root / "contracts/schemas/test-run-result.schema.json").read_text(encoding="utf-8")
    )
    report = json.loads(
        (root / "contracts/schemas/test-report.schema.json").read_text(encoding="utf-8")
    )

    assert set(catalog["$defs"]["case"]["required"]) >= {
        "traceability",
        "steps",
        "automation",
    }
    assert set(result["required"]) >= {
        "environment",
        "step_results",
        "evidence",
    }
    assert set(result["$defs"]["status"]["enum"]) == {
        "passed",
        "failed",
        "error",
        "blocked",
        "skipped",
        "not_run",
        "cancelled",
    }
    assert set(report["$defs"]["result_ref"]["required"]) == {
        "result_id",
        "test_case_id",
        "status",
        "evidence_path",
        "sha256",
    }


class _FakeApplication:
    def __init__(self) -> None:
        self.commands: list[str] = []

    def execute(self, command: str, **arguments: Any) -> dict[str, Any]:
        self.commands.append(command)
        return {"valid": True, "arguments": arguments}


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        (["design", "validate", "--json"], "design.validate"),
        (["api", "validate", "--json"], "api.validate"),
        (["test-cases", "validate", "--json"], "test-cases.validate"),
    ],
)
def test_cli_exposes_fixed_artifact_validation_commands(argv: list[str], expected: str) -> None:
    application = _FakeApplication()
    stdout = io.StringIO()

    exit_code = run(argv, application, stdout=stdout)

    assert exit_code == 0
    assert application.commands == [expected]
    assert json.loads(stdout.getvalue())["command"] == expected


def test_cli_keeps_existing_project_root_commands() -> None:
    application = _FakeApplication()
    stdout = io.StringIO()

    exit_code = run(["project", "find", "任务", "--json"], application, stdout=stdout)

    assert exit_code == 0
    assert application.commands == ["find"]


def test_repository_and_service_validate_all_artifacts(tmp_path: Path) -> None:
    import yaml

    (tmp_path / "design/ux-ui").mkdir(parents=True)
    (tmp_path / "contracts/openapi").mkdir(parents=True)
    (tmp_path / "tests/specifications").mkdir(parents=True)
    (tmp_path / "design/ux-ui/tokens.json").write_text(
        json.dumps(_valid_design_tokens(), ensure_ascii=False),
        encoding="utf-8",
    )
    (tmp_path / "design/ux-ui/design-manifest.yaml").write_text(
        yaml.safe_dump(_valid_design_manifest(), allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    (tmp_path / "contracts/openapi/openapi.yaml").write_text(
        yaml.safe_dump(_valid_openapi(), allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    (tmp_path / "tests/specifications/project-artifacts.testcases.yaml").write_text(
        yaml.safe_dump(_valid_test_catalog(), allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )

    repository = LocalProjectArtifactRepository(tmp_path)
    service = ProjectArtifactValidationService(
        repository,
        expected_routes={("GET", "/projects/{project_id}/status")},
    )

    result = service.validate_all()

    assert result["valid"] is True
    assert result["reports"]["design"]["subject_count"] == 2
    assert result["reports"]["api"]["subject_count"] == 1
    assert result["reports"]["test_cases"]["subject_count"] == 1
