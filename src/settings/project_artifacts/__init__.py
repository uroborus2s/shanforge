"""Settings implementations for project artifact sources."""

from settings.project_artifacts.local_repository import LocalProjectArtifactRepository
from settings.project_artifacts.source_registry import ProjectArtifactSourceRegistry

__all__ = ["LocalProjectArtifactRepository", "ProjectArtifactSourceRegistry"]
