from __future__ import annotations

from typing import Any, Mapping, Protocol


class FileSystemProviderPort(Protocol):
    """Settings-provider contract owned by the basic capability layer for file access."""

    def read_text(self, path: str) -> str: ...

    def write_text(self, path: str, content: str) -> None: ...

    def exists(self, path: str) -> bool: ...

    def list_dir(self, path: str) -> tuple[str, ...]: ...


class StructuredStoreProviderPort(Protocol):
    """Settings-provider contract owned by the basic capability layer for structured records."""

    def put_record(
        self,
        namespace: str,
        record_id: str,
        payload: Mapping[str, Any],
    ) -> None: ...

    def get_record(self, namespace: str, record_id: str) -> Mapping[str, Any] | None: ...

    def query_records(
        self,
        namespace: str,
        filters: Mapping[str, Any] | None = None,
        limit: int = 100,
    ) -> tuple[Mapping[str, Any], ...]: ...


class BlobStoreProviderPort(Protocol):
    """Settings-provider contract owned by the basic capability layer for binary payloads."""

    def put_blob(self, namespace: str, blob_id: str, payload: bytes) -> None: ...

    def get_blob(self, namespace: str, blob_id: str) -> bytes | None: ...


class SearchIndexProviderPort(Protocol):
    """Settings-provider contract owned by the basic capability layer for search indexes."""

    def search(
        self,
        namespace: str,
        query_text: str,
        limit: int = 20,
        filters: Mapping[str, Any] | None = None,
    ) -> tuple[Mapping[str, Any], ...]: ...


class VectorIndexProviderPort(Protocol):
    """Settings-provider contract owned by the basic capability layer for vector indexes."""

    def query(
        self,
        namespace: str,
        vector: tuple[float, ...],
        limit: int = 20,
        filters: Mapping[str, Any] | None = None,
    ) -> tuple[Mapping[str, Any], ...]: ...
