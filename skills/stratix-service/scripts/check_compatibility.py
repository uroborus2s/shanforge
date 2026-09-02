#!/usr/bin/env python3
"""Check the fixed Stratix package matrix for a project."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    args = parser.parse_args()
    project = args.project.resolve()
    expected = {
        "@stratix/core": "1.1.2",
        "@stratix/forge": "1.1.4",
        "@stratix/create": "1.1.2",
        "@stratix/database": "1.1.1",
        "@stratix/testing": "1.0.0-beta.1",
    }
    try:
        package = json.loads((project / "package.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"package.json is invalid: {error}")
        return 1
    if not isinstance(package, dict):
        print("package.json must contain an object")
        return 1
    dependencies = package.get("dependencies", {})
    dev_dependencies = package.get("devDependencies", {})
    if not isinstance(dependencies, dict):
        print("dependencies must be an object")
        return 1
    if not isinstance(dev_dependencies, dict):
        print("devDependencies must be an object")
        return 1
    declared = {**dependencies, **dev_dependencies}
    errors: list[str] = []
    lockfile = project / "pnpm-lock.yaml"
    try:
        lock_text = lockfile.read_text(encoding="utf-8")
    except OSError as error:
        print(f"pnpm-lock.yaml is invalid: {error}")
        return 1
    for name, required in expected.items():
        installed = project / "node_modules" / name / "package.json"
        if installed.is_file():
            try:
                detected = json.loads(installed.read_text(encoding="utf-8")).get(
                    "version", "unknown"
                )
            except (OSError, json.JSONDecodeError):
                detected = "invalid installed package.json"
        else:
            detected = declared.get(name, "unknown")
        if detected != required:
            errors.append(f"{name}: detected={detected} required={required}")
        if f"{name}@{required}" not in lock_text:
            errors.append(f"{name}: lock detected=missing required={required}")
    if errors:
        print("\n".join(errors))
        return 1
    for command in (
        ["pnpm", "exec", "stratix", "--help"],
        ["pnpm", "exec", "stratix", "doctor"],
    ):
        try:
            smoke = subprocess.run(command, text=True, capture_output=True, cwd=project)
        except OSError as error:
            print(f"{' '.join(command)} failed: {error}")
            return 1
        if smoke.returncode != 0:
            print(f"{' '.join(command)} smoke failed")
            return 1
    print("compatible: fixed Stratix package matrix")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
