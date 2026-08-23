from __future__ import annotations

import json
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "using-shanforge" / "scripts" / "project_snapshot.py"


class ProjectSnapshotTest(unittest.TestCase):
    def test_plan_stages_use_explicit_parent_ids_at_arbitrary_depth(self) -> None:
        parse = runpy.run_path(str(SCRIPT))["_plan_stages"]

        nodes = parse(
            "# 计划\n\n"
            "### OUTSIDE-001 不属于路线\n\n"
            "## Work Breakdown\n\n"
            "| id | parent_id | title | status |\n"
            "|---|---|---|---|\n"
            "| ROOT | | 项目路线 | completed |\n"
            "| L1 | ROOT | 第一层 | completed |\n"
            "| L2 | L1 | 第二层 | completed |\n"
            "| L3 | L2 | 第三层 | current |\n"
            "| L4 | L3 | 第四层 | planned |\n"
            "| L5 | L4 | 第五层 | planned |\n"
            "| L6 | L5 | 第六层 | planned |\n\n"
            "### INSIDE-001 标题也不再产生路线节点\n\n"
            "## Verification\n\n"
            "### TEST-001 不属于路线\n"
        )

        self.assertEqual(
            [node["id"] for node in nodes],
            ["ROOT", "L1", "L2", "L3", "L4", "L5", "L6"],
        )
        self.assertIsNone(nodes[0]["parent_id"])
        self.assertEqual(nodes[0]["children"], ["L1"])
        self.assertEqual(nodes[1]["parent_id"], "ROOT")
        self.assertEqual(nodes[1]["children"], ["L2"])
        self.assertEqual([node["depth"] for node in nodes], list(range(7)))
        self.assertEqual(nodes[3]["state"], "current")
        self.assertEqual(nodes[6]["state"], "planned")

    def test_invalid_route_tree_fails_closed(self) -> None:
        loaded = runpy.run_path(str(SCRIPT))
        parse = loaded["_plan_stages"]
        error = loaded["SnapshotError"]
        header = (
            "# 计划\n\n## Work Breakdown\n\n"
            "| id | parent_id | title | status |\n"
            "|---|---|---|---|\n"
        )
        invalid_rows = {
            "duplicate": (
                "| ROOT | | 根 | current |\n| ROOT | | 重复 | planned |\n",
                "duplicate route id: ROOT",
            ),
            "orphan": (
                "| CHILD | MISSING | 孤儿 | current |\n",
                "missing parent MISSING for route CHILD",
            ),
            "self": (
                "| ROOT | ROOT | 自引用 | current |\n",
                "route ROOT cannot be its own parent",
            ),
            "cycle": (
                "| A | B | 节点 A | current |\n| B | A | 节点 B | current |\n",
                "route parent cycle",
            ),
        }
        for name, (rows, message) in invalid_rows.items():
            with self.subTest(name=name):
                with self.assertRaisesRegex(error, message):
                    parse(header + rows)

        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            work_item = project / ".factory" / "workitems" / "WI-BROKEN"
            work_item.mkdir(parents=True)
            (work_item / "brief.md").write_text(
                "# WI-BROKEN\n\n- 状态：in_progress\n",
                encoding="utf-8",
            )
            (work_item / "plan.md").write_text(
                header + "| CHILD | MISSING | 孤儿 | current |\n",
                encoding="utf-8",
            )
            current = project / ".factory" / "cache" / "site" / "current"
            current.mkdir(parents=True)
            (current / "index.html").write_text("old snapshot", encoding="utf-8")

            result = self._raw_run(project)

            self.assertEqual(result.returncode, 2)
            receipt = json.loads(result.stdout)
            self.assertEqual(receipt["status"], "failed")
            self.assertIn("missing parent MISSING for route CHILD", receipt["error"])
            self.assertEqual((current / "index.html").read_text(encoding="utf-8"), "old snapshot")
            self.assertFalse((current / "stages").exists())

    def test_board_groups_use_native_details_and_flat_tagged_task_rows(self) -> None:
        render = runpy.run_path(str(SCRIPT))["_grouped_board_cards"]
        task = {
            "id": "WI-001-T01",
            "title": "完成登录流程验收",
            "goal": "确认登录功能满足业务要求。",
            "work_item_id": "WI-001",
            "work_item_title": "交付登录流程",
            "work_item_purpose": "让门店员工安全登录。",
            "module": "账号与权限",
            "task_type": "验收测试",
            "priority": "P0",
            "route": "WI-001-T01",
            "status": "ready_for_review",
            "status_label": "等待独立评审",
            "next_action": "完成独立评审",
            "category": "active",
            "scope": "requirement",
            "relations": "REQ-LOGIN-001",
            "updated_at": "2026-07-29T00:01:00+08:00",
            "work_item_has_plan": True,
            "is_current": True,
        }

        rendered = render(
            [task],
            {"REQ-LOGIN-001": {"title": "安全登录"}},
        )

        self.assertIn('<details class="board-swimlane requirement-group"', rendered)
        self.assertIn('class="board-swimlane__heading"', rendered)
        self.assertIn('class="swimlane-grid"', rendered)
        self.assertEqual(rendered.count('data-board-column="'), 1)
        self.assertNotIn('class="empty-cell"', rendered)
        self.assertIn('class="board-card__tags tags"', rendered)
        self.assertIn("下一步：完成独立评审", rendered)
        self.assertNotIn('class="board-card__relations"', rendered)
        self.assertEqual(rendered.count('href="requirements/REQ-LOGIN-001.html"'), 1)
        self.assertNotIn("<p>", rendered)
        self.assertNotIn('class="task-nature-group"', rendered)
        self.assertNotIn('class="classification-group"', rendered)

    def test_work_item_board_group_links_to_plan_or_current_task(self) -> None:
        render = runpy.run_path(str(SCRIPT))["_grouped_board_cards"]
        task = {
            "id": "WI-PLAN-T01",
            "title": "完成项目设计",
            "goal": "完成系统级设计。",
            "work_item_id": "WI-PLAN",
            "work_item_title": "系统设计",
            "work_item_purpose": "形成项目技术基线。",
            "module": "系统设计",
            "task_type": "设计",
            "priority": "P0",
            "route": "WI-PLAN-T01",
            "status": "in_progress",
            "status_label": "进行中",
            "next_action": "完成设计评审",
            "category": "active",
            "scope": "project",
            "relations": "",
            "updated_at": "2026-07-29T00:01:00+08:00",
            "work_item_has_plan": True,
            "is_current": True,
        }

        planned = render([task], {})
        task_only = render(
            [
                task
                | {
                    "id": "WI-TASK-T01",
                    "work_item_id": "WI-TASK",
                    "work_item_title": "局部调整",
                    "route": "WI-TASK-T01",
                    "work_item_has_plan": False,
                }
            ],
            {},
        )

        self.assertIn('href="plans/WI-PLAN.html"', planned)
        self.assertIn('href="tasks/WI-TASK-T01.html"', task_only)

    def test_shanforge_session_card_matches_current_mainline_ledger(self) -> None:
        session = (ROOT / ".factory" / "memory" / "agent-session.md").read_text(encoding="utf-8")
        ledger = ROOT / ".factory" / "workitems" / "MODEL-ROUTING-001" / "ledger.jsonl"
        latest = json.loads(ledger.read_text(encoding="utf-8").splitlines()[-1])

        self.assertEqual(latest["task_card_id"], "MODEL-ROUTING-001-T03")
        self.assertIn(latest["next_required_action"], session)
        self.assertIn(latest["work_item_id"], session)
        self.assertIn("MODEL-ROUTING-001 已完成", session)
        self.assertNotIn("客户确认六角色映射", session)

    def test_skill_first_boundary_has_no_repository_runtime(self) -> None:
        self.assertFalse((ROOT / "src").exists())
        for path in (
            ROOT / "skills" / "using-shanforge" / "SKILL.md",
            ROOT / "skills" / "using-shanforge" / "references" / "pm-dashboard-rendering.md",
        ):
            content = path.read_text(encoding="utf-8")
            self.assertIn("scripts/project_snapshot.py", content)
            self.assertNotIn("PYTHONPATH=src", content)
            self.assertNotIn("settings.composition.project_knowledge", content)

    def test_snapshot_renders_compact_scoped_board_without_duplicate_tasks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / ".factory" / "memory").mkdir(parents=True)
            (project / ".factory" / "project.json").write_text(
                json.dumps(
                    {
                        "project_name": "门店工作台",
                        "idea": "让门店员工安全、高效地处理日常订单。",
                        "owner": "产品负责人",
                        "stage": "IMPLEMENTATION",
                        "workflow_docs": [
                            "docs/04-product/prd.md",
                            "docs/05-design/solution-overview.md",
                            "docs/05-design/system-architecture.md",
                            "docs/03-developer-guide/application-development.md",
                            "docs/06-delivery/test-plan.md",
                            "docs/06-delivery/release-notes.md",
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            (project / ".factory" / "memory" / "agent-session.md").write_text(
                "# Agent 会话卡\n\n"
                "- 当前阶段：`WI-001 / WI-001-T01`\n"
                "- 当前状态：`in_progress`\n"
                "- 当前焦点：登录流程交付\n"
                "- 停止原因：无\n"
                "- 唯一下一动作：旧会话动作，不得覆盖最新 ledger\n",
                encoding="utf-8",
            )
            (project / ".factory" / "memory" / "doc-map.md").write_text(
                "# 文档映射\n\n"
                "- `docs/04-product/prd.md` -> 需求\n"
                "- `docs/05-design/*.md` -> 设计\n"
                "- `docs/03-developer-guide/*.md` -> 开发\n"
                "- `docs/06-delivery/*.md` -> 测试与交付\n",
                encoding="utf-8",
            )
            documents = {
                "docs/04-product/prd.md": (
                    "# 门店工作台产品需求\n\n"
                    "| 项目 | 内容 |\n|---|---|\n| 文档 ID | `PRD-STORE-001` |\n"
                ),
                "docs/05-design/solution-overview.md": "# 登录解决方案\n",
                "docs/05-design/system-architecture.md": (
                    "# 系统架构\n\n## 1. 架构结论\n\n"
                    "门店工作台是一套帮助门店员工安全处理订单的业务应用。\n\n"
                    "## 2. 交付单元\n\n- 可安装应用\n- 操作手册\n"
                ),
                "docs/03-developer-guide/application-development.md": "# 开发指南\n",
                "docs/06-delivery/test-plan.md": "# 登录测试计划\n",
                "docs/06-delivery/release-notes.md": "# 发布说明\n",
            }
            for relative_path, content in documents.items():
                path = project / relative_path
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            work_item = project / ".factory" / "workitems" / "WI-001"
            task_briefs = work_item / "task-briefs"
            task_briefs.mkdir(parents=True)
            (work_item / "brief.md").write_text(
                "# WI-001：交付登录流程\n\n"
                "- 阶段：IMPLEMENTATION\n"
                "- 状态：in_progress\n"
                "- 用户目标：让门店员工安全登录并继续处理订单。\n\n"
                "### REQ-LOGIN-001：安全登录\n\n"
                "作为门店员工，我希望使用账号安全登录，以便继续处理订单。\n\n"
                "### REQ-LOGIN-002：登录审计\n\n"
                "作为门店管理员，我希望查看登录审计记录，以便发现异常访问。\n\n"
                "### REQ-LOGIN-003：会话安全\n\n"
                "作为门店员工，我希望登录会话按期失效，以便降低账号风险。\n",
                encoding="utf-8",
            )
            (work_item / "plan.md").write_text(
                "# 登录流程实施计划\n\n"
                "## Work Breakdown\n\n"
                "| id | parent_id | title | status |\n"
                "|---|---|---|---|\n"
                "| PHASE-001 | | 需求确认 | completed |\n"
                "| PHASE-001-S01 | PHASE-001 | 确认业务目标 | completed |\n"
                "| PHASE-002 | | 登录设计 | completed |\n"
                "| PHASE-002-S01 | PHASE-002 | 完成登录交互设计 | completed |\n"
                "| WI-001-T01 | | 登录流程验收 | ready_for_review |\n"
                "| WI-001-T01-S01 | WI-001-T01 | 验证登录成功路径 | completed |\n"
                "| WI-001-T01-S02 | WI-001-T01 | 完成独立验收 | current |\n"
                "| WI-001-T01-S02-A | WI-001-T01-S02 | 记录验收结论 | planned |\n"
                "| WI-001-T01-S02-B | WI-001-T01-S02-A | 汇总验收证据 | planned |\n"
                "| WI-001-T01-S02-C | WI-001-T01-S02-B | 核对证据索引 | planned |\n"
                "| WI-001-T01-S02-D | WI-001-T01-S02-C | 形成评审输入 | planned |\n"
                "| WI-001-T01-S02-E | WI-001-T01-S02-D | 完成最终签核 | planned |\n"
                "| PHASE-004 | | 发布准备 | planned |\n"
                "| PHASE-004-S01 | PHASE-004 | 整理发布材料 | planned |\n"
                "| PHASE-005 | | 门店试点 | planned |\n",
                encoding="utf-8",
            )
            (task_briefs / "WI-001-T01.md").write_text(
                "# WI-001-T01：完成登录流程验收\n\n"
                "- 状态：ready_for_review\n"
                "- 优先级：P0\n"
                "- 任务层级：requirement\n"
                "- task_type：验收测试\n"
                "- 需求模块：账号与权限\n"
                "- 关联目标：REQ-LOGIN-001、REQ-LOGIN-002\n\n"
                "## 目标\n\n"
                "确认登录功能满足门店业务要求。\n\n"
                "## 验证\n\n"
                "登录成功、失败提示和移动端布局均通过验收。\n",
                encoding="utf-8",
            )
            (task_briefs / "WI-001-T00.md").write_text(
                "# WI-001-T00：旧登录设计任务\n\n"
                "- 状态：in_progress\n"
                "- 类型：界面设计\n"
                "- 需求模块：账号与权限\n\n"
                "## 目标\n\n"
                "保留历史任务简报，但不能冒充当前正在执行的任务。\n",
                encoding="utf-8",
            )
            (task_briefs / "WI-001-T02.md").write_text(
                "# WI-001-T02：验证登录审计和会话安全\n\n"
                "- 状态：registered_backlog\n"
                "- 任务层级：requirement\n"
                "- task_type：验收测试\n"
                "- 需求模块：账号与权限\n"
                "- 关联目标：REQ-LOGIN-002、REQ-LOGIN-003\n\n"
                "## 目标\n\n"
                "验证登录审计和会话安全要求。\n",
                encoding="utf-8",
            )
            (work_item / "ledger.jsonl").write_text(
                json.dumps(
                    {
                        "time": "2026-07-28T23:58:00+08:00",
                        "task_card_id": "WI-001-T01",
                        "event_type": "verification_completed",
                        "status": "verification_passed",
                        "outputs": ["build/login.html"],
                        "evidence": "evidence/login-check.md",
                        "commits": ["abc1234"],
                    },
                    ensure_ascii=False,
                )
                + "\n"
                + json.dumps(
                    {
                        "time": "2026-07-29T00:01:00+08:00",
                        "task_card_id": "WI-001-T01",
                        "task_title": "完成登录流程验收",
                        "status": "ready_for_review",
                        "next_required_action": "request_independent_review",
                        "outputs": ["build/login-v2.html"],
                        "evidence": "evidence/login-review.md",
                        "commits": ["def4567"],
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            completed = project / ".factory" / "workitems" / "WI-OLD"
            completed.mkdir()
            (completed / "brief.md").write_text(
                "# WI-OLD\n\n- 名称：旧登录方案\n- 阶段：DESIGN\n- 状态：superseded\n",
                encoding="utf-8",
            )
            (completed / "ledger.jsonl").write_text(
                json.dumps(
                    {
                        "time": "2026-07-27T10:00:00+08:00",
                        "event_type": "work_item_superseded",
                        "status": "superseded",
                        "outputs": ["docs/login-v1.md"],
                        "commits": ["old1234"],
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            attention = project / ".factory" / "workitems" / "WI-DECISION"
            attention.mkdir()
            (attention / "brief.md").write_text(
                "# WI-DECISION：确认登录方式\n\n"
                "- 阶段：REQUIREMENTS\n"
                "- 状态：needs_user_input\n"
                "- 里程碑：登录方案确认\n"
                "- 目标日期：2026-07-31\n",
                encoding="utf-8",
            )
            (attention / "ledger.jsonl").write_text(
                json.dumps(
                    {
                        "time": "2026-07-29T00:00:00+08:00",
                        "actor": "产品负责人",
                        "actor_type": "human",
                        "event_type": "decision_requested",
                        "status": "approved_pending_human_ui_acceptance",
                        "stop_reason": "等待产品负责人选择登录方式",
                        "next_required_action": "确认短信或密码登录",
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            maintenance = project / ".factory" / "workitems" / "WI-MAINT"
            maintenance_tasks = maintenance / "task-briefs"
            maintenance_tasks.mkdir(parents=True)
            (maintenance / "brief.md").write_text(
                "# WI-MAINT：改进项目看板\n\n"
                "- 阶段：IMPLEMENTATION\n"
                "- 状态：in_progress\n"
                "- 用户目标：让负责人更快看懂项目状态。\n",
                encoding="utf-8",
            )
            (maintenance_tasks / "WI-MAINT-T01.md").write_text(
                "# WI-MAINT-T01：重做看板内容\n\n"
                "- 状态：in_progress\n"
                "- 类型：UI 实现\n"
                "- 需求模块：项目管理\n\n"
                "## 目标\n\n"
                "把内部日志改成负责人可读内容。\n",
                encoding="utf-8",
            )
            (maintenance / "ledger.jsonl").write_text(
                json.dumps(
                    {
                        "time": "2026-07-29T00:02:00+08:00",
                        "task_card_id": "WI-MAINT-T01",
                        "task_title": "重做看板内容",
                        "status": "in_progress",
                        "next_required_action": "完成负责人视图",
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            commit_ready = project / ".factory" / "workitems" / "WI-COMMIT"
            commit_ready_tasks = commit_ready / "task-briefs"
            commit_ready_tasks.mkdir(parents=True)
            (commit_ready / "brief.md").write_text(
                "# WI-COMMIT：提交登录验收结果\n\n"
                "- 阶段：IMPLEMENTATION\n"
                "- 状态：approved_ready_for_exact_local_commit\n"
                "- 用户目标：保留已批准成果的精确版本。\n",
                encoding="utf-8",
            )
            (commit_ready_tasks / "WI-COMMIT-T01.md").write_text(
                "# WI-COMMIT-T01：提交已批准登录成果\n\n"
                "- 状态：approved_ready_for_exact_local_commit\n\n"
                "## 目标\n\n"
                "完成已批准候选的本地提交。\n",
                encoding="utf-8",
            )
            (commit_ready / "ledger.jsonl").write_text(
                json.dumps(
                    {
                        "time": "2026-07-29T00:04:00+08:00",
                        "task_card_id": "WI-COMMIT-T01",
                        "status": "approved_ready_for_exact_local_commit",
                        "next_required_action": "完成本地提交",
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            closed = project / ".factory" / "workitems" / "WI-CLOSED"
            closed_tasks = closed / "task-briefs"
            closed_tasks.mkdir(parents=True)
            (closed / "brief.md").write_text(
                "# WI-CLOSED：已关闭流程任务\n\n"
                "- 阶段：IMPLEMENTATION\n"
                "- 状态：closed\n"
                "- 用户目标：保证关闭状态不会被收尾审计重开。\n",
                encoding="utf-8",
            )
            (closed_tasks / "FLOW-TASK-015.md").write_text(
                "# FLOW-TASK-015：关闭流程任务\n\n"
                "- 状态：closed\n\n"
                "## 目标\n\n"
                "完成流程任务并保持终态。\n",
                encoding="utf-8",
            )
            (closed / "ledger.jsonl").write_text(
                json.dumps(
                    {
                        "time": "2026-07-29T00:02:30+08:00",
                        "task_card_id": "FLOW-TASK-015",
                        "event_type": "work_item_closed",
                        "status": "closed",
                    },
                    ensure_ascii=False,
                )
                + "\n"
                + json.dumps(
                    {
                        "time": "2026-07-29T00:03:00+08:00",
                        "task_card_id": "FLOW-TASK-015",
                        "event_type": "closeout_verification_ready",
                        "status": "approved_ready_for_exact_local_commit",
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            sequence = project / ".factory" / "workitems" / "WI-SEQUENCE"
            sequence_tasks = sequence / "task-briefs"
            sequence_tasks.mkdir(parents=True)
            (sequence / "brief.md").write_text(
                "# WI-SEQUENCE：连续交付登录任务\n\n"
                "- 阶段：IMPLEMENTATION\n"
                "- 状态：in_progress\n"
                "- 用户目标：一个任务完成后继续同一工作项的下一任务。\n",
                encoding="utf-8",
            )
            (sequence_tasks / "WI-SEQUENCE-T01.md").write_text(
                "# WI-SEQUENCE-T01：完成登录接口\n\n"
                "- 状态：completed_local_commit_created\n"
                "- 类型：开发\n\n"
                "## 目标\n\n完成登录接口。\n",
                encoding="utf-8",
            )
            (sequence_tasks / "WI-SEQUENCE-T02.md").write_text(
                "# WI-SEQUENCE-T02：继续登录页面\n\n"
                "- 状态：in_progress\n"
                "- 类型：开发\n\n"
                "## 目标\n\n继续实现登录页面。\n",
                encoding="utf-8",
            )
            (sequence / "ledger.jsonl").write_text(
                json.dumps(
                    {
                        "time": "2026-07-29T00:03:10+08:00",
                        "task_card_id": "WI-SEQUENCE-T01",
                        "event_type": "task_local_commit_created",
                        "status": "completed_local_commit_created",
                    },
                    ensure_ascii=False,
                )
                + "\n"
                + json.dumps(
                    {
                        "time": "2026-07-29T00:03:20+08:00",
                        "task_card_id": "WI-SEQUENCE-T02",
                        "event_type": "task_started",
                        "status": "in_progress",
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            (project / ".factory" / "workitems" / "implementation").mkdir()

            first = self._run(project)
            second = self._run(project)
            relative = self._run(project, "--relative-paths")

            self.assertEqual(first["status"], "success")
            self.assertFalse(first["cache_hit"])
            self.assertTrue(second["cache_hit"])
            self.assertEqual(relative["html_path"], ".factory/cache/site/current/index.html")
            output = project / ".factory" / "cache" / "site" / "current" / "index.html"
            site = output.parent
            pages = {
                "overview": "index.html",
                "roadmap": "roadmap.html",
                "work": "work.html",
                "decisions": "decisions.html",
                "readiness": "readiness.html",
                "documents": "documents.html",
            }
            rendered = {
                view: (site / filename).read_text(encoding="utf-8")
                for view, filename in pages.items()
            }
            html = rendered["overview"]
            for view, filename in pages.items():
                self.assertTrue((site / filename).is_file())
                self.assertIn(f'id="{view}"', rendered[view])
                self.assertIn(f'href="{filename}"', rendered[view])
                self.assertIn('aria-current="page"', rendered[view])
                for other_view in pages:
                    if other_view != view:
                        self.assertNotIn(f'id="{other_view}"', rendered[view])
            self.assertIn("让门店员工安全、高效地处理日常订单", html)
            self.assertIn("30 秒接手摘要", html)
            self.assertIn("负责人视图（6 项）", html)
            work_html = rendered["work"]
            documents_html = rendered["documents"]
            roadmap_html = rendered["roadmap"]
            self.assertIn("10 类底层内容", documents_html)
            for board_column in (
                "待开始",
                "进行中",
                "测试中",
                "待评审",
                "待确认 / 阻塞",
                "已完成",
            ):
                self.assertEqual(
                    work_html.count(f'data-board-summary="{board_column}"'),
                    1,
                )
            for rendered_page in rendered.values():
                self.assertIn('<ul class="nav-tabs">', rendered_page)
                self.assertNotIn('class="nav-menu"', rendered_page)
            self.assertIn("门店工作台是一套帮助门店员工安全处理订单的业务应用", html)
            self.assertIn("当前主线完成 2 / 5 步", roadmap_html)
            self.assertIn("2 步未开始", roadmap_html)
            self.assertEqual(roadmap_html.count('<li class="stage-card'), 5)
            self.assertEqual(roadmap_html.count('class="stage-card__link"'), 5)
            route_node_ids = (
                "PHASE-001",
                "PHASE-001-S01",
                "PHASE-002",
                "PHASE-002-S01",
                "WI-001-T01",
                "WI-001-T01-S01",
                "WI-001-T01-S02",
                "WI-001-T01-S02-A",
                "WI-001-T01-S02-B",
                "WI-001-T01-S02-C",
                "WI-001-T01-S02-D",
                "WI-001-T01-S02-E",
                "PHASE-004",
                "PHASE-004-S01",
                "PHASE-005",
            )
            for stage_id in route_node_ids:
                self.assertTrue((site / "stages" / f"{stage_id}.html").is_file())
            for stage_id in (
                "PHASE-001",
                "PHASE-002",
                "WI-001-T01",
                "PHASE-004",
                "PHASE-005",
            ):
                self.assertIn(
                    f'href="stages/{stage_id}.html"',
                    roadmap_html,
                )
            phase_3 = (site / "stages" / "WI-001-T01.html").read_text(encoding="utf-8")
            self.assertIn("登录流程验收", phase_3)
            self.assertIn("2 个直接子步骤", phase_3)
            self.assertIn("验证登录成功路径", phase_3)
            self.assertIn("完成独立验收", phase_3)
            self.assertNotIn("记录验收结论", phase_3)
            self.assertNotIn("确认业务目标", phase_3)
            self.assertNotIn("整理发布材料", phase_3)
            self.assertIn('href="../stages/WI-001-T01-S01.html"', phase_3)
            self.assertIn('href="../stages/WI-001-T01-S02.html"', phase_3)
            self.assertIn('href="../tasks/WI-001-T01.html"', phase_3)
            self.assertIn('href="../roadmap.html"', phase_3)
            route_chain = (
                ("WI-001-T01-S02", "WI-001-T01-S02-A"),
                ("WI-001-T01-S02-A", "WI-001-T01-S02-B"),
                ("WI-001-T01-S02-B", "WI-001-T01-S02-C"),
                ("WI-001-T01-S02-C", "WI-001-T01-S02-D"),
                ("WI-001-T01-S02-D", "WI-001-T01-S02-E"),
            )
            for parent_id, child_id in route_chain:
                parent_page = (site / "stages" / f"{parent_id}.html").read_text(encoding="utf-8")
                self.assertIn(f'href="../stages/{child_id}.html"', parent_page)
            self.assertIn("登录流程交付", html)
            self.assertIn("产品主线", html)
            self.assertIn("负责人当前范围", work_html)
            self.assertIn("并行范围", work_html)
            self.assertIn("产品完成率暂不可计算", html)
            self.assertIn("交付登录流程", work_html)
            self.assertIn("完成登录流程验收", work_html)
            self.assertIn("REQ-LOGIN-001", work_html)
            self.assertIn(
                '<a class="requirement-link" href="requirements/REQ-LOGIN-001.html">',
                work_html,
            )
            self.assertIn("<small>REQ-LOGIN-001</small></a>", work_html)
            self.assertEqual(
                work_html.count('data-requirement-id="REQ-LOGIN-002"'),
                1,
            )
            self.assertNotIn(
                'data-requirement-id="REQ-LOGIN-003"',
                work_html,
            )
            self.assertNotIn('href="requirements/REQ-LOGIN-003.html"', work_html)
            self.assertIn('href="tasks/WI-001-T01.html"', work_html)
            self.assertIn('href="plans/WI-001.html"', roadmap_html)
            self.assertIn(
                'class="section-action" href="roadmap.html">查看分层路线图',
                work_html,
            )
            self.assertIn(
                'class="roadmap-card__action" href="tasks/WI-COMMIT-T01.html"',
                roadmap_html,
            )
            self.assertNotIn('class="lane-card-link"', work_html)
            self.assertNotIn('class="lane-card__action"', work_html)
            self.assertNotIn('class="task-nature-group"', work_html)
            self.assertIn("项目级任务", work_html)
            self.assertIn('id="agile-board"', work_html)
            self.assertIn('<details class="board-swimlane requirement-group"', work_html)
            self.assertIn('<details class="board-swimlane work-item-group"', work_html)
            self.assertIn('class="board-swimlane__heading"', work_html)
            self.assertIn('class="swimlane-grid"', work_html)
            self.assertNotIn('class="classification-group"', work_html)
            self.assertNotIn("未拆分独立需求", work_html)
            self.assertIn("提交与收尾", work_html)
            self.assertNotIn("任务分类未登记", work_html)
            self.assertIn("P0", work_html)
            self.assertIn("需求任务", work_html)
            self.assertIn("账号与权限", work_html)
            self.assertIn("测试", work_html)
            self.assertIn("验收测试", work_html)
            board_start = work_html.index('id="agile-board"')
            history_start = work_html.index('class="board-history"', board_start)
            current_board = work_html[board_start:history_start]
            history_board = work_html[history_start:]
            self.assertNotIn('href="tasks/WI-DECISION.html"', current_board)
            self.assertNotIn('data-work-item-id="WI-MAINT"', current_board)
            self.assertNotIn('data-work-item-id="WI-SEQUENCE"', current_board)
            self.assertNotIn("旧登录方案", current_board)
            self.assertIn("旧登录方案", history_board)
            self.assertNotIn("旧登录设计任务", work_html)
            self.assertEqual(current_board.count('data-task-id="WI-001-T01"'), 1)
            self.assertEqual(current_board.count('data-task-id="WI-001-T02"'), 1)
            self.assertEqual(current_board.count('data-task-id="WI-COMMIT-T01"'), 1)
            self.assertEqual(
                work_html.count('<article class="board-card"'),
                work_html.count('class="board-card__action"'),
            )
            self.assertEqual(
                work_html.count('<article class="board-card"'),
                work_html.count('class="board-card__tags tags"'),
            )
            self.assertNotIn(
                ".board-card{min-width:0;padding:12px;border:1px",
                work_html,
            )
            self.assertEqual(
                roadmap_html.count('<article class="list-card'),
                roadmap_html.count('class="roadmap-card__action"'),
            )
            self.assertNotIn('href="tasks/FLOW-TASK-015.html"', current_board)
            self.assertIn('href="tasks/FLOW-TASK-015.html"', history_board)
            self.assertNotIn('href="tasks/WI-SEQUENCE-T01.html"', current_board)
            self.assertNotIn('href="tasks/WI-SEQUENCE-T02.html"', current_board)
            self.assertNotIn('class="empty-cell"', current_board)
            self.assertNotIn('class="board-card__relations"', current_board)
            self.assertNotIn('class="board-status-head"', work_html)
            self.assertNotIn('class="board-jumps"', work_html)
            self.assertIn("等待独立评审", html)
            self.assertIn("唯一下一动作：完成独立评审", html)
            self.assertNotIn("旧会话动作，不得覆盖最新 ledger", html)
            self.assertIn("业务分组内只显示实际存在的状态", work_html)
            self.assertNotIn("移动端可横向滑动", work_html)
            self.assertIn("未纳入当前会话 / 后续工作", work_html)
            self.assertNotIn("登录方案确认", html)
            self.assertNotIn("等待产品负责人选择登录方式", html)
            self.assertIn("evidence/login-check.md", documents_html)
            self.assertIn("build/login.html", documents_html)
            self.assertIn("abc1234", documents_html)
            self.assertLess(
                documents_html.index("evidence/login-review.md"),
                documents_html.index("evidence/login-check.md"),
            )
            self.assertLess(
                documents_html.index("build/login-v2.html"),
                documents_html.index("build/login.html"),
            )
            self.assertLess(documents_html.index("def4567"), documents_html.index("abc1234"))
            for category, label, path in (
                ("需求文档", "产品需求（PRD）", "docs/04-product/prd.md"),
                ("设计文档", "解决方案总览", "docs/05-design/solution-overview.md"),
                (
                    "开发文档",
                    "应用开发指南",
                    "docs/03-developer-guide/application-development.md",
                ),
                ("测试文档", "测试计划", "docs/06-delivery/test-plan.md"),
                ("发布与运维", "发布说明", "docs/06-delivery/release-notes.md"),
            ):
                self.assertIn(category, documents_html)
                self.assertIn(label, documents_html)
                self.assertIn(path, documents_html)
            self.assertIn('href="documents/PRD-STORE-001.html"', documents_html)
            self.assertNotIn('href="../../../../docs/04-product/prd.md"', documents_html)
            self.assertNotIn("implementation · implementation", html)
            self.assertIn('class="skip-link"', html)
            self.assertIn('<main id="main">', html)
            self.assertNotIn(str(ROOT / "src"), html)

            task_detail = (output.parent / "tasks" / "WI-001-T01.html").read_text(encoding="utf-8")
            self.assertIn("完成登录流程验收", task_detail)
            self.assertIn('href="../requirements/REQ-LOGIN-001.html"', task_detail)
            self.assertIn('href="../plans/WI-001.html"', task_detail)
            self.assertIn('href="../stages/WI-001-T01.html"', task_detail)
            self.assertIn('href="../work.html"', task_detail)
            self.assertIn("每日路线与进展", task_detail)
            self.assertIn("2026-07-29", task_detail)
            self.assertIn("后续路线：完成独立评审", task_detail)
            backlog_detail = (output.parent / "tasks" / "WI-001-T02.html").read_text(
                encoding="utf-8"
            )
            self.assertIn('href="../requirements/REQ-LOGIN-003.html"', backlog_detail)

            requirement_detail = (output.parent / "requirements" / "REQ-LOGIN-001.html").read_text(
                encoding="utf-8"
            )
            self.assertIn("安全登录", requirement_detail)
            self.assertIn("作为门店员工", requirement_detail)
            self.assertIn('href="../work.html"', requirement_detail)

            plan_detail = (output.parent / "plans" / "WI-001.html").read_text(encoding="utf-8")
            self.assertIn("登录流程实施计划", plan_detail)
            self.assertIn("门店试点", plan_detail)
            self.assertIn('href="../roadmap.html"', plan_detail)
            self.assertIn('href="../tasks/WI-001-T01.html"', plan_detail)
            self.assertIn("计划阶段与任务", plan_detail)
            for stage_id in (
                "PHASE-001",
                "PHASE-002",
                "WI-001-T01",
                "PHASE-004",
                "PHASE-005",
            ):
                self.assertIn(f'id="stage-{stage_id}"', plan_detail)
            self.assertIn("任务尚未拆分", plan_detail)

            document_detail = (output.parent / "documents" / "PRD-STORE-001.html").read_text(
                encoding="utf-8"
            )
            self.assertIn("<h1", document_detail)
            self.assertIn("<table", document_detail)
            self.assertNotIn("# 门店工作台产品需求", document_detail)
            self.assertIn('href="../documents.html"', document_detail)

    def test_explicit_reopen_and_changes_requested_override_terminal_state(self) -> None:
        effective_event = runpy.run_path(str(SCRIPT))["_effective_event"]
        closed = {
            "time": "2026-07-29T00:00:00+08:00",
            "event_type": "work_item_closed",
            "status": "closed",
        }

        reopened = effective_event(
            [
                closed,
                {
                    "time": "2026-07-29T00:01:00+08:00",
                    "event_type": "work_item_reopened",
                    "status": "in_progress",
                },
            ],
            work_item=True,
        )
        changes_requested = effective_event(
            [
                closed,
                {
                    "time": "2026-07-29T00:01:00+08:00",
                    "event_type": "review_completed",
                    "status": "changes_requested",
                },
            ],
            work_item=True,
        )

        self.assertEqual(reopened["status"], "in_progress")
        self.assertEqual(changes_requested["status"], "changes_requested")

    def test_empty_project_keeps_the_complete_snapshot_structure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / ".factory").mkdir()

            self._run(project)

            site = project / ".factory" / "cache" / "site" / "current"
            for section_id, filename in (
                ("overview", "index.html"),
                ("roadmap", "roadmap.html"),
                ("work", "work.html"),
                ("decisions", "decisions.html"),
                ("readiness", "readiness.html"),
                ("documents", "documents.html"),
            ):
                html = (site / filename).read_text(encoding="utf-8")
                self.assertIn(f'id="{section_id}"', html)
                self.assertTrue(
                    any(marker in html for marker in ("尚未登记", "当前没有已登记", "暂无任务"))
                )

    def test_failures_use_receipt_and_output_cannot_escape_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project = base / "project"
            factory = project / ".factory"
            factory.mkdir(parents=True)
            (factory / "cache").write_text("conflict", encoding="utf-8")

            conflict = self._raw_run(project)
            self.assertEqual(conflict.returncode, 2)
            self.assertEqual(json.loads(conflict.stdout)["status"], "failed")
            self.assertNotIn("Traceback", conflict.stderr)

            (factory / "cache").unlink()
            outside = base / "outside"
            outside.mkdir()
            (factory / "cache").symlink_to(outside, target_is_directory=True)

            escaped = self._raw_run(project)
            self.assertEqual(escaped.returncode, 2)
            self.assertIn("outside project root", json.loads(escaped.stdout)["error"])
            self.assertFalse((outside / "site" / "current" / "index.html").exists())

            metadata_project = base / "metadata-project"
            current = metadata_project / ".factory" / "cache" / "site" / "current"
            current.mkdir(parents=True)
            (current / "index.html").write_text("old", encoding="utf-8")
            (current / "snapshot.json").write_text("[]\n", encoding="utf-8")

            invalid_metadata = self._raw_run(metadata_project)
            self.assertEqual(invalid_metadata.returncode, 2)
            self.assertIn(
                "metadata must be an object",
                json.loads(invalid_metadata.stdout)["error"],
            )
            self.assertNotIn("Traceback", invalid_metadata.stderr)

    def _run(self, project: Path, *arguments: str) -> dict[str, object]:
        result = self._raw_run(project, *arguments)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def _raw_run(self, project: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--project-root",
                str(project),
                *arguments,
            ],
            check=False,
            capture_output=True,
            text=True,
        )


if __name__ == "__main__":
    unittest.main()
