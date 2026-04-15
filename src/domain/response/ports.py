from __future__ import annotations

from typing import Any, Mapping, Protocol


class ResponseSchemaValidationPort(Protocol):
    """Foundation capability contract consumed by the response domain for schema validation."""

    def validate_output(
        self,
        schema_name: str,
        payload: Mapping[str, Any],
    ) -> tuple[bool, tuple[str, ...]]: ...


class ResponseArtifactResolverPort(Protocol):
    """Foundation capability contract consumed by the response domain for artifact resolution."""

    def resolve_artifact(self, artifact_id: str) -> Mapping[str, Any] | None: ...


class ResponseUsageAccountingPort(Protocol):
    """Foundation capability contract consumed by the response domain for usage tracking."""

    def record_usage(
        self,
        session_id: str,
        usage: Mapping[str, Any],
    ) -> None: ...
