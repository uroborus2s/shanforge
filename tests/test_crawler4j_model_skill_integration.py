import importlib.util
import json
import sys
import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_CREATOR_SCRIPTS = REPO_ROOT / "skills" / "skill-creator" / "scripts"
DEFAULTS_CONFIG = REPO_ROOT / "config" / "software-factory.defaults.json"


def load_script_module(module_name: str, script_path: Path):
    loader = SourceFileLoader(module_name, str(script_path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class Crawler4jModelSkillIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.quick_validate = load_script_module(
            "skill_creator_quick_validate_crawler4j_skill",
            SKILL_CREATOR_SCRIPTS / "quick_validate.py",
        )

    def test_defaults_register_crawler4j_model_skill(self):
        payload = json.loads(DEFAULTS_CONFIG.read_text(encoding="utf-8"))
        skill_map = {item["name"]: item for item in payload["shared_skills"]}

        self.assertIn("crawler4j-model-project", skill_map)
        self.assertEqual(
            skill_map["crawler4j-model-project"]["path"],
            "skills/crawler4j-model-project/SKILL.md",
        )

    def test_crawler4j_model_skill_definition_is_valid(self):
        valid, message = self.quick_validate.validate_skill(
            REPO_ROOT / "skills" / "crawler4j-model-project"
        )

        self.assertTrue(valid, message)

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
