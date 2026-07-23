"""Strict repository-backed loader for design, API, and test artifacts."""

from __future__ import annotations

import json
from collections.abc import Mapping, Set
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

_MAX_ARTIFACT_BYTES = 4 * 1024 * 1024


class LocalProjectArtifactRepository:
    def __init__(self, project_root: Path) -> None:
        self._root = project_root.resolve()

    def _path(self, relative_path: str) -> Path:
        pure = PurePosixPath(relative_path)
        if pure.is_absolute() or ".." in pure.parts:
            raise ValueError("artifact path must remain inside the project root")
        unresolved = self._root / pure
        candidate = unresolved
        while candidate != self._root:
            if candidate.is_symlink():
                raise ValueError(f"artifact source must not be a symlink: {relative_path}")
            candidate = candidate.parent
        path = unresolved.resolve()
        if not path.is_relative_to(self._root):
            raise ValueError("artifact path must remain inside the project root")
        return path

    def _read_mapping(self, relative_path: str) -> Mapping[str, Any]:
        path = self._path(relative_path)
        if not path.is_file():
            raise ValueError(f"required project artifact is missing: {relative_path}")
        if path.stat().st_size > _MAX_ARTIFACT_BYTES:
            raise ValueError(f"project artifact exceeds size limit: {relative_path}")
        if path.suffix.casefold() == ".json":
            payload = json.loads(path.read_text(encoding="utf-8"))
        else:
            payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(payload, Mapping):
            raise ValueError(f"project artifact root must be an object: {relative_path}")
        return payload

    def design_manifest(self) -> Mapping[str, Any]:
        return self._read_mapping("design/ux-ui/design-manifest.yaml")

    def design_tokens(self, relative_path: str) -> Mapping[str, Any]:
        return self._read_mapping(relative_path)

    def openapi_contract(self) -> Mapping[str, Any]:
        return self._read_mapping("contracts/openapi/openapi.yaml")

    def test_case_catalogs(self) -> tuple[Mapping[str, Any], ...]:
        root = self._path("tests/specifications")
        if not root.is_dir():
            raise ValueError("required project artifact directory is missing: tests/specifications")
        paths = sorted(
            path
            for pattern in ("*.testcases.yaml", "*.testcases.yml")
            for path in root.glob(pattern)
            if path.is_file() and not path.is_symlink()
        )
        if not paths:
            raise ValueError("no test case catalogs were found")
        return tuple(self._read_mapping(path.relative_to(self._root).as_posix()) for path in paths)

    def available_design_paths(self) -> Set[str]:
        root = self._path("design/ux-ui")
        if not root.is_dir():
            return frozenset()
        return frozenset(
            path.relative_to(self._root).as_posix()
            for path in root.rglob("*")
            if path.is_file() and not path.is_symlink()
        )
