from __future__ import annotations

import copy
from dataclasses import dataclass, field

from domain.session.models import SessionArtifact


@dataclass(slots=True)
class InMemoryArtifactStore:
    """Simple in-memory artifact store for scaffold and tests."""

    artifacts: list[SessionArtifact] = field(default_factory=list)
    session_artifact_ids: dict[str, list[str]] = field(default_factory=dict)

    def save(self, artifact: SessionArtifact) -> None:
        self._upsert_artifact(artifact)

    def save_artifact(self, session_id: str, artifact: SessionArtifact) -> None:
        self._upsert_artifact(artifact)
        artifact_ids = self.session_artifact_ids.setdefault(session_id, [])
        if artifact.id not in artifact_ids:
            artifact_ids.append(artifact.id)

    def load_artifact(self, artifact_id: str) -> SessionArtifact | None:
        for artifact in self.artifacts:
            if artifact.id == artifact_id:
                return copy.deepcopy(artifact)
        return None

    def list_artifacts(self, session_id: str) -> tuple[SessionArtifact, ...]:
        artifact_ids = set(self.session_artifact_ids.get(session_id, ()))
        return tuple(
            copy.deepcopy(artifact)
            for artifact in self.artifacts
            if artifact.id in artifact_ids
        )

    def _upsert_artifact(self, artifact: SessionArtifact) -> None:
        for index, existing in enumerate(self.artifacts):
            if existing.id == artifact.id:
                self.artifacts[index] = copy.deepcopy(artifact)
                break
        else:
            self.artifacts.append(copy.deepcopy(artifact))
