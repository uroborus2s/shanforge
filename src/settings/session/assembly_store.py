from __future__ import annotations

import copy
from dataclasses import dataclass, field
from pathlib import Path

from domain.session.assembly_models import SessionAssemblyManifest
from settings.shared.jsonl import JsonlStore


def _deserialize_manifest(payload: dict[str, object]) -> SessionAssemblyManifest:
    normalized = dict(payload)
    normalized.pop("id", None)
    return SessionAssemblyManifest.from_mapping(normalized)


@dataclass(slots=True)
class InMemorySessionAssemblyStore:
    """Simple in-memory persistence for session assembly manifests."""

    manifests: dict[str, SessionAssemblyManifest] = field(default_factory=dict)

    def save(self, manifest: SessionAssemblyManifest) -> None:
        self.manifests[manifest.session_id] = copy.deepcopy(manifest)

    def get(self, session_id: str) -> SessionAssemblyManifest | None:
        manifest = self.manifests.get(session_id)
        return copy.deepcopy(manifest) if manifest is not None else None


class JsonlSessionAssemblyStore(JsonlStore):
    """JSONL-backed persistence for session assembly manifests."""

    def __init__(self, root: str | Path) -> None:
        super().__init__(root=root, filename="session-assemblies.jsonl")

    def save(self, manifest: SessionAssemblyManifest) -> None:
        payload = {"id": manifest.session_id, **manifest.to_mapping()}
        self.replace_or_append(manifest.session_id, payload)

    def get(self, session_id: str) -> SessionAssemblyManifest | None:
        for manifest in self.read_all(_deserialize_manifest):
            if manifest.session_id == session_id:
                return manifest
        return None
