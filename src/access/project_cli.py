"""Argument parsing and receipt presentation for the project CLI."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from dataclasses import asdict, dataclass
from typing import Any, Protocol, TextIO

from application.project_knowledge.query_service import QueryFailure
from domain.project_knowledge.sensitive_values import sanitize_value


class ProjectCommandApplication(Protocol):
    def execute(self, command: str, **arguments: Any) -> dict[str, Any]: ...


@dataclass(frozen=True, slots=True)
class ProjectCommandReceipt:
    schema_id: str
    command: str
    status: str
    exit_code: int
    failure_code: str | None
    summary: str
    data: dict[str, Any] | None


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="project", add_help=False, exit_on_error=False)
    root = parser.add_subparsers(dest="root")
    project = root.add_parser("project", add_help=False, exit_on_error=False)
    commands = project.add_subparsers(dest="command")
    index = commands.add_parser("index", add_help=False, exit_on_error=False)
    index.add_argument("action", choices=("check", "refresh", "rebuild"))
    index.add_argument("--json", action="store_true")
    find = commands.add_parser("find", add_help=False, exit_on_error=False)
    find.add_argument("query")
    find.add_argument("--json", action="store_true")
    show = commands.add_parser("show", add_help=False, exit_on_error=False)
    show.add_argument("entity_id")
    show.add_argument("--json", action="store_true")
    trace = commands.add_parser("trace", add_help=False, exit_on_error=False)
    trace.add_argument("entity_id")
    trace.add_argument("--depth", type=int, default=2)
    trace.add_argument("--json", action="store_true")
    context = commands.add_parser("context", add_help=False, exit_on_error=False)
    context.add_argument("entity_id")
    context.add_argument("--max-files", type=int, default=4)
    context.add_argument("--max-bytes", type=int, default=32 * 1024)
    context.add_argument("--json", action="store_true")
    sync = commands.add_parser("sync", add_help=False, exit_on_error=False)
    sync.add_argument("action", choices=("enqueue", "head"))
    sync.add_argument("--head")
    sync.add_argument("--scope", default="project")
    sync.add_argument("--json", action="store_true")
    snapshot = commands.add_parser("snapshot", add_help=False, exit_on_error=False)
    snapshot.add_argument("--html", action="store_true")
    snapshot_mode = snapshot.add_mutually_exclusive_group()
    snapshot_mode.add_argument("--check", action="store_true")
    snapshot_mode.add_argument("--rebuild", action="store_true")
    snapshot.add_argument(
        "--profile", choices=("local-owner", "shared-restricted"), default="local-owner"
    )
    snapshot.add_argument("--json", action="store_true")
    maintain = commands.add_parser("maintain", add_help=False, exit_on_error=False)
    maintain_mode = maintain.add_mutually_exclusive_group(required=True)
    maintain_mode.add_argument("--dry-run", action="store_true")
    maintain_mode.add_argument("--apply", action="store_true")
    maintain.add_argument("--json", action="store_true")
    return parser


def _receipt_json(receipt: ProjectCommandReceipt) -> str:
    return json.dumps(
        sanitize_value(asdict(receipt)),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def _emit(receipt: ProjectCommandReceipt, *, json_only: bool, stdout: TextIO) -> None:
    if not json_only:
        stdout.write(receipt.summary + "\n")
    stdout.write(_receipt_json(receipt) + "\n")


def run(
    argv: list[str],
    application: ProjectCommandApplication,
    *,
    stdout: TextIO = sys.stdout,
    stderr: TextIO = sys.stderr,
) -> int:
    del stderr
    command_name = "invalid"
    json_only = "--json" in argv
    try:
        arguments = _parser().parse_args(argv)
        if arguments.root != "project" or arguments.command is None:
            raise QueryFailure("INVALID_INPUT", "请指定 project 子命令", exit_code=2)
        command_name = str(arguments.command)
        values = vars(arguments)
        values.pop("root", None)
        values.pop("command", None)
        values.pop("json", None)
        if command_name == "index":
            action = str(values.pop("action"))
            command_name = f"index.{action}"
        elif command_name == "sync":
            action = str(values.pop("action"))
            command_name = f"sync.{action}"
            if action == "enqueue" and not values.get("head"):
                raise QueryFailure("INVALID_INPUT", "sync enqueue 需要 --head", exit_code=2)
            if action == "head":
                values.pop("head", None)
        elif command_name == "snapshot" and not values.get("html"):
            raise QueryFailure("INVALID_INPUT", "snapshot 需要 --html", exit_code=2)
        data = application.execute(command_name, **values)
        receipt = ProjectCommandReceipt(
            schema_id="ProjectCommandReceipt/v1",
            command=command_name,
            status="success",
            exit_code=0,
            failure_code=None,
            summary=f"成功：{command_name} 已完成",
            data=data,
        )
    except (argparse.ArgumentError, SystemExit, QueryFailure, ValueError) as error:
        if isinstance(error, QueryFailure):
            exit_code = error.exit_code
            failure_code = error.code
            message = str(error)
        else:
            exit_code = 2
            failure_code = "INVALID_INPUT"
            message = str(error) or "invalid command input"
        receipt = ProjectCommandReceipt(
            schema_id="ProjectCommandReceipt/v1",
            command=command_name,
            status="failed",
            exit_code=exit_code,
            failure_code=failure_code,
            summary=f"失败：{message}",
            data=None,
        )
    except sqlite3.Error as error:
        receipt = ProjectCommandReceipt(
            schema_id="ProjectCommandReceipt/v1",
            command=command_name,
            status="failed",
            exit_code=6,
            failure_code="INDEX_CORRUPT_OR_REBUILD_REQUIRED",
            summary=f"失败：{error}",
            data=None,
        )
    except Exception as error:  # pragma: no cover - defensive CLI boundary
        receipt = ProjectCommandReceipt(
            schema_id="ProjectCommandReceipt/v1",
            command=command_name,
            status="failed",
            exit_code=8,
            failure_code="INTERNAL_FAILURE",
            summary=f"失败：{type(error).__name__}",
            data=None,
        )
    _emit(receipt, json_only=json_only, stdout=stdout)
    return receipt.exit_code


def main(argv: list[str] | None = None) -> int:
    raise RuntimeError("project CLI must be invoked through settings.composition.project_knowledge")
