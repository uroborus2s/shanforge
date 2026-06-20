from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_workspace_profile_catalog(
    workspace_root: Path | None,
    catalog_path: Path | None = None,
) -> dict[str, Any] | None:
    if catalog_path is not None:
        payload = _load_json_file(catalog_path)
        return payload if isinstance(payload, dict) else None
    if workspace_root is None:
        return None
    for candidate in (
        workspace_root / ".factory" / "runtime" / "profiles.json",
        workspace_root / ".factory" / "profiles.json",
    ):
        payload = _load_json_file(candidate)
        if isinstance(payload, dict):
            return payload
    return None


def list_workspace_profiles(
    workspace_root: Path | None,
    catalog_path: Path | None = None,
) -> tuple[dict[str, Any], ...]:
    catalog = load_workspace_profile_catalog(workspace_root, catalog_path=catalog_path)
    if catalog is None:
        return ()
    shared_backend_ids = _normalize_backend_ids(catalog.get("shared_backend_ids"))
    records: list[dict[str, Any]] = []
    for raw_profile in _normalize_profiles(catalog.get("profiles")):
        normalized = _merge_profile_record(
            raw_profile,
            workspace_root=workspace_root,
            shared_backend_ids=shared_backend_ids,
        )
        if normalized is not None:
            records.append(normalized)
    return tuple(records)


def resolve_workspace_profile(
    profile_id: str,
    workspace_root: Path | None,
    catalog_path: Path | None = None,
) -> dict[str, Any] | None:
    for record in list_workspace_profiles(workspace_root, catalog_path=catalog_path):
        if record.get("profile_id") == profile_id:
            return record
    return None


def resolve_workspace_default_profile_id(
    workspace_root: Path | None,
    catalog_path: Path | None = None,
) -> str | None:
    catalog = load_workspace_profile_catalog(workspace_root, catalog_path=catalog_path)
    if catalog is None:
        return None
    default_profile_id = catalog.get("default_profile_id")
    if default_profile_id is None:
        return None
    normalized = str(default_profile_id).strip()
    return normalized or None


def resolve_profile_rule_bundle_path(
    workspace_root: Path | None,
    profile_id: str,
    catalog_path: Path | None = None,
) -> Path | None:
    if workspace_root is None:
        return None
    record = resolve_workspace_profile(
        profile_id=profile_id,
        workspace_root=workspace_root,
        catalog_path=catalog_path,
    )
    if record is not None:
        profile_rule_path = record.get("rule_bundle_path")
        if isinstance(profile_rule_path, str) and profile_rule_path.strip():
            candidate = Path(profile_rule_path).expanduser()
            if not candidate.is_absolute():
                candidate = workspace_root / candidate
            candidate = candidate.resolve()
            if candidate.exists():
                return candidate
    for candidate in (
        workspace_root / ".factory" / "runtime" / "profiles" / profile_id / "rule-bundle.json",
        workspace_root / ".factory" / "profiles" / profile_id / "rule-bundle.json",
    ):
        if candidate.exists():
            return candidate
    return None


def _merge_profile_record(
    payload: dict[str, Any],
    workspace_root: Path | None,
    shared_backend_ids: dict[str, str],
) -> dict[str, Any] | None:
    profile_id = payload.get("profile_id", payload.get("id"))
    if profile_id is None:
        return None
    normalized_profile_id = str(profile_id).strip()
    if not normalized_profile_id:
        return None

    record = dict(payload)
    record["profile_id"] = normalized_profile_id
    record.setdefault("label", normalized_profile_id)
    merged_backend_ids = dict(shared_backend_ids)
    merged_backend_ids.update(_normalize_backend_ids(record.get("backend_ids")))
    if not merged_backend_ids and isinstance(record.get("bindings"), dict):
        merged_backend_ids.update(_normalize_backend_ids(record.get("bindings")))
    if merged_backend_ids:
        record["backend_ids"] = merged_backend_ids

    if workspace_root is not None:
        record.setdefault("workspace_root", str(workspace_root))
    profile_file_override = _load_profile_override(
        workspace_root=workspace_root,
        profile_id=normalized_profile_id,
    )
    if profile_file_override is not None:
        override_backend_ids = dict(record.get("backend_ids", {}))
        override_backend_ids.update(_normalize_backend_ids(profile_file_override.get("backend_ids")))
        record.update(profile_file_override)
        if override_backend_ids:
            record["backend_ids"] = override_backend_ids

    record.setdefault("source", "workspace-profile")
    return record


def _load_profile_override(
    workspace_root: Path | None,
    profile_id: str,
) -> dict[str, Any] | None:
    if workspace_root is None:
        return None
    for candidate in (
        workspace_root / ".factory" / "runtime" / "profiles" / f"{profile_id}.json",
        workspace_root / ".factory" / "profiles" / f"{profile_id}.json",
    ):
        payload = _load_json_file(candidate)
        if isinstance(payload, dict):
            return payload
    return None


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


def _load_json_file(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))
