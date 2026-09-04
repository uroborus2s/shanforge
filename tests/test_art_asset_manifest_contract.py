from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "skills/art-asset-pipeline/scripts/validate_manifest.py"


def test_manifest_validator_accepts_valid_and_rejects_invalid_assets(tmp_path: Path) -> None:
    valid = {
        "pack_type": "app",
        "assets": [
            {"path": "approved/icon.png", "purpose": "icon", "source": "approved/source.png"},
        ],
    }
    (tmp_path / "approved").mkdir()
    (tmp_path / "approved/icon.png").write_bytes(b"png")
    (tmp_path / "approved/source.png").write_bytes(b"png")
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps(valid), encoding="utf-8")
    accepted = subprocess.run(
        [sys.executable, str(VALIDATOR), str(manifest)], text=True, capture_output=True
    )
    assert accepted.returncode == 0, accepted.stderr

    valid["assets"].append(
        {"path": "tmp/draft.png", "purpose": "draft", "source": "approved/missing.png"}
    )
    manifest.write_text(json.dumps(valid), encoding="utf-8")
    rejected = subprocess.run(
        [sys.executable, str(VALIDATOR), str(manifest)], text=True, capture_output=True
    )
    assert rejected.returncode == 1
    assert "tmp/draft.png" in rejected.stdout


def test_skill_states_machine_checkable_manifest_fields() -> None:
    skill = (REPO_ROOT / "skills/art-asset-pipeline/SKILL.md").read_text(encoding="utf-8")

    for phrase in ("`pack_type`", "`assets`", "`path`", "`source`", "临时路径", "缺失文件"):
        assert phrase in skill

    assert "不属于 UI 项目流程" in skill
