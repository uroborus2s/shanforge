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
FACTORY_SKILL_DELETE_APPROVAL = REPO_ROOT / "scripts" / "factory-skill-delete-approval"
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


class FactorySkillDeleteApprovalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill_draft = load_script_module("factory_skill_draft_for_delete_approval", FACTORY_SKILL_DRAFT)
        cls.skill_approval = load_script_module("factory_skill_approval_for_delete_approval", FACTORY_SKILL_APPROVAL)
        cls.skill_eval = load_script_module("factory_skill_eval_for_delete_approval", FACTORY_SKILL_EVAL)
        cls.skill_promote = load_script_module("factory_skill_promote_for_delete_approval", FACTORY_SKILL_PROMOTE)
        cls.skill_delete_approval = load_script_module(
            "factory_skill_delete_approval", FACTORY_SKILL_DELETE_APPROVAL
        )
        cls.dispatch = load_script_module("factory_dispatch_skill_delete_approval", FACTORY_DISPATCH)

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
            "delete_workspace": self.skill_delete_approval.factory_workspace_root,
            "delete_governance": self.skill_delete_approval.skill_change_governance,
        }
        governance = lambda: {
            "candidate_root": "skills-drafts",
            "require_candidate_first": True,
            "require_eval": True,
            "require_approval_ticket": True,
            "require_first_publish_delete_approval": True,
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
        self.skill_delete_approval.factory_workspace_root = lambda: root
        self.skill_delete_approval.skill_change_governance = governance
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
        self.skill_delete_approval.factory_workspace_root = originals["delete_workspace"]
        self.skill_delete_approval.skill_change_governance = originals["delete_governance"]

    def _create_candidate(self, root: Path, *, name: str, target_skill: str = "") -> dict:
        return self.skill_draft.create_skill_draft(
            name=name,
            summary="为首次发布 skill 删除回退补充审批边界",
            triggers=["当需要删除首次发布的新 skill 时使用。"],
            signals=["新 skill 没有旧版本备份，不能直接恢复。"],
            constraints=["正式 skill 删除前必须保留明确审批记录。"],
            target_skill=target_skill,
            owner="tester",
            project_path=root / "sample-project",
            note="draft candidate",
        )

    def _prepare_promoted_candidate(self, root: Path, draft: dict):
        candidate_name = draft["record"]["name"]
        change_summary = root / draft["record"]["candidate_dir"] / "change-summary.md"
        change_summary.write_text(
            f"# Skill 变更摘要：{candidate_name}\n\n"
            "## 变更动机\n\n"
            "- 需要为首次发布的新 skill 提供删除回退审批边界。\n\n"
            "## 预期收益\n\n"
            "- 删除动作具备明确审批记录，避免裸删。\n\n"
            "## 影响范围\n\n"
            "- 影响候选 skill 的评估、审批、晋升和回退链路。\n\n"
            "## 验证计划\n\n"
            "- 运行 skill-eval、skill-approval、skill-promote 和 skill-delete-approval 回归。\n",
            encoding="utf-8",
        )
        eval_payload = self.skill_eval.evaluate_candidate(candidate_name, owner="qa", note="delete approval test")
        self.assertEqual(eval_payload["status"], "passed")
        ticket = self.skill_approval.request_ticket(candidate_name, owner="approver", note="review")
        self.skill_approval.decide_ticket(ticket["ticket"], decision="approve", owner="lead", note="ok")
        promote_payload = self.skill_promote.promote_candidate(candidate_name, owner="publisher", note="ship")
        self.assertEqual(promote_payload["status"], "promoted")

    def test_delete_approval_request_creates_ticket_for_first_publish_skill(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            originals = self._patch_workspace(root)
            try:
                draft = self._create_candidate(root, name="intent-governance-coach")
                self._prepare_promoted_candidate(root, draft)
                payload = self.skill_delete_approval.request_ticket(draft["record"]["name"], owner="approver", note="delete")
            finally:
                self._restore_workspace(originals)

            state = json.loads((root / ".factory" / "process" / "skill-delete-approvals.json").read_text(encoding="utf-8"))

        self.assertEqual(payload["status"], "pending_approval")
        self.assertTrue(payload["ticket"].startswith("SDA-"))
        self.assertEqual(state["records"][0]["candidate_name"], draft["record"]["name"])
        self.assertEqual(payload["reply_summary"]["action"], "skill-delete-approval")

    def test_delete_approval_rejects_existing_skill_update(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "skills" / "brainstorming").mkdir(parents=True)
            (root / "skills" / "brainstorming" / "SKILL.md").write_text(
                "---\nname: brainstorming\ndescription: >\n  old\n---\n\n# Old\n",
                encoding="utf-8",
            )
            originals = self._patch_workspace(root)
            try:
                draft = self._create_candidate(root, name="brainstorming", target_skill="brainstorming")
                self._prepare_promoted_candidate(root, draft)
                with self.assertRaisesRegex(RuntimeError, "存在旧版本备份"):
                    self.skill_delete_approval.request_ticket(draft["record"]["name"], owner="approver", note="delete")
            finally:
                self._restore_workspace(originals)

    def test_delete_approval_approve_updates_candidate_proposal(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            originals = self._patch_workspace(root)
            try:
                draft = self._create_candidate(root, name="intent-governance-coach")
                self._prepare_promoted_candidate(root, draft)
                ticket = self.skill_delete_approval.request_ticket(draft["record"]["name"], owner="approver", note="delete")
                payload = self.skill_delete_approval.decide_ticket(
                    ticket["ticket"], decision="approve", owner="lead", note="ok"
                )
            finally:
                self._restore_workspace(originals)

            proposal = json.loads((root / draft["record"]["candidate_dir"] / "proposal.json").read_text(encoding="utf-8"))
            approval = json.loads(
                (root / draft["record"]["candidate_dir"] / "delete-approval.json").read_text(encoding="utf-8")
            )

        self.assertEqual(payload["status"], "approved")
        self.assertEqual(proposal["delete_approval_status"], "approved")
        self.assertEqual(approval["decision"], "approve")
        self.assertEqual(approval["mode"], "first_publish_delete")

    def test_dispatch_resolves_skill_delete_approval_alias(self):
        self.assertEqual(self.dispatch.resolve_action("approve-skill-delete"), "skill-delete-approval")
        self.assertEqual(self.dispatch.resolve_action("skill-delete-ticket"), "skill-delete-approval")


if __name__ == "__main__":
    unittest.main()
