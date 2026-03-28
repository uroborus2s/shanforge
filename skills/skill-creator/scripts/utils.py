"""Shared utilities for skill-creator scripts."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any


FRONTMATTER_REGEX = re.compile(r"^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n([\s\S]*))?$")
FOLDED_MARKERS = {">", ">-"}
LITERAL_MARKERS = {"|", "|-"}


def ensure_script_dir_on_path(script_file: str | Path) -> Path:
    """Allow standalone script execution from the repo root."""
    script_dir = Path(script_file).resolve().parent
    script_dir_str = str(script_dir)
    if script_dir_str not in sys.path:
        sys.path.insert(0, script_dir_str)
    return script_dir


def extract_frontmatter(content: str) -> tuple[str, str]:
    """Split SKILL.md content into frontmatter and markdown body."""
    match = FRONTMATTER_REGEX.match(content)
    if not match:
        raise ValueError("Invalid frontmatter format")
    body = match.group(2) or ""
    return match.group(1), body


def _strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _dedent_block(block_lines: list[str]) -> list[str]:
    dedented: list[str] = []
    for line in block_lines:
        if line.startswith("  "):
            dedented.append(line[2:])
        elif line.startswith("\t"):
            dedented.append(line[1:])
        else:
            dedented.append(line)
    return dedented


def _parse_block_value(raw_value: str, block_lines: list[str]) -> Any:
    if raw_value in FOLDED_MARKERS | LITERAL_MARKERS:
        dedented = _dedent_block(block_lines)
        if raw_value in FOLDED_MARKERS:
            return " ".join(line.strip() for line in dedented if line.strip())
        return "\n".join(dedented).strip()

    if raw_value:
        return _strip_quotes(raw_value)

    dedented = _dedent_block(block_lines)
    nonempty = [line for line in dedented if line.strip()]
    if not nonempty:
        return ""

    if all(line.lstrip().startswith("- ") for line in nonempty):
        return [_strip_quotes(line.lstrip()[2:].strip()) for line in nonempty]

    nested: dict[str, str] = {}
    for line in nonempty:
        if ":" not in line:
            return " ".join(item.strip() for item in nonempty)
        key, value = line.split(":", 1)
        nested[key.strip()] = _strip_quotes(value.strip())
    return nested


def parse_frontmatter(frontmatter_text: str) -> dict[str, Any]:
    """Parse the simple YAML subset used by SKILL.md frontmatter."""
    data: dict[str, Any] = {}
    lines = frontmatter_text.splitlines()
    i = 0

    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith((" ", "\t", "-")):
            raise ValueError(f"Invalid top-level frontmatter line: {line}")
        if ":" not in line:
            raise ValueError(f"Invalid frontmatter line: {line}")

        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if not key:
            raise ValueError("Frontmatter key cannot be empty")

        i += 1
        block_lines: list[str] = []
        while i < len(lines):
            next_line = lines[i]
            if not next_line.strip():
                block_lines.append("")
                i += 1
                continue
            if next_line.startswith((" ", "\t")):
                block_lines.append(next_line)
                i += 1
                continue
            break

        data[key] = _parse_block_value(raw_value, block_lines)

    return data


def parse_skill_md(skill_path: Path) -> tuple[str, str, str]:
    """Parse a SKILL.md file, returning (name, description, full_content)."""
    content = (skill_path / "SKILL.md").read_text(encoding="utf-8")
    frontmatter_text, _ = extract_frontmatter(content)
    frontmatter = parse_frontmatter(frontmatter_text)

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if not isinstance(name, str):
        raise ValueError("Frontmatter field 'name' must be a string")
    if not isinstance(description, str):
        raise ValueError("Frontmatter field 'description' must be a string")

    return name.strip(), description.strip(), content
