from __future__ import annotations

import unittest
from contextlib import redirect_stdout
from dataclasses import dataclass
from io import StringIO

from access.api.runtime_api import RuntimeAPI
from access.cli.main import main as run_demo
from domain.agent_app.manifest import AgentAppManifest
from domain.agent_app.models import AgentApp
from domain.response.models import AgentResponse


@dataclass(slots=True, frozen=True)
class _ExecutionResult:
    response: AgentResponse


@dataclass(slots=True)
class _RuntimeExecutionUseCase:
    manifest: AgentAppManifest | None = None
    user_input: str | None = None

    def execute_manifest(
        self,
        manifest: AgentAppManifest,
        user_input: str,
        workflow_id: str | None = None,
        session_id: str | None = None,
    ) -> _ExecutionResult:
        self.manifest = manifest
        self.user_input = user_input
        return _ExecutionResult(response=AgentResponse(summary="ok", raw_output="demo scaffold output"))

    def execute_app(
        self,
        app: AgentApp,
        user_input: str,
        workflow_id: str | None = None,
        session_id: str | None = None,
    ) -> _ExecutionResult:
        raise AssertionError("CLI demo should execute a manifest, not a pre-built app.")


class AccessCliTests(unittest.TestCase):
    def test_run_demo_executes_manifest_through_injected_runtime_api(self) -> None:
        runtime_use_case = _RuntimeExecutionUseCase()
        runtime_api = RuntimeAPI(service=runtime_use_case)
        stdout = StringIO()

        with redirect_stdout(stdout):
            run_demo(runtime_api)

        self.assertEqual(stdout.getvalue().strip(), "demo scaffold output")
        self.assertIsNotNone(runtime_use_case.manifest)
        assert runtime_use_case.manifest is not None
        self.assertEqual(runtime_use_case.manifest.metadata.id, "demo.writer")
        self.assertEqual(runtime_use_case.user_input, "Build the abstract shanforge v2 platform scaffold.")


if __name__ == "__main__":
    unittest.main()
