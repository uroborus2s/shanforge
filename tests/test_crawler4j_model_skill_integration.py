import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULTS_CONFIG = REPO_ROOT / "config" / "software-factory.defaults.json"
CHECKER = REPO_ROOT / "skills/crawler4j-model-project/scripts/check_compatibility.py"


def write_fake_crawler4j(
    path: Path, marker: Path, version: str = "0.4.0", version_exit: int = 0, structure_exit: int = 0
) -> None:
    path.write_text(
        "#!/bin/sh\n"
        f"printf '%s\\n' \"$*\" >> {marker}\n"
        f"if [ \"$1\" = \"--version\" ]; then echo {version}; exit {version_exit}; fi\n"
        f"exit {structure_exit}\n",
        encoding="utf-8",
    )
    path.chmod(0o755)


class Crawler4jModelSkillIntegrationTests(unittest.TestCase):
    def test_defaults_register_crawler4j_model_skill(self):
        payload = json.loads(DEFAULTS_CONFIG.read_text(encoding="utf-8"))
        skill_map = {item["name"]: item for item in payload["shared_skills"]}

        self.assertIn("crawler4j-model-project", skill_map)
        self.assertEqual(
            skill_map["crawler4j-model-project"]["path"],
            "skills/crawler4j-model-project/SKILL.md",
        )

    def test_crawler4j_model_skill_reports_shanforge_status_package(self):
        content = (REPO_ROOT / "skills" / "crawler4j-model-project" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        for phrase in (
            "工作结果：",
            "- work_item: <WORKITEM-ID>",
            "- skill: crawler4j-model-project",
            "- status: ready_for_review | blocked | needs_user_input",
            "- ledger_event: <event id or none>",
            "`blocked` 用于 CLI 不存在",
            "`needs_user_input` 用于模块名",
        ):
            self.assertIn(phrase, content)

    def test_crawler4j_model_skill_fails_closed_on_unknown_or_incompatible_protocol(self):
        content = (REPO_ROOT / "skills" / "crawler4j-model-project" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        for phrase in (
            "## 版本兼容门",
            "任何 `0.4.0` / `core-native-v2` 指导或命令前",
            "实际 CLI/包版本",
            "`module.yaml.runtime_api`",
            "`.crawler4j/manifest.lock.json`",
            "仅当实际版本为 `0.4.0` 且协议为 `core-native-v2`",
            "缺版本、未知或不兼容时，立即 `blocked`",
            "- detected_version:",
            "- required_version: 0.4.0/core-native-v2",
            "- difference:",
            "- not_executed_commands:",
            "- next_required_action:",
        ):
            self.assertIn(phrase, content)

    def test_version_and_protocol_smoke_runs_real_cli_after_lock_compatibility(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            module = project / "module.yaml"
            module.write_text("runtime_api: core-native-v2\n", encoding="utf-8")
            lock = project / ".crawler4j" / "manifest.lock.json"
            lock.parent.mkdir()
            lock.write_text(json.dumps({"scanned": []}), encoding="utf-8")
            marker = project / "crawler4j.calls"
            bin_dir = project / "bin"
            bin_dir.mkdir()
            write_fake_crawler4j(bin_dir / "crawler4j", marker)
            compatible = subprocess.run(
                [sys.executable, str(CHECKER), str(project)],
                check=False,
                text=True,
                capture_output=True,
                env={"PATH": str(bin_dir)},
            )
            self.assertEqual(compatible.returncode, 0, compatible.stdout)
            self.assertEqual(
                marker.read_text(encoding="utf-8").splitlines(),
                ["--version", "module check structure"],
            )

    def test_version_gate_rejects_invalid_lock_without_running_smoke(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "module.yaml").write_text("runtime_api: core-native-v2\n", encoding="utf-8")
            lock = project / ".crawler4j" / "manifest.lock.json"
            lock.parent.mkdir()
            marker = project / "crawler4j.calls"
            bin_dir = project / "bin"
            bin_dir.mkdir()
            write_fake_crawler4j(bin_dir / "crawler4j", marker)
            for content in ("not json", "[]"):
                with self.subTest(content=content):
                    lock.write_text(content, encoding="utf-8")
                    incompatible = subprocess.run(
                        [sys.executable, str(CHECKER), str(project)],
                        check=False,
                        text=True,
                        capture_output=True,
                        env={"PATH": str(bin_dir)},
                    )
                    self.assertNotEqual(incompatible.returncode, 0)
                    self.assertIn("manifest lock is invalid", incompatible.stdout)
                    self.assertFalse(marker.exists())

    def test_cli_smoke_failure_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "module.yaml").write_text("runtime_api: core-native-v2\n", encoding="utf-8")
            lock = project / ".crawler4j" / "manifest.lock.json"
            lock.parent.mkdir()
            lock.write_text("{}", encoding="utf-8")
            marker = project / "crawler4j.calls"
            bin_dir = project / "bin"
            bin_dir.mkdir()
            for version, version_exit, structure_exit, calls in (
                ("0.3.9", 0, 0, ["--version"]),
                ("0.4.0", 1, 0, ["--version"]),
                ("0.4.0", 0, 1, ["--version", "module check structure"]),
            ):
                with self.subTest(version=version, structure_exit=structure_exit):
                    write_fake_crawler4j(
                        bin_dir / "crawler4j", marker, version, version_exit, structure_exit
                    )
                    result = subprocess.run(
                        [sys.executable, str(CHECKER), str(project)],
                        check=False,
                        text=True,
                        capture_output=True,
                        env={"PATH": str(bin_dir)},
                    )
                    self.assertEqual(result.returncode, 1)
                    self.assertEqual(marker.read_text(encoding="utf-8").splitlines(), calls)
                    marker.unlink()

    def test_incompatible_protocol_or_override_skips_structure_smoke(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            lock = project / ".crawler4j" / "manifest.lock.json"
            lock.parent.mkdir()
            lock.write_text("{}", encoding="utf-8")
            marker = project / "crawler4j.calls"
            bin_dir = project / "bin"
            bin_dir.mkdir()
            write_fake_crawler4j(bin_dir / "crawler4j", marker)
            for runtime_api, cli_version in (("legacy-v1", None), ("core-native-v2", "0.3.9")):
                with self.subTest(runtime_api=runtime_api, cli_version=cli_version):
                    (project / "module.yaml").write_text(
                        f"runtime_api: {runtime_api}\n", encoding="utf-8"
                    )
                    command = [sys.executable, str(CHECKER), str(project)]
                    if cli_version is not None:
                        command.extend(("--cli-version", cli_version))
                    result = subprocess.run(
                        command,
                        check=False,
                        text=True,
                        capture_output=True,
                        env={"PATH": str(bin_dir)},
                    )
                    self.assertEqual(result.returncode, 1)
                    self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
