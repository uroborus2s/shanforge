"""Strict file-backed source registry."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
from typing import Any

from domain.project_knowledge.models import AccessClass, SourceDefinition, stable_id


class FileSourceRegistry:
    def __init__(
        self,
        project_root: Path,
        registry_path: Path,
        *,
        discovery_cache_path: Path | None = None,
    ) -> None:
        self._root = project_root.resolve()
        self._registry_path = registry_path.resolve()
        self._cache_path: Path | None
        if not self._registry_path.is_relative_to(self._root):
            raise ValueError("source registry must be inside the project root")
        if discovery_cache_path is not None:
            resolved_cache = discovery_cache_path.resolve()
            if not resolved_cache.is_relative_to(self._root):
                raise ValueError("source discovery cache must be inside the project root")
            self._cache_path = resolved_cache
        else:
            self._cache_path = None
        self._limits: dict[str, int] = {}
        self._unchanged_hint = False
        self._pending_cache: (
            tuple[dict[str, Any], tuple[SourceDefinition, ...], set[Path]] | None
        ) = None

    def _payload(self) -> dict[str, Any]:
        payload = json.loads(self._registry_path.read_text(encoding="utf-8"))
        if payload.get("schema_id") != "ProjectKnowledgeSourceRegistry/v1":
            raise ValueError("unsupported source registry schema")
        if not isinstance(payload.get("sources"), list):
            raise ValueError("source registry sources must be a list")
        return payload

    def sources(self) -> tuple[SourceDefinition, ...]:
        payload = self._payload()
        cached = self._cached_sources(payload)
        if cached is not None:
            self._unchanged_hint = True
            return cached
        self._unchanged_hint = False
        registry_version = str(payload.get("registry_version") or "")
        concrete: dict[str, SourceDefinition] = {}
        watch_directories: set[Path] = set()
        for group in payload["sources"]:
            registry_id = str(group["registry_source_id"])
            kind = str(group["kind"])
            include = group.get("include")
            exclude = tuple(str(item) for item in group.get("exclude", []))
            roots = group.get("roots")
            if not isinstance(include, list) or not include or not isinstance(roots, list):
                raise ValueError(f"registry group {registry_id!r} requires roots and include")
            max_file_bytes = int(group["max_file_bytes"])
            for raw_root in roots:
                root_relative = PurePosixPath(str(raw_root))
                if root_relative.is_absolute() or ".." in root_relative.parts:
                    raise ValueError("registry root must remain inside the project root")
                root = (self._root / root_relative).resolve()
                if not root.is_relative_to(self._root):
                    raise ValueError("registry root must remain inside the project root")
                if not root.exists():
                    continue
                watch_directories.add(root)
                if any("**" in str(pattern) for pattern in include):
                    for directory, names, _ in os.walk(root):
                        names[:] = [
                            name
                            for name in names
                            if name not in {"__pycache__", ".git", "design-assets"}
                        ]
                        watch_directories.add(Path(directory))
                for pattern in include:
                    for candidate in root.glob(str(pattern)):
                        if not candidate.is_file():
                            continue
                        real = candidate.resolve()
                        if not real.is_relative_to(self._root):
                            raise ValueError("registered source resolves outside the project root")
                        relative = real.relative_to(self._root).as_posix()
                        if any(PurePosixPath(relative).match(item) for item in exclude):
                            continue
                        source_id = stable_id("source", [registry_id, relative])
                        definition = SourceDefinition(
                            source_id=source_id,
                            registry_source_id=registry_id,
                            kind=kind,
                            relative_path=relative,
                            extractor_id=str(group["extractor_id"]),
                            registry_version=registry_version,
                            authority_rank=int(group.get("authority_rank", 0)),
                            access_class=AccessClass(str(group["access_class"])),
                            config={
                                "stable_id_policy": str(group["stable_id_policy"]),
                                "max_file_bytes": max_file_bytes,
                            },
                        )
                        if source_id in concrete and concrete[source_id] != definition:
                            raise ValueError(f"conflicting registry definition for {relative}")
                        concrete[source_id] = definition
                        self._limits[source_id] = max_file_bytes
                        watch_directories.add(real.parent)
        result = tuple(sorted(concrete.values(), key=lambda item: item.relative_path))
        self._pending_cache = (payload, result, watch_directories)
        return result

    def unchanged_hint(self) -> bool:
        return self._unchanged_hint

    def commit_discovery(self) -> None:
        if self._pending_cache is None:
            return
        payload, sources, watch_directories = self._pending_cache
        self._write_discovery_cache(payload, sources, watch_directories)
        self._pending_cache = None

    def _cached_sources(self, payload: dict[str, Any]) -> tuple[SourceDefinition, ...] | None:
        if self._cache_path is None or not self._cache_path.is_file():
            return None
        try:
            cached = json.loads(self._cache_path.read_text(encoding="utf-8"))
            registry_sha256 = hashlib.sha256(self._registry_path.read_bytes()).hexdigest()
            if cached.get("registry_sha256") != registry_sha256:
                return None
            if cached.get("registry_version") != payload.get("registry_version"):
                return None
            for raw_directory in cached.get("directories", []):
                directory = self._root / str(raw_directory["relative_path"])
                metadata = directory.stat()
                if metadata.st_mtime_ns != int(raw_directory["mtime_ns"]):
                    return None
            definitions: list[SourceDefinition] = []
            for raw in cached.get("sources", []):
                relative_path = str(raw["relative_path"])
                path = self._root / relative_path
                metadata = path.stat()
                if metadata.st_size != int(raw["size_bytes"]) or metadata.st_mtime_ns != int(
                    raw["mtime_ns"]
                ):
                    return None
                definition = SourceDefinition(
                    source_id=str(raw["source_id"]),
                    registry_source_id=str(raw["registry_source_id"]),
                    kind=str(raw["kind"]),
                    relative_path=relative_path,
                    extractor_id=str(raw["extractor_id"]),
                    registry_version=str(raw["registry_version"]),
                    authority_rank=int(raw["authority_rank"]),
                    access_class=AccessClass(str(raw["access_class"])),
                    config=dict(raw["config"]),
                )
                definitions.append(definition)
                self._limits[definition.source_id] = int(definition.config["max_file_bytes"])
            return tuple(definitions)
        except KeyError, OSError, TypeError, ValueError, json.JSONDecodeError:
            return None

    def _write_discovery_cache(
        self,
        payload: dict[str, Any],
        sources: tuple[SourceDefinition, ...],
        watch_directories: set[Path],
    ) -> None:
        if self._cache_path is None:
            return
        cache_payload = {
            "schema_id": "ProjectKnowledgeSourceDiscoveryCache/v1",
            "registry_sha256": hashlib.sha256(self._registry_path.read_bytes()).hexdigest(),
            "registry_version": payload.get("registry_version"),
            "directories": [
                {
                    "relative_path": directory.relative_to(self._root).as_posix(),
                    "mtime_ns": directory.stat().st_mtime_ns,
                }
                for directory in sorted(watch_directories)
            ],
            "sources": [
                {
                    "source_id": source.source_id,
                    "registry_source_id": source.registry_source_id,
                    "kind": source.kind,
                    "relative_path": source.relative_path,
                    "extractor_id": source.extractor_id,
                    "registry_version": source.registry_version,
                    "authority_rank": source.authority_rank,
                    "access_class": source.access_class.value,
                    "config": dict(source.config),
                    "size_bytes": (self._root / source.relative_path).stat().st_size,
                    "mtime_ns": (self._root / source.relative_path).stat().st_mtime_ns,
                }
                for source in sources
            ],
        }
        self._cache_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self._cache_path.with_suffix(self._cache_path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(cache_payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True),
            encoding="utf-8",
        )
        os.replace(temporary, self._cache_path)

    def read_bytes(self, source: SourceDefinition) -> bytes:
        path = (self._root / source.relative_path).resolve()
        if not path.is_relative_to(self._root) or not path.is_file():
            raise ValueError("registered source is no longer a safe project file")
        maximum = self._limits.get(source.source_id)
        if maximum is None:
            maximum = int(source.config["max_file_bytes"])
        size = path.stat().st_size
        if size > maximum:
            raise ValueError(f"registered source exceeds max_file_bytes: {source.relative_path}")
        return path.read_bytes()

    def stat(self, source: SourceDefinition) -> tuple[int, int]:
        stat = (self._root / source.relative_path).stat()
        return stat.st_size, stat.st_mtime_ns
