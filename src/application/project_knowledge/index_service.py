"""Incremental indexing use case."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Protocol

from domain.project_knowledge.models import SourceDefinition, canonical_json


class SourceRegistryPort(Protocol):
    def sources(self) -> tuple[SourceDefinition, ...]: ...

    def unchanged_hint(self) -> bool: ...

    def commit_discovery(self) -> None: ...

    def stat(self, source: SourceDefinition) -> tuple[int, int]: ...

    def read_bytes(self, source: SourceDefinition) -> bytes: ...


class KnowledgeIndexPort(Protocol):
    def source_contributions(self) -> dict[str, dict[str, Any]]: ...

    def current_generation_id(self) -> str | None: ...

    def current_generation(self) -> dict[str, str] | None: ...

    def update_source_stats(self, stats: Mapping[str, tuple[int, int]]) -> None: ...

    def publish(
        self,
        *,
        sources: tuple[SourceDefinition, ...],
        contributions: Mapping[str, dict[str, Any]],
        content_hashes: Mapping[str, str],
        stats: Mapping[str, tuple[int, int]],
        as_of: str,
        git_commit: str | None,
        contribution_jsons: Mapping[str, str] | None = None,
        contribution_hashes: Mapping[str, str] | None = None,
        changed_source_ids: frozenset[str] | None = None,
        previous_changed_contributions: Mapping[str, dict[str, Any]] | None = None,
    ) -> dict[str, str]: ...


class ExtractorPort(Protocol):
    def extract(self, source: SourceDefinition, content: bytes) -> dict[str, Any]: ...


@dataclass(frozen=True, slots=True)
class RefreshReport:
    generation_id: str
    source_root_sha256: str
    source_count: int
    parsed_count: int
    reused_count: int
    deleted_count: int
    changed: bool


class ProjectKnowledgeIndexService:
    def __init__(
        self,
        registry: SourceRegistryPort,
        index: KnowledgeIndexPort,
        extractors: ExtractorPort,
    ) -> None:
        self._registry = registry
        self._index = index
        self._extractors = extractors

    def refresh(self, *, as_of: str, git_commit: str | None = None) -> RefreshReport:
        sources = self._registry.sources()
        current = self._index.current_generation()
        if (
            self._registry.unchanged_hint()
            and current is not None
            and current.get("git_commit") == (git_commit or "")
        ):
            return RefreshReport(
                generation_id=current["generation_id"],
                source_root_sha256=current["source_root_sha256"],
                source_count=len(sources),
                parsed_count=0,
                reused_count=len(sources),
                deleted_count=0,
                changed=False,
            )
        previous = self._index.source_contributions()
        contributions: dict[str, dict[str, Any]] = {}
        contribution_jsons: dict[str, str] = {}
        contribution_hashes: dict[str, str] = {}
        changed_source_ids: set[str] = set()
        previous_changed_contributions: dict[str, dict[str, Any]] = {}
        content_hashes: dict[str, str] = {}
        stats: dict[str, tuple[int, int]] = {}
        changed_stats: dict[str, tuple[int, int]] = {}
        parsed_count = 0
        reused_count = 0
        for source in sources:
            size_bytes, mtime_ns = self._registry.stat(source)
            stats[source.source_id] = (size_bytes, mtime_ns)
            old = previous.get(source.source_id)
            if old is None or old["size_bytes"] != size_bytes or old["mtime_ns"] != mtime_ns:
                changed_stats[source.source_id] = (size_bytes, mtime_ns)
            if (
                old is not None
                and old["size_bytes"] == size_bytes
                and old["mtime_ns"] == mtime_ns
                and old["extractor_id"] == source.extractor_id
                and old["registry_version"] == source.registry_version
            ):
                contributions[source.source_id] = old["contribution"]
                contribution_jsons[source.source_id] = str(old["contribution_json"])
                contribution_hashes[source.source_id] = str(old["contribution_sha256"])
                content_hashes[source.source_id] = str(old["content_sha256"])
                reused_count += 1
                continue
            content = self._registry.read_bytes(source)
            content_sha256 = hashlib.sha256(content).hexdigest()
            content_hashes[source.source_id] = content_sha256
            if (
                old is not None
                and old["content_sha256"] == content_sha256
                and old["extractor_id"] == source.extractor_id
                and old["registry_version"] == source.registry_version
            ):
                contributions[source.source_id] = old["contribution"]
                contribution_jsons[source.source_id] = str(old["contribution_json"])
                contribution_hashes[source.source_id] = str(old["contribution_sha256"])
                reused_count += 1
            else:
                contribution = self._extractors.extract(source, content)
                serialized = canonical_json(contribution)
                contributions[source.source_id] = contribution
                contribution_jsons[source.source_id] = serialized
                contribution_hashes[source.source_id] = hashlib.sha256(
                    serialized.encode("utf-8")
                ).hexdigest()
                changed_source_ids.add(source.source_id)
                if old is not None:
                    previous_changed_contributions[source.source_id] = dict(old["contribution"])
                parsed_count += 1
        deleted_count = len(set(previous) - set(contributions))
        if parsed_count == 0 and deleted_count == 0:
            current = self._index.current_generation()
            if current is not None and current.get("git_commit") == (git_commit or ""):
                if changed_stats:
                    self._index.update_source_stats(changed_stats)
                self._registry.commit_discovery()
                return RefreshReport(
                    generation_id=current["generation_id"],
                    source_root_sha256=current["source_root_sha256"],
                    source_count=len(sources),
                    parsed_count=0,
                    reused_count=reused_count,
                    deleted_count=0,
                    changed=False,
                )
        publication = self._index.publish(
            sources=sources,
            contributions=contributions,
            contribution_jsons=contribution_jsons,
            contribution_hashes=contribution_hashes,
            changed_source_ids=frozenset(changed_source_ids),
            previous_changed_contributions=previous_changed_contributions,
            content_hashes=content_hashes,
            stats=stats,
            as_of=as_of,
            git_commit=git_commit,
        )
        self._registry.commit_discovery()
        return RefreshReport(
            generation_id=publication["generation_id"],
            source_root_sha256=publication["source_root_sha256"],
            source_count=len(sources),
            parsed_count=parsed_count,
            reused_count=reused_count,
            deleted_count=deleted_count,
            changed=True,
        )
