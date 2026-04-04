import importlib.util
import json
import tempfile
import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FACTORY_SKILL_DRAFT = REPO_ROOT / "scripts" / "factory-skill-draft"
FACTORY_SKILL_APPROVAL = REPO_ROOT / "scripts" / "factory-skill-approval"
FACTORY_SKILL_EVAL = REPO_ROOT / "scripts" / "factory-skill-eval"
FACTORY_SKILL_PROMOTE = REPO_ROOT / "scripts" / "factory-skill-promote"
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


class FactorySkillPromoteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill_draft = load_script_module("factory_skill_draft_for_promote", FACTORY_SKILL_DRAFT)
        cls.skill_approval = load_script_module("factory_skill_approval_for_promote", FACTORY_SKILL_APPROVAL)
        cls.skill_eval = load_script_module("factory_skill_eval_for_promote", FACTORY_SKILL_EVAL)
        cls.skill_promote = load_script_module("factory_skill_promote", FACTORY_SKILL_PROMOTE)
        cls.dispatch = load_script_module("factory_dispatch_skill_promote", FACTORY_DISPATCH)

    def _patch_workspace(self, root: Path):
        originals = {
            "draft_workspace": self.skill_draft.factory_workspace_root,
            "draft_governance": self.skill_draft.skill_change_governance,
            "approval_workspace": self.skill_approval.factory_workspace_root,
            "approval_governance": self.skill_approval.skill_change_governance,
            "eval_workspace": self.skill_eval.factory_workspace_root,
            "eval_governance": self.skill_eval.skill_change_governance,
            "promote_workspace": self.skill_promote.factory_workspace_root,
            "promote_governance": self.skill_promote.skill_change_governance,
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
        self.skill_approval.factory_workspace_root = lambda: root
        self.skill_approval.skill_change_governance = governance
        self.skill_eval.factory_workspace_root = lambda: root
        self.skill_eval.skill_change_governance = governance
        self.skill_promote.factory_workspace_root = lambda: root
        self.skill_promote.skill_change_governance = governance
        return originals

    def _restore_workspace(self, originals):
        self.skill_draft.factory_workspace_root = originals["draft_workspace"]
        self.skill_draft.skill_change_governance = originals["draft_governance"]
        self.skill_approval.factory_workspace_root = originals["approval_workspace"]
        self.skill_approval.skill_change_governance = originals["approval_governance"]
        self.skill_eval.factory_workspace_root = originals["eval_workspace"]
        self.skill_eval.skill_change_governance = originals["eval_governance"]
        self.skill_promote.factory_workspace_root = originals["promote_workspace"]
        self.skill_promote.skill_change_governance = originals["promote_governance"]

    def _create_candidate(self, root: Path, *, name: str = "intent-governance-coach", target_skill: str = "") -> dict:
        return self.skill_draft.create_skill_draft(
            name=name,
            summary="为 intent 审批和评估收口生成 skill 候选",
            triggers=["当用户要求为 skill 优化生成候选草案时使用。"],
            signals=["重复出现 skill 进化问题但没有候选生成入口。"],
            constraints=["正式 skill 变更前必须保留候选目录。"],
            target_skill=target_skill,
            owner="tester",
            project_path=root / "sample-project",
            note="draft candidate",
        )

    def _approve_candidate(self, draft: dict, owner: str = "lead") -> str:
        ticket = self.skill_approval.request_ticket(draft["record"]["name"], owner="approver", note="review")
        self.skill_approval.decide_ticket(ticket["ticket"], decision="approve", owner=owner, note="ok")
        return ticket["ticket"]

    def _finalize_change_summary(self, root: Path, draft: dict):
        candidate_name = draft["record"]["name"]
        path = root / draft["record"]["candidate_dir"] / "change-summary.md"
        path.write_text(
            f"# Skill 变更摘要：{candidate_name}\n\n"
            "## 变更动机\n\n"
            "- 需要通过正式评估后再进入 skill 晋升。\n\n"
            "## 预期收益\n\n"
            "- 降低手工篡改 eval-report.json 的风险。\n\n"
            "## 影响范围\n\n"
            "- 影响候选 skill 的评估、审批和晋升链路。\n\n"
            "## 验证计划\n\n"
            "- 运行 factory-skill-eval 并继续执行 promote 回归。\n",
            encoding="utf-8",
        )

    def _run_eval(self, root: Path, draft: dict):
        self._finalize_change_summary(root, draft)
        payload = self.skill_eval.evaluate_candidate(draft["record"]["name"], owner="qa", note="promote test")
        self.assertEqual(payload["status"], "passed")

    def test_promote_requires_passed_eval(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            originals = self._patch_workspace(root)
            try:
                draft = self._create_candidate(root)
                failed_eval = self.skill_eval.evaluate_candidate(
                    draft["record"]["name"], owner="qa", note="promote blocked"
                )
                self.assertEqual(failed_eval["status"], "failed")
                candidate_dir = root / draft["record"]["candidate_dir"]
                (candidate_dir / "approval.json").write_text(
                    json.dumps(
                        {
                            "version": 1,
                            "ticket": "SA-test",
                            "decision": "approve",
                            "owner": "lead",
                            "note": "manual gate for promote test",
                            "decided_at": "2026-04-03 10:00:00",
                        },
                        ensure_ascii=False,
                        indent=2,
                    ),
                    encoding="utf-8",
                )
                proposal_path = candidate_dir / "proposal.json"
                proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
                proposal["approval_status"] = "approved"
                proposal["approval_record"] = {"ticket": "SA-test", "decision": "approve", "owner": "lead"}
                proposal_path.write_text(json.dumps(proposal, ensure_ascii=False, indent=2), encoding="utf-8")
                with self.assertRaisesRegex(RuntimeError, "评估结果未通过"):
                    self.skill_promote.promote_candidate(draft["record"]["name"], owner="publisher", note="ship")
            finally:
                self._restore_workspace(originals)

    def test_promote_approved_candidate_writes_official_skill(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            resolved_root = root.resolve()
            originals = self._patch_workspace(root)
            try:
                draft = self._create_candidate(root)
                self._run_eval(root, draft)
                self._approve_candidate(draft)
                payload = self.skill_promote.promote_candidate(draft["record"]["name"], owner="publisher", note="ship")
            finally:
                self._restore_workspace(originals)

            official = resolved_root / "skills" / draft["record"]["name"] / "SKILL.md"
            proposal = json.loads(
                (resolved_root / draft["record"]["candidate_dir"] / "proposal.json").read_text(encoding="utf-8")
            )
            promotion = json.loads(
                (resolved_root / draft["record"]["candidate_dir"] / "promotion.json").read_text(encoding="utf-8")
            )
            state = json.loads(
                (resolved_root / ".factory" / "process" / "skill-promotions.json").read_text(encoding="utf-8")
            )
            official_exists = official.exists()

        self.assertEqual(payload["status"], "promoted")
        self.assertTrue(official_exists)
        self.assertEqual(proposal["promotion_status"], "promoted")
        self.assertEqual(promotion["official_skill_path"], f"skills/{draft['record']['name']}/SKILL.md")
        self.assertEqual(state["records"][0]["candidate_name"], draft["record"]["name"])
        self.assertEqual(payload["reply_summary"]["action"], "skill-promote")

    def test_promote_existing_official_skill_creates_backup(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            resolved_root = root.resolve()
            (root / "skills" / "brainstorming").mkdir(parents=True)
            (root / "skills" / "brainstorming" / "SKILL.md").write_text(
                "---\nname: brainstorming\ndescription: >\n  old\n---\n\n# Old\n",
                encoding="utf-8",
            )
            originals = self._patch_workspace(root)
            try:
                draft = self._create_candidate(root, name="brainstorming", target_skill="brainstorming")
                self._run_eval(root, draft)
                self._approve_candidate(draft)
                payload = self.skill_promote.promote_candidate(draft["record"]["name"], owner="publisher", note="update")
            finally:
                self._restore_workspace(originals)

            backup_dir = resolved_root / draft["record"]["candidate_dir"] / "backups"
            backup_texts = [path.read_text(encoding="utf-8") for path in backup_dir.glob("official-SKILL.before-promote-*.md")]

        self.assertEqual(payload["status"], "promoted")
        self.assertTrue(backup_texts)
        self.assertIn("old", backup_texts[0])

    def test_dispatch_resolves_skill_promote_alias(self):
        self.assertEqual(self.dispatch.resolve_action("promote-skill"), "skill-promote")
        self.assertEqual(self.dispatch.resolve_action("publish-skill"), "skill-promote")


if __name__ == "__main__":
    unittest.main()
