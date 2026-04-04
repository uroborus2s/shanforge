import importlib.util
import json
import tempfile
import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FACTORY_SKILL_DRAFT = REPO_ROOT / "scripts" / "factory-skill-draft"
FACTORY_SKILL_EVAL = REPO_ROOT / "scripts" / "factory-skill-eval"
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


class FactorySkillEvalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill_draft = load_script_module("factory_skill_draft_for_eval", FACTORY_SKILL_DRAFT)
        cls.skill_eval = load_script_module("factory_skill_eval", FACTORY_SKILL_EVAL)
        cls.dispatch = load_script_module("factory_dispatch_skill_eval", FACTORY_DISPATCH)

    def _patch_workspace(self, root: Path):
        originals = {
            "draft_workspace": self.skill_draft.factory_workspace_root,
            "draft_governance": self.skill_draft.skill_change_governance,
            "eval_workspace": self.skill_eval.factory_workspace_root,
            "eval_governance": self.skill_eval.skill_change_governance,
        }
        governance = lambda: {
            "candidate_root": "skills-drafts",
            "require_candidate_first": True,
            "require_eval": True,
            "require_approval_ticket": True,
            "required_artifacts": ["candidate_skill", "eval_report", "approval_record", "change_summary"],
        }
        self.skill_draft.factory_workspace_root = lambda: root
        self.skill_draft.skill_change_governance = governance
        self.skill_eval.factory_workspace_root = lambda: root
        self.skill_eval.skill_change_governance = governance
        return originals

    def _restore_workspace(self, originals):
        self.skill_draft.factory_workspace_root = originals["draft_workspace"]
        self.skill_draft.skill_change_governance = originals["draft_governance"]
        self.skill_eval.factory_workspace_root = originals["eval_workspace"]
        self.skill_eval.skill_change_governance = originals["eval_governance"]

    def _create_candidate(self, root: Path, name: str = "intent-governance-coach") -> dict:
        return self.skill_draft.create_skill_draft(
            name=name,
            summary="为 intent 审批和评估收口生成 skill 候选",
            triggers=["当用户要求为 skill 优化生成候选草案时使用。"],
            signals=["重复出现 skill 进化问题但没有候选生成入口。"],
            constraints=["正式 skill 变更前必须保留候选目录。"],
            target_skill="",
            owner="tester",
            project_path=root / "sample-project",
            note="draft candidate",
        )

    def _finalize_change_summary(self, root: Path, draft: dict):
        path = root / draft["record"]["candidate_dir"] / "change-summary.md"
        path.write_text(
            "# Skill 变更摘要：intent-governance-coach\n\n"
            "## 变更动机\n\n"
            "- 需要为 skill 候选提供正式评估入口。\n\n"
            "## 预期收益\n\n"
            "- 降低手工把 eval-report.json 改成 passed 的风险。\n\n"
            "## 影响范围\n\n"
            "- 影响 skill 候选评估、晋升和回退链路。\n\n"
            "## 验证计划\n\n"
            "- 运行 factory-skill-eval 与后续 promote/rollback 回归。\n",
            encoding="utf-8",
        )

    def test_skill_eval_fails_with_placeholder_change_summary(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            originals = self._patch_workspace(root)
            try:
                draft = self._create_candidate(root)
                payload = self.skill_eval.evaluate_candidate(draft["record"]["name"], owner="qa", note="check")
            finally:
                self._restore_workspace(originals)

            report = json.loads(
                (root.resolve() / draft["record"]["candidate_dir"] / "evals" / "eval-report.json").read_text(encoding="utf-8")
            )

        self.assertEqual(payload["status"], "failed")
        self.assertEqual(report["status"], "failed")
        self.assertEqual(payload["reply_summary"]["action"], "skill-eval")
        self.assertTrue(any(item["name"] == "change_summary" and not item["passed"] for item in report["checks"]))

    def test_skill_eval_passes_after_summary_completed(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            originals = self._patch_workspace(root)
            try:
                draft = self._create_candidate(root)
                self._finalize_change_summary(root, draft)
                payload = self.skill_eval.evaluate_candidate(draft["record"]["name"], owner="qa", note="check")
            finally:
                self._restore_workspace(originals)

            proposal = json.loads(
                (root.resolve() / draft["record"]["candidate_dir"] / "proposal.json").read_text(encoding="utf-8")
            )
            state = json.loads((root.resolve() / ".factory" / "process" / "skill-evals.json").read_text(encoding="utf-8"))

        self.assertEqual(payload["status"], "passed")
        self.assertEqual(proposal["eval_status"], "passed")
        self.assertEqual(state["records"][0]["candidate_name"], draft["record"]["name"])
        self.assertEqual(payload["passed_checks"], payload["total_checks"])

    def test_skill_eval_fails_when_evals_schema_is_broken(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            originals = self._patch_workspace(root)
            try:
                draft = self._create_candidate(root)
                self._finalize_change_summary(root, draft)
                evals_path = root / draft["record"]["candidate_dir"] / "evals" / "evals.json"
                evals = json.loads(evals_path.read_text(encoding="utf-8"))
                evals["evals"][0]["expected_output"] = ""
                evals_path.write_text(json.dumps(evals, ensure_ascii=False, indent=2), encoding="utf-8")
                payload = self.skill_eval.evaluate_candidate(draft["record"]["name"], owner="qa", note="check")
            finally:
                self._restore_workspace(originals)

        self.assertEqual(payload["status"], "failed")
        self.assertTrue(any(item["name"] == "evals_schema" and not item["passed"] for item in payload["checks"]))

    def test_dispatch_resolves_skill_eval_alias(self):
        self.assertEqual(self.dispatch.resolve_action("eval-skill"), "skill-eval")
        self.assertEqual(self.dispatch.resolve_action("evaluate-skill"), "skill-eval")


if __name__ == "__main__":
    unittest.main()
