"""Pure identities and validation rules for project knowledge."""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import PurePosixPath
from typing import Any


class AccessClass(StrEnum):
    PUBLIC = "public"
    PROJECT = "project"
    RESTRICTED = "restricted"


class ValueState(StrEnum):
    KNOWN = "known"
    UNKNOWN = "unknown"
    NOT_REGISTERED = "not_registered"
    NOT_APPLICABLE = "not_applicable"


def _reject_non_finite(value: object) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("canonical JSON does not permit non-finite numbers")
    if isinstance(value, Mapping):
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError("canonical JSON object keys must be strings")
            _reject_non_finite(item)
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for item in value:
            _reject_non_finite(item)


def canonical_json(value: object) -> str:
    """Return the repository's deterministic JSON representation.

    The supported contract data contains strings, integers, booleans, null, lists
    and objects. Sorting keys and rejecting non-finite values gives the JCS
    properties required by the stable identity formulas used here.
    """

    _reject_non_finite(value)
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def stable_id(namespace: str, identity: object) -> str:
    if not namespace or namespace.strip() != namespace or ":" in namespace:
        raise ValueError("namespace must be a non-empty trimmed token without ':'")
    digest = hashlib.sha256(canonical_json(identity).encode("utf-8")).hexdigest()
    return f"{namespace}:{digest}"


def document_section_key(document_id: str, section_id: str) -> str:
    return stable_id("mdsec", [document_id, section_id])


def _require_trimmed(value: str, name: str) -> None:
    if not value or value.strip() != value:
        raise ValueError(f"{name} must be a non-empty trimmed string")


def _validate_relative_path(relative_path: str) -> None:
    path = PurePosixPath(relative_path)
    if (
        not relative_path
        or relative_path != path.as_posix()
        or path.is_absolute()
        or ".." in path.parts
        or "." in path.parts
    ):
        raise ValueError("relative_path must be a normalized repository-relative path")


def _contains_line_locator(value: object) -> bool:
    if isinstance(value, Mapping):
        for key, item in value.items():
            lowered = str(key).lower()
            if lowered in {"line", "line_no", "line_number", "start_line", "end_line"}:
                return True
            if _contains_line_locator(item):
                return True
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return any(_contains_line_locator(item) for item in value)
    return False


@dataclass(frozen=True, slots=True)
class SourceDefinition:
    source_id: str
    registry_source_id: str
    kind: str
    relative_path: str
    extractor_id: str
    registry_version: str
    authority_rank: int
    access_class: AccessClass
    enabled: bool = True
    config: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in (
            "source_id",
            "registry_source_id",
            "kind",
            "extractor_id",
            "registry_version",
        ):
            _require_trimmed(getattr(self, name), name)
        _validate_relative_path(self.relative_path)
        if self.authority_rank < 0:
            raise ValueError("authority_rank must be non-negative")
        if type(self.enabled) is not bool:
            raise ValueError("enabled must be a bool")
        canonical_json(self.config)


@dataclass(frozen=True, slots=True)
class Locator:
    locator_id: str
    locator_kind: str
    selector: Mapping[str, Any]
    source_id: str

    def __post_init__(self) -> None:
        for name in ("locator_id", "locator_kind", "source_id"):
            _require_trimmed(getattr(self, name), name)
        if _contains_line_locator(self.selector):
            raise ValueError("line numbers cannot be part of a stable locator")
        canonical_json(self.selector)
