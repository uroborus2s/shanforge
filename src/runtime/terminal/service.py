from __future__ import annotations

from dataclasses import dataclass

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
        raise NotImplementedError("Scaffold only: implement command execution in TASK-017.")

    def run_git(
        self,
        argv: tuple[str, ...],
        cwd: str,
        context: CapabilityInvocationContext,
    ) -> CommandExecutionResult:
        raise NotImplementedError("Scaffold only: implement git execution in TASK-017.")

    def stream_command(
        self,
        request: CommandExecutionRequest,
        context: CapabilityInvocationContext,
    ) -> CommandExecutionResult:
        raise NotImplementedError("Scaffold only: implement command streaming in TASK-017.")

    def inspect_writeset(
        self,
        result: CommandExecutionResult,
        context: CapabilityInvocationContext,
    ) -> WriteSetAudit:
        raise NotImplementedError("Scaffold only: implement write-set inspection in TASK-017.")
