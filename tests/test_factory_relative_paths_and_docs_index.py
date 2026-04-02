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
FACTORY_DOCS_STANDARD_UPGRADE_BATCH = REPO_ROOT / "scripts" / "factory-docs-standard-upgrade-batch"
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
        cls.docs_upgrade_batch = load_script_module("factory_docs_standard_upgrade_batch", FACTORY_DOCS_STANDARD_UPGRADE_BATCH)
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

    def test_dispatch_resolves_docs_standard_upgrade_alias(self):
        self.assertEqual(self.dispatch.resolve_action("docs-upgrade"), "docs-standard-upgrade")
        self.assertEqual(self.dispatch.resolve_action("upgrade-docs-standard"), "docs-standard-upgrade")
        self.assertEqual(self.dispatch.resolve_action("docs-upgrade-batch"), "docs-standard-upgrade-batch")
        self.assertEqual(self.dispatch.resolve_action("frontend"), "frontend-capabilities")
        self.assertEqual(self.dispatch.resolve_action("intent"), "intent-resolver")
        self.assertEqual(self.dispatch.resolve_action("intent-replay"), "intent-eval")
        self.assertEqual(self.dispatch.resolve_action("intent-approve"), "intent-approval")

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
        self.assertIn("docs-standard-upgrade", registry)
        self.assertEqual(registry["state-doctor"]["risk_level"], "L0")
        self.assertEqual(registry["docs-standard-upgrade"]["risk_level"], "L1")

    def test_dispatch_action_policy_uses_registry_and_safe_default(self):
        policy = self.dispatch.action_policy("docs-standard-upgrade")
        default_policy = self.dispatch.action_policy("non-existent-action")

        self.assertEqual(policy["risk_level"], "L1")
        self.assertEqual(policy["approval"], "auto")
        self.assertEqual(default_policy["risk_level"], "L3")
        self.assertEqual(default_policy["approval"], "explicit_confirm")

    def test_intent_resolver_recommends_init_for_empty_project(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.intent_resolver.resolve_intent("初始化这个空目录项目", Path(temp_dir), tool="codex")

        self.assertEqual(result["primary"]["action"], "init")
        self.assertEqual(result["primary"]["policy"]["risk_level"], "L2")

    def test_intent_resolver_recommends_onboarding_for_unmanaged_project(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "README.md").write_text("# Legacy Project\n", encoding="utf-8")

            result = self.intent_resolver.resolve_intent("先接管这个历史项目", project_root, tool="codex")

        self.assertEqual(result["primary"]["action"], "historical-project-onboarding")
        self.assertFalse(result["primary"]["blocked"])

    def test_intent_resolver_prefers_docs_upgrade_for_managed_project(self):
        result = self.intent_resolver.resolve_intent("把 docs 刷新到最新规范并重建目录", REPO_ROOT, tool="opencode")

        self.assertEqual(result["primary"]["action"], "docs-standard-upgrade")
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

    def test_intent_resolver_safe_execution_blocks_non_auto_policy(self):
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

        self.assertEqual(result["primary"]["action"], "historical-project-onboarding")
        self.assertEqual(execution["status"], "policy_denied")

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

        self.assertGreaterEqual(len(cases), 7)
        ids = {case["id"] for case in cases}
        self.assertIn("intent-managed-next-step", ids)
        self.assertIn("intent-managed-daily-workflow", ids)
        self.assertIn("intent-managed-daily-profile", ids)

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
            "expected": {"action": "docs-standard-upgrade"},
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

    def test_docs_stratego_indexes_have_front_matter_and_nav(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "docs" / "04-project-development" / "03-requirements").mkdir(parents=True)
            (project_root / "docs" / "04-project-development" / "04-design" / "private-design").mkdir(parents=True)
            (project_root / "docs" / "04-project-development" / "03-requirements" / "prd.md").write_text(
                "# 产品需求文档\n",
                encoding="utf-8",
            )
            (project_root / "docs" / "04-project-development" / "04-design" / "system-architecture.md").write_text(
                "# 系统架构设计\n",
                encoding="utf-8",
            )
            (project_root / "docs" / "04-project-development" / "04-design" / "private-design" / "overview.md").write_text(
                "# 内部方案总览\n",
                encoding="utf-8",
            )

            written = self.factory_core.write_docs_stratego_indexes(project_root, "示例项目")

            root_index = (project_root / "docs" / "index.md").read_text(encoding="utf-8")
            requirements_index = (
                project_root / "docs" / "04-project-development" / "03-requirements" / "index.md"
            ).read_text(encoding="utf-8")
            solution_index = (
                project_root / "docs" / "04-project-development" / "04-design" / "index.md"
            ).read_text(encoding="utf-8")
            private_design_index = (
                project_root / "docs" / "04-project-development" / "04-design" / "private-design" / "index.md"
            ).read_text(encoding="utf-8")

        self.assertIn("docs/index.md", written)
        self.assertIn("---\n", root_index)
        self.assertIn("title: 示例项目", root_index)
        self.assertIn("home_access: public", root_index)
        self.assertIn("path: 04-project-development/index.md", root_index)
        self.assertIn("path: 04-project-development/03-requirements/index.md", root_index)
        self.assertIn("path: 04-project-development/03-requirements/prd.md", root_index)
        self.assertIn("path: 04-project-development/04-design/index.md", root_index)
        self.assertIn("path: 04-project-development/04-design/system-architecture.md", root_index)
        self.assertIn("title: 内部专题", root_index)
        self.assertIn("path: 04-project-development/04-design/private-design/index.md", root_index)
        self.assertIn("path: 04-project-development/04-design/private-design/overview.md", root_index)
        self.assertIn("access: public", root_index)
        self.assertIn("access: private", root_index)
        self.assertTrue(requirements_index.startswith("# 需求概览\n"))
        self.assertIn("目录树、页面路径和访问级别统一由根 `docs/index.md` 声明", requirements_index)
        self.assertNotIn("建议阅读顺序", requirements_index)
        self.assertNotIn("mkdocs:", requirements_index)
        self.assertNotIn("default_access:", requirements_index)
        self.assertTrue(solution_index.startswith("# 设计文档概览\n"))
        self.assertIn("目录树、页面路径和访问级别统一由根 `docs/index.md` 声明", solution_index)
        self.assertNotIn("建议阅读顺序", solution_index)
        self.assertTrue(private_design_index.startswith("# 内部专题概览\n"))
        self.assertIn("本页是该目录的正文首页", private_design_index)
        self.assertNotIn("/Users/", root_index)

    def test_docs_stratego_source_status_detects_missing_indexes_and_absolute_paths(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "docs" / "04-project-development" / "02-discovery").mkdir(parents=True)
            input_path = project_root / "docs" / "04-project-development" / "02-discovery" / "input.md"
            input_path.write_text("# 项目输入\n\n路径 `/Users/example/project`。\n", encoding="utf-8")

            status_before, lines_before = self.factory_core.docs_stratego_source_status(project_root, "示例项目")

            input_path.write_text("# 项目输入\n\n使用相对路径 `./docs/index.md`。\n", encoding="utf-8")
            self.factory_core.write_docs_stratego_indexes(project_root, "示例项目")
            status_after, lines_after = self.factory_core.docs_stratego_source_status(project_root, "示例项目")

        self.assertEqual(status_before, "异常")
        self.assertTrue(any("docs/index.md" in line or "机器绝对路径" in line for line in lines_before))
        self.assertEqual(status_after, "就绪")
        self.assertTrue(any("根 `docs/index.md`" in line or "未发现明显机器绝对路径污染" in line for line in lines_after))

    def test_docs_stratego_source_status_detects_missing_nav_targets_and_explicit_self_anchors(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            user_guide_dir = project_root / "docs" / "02-user-guide"
            user_guide_dir.mkdir(parents=True)
            prompt_path = user_guide_dir / "prompt-templates.md"
            prompt_path.write_text(
                "# 提示词速查\n\n[跳转](#3-空目录新项目初始化)\n\n## 3. 空目录新项目初始化\n",
                encoding="utf-8",
            )
            (user_guide_dir / "user-guide.md").write_text("# 使用指南\n", encoding="utf-8")

            self.factory_core.write_docs_stratego_indexes(project_root, "示例项目")

            root_path = project_root / "docs" / "index.md"
            root_text = root_path.read_text(encoding="utf-8")
            root_path.write_text(
                root_text.replace(
                    "path: 02-user-guide/user-guide.md\n          access: public\n",
                    "path: 02-user-guide/user-guide.md\n"
                    "          access: public\n"
                    "        - title: 缺失页面\n"
                    "          path: 02-user-guide/missing.md\n"
                    "          access: public\n",
                ),
                encoding="utf-8",
            )

            status_before, lines_before = self.factory_core.docs_stratego_source_status(project_root, "示例项目")

            prompt_path.write_text(
                "# 提示词速查\n\n[跳转](#3-空目录新项目初始化)\n\n<a id=\"3-空目录新项目初始化\"></a>\n\n## 3. 空目录新项目初始化\n",
                encoding="utf-8",
            )
            self.factory_core.write_docs_stratego_indexes(project_root, "示例项目")
            status_after, lines_after = self.factory_core.docs_stratego_source_status(project_root, "示例项目")

        self.assertEqual(status_before, "异常")
        self.assertTrue(any("导航项指向不存在的页面" in line for line in lines_before))
        self.assertTrue(any("未声明显式锚点" in line for line in lines_before))
        self.assertEqual(status_after, "就绪")
        self.assertTrue(any("根 `docs/index.md`" in line for line in lines_after))

    def test_factory_init_creates_section_indexes_for_docs_stratego(self):
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
            governance_index = (
                project_root / "docs" / "04-project-development" / "01-governance" / "index.md"
            ).read_text(encoding="utf-8")
            solution_index = (
                project_root / "docs" / "04-project-development" / "04-design" / "index.md"
            ).read_text(encoding="utf-8")
            developer_index = (
                project_root / "docs" / "03-developer-guide" / "index.md"
            ).read_text(encoding="utf-8")
            status, lines = self.factory_core.docs_stratego_source_status(project_root, "managed-project")

        self.assertIn(str(project_root / "docs" / "index.md"), written)
        self.assertIn(str(project_root / "docs" / "04-project-development" / "01-governance" / "index.md"), written)
        self.assertIn("home_access: public", root_index)
        self.assertIn("path: 01-getting-started/index.md", root_index)
        self.assertIn("path: 04-project-development/index.md", root_index)
        self.assertTrue(governance_index.startswith("# 项目治理概览\n"))
        self.assertIn("本页是该目录的正文首页", governance_index)
        self.assertNotIn("mkdocs:", governance_index)
        self.assertTrue(solution_index.startswith("# 设计文档概览\n"))
        self.assertIn("本页是该目录的正文首页", solution_index)
        self.assertIn("module 开发、调试、交付与排错", developer_index)
        self.assertEqual(status, "就绪")
        self.assertTrue(any("根 `docs/index.md`" in line for line in lines))

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

    def test_docs_stratego_source_status_accepts_custom_index_content(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "docs" / "03-developer-guide").mkdir(parents=True)
            (project_root / "docs" / "03-developer-guide" / "application-development.md").write_text(
                "# 应用开发\n",
                encoding="utf-8",
            )
            (project_root / "docs" / "03-developer-guide" / "plugin-development.md").write_text(
                "# 插件开发\n",
                encoding="utf-8",
            )

            self.factory_core.write_docs_stratego_indexes(project_root, "示例项目")

            root_path = project_root / "docs" / "index.md"
            root_text = root_path.read_text(encoding="utf-8")
            root_front_matter, _ = self.factory_core.split_markdown_front_matter(root_text)
            self.assertIsNotNone(root_front_matter)
            root_path.write_text(
                f"{root_front_matter}\n# 示例项目自定义入口\n\n这里保留人工维护的正文，不要求和生成模板逐字一致。\n",
                encoding="utf-8",
            )

            developer_index_path = project_root / "docs" / "03-developer-guide" / "index.md"
            developer_index_path.write_text(
                "# 开发者指南\n\n## 自定义正文\n\n先看应用开发，再看插件开发，函数和接口按项目实际情况扩展。\n",
                encoding="utf-8",
            )

            status, lines = self.factory_core.docs_stratego_source_status(project_root, "示例项目")

        self.assertEqual(status, "就绪")
        self.assertTrue(any("根 `docs/index.md`" in line for line in lines))

    def test_write_docs_stratego_indexes_preserves_custom_index_bodies(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "docs" / "03-developer-guide").mkdir(parents=True)
            (project_root / "docs" / "03-developer-guide" / "application-development.md").write_text(
                "# 应用开发\n",
                encoding="utf-8",
            )

            self.factory_core.write_docs_stratego_indexes(project_root, "示例项目")

            root_path = project_root / "docs" / "index.md"
            root_text = root_path.read_text(encoding="utf-8")
            root_front_matter, _ = self.factory_core.split_markdown_front_matter(root_text)
            root_path.write_text(
                f"{root_front_matter}\n# 自定义首页\n\n保留人工撰写的首页正文。\n",
                encoding="utf-8",
            )

            developer_index_path = project_root / "docs" / "03-developer-guide" / "index.md"
            developer_index_path.write_text(
                "# 自定义开发者指南\n\n这里是人工维护的目录概览，不应被刷新动作覆盖。\n",
                encoding="utf-8",
            )

            (project_root / "docs" / "03-developer-guide" / "function-reference.md").write_text(
                "# 函数说明\n",
                encoding="utf-8",
            )

            self.factory_core.write_docs_stratego_indexes(project_root, "示例项目")

            refreshed_root = root_path.read_text(encoding="utf-8")
            refreshed_developer_index = developer_index_path.read_text(encoding="utf-8")

        self.assertIn("# 自定义首页", refreshed_root)
        self.assertIn("path: 03-developer-guide/function-reference.md", refreshed_root)
        self.assertEqual(
            refreshed_developer_index,
            "# 自定义开发者指南\n\n这里是人工维护的目录概览，不应被刷新动作覆盖。\n",
        )

    def test_write_docs_stratego_indexes_preserves_manual_nav_grouping_and_order(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            developer_dir = project_root / "docs" / "03-developer-guide"
            user_dir = project_root / "docs" / "02-user-guide"
            getting_started_dir = project_root / "docs" / "01-getting-started"
            project_dev_dir = project_root / "docs" / "04-project-development"
            developer_dir.mkdir(parents=True)
            user_dir.mkdir(parents=True)
            getting_started_dir.mkdir(parents=True)
            project_dev_dir.mkdir(parents=True)
            (developer_dir / "index.md").write_text("# 开发者指南\n", encoding="utf-8")
            (developer_dir / "application-development.md").write_text("# 应用开发\n", encoding="utf-8")
            (developer_dir / "function-reference.md").write_text("# 函数说明\n", encoding="utf-8")
            (developer_dir / "plugin-development.md").write_text("# 插件开发\n", encoding="utf-8")
            (user_dir / "index.md").write_text("# 用户指南\n", encoding="utf-8")
            (user_dir / "user-guide.md").write_text("# 使用指南\n", encoding="utf-8")
            (getting_started_dir / "index.md").write_text("# 入门说明\n", encoding="utf-8")
            (getting_started_dir / "quick-start.md").write_text("# 快速开始\n", encoding="utf-8")
            (project_dev_dir / "index.md").write_text("# 项目开发文档\n", encoding="utf-8")

            custom_root = """---
title: 示例项目
mkdocs:
  home_access: public
  nav:
    - title: 二次开发中心
      children:
        - title: 概览
          path: 03-developer-guide/index.md
          access: public
        - title: 函数先看
          path: 03-developer-guide/function-reference.md
          access: public
        - title: 应用开发
          path: 03-developer-guide/application-development.md
          access: public
    - title: 用户入口
      children:
        - title: 概览
          path: 02-user-guide/index.md
          access: public
        - title: 使用指南
          path: 02-user-guide/user-guide.md
          access: public
---
# 自定义首页

这里保留人工维护的导航分组顺序。
"""
            (project_root / "docs" / "index.md").write_text(custom_root, encoding="utf-8")

            self.factory_core.write_docs_stratego_indexes(project_root, "示例项目")
            refreshed_root = (project_root / "docs" / "index.md").read_text(encoding="utf-8")

        self.assertIn("title: 二次开发中心", refreshed_root)
        self.assertIn("title: 用户入口", refreshed_root)
        self.assertIn("title: 函数先看", refreshed_root)
        self.assertIn("path: 03-developer-guide/plugin-development.md", refreshed_root)
        self.assertLess(refreshed_root.index("title: 二次开发中心"), refreshed_root.index("title: 用户入口"))
        self.assertLess(
            refreshed_root.index("path: 03-developer-guide/function-reference.md"),
            refreshed_root.index("path: 03-developer-guide/application-development.md"),
        )
        self.assertLess(
            refreshed_root.index("path: 03-developer-guide/application-development.md"),
            refreshed_root.index("path: 03-developer-guide/plugin-development.md"),
        )
        self.assertIn("title: 入门说明", refreshed_root)
        self.assertIn("title: 项目开发文档（内）", refreshed_root)

    def test_write_docs_stratego_indexes_refreshes_generated_directory_indexes_without_mkdocs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            concepts_dir = project_root / "docs" / "03-developer-guide" / "01-concepts"
            concepts_dir.mkdir(parents=True)
            (concepts_dir / "01-system-map.md").write_text(
                "# 1.1 系统地图与术语\n",
                encoding="utf-8",
            )
            (concepts_dir / "02-real-constraints.md").write_text(
                "# 1.2 当前真实约束\n",
                encoding="utf-8",
            )
            stale_index_path = concepts_dir / "index.md"
            stale_index_path.write_text(
                "# 01 concepts概览\n\n本目录收纳与“01 concepts”相关的页面和子目录。\n\n建议阅读顺序：\n\n1. 1.1 系统地图与术语\n2. 1.2 当前真实约束\n",
                encoding="utf-8",
            )

            written = self.factory_core.write_docs_stratego_indexes(project_root, "示例项目")
            refreshed_index = stale_index_path.read_text(encoding="utf-8")

        self.assertIn("docs/03-developer-guide/01-concepts/index.md", written)
        self.assertTrue(refreshed_index.startswith("# 01 概念与约束概览\n"))
        self.assertIn("系统地图、术语和真实约束", refreshed_index)
        self.assertIn("本页是该目录的正文首页", refreshed_index)
        self.assertNotIn("建议阅读顺序", refreshed_index)

    def test_docs_stratego_indexes_include_contract_files_and_preserve_access_overrides(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            openapi_dir = project_root / "docs" / "04-project-development" / "04-design" / "subsystems" / "gateway" / "openapi"
            tools_dir = project_root / "docs" / "03-developer-guide" / "tools"
            openapi_dir.mkdir(parents=True)
            tools_dir.mkdir(parents=True)
            (openapi_dir / "index.md").write_text("# Gateway OpenAPI 概览\n", encoding="utf-8")
            (tools_dir / "index.md").write_text("# 工具契约概览\n", encoding="utf-8")
            (openapi_dir / "app.openapi.yaml").write_text(
                "openapi: 3.1.0\ninfo:\n  title: App API\n  version: 1.0.0\npaths: {}\n",
                encoding="utf-8",
            )
            (tools_dir / "public-agent.mcp-tools.json").write_text(
                json.dumps(
                    {
                        "tools": [
                            {
                                "name": "build_site",
                                "title": "Public Agent Tools",
                                "description": "Build docs site.",
                                "inputSchema": {"type": "object"},
                            }
                        ]
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            self.factory_core.write_docs_stratego_indexes(project_root, "示例项目")

            root_path = project_root / "docs" / "index.md"
            root_text = root_path.read_text(encoding="utf-8")
            root_text = root_text.replace("home_access: public", "home_access: private")
            root_text = root_text.replace("title: App API", "title: 外部 App API")
            root_text = root_text.replace(
                "path: 04-project-development/04-design/subsystems/gateway/openapi/app.openapi.yaml\n"
                "                          access: private",
                "path: 04-project-development/04-design/subsystems/gateway/openapi/app.openapi.yaml\n"
                "                          access: public",
            )
            root_path.write_text(root_text, encoding="utf-8")

            self.factory_core.write_docs_stratego_indexes(project_root, "示例项目")
            refreshed_root = root_path.read_text(encoding="utf-8")

        self.assertIn("home_access: private", refreshed_root)
        self.assertIn("path: 04-project-development/04-design/subsystems/gateway/openapi/app.openapi.yaml", refreshed_root)
        self.assertIn("title: 外部 App API", refreshed_root)
        self.assertIn("access: public", refreshed_root)
        self.assertIn("path: 03-developer-guide/tools/public-agent.mcp-tools.json", refreshed_root)
        self.assertIn("title: Public Agent Tools", refreshed_root)

    def test_docs_stratego_source_status_rejects_invalid_contract_pages_and_assets_contracts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            openapi_dir = project_root / "docs" / "03-developer-guide" / "openapi"
            assets_dir = project_root / "docs" / "03-developer-guide" / "assets"
            openapi_dir.mkdir(parents=True)
            assets_dir.mkdir(parents=True)
            (openapi_dir / "index.md").write_text("# OpenAPI 概览\n", encoding="utf-8")
            (openapi_dir / "broken.openapi.yaml").write_text(
                "openapi: 3.1.0\ninfo:\n  title: Broken API\npaths: {}\n",
                encoding="utf-8",
            )
            (assets_dir / "hidden.mcp-tools.yaml").write_text(
                "tools:\n  - name: hidden\n    description: hidden tool\n    inputSchema:\n      type: object\n",
                encoding="utf-8",
            )

            self.factory_core.write_docs_stratego_indexes(project_root, "示例项目")
            status, lines = self.factory_core.docs_stratego_source_status(project_root, "示例项目")

        self.assertEqual(status, "异常")
        self.assertTrue(any("broken.openapi.yaml" in line and "info.version" in line for line in lines))
        self.assertTrue(any("assets/" in line and "契约文件" in line for line in lines))

    def test_upgrade_docs_source_standard_migrates_legacy_project_and_returns_ready(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "docs" / "02-requirements").mkdir(parents=True)
            (project_root / "docs" / "08-handover").mkdir(parents=True)
            (project_root / "docs" / "README.md").write_text("# 旧入口\n", encoding="utf-8")
            (project_root / "docs" / "02-requirements" / "prd.md").write_text("# 产品需求文档\n", encoding="utf-8")
            (project_root / "docs" / "08-handover" / "user-guide.md").write_text("# 用户指南\n", encoding="utf-8")

            result = self.factory_core.upgrade_docs_source_standard(project_root, "示例项目")

            root_index = (project_root / "docs" / "index.md").read_text(encoding="utf-8")
            policy_text = (project_root / "docs" / "publication-policy.json").read_text(encoding="utf-8")

        self.assertTrue(result["migrated"])
        self.assertEqual(result["status"], "就绪")
        self.assertIn("path: 04-project-development/03-requirements/prd.md", root_index)
        self.assertIn("docs/index.md", policy_text)

    def test_discover_upgrade_candidate_projects_finds_managed_projects_only(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            managed_a = root / "proj-a"
            managed_b = root / "group" / "proj-b"
            unmanaged = root / "proj-c"
            skipped = root / "node_modules" / "proj-d"

            for project in [managed_a, managed_b]:
                (project / ".factory").mkdir(parents=True)
                (project / "docs").mkdir(parents=True)
                (project / ".factory" / "project.json").write_text('{"project_name":"demo"}', encoding="utf-8")

            (unmanaged / "docs").mkdir(parents=True)
            (skipped / ".factory").mkdir(parents=True)
            (skipped / "docs").mkdir(parents=True)
            (skipped / ".factory" / "project.json").write_text('{"project_name":"skip"}', encoding="utf-8")

            discovered = self.docs_upgrade_batch.discover_upgrade_candidate_projects([root], max_depth=3)

        self.assertEqual(discovered, sorted([managed_a.resolve(), managed_b.resolve()]))

    def test_migrate_docs_structure_upgrades_legacy_layout_and_rewrites_links(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "docs" / "02-requirements").mkdir(parents=True)
            (project_root / "docs" / "03-solution").mkdir(parents=True)
            (project_root / "docs" / "08-handover").mkdir(parents=True)
            (project_root / "docs" / "README.md").write_text(
                "# 旧入口\n\n查看 [需求](./02-requirements/prd.md)。\n",
                encoding="utf-8",
            )
            (project_root / "docs" / "02-requirements" / "prd.md").write_text(
                "# 产品需求文档\n",
                encoding="utf-8",
            )
            (project_root / "docs" / "03-solution" / "solution-overview.md").write_text(
                "# 总体方案与协作总览\n\n- [PRD](../02-requirements/prd.md)\n- [用户指南](../08-handover/user-guide.md)\n",
                encoding="utf-8",
            )
            (project_root / "docs" / "08-handover" / "user-guide.md").write_text(
                "# 用户指南\n",
                encoding="utf-8",
            )
            (project_root / "docs" / "08-handover" / "historical-project-prompt-templates.md").write_text(
                "# 历史项目标准提示词模板\n",
                encoding="utf-8",
            )

            status_before, lines_before = self.factory_core.docs_stratego_source_status(project_root, "示例项目")
            result = self.factory_core.migrate_docs_structure(project_root, "示例项目")
            status_after, lines_after = self.factory_core.docs_stratego_source_status(project_root, "示例项目")

            overview_path = project_root / "docs" / "04-project-development" / "04-design" / "solution-overview.md"
            migrated_text = overview_path.read_text(encoding="utf-8")
            project_overview = (project_root / "docs" / "01-getting-started" / "project-overview.md").read_text(encoding="utf-8")
            root_index = (project_root / "docs" / "index.md").read_text(encoding="utf-8")
            policy_text = (project_root / "docs" / "publication-policy.json").read_text(encoding="utf-8")
            legacy_solution_exists = (project_root / "docs" / "03-solution").exists()
            prompt_templates_exists = (project_root / "docs" / "02-user-guide" / "prompt-templates.md").exists()

            self.assertEqual(status_before, "异常")
            self.assertTrue(any("docs-migrate-structure" in line for line in lines_before))
            self.assertTrue(any("docs/03-solution/solution-overview.md" in item for item in result["moved"]))
            self.assertFalse(legacy_solution_exists)
            self.assertTrue(prompt_templates_exists)
            self.assertIn("[PRD](../03-requirements/prd.md)", migrated_text)
            self.assertIn("[用户指南](../../02-user-guide/user-guide.md)", migrated_text)
            self.assertIn("[需求](../04-project-development/03-requirements/prd.md)", project_overview)
            self.assertIn("title: 入门说明", root_index)
            self.assertIn("title: 项目开发文档（内）", root_index)
            self.assertIn("docs/03-developer-guide/**", policy_text)
            self.assertEqual(status_after, "就绪")
            self.assertTrue(any("根 `docs/index.md`" in line for line in lines_after))


if __name__ == "__main__":
    unittest.main()
