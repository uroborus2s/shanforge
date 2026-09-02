#!/usr/bin/env python3
"""Validate an approved art asset manifest using only the standard library."""

from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    manifest_path = args.manifest.resolve()
    errors: list[str] = []
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"invalid manifest: {error}")
        return 1
    if not isinstance(payload, dict) or payload.get("pack_type") not in {"app", "game"}:
        errors.append("pack_type must be app or game")
    assets = payload.get("assets") if isinstance(payload, dict) else None
    if not isinstance(assets, list):
        errors.append("assets must be an array")
        assets = []
    for index, asset in enumerate(assets):
        if not isinstance(asset, dict):
            errors.append(f"assets[{index}] must be an object")
            continue
        for field in ("path", "purpose", "source"):
            if not isinstance(asset.get(field), str) or not asset[field]:
                errors.append(f"assets[{index}].{field} must be a non-empty string")
        for field in ("path", "source"):
            value = asset.get(field)
            if not isinstance(value, str):
                continue
            path = PurePosixPath(value)
            forbidden_root = path.parts[:1] in {("tmp",), ("candidates",)}
            if path.is_absolute() or ".." in path.parts or forbidden_root:
                errors.append(f"assets[{index}].{field} is not an approved relative path: {value}")
            elif not (manifest_path.parent / path).is_file():
                errors.append(f"assets[{index}].{field} is missing: {value}")
        source = asset.get("source")
        if isinstance(source, str) and not source.startswith("approved/"):
            errors.append(f"assets[{index}].source is not under approved/: {source}")
    if errors:
        print("\n".join(errors))
        return 1
    print("manifest validation PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
