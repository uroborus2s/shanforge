from __future__ import annotations

import io
import json
from typing import Any

from access.project_cli import run
from application.project_knowledge.query_service import QueryFailure


class FakeApplication:
    def execute(self, command: str, **arguments: Any) -> dict[str, Any]:
        if command == "show" and arguments["entity_id"] == "missing":
            raise QueryFailure("ENTITY_NOT_FOUND", "entity was not found", exit_code=4)
        return {"command": command, "arguments": arguments, "items": []}


def test_cli_emits_stable_json_receipt_and_chinese_summary() -> None:
    stdout = io.StringIO()
    stderr = io.StringIO()
    exit_code = run(
        ["project", "find", "knowledge", "--json"],
        FakeApplication(),
        stdout=stdout,
        stderr=stderr,
    )
    receipt = json.loads(stdout.getvalue())
    assert exit_code == 0
    assert receipt["schema_id"] == "ProjectCommandReceipt/v1"
    assert receipt["status"] == "success"
    assert receipt["command"] == "find"
    assert stderr.getvalue() == ""

    stdout = io.StringIO()
    exit_code = run(
        ["project", "show", "REQ-1"], FakeApplication(), stdout=stdout, stderr=io.StringIO()
    )
    lines = stdout.getvalue().splitlines()
    assert lines[0].startswith("成功：")
    assert json.loads(lines[1])["exit_code"] == 0


def test_cli_maps_invalid_and_query_failures_to_stable_exit_codes() -> None:
    stdout = io.StringIO()
    assert (
        run(
            ["project", "unknown", "--json"],
            FakeApplication(),
            stdout=stdout,
            stderr=io.StringIO(),
        )
        == 2
    )
    receipt = json.loads(stdout.getvalue())
    assert receipt["failure_code"] == "INVALID_INPUT"

    stdout = io.StringIO()
    assert (
        run(
            ["project", "show", "missing", "--json"],
            FakeApplication(),
            stdout=stdout,
            stderr=io.StringIO(),
        )
        == 4
    )
    assert json.loads(stdout.getvalue())["failure_code"] == "ENTITY_NOT_FOUND"


def test_snapshot_rejects_browser_and_server_side_effect_flags() -> None:
    for unsupported_flag in ("--open", "--serve"):
        stdout = io.StringIO()
        assert (
            run(
                ["project", "snapshot", "--html", unsupported_flag, "--json"],
                FakeApplication(),
                stdout=stdout,
                stderr=io.StringIO(),
            )
            == 2
        )
        receipt = json.loads(stdout.getvalue())
        assert receipt["failure_code"] == "INVALID_INPUT"
        assert receipt["status"] == "failed"


def test_cli_receipt_redacts_sensitive_result_fields_and_token_shapes() -> None:
    class SensitiveApplication:
        def execute(self, command: str, **arguments: Any) -> dict[str, Any]:
            return {
                "password": "never-store-me",
                "message": "Bearer abcdefghijklmnopqrstuvwxyz",
            }

    stdout = io.StringIO()
    assert (
        run(
            ["project", "find", "secret", "--json"],
            SensitiveApplication(),
            stdout=stdout,
            stderr=io.StringIO(),
        )
        == 0
    )
    output = stdout.getvalue()
    assert "never-store-me" not in output
    assert "abcdefghijklmnopqrstuvwxyz" not in output
    assert output.count("[REDACTED]") == 2
