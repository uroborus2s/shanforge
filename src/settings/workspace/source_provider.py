from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from runtime.ports.source_backends import ProfileSourceProviderPort, RuleSourceProviderPort
from settings.workspace.backend_catalog import resolve_workspace_backend_bindings
from settings.workspace.profile_catalog import (
    list_workspace_profiles,
    resolve_profile_rule_bundle_path,
    resolve_workspace_default_profile_id,
    resolve_workspace_profile,
)
from settings.workspace.provider_catalog import resolve_workspace_provider_bindings


def _first_non_empty(*values: object) -> str | None:
    for value in values:
        if value is None:
            continue
        normalized = str(value).strip()
        if normalized:
            return normalized
    return None


@dataclass(slots=True)
class LocalProfileSourceProvider(ProfileSourceProviderPort):
    """Local profile resolver backed by explicit hints and settings defaults."""

    default_profile_id: str = "local-dev"
    default_workspace_root: Path | None = None
    catalog_path: Path | None = None
    backend_catalog_path: Path | None = None
    provider_catalog_path: Path | None = None
    labels: Mapping[str, str] | None = None

    def resolve_profile(self, lookup: Mapping[str, Any]) -> Mapping[str, Any] | None:
        workspace_root = self._resolve_workspace_root(lookup.get("workspace_root"))
        catalog_default_profile_id = resolve_workspace_default_profile_id(
            workspace_root,
            catalog_path=self.catalog_path,
        )
        profile_id = _first_non_empty(
            lookup.get("profile_id"),
            lookup.get("context_profile_id"),
            catalog_default_profile_id,
            lookup.get("default_profile_id"),
            self.default_profile_id,
        )
        if profile_id is None:
            return None
        catalog_profile = resolve_workspace_profile(
            profile_id=profile_id,
            workspace_root=workspace_root,
            catalog_path=self.catalog_path,
        )
        if catalog_profile is not None:
            payload = dict(catalog_profile)
            payload.update(
                _merge_profile_backend_payload(
                    payload,
                    profile_id=profile_id,
                    workspace_root=workspace_root,
                    backend_catalog_path=self.backend_catalog_path,
                )
            )
            payload.update(
                _merge_profile_provider_payload(
                    payload,
                    profile_id=profile_id,
                    workspace_root=workspace_root,
                    provider_catalog_path=self.provider_catalog_path,
                )
            )
            payload.setdefault("label", self._resolve_label(profile_id))
            payload.setdefault("source", "workspace-profile")
            return payload
        payload = {
            "profile_id": profile_id,
            "label": self._resolve_label(profile_id),
            "source": "settings-local",
        }
        payload.update(
            _merge_profile_backend_payload(
                payload,
                profile_id=profile_id,
                workspace_root=workspace_root,
                backend_catalog_path=self.backend_catalog_path,
            )
        )
        payload.update(
            _merge_profile_provider_payload(
                payload,
                profile_id=profile_id,
                workspace_root=workspace_root,
                provider_catalog_path=self.provider_catalog_path,
            )
        )
        return payload

    def list_profiles(self) -> tuple[Mapping[str, Any], ...]:
        workspace_profiles = list_workspace_profiles(
            self._resolve_workspace_root(None),
            catalog_path=self.catalog_path,
        )
        if workspace_profiles:
            workspace_root = self._resolve_workspace_root(None)
            return tuple(
                _merge_profile_provider_payload(
                    _merge_profile_backend_payload(
                        dict(record),
                        profile_id=str(record.get("profile_id") or ""),
                        workspace_root=workspace_root,
                        backend_catalog_path=self.backend_catalog_path,
                    ),
                    profile_id=str(record.get("profile_id") or ""),
                    workspace_root=workspace_root,
                    provider_catalog_path=self.provider_catalog_path,
                )
                for record in workspace_profiles
            )
        if self.labels:
            return tuple(
                _merge_profile_provider_payload(
                    _merge_profile_backend_payload(
                        {
                            "profile_id": profile_id,
                            "label": label,
                            "source": "settings-local",
                        },
                        profile_id=profile_id,
                        workspace_root=self._resolve_workspace_root(None),
                        backend_catalog_path=self.backend_catalog_path,
                    ),
                    profile_id=profile_id,
                    workspace_root=self._resolve_workspace_root(None),
                    provider_catalog_path=self.provider_catalog_path,
                )
                for profile_id, label in self.labels.items()
            )
        return (
            _merge_profile_provider_payload(
                _merge_profile_backend_payload(
                    {
                        "profile_id": self.default_profile_id,
                        "label": self._resolve_label(self.default_profile_id),
                        "source": "settings-local",
                    },
                    profile_id=self.default_profile_id,
                    workspace_root=self._resolve_workspace_root(None),
                    backend_catalog_path=self.backend_catalog_path,
                ),
                profile_id=self.default_profile_id,
                workspace_root=self._resolve_workspace_root(None),
                provider_catalog_path=self.provider_catalog_path,
            ),
        )

    def _resolve_label(self, profile_id: str) -> str:
        if self.labels is not None and profile_id in self.labels:
            return str(self.labels[profile_id])
        return profile_id

    def _resolve_workspace_root(self, workspace_root: Any) -> Path | None:
        if workspace_root is None and self.default_workspace_root is None:
            return None
        candidate = workspace_root or self.default_workspace_root
        if candidate is None:
            return None
        return Path(candidate).expanduser().resolve()


def _merge_profile_backend_payload(
    payload: dict[str, Any],
    *,
    profile_id: str,
    workspace_root: Path | None,
    backend_catalog_path: Path | None,
) -> dict[str, Any]:
    resolved_payload = dict(payload)
    if not profile_id:
        return resolved_payload
    backend_payload = resolve_workspace_backend_bindings(
        profile_id=profile_id,
        workspace_root=workspace_root,
        catalog_path=backend_catalog_path,
    )
    if not backend_payload:
        return resolved_payload
    existing_backend_ids = _normalize_backend_ids(resolved_payload.get("backend_ids"))
    merged_backend_ids = dict(existing_backend_ids)
    merged_backend_ids.update(_normalize_backend_ids(backend_payload.get("backend_ids")))
    if merged_backend_ids:
        resolved_payload["backend_ids"] = merged_backend_ids
    existing_metadata = _normalize_backend_binding_metadata(
        resolved_payload.get("backend_binding_metadata")
    )
    merged_metadata = dict(existing_metadata)
    for family, metadata in _normalize_backend_binding_metadata(
        backend_payload.get("backend_binding_metadata")
    ).items():
        family_metadata = dict(merged_metadata.get(family, {}))
        family_metadata.update(metadata)
        merged_metadata[family] = family_metadata
    if merged_metadata:
        resolved_payload["backend_binding_metadata"] = merged_metadata
    return resolved_payload


def _merge_profile_provider_payload(
    payload: dict[str, Any],
    *,
    profile_id: str,
    workspace_root: Path | None,
    provider_catalog_path: Path | None,
) -> dict[str, Any]:
    resolved_payload = dict(payload)
    if not profile_id:
        return resolved_payload
    provider_payload = resolve_workspace_provider_bindings(
        profile_id=profile_id,
        workspace_root=workspace_root,
        catalog_path=provider_catalog_path,
    )
    if not provider_payload:
        return resolved_payload
    provider_id = _first_non_empty(
        provider_payload.get("provider_id"),
        resolved_payload.get("provider_id"),
    )
    if provider_id is not None:
        resolved_payload["provider_id"] = provider_id
    default_model = _first_non_empty(
        provider_payload.get("default_model"),
        resolved_payload.get("default_model"),
    )
    if default_model is not None:
        resolved_payload["default_model"] = default_model
    existing_metadata = _normalize_backend_binding_metadata(
        resolved_payload.get("provider_binding_metadata")
    )
    merged_metadata = dict(existing_metadata)
    for family, metadata in _normalize_backend_binding_metadata(
        provider_payload.get("provider_binding_metadata")
    ).items():
        family_metadata = dict(merged_metadata.get(family, {}))
        family_metadata.update(metadata)
        merged_metadata[family] = family_metadata
    if merged_metadata:
        resolved_payload["provider_binding_metadata"] = merged_metadata
    return resolved_payload


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


def _normalize_backend_binding_metadata(raw_metadata: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(raw_metadata, dict):
        return {}
    normalized: dict[str, dict[str, Any]] = {}
    for family, payload in raw_metadata.items():
        family_text = str(family).strip()
        if not family_text or not isinstance(payload, dict):
            continue
        normalized[family_text] = dict(payload)
    return normalized


@dataclass(slots=True)
class LocalRuleSourceProvider(RuleSourceProviderPort):
    """Local rule loader backed by optional workspace JSON and derived defaults."""

    default_workspace_root: Path | None = None
    catalog_path: Path | None = None

    def load_rule_bundle(
        self,
        workspace_root: str | None,
        profile_id: str | None,
    ) -> Mapping[str, Any]:
        resolved_workspace_root = (
            str(self.default_workspace_root.expanduser().resolve())
            if workspace_root is None and self.default_workspace_root is not None
            else workspace_root
        )
        project_scope_key = self._derive_project_scope_key(resolved_workspace_root)
        payload = {
            "source": "workspace-default",
            "project_scope_key": project_scope_key,
            "summary": (
                f"Workspace rules resolved for '{project_scope_key}'."
                if project_scope_key
                else "Workspace rules are unavailable."
            ),
        }
        if resolved_workspace_root is None:
            return payload
        configured_payload = self._load_workspace_rule_file(Path(resolved_workspace_root))
        if configured_payload is not None:
            payload.update(configured_payload)
            payload.setdefault("source", "workspace-config")
            payload.setdefault("project_scope_key", project_scope_key)
            payload.setdefault(
                "summary",
                f"Workspace rules loaded for '{project_scope_key or 'workspace'}'.",
            )
        if profile_id is not None:
            profile_rule_payload = self._load_profile_rule_file(
                workspace_root=Path(resolved_workspace_root),
                profile_id=profile_id,
            )
            if profile_rule_payload is not None:
                payload.update(profile_rule_payload)
                payload["source"] = "workspace-profile"
                payload.setdefault(
                    "summary",
                    f"Workspace profile rules loaded for '{profile_id}'.",
                )
        if profile_id is not None:
            payload.setdefault("profile_id", profile_id)
        payload.setdefault("workspace_root", resolved_workspace_root)
        return payload

    def _load_workspace_rule_file(self, workspace_root: Path) -> dict[str, Any] | None:
        for candidate in (
            workspace_root / ".factory" / "runtime" / "rule-bundle.json",
            workspace_root / ".factory" / "rule-bundle.json",
            workspace_root / ".factory" / "rules.json",
        ):
            if not candidate.exists():
                continue
            payload = json.loads(candidate.read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                return payload
        return None

    def _load_profile_rule_file(
        self,
        workspace_root: Path,
        profile_id: str,
    ) -> dict[str, Any] | None:
        candidate = resolve_profile_rule_bundle_path(
            workspace_root=workspace_root,
            profile_id=profile_id,
            catalog_path=self.catalog_path,
        )
        if candidate is None:
            return None
        payload = json.loads(candidate.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            return payload
        return None

    @staticmethod
    def _derive_project_scope_key(workspace_root: str | None) -> str | None:
        if workspace_root is None:
            return None
        return Path(workspace_root).expanduser().resolve().name or None
