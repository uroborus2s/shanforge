import importlib.util
import json
import sys
import tempfile
import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FACTORY_CORE = REPO_ROOT / "scripts" / "factory_core.py"
FACTORY_HISTORICAL_PROJECT_ONBOARDING = REPO_ROOT / "scripts" / "factory-historical-project-onboarding"
FACTORY_TECH_PROFILE = REPO_ROOT / "scripts" / "factory-tech-profile"
SKILL_CREATOR_SCRIPTS = REPO_ROOT / "skills" / "skill-creator" / "scripts"
DEFAULTS_CONFIG = REPO_ROOT / "config" / "software-factory.defaults.json"


def load_script_module(module_name: str, script_path: Path):
    script_dir = str(script_path.parent)
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
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
        cls.factory_core = load_script_module("factory_core_crawler4j_skill", FACTORY_CORE)
        cls.onboarding = load_script_module(
            "factory_historical_project_onboarding_crawler4j_skill",
            FACTORY_HISTORICAL_PROJECT_ONBOARDING,
        )
        cls.factory_tech_profile = load_script_module(
            "factory_tech_profile_crawler4j_skill",
            FACTORY_TECH_PROFILE,
        )
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

    def test_crawler4j_model_preset_requires_domain_skill(self):
        profile = self.factory_core.build_tech_profile_from_preset("crawler4j-core-model")

        self.assertEqual(profile["preset"], "crawler4j-model")
        self.assertIn("crawler4j-model-project", profile["required_skills"])
        self.assertIn("python-uv-project", profile["required_skills"])
        self.assertIn("skills/crawler4j-model-project/SKILL.md", profile["guides"])
        self.assertTrue(any("uvx --from crawler4j-sdk crawler4j init-model" in item for item in profile["commands"]))
        self.assertFalse(any("crawler4j-sdk==" in item for item in profile["commands"]))

    def test_merge_profile_keeps_preset_required_skills(self):
        merged = self.factory_tech_profile.merge_profile(
            existing=self.factory_core.normalize_tech_profile_record({"preset": "python-backend"}),
            incoming={"preset": "crawler4j-model"},
            replace=False,
        )

        self.assertIn("crawler4j-model-project", merged["required_skills"])
        self.assertIn("python-uv-project", merged["required_skills"])
        self.assertIn("backend-engineer", merged["role_required_skills"])
        self.assertIn("crawler4j-model-project", merged["role_required_skills"]["backend-engineer"])

    def test_merge_profile_reapplying_same_preset_replaces_stale_commands(self):
        existing = self.factory_core.normalize_tech_profile_record({"preset": "crawler4j-model"})
        existing["commands"] = [
            "优先执行 `uvx --from crawler4j-sdk==1.0.3 crawler4j init-model <module_name>` 创建模块项目；脚本化场景加 `--defaults --no-git --no-install`。"
        ]

        merged = self.factory_tech_profile.merge_profile(
            existing=existing,
            incoming={"preset": "crawler4j-model"},
            replace=False,
        )

        self.assertTrue(any("uvx --from crawler4j-sdk crawler4j init-model" in item for item in merged["commands"]))
        self.assertFalse(any("crawler4j-sdk==" in item for item in merged["commands"]))

    def test_detect_stack_identifies_generated_crawler4j_model_project(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "README.md").write_text("# hotel_demo\n", encoding="utf-8")
            (project_root / "module.yaml").write_text("name: hotel_demo\nversion: 1.0.0\n", encoding="utf-8")
            (project_root / "pyproject.toml").write_text(
                "\n".join(
                    [
                        "[project]",
                        'name = "hotel-demo"',
                        'dependencies = ["crawler4j-sdk"]',
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            scan = self.onboarding.detect_stack(project_root, "auto")

        self.assertEqual(scan["preset"], "crawler4j-model")
        self.assertIn("crawler4j", scan["stack_label"].lower())
        self.assertTrue(any("model/模块项目" in line for line in scan["findings"]))

    def test_detect_stack_identifies_crawler4j_core_repo(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "README.md").write_text("# crawler4j\n", encoding="utf-8")
            (project_root / "pyproject.toml").write_text("[project]\nname = \"crawler4j\"\n", encoding="utf-8")
            (project_root / "crawler4j_sdk").mkdir()
            (project_root / "crawler4j_contracts").mkdir()
            (project_root / "crawler4j_sdk" / "pyproject.toml").write_text(
                "[project]\nname = \"crawler4j-sdk\"\n",
                encoding="utf-8",
            )
            (project_root / "crawler4j_contracts" / "pyproject.toml").write_text(
                "[project]\nname = \"crawler4j-contracts\"\n",
                encoding="utf-8",
            )

            scan = self.onboarding.detect_stack(project_root, "auto")

        self.assertEqual(scan["preset"], "crawler4j-model")
        self.assertIn("crawler4j", scan["stack_label"].lower())
        self.assertTrue(any("Core + SDK" in line for line in scan["findings"]))

    def test_crawler4j_model_skill_definition_is_valid(self):
        valid, message = self.quick_validate.validate_skill(REPO_ROOT / "skills" / "crawler4j-model-project")

        self.assertTrue(valid, message)


if __name__ == "__main__":
    unittest.main()
