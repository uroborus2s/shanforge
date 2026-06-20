from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_workspace_backend_catalog(
    workspace_root: Path | None,
    catalog_path: Path | None = None,
) -> dict[str, Any] | None:
    resolved_path = resolve_workspace_backend_catalog_path(
        workspace_root,
        catalog_path=catalog_path,
    )
    if resolved_path is None:
        return None
    payload = _load_json_file(resolved_path)
    return payload if isinstance(payload, dict) else None


def resolve_workspace_backend_catalog_path(
    workspace_root: Path | None,
    catalog_path: Path | None = None,
) -> Path | None:
    if catalog_path is not None and catalog_path.exists():
        return catalog_path.expanduser().resolve()
    if workspace_root is None:
        return None
    for candidate in (
        workspace_root / ".factory" / "runtime" / "backend-bindings.json",
        workspace_root / ".factory" / "backend-bindings.json",
    ):
        if candidate.exists():
            return candidate.resolve()
    return None


def resolve_workspace_backend_bindings(
    profile_id: str,
    workspace_root: Path | None,
    catalog_path: Path | None = None,
) -> dict[str, Any]:
    resolved_backend_ids: dict[str, str] = {}
    resolved_backend_binding_metadata: dict[str, dict[str, Any]] = {}

    resolved_catalog_path = resolve_workspace_backend_catalog_path(
        workspace_root,
        catalog_path=catalog_path,
    )
    catalog = load_workspace_backend_catalog(workspace_root, catalog_path=catalog_path)
    if catalog is not None:
        source_path = str(resolved_catalog_path) if resolved_catalog_path is not None else None
        shared_backend_ids = _normalize_backend_ids(catalog.get("shared_backend_ids"))
        _merge_backend_ids(resolved_backend_ids, shared_backend_ids)
        _merge_backend_binding_metadata(
            resolved_backend_binding_metadata,
            _default_backend_binding_metadata(
                shared_backend_ids,
                binding_source="workspace-shared-backend-catalog",
                source_path=source_path,
            ),
        )
        _merge_backend_binding_metadata(
            resolved_backend_binding_metadata,
            _normalize_backend_binding_metadata(
                catalog.get("shared_backend_binding_metadata"),
                binding_source="workspace-shared-backend-catalog",
                source_path=source_path,
                base_path=(
                    resolved_catalog_path.parent
                    if resolved_catalog_path is not None
                    else None
                ),
            ),
        )
        for profile_record in _normalize_profiles(catalog.get("profiles")):
            if str(profile_record.get("profile_id", "")).strip() != profile_id:
                continue
            profile_backend_ids = _normalize_backend_ids(profile_record.get("backend_ids"))
            _merge_backend_ids(resolved_backend_ids, profile_backend_ids)
            _merge_backend_binding_metadata(
                resolved_backend_binding_metadata,
                _default_backend_binding_metadata(
                    profile_backend_ids,
                    binding_source="workspace-backend-catalog",
                    source_path=source_path,
                ),
            )
            _merge_backend_binding_metadata(
                resolved_backend_binding_metadata,
                _normalize_backend_binding_metadata(
                    profile_record.get("backend_binding_metadata"),
                    binding_source="workspace-backend-catalog",
                    source_path=source_path,
                    base_path=(
                        resolved_catalog_path.parent
                        if resolved_catalog_path is not None
                        else None
                    ),
                ),
            )
            break

    profile_override_path = resolve_profile_backend_bindings_path(
        workspace_root=workspace_root,
        profile_id=profile_id,
    )
    if profile_override_path is not None:
        payload = _load_json_file(profile_override_path)
        if isinstance(payload, dict):
            override_backend_ids = _normalize_backend_ids(payload.get("backend_ids"))
            _merge_backend_ids(resolved_backend_ids, override_backend_ids)
            _merge_backend_binding_metadata(
                resolved_backend_binding_metadata,
                _default_backend_binding_metadata(
                    override_backend_ids,
                    binding_source="workspace-profile-backend-file",
                    source_path=str(profile_override_path),
                ),
            )
            _merge_backend_binding_metadata(
                resolved_backend_binding_metadata,
                _normalize_backend_binding_metadata(
                    payload.get("backend_binding_metadata"),
                    binding_source="workspace-profile-backend-file",
                    source_path=str(profile_override_path),
                    base_path=profile_override_path.parent,
                ),
            )

    result: dict[str, Any] = {}
    if resolved_backend_ids:
        result["backend_ids"] = resolved_backend_ids
    if resolved_backend_binding_metadata:
        result["backend_binding_metadata"] = resolved_backend_binding_metadata
    return result


def resolve_profile_backend_bindings_path(
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
        / "backend-bindings.json",
        workspace_root / ".factory" / "profiles" / profile_id / "backend-bindings.json",
    ):
        if candidate.exists():
            return candidate.resolve()
    return None


def _merge_backend_ids(target: dict[str, str], source: dict[str, str]) -> None:
    for family, binding_id in source.items():
        target[family] = binding_id


def _merge_backend_binding_metadata(
    target: dict[str, dict[str, Any]],
    source: dict[str, dict[str, Any]],
) -> None:
    for family, metadata in source.items():
        merged = dict(target.get(family, {}))
        merged.update(metadata)
        target[family] = merged


def _default_backend_binding_metadata(
    backend_ids: dict[str, str],
    *,
    binding_source: str,
    source_path: str | None,
) -> dict[str, dict[str, Any]]:
    metadata: dict[str, dict[str, Any]] = {}
    for family in backend_ids:
        payload: dict[str, Any] = {"binding_source": binding_source}
        if source_path:
            payload["source_path"] = source_path
        metadata[family] = payload
    return metadata


def _normalize_profiles(raw_profiles: Any) -> tuple[dict[str, Any], ...]:
    if not isinstance(raw_profiles, list):
        return ()
    normalized: list[dict[str, Any]] = []
    for item in raw_profiles:
        if isinstance(item, dict):
            normalized.append(dict(item))
    return tuple(normalized)


def _normalize_backend_ids(raw_backend_ids: Any) -> dict[str, str]:
    if not isinstance(raw_backend_ids, dict):
        return {}
    normalized: dict[str, str] = {}
    for family, choice in raw_backend_ids.items():
        family_text = str(family).strip()
        choice_text = str(choice).strip()
        if family_text and choice_text:
            normalized[family_text] = choice_text
    return normalized


def _normalize_backend_binding_metadata(
    raw_metadata: Any,
    *,
    binding_source: str,
    source_path: str | None,
    base_path: Path | None = None,
) -> dict[str, dict[str, Any]]:
    if not isinstance(raw_metadata, dict):
        return {}
    normalized: dict[str, dict[str, Any]] = {}
    for family, payload in raw_metadata.items():
        family_text = str(family).strip()
        if not family_text or not isinstance(payload, dict):
            continue
        metadata = _resolve_metadata_source(dict(payload), base_path=base_path)
        metadata.setdefault("binding_source", binding_source)
        if source_path:
            metadata.setdefault("source_path", source_path)
        normalized[family_text] = metadata
    return normalized


def _resolve_metadata_source(
    metadata: dict[str, Any],
    *,
    base_path: Path | None,
) -> dict[str, Any]:
    metadata_file = str(metadata.get("metadata_file") or "").strip()
    if not metadata_file:
        return _resolve_relative_file_fields(metadata, base_path=base_path)
    resolved_path = _resolve_relative_path(metadata_file, base_path=base_path)
    source_payload = _load_json_file(resolved_path)
    merged = dict(source_payload) if isinstance(source_payload, dict) else {}
    merged.update(metadata)
    merged.pop("metadata_file", None)
    merged["metadata_source_path"] = str(resolved_path)
    return _resolve_relative_file_fields(merged, base_path=resolved_path.parent)


def _resolve_relative_file_fields(
    metadata: dict[str, Any],
    *,
    base_path: Path | None,
) -> dict[str, Any]:
    if base_path is None:
        return dict(metadata)
    resolved = dict(metadata)
    for key, value in tuple(resolved.items()):
        key_text = str(key).strip()
        if not key_text.endswith("_file"):
            continue
        raw_path = str(value or "").strip()
        if not raw_path:
            continue
        resolved[key_text] = str(_resolve_relative_path(raw_path, base_path=base_path))
    return resolved


def _resolve_relative_path(raw_path: str, *, base_path: Path | None) -> Path:
    candidate = Path(raw_path).expanduser()
    if candidate.is_absolute():
        return candidate.resolve()
    if base_path is None:
        return candidate.resolve()
    return (base_path / candidate).resolve()


def _load_json_file(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))
