from __future__ import annotations

import os
import subprocess
import time
from dataclasses import dataclass
from typing import Any

from runtime.ports.execution_backends import GitProviderPort, ShellCommandProviderPort


@dataclass(slots=True)
class LocalShellCommandProvider(ShellCommandProviderPort):
    """Local subprocess-backed shell command provider."""

    def run(
        self,
        argv: tuple[str, ...],
        cwd: str | None = None,
    ) -> dict[str, Any]:
        started_at = time.monotonic()
        completed = subprocess.run(
            argv,
            cwd=cwd,
            capture_output=True,
            text=True,
            env=os.environ.copy(),
            check=False,
        )
        duration_ms = int((time.monotonic() - started_at) * 1000)
        return {
            "argv": argv,
            "cwd": cwd,
            "exit_code": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "duration_ms": duration_ms,
        }


@dataclass(slots=True)
class LocalGitProvider(GitProviderPort):
    """Local subprocess-backed git provider."""

    git_executable: str = "git"

    def run_git(self, cwd: str, argv: tuple[str, ...]) -> dict[str, Any]:
        started_at = time.monotonic()
        completed = subprocess.run(
            (self.git_executable, *argv),
            cwd=cwd,
            capture_output=True,
            text=True,
            env=os.environ.copy(),
            check=False,
        )
        duration_ms = int((time.monotonic() - started_at) * 1000)
        return {
            "argv": (self.git_executable, *argv),
            "cwd": cwd,
            "exit_code": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "duration_ms": duration_ms,
        }
