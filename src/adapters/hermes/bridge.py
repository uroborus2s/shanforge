from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class HermesBridgeConfig:
    """Filesystem-based bridge configuration for the local hermes-agent checkout."""

    repo_root: Path

    @classmethod
    def from_repo_root(cls, repo_root: str | Path) -> "HermesBridgeConfig":
        return cls(repo_root=Path(repo_root).expanduser().resolve())

    def module_path(self, relative_path: str) -> Path:
        return self.repo_root / relative_path

    def has_module(self, relative_path: str) -> bool:
        return self.module_path(relative_path).is_file()

    def has_modules(self, *relative_paths: str) -> bool:
        return all(self.has_module(path) for path in relative_paths)
