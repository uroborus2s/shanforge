from __future__ import annotations

from typing import Protocol

from domain.session.models import SessionArtifact


class ArtifactStorePort(Protocol):
    """Application-owned persistence contract for session artifacts."""

    def save(self, artifact: SessionArtifact) -> None: ...
