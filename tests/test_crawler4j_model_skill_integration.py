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


if __name__ == "__main__":
    unittest.main()
