from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class InMemoryBlobStore:
    """Simple in-memory blob store reserved for future artifact payload backends."""

    blobs: dict[str, dict[str, bytes]] = field(default_factory=dict)

    def put_blob(self, namespace: str, blob_id: str, payload: bytes) -> None:
        namespace_bucket = self.blobs.setdefault(namespace, {})
        namespace_bucket[blob_id] = bytes(payload)

    def get_blob(self, namespace: str, blob_id: str) -> bytes | None:
        namespace_bucket = self.blobs.get(namespace, {})
        payload = namespace_bucket.get(blob_id)
        return None if payload is None else bytes(payload)
