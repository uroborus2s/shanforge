#!/usr/bin/env python3
"""Check the crawler4j 0.4.0/core-native-v2 compatibility gate."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--cli-version")
    args = parser.parse_args()
    project = args.project.resolve()
    module = project / "module.yaml"
    manifest = project / ".crawler4j" / "manifest.lock.json"
    errors: list[str] = []
    if not module.is_file():
        errors.append("module.yaml is missing")
        runtime_api = "unknown"
    else:
        match = re.search(r"^runtime_api:\s*([^\s#]+)", module.read_text(encoding="utf-8"), re.M)
        runtime_api = match.group(1) if match else "unknown"
    try:
        lock = json.loads(manifest.read_text(encoding="utf-8"))
        if not isinstance(lock, dict):
            raise ValueError("must contain an object")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        errors.append(f"manifest lock is invalid: {error}")
    if runtime_api != "core-native-v2":
        errors.append(f"runtime_api detected={runtime_api} required=core-native-v2")
    if args.cli_version is not None and args.cli_version != "0.4.0":
        errors.append(f"cli_version detected={args.cli_version} required=0.4.0")
    if errors:
        print("\n".join(errors))
        return 1
    try:
        version_smoke = subprocess.run(
            ["crawler4j", "--version"], text=True, capture_output=True, cwd=project
        )
    except OSError as error:
        print(f"crawler4j --version failed: {error}")
        return 1
    if version_smoke.returncode != 0 or not re.search(r"\b0\.4\.0\b", version_smoke.stdout):
        print("crawler4j --version smoke failed")
        return 1
    try:
        structure_smoke = subprocess.run(
            ["crawler4j", "module", "check", "structure"],
            text=True,
            capture_output=True,
            cwd=project,
        )
    except OSError as error:
        print(f"crawler4j module check structure failed: {error}")
        return 1
    if structure_smoke.returncode != 0:
        print("crawler4j module check structure smoke failed")
        return 1
    print("compatible: 0.4.0/core-native-v2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
