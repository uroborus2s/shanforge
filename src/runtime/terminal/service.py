from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from pathlib import Path

from runtime.capability.contracts import (
    CapabilityInvocationContext,
    CapabilityOperationDescriptor,
    CapabilityPackageDescriptor,
    CapabilityProviderDependency,
)
from runtime.ports.execution_backends import GitProviderPort, ShellCommandProviderPort
from runtime.terminal.models import CommandExecutionRequest, CommandExecutionResult, WriteSetAudit


@dataclass(slots=True)
class TerminalService:
    """Self-owned scaffold for shell and git execution capabilities."""

    shell_provider: ShellCommandProviderPort | None = None
    git_provider: GitProviderPort | None = None

    def describe_package(self) -> CapabilityPackageDescriptor:
        return CapabilityPackageDescriptor(
            package_id="terminal",
            name="Terminal",
            summary="Runs governed shell and git operations with write-set auditing.",
            operations=(
                CapabilityOperationDescriptor(
                    operation_id="terminal.run_command",
                    method_name="run_command",
                    summary="Run one shell command.",
                    risk_level="L2",
                    writes_data=True,
                ),
                CapabilityOperationDescriptor(
                    operation_id="terminal.run_git",
                    method_name="run_git",
                    summary="Run one git command.",
                    risk_level="L2",
                    writes_data=True,
                ),
                CapabilityOperationDescriptor(
                    operation_id="terminal.stream_command",
                    method_name="stream_command",
                    summary="Stream one shell command.",
                    risk_level="L2",
                    writes_data=True,
                ),
                CapabilityOperationDescriptor(
                    operation_id="terminal.inspect_writeset",
                    method_name="inspect_writeset",
                    summary="Inspect command-side effects.",
                    risk_level="L1",
                ),
            ),
            provider_dependencies=(
                CapabilityProviderDependency("shell_command", required=False),
                CapabilityProviderDependency("git", required=False),
            ),
        )

    def run_command(
        self,
        request: CommandExecutionRequest,
        context: CapabilityInvocationContext,
    ) -> CommandExecutionResult:
        self._ensure_execution_allowed(context)
        provider = self._require_shell_provider()
        cwd = request.cwd or context.cwd or context.workspace_root or os.getcwd()
        before_snapshot = self._snapshot_paths(cwd)
        payload = provider.run(request.argv, cwd=cwd)
        after_snapshot = self._snapshot_paths(cwd)
        audit = self._build_writeset(before_snapshot, after_snapshot)
        return CommandExecutionResult(
            argv=tuple(payload.get("argv") or request.argv),
            cwd=str(payload.get("cwd") or cwd),
            exit_code=int(payload.get("exit_code") or 0),
            stdout=str(payload.get("stdout") or ""),
            stderr=str(payload.get("stderr") or ""),
            duration_ms=int(payload.get("duration_ms") or 0),
            metadata={
                "writeset": asdict(audit),
                "capture_output": request.capture_output,
            },
        )

    def run_git(
        self,
        argv: tuple[str, ...],
        cwd: str,
        context: CapabilityInvocationContext,
    ) -> CommandExecutionResult:
        self._ensure_execution_allowed(context)
        provider = self._require_git_provider()
        before_snapshot = self._snapshot_paths(cwd)
        payload = provider.run_git(cwd=cwd, argv=argv)
        after_snapshot = self._snapshot_paths(cwd)
        audit = self._build_writeset(before_snapshot, after_snapshot)
        return CommandExecutionResult(
            argv=tuple(payload.get("argv") or ("git", *argv)),
            cwd=str(payload.get("cwd") or cwd),
            exit_code=int(payload.get("exit_code") or 0),
            stdout=str(payload.get("stdout") or ""),
            stderr=str(payload.get("stderr") or ""),
            duration_ms=int(payload.get("duration_ms") or 0),
            metadata={"writeset": asdict(audit)},
        )

    def stream_command(
        self,
        request: CommandExecutionRequest,
        context: CapabilityInvocationContext,
    ) -> CommandExecutionResult:
        result = self.run_command(request, context)
        metadata = dict(result.metadata)
        metadata["streamed"] = True
        return CommandExecutionResult(
            argv=result.argv,
            cwd=result.cwd,
            exit_code=result.exit_code,
            stdout=result.stdout,
            stderr=result.stderr,
            duration_ms=result.duration_ms,
            metadata=metadata,
        )

    def inspect_writeset(
        self,
        result: CommandExecutionResult,
        context: CapabilityInvocationContext,
    ) -> WriteSetAudit:
        del context
        writeset = result.metadata.get("writeset")
        if isinstance(writeset, dict):
            return WriteSetAudit(
                touched_paths=tuple(str(item) for item in writeset.get("touched_paths", ())),
                created_paths=tuple(str(item) for item in writeset.get("created_paths", ())),
                deleted_paths=tuple(str(item) for item in writeset.get("deleted_paths", ())),
                warnings=tuple(str(item) for item in writeset.get("warnings", ())),
            )
        return WriteSetAudit(warnings=("write-set metadata missing",))

    def _ensure_execution_allowed(self, context: CapabilityInvocationContext) -> None:
        if context.sandbox_decision == "denied":
            raise PermissionError("Sandbox denied the terminal execution request.")
        if not context.approval_ref:
            raise PermissionError("Approval is required before running terminal commands.")

    def _require_shell_provider(self) -> ShellCommandProviderPort:
        if self.shell_provider is None:
            raise RuntimeError("Shell command provider is not configured.")
        return self.shell_provider

    def _require_git_provider(self) -> GitProviderPort:
        if self.git_provider is None:
            raise RuntimeError("Git provider is not configured.")
        return self.git_provider

    def _snapshot_paths(self, cwd: str) -> dict[str, tuple[int, int]]:
        root = Path(cwd).expanduser().resolve()
        if not root.exists() or not root.is_dir():
            return {}

        snapshot: dict[str, tuple[int, int]] = {}
        for path in root.rglob("*"):
            if ".git" in path.parts:
                continue
            if not path.is_file():
                continue
            try:
                stat = path.stat()
            except OSError:
                continue
            relative = str(path.relative_to(root))
            snapshot[relative] = (stat.st_size, stat.st_mtime_ns)
        return snapshot

    def _build_writeset(
        self,
        before_snapshot: dict[str, tuple[int, int]],
        after_snapshot: dict[str, tuple[int, int]],
    ) -> WriteSetAudit:
        before_paths = set(before_snapshot)
        after_paths = set(after_snapshot)
        created_paths = tuple(sorted(after_paths - before_paths))
        deleted_paths = tuple(sorted(before_paths - after_paths))
        modified_paths = tuple(
            sorted(
                path
                for path in before_paths & after_paths
                if before_snapshot[path] != after_snapshot[path]
            )
        )
        touched_paths = tuple(
            sorted(set(created_paths) | set(deleted_paths) | set(modified_paths))
        )
        return WriteSetAudit(
            touched_paths=touched_paths,
            created_paths=created_paths,
            deleted_paths=deleted_paths,
        )
