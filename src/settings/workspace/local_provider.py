from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from runtime.ports.data_access import FileSystemProviderPort
from runtime.ports.execution_backends import WorkspaceProviderPort

_BLOCKED_DEVICE_PATHS = frozenset(
    {
        "/dev/zero",
        "/dev/random",
        "/dev/urandom",
        "/dev/full",
        "/dev/stdin",
        "/dev/stdout",
        "/dev/stderr",
        "/dev/tty",
        "/dev/console",
        "/dev/fd/0",
        "/dev/fd/1",
        "/dev/fd/2",
    }
)


def _has_traversal_component(path_str: str) -> bool:
    return ".." in Path(path_str).parts


def _validate_within_dir(path: Path, root: Path) -> str | None:
    try:
        path.resolve().relative_to(root.resolve())
    except (ValueError, OSError) as exc:
        return f"Path escapes allowed directory: {exc}"
    return None


@dataclass(slots=True)
class LocalWorkspaceProvider(FileSystemProviderPort, WorkspaceProviderPort):
    """Local workspace-backed implementation for file and workspace access."""

    workspace_root: Path

    def __post_init__(self) -> None:
        self.workspace_root = self.workspace_root.expanduser().resolve()

    def resolve_root(self) -> str:
        return str(self.workspace_root)

    def read_text(self, path: str) -> str:
        resolved = self._resolve_path(path, allow_missing=False)
        if resolved.is_dir():
            raise IsADirectoryError(str(resolved))
        if self._is_blocked_device(resolved):
            raise ValueError(f"Blocked device path: {path}")

        return resolved.read_text(encoding="utf-8")

    def write_text(self, path: str, content: str) -> None:
        resolved = self._resolve_path(path, allow_missing=True)
        resolved.parent.mkdir(parents=True, exist_ok=True)
        resolved.write_text(content, encoding="utf-8")

    def exists(self, path: str) -> bool:
        try:
            resolved = self._resolve_path(path, allow_missing=True)
        except ValueError:
            return False
        return resolved.exists()

    def list_dir(self, path: str) -> tuple[str, ...]:
        resolved = self._resolve_path(path or ".", allow_missing=False)
        if not resolved.exists():
            return ()
        if not resolved.is_dir():
            return (self._relative_display_path(resolved),)

        return tuple(
            sorted(self._relative_display_path(item) for item in resolved.iterdir())
        )

    def list_paths(self, root: str, pattern: str | None = None) -> tuple[str, ...]:
        resolved_root = self._resolve_path(root or ".", allow_missing=False)
        if not resolved_root.exists():
            return ()

        glob_pattern = pattern or "**/*"
        if resolved_root.is_file():
            return (self._relative_display_path(resolved_root),)

        matches = []
        for match in resolved_root.glob(glob_pattern):
            if match == resolved_root:
                continue
            matches.append(self._relative_display_path(match))

        return tuple(sorted(dict.fromkeys(matches)))

    def absolute_path(self, path: str) -> str:
        return str(self._resolve_path(path, allow_missing=True))

    def is_dir(self, path: str) -> bool:
        return self._resolve_path(path, allow_missing=True).is_dir()

    def _resolve_path(self, path: str, allow_missing: bool) -> Path:
        raw_path = Path(path).expanduser()
        candidate = raw_path if raw_path.is_absolute() else self.workspace_root / raw_path
        if _has_traversal_component(path):
            raise ValueError(f"Path traversal is not allowed: {path}")
        error = _validate_within_dir(candidate, self.workspace_root)
        if error is not None:
            raise ValueError(error)
        resolved = candidate.resolve(strict=False)
        if not allow_missing and not resolved.exists():
            raise FileNotFoundError(str(resolved))
        return resolved

    def _relative_display_path(self, path: Path) -> str:
        try:
            return str(path.resolve().relative_to(self.workspace_root))
        except ValueError:
            return str(path.resolve())

    def _is_blocked_device(self, path: Path) -> bool:
        normalized = str(path)
        if normalized in _BLOCKED_DEVICE_PATHS:
            return True
        return normalized.startswith("/proc/") and normalized.endswith(("/fd/0", "/fd/1", "/fd/2"))
