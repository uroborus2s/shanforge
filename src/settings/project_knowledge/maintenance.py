"""Bounded maintenance for explicitly registered, disposable project caches."""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath


@dataclass(frozen=True, slots=True)
class CacheRegistration:
    cache_key: str
    relative_root: str
    ttl_seconds: int
    max_bytes: int
    current_refs: tuple[str, ...] = ()
    legal_holds: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        path = PurePosixPath(self.relative_root)
        if (
            not self.cache_key
            or path.is_absolute()
            or ".." in path.parts
            or path.as_posix() != self.relative_root
            or path.parts[:2] != (".factory", "cache")
        ):
            raise ValueError("cache registration must be a normalized .factory/cache path")
        if self.ttl_seconds < 0 or self.max_bytes < 0:
            raise ValueError("cache bounds cannot be negative")


@dataclass(frozen=True, slots=True)
class MaintenanceItem:
    cache_key: str
    relative_path: str
    realpath: str
    bytes: int
    reason: str


@dataclass(frozen=True, slots=True)
class MaintenancePlan:
    schema_id: str
    planned_at: str
    items: tuple[MaintenanceItem, ...]
    total_bytes: int


@dataclass(frozen=True, slots=True)
class MaintenanceReceipt:
    schema_id: str
    deleted_paths: tuple[str, ...]
    reclaimed_bytes: int


def _timestamp(value: datetime) -> tuple[str, float]:
    if value.tzinfo is None:
        raise ValueError("datetime must be timezone-aware")
    normalized = value.astimezone(UTC)
    return normalized.isoformat().replace("+00:00", "Z"), normalized.timestamp()


def _tree_size(path: Path) -> int:
    if path.is_file():
        return path.stat(follow_symlinks=False).st_size
    return sum(
        item.stat(follow_symlinks=False).st_size
        for item in path.rglob("*")
        if item.is_file() and not item.is_symlink()
    )


def _oldest_mtime(path: Path) -> float:
    values = [path.stat(follow_symlinks=False).st_mtime]
    values.extend(
        item.stat(follow_symlinks=False).st_mtime
        for item in path.rglob("*")
        if not item.is_symlink()
    )
    return min(values)


class ProjectKnowledgeMaintenance:
    def __init__(self, *, project_root: Path, registrations: tuple[CacheRegistration, ...]) -> None:
        self._root = project_root.resolve()
        if len({item.cache_key for item in registrations}) != len(registrations):
            raise ValueError("cache registration keys must be unique")
        self._registrations = {item.cache_key: item for item in registrations}

    def plan(self, *, now: datetime) -> MaintenancePlan:
        planned_at, now_seconds = _timestamp(now)
        items: list[MaintenanceItem] = []
        for registration in self._registrations.values():
            root = self._safe_root(registration)
            if not root.exists():
                continue
            candidates: list[tuple[Path, int, float]] = []
            for child in sorted(root.iterdir(), key=lambda value: value.name):
                if child.is_symlink():
                    raise ValueError(f"registered cache contains symlink: {child}")
                if child.stat(follow_symlinks=False).st_uid != os.getuid():
                    raise PermissionError(f"registered cache is not owned by current user: {child}")
                if (
                    child.name in registration.current_refs
                    or child.name in registration.legal_holds
                ):
                    continue
                candidates.append((child, _tree_size(child), _oldest_mtime(child)))
            total_bytes = sum(
                _tree_size(child) for child in root.iterdir() if not child.is_symlink()
            )
            selected: dict[Path, str] = {}
            for child, _, modified in candidates:
                if now_seconds - modified >= registration.ttl_seconds:
                    selected[child] = "ttl_expired"
            remaining = total_bytes - sum(
                size for child, size, _ in candidates if child in selected
            )
            for child, size, _ in sorted(candidates, key=lambda item: (item[2], item[0].name)):
                if remaining <= registration.max_bytes:
                    break
                if child not in selected:
                    selected[child] = "capacity_limit"
                    remaining -= size
            for child, size, _ in candidates:
                if child not in selected:
                    continue
                relative = child.relative_to(self._root).as_posix()
                items.append(
                    MaintenanceItem(
                        registration.cache_key,
                        relative,
                        str(child.resolve(strict=True)),
                        size,
                        selected[child],
                    )
                )
        ordered = tuple(sorted(items, key=lambda item: (item.cache_key, item.relative_path)))
        return MaintenancePlan(
            "ProjectKnowledgeMaintenancePlan/v1",
            planned_at,
            ordered,
            sum(item.bytes for item in ordered),
        )

    def apply(self, plan: MaintenancePlan, *, now: datetime) -> MaintenanceReceipt:
        del now
        deleted: list[str] = []
        reclaimed = 0
        for item in plan.items:
            registration = self._registrations.get(item.cache_key)
            if registration is None:
                raise ValueError(f"unregistered cache key: {item.cache_key}")
            root = self._safe_root(registration)
            target = self._root / item.relative_path
            if target.is_symlink() or not target.exists():
                raise ValueError(f"cache target changed since plan: {item.relative_path}")
            resolved = target.resolve(strict=True)
            if not resolved.is_relative_to(root) or str(resolved) != item.realpath:
                raise ValueError(f"cache target escaped registration: {item.relative_path}")
            if resolved.stat(follow_symlinks=False).st_uid != os.getuid():
                raise PermissionError(
                    f"cache target is not owned by current user: {item.relative_path}"
                )
            if (
                resolved.name in registration.current_refs
                or resolved.name in registration.legal_holds
            ):
                raise PermissionError(f"cache target became protected: {item.relative_path}")
            if resolved.is_dir():
                shutil.rmtree(resolved)
            else:
                resolved.unlink()
            deleted.append(item.relative_path)
            reclaimed += item.bytes
        return MaintenanceReceipt(
            "ProjectKnowledgeMaintenanceReceipt/v1", tuple(deleted), reclaimed
        )

    def _safe_root(self, registration: CacheRegistration) -> Path:
        candidate = self._root / registration.relative_root
        if candidate.is_symlink():
            raise ValueError(f"registered cache root is a symlink: {registration.relative_root}")
        if candidate.exists():
            resolved = candidate.resolve(strict=True)
            cache_root = (self._root / ".factory/cache").resolve(strict=False)
            if not resolved.is_relative_to(cache_root):
                raise ValueError(
                    f"registered cache root escapes cache: {registration.relative_root}"
                )
            return resolved
        return candidate
