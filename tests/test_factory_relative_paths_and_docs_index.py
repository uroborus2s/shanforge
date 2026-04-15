import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from importlib.machinery import SourceFileLoader
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FACTORY_PROJECT_COMPRESS = REPO_ROOT / "scripts" / "factory-project-compress"
FACTORY_INIT = REPO_ROOT / "scripts" / "factory-init"
FACTORY_AGENT_SESSION = REPO_ROOT / "scripts" / "factory-agent-session"
FACTORY_DISPATCH = REPO_ROOT / "scripts" / "factory-dispatch"
FACTORY_CHAT_BOOTSTRAP = REPO_ROOT / "scripts" / "factory-chat-bootstrap"
FACTORY_FRONTEND_CAPABILITIES = REPO_ROOT / "scripts" / "factory-frontend-capabilities"
FACTORY_INTENT_RESOLVER = REPO_ROOT / "scripts" / "factory-intent-resolver"
FACTORY_INTENT_APPROVAL = REPO_ROOT / "scripts" / "factory-intent-approval"
FACTORY_INTENT_EVAL = REPO_ROOT / "scripts" / "factory-intent-eval"
FACTORY_MULTI_AGENT_BOARD = REPO_ROOT / "scripts" / "factory-multi-agent-board"
FACTORY_ROLE_ASSIGN = REPO_ROOT / "scripts" / "factory-role-assign"
LEGACY_ROOT = str(Path("/") / "Users" / "uroborus" / "shanforge")
EXAMPLE_PROJECT = Path("/tmp/example-project")


def load_script_module(module_name: str, script_path: Path):
    script_dir = str(script_path.parent)
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    loader = SourceFileLoader(module_name, str(script_path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FactoryRelativePathAndDocsIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project_compress = load_script_module("factory_project_compress", FACTORY_PROJECT_COMPRESS)
        cls.factory_init = load_script_module("factory_init", FACTORY_INIT)
        cls.agent_session = load_script_module("factory_agent_session", FACTORY_AGENT_SESSION)
        cls.dispatch = load_script_module("factory_dispatch", FACTORY_DISPATCH)
        cls.chat_bootstrap = load_script_module("factory_chat_bootstrap", FACTORY_CHAT_BOOTSTRAP)
        cls.frontend_capabilities = load_script_module("factory_frontend_capabilities", FACTORY_FRONTEND_CAPABILITIES)
        cls.intent_resolver = load_script_module("factory_intent_resolver", FACTORY_INTENT_RESOLVER)
        cls.intent_approval = load_script_module("factory_intent_approval", FACTORY_INTENT_APPROVAL)
        cls.intent_eval = load_script_module("factory_intent_eval", FACTORY_INTENT_EVAL)
        cls.multi_agent_board = load_script_module("factory_multi_agent_board", FACTORY_MULTI_AGENT_BOARD)
        cls.role_assign = load_script_module("factory_role_assign", FACTORY_ROLE_ASSIGN)
        cls.factory_core = sys.modules["factory_core"]
        cls.example_project_resolved = EXAMPLE_PROJECT.resolve()
        cls.expected_runtime_protocol = Path(
            os.path.relpath(
                REPO_ROOT / "skills" / "software-factory-cli" / "references" / "ai-runtime-protocol.md",
                cls.example_project_resolved,
            )
        ).as_posix()
        cls.expected_role_charter = Path(
            os.path.relpath(
                REPO_ROOT / "skills" / "software-factory-cli" / "references" / "ai-role-charter.md",
                cls.example_project_resolved,
            )
        ).as_posix()
        cls.expected_dispatch = Path(
            os.path.relpath(REPO_ROOT / "scripts" / "factory-dispatch", cls.example_project_resolved)
        ).as_posix()
        cls.expected_docs_index = Path(
            os.path.relpath(REPO_ROOT / "docs" / "index.md", cls.example_project_resolved)
        ).as_posix()
        cls.expected_brainstorm_skill = Path(
            os.path.relpath(REPO_ROOT / "skills" / "brainstorming" / "SKILL.md", cls.example_project_resolved)
        ).as_posix()

    def set_intent_approval_root(self, root: Path) -> None:
        env_key = self.factory_core.INTENT_APPROVAL_ROOT_ENV
        previous = os.environ.get(env_key)
        os.environ[env_key] = str(root)

        def restore() -> None:
            if previous is None:
                os.environ.pop(env_key, None)
            else:
                os.environ[env_key] = previous

        self.addCleanup(restore)

    def set_intent_workspace_root(self, root: Path) -> None:
        previous = self.intent_resolver.factory_workspace_root
        self.intent_resolver.factory_workspace_root = lambda: root

        def restore() -> None:
            self.intent_resolver.factory_workspace_root = previous

        self.addCleanup(restore)

    def create_skill_candidate_state(
        self,
        project_root: Path,
        *,
        name: str,
        eval_status: str = "",
        approval_status: str = "",
        promotion_status: str = "",
        rollback_status: str = "",
        delete_approval_status: str = "",
        has_backup: bool = False,
        delete_approval_decision: str = "",
    ) -> Path:
        candidate_dir = project_root / "skills-drafts" / name
        candidate_dir.mkdir(parents=True)
        proposal = {
            "version": 1,
            "name": name,
            "summary": f"{name} summary",
            "target_skill": "",
            "official_skill_path": f"skills/{name}/SKILL.md",
            "eval_status": eval_status,
            "approval_status": approval_status,
            "promotion_status": promotion_status,
            "rollback_status": rollback_status,
            "delete_approval_status": delete_approval_status,
        }
        (candidate_dir / "proposal.json").write_text(json.dumps(proposal, ensure_ascii=False, indent=2), encoding="utf-8")
        if promotion_status:
            promotion = {
                "version": 1,
                "id": "SP-test",
                "candidate_name": name,
                "official_skill_path": f"skills/{name}/SKILL.md",
                "backup_path": f"skills-drafts/{name}/backups/official-SKILL.before-promote.md" if has_backup else "",
            }
            (candidate_dir / "promotion.json").write_text(
                json.dumps(promotion, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            skill_dir = project_root / "skills" / name
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(f"---\nname: {name}\n---\n\n# {name}\n", encoding="utf-8")
            if has_backup:
                backup_path = project_root / promotion["backup_path"]
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                backup_path.write_text(f"---\nname: {name}\n---\n\n# old {name}\n", encoding="utf-8")
        if delete_approval_decision:
            delete_approval = {
                "version": 1,
                "ticket": "SDA-test",
                "decision": delete_approval_decision,
                "owner": "lead",
                "mode": "first_publish_delete",
                "official_skill_path": f"skills/{name}/SKILL.md",
            }
            (candidate_dir / "delete-approval.json").write_text(
                json.dumps(delete_approval, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        return candidate_dir

    def test_project_compress_agents_md_uses_relative_workspace_paths(self):
        output = self.project_compress.build_agents_md(
            EXAMPLE_PROJECT,
            {"project_name": "example-project"},
        )

        self.assertIn(f"`{self.expected_runtime_protocol}`", output)
        self.assertIn(f"`{self.expected_role_charter}`", output)
        self.assertIn("项目根目录：`.`", output)
        self.assertNotIn("`/Users/", output)
        self.assertNotIn(LEGACY_ROOT, output)

    def test_project_compress_gemini_md_uses_relative_workspace_paths(self):
        output = self.project_compress.build_gemini_md(
            EXAMPLE_PROJECT,
            {"project_name": "example-project"},
        )

        self.assertIn(f"`{self.expected_runtime_protocol}`", output)
        self.assertIn(f"`{self.expected_role_charter}`", output)
        self.assertIn("项目根目录：`.`", output)
        self.assertNotIn("`/Users/", output)
        self.assertNotIn(LEGACY_ROOT, output)

    def test_project_compress_runtime_brief_uses_relative_dispatch_path(self):
        output = self.project_compress.build_runtime_brief(
            EXAMPLE_PROJECT,
            {
                "project_name": "example-project",
                "stage": "MAINTENANCE",
                "active_mode": "DEFAULT",
                "stack": "node",
            },
            owner="tester",
            note="path-regression",
        )

        self.assertIn(f"python3 {self.expected_dispatch}", output)
        self.assertIn('--project "."', output)
        self.assertNotIn("python3 /Users/", output)
        self.assertNotIn(LEGACY_ROOT, output)

    def test_agent_session_recommended_commands_use_relative_dispatch_path(self):
        commands = self.agent_session.recommended_commands(
            EXAMPLE_PROJECT,
            "MAINTENANCE",
            "tester",
            "focus",
            0,
        )

        command_blob = "\n".join(commands)
        self.assertIn(f"python3 {self.expected_dispatch}", command_blob)
        self.assertIn('--project "."', command_blob)
        self.assertNotIn("python3 /Users/", command_blob)
        self.assertNotIn(LEGACY_ROOT, command_blob)

    def test_dispatch_rejects_removed_docs_upgrade_aliases(self):
        with self.assertRaises(RuntimeError):
            self.dispatch.resolve_action("docs-upgrade")
        with self.assertRaises(RuntimeError):
            self.dispatch.resolve_action("upgrade-docs-standard")
        with self.assertRaises(RuntimeError):
            self.dispatch.resolve_action("docs-upgrade-batch")
        self.assertEqual(self.dispatch.resolve_action("frontend"), "frontend-capabilities")
        self.assertEqual(self.dispatch.resolve_action("intent"), "intent-resolver")
        self.assertEqual(self.dispatch.resolve_action("intent-replay"), "intent-eval")
        self.assertEqual(self.dispatch.resolve_action("intent-approve"), "intent-approval")
        self.assertEqual(self.dispatch.resolve_action("approve-skill-delete"), "skill-delete-approval")

    def test_dispatch_does_not_consume_subcommand_list_flag(self):
        previous_argv = sys.argv[:]
        try:
            sys.argv = [str(FACTORY_DISPATCH), "intent-approval", "--list"]
            args, passthrough = self.dispatch.parse_args()
        finally:
            sys.argv = previous_argv

        self.assertEqual(args.action, "intent-approval")
        self.assertFalse(args.list_actions)
        self.assertEqual(passthrough, ["--list"])

    def test_dispatch_loads_registered_action_specs(self):
        registry = self.dispatch.load_action_registry()

        self.assertIn("state-doctor", registry)
        self.assertEqual(registry["state-doctor"]["risk_level"], "L0")
        self.assertNotIn("docs-standard-upgrade", registry)

    def test_dispatch_action_policy_uses_registry_and_safe_default(self):
        policy = self.dispatch.action_policy("state-doctor")
        default_policy = self.dispatch.action_policy("non-existent-action")

        self.assertEqual(policy["risk_level"], "L0")
        self.assertEqual(policy["approval"], "auto")
        self.assertEqual(default_policy["risk_level"], "L3")
        self.assertEqual(default_policy["approval"], "explicit_confirm")

    def test_intent_resolver_recommends_init_for_empty_project(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.intent_resolver.resolve_intent("初始化这个空目录项目", Path(temp_dir), tool="codex")

        self.assertEqual(result["primary"]["action"], "init")
        self.assertEqual(result["primary"]["policy"]["risk_level"], "L2")

    def test_intent_resolver_recommends_state_doctor_for_unmanaged_project(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "README.md").write_text("# Legacy Project\n", encoding="utf-8")

            result = self.intent_resolver.resolve_intent("先接管这个历史项目", project_root, tool="codex")

        self.assertEqual(result["primary"]["action"], "state-doctor")
        self.assertFalse(result["primary"]["blocked"])

    def test_intent_resolver_prefers_state_doctor_for_managed_docs_request(self):
        result = self.intent_resolver.resolve_intent("把 docs 刷新到最新规范并重建目录", REPO_ROOT, tool="opencode")

        self.assertEqual(result["primary"]["action"], "state-doctor")
        self.assertEqual(result["frontend"]["id"], "opencode")

    def test_intent_resolver_uses_state_doctor_for_generic_next_step(self):
        result = self.intent_resolver.resolve_intent("继续下一步", REPO_ROOT, tool="gemini")

        self.assertEqual(result["primary"]["action"], "state-doctor")
        self.assertEqual(result["primary"]["policy"]["approval"], "auto")

    def test_intent_resolver_selects_command_profile_for_design_kickoff_intent(self):
        result = self.intent_resolver.resolve_intent("开始设计阶段并生成会话入口", REPO_ROOT, tool="codex")

        self.assertEqual(result["primary"]["action"], "command-profiles")
        self.assertEqual(result["primary"]["selected_profile"], "design-kickoff")

    def test_intent_resolver_escalates_workflow_backed_profile_policy(self):
        result = self.intent_resolver.resolve_intent("今天收尾并生成会话入口", REPO_ROOT, tool="codex")

        self.assertEqual(result["primary"]["action"], "command-profiles")
        self.assertEqual(result["primary"]["selected_profile"], "daily-close")
        self.assertEqual(result["primary"]["policy"]["risk_level"], "L2")
        self.assertEqual(result["primary"]["policy"]["approval"], "summary_confirm")

    def test_intent_resolver_selects_workflow_runner_for_explicit_workflow_intent(self):
        result = self.intent_resolver.resolve_intent("执行 daily close workflow", REPO_ROOT, tool="codex")

        self.assertEqual(result["primary"]["action"], "workflow-runner")
        self.assertEqual(result["primary"]["selected_workflow"], "daily_close")

    def test_intent_resolver_selects_skill_eval_for_candidate_next_step(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            self.set_intent_workspace_root(project_root)
            self.create_skill_candidate_state(project_root, name="intent-governance-coach")

            result = self.intent_resolver.resolve_intent("继续推进这个 skill intent-governance-coach", project_root, tool="codex")

        self.assertEqual(result["primary"]["action"], "skill-eval")
        self.assertEqual(result["primary"]["selected_skill_operation"], "eval")
        self.assertEqual(result["primary"]["selected_skill_candidate"], "skills-drafts/intent-governance-coach")

    def test_intent_resolver_keeps_skill_boundary_when_candidate_missing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "managed-project"
            self.factory_init.initialize_project(
                target=project_root,
                project_name="managed-project",
                idea="govern skills",
                stack="python",
                owner="tester",
                force=False,
            )
            self.set_intent_workspace_root(project_root)

            result = self.intent_resolver.resolve_intent("撤回刚发布的新 skill intent-governance-coach", project_root, tool="codex")

        self.assertEqual(result["primary"]["action"], "skill-delete-approval")
        self.assertEqual(result["primary"]["selected_skill_operation"], "delete_first_publish")
        self.assertIn("skills-drafts", " ".join(result["primary"]["blocked"]))

    def test_intent_resolver_selects_skill_approval_for_passed_candidate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            self.set_intent_workspace_root(project_root)
            self.create_skill_candidate_state(
                project_root,
                name="intent-governance-coach",
                eval_status="passed",
            )

            result = self.intent_resolver.resolve_intent("让这个 skill 进入审批 intent-governance-coach", project_root, tool="codex")

        self.assertEqual(result["primary"]["action"], "skill-approval")
        self.assertEqual(result["primary"]["selected_skill_operation"], "approval_request")

    def test_intent_resolver_selects_skill_promote_for_approved_candidate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            self.set_intent_workspace_root(project_root)
            self.create_skill_candidate_state(
                project_root,
                name="intent-governance-coach",
                eval_status="passed",
                approval_status="approved",
            )

            result = self.intent_resolver.resolve_intent("正式发布这个 skill intent-governance-coach", project_root, tool="codex")

        self.assertEqual(result["primary"]["action"], "skill-promote")
        self.assertEqual(result["primary"]["selected_skill_operation"], "promote")

    def test_intent_resolver_selects_skill_delete_approval_for_first_publish_withdraw(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            self.set_intent_workspace_root(project_root)
            self.create_skill_candidate_state(
                project_root,
                name="intent-governance-coach",
                eval_status="passed",
                approval_status="approved",
                promotion_status="promoted",
            )

            result = self.intent_resolver.resolve_intent("撤回刚发布的新 skill intent-governance-coach", project_root, tool="codex")

        self.assertEqual(result["primary"]["action"], "skill-delete-approval")
        self.assertEqual(result["primary"]["selected_skill_operation"], "delete_first_publish")

    def test_intent_resolver_switches_to_skill_rollback_after_delete_approval(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            self.set_intent_workspace_root(project_root)
            self.create_skill_candidate_state(
                project_root,
                name="intent-governance-coach",
                eval_status="passed",
                approval_status="approved",
                promotion_status="promoted",
                delete_approval_status="approved",
                delete_approval_decision="approve",
            )

            result = self.intent_resolver.resolve_intent("撤回刚发布的新 skill intent-governance-coach", project_root, tool="codex")

        self.assertEqual(result["primary"]["action"], "skill-rollback")
        self.assertEqual(result["primary"]["selected_skill_operation"], "delete_first_publish")

    def test_intent_resolver_builds_execution_plan_for_profile(self):
        result = self.intent_resolver.resolve_intent("开始设计阶段并生成会话入口", REPO_ROOT, tool="codex")
        plan = self.intent_resolver.build_execution_plan(
            result,
            owner="tester",
            note="kickoff",
            focus="继续设计",
            strict=True,
        )

        self.assertEqual(plan["script_name"], "factory-command-profiles")
        self.assertEqual(plan["arguments"][0], "design-kickoff")
        self.assertIn("--strict", plan["arguments"])

    def test_intent_resolver_safe_execution_reports_error_for_unmanaged_project(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "README.md").write_text("# Legacy Project\n", encoding="utf-8")

            result = self.intent_resolver.resolve_intent("接管这个历史项目", project_root, tool="codex")
            execution = self.intent_resolver.execute_primary_safe(
                result,
                owner="tester",
                note="",
                focus="",
                strict=False,
            )

        self.assertEqual(result["primary"]["action"], "state-doctor")
        self.assertEqual(execution["status"], "error")

    def test_intent_resolver_request_approval_for_workflow_backed_profile(self):
        with tempfile.TemporaryDirectory() as control_dir:
            self.set_intent_approval_root(Path(control_dir))
            result = self.intent_resolver.resolve_intent("今天收尾并生成会话入口", REPO_ROOT, tool="codex")
            approval = self.intent_resolver.request_primary_approval(
                result,
                owner="tester",
                note="close day",
                focus="handover",
                strict=False,
            )

        self.assertEqual(approval["status"], "pending_approval")
        self.assertEqual(approval["plan"]["script_name"], "factory-command-profiles")
        self.assertEqual(approval["plan"]["arguments"][0], "daily-close")
        self.assertEqual(approval["record"]["ownership"]["role_id"], "release-manager")
        self.assertIn(".factory", approval["record"]["ownership"]["write_targets"])
        self.assertIn("docs", approval["record"]["ownership"]["write_targets"])

    def test_intent_resolver_request_approval_creates_ticket_for_init(self):
        with tempfile.TemporaryDirectory() as temp_dir, tempfile.TemporaryDirectory() as control_dir:
            project_root = Path(temp_dir)
            self.set_intent_approval_root(Path(control_dir))

            result = self.intent_resolver.resolve_intent("初始化这个空目录项目", project_root, tool="codex")
            approval = self.intent_resolver.request_primary_approval(
                result,
                owner="tester",
                note="create managed project",
                focus="bootstrap",
                strict=False,
            )

            state_path = Path(control_dir) / ".factory" / "process" / "intent-approvals.json"
            payload = json.loads(state_path.read_text(encoding="utf-8"))

        self.assertEqual(approval["status"], "pending_approval")
        self.assertTrue(approval["ticket"].startswith("IA-"))
        self.assertEqual(payload["records"][0]["action"], "init")
        self.assertEqual(payload["records"][0]["status"], "pending")

    def test_intent_approval_can_approve_and_execute_init_ticket(self):
        with tempfile.TemporaryDirectory() as temp_dir, tempfile.TemporaryDirectory() as control_dir:
            project_root = Path(temp_dir)
            self.set_intent_approval_root(Path(control_dir))

            result = self.intent_resolver.resolve_intent("初始化这个空目录项目", project_root, tool="codex")
            approval = self.intent_resolver.request_primary_approval(
                result,
                owner="tester",
                note="create managed project",
                focus="bootstrap",
                strict=False,
            )
            execution = self.intent_approval.decide_ticket(
                approval["ticket"],
                decision="approve",
                owner="approver",
                note="looks good",
            )
            project_config_exists = (project_root / ".factory" / "project.json").exists()
            payload = json.loads(
                (Path(control_dir) / ".factory" / "process" / "intent-approvals.json").read_text(encoding="utf-8")
            )

        self.assertEqual(execution["status"], "executed")
        self.assertTrue(project_config_exists)
        self.assertEqual(payload["records"][0]["status"], "executed")
        self.assertEqual(payload["records"][0]["decision_owner"], "approver")

    def test_intent_approval_can_reject_ticket(self):
        with tempfile.TemporaryDirectory() as temp_dir, tempfile.TemporaryDirectory() as control_dir:
            project_root = Path(temp_dir)
            self.set_intent_approval_root(Path(control_dir))

            result = self.intent_resolver.resolve_intent("初始化这个空目录项目", project_root, tool="codex")
            approval = self.intent_resolver.request_primary_approval(
                result,
                owner="tester",
                note="create managed project",
                focus="bootstrap",
                strict=False,
            )
            rejection = self.intent_approval.decide_ticket(
                approval["ticket"],
                decision="reject",
                owner="approver",
                note="wait for more context",
            )
            project_config_exists = (project_root / ".factory" / "project.json").exists()
            payload = json.loads(
                (Path(control_dir) / ".factory" / "process" / "intent-approvals.json").read_text(encoding="utf-8")
            )

        self.assertEqual(rejection["status"], "rejected")
        self.assertFalse(project_config_exists)
        self.assertEqual(payload["records"][0]["status"], "rejected")
        self.assertEqual(payload["records"][0]["decision_note"], "wait for more context")

    def test_intent_approval_blocks_ticket_when_frozen_ownership_conflicts(self):
        with tempfile.TemporaryDirectory() as temp_dir, tempfile.TemporaryDirectory() as control_dir:
            project_root = Path(temp_dir) / "managed-project"
            self.factory_init.initialize_project(
                target=project_root,
                project_name="managed-project",
                idea="ship docs",
                stack="python",
                owner="tester",
                force=False,
            )
            config = self.factory_core.load_project_config(project_root)
            self.factory_core.ensure_role_catalog(config)
            self.factory_core.set_current_role_assignment(
                config,
                "coordinator",
                {
                    "owner": "planner",
                    "tool": "codex",
                    "items": [],
                    "status": "进行中",
                    "focus": "plan",
                    "note": "",
                    "write_targets": [".factory"],
                    "assigned_at": "2026-04-02 10:00:00",
                },
            )
            self.factory_core.save_project_config(project_root, config)
            self.set_intent_approval_root(Path(control_dir))

            result = self.intent_resolver.resolve_intent("今天收尾并生成会话入口", project_root, tool="codex")
            approval = self.intent_resolver.request_primary_approval(
                result,
                owner="tester",
                note="close day",
                focus="handover",
                strict=False,
            )
            execution = self.intent_approval.decide_ticket(
                approval["ticket"],
                decision="approve",
                owner="approver",
                note="check ownership",
            )

        self.assertEqual(execution["status"], "blocked_conflict")
        self.assertIn("写集冲突", execution["summary"])
        self.assertEqual(execution["record"]["ownership_check"]["status"], "blocked_conflict")
        self.assertIsNone(execution["step"])

    def test_intent_approval_guard_binds_frozen_ownership_to_role_assignment(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "managed-project"
            self.factory_init.initialize_project(
                target=project_root,
                project_name="managed-project",
                idea="ship docs",
                stack="python",
                owner="tester",
                force=False,
            )
            result = self.intent_resolver.resolve_intent("今天收尾并生成会话入口", project_root, tool="codex")
            approval = self.intent_resolver.request_primary_approval(
                result,
                owner="tester",
                note="close day",
                focus="handover",
                strict=False,
            )

            guard = self.intent_approval.enforce_ownership_guard(approval["record"])
            config = self.factory_core.load_project_config(project_root)
            assignment = self.factory_core.current_role_assignment(config, "release-manager")

        self.assertEqual(guard["status"], "ready")
        self.assertEqual(assignment["owner"], "tester")
        self.assertIn(".factory", assignment["write_targets"])
        self.assertIn("docs", assignment["write_targets"])

    def test_intent_eval_loads_default_cases(self):
        cases = self.intent_eval.load_cases(self.intent_eval.DEFAULT_CASES_PATH)

        self.assertGreaterEqual(len(cases), 13)
        ids = {case["id"] for case in cases}
        self.assertIn("intent-managed-next-step", ids)
        self.assertIn("intent-managed-daily-workflow", ids)
        self.assertIn("intent-managed-daily-profile", ids)
        self.assertIn("intent-skill-without-candidate", ids)
        self.assertIn("intent-skill-delete-approval", ids)
        self.assertIn("intent-skill-delete-approved-rollback", ids)

    def test_intent_eval_evaluates_cases_with_full_pass(self):
        cases = self.intent_eval.load_cases(self.intent_eval.DEFAULT_CASES_PATH)
        summary = self.intent_eval.evaluate_cases(cases)

        self.assertEqual(summary["failed"], 0)
        self.assertEqual(summary["passed"], summary["total"])
        self.assertEqual(summary["status"], "success")
        self.assertEqual(summary["reply_summary"]["action"], "intent-eval")
        labels = {item["label"] for item in summary["reply_summary"]["items"]}
        self.assertIn("命中率", labels)

    def test_intent_eval_reports_mismatch_for_wrong_expectation(self):
        broken_case = {
            "id": "broken",
            "intent": "继续下一步",
            "fixture": "managed_project",
            "tool": "codex",
            "expected": {"action": "init"},
        }

        result = self.intent_eval.evaluate_case(broken_case)

        self.assertFalse(result["passed"])
        self.assertTrue(any("expected action" in item for item in result["mismatches"]))

    def test_factory_core_loads_reply_policy_and_skill_change_governance(self):
        policy = self.factory_core.load_reply_policy()
        skill_changes = self.factory_core.skill_change_governance()

        self.assertIn("intent-resolver", policy["actions"])
        self.assertTrue(skill_changes["require_candidate_first"])
        self.assertTrue(skill_changes["require_approval_ticket"])

    def test_intent_resolver_provides_approval_guidance_for_l2_actions(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "managed-project"
            self.factory_init.initialize_project(
                target=project_root,
                project_name="managed-project",
                idea="ship docs",
                stack="python",
                owner="tester",
                force=False,
            )

            result = self.intent_resolver.resolve_intent("今天收尾并生成会话入口", project_root, tool="codex")

        self.assertEqual(result["primary"]["action"], "command-profiles")
        self.assertTrue(result["approval_guidance"]["ticket_required"])
        self.assertIn("--request-approval", result["approval_guidance"]["next_actions"][0])
        labels = {item["label"] for item in result["reply_summary"]["items"]}
        self.assertIn("主推荐动作", labels)

    def test_intent_approval_payload_contains_reply_summary(self):
        with tempfile.TemporaryDirectory() as temp_dir, tempfile.TemporaryDirectory() as control_dir:
            project_root = Path(temp_dir)
            self.set_intent_approval_root(Path(control_dir))

            result = self.intent_resolver.resolve_intent("初始化这个空目录项目", project_root, tool="codex")
            approval = self.intent_resolver.request_primary_approval(
                result,
                owner="tester",
                note="create managed project",
                focus="bootstrap",
                strict=False,
            )
            execution = self.intent_approval.decide_ticket(
                approval["ticket"],
                decision="approve",
                owner="approver",
                note="looks good",
            )

        self.assertEqual(execution["reply_summary"]["action"], "intent-approval")
        labels = {item["label"] for item in execution["reply_summary"]["items"]}
        self.assertIn("ownership 校验", labels)

    def test_multi_agent_board_marks_high_risk_recommended_commands(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "managed-project"
            self.factory_init.initialize_project(
                target=project_root,
                project_name="managed-project",
                idea="ship docs",
                stack="python",
                owner="tester",
                force=False,
            )
            config = self.factory_core.load_project_config(project_root)
            self.factory_core.ensure_role_catalog(config)
            active_roles = self.factory_core.active_roles_for_stage(config, config.get("stage", ""))
            grouped = self.factory_core.group_items_by_role(config, [])

            summary = self.multi_agent_board.summary_markdown(
                config,
                "审批治理",
                [],
                [],
                active_roles,
                grouped,
                project_root,
                "tester",
                3,
            )

        self.assertIn("## 审批与边界", summary)
        self.assertIn("command-profiles/pre-gate", summary)
        self.assertIn("summary_confirm", summary)
        self.assertIn("当前项目暂无待审批票据", summary)

    def test_multi_agent_board_shows_pending_approval_records_for_project(self):
        with tempfile.TemporaryDirectory() as temp_dir, tempfile.TemporaryDirectory() as control_dir:
            project_root = Path(temp_dir) / "managed-project"
            self.factory_init.initialize_project(
                target=project_root,
                project_name="managed-project",
                idea="ship docs",
                stack="python",
                owner="tester",
                force=False,
            )
            self.set_intent_approval_root(Path(control_dir))
            result = self.intent_resolver.resolve_intent("今天收尾并生成会话入口", project_root, tool="codex")
            approval = self.intent_resolver.request_primary_approval(
                result,
                owner="tester",
                note="close day",
                focus="handover",
                strict=False,
            )

            pending = self.multi_agent_board.pending_approval_records(project_root)

        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0]["id"], approval["ticket"])
        self.assertEqual(pending[0]["action"], "command-profiles")

    def test_factory_core_detects_role_assignment_write_target_conflicts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "managed-project"
            self.factory_init.initialize_project(
                target=project_root,
                project_name="managed-project",
                idea="ship docs",
                stack="python",
                owner="tester",
                force=False,
            )
            config = self.factory_core.load_project_config(project_root)
            self.factory_core.ensure_role_catalog(config)
            self.factory_core.set_current_role_assignment(
                config,
                "coordinator",
                {
                    "owner": "planner",
                    "tool": "codex",
                    "items": [],
                    "status": "进行中",
                    "focus": "plan",
                    "note": "",
                    "write_targets": ["scripts"],
                    "assigned_at": "2026-04-02 10:00:00",
                },
            )
            self.factory_core.set_current_role_assignment(
                config,
                "release-manager",
                {
                    "owner": "releaser",
                    "tool": "gemini",
                    "items": [],
                    "status": "进行中",
                    "focus": "release",
                    "note": "",
                    "write_targets": ["scripts/factory-dispatch"],
                    "assigned_at": "2026-04-02 10:01:00",
                },
            )

            conflicts = self.factory_core.role_assignment_conflicts(project_root, config)

        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]["roles"], ["coordinator", "release-manager"])
        self.assertIn("scripts <-> scripts/factory-dispatch", conflicts[0]["overlaps"])

    def test_role_assign_blocks_conflicting_write_targets(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "managed-project"
            self.factory_init.initialize_project(
                target=project_root,
                project_name="managed-project",
                idea="ship docs",
                stack="python",
                owner="tester",
                force=False,
            )

            original_argv = sys.argv[:]
            try:
                sys.argv = [
                    str(FACTORY_ROLE_ASSIGN),
                    "--project",
                    str(project_root),
                    "--role",
                    "coordinator",
                    "--owner",
                    "planner",
                    "--write-targets",
                    "scripts",
                ]
                self.assertEqual(self.role_assign.main(), 0)

                stderr = io.StringIO()
                sys.argv = [
                    str(FACTORY_ROLE_ASSIGN),
                    "--project",
                    str(project_root),
                    "--role",
                    "release-manager",
                    "--owner",
                    "releaser",
                    "--write-targets",
                    "scripts/factory-dispatch",
                ]
                with redirect_stderr(stderr):
                    exit_code = self.role_assign.main()
            finally:
                sys.argv = original_argv

            config = self.factory_core.load_project_config(project_root)
            assignments = self.factory_core.ensure_role_assignment_state(config)

        self.assertEqual(exit_code, 1)
        self.assertIn("检测到写集冲突", stderr.getvalue())
        self.assertNotIn("release-manager", assignments)

    def test_multi_agent_board_reports_write_target_conflicts_and_blocks_parallel(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "managed-project"
            self.factory_init.initialize_project(
                target=project_root,
                project_name="managed-project",
                idea="ship docs",
                stack="python",
                owner="tester",
                force=False,
            )
            config = self.factory_core.load_project_config(project_root)
            self.factory_core.ensure_role_catalog(config)
            self.factory_core.set_current_role_assignment(
                config,
                "coordinator",
                {
                    "owner": "planner",
                    "tool": "codex",
                    "items": [],
                    "status": "进行中",
                    "focus": "plan",
                    "note": "",
                    "write_targets": ["scripts"],
                    "assigned_at": "2026-04-02 10:00:00",
                },
            )
            self.factory_core.set_current_role_assignment(
                config,
                "release-manager",
                {
                    "owner": "releaser",
                    "tool": "gemini",
                    "items": [],
                    "status": "进行中",
                    "focus": "release",
                    "note": "",
                    "write_targets": ["scripts/factory-dispatch"],
                    "assigned_at": "2026-04-02 10:01:00",
                },
            )
            self.factory_core.save_project_config(project_root, config)
            grouped = self.factory_core.group_items_by_role(config, [])
            active_roles = self.factory_core.active_roles_for_stage(config, config.get("stage", ""))

            summary = self.multi_agent_board.summary_markdown(
                config,
                "冲突阻断",
                [],
                [],
                active_roles,
                grouped,
                project_root,
                "tester",
                4,
            )

        self.assertIn("## Ownership 与冲突", summary)
        self.assertIn("写集冲突：1", summary)
        self.assertIn("`项目协调者` <-> `发布经理`", summary)
        self.assertIn("scripts <-> scripts/factory-dispatch", summary)

    def test_frontend_profiles_support_opencode_and_aliases(self):
        profiles = self.factory_core.load_frontend_profiles()
        opencode = self.factory_core.resolve_frontend_profile("open-code")

        self.assertIn("codex", profiles)
        self.assertIn("gemini", profiles)
        self.assertIn("opencode", profiles)
        self.assertEqual(opencode["id"], "opencode")
        self.assertTrue(opencode["capabilities"]["command_exec"])

    def test_chat_bootstrap_uses_frontend_profile_for_opencode(self):
        profile = self.factory_core.resolve_frontend_profile("opencode")

        self.assertEqual(self.chat_bootstrap.tool_label(profile), "OpenCode")
        self.assertEqual(self.chat_bootstrap.primary_rule_file(profile), "AGENTS.md 与 GEMINI.md")
        prompts = self.chat_bootstrap.example_prompts("架构负责人", "opencode", "继续设计")
        self.assertTrue(any("继续设计" in line for line in prompts))

    def test_frontend_capabilities_lists_registered_frontends(self):
        payload = self.frontend_capabilities.list_payload()

        ids = {item["id"] for item in payload}
        self.assertIn("codex", ids)
        self.assertIn("gemini", ids)
        self.assertIn("opencode", ids)

    def test_load_project_config_normalizes_legacy_current_stage(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            factory_dir = project_root / ".factory"
            factory_dir.mkdir(parents=True)
            (factory_dir / "project.json").write_text(
                json.dumps(
                    {
                        "project_name": "legacy-project",
                        "current_stage": "MAINTENANCE",
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            config = self.factory_core.load_project_config(project_root)

        self.assertEqual(config["stage"], "MAINTENANCE")

    def test_factory_init_project_config_uses_relative_paths(self):
        payload = json.loads(
            self.factory_init.build_project_config(
                project_name="example-project",
                idea="idea",
                stack="python",
                owner="tester",
                target=EXAMPLE_PROJECT,
                config=self.factory_init.load_config(),
            )
        )

        self.assertEqual(payload["project_root"], ".")
        self.assertIn(self.expected_runtime_protocol, payload["ai_runtime_docs"])
        self.assertIn(self.expected_docs_index, payload["human_workflow_docs"])
        self.assertIn(self.expected_brainstorm_skill, [item["path"] for item in payload["shared_skills"]])
        self.assertFalse(any(Path(item).is_absolute() for item in payload["ai_runtime_docs"]))
        self.assertFalse(any(Path(item["path"]).is_absolute() for item in payload["shared_skills"]))

    def test_factory_init_creates_docs_stratego_root_and_top_level_indexes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "managed-project"
            written = self.factory_init.initialize_project(
                target=project_root,
                project_name="managed-project",
                idea="ship docs",
                stack="python",
                owner="tester",
                force=False,
            )
            root_index = (project_root / "docs" / "index.md").read_text(encoding="utf-8")
            getting_started_index = (project_root / "docs" / "01-getting-started" / "index.md").read_text(encoding="utf-8")
            user_index = (project_root / "docs" / "02-user-guide" / "index.md").read_text(encoding="utf-8")
            developer_index = (project_root / "docs" / "03-developer-guide" / "index.md").read_text(encoding="utf-8")
            project_dev_index = (project_root / "docs" / "04-project-development" / "index.md").read_text(encoding="utf-8")

        self.assertIn(str(project_root / "docs" / "index.md"), written)
        self.assertIn(str(project_root / "docs" / "01-getting-started" / "index.md"), written)
        self.assertIn(str(project_root / "docs" / "02-user-guide" / "index.md"), written)
        self.assertIn(str(project_root / "docs" / "03-developer-guide" / "index.md"), written)
        self.assertIn(str(project_root / "docs" / "04-project-development" / "index.md"), written)
        self.assertIn("home_access: public", root_index)
        self.assertIn("path: 01-getting-started/index.md", root_index)
        self.assertIn("path: 01-getting-started/project-overview.md", root_index)
        self.assertIn("path: 02-user-guide/user-guide.md", root_index)
        self.assertIn("path: 03-developer-guide/index.md", root_index)
        self.assertIn("path: 04-project-development/index.md", root_index)
        self.assertTrue(getting_started_index.startswith("# 入门说明\n"))
        self.assertTrue(user_index.startswith("# 用户指南\n"))
        self.assertTrue(developer_index.startswith("# 开发者指南\n"))
        self.assertTrue(project_dev_index.startswith("# 项目开发文档（内）\n"))
        self.assertNotIn("/Users/", root_index)

    def test_detect_docs_profile_omits_developer_guide_for_docs_site(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "README.md").write_text(
                "# 章略·墨衡 文档站点\n\n这是一个供用户阅读和运营维护的 docs-stratego / mkdocs 文档站点。\n",
                encoding="utf-8",
            )
            (project_root / "mkdocs.yml").write_text("site_name: docs-site\n", encoding="utf-8")

            profile = self.factory_core.detect_docs_profile(
                project_root,
                project_name="docs-site",
                idea="构建章略·墨衡文档站点，供用户阅读和站点运维，不提供 SDK、插件或对外 API。",
                stack="mkdocs",
            )

        self.assertEqual(profile["project_kind"], "docs_site")
        self.assertEqual(profile["modules"]["02-user-guide"], "required")
        self.assertEqual(profile["modules"]["03-developer-guide"], "omit")
        self.assertFalse(profile["surfaces"]["secondary_development"])

    def test_factory_init_uses_docs_profile_to_omit_developer_guide(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "docs-site"
            written = self.factory_init.initialize_project(
                target=project_root,
                project_name="docs-site",
                idea="构建章略·墨衡文档站点，供用户阅读和站点运维，不提供 SDK、插件或对外 API。",
                stack="mkdocs",
                owner="tester",
                force=False,
            )
            project_config = json.loads((project_root / ".factory" / "project.json").read_text(encoding="utf-8"))
            root_index = (project_root / "docs" / "index.md").read_text(encoding="utf-8")
            publication_policy = (project_root / "docs" / "publication-policy.json").read_text(encoding="utf-8")

        self.assertIn(str(project_root / "docs" / "publication-policy.json"), written)
        self.assertEqual(project_config["docs_profile"]["modules"]["03-developer-guide"], "omit")
        self.assertFalse((project_root / "docs" / "03-developer-guide").exists())
        self.assertNotIn("path: 03-developer-guide/index.md", root_index)
        self.assertNotIn("docs/03-developer-guide/**", publication_policy)
        self.assertFalse(any("03-developer-guide/application-development.md" in item for item in project_config["human_workflow_docs"]))

if __name__ == "__main__":
    unittest.main()
