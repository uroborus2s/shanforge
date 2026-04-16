from __future__ import annotations

import json
import mimetypes
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from runtime.capability.contracts import (
    CapabilityInvocationContext,
    CapabilityOperationDescriptor,
    CapabilityPackageDescriptor,
    CapabilityProviderDependency,
)
from runtime.file_access.models import FileReadResult, FileWritePlan, PathMatch, WorkspaceSnapshot
from runtime.ports.data_access import FileSystemProviderPort
from runtime.ports.execution_backends import WorkspaceProviderPort


@dataclass(slots=True)
class FileAccessService:
    """Self-owned scaffold for the file and workspace capability package."""

    file_provider: FileSystemProviderPort | None = None
    workspace_provider: WorkspaceProviderPort | None = None

    def describe_package(self) -> CapabilityPackageDescriptor:
        return CapabilityPackageDescriptor(
            package_id="file_access",
            name="File Access",
            summary="Reads workspace files, lists paths, and plans governed writes.",
            operations=(
                CapabilityOperationDescriptor(
                    operation_id="file.read_text",
                    method_name="read_text",
                    summary="Read one text file.",
                ),
                CapabilityOperationDescriptor(
                    operation_id="file.read_structured",
                    method_name="read_structured",
                    summary="Read one structured file resource.",
                ),
                CapabilityOperationDescriptor(
                    operation_id="file.list_paths",
                    method_name="list_paths",
                    summary="List paths under one workspace root.",
                ),
                CapabilityOperationDescriptor(
                    operation_id="file.search_paths",
                    method_name="search_paths",
                    summary="Search workspace paths by pattern.",
                ),
                CapabilityOperationDescriptor(
                    operation_id="file.plan_write",
                    method_name="plan_write",
                    summary="Plan a governed file mutation.",
                    risk_level="L1",
                    writes_data=True,
                ),
                CapabilityOperationDescriptor(
                    operation_id="file.apply_write",
                    method_name="apply_write",
                    summary="Apply one governed file mutation.",
                    risk_level="L2",
                    writes_data=True,
                ),
            ),
            provider_dependencies=(
                CapabilityProviderDependency("file_system", required=False),
                CapabilityProviderDependency("workspace", required=False),
            ),
        )

    def read_text(
        self,
        path: str,
        context: CapabilityInvocationContext,
    ) -> FileReadResult:
        provider = self._require_file_provider()
        resolved_path = self._resolve_path(path, context)
        if not provider.exists(resolved_path):
            return FileReadResult(
                path=path,
                content="",
                exists=False,
                metadata={"absolute_path": resolved_path},
            )

        content = provider.read_text(resolved_path)
        media_type, _ = mimetypes.guess_type(path)
        return FileReadResult(
            path=path,
            content=content,
            exists=True,
            media_type=media_type or "text/plain",
            metadata={
                "absolute_path": resolved_path,
                "workspace_root": self._resolve_workspace_root(context),
                "bytes": len(content.encode("utf-8")),
            },
        )

    def read_structured(
        self,
        path: str,
        format_name: str,
        context: CapabilityInvocationContext,
    ) -> FileReadResult:
        read_result = self.read_text(path, context)
        if not read_result.exists:
            return read_result

        normalized_format = format_name.strip().lower()
        parsed_payload = self._parse_structured(
            read_result.content,
            normalized_format,
            path,
        )
        metadata = dict(read_result.metadata)
        metadata["format"] = normalized_format
        metadata["parsed"] = parsed_payload
        return FileReadResult(
            path=read_result.path,
            content=read_result.content,
            exists=read_result.exists,
            media_type=_structured_media_type(normalized_format),
            metadata=metadata,
        )

    def list_paths(
        self,
        root: str | None,
        pattern: str | None,
        context: CapabilityInvocationContext,
    ) -> WorkspaceSnapshot:
        provider = self._require_workspace_provider()
        effective_root = root or "."
        matches = tuple(
            PathMatch(
                path=match,
                is_dir=self._is_dir(match, context),
            )
            for match in provider.list_paths(effective_root, pattern)
        )
        return WorkspaceSnapshot(
            root=self._resolve_workspace_root(context),
            cwd=context.cwd,
            matches=matches,
            metadata={
                "scope_root": effective_root,
                "pattern": pattern,
                "match_count": len(matches),
            },
        )

    def search_paths(
        self,
        pattern: str,
        scope: str | None,
        context: CapabilityInvocationContext,
    ) -> WorkspaceSnapshot:
        return self.list_paths(root=scope, pattern=pattern, context=context)

    def plan_write(
        self,
        path: str,
        content: str,
        mode: str,
        context: CapabilityInvocationContext,
    ) -> FileWritePlan:
        provider = self._require_file_provider()
        resolved_path = self._resolve_path(path, context)
        existing = provider.exists(resolved_path)
        normalized_mode = (mode or "overwrite").strip().lower()
        if normalized_mode not in {"overwrite", "create", "append"}:
            raise ValueError(f"Unsupported file mutation mode: {normalized_mode}")
        requires_approval = normalized_mode in {"append", "patch", "delete"} or (
            context.risk_level in {"L2", "L3"}
        )
        return FileWritePlan(
            path=path,
            content=content,
            mode=normalized_mode,
            reason="governed file mutation",
            requires_approval=requires_approval,
            metadata={
                "absolute_path": resolved_path,
                "existing": existing,
                "workspace_root": self._resolve_workspace_root(context),
                "bytes": len(content.encode("utf-8")),
            },
        )

    def apply_write(
        self,
        plan: FileWritePlan,
        context: CapabilityInvocationContext,
    ) -> FileReadResult:
        provider = self._require_file_provider()
        normalized_mode = plan.mode.strip().lower()
        if normalized_mode not in {"overwrite", "create", "append"}:
            raise ValueError(f"Unsupported file mutation mode: {normalized_mode}")
        if context.sandbox_decision == "denied":
            raise PermissionError("Sandbox denied the file mutation request.")
        if plan.requires_approval and not context.approval_ref:
            raise PermissionError("Approval is required before applying this file mutation.")

        resolved_path = self._resolve_path(plan.path, context)
        existing_text = provider.read_text(resolved_path) if provider.exists(resolved_path) else ""
        if normalized_mode == "create" and provider.exists(resolved_path):
            raise FileExistsError(f"File already exists: {plan.path}")
        if normalized_mode == "append":
            final_content = existing_text + plan.content
        else:
            final_content = plan.content

        provider.write_text(resolved_path, final_content)
        return FileReadResult(
            path=plan.path,
            content=final_content,
            exists=True,
            media_type=mimetypes.guess_type(plan.path)[0] or "text/plain",
            metadata={
                **plan.metadata,
                "absolute_path": resolved_path,
                "applied_mode": normalized_mode,
            },
        )

    def _require_file_provider(self) -> FileSystemProviderPort:
        if self.file_provider is None:
            raise RuntimeError("File provider is not configured.")
        return self.file_provider

    def _require_workspace_provider(self) -> WorkspaceProviderPort:
        if self.workspace_provider is None:
            raise RuntimeError("Workspace provider is not configured.")
        return self.workspace_provider

    def _resolve_workspace_root(self, context: CapabilityInvocationContext) -> str:
        if context.workspace_root:
            return context.workspace_root
        return self._require_workspace_provider().resolve_root()

    def _resolve_path(
        self,
        path: str,
        context: CapabilityInvocationContext,
    ) -> str:
        workspace_root = Path(self._resolve_workspace_root(context)).resolve()
        raw_path = Path(path).expanduser()
        candidate = raw_path if raw_path.is_absolute() else workspace_root / raw_path
        resolved = candidate.resolve(strict=False)
        try:
            resolved.relative_to(workspace_root)
        except ValueError as exc:
            raise ValueError(f"Path escapes workspace root: {path}") from exc
        return str(resolved)

    def _is_dir(self, path: str, context: CapabilityInvocationContext) -> bool:
        raw_path = Path(path)
        if raw_path.is_absolute():
            resolved = raw_path
        else:
            resolved = Path(self._resolve_workspace_root(context)) / raw_path
        return resolved.exists() and resolved.is_dir()

    def _parse_structured(
        self,
        content: str,
        format_name: str,
        path: str,
    ) -> Any:
        if format_name == "json":
            return json.loads(content)
        if format_name == "toml":
            return tomllib.loads(content)
        if format_name in {"yaml", "yml"}:
            try:
                import yaml
            except ImportError as exc:  # pragma: no cover - optional dependency path
                raise RuntimeError(
                    f"YAML parsing requires PyYAML for structured read: {path}"
                ) from exc
            return yaml.safe_load(content)
        raise ValueError(f"Unsupported structured format: {format_name}")


def _structured_media_type(format_name: str) -> str:
    if format_name == "json":
        return "application/json"
    if format_name == "toml":
        return "application/toml"
    if format_name in {"yaml", "yml"}:
        return "application/yaml"
    return "text/plain"
