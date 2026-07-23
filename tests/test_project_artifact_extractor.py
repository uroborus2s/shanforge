from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest
import yaml

from domain.project_knowledge.models import AccessClass, SourceDefinition
from runtime.project_artifacts.yaml_extractor import YamlProjectArtifactExtractor
from settings.project_artifacts.source_registry import ProjectArtifactSourceRegistry


def _source(relative_path: str) -> SourceDefinition:
    return SourceDefinition(
        source_id=f"source:yaml:{relative_path}",
        registry_source_id="SRC-PROJECT-ARTIFACT-YAML",
        kind="yaml",
        relative_path=relative_path,
        extractor_id="project-artifact-yaml-v1",
        registry_version="1",
        authority_rank=100,
        access_class=AccessClass.PROJECT,
    )


def _extract(relative_path: str) -> dict[str, object]:
    root = Path(__file__).resolve().parents[1]
    available_design_paths = {
        path.relative_to(root).as_posix()
        for path in (root / "design/ux-ui").rglob("*")
        if path.is_file() and not path.is_symlink()
    }
    return YamlProjectArtifactExtractor(available_design_paths=available_design_paths).extract(
        _source(relative_path),
        (root / relative_path).read_bytes(),
    )


def test_design_manifest_has_stable_entities_locators_and_contains_relations() -> None:
    contribution = _extract("design/ux-ui/design-manifest.yaml")
    entities = {
        item["entity_id"]: item
        for item in contribution["entities"]  # type: ignore[index,union-attr]
    }

    assert entities["DESIGN-ASSET-UX-UI-001"]["entity_kind"] == "design_asset"
    assert entities["UI-PAGE-PROJECT-DASHBOARD"]["entity_kind"] == "ui_page"
    assert entities["UI-COMPONENT-TASK-CARD"]["entity_kind"] == "ui_component"
    assert {
        (item["from_entity_id"], item["to_entity_id"], item["relation_type"])
        for item in contribution["relations"]  # type: ignore[index,union-attr]
    } >= {
        ("doc:DESIGN-UX-UI-001", "DESIGN-ASSET-UX-UI-001", "CONTAINS"),
        ("DESIGN-ASSET-UX-UI-001", "UI-PAGE-PROJECT-DASHBOARD", "CONTAINS"),
        ("DESIGN-ASSET-UX-UI-001", "UI-COMPONENT-TASK-CARD", "CONTAINS"),
    }
    selectors = [
        item["selector"]
        for item in contribution["locators"]  # type: ignore[index,union-attr]
    ]
    assert {"kind": "yaml_path", "path": ["pages", 0]} in selectors
    assert all("line" not in str(selector).casefold() for selector in selectors)


def test_openapi_operations_have_stable_entities_locators_and_relations() -> None:
    contribution = _extract("contracts/openapi/openapi.yaml")
    entities = {
        item["entity_id"]: item
        for item in contribution["entities"]  # type: ignore[index,union-attr]
    }

    operation = entities["API-HTTP-PROJECT-STATUS"]
    assert operation["entity_kind"] == "api_operation"
    assert operation["display_name"] == "查询项目状态"
    assert operation["details"]["method"] == "GET"  # type: ignore[index]
    assert operation["details"]["path"] == "/projects/{project_id}/status"  # type: ignore[index]
    assert {
        (item["from_entity_id"], item["to_entity_id"], item["relation_type"])
        for item in contribution["relations"]  # type: ignore[index,union-attr]
    } >= {
        ("doc:DESIGN-API-001", "API-HTTP-PROJECT-STATUS", "CONTAINS"),
        ("API-HTTP-PROJECT-STATUS", "REQ-PKI-008", "SATISFIES"),
    }
    locator = next(
        item
        for item in contribution["locators"]  # type: ignore[index,union-attr]
        if item["entity_id"] == "API-HTTP-PROJECT-STATUS"
    )
    assert locator["selector"] == {
        "kind": "yaml_path",
        "path": ["paths", "/projects/{project_id}/status", "get"],
    }


def test_composite_registry_discovers_human_docs_and_machine_artifacts() -> None:
    root = Path(__file__).resolve().parents[1]
    registry = ProjectArtifactSourceRegistry(
        root,
        root / ".factory/project-knowledge/source-registry.json",
        root / ".factory/project-knowledge/artifact-source-registry.json",
    )

    sources = registry.sources()
    paths = {source.relative_path: source for source in sources}

    assert paths["docs/05-design/ux-ui-design.md"].kind == "markdown"
    assert paths["design/ux-ui/design-manifest.yaml"].kind == "yaml"
    assert paths["contracts/openapi/openapi.yaml"].kind == "yaml"
    assert len({source.source_id for source in sources}) == len(sources)


def test_yaml_extractor_rejects_openapi_that_fails_the_machine_contract() -> None:
    root = Path(__file__).resolve().parents[1]
    payload = yaml.safe_load((root / "contracts/openapi/openapi.yaml").read_text())
    payload["paths"]["/projects/{project_id}/status"]["get"]["summary"] = "Get status"
    content = yaml.safe_dump(payload, allow_unicode=True, sort_keys=False).encode()

    with pytest.raises(ValueError, match="CHINESE_SUMMARY_REQUIRED"):
        YamlProjectArtifactExtractor().extract(
            _source("contracts/openapi/openapi.yaml"),
            content,
        )


def test_composite_registry_rejects_forged_definition_with_registered_source_id() -> None:
    root = Path(__file__).resolve().parents[1]
    registry = ProjectArtifactSourceRegistry(
        root,
        root / ".factory/project-knowledge/source-registry.json",
        root / ".factory/project-knowledge/artifact-source-registry.json",
    )
    source = next(
        item
        for item in registry.sources()
        if item.relative_path == "contracts/openapi/openapi.yaml"
    )
    forged = replace(source, relative_path="README.md")

    with pytest.raises(ValueError, match="definition"):
        registry.read_bytes(forged)


def test_test_catalog_projects_definitions_and_traceability_without_run_results() -> None:
    contribution = _extract("tests/specifications/project-artifacts.testcases.yaml")
    entities = {
        item["entity_id"]: item
        for item in contribution["entities"]  # type: ignore[index,union-attr]
    }
    test = entities["TEST-API-PROJECT-STATUS-001"]

    assert test["entity_kind"] == "test"
    assert test["lifecycle_status"] == "active"
    assert {
        (item["from_entity_id"], item["to_entity_id"], item["relation_type"])
        for item in contribution["relations"]  # type: ignore[index,union-attr]
        if item["from_entity_id"] == "TEST-API-PROJECT-STATUS-001"
    } >= {
        ("TEST-API-PROJECT-STATUS-001", "REQ-PKI-008", "VERIFIES"),
        (
            "TEST-API-PROJECT-STATUS-001",
            "doc:DESIGN-API-001",
            "VERIFIES",
        ),
        (
            "TEST-API-PROJECT-STATUS-001",
            "UI-PAGE-PROJECT-DASHBOARD",
            "VERIFIES",
        ),
        (
            "TEST-API-PROJECT-STATUS-001",
            "API-HTTP-PROJECT-STATUS",
            "VERIFIES",
        ),
    }
    tests = contribution["tests"]  # type: ignore[index]
    assert tests[3]["test_status"] == "definition:active"  # type: ignore[index]
    assert "result" not in contribution
