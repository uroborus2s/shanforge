"""Application orchestration for project artifact validation."""

from __future__ import annotations

from collections.abc import Mapping, Set
from typing import Any, Protocol

from domain.project_artifacts.validation import (
    validate_design_manifest,
    validate_design_tokens,
    validate_openapi,
    validate_test_case_catalog,
)


class ProjectArtifactRepositoryPort(Protocol):
    def design_manifest(self) -> Mapping[str, Any]: ...

    def design_tokens(self, relative_path: str) -> Mapping[str, Any]: ...

    def openapi_contract(self) -> Mapping[str, Any]: ...

    def test_case_catalogs(self) -> tuple[Mapping[str, Any], ...]: ...

    def available_design_paths(self) -> Set[str]: ...


class ProjectArtifactValidationService:
    def __init__(
        self,
        repository: ProjectArtifactRepositoryPort,
        *,
        expected_routes: set[tuple[str, str]] | frozenset[tuple[str, str]],
    ) -> None:
        self._repository = repository
        self._expected_routes = frozenset(expected_routes)

    def validate_design(self) -> dict[str, Any]:
        manifest = self._repository.design_manifest()
        manifest_report = validate_design_manifest(
            manifest,
            available_paths=self._repository.available_design_paths(),
        ).to_dict()
        tokens_path = manifest.get("tokens_file")
        if not isinstance(tokens_path, str) or not tokens_path:
            return manifest_report
        tokens_report = validate_design_tokens(
            self._repository.design_tokens(tokens_path)
        ).to_dict()
        issues = list(manifest_report["issues"]) + [
            {
                **dict(issue),
                "path": f"/tokens{issue['path']}",
            }
            for issue in list(tokens_report["issues"])
        ]
        return {
            **manifest_report,
            "valid": not issues,
            "issues": issues,
            "token_subject_count": tokens_report["subject_count"],
        }

    def validate_api(self) -> dict[str, Any]:
        return validate_openapi(
            self._repository.openapi_contract(),
            expected_routes=self._expected_routes,
        ).to_dict()

    def validate_test_cases(self) -> dict[str, Any]:
        reports = [
            validate_test_case_catalog(catalog).to_dict()
            for catalog in self._repository.test_case_catalogs()
        ]
        issues = [issue for report in reports for issue in list(report.get("issues") or [])]
        return {
            "schema_id": "ArtifactValidationReport/v1",
            "artifact_kind": "test_cases",
            "valid": not issues,
            "subject_count": sum(int(report["subject_count"]) for report in reports),
            "issues": issues,
            "catalog_count": len(reports),
        }

    def validate_all(self) -> dict[str, Any]:
        reports = {
            "design": self.validate_design(),
            "api": self.validate_api(),
            "test_cases": self.validate_test_cases(),
        }
        return {
            "schema_id": "ProjectArtifactValidationSummary/v1",
            "valid": all(bool(report["valid"]) for report in reports.values()),
            "reports": reports,
        }
