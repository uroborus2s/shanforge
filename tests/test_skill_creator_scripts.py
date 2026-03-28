import importlib.util
import tempfile
import unittest
import zipfile
from importlib.machinery import SourceFileLoader
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_CREATOR_SCRIPTS = REPO_ROOT / "skills" / "skill-creator" / "scripts"


def load_script_module(module_name: str, script_path: Path):
    script_dir = str(script_path.parent)
    import sys

    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    loader = SourceFileLoader(module_name, str(script_path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class SkillCreatorScriptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.utils = load_script_module("skill_creator_utils", SKILL_CREATOR_SCRIPTS / "utils.py")
        cls.quick_validate = load_script_module("skill_creator_quick_validate", SKILL_CREATOR_SCRIPTS / "quick_validate.py")
        cls.package_skill = load_script_module("skill_creator_package_skill", SKILL_CREATOR_SCRIPTS / "package_skill.py")
        cls.providers = load_script_module("skill_creator_providers", SKILL_CREATOR_SCRIPTS / "providers.py")
        cls.improve_description = load_script_module("skill_creator_improve_description", SKILL_CREATOR_SCRIPTS / "improve_description.py")

    def _write_skill(self, root: Path, name: str = "sample-skill") -> Path:
        skill_dir = root / name
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            """---
name: sample-skill
description: >
  Use this skill for
  multiline trigger descriptions.
metadata:
  owner: team
allowed-tools:
  - Bash(echo *)
compatibility: codex and gemini
---

# Sample

Body.
""",
            encoding="utf-8",
        )
        return skill_dir

    def test_parse_frontmatter_supports_multiline_values(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_dir = self._write_skill(Path(temp_dir))
            name, description, _ = self.utils.parse_skill_md(skill_dir)

        self.assertEqual(name, "sample-skill")
        self.assertEqual(description, "Use this skill for multiline trigger descriptions.")

    def test_validate_skill_accepts_zero_dependency_frontmatter_parser(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_dir = self._write_skill(Path(temp_dir))
            valid, message = self.quick_validate.validate_skill(skill_dir)

        self.assertTrue(valid, message)
        self.assertEqual(message, "Skill is valid!")

    def test_package_skill_excludes_root_evals_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skill_dir = self._write_skill(root)
            (skill_dir / "evals").mkdir()
            (skill_dir / "evals" / "should_skip.txt").write_text("skip", encoding="utf-8")
            (skill_dir / "references").mkdir()
            (skill_dir / "references" / "keep.txt").write_text("keep", encoding="utf-8")
            dist_dir = root / "dist"

            archive = self.package_skill.package_skill(skill_dir, dist_dir)
            self.assertIsNotNone(archive)

            with zipfile.ZipFile(archive) as zip_file:
                members = set(zip_file.namelist())

        self.assertIn("sample-skill/SKILL.md", members)
        self.assertIn("sample-skill/references/keep.txt", members)
        self.assertNotIn("sample-skill/evals/should_skip.txt", members)

    def test_get_provider_returns_codex_provider_for_codex_models(self):
        provider = self.providers.get_provider("codex")
        self.assertIsInstance(provider, self.providers.CodexProvider)

    def test_parse_gemini_stream_detects_activate_skill(self):
        raw_output = "\n".join(
            [
                '{"type":"message","role":"assistant","content":"Working...","delta":true}',
                '{"type":"tool_use","tool_name":"activate_skill","parameters":{"name":"sample-skill"}}',
                '{"type":"result","status":"success","stats":{"tokens":{"totalTokenCount":42}}}',
            ]
        )

        content, triggered, tokens = self.providers.parse_gemini_stream(raw_output, "sample-skill")

        self.assertTrue(triggered)
        self.assertEqual(content, "Working...")
        self.assertEqual(tokens, 42)

    def test_parse_codex_exec_stream_detects_skill_marker(self):
        raw_output = "\n".join(
            [
                '{"type":"response_item","payload":{"type":"message","content":[{"type":"output_text","text":"done\\nSKILL_TRIGGER: sample-skill"}]}}',
                '{"type":"turn.completed","usage":{"total_tokens":17}}',
            ]
        )

        content, triggered, tokens = self.providers.parse_codex_exec_stream(raw_output, "sample-skill")

        self.assertTrue(triggered)
        self.assertIn("SKILL_TRIGGER: sample-skill", content)
        self.assertEqual(tokens, 17)

    def test_build_model_command_switches_between_hosts(self):
        gemini_cmd, _ = self.improve_description._build_model_command("gemini-2.5-pro")
        codex_cmd, _ = self.improve_description._build_model_command("codex")
        claude_cmd, claude_env = self.improve_description._build_model_command("claude-sonnet")

        self.assertEqual(gemini_cmd[:2], ["gemini", "--prompt"])
        self.assertEqual(codex_cmd[:2], ["codex", "exec"])
        self.assertEqual(claude_cmd[:2], ["claude", "-p"])
        self.assertNotIn("CLAUDECODE", claude_env)


if __name__ == "__main__":
    unittest.main()
