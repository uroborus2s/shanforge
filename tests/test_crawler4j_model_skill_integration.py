import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULTS_CONFIG = REPO_ROOT / "config" / "software-factory.defaults.json"


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


if __name__ == "__main__":
    unittest.main()
