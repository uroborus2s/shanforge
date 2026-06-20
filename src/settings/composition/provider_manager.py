from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(slots=True, frozen=True)
class ResolvedProviderSelection:
    provider_id: str
    model_id: str
    source: str
    metadata: dict[str, Any] = field(default_factory=dict)
    requested_provider_id: str | None = None
    provider_bindings: tuple[str, ...] = ()


@dataclass(slots=True)
class DefaultProviderManager:
    """Resolves stable provider/model bindings from profile and settings inputs."""

    available_llm_providers: tuple[str, ...]
    ready_llm_providers: tuple[str, ...]
    default_provider: str
    default_model: str

    def resolve_llm_selection(
        self,
        profile_payload: Mapping[str, Any],
    ) -> ResolvedProviderSelection:
        provider_binding_metadata = _normalize_provider_binding_metadata(
            profile_payload.get("provider_binding_metadata")
        )
        llm_metadata = dict(provider_binding_metadata.get("llm_provider", {}))
        requested_provider_id = _first_non_empty(
            profile_payload.get("provider_id"),
            _lookup_backend_provider(profile_payload),
            self.default_provider,
            self.available_llm_providers[0] if self.available_llm_providers else None,
            "mock",
        )
        resolved_provider_id = self._resolve_provider_id(requested_provider_id)
        model_id = _first_non_empty(
            profile_payload.get("default_model"),
            self.default_model,
            "mock-chat",
        ) or "mock-chat"
        if requested_provider_id != resolved_provider_id:
            llm_metadata["requested_provider_id"] = requested_provider_id
            llm_metadata.setdefault("resolution", "fallback")
        llm_metadata.setdefault("binding_family", "llm_provider")
        source = (
            str(llm_metadata.get("binding_source") or "").strip()
            or ("profile" if profile_payload else "settings-default")
        )
        return ResolvedProviderSelection(
            provider_id=resolved_provider_id,
            model_id=model_id,
            source=source,
            metadata=llm_metadata,
            requested_provider_id=requested_provider_id,
            provider_bindings=(f"llm_provider:{resolved_provider_id}",),
        )

    def _resolve_provider_id(self, requested_provider_id: str | None) -> str:
        ready = set(self.ready_llm_providers)
        if requested_provider_id and requested_provider_id in ready:
            return requested_provider_id
        if self.default_provider in ready:
            return self.default_provider
        if "mock" in ready:
            return "mock"
        if self.ready_llm_providers:
            return self.ready_llm_providers[0]
        available = set(self.available_llm_providers)
        if requested_provider_id and requested_provider_id in available:
            return requested_provider_id
        if self.default_provider in available:
            return self.default_provider
        if "mock" in available:
            return "mock"
        if self.available_llm_providers:
            return self.available_llm_providers[0]
        return requested_provider_id or self.default_provider or "mock"


def _first_non_empty(*values: object) -> str | None:
    for value in values:
        if value is None:
            continue
        normalized = str(value).strip()
        if normalized:
            return normalized
    return None


def _lookup_backend_provider(profile_payload: Mapping[str, Any]) -> str | None:
    raw_backend_ids = profile_payload.get("backend_ids")
    if not isinstance(raw_backend_ids, Mapping):
        return None
    provider_id = raw_backend_ids.get("llm_provider")
    return _first_non_empty(provider_id)


def _normalize_provider_binding_metadata(raw_metadata: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(raw_metadata, Mapping):
        return {}
    normalized: dict[str, dict[str, Any]] = {}
    for family, payload in raw_metadata.items():
        family_text = str(family).strip()
        if not family_text or not isinstance(payload, Mapping):
            continue
        normalized[family_text] = dict(payload)
    return normalized
