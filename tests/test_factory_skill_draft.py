import importlib.util
import json
import tempfile
import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FACTORY_SKILL_DRAFT = REPO_ROOT / "scripts" / "factory-skill-draft"
FACTORY_DISPATCH = REPO_ROOT / "scripts" / "factory-dispatch"


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


class FactorySkillDraftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill_draft = load_script_module("factory_skill_draft", FACTORY_SKILL_DRAFT)
        cls.dispatch = load_script_module("factory_dispatch_skill_draft", FACTORY_DISPATCH)

    def _patch_workspace(self, root: Path):
        original_workspace_root = self.skill_draft.factory_workspace_root
        original_governance = self.skill_draft.skill_change_governance
        self.skill_draft.factory_workspace_root = lambda: root
        self.skill_draft.skill_change_governance = lambda: {
            "candidate_root": "skills-drafts",
            "require_candidate_first": True,
            "require_eval": True,
            "require_approval_ticket": True,
            "required_artifacts": ["candidate_skill", "eval_report", "approval_record", "change_summary"],
        }
        return original_workspace_root, original_governance

    def _restore_workspace(self, originals):
        original_workspace_root, original_governance = originals
        self.skill_draft.factory_workspace_root = original_workspace_root
        self.skill_draft.skill_change_governance = original_governance

    def test_create_skill_draft_writes_candidate_artifacts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            originals = self._patch_workspace(root)
            try:
                payload = self.skill_draft.create_skill_draft(
                    name="Intent Governance Coach",
                    summary="为 intent 审批和评估收口生成 skill 候选",
                    triggers=["当用户要求为 skill 优化生成候选草案时使用。"],
                    signals=["重复出现 skill 进化问题但没有候选生成入口。"],
                    constraints=["正式 skill 变更前必须保留候选目录。"],
                    target_skill="",
                    owner="tester",
                    project_path=root / "sample-project",
                    note="draft candidate",
                )
            finally:
                self._restore_workspace(originals)

            draft_dir = root / payload["record"]["candidate_dir"]
            exists = (draft_dir / "SKILL.md").exists()
            proposal = json.loads((draft_dir / "proposal.json").read_text(encoding="utf-8"))
            evals = json.loads((draft_dir / "evals" / "evals.json").read_text(encoding="utf-8"))
            eval_report = json.loads((draft_dir / "evals" / "eval-report.json").read_text(encoding="utf-8"))
            change_summary = (draft_dir / "change-summary.md").read_text(encoding="utf-8")
            skill_md = (draft_dir / "SKILL.md").read_text(encoding="utf-8")

        self.assertEqual(payload["status"], "success")
        self.assertTrue(exists)
        self.assertEqual(proposal["name"], payload["record"]["name"])
        self.assertEqual(evals["skill_name"], payload["record"]["name"])
        self.assertEqual(eval_report["status"], "pending")
        self.assertIn("Skill 变更摘要", change_summary)
        self.assertIn("Candidate Skill Draft", skill_md)
        self.assertEqual(payload["reply_summary"]["action"], "skill-draft")

    def test_create_skill_draft_records_official_target_skill_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "skills" / "brainstorming").mkdir(parents=True)
            (root / "skills" / "brainstorming" / "SKILL.md").write_text("# official\n", encoding="utf-8")
            originals = self._patch_workspace(root)
            try:
                payload = self.skill_draft.create_skill_draft(
                    name="brainstorming",
                    summary="增强 brainstorming 对软件工厂演进的边界控制",
                    triggers=["当需要改进 brainstorming 触发边界时使用。"],
                    signals=["brainstorming 与实现期规则衔接不足。"],
                    constraints=[],
                    target_skill="brainstorming",
                    owner="tester",
                    project_path=root / "sample-project",
                    note="update official skill",
                )
            finally:
                self._restore_workspace(originals)

            proposal = json.loads(
                (root / payload["record"]["candidate_dir"] / "proposal.json").read_text(encoding="utf-8")
            )

        self.assertEqual(proposal["official_skill_path"], "skills/brainstorming/SKILL.md")
        self.assertEqual(payload["record"]["official_skill_path"], "skills/brainstorming/SKILL.md")

    def test_dispatch_resolves_skill_draft_alias(self):
        self.assertEqual(self.dispatch.resolve_action("skill-candidate"), "skill-draft")
        self.assertEqual(self.dispatch.resolve_action("propose-skill"), "skill-draft")


if __name__ == "__main__":
    unittest.main()
