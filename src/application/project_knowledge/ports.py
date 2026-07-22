"""Application-owned ports for deterministic project knowledge."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Protocol

from domain.project_knowledge.models import SourceDefinition


class SourceRegistryPort(Protocol):
    def sources(self) -> tuple[SourceDefinition, ...]: ...


class KnowledgeIndexPort(Protocol):
    def current_generation_id(self) -> str | None: ...

    def replace_generation(
        self,
        generation_id: str,
        contributions: Mapping[str, object],
    ) -> None: ...

    def search(self, query: str, *, limit: int) -> tuple[Mapping[str, object], ...]: ...


class SourceContentPort(Protocol):
    def read_bytes(self, relative_path: str) -> bytes: ...

    def expand(self, pattern: str) -> tuple[str, ...]: ...


class KnowledgeExtractorPort(Protocol):
    def supports(self, source: SourceDefinition) -> bool: ...

    def extract(self, source: SourceDefinition, content: bytes) -> Mapping[str, object]: ...


class SitePublisherPort(Protocol):
    def publish(self, build_id: str, pages: Mapping[str, str]) -> Path: ...


class ProjectStateSyncQueuePort(Protocol):
    def enqueue(self, *, head: int, scope: str, request_key: str) -> str: ...

    def claim(self, *, worker_id: str, lease_seconds: int) -> Mapping[str, object] | None: ...

    def complete(self, request_id: str, *, worker_id: str, fencing_token: int) -> None: ...


class MaintenancePort(Protocol):
    def plan(self, *, now: str) -> Mapping[str, object]: ...

    def execute(self, cache_keys: Iterable[str]) -> Mapping[str, object]: ...
