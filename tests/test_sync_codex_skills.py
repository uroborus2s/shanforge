import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sync_only_discovers_directories_with_skill_md(tmp_path: Path) -> None:
    source = tmp_path / "skills"
    (source / "valid-skill").mkdir(parents=True)
    (source / "valid-skill" / "SKILL.md").write_text("---\nname: valid-skill\n---\n")
    (source / "references").mkdir()

    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "sync-codex-skills"),
            "--source",
            str(source),
            "--codex-dir",
            str(tmp_path / "target"),
            "--skip-gemini",
            "--skip-agents",
            "--dry-run",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "valid-skill" in result.stdout
    assert "references" not in result.stdout
    assert "linked=1" in result.stdout
