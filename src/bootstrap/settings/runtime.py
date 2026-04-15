from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class Settings:
    """Runtime settings for the v2 platform scaffold."""

    default_provider: str = "mock"
    default_model: str = "mock-chat"
    allowed_writeset_prefixes: tuple[str, ...] = ()
    memory_store_root: str | None = None
    memory_summarizer_provider: str | None = None
    memory_summarizer_model: str | None = None
    memory_summarizer_extract_model: str | None = None
    memory_promotion_default_min_confidence: float = 0.6
    memory_promotion_min_confidence_by_kind: dict[str, float] = field(default_factory=dict)
    memory_promotion_draft_kinds: tuple[str, ...] = ("procedural", "reflective")
    memory_promotion_allowed_scopes_by_kind: dict[str, tuple[str, ...]] = field(
        default_factory=dict
    )
    hermes_repo_root: str | None = None
    hermes_enabled_adapters: tuple[str, ...] = ()

    @classmethod
    def from_env(cls) -> "Settings":
        prefixes = tuple(
            item.strip()
            for item in os.getenv("SHANFORGE_ALLOWED_WRITESET_PREFIXES", "").split(",")
            if item.strip()
        )

        return cls(
            default_provider=os.getenv("SHANFORGE_DEFAULT_PROVIDER", "mock"),
            default_model=os.getenv("SHANFORGE_DEFAULT_MODEL", "mock-chat"),
            allowed_writeset_prefixes=prefixes,
            memory_store_root=os.getenv("SHANFORGE_MEMORY_STORE_ROOT") or None,
            memory_summarizer_provider=os.getenv("SHANFORGE_MEMORY_SUMMARIZER_PROVIDER") or None,
            memory_summarizer_model=os.getenv("SHANFORGE_MEMORY_SUMMARIZER_MODEL") or None,
            memory_summarizer_extract_model=(
                os.getenv("SHANFORGE_MEMORY_SUMMARIZER_EXTRACT_MODEL") or None
            ),
            memory_promotion_default_min_confidence=float(
                os.getenv("SHANFORGE_MEMORY_PROMOTION_DEFAULT_MIN_CONFIDENCE", "0.6")
            ),
            memory_promotion_min_confidence_by_kind=_parse_float_mapping(
                os.getenv("SHANFORGE_MEMORY_PROMOTION_MIN_CONFIDENCE_BY_KIND", "")
            ),
            memory_promotion_draft_kinds=_parse_csv(
                os.getenv("SHANFORGE_MEMORY_PROMOTION_DRAFT_KINDS", "procedural,reflective")
            ),
            memory_promotion_allowed_scopes_by_kind=_parse_scope_mapping(
                os.getenv("SHANFORGE_MEMORY_PROMOTION_ALLOWED_SCOPES_BY_KIND", "")
            ),
            hermes_repo_root=os.getenv("SHANFORGE_HERMES_REPO_ROOT") or None,
            hermes_enabled_adapters=_parse_csv(
                os.getenv("SHANFORGE_HERMES_ENABLED_ADAPTERS", "")
            ),
        )


def _parse_csv(raw: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in raw.split(",") if item.strip())


def _parse_float_mapping(raw: str) -> dict[str, float]:
    mapping: dict[str, float] = {}
    for chunk in raw.split(","):
        key, separator, value = chunk.partition(":")
        if not separator:
            continue
        key = key.strip()
        value = value.strip()
        if not key or not value:
            continue
        mapping[key] = float(value)
    return mapping


def _parse_scope_mapping(raw: str) -> dict[str, tuple[str, ...]]:
    mapping: dict[str, tuple[str, ...]] = {}
    for chunk in raw.split(";"):
        key, separator, value = chunk.partition(":")
        if not separator:
            continue
        key = key.strip()
        scopes = tuple(item.strip() for item in value.split("|") if item.strip())
        if key and scopes:
            mapping[key] = scopes
    return mapping
