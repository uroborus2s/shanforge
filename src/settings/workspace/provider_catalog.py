from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_workspace_provider_catalog(
    workspace_root: Path | None,
    catalog_path: Path | None = None,
) -> dict[str, Any] | None:
    resolved_path = resolve_workspace_provider_catalog_path(
        workspace_root,
        catalog_path=catalog_path,
    )
    if resolved_path is None:
        return None
    payload = _load_json_file(resolved_path)
    return payload if isinstance(payload, dict) else None


def resolve_workspace_provider_catalog_path(
    workspace_root: Path | None,
    catalog_path: Path | None = None,
) -> Path | None:
    if catalog_path is not None and catalog_path.exists():
        return catalog_path.expanduser().resolve()
    if workspace_root is None:
        return None
    for candidate in (
        workspace_root / ".factory" / "runtime" / "provider-bindings.json",
        workspace_root / ".factory" / "provider-bindings.json",
    ):
        if candidate.exists():
            return candidate.resolve()
    return None


def resolve_workspace_provider_bindings(
    profile_id: str,
    workspace_root: Path | None,
    catalog_path: Path | None = None,
) -> dict[str, Any]:
    resolved_provider_id: str | None = None
    resolved_default_model: str | None = None
    resolved_provider_binding_metadata: dict[str, dict[str, Any]] = {}

    resolved_catalog_path = resolve_workspace_provider_catalog_path(
        workspace_root,
        catalog_path=catalog_path,
    )
    catalog = load_workspace_provider_catalog(workspace_root, catalog_path=catalog_path)
    if catalog is not None:
        source_path = str(resolved_catalog_path) if resolved_catalog_path is not None else None
        resolved_provider_id = _first_non_empty(
            catalog.get("shared_provider_id"),
            resolved_provider_id,
        )
        resolved_default_model = _first_non_empty(
            catalog.get("shared_default_model"),
            resolved_default_model,
        )
        _merge_provider_binding_metadata(
            resolved_provider_binding_metadata,
            _normalize_provider_binding_metadata(
                catalog.get("shared_provider_binding_metadata"),
                binding_source="workspace-shared-provider-catalog",
                source_path=source_path,
            ),
        )
        for profile_record in _normalize_profiles(catalog.get("profiles")):
            if str(profile_record.get("profile_id", "")).strip() != profile_id:
                continue
            resolved_provider_id = _first_non_empty(
                profile_record.get("provider_id"),
                resolved_provider_id,
            )
            resolved_default_model = _first_non_empty(
                profile_record.get("default_model"),
                resolved_default_model,
            )
            _merge_provider_binding_metadata(
                resolved_provider_binding_metadata,
                _default_provider_binding_metadata(
                    provider_id=profile_record.get("provider_id"),
                    binding_source="workspace-provider-catalog",
                    source_path=source_path,
                ),
            )
            _merge_provider_binding_metadata(
                resolved_provider_binding_metadata,
                _normalize_provider_binding_metadata(
                    profile_record.get("provider_binding_metadata"),
                    binding_source="workspace-provider-catalog",
                    source_path=source_path,
                ),
            )
            break

    profile_override_path = resolve_profile_provider_bindings_path(
        workspace_root=workspace_root,
        profile_id=profile_id,
    )
    if profile_override_path is not None:
        payload = _load_json_file(profile_override_path)
        if isinstance(payload, dict):
            resolved_provider_id = _first_non_empty(
                payload.get("provider_id"),
                resolved_provider_id,
            )
            resolved_default_model = _first_non_empty(
                payload.get("default_model"),
                resolved_default_model,
            )
            _merge_provider_binding_metadata(
                resolved_provider_binding_metadata,
                _default_provider_binding_metadata(
                    provider_id=payload.get("provider_id"),
                    binding_source="workspace-profile-provider-file",
                    source_path=str(profile_override_path),
                ),
            )
            _merge_provider_binding_metadata(
                resolved_provider_binding_metadata,
                _normalize_provider_binding_metadata(
                    payload.get("provider_binding_metadata"),
                    binding_source="workspace-profile-provider-file",
                    source_path=str(profile_override_path),
                ),
            )

    result: dict[str, Any] = {}
    if resolved_provider_id is not None:
        result["provider_id"] = resolved_provider_id
    if resolved_default_model is not None:
        result["default_model"] = resolved_default_model
    if resolved_provider_binding_metadata:
        result["provider_binding_metadata"] = resolved_provider_binding_metadata
    return result


def resolve_profile_provider_bindings_path(
    workspace_root: Path | None,
    profile_id: str,
) -> Path | None:
    if workspace_root is None:
        return None
    for candidate in (
        workspace_root
        / ".factory"
        / "runtime"
        / "profiles"
        / profile_id
        / "provider-bindings.json",
        workspace_root / ".factory" / "profiles" / profile_id / "provider-bindings.json",
    ):
        if candidate.exists():
            return candidate.resolve()
    return None


def _first_non_empty(*values: object) -> str | None:
    for value in values:
        if value is None:
            continue
        normalized = str(value).strip()
        if normalized:
            return normalized
    return None


def _merge_provider_binding_metadata(
    target: dict[str, dict[str, Any]],
    source: dict[str, dict[str, Any]],
) -> None:
    for family, metadata in source.items():
        merged = dict(target.get(family, {}))
        merged.update(metadata)
        target[family] = merged


def _default_provider_binding_metadata(
    *,
    provider_id: object,
    binding_source: str,
    source_path: str | None,
) -> dict[str, dict[str, Any]]:
    provider_text = _first_non_empty(provider_id)
    if provider_text is None:
        return {}
    payload: dict[str, Any] = {
        "binding_source": binding_source,
        "requested_binding_id": provider_text,
    }
    if source_path:
        payload["source_path"] = source_path
    return {"llm_provider": payload}


def _normalize_provider_binding_metadata(
    raw_metadata: Any,
    *,
    binding_source: str,
    source_path: str | None,
) -> dict[str, dict[str, Any]]:
    if not isinstance(raw_metadata, dict):
        return {}
    normalized: dict[str, dict[str, Any]] = {}
    for family, payload in raw_metadata.items():
        family_text = str(family).strip()
        if not family_text or not isinstance(payload, dict):
            continue
        metadata = dict(payload)
        metadata.setdefault("binding_source", binding_source)
        if source_path:
            metadata.setdefault("source_path", source_path)
        normalized[family_text] = metadata
    return normalized


def _normalize_profiles(raw_profiles: Any) -> tuple[dict[str, Any], ...]:
    if not isinstance(raw_profiles, list):
        return ()
    normalized: list[dict[str, Any]] = []
    for item in raw_profiles:
        if isinstance(item, dict):
            normalized.append(dict(item))
    return tuple(normalized)


def _load_json_file(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))
