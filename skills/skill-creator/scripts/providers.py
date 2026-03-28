from __future__ import annotations

import json
import os
import select
import subprocess
import tempfile
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


ACTIVATE_SKILL_TOOL_NAME = "activate_skill"
SKILL_TRIGGER_PREFIX = "SKILL_TRIGGER:"


@dataclass
class CompletionResult:
    content: str
    triggered: bool
    tokens: int
    duration_ms: int


class ModelProvider(ABC):
    @abstractmethod
    def run_query(self, query: str, skill_name: str, skill_desc: str, timeout: int, project_root: str) -> CompletionResult:
        pass


def _count_tokens(payload: Any) -> int:
    total = 0
    if isinstance(payload, dict):
        for key, value in payload.items():
            if isinstance(value, (dict, list)):
                total += _count_tokens(value)
            elif isinstance(value, int) and "token" in key.lower():
                total += value
    elif isinstance(payload, list):
        for item in payload:
            total += _count_tokens(item)
    return total


def _build_skill_md(skill_name: str, skill_desc: str) -> str:
    return (
        "---\n"
        f"name: {skill_name}\n"
        f"description: {json.dumps(skill_desc, ensure_ascii=False)}\n"
        "---\n\n"
        f"# {skill_name}\n\n"
        "Ephemeral evaluation skill used for trigger testing.\n"
    )


def _create_temp_skill_workspace(host: str, skill_name: str, skill_desc: str) -> tempfile.TemporaryDirectory[str]:
    temp_dir = tempfile.TemporaryDirectory(prefix=f"skill-creator-{host}-")
    workspace = Path(temp_dir.name)
    roots = [workspace / ".agents" / "skills"]
    if host == "gemini":
        roots.append(workspace / ".gemini" / "skills")
    elif host == "codex":
        roots.append(workspace / ".codex" / "skills")

    for root in roots:
        skill_dir = root / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(_build_skill_md(skill_name, skill_desc), encoding="utf-8")

    return temp_dir


def _extract_codex_text(event: dict[str, Any]) -> str:
    if event.get("type") != "response_item":
        return ""
    payload = event.get("payload", {})
    if payload.get("type") != "message":
        return ""
    chunks: list[str] = []
    for item in payload.get("content", []):
        if item.get("type") in {"output_text", "text"} and isinstance(item.get("text"), str):
            chunks.append(item["text"])
    return "\n".join(chunks)


def parse_gemini_stream(raw_output: str, skill_name: str) -> tuple[str, bool, int]:
    content_parts: list[str] = []
    triggered = False
    total_tokens = 0

    for line in raw_output.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        event_type = event.get("type")
        if event_type == "message" and event.get("role") == "assistant":
            text = event.get("content")
            if isinstance(text, str):
                content_parts.append(text)
        elif event_type == "tool_use" and event.get("tool_name") == ACTIVATE_SKILL_TOOL_NAME:
            parameters = event.get("parameters", {})
            if isinstance(parameters, dict) and parameters.get("name") == skill_name:
                triggered = True
        elif event_type == "result":
            total_tokens += _count_tokens(event.get("stats", {}))

    return "\n".join(content_parts).strip(), triggered, total_tokens


def parse_codex_exec_stream(raw_output: str, skill_name: str) -> tuple[str, bool, int]:
    content_parts: list[str] = []
    triggered = False
    total_tokens = 0
    trigger_line = f"{SKILL_TRIGGER_PREFIX} {skill_name}"
    none_line = f"{SKILL_TRIGGER_PREFIX} none"

    for line in raw_output.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            if trigger_line in line:
                triggered = True
            continue

        total_tokens += _count_tokens(event)
        text = _extract_codex_text(event)
        if text:
            content_parts.append(text)
            if trigger_line in text:
                triggered = True
            elif none_line in text:
                triggered = False

    return "\n".join(content_parts).strip(), triggered, total_tokens


class ClaudeProvider(ModelProvider):
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name

    def run_query(self, query: str, skill_name: str, skill_desc: str, timeout: int, project_root: str) -> CompletionResult:
        unique_id = uuid.uuid4().hex[:8]
        clean_name = f"{skill_name}-skill-{unique_id}"
        project_commands_dir = Path(project_root) / ".claude" / "commands"
        command_file = project_commands_dir / f"{clean_name}.md"

        try:
            project_commands_dir.mkdir(parents=True, exist_ok=True)
            indented_desc = "\n  ".join(skill_desc.split("\n"))
            command_content = (
                f"---\n"
                f"description: |\n"
                f"  {indented_desc}\n"
                f"---\n\n"
                f"# {skill_name}\n\n"
                f"This skill handles: {skill_desc}\n"
            )
            command_file.write_text(command_content, encoding="utf-8")

            cmd = [
                "claude",
                "-p", query,
                "--output-format", "stream-json",
                "--verbose",
                "--include-partial-messages",
            ]
            if self.model_name:
                cmd.extend(["--model", self.model_name])

            env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                cwd=project_root,
                env=env,
            )

            triggered = False
            start_time = time.time()
            buffer = ""
            pending_tool_name = None
            accumulated_json = ""
            total_tokens = 0

            while time.time() - start_time < timeout:
                if process.poll() is not None:
                    break
                ready, _, _ = select.select([process.stdout], [], [], 1.0)
                if not ready:
                    continue
                chunk = os.read(process.stdout.fileno(), 8192)
                if not chunk:
                    break
                buffer += chunk.decode("utf-8", errors="replace")

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if not line.strip():
                        continue
                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if event.get("type") == "stream_event":
                        stream_event = event.get("event", {})
                        event_type = stream_event.get("type", "")
                        if event_type == "content_block_start":
                            content_block = stream_event.get("content_block", {})
                            if content_block.get("type") == "tool_use" and content_block.get("name", "") in ("Skill", "Read"):
                                pending_tool_name = content_block.get("name", "")
                        elif event_type == "content_block_delta" and pending_tool_name:
                            delta = stream_event.get("delta", {})
                            if delta.get("type") == "input_json_delta":
                                accumulated_json += delta.get("partial_json", "")
                                if clean_name in accumulated_json:
                                    triggered = True
                    elif event.get("type") == "message_stop":
                        total_tokens = event.get("usage", {}).get("total_tokens", 0)

            duration = int((time.time() - start_time) * 1000)
            return CompletionResult(content=accumulated_json, triggered=triggered, tokens=total_tokens, duration_ms=duration)
        finally:
            if command_file.exists():
                command_file.unlink()


class GeminiProvider(ModelProvider):
    def __init__(self, model_name: str = "gemini"):
        self.model_name = model_name

    def run_query(self, query: str, skill_name: str, skill_desc: str, timeout: int, project_root: str) -> CompletionResult:
        start_time = time.time()
        temp_dir = _create_temp_skill_workspace("gemini", skill_name, skill_desc)
        try:
            cmd = ["gemini", "--prompt", " ", "--output-format", "stream-json", "--approval-mode", "plan"]
            if self.model_name:
                cmd.extend(["--model", self.model_name])

            result = subprocess.run(
                cmd,
                input=query,
                capture_output=True,
                text=True,
                cwd=temp_dir.name,
                timeout=timeout,
            )
            if result.returncode != 0:
                raise RuntimeError(f"gemini exited {result.returncode}: {result.stderr.strip()}")

            content, triggered, tokens = parse_gemini_stream(result.stdout, skill_name)
            duration = int((time.time() - start_time) * 1000)
            return CompletionResult(content=content, triggered=triggered, tokens=tokens, duration_ms=duration)
        finally:
            temp_dir.cleanup()


class CodexProvider(ModelProvider):
    def __init__(self, model_name: str = "codex"):
        self.model_name = model_name

    def run_query(self, query: str, skill_name: str, skill_desc: str, timeout: int, project_root: str) -> CompletionResult:
        start_time = time.time()
        temp_dir = _create_temp_skill_workspace("codex", skill_name, skill_desc)
        try:
            wrapped_query = (
                f"{query}\n\n"
                f"After you finish, add a final line exactly `{SKILL_TRIGGER_PREFIX} {skill_name}` "
                f"if you activated the `{skill_name}` skill. Otherwise add `{SKILL_TRIGGER_PREFIX} none`."
            )
            cmd = [
                "codex",
                "exec",
                "--json",
                "--skip-git-repo-check",
                "--sandbox",
                "read-only",
                "--ephemeral",
                "-",
            ]
            if self.model_name:
                cmd.extend(["--model", self.model_name])

            result = subprocess.run(
                cmd,
                input=wrapped_query,
                capture_output=True,
                text=True,
                cwd=temp_dir.name,
                timeout=timeout,
            )
            if result.returncode != 0 and not result.stdout:
                raise RuntimeError(f"codex exited {result.returncode}: {result.stderr.strip()}")

            content, triggered, tokens = parse_codex_exec_stream(result.stdout, skill_name)
            duration = int((time.time() - start_time) * 1000)
            return CompletionResult(content=content, triggered=triggered, tokens=tokens, duration_ms=duration)
        finally:
            temp_dir.cleanup()


def get_provider(model_name: str) -> ModelProvider:
    lowered = model_name.lower()
    if "claude" in lowered:
        return ClaudeProvider(model_name)
    if "gemini" in lowered:
        return GeminiProvider(model_name)
    if "gpt" in lowered or "codex" in lowered:
        return CodexProvider(model_name)
    return ClaudeProvider(model_name)
