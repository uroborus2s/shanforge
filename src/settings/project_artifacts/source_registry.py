"""Composite source registry for human documents and typed machine artifacts."""

from __future__ import annotations

from pathlib import Path

from domain.project_knowledge.models import SourceDefinition
from settings.project_knowledge.source_registry import FileSourceRegistry


class ProjectArtifactSourceRegistry:
    """Merge two strict registries while preserving their independent caches."""

    def __init__(
        self,
        project_root: Path,
        base_registry_path: Path,
        artifact_registry_path: Path,
        *,
        base_discovery_cache_path: Path | None = None,
        artifact_discovery_cache_path: Path | None = None,
    ) -> None:
        self._registries = (
            FileSourceRegistry(
                project_root,
                base_registry_path,
                discovery_cache_path=base_discovery_cache_path,
            ),
            FileSourceRegistry(
                project_root,
                artifact_registry_path,
                discovery_cache_path=artifact_discovery_cache_path,
            ),
        )
        self._owners: dict[str, tuple[FileSourceRegistry, SourceDefinition]] = {}
        self._unchanged_hint = False

    def sources(self) -> tuple[SourceDefinition, ...]:
        sources: dict[str, SourceDefinition] = {}
        owners: dict[str, tuple[FileSourceRegistry, SourceDefinition]] = {}
        unchanged = True
        for registry in self._registries:
            for source in registry.sources():
                existing = sources.get(source.source_id)
                if existing is not None and existing != source:
                    raise ValueError(f"conflicting composite source definition: {source.source_id}")
                sources[source.source_id] = source
                owners[source.source_id] = (registry, source)
            unchanged = unchanged and registry.unchanged_hint()
        self._owners = owners
        self._unchanged_hint = unchanged
        return tuple(
            sorted(
                sources.values(),
                key=lambda item: (item.relative_path, item.registry_source_id),
            )
        )

    def unchanged_hint(self) -> bool:
        return self._unchanged_hint

    def commit_discovery(self) -> None:
        for registry in self._registries:
            registry.commit_discovery()

    def read_bytes(self, source: SourceDefinition) -> bytes:
        return self._owner(source).read_bytes(source)

    def stat(self, source: SourceDefinition) -> tuple[int, int]:
        return self._owner(source).stat(source)

    def _owner(self, source: SourceDefinition) -> FileSourceRegistry:
        registered = self._owners.get(source.source_id)
        if registered is None:
            raise ValueError(f"source is not owned by the composite registry: {source.source_id}")
        owner, expected = registered
        if source != expected:
            raise ValueError(
                f"source definition does not match the registered definition: {source.source_id}"
            )
        return owner
