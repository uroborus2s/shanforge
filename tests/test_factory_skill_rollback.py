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
FACTORY_SKILL_ROLLBACK = REPO_ROOT / "scripts" / "factory-skill-rollback"
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


class FactorySkillRollbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill_draft = load_script_module("factory_skill_draft_for_rollback", FACTORY_SKILL_DRAFT)
        cls.skill_approval = load_script_module("factory_skill_approval_for_rollback", FACTORY_SKILL_APPROVAL)
        cls.skill_eval = load_script_module("factory_skill_eval_for_rollback", FACTORY_SKILL_EVAL)
        cls.skill_promote = load_script_module("factory_skill_promote_for_rollback", FACTORY_SKILL_PROMOTE)
        cls.skill_delete_approval = load_script_module(
            "factory_skill_delete_approval_for_rollback", FACTORY_SKILL_DELETE_APPROVAL
        )
        cls.skill_rollback = load_script_module("factory_skill_rollback", FACTORY_SKILL_ROLLBACK)
        cls.dispatch = load_script_module("factory_dispatch_skill_rollback", FACTORY_DISPATCH)

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
            "rollback_workspace": self.skill_rollback.factory_workspace_root,
            "rollback_governance": self.skill_rollback.skill_change_governance,
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
        self.skill_rollback.factory_workspace_root = lambda: root
        self.skill_rollback.skill_change_governance = governance
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
        self.skill_rollback.factory_workspace_root = originals["rollback_workspace"]
        self.skill_rollback.skill_change_governance = originals["rollback_governance"]

    def _create_candidate(self, root: Path, *, name: str = "brainstorming", target_skill: str = "brainstorming") -> dict:
        return self.skill_draft.create_skill_draft(
            name=name,
            summary="增强 skill 边界约束",
            triggers=["当需要演进正式 skill 时使用。"],
            signals=["正式 skill 需要候选治理与回退链路。"],
            constraints=["正式 skill 变更前必须保留候选目录。"],
            target_skill=target_skill,
            owner="tester",
            project_path=root / "sample-project",
            note="draft candidate",
        )

    def _approve_and_pass_eval(self, root: Path, draft: dict):
        candidate_name = draft["record"]["name"]
        change_summary = root / draft["record"]["candidate_dir"] / "change-summary.md"
        change_summary.write_text(
            f"# Skill 变更摘要：{candidate_name}\n\n"
            "## 变更动机\n\n"
            "- 需要为已有正式 skill 提供安全回退链路。\n\n"
            "## 预期收益\n\n"
            "- 发布失败时可以恢复到旧版本。\n\n"
            "## 影响范围\n\n"
            "- 影响 skill 晋升与回退链路。\n\n"
            "## 验证计划\n\n"
            "- 运行 factory-skill-eval、promote 和 rollback 回归。\n",
            encoding="utf-8",
        )
        payload = self.skill_eval.evaluate_candidate(candidate_name, owner="qa", note="rollback test")
        self.assertEqual(payload["status"], "passed")
        ticket = self.skill_approval.request_ticket(draft["record"]["name"], owner="approver", note="review")
        self.skill_approval.decide_ticket(ticket["ticket"], decision="approve", owner="lead", note="ok")

    def test_rollback_new_skill_without_backup_is_blocked(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            originals = self._patch_workspace(root)
            try:
                draft = self.skill_draft.create_skill_draft(
                    name="intent-governance-coach",
                    summary="新增 skill",
                    triggers=["当需要新增 skill 时使用。"],
                    signals=["需要新能力。"],
                    constraints=["正式 skill 变更前必须保留候选目录。"],
                    target_skill="",
                    owner="tester",
                    project_path=root / "sample-project",
                    note="draft candidate",
                )
                self._approve_and_pass_eval(root, draft)
                self.skill_promote.promote_candidate(draft["record"]["name"], owner="publisher", note="ship")
                with self.assertRaisesRegex(RuntimeError, "需要先通过 `skill-delete-approval`"):
                    self.skill_rollback.rollback_candidate(draft["record"]["name"], owner="rollbacker", note="revert")
            finally:
                self._restore_workspace(originals)

    def test_rollback_new_skill_after_delete_approval_removes_official_skill(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            resolved_root = root.resolve()
            originals = self._patch_workspace(root)
            try:
                draft = self.skill_draft.create_skill_draft(
                    name="intent-governance-coach",
                    summary="新增 skill",
                    triggers=["当需要新增 skill 时使用。"],
                    signals=["需要新能力。"],
                    constraints=["正式 skill 变更前必须保留候选目录。"],
                    target_skill="",
                    owner="tester",
                    project_path=root / "sample-project",
                    note="draft candidate",
                )
                self._approve_and_pass_eval(root, draft)
                self.skill_promote.promote_candidate(draft["record"]["name"], owner="publisher", note="ship")
                ticket = self.skill_delete_approval.request_ticket(
                    draft["record"]["name"], owner="approver", note="delete"
                )
                self.skill_delete_approval.decide_ticket(ticket["ticket"], decision="approve", owner="lead", note="ok")
                payload = self.skill_rollback.rollback_candidate(draft["record"]["name"], owner="rollbacker", note="revert")
            finally:
                self._restore_workspace(originals)

            official = resolved_root / "skills" / draft["record"]["name"] / "SKILL.md"
            rollback = json.loads(
                (resolved_root / draft["record"]["candidate_dir"] / "rollback.json").read_text(encoding="utf-8")
            )
            proposal = json.loads(
                (resolved_root / draft["record"]["candidate_dir"] / "proposal.json").read_text(encoding="utf-8")
            )

        self.assertEqual(payload["status"], "rolled_back")
        self.assertFalse(official.exists())
        self.assertEqual(rollback["rollback_mode"], "delete_first_publish")
        self.assertTrue(rollback["delete_approval_ticket"].startswith("SDA-"))
        self.assertEqual(proposal["rollback_status"], "rolled_back")

    def test_rollback_restores_previous_official_skill(self):
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
                draft = self._create_candidate(root)
                self._approve_and_pass_eval(root, draft)
                self.skill_promote.promote_candidate(draft["record"]["name"], owner="publisher", note="ship")
                payload = self.skill_rollback.rollback_candidate(draft["record"]["name"], owner="rollbacker", note="revert")
            finally:
                self._restore_workspace(originals)

            official_text = (resolved_root / "skills" / "brainstorming" / "SKILL.md").read_text(encoding="utf-8")
            rollback = json.loads(
                (resolved_root / draft["record"]["candidate_dir"] / "rollback.json").read_text(encoding="utf-8")
            )
            proposal = json.loads(
                (resolved_root / draft["record"]["candidate_dir"] / "proposal.json").read_text(encoding="utf-8")
            )
            state = json.loads((resolved_root / ".factory" / "process" / "skill-rollbacks.json").read_text(encoding="utf-8"))

        self.assertEqual(payload["status"], "rolled_back")
        self.assertIn("old", official_text)
        self.assertEqual(rollback["candidate_name"], "brainstorming")
        self.assertEqual(proposal["rollback_status"], "rolled_back")
        self.assertEqual(state["records"][0]["candidate_name"], "brainstorming")
        self.assertEqual(payload["reply_summary"]["action"], "skill-rollback")

    def test_dispatch_resolves_skill_rollback_alias(self):
        self.assertEqual(self.dispatch.resolve_action("rollback-skill"), "skill-rollback")
        self.assertEqual(self.dispatch.resolve_action("revert-skill"), "skill-rollback")


if __name__ == "__main__":
    unittest.main()
