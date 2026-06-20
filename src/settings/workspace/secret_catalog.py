from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class DurableSecretSelection:
    """One resolved secret selection from a durable secret catalog."""

    secret_id: str | None = None
    selection_source: str | None = None
    payload: Mapping[str, Any] = field(default_factory=dict)

    def get(self, key: str) -> Any:
        return self.payload.get(key)


@dataclass(slots=True)
class LocalSecretCatalogProvider:
    """Loads and resolves durable secret catalogs from workspace-backed metadata."""

    def load_catalog(self, metadata: Mapping[str, Any]) -> tuple[dict[str, Any], str | None]:
        catalog_file = str(metadata.get("secret_catalog_file") or "").strip()
        if not catalog_file:
            return {}, None
        resolved_path = self._resolve_secret_catalog_path(catalog_file, metadata=metadata)
        if not resolved_path.exists():
            raise FileNotFoundError(f"Secret catalog file not found: {resolved_path}")
        payload = json.loads(resolved_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("secret_catalog_file must point to a JSON object")
        return (
            self._resolve_secret_catalog_paths(dict(payload), base_path=resolved_path.parent),
            str(resolved_path),
        )

    def resolve_secret_selection(
        self,
        *,
        secret_catalog: Mapping[str, Any],
        metadata: Mapping[str, Any],
        secret_family: str,
        requested_id_key: str,
        fallback_id_key: str,
        default_id_key: str,
        source_path: str | None,
    ) -> DurableSecretSelection:
        secret_id, selection_source = self._resolve_secret_selection_id(
            secret_catalog,
            metadata=metadata,
            requested_id_key=requested_id_key,
            fallback_id_key=fallback_id_key,
            default_id_key=default_id_key,
        )
        if secret_id is None:
            return DurableSecretSelection()
        entries = secret_catalog.get(secret_family)
        if not isinstance(entries, Mapping):
            return DurableSecretSelection(
                secret_id=secret_id,
                selection_source=selection_source,
            )
        entry = entries.get(secret_id)
        if not isinstance(entry, Mapping):
            raise ValueError(
                f"{secret_family} secret id '{secret_id}' was not found in "
                f"{source_path or 'catalog'}"
            )
        return DurableSecretSelection(
            secret_id=secret_id,
            selection_source=selection_source,
            payload=dict(entry),
        )

    def _resolve_secret_catalog_paths(
        self,
        payload: object,
        *,
        base_path: Path,
    ) -> object:
        if isinstance(payload, dict):
            resolved: dict[str, Any] = {}
            for key, value in payload.items():
                key_text = str(key).strip()
                if key_text.endswith("_file") and value not in {None, ""}:
                    resolved[key_text] = str(
                        self._resolve_catalog_relative_path(str(value), base_path=base_path)
                    )
                    continue
                resolved[key_text] = self._resolve_secret_catalog_paths(
                    value,
                    base_path=base_path,
                )
            return resolved
        if isinstance(payload, list):
            return [
                self._resolve_secret_catalog_paths(item, base_path=base_path)
                for item in payload
            ]
        return payload

    @staticmethod
    def _resolve_catalog_relative_path(raw_path: str, *, base_path: Path) -> Path:
        candidate = Path(raw_path).expanduser()
        if candidate.is_absolute():
            return candidate.resolve()
        return (base_path / candidate).resolve()

    @staticmethod
    def _resolve_secret_catalog_path(
        raw_path: str,
        *,
        metadata: Mapping[str, Any],
    ) -> Path:
        candidate = Path(raw_path).expanduser()
        if candidate.is_absolute():
            return candidate.resolve()
        source_path = str(
            metadata.get("metadata_source_path") or metadata.get("source_path") or ""
        ).strip()
        if not source_path:
            return candidate.resolve()
        return (Path(source_path).expanduser().resolve().parent / candidate).resolve()

    @staticmethod
    def _resolve_secret_selection_id(
        secret_catalog: Mapping[str, Any],
        *,
        metadata: Mapping[str, Any],
        requested_id_key: str,
        fallback_id_key: str,
        default_id_key: str,
    ) -> tuple[str | None, str | None]:
        requested_id = str(metadata.get(requested_id_key) or "").strip()
        if requested_id:
            return requested_id, f"metadata:{requested_id_key}"
        fallback_id = str(metadata.get(fallback_id_key) or "").strip()
        if fallback_id:
            return fallback_id, f"metadata:{fallback_id_key}"
        default_id = str(secret_catalog.get(default_id_key) or "").strip()
        if default_id:
            return default_id, f"catalog:{default_id_key}"
        return None, None
