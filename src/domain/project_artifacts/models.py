"""Value objects returned by project artifact validation."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ArtifactValidationIssue:
    code: str
    path: str
    message: str


@dataclass(frozen=True, slots=True)
class ArtifactValidationReport:
    schema_id: str
    artifact_kind: str
    valid: bool
    subject_count: int
    issues: tuple[ArtifactValidationIssue, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ValidatedTestResult:
    """Trusted fields exposed to the report validator after result validation."""

    result_id: str
    run_id: str
    test_case_id: str
    status: str
    evidence: tuple[tuple[str, str], ...]
