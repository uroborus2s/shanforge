from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FORMAL_CONTRACT_PATH = "docs/05-design/workflow-execution-design.md"
CANDIDATE_PATH = (
    ".factory/workitems/FLOW-CONTRACT-001/drafts/"
    "FLOW-TASK-015-workflow-contract.v1.2.0.candidate.md"
)

EXPECTED_BEHAVIORS = {
    "SB-EXPLAIN": "解释",
    "SB-CLARIFY": "澄清",
    "SB-REQUIREMENT": "需求",
    "SB-CHANGE": "变更",
    "SB-DESIGN": "方案",
    "SB-PLAN": "计划",
    "SB-EXECUTE": "执行",
    "SB-BUG": "Bug",
    "SB-TEST": "测试",
    "SB-REVIEW": "Review",
    "SB-VERIFY": "验证",
    "SB-COMMIT": "提交",
    "SB-STATUS": "状态查看",
    "SB-RESUME": "恢复",
    "SB-PAUSE": "暂停",
    "SB-DEPRECATE": "废弃",
}

CURRENT_BEHAVIORS = EXPECTED_BEHAVIORS | {
    "SB-REMOTE": "远端交付",
    "SB-RELEASE": "发布部署",
}

EXPECTED_WORKFLOWS = {
    "tracking-identity-workflow",
    "direct-answer-workflow",
    "requirements-workflow",
    "change-control-workflow",
    "design-workflow",
    "planning-workflow",
    "execution-workflow",
    "debugging-workflow",
    "testing-workflow",
    "review-workflow",
    "verification-workflow",
    "commit-workflow",
    "status-memory-workflow",
}

CURRENT_WORKFLOWS = EXPECTED_WORKFLOWS | {
    "remote-pr-workflow",
    "release-workflow",
}

RUNTIME_SKILLS = {
    "skills/using-shanforge/SKILL.md": {
        "tracking-identity-workflow",
        "direct-answer-workflow",
        "change-control-workflow",
        "design-workflow",
        "remote-pr-workflow",
    },
    "skills/project-memory/SKILL.md": {"status-memory-workflow"},
    "skills/requirements-engineering/SKILL.md": {"requirements-workflow"},
    "skills/writing-plans/SKILL.md": {"planning-workflow"},
    "skills/executing-plans/SKILL.md": {"execution-workflow"},
    "skills/subagent-driven-development/SKILL.md": {"execution-workflow"},
    "skills/requesting-code-review/SKILL.md": {"review-workflow"},
    "skills/receiving-code-review/SKILL.md": {"review-workflow"},
    "skills/verification-before-completion/SKILL.md": {
        "testing-workflow",
        "verification-workflow",
    },
    "skills/release-deployment/SKILL.md": {"release-workflow"},
}

RUNTIME_POLICIES = {
    "skills/using-shanforge/SKILL.md": {
        "no_project_write",
        "create_tracking_identity",
        "project_fact_write",
        "source_or_test_write",
        "state_or_gate_write",
    },
    "skills/project-memory/SKILL.md": {
        "no_project_write",
        "state_or_gate_write",
    },
    "skills/requirements-engineering/SKILL.md": {"project_fact_write"},
    "skills/writing-plans/SKILL.md": {"project_fact_write"},
    "skills/executing-plans/SKILL.md": {"source_or_test_write"},
    "skills/subagent-driven-development/SKILL.md": {"source_or_test_write"},
    "skills/requesting-code-review/SKILL.md": {"state_or_gate_write"},
    "skills/receiving-code-review/SKILL.md": {
        "source_or_test_write",
        "state_or_gate_write",
    },
    "skills/verification-before-completion/SKILL.md": {
        "source_or_test_write",
        "state_or_gate_write",
    },
    "skills/release-deployment/SKILL.md": {"state_or_gate_write"},
}


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def markdown_table(document: str, heading: str) -> list[dict[str, str]]:
    section = document.split(heading, 1)[1].split("\n## ", 1)[0]
    lines = [line.strip() for line in section.splitlines() if line.startswith("|")]
    assert len(lines) >= 3, f"{heading} must contain a Markdown table"
    headers = [cell.strip() for cell in lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in lines[2:]:
        values = [cell.strip() for cell in line.strip("|").split("|")]
        assert len(values) == len(headers), (heading, line)
        rows.append(dict(zip(headers, values, strict=True)))
    return rows


def markdown_section(document: str, heading: str) -> str:
    return document.split(heading, 1)[1].split("\n## ", 1)[0]


def test_candidate_defines_full_project_session_routing() -> None:
    contract = read(CANDIDATE_PATH)

    for phrase in (
        "完整软件项目会话归因模型",
        "当前消息 -> 会话行为 -> 工作流 -> 节点 -> 允许动作 -> 状态包",
        "所有完整软件项目会话必须先归因，再执行",
        "普通项目事实写入前必须验证已存在且非空的 work_item_id 和 task_card_id",
        "memory summary 不能作为项目事实写入的唯一凭据",
    ):
        assert phrase in contract


def test_candidate_behavior_map_is_complete_and_each_mapping_is_unique() -> None:
    candidate = read(CANDIDATE_PATH)
    rows = markdown_table(candidate, "## 会话行为合同")
    by_id = {row["行为 ID"].strip("`"): row for row in rows}

    assert len(rows) == len(by_id) == len(EXPECTED_BEHAVIORS)
    assert {behavior_id: row["中文名称"] for behavior_id, row in by_id.items()} == (
        EXPECTED_BEHAVIORS
    )
    assert all(row["触发谓词"] for row in rows)
    assert all(row["默认工作流"].strip("`") in EXPECTED_WORKFLOWS for row in rows)
    assert all(" 或 " not in row["默认工作流"] for row in rows)
    assert all(row["Handler"] for row in rows)


def test_candidate_workflow_contract_has_all_required_non_empty_fields() -> None:
    candidate = read(CANDIDATE_PATH)
    rows = markdown_table(candidate, "## 工作流合同")
    required = {
        "工作流 ID",
        "写策略",
        "优先级",
        "触发",
        "输入 Schema",
        "允许动作",
        "禁止动作",
        "输出 Schema",
        "Ledger event",
        "Evidence",
        "进入 Gate",
        "退出 Gate",
    }
    assert set(rows[0]) == required
    workflow_ids = {row["工作流 ID"].strip("`") for row in rows}
    assert len(rows) == len(workflow_ids) == len(EXPECTED_WORKFLOWS)
    assert workflow_ids == EXPECTED_WORKFLOWS
    for row in rows:
        for field in required:
            assert row[field], (row["工作流 ID"], field)
        if row["Ledger event"].startswith("N/A"):
            assert ":" in row["Ledger event"]
        if row["Evidence"].startswith("N/A"):
            assert ":" in row["Evidence"]


def test_candidate_defines_fail_closed_write_authorization() -> None:
    candidate = read(CANDIDATE_PATH)
    rows = markdown_table(candidate, "## 写入授权矩阵")
    by_action = {row["动作类别"].strip("`"): row for row in rows}

    assert set(by_action) == {
        "no_project_write",
        "create_tracking_identity",
        "project_fact_write",
        "source_or_test_write",
        "state_or_gate_write",
    }
    for action in (
        "project_fact_write",
        "source_or_test_write",
        "state_or_gate_write",
    ):
        assert by_action[action]["WorkItem"] == "必须已存在"
        assert by_action[action]["TaskCard"] == "必须已存在"
        assert by_action[action]["Ledger"] == "必须"
        assert by_action[action]["Memory 可单独证明"] == "否"
    create = by_action["create_tracking_identity"]
    assert "WorkItem + TaskCard + 首条 ledger" in create["唯一允许写入"]
    assert "其他写入 0 次" in create["唯一允许写入"]

    def permits(
        action: str,
        *,
        work_item_id: str = "",
        task_card_id: str = "",
        ledger: bool = False,
        evidence: bool = False,
        memory_only: bool = False,
        writes: tuple[str, ...] = (),
    ) -> bool:
        policy = by_action[action]
        if action == "no_project_write":
            return not writes
        if action == "create_tracking_identity":
            return writes == ("WorkItem", "TaskCard", "首条 ledger") and ledger and evidence
        return (
            bool(work_item_id)
            and bool(task_card_id)
            and ledger
            and evidence
            and not memory_only
            and policy["Memory 可单独证明"] == "否"
        )

    assert not permits("project_fact_write", ledger=True, evidence=True)
    assert not permits(
        "project_fact_write",
        work_item_id="WI-1",
        task_card_id="TASK-1",
        ledger=True,
        memory_only=True,
    )
    assert not permits(
        "create_tracking_identity",
        ledger=True,
        evidence=True,
        writes=("WorkItem", "TaskCard", "首条 ledger", "source.py"),
    )
    assert permits(
        "source_or_test_write",
        work_item_id="WI-1",
        task_card_id="TASK-1",
        ledger=True,
        evidence=True,
        writes=("source.py",),
    )

    workflows = markdown_table(candidate, "## 工作流合同")
    reachable_policies = {
        policy.strip()
        for row in workflows
        for policy in re.findall(
            r"(?:no_project_write|create_tracking_identity|project_fact_write|"
            r"source_or_test_write|state_or_gate_write)",
            row["写策略"],
        )
    }
    assert reachable_policies == set(by_action)
    identity = next(row for row in workflows if row["工作流 ID"] == "`tracking-identity-workflow`")
    assert identity["写策略"] == "`create_tracking_identity`"
    assert "proposed_work_item_id" in identity["输入 Schema"]
    assert "proposed_task_card_id" in identity["输入 Schema"]

    status_memory = next(row for row in workflows if row["工作流 ID"] == "`status-memory-workflow`")
    assert "SB-RESUME 时必须含 work_item_id 和 task_card_id" in (status_memory["输入 Schema"])


def test_candidate_declares_per_workflow_nodes_transitions_and_human_gate_rules() -> None:
    candidate = read(CANDIDATE_PATH)
    rows = markdown_table(candidate, "## 工作流节点与转换")
    by_workflow = {row["工作流 ID"].strip("`"): row for row in rows}

    assert len(rows) == len(by_workflow) == len(EXPECTED_WORKFLOWS)
    assert set(by_workflow) == EXPECTED_WORKFLOWS
    for workflow, row in by_workflow.items():
        assert row["允许节点"]
        assert "->" in row["合法主路径"]
        assert row["停止态"]
        assert row["人工 Gate 规则"]
        if workflow == "review-workflow":
            assert "普通任务 Review 不自动进入人工 Gate" in row["人工 Gate 规则"]
    identity = by_workflow["tracking-identity-workflow"]
    assert "identity_creating" in identity["允许节点"]
    assert identity["合法主路径"].endswith("identity_readback -> reroute`")


def test_formal_contract_preserves_v1_2_baseline_and_adds_delivery_workflows() -> None:
    candidate = read(CANDIDATE_PATH)
    formal = read(FORMAL_CONTRACT_PATH)

    assert "- 候选 ID：`FLOW-TASK-015-C001`" in candidate
    assert "- 候选版本：`v1.2.0`" in candidate
    assert "- 候选状态：`ready_for_same_reviewer_rereview`（未生效）" in candidate
    assert f"- 正式基线路径：`{FORMAL_CONTRACT_PATH}`" in candidate
    assert "- 正式基线版本：`v1.1.0`" in candidate
    match = re.search(r"- 正式基线 SHA-256：`([0-9a-f]{64})`", candidate)
    assert match
    assert match.group(1) == ("5769beb3478d528a0b0888328381173aa799e1e137925fc393bd98d97d3eb687")
    assert hashlib.sha256((REPO_ROOT / CANDIDATE_PATH).read_bytes()).hexdigest() == (
        "3d5f4cbabda86312da0603db5662175453d12dd5966c788301b0c79c2cb4992f"
    )
    assert "批准前不得修改正式文档或同步 runtime Skill" in candidate
    assert "| 正式版本 | `v1.4.0` |" in formal
    assert "| 来源候选 | `2026-08-08 用户阶段门控与闭环优化决策` |" in formal
    assert "| 发布事务 | `N/A（直接策略变更）` |" in formal
    assert "| `v1.2.0` | 发布完整项目会话归因" in formal
    assert "| `v1.3.0` | 开发期轻门禁" in formal
    assert "| `v1.3.1` | 明确低、中、高风险任务" in formal
    assert "| `v1.4.0` | 增加设计至生产阶段门" in formal
    assert formal.count("## 完整软件项目会话归因模型") == 1
    assert formal.count("## 工作流合同") == 1
    assert "| 当前版本 | `0.2.0` |" not in formal
    formal_behaviors = {
        row["行为 ID"].strip("`") for row in markdown_table(formal, "## 会话行为合同")
    }
    formal_workflows = {
        row["工作流 ID"].strip("`") for row in markdown_table(formal, "## 工作流合同")
    }
    assert formal_behaviors == set(CURRENT_BEHAVIORS)
    assert formal_workflows == CURRENT_WORKFLOWS
    assert set(EXPECTED_BEHAVIORS) < formal_behaviors
    assert EXPECTED_WORKFLOWS < formal_workflows
    assert markdown_table(formal, "## 写入授权矩阵") == markdown_table(candidate, "## 写入授权矩阵")
    for obsolete_rule in (
        "Reviewer `approved` 后仍必须进入人工确认门",
        "`ReviewDecision=approved` 只能把 WorkflowRun 推到 `pending_human_confirmation`",
    ):
        assert obsolete_rule not in formal
    for phrase in (
        "route_kind: tracking_identity_intake",
        "proposed_work_item_id: <new non-empty ID>",
        "proposed_task_card_id: <new non-empty ID>",
        "write_policy: create_tracking_identity",
        "成功后必须使用已回读身份重新路由原始行为",
    ):
        assert phrase in candidate
        assert phrase in formal


def test_formal_contract_and_router_define_deterministic_risk_levels() -> None:
    formal = read(FORMAL_CONTRACT_PATH)
    router = read("skills/using-shanforge/SKILL.md")

    for content in (formal, router):
        for phrase in (
            "高风险优先、低风险全量满足、其余中风险",
            "禁止按代码行数、文件数或预计工时分级",
            "任一条件命中即为高风险",
            "全部条件满足才是低风险",
            "未命中高风险且未满足全部低风险条件",
            "信息不足时不得判为低风险",
        ):
            assert phrase in content


def test_runtime_skills_expose_the_minimum_route_and_result_contract() -> None:
    for path, workflows in RUNTIME_SKILLS.items():
        skill = read(path)
        heading_match = re.search(r"^## v[0-9.]+ 运行时路由合同$", skill, re.MULTILINE)
        assert heading_match, path
        runtime_contract = markdown_section(skill, heading_match.group())
        for workflow in workflows:
            assert workflow in runtime_contract, (path, workflow)
        for policy in RUNTIME_POLICIES[path]:
            assert policy in runtime_contract, (path, policy)
        for field in (
            "work_item_id",
            "task_card_id",
            "allowed_paths",
            "forbidden_actions",
            "current_gate",
            "write_policy",
            "outputs",
            "evidence",
            "ledger_event",
            "gate",
            "next_required_action",
        ):
            assert field in runtime_contract, (path, field)

    router = read("skills/using-shanforge/SKILL.md")
    for behavior_id in CURRENT_BEHAVIORS:
        assert behavior_id in router
    for phrase in (
        "route_kind: tracking_identity_intake",
        "write_policy: create_tracking_identity",
        "原子创建 WorkItem、TaskCard 和首条 ledger",
        "readback",
        "重新路由原始行为",
    ):
        assert phrase in router
    formal_routes = {
        row["行为 ID"].strip("`"): (
            row["默认工作流"].strip("`"),
            row["默认写策略"].strip("`"),
        )
        for row in markdown_table(read(FORMAL_CONTRACT_PATH), "## 会话行为合同")
    }
    runtime_routes = {}
    for row in markdown_table(router, "## v1.3.0 运行时路由合同"):
        for behavior_id in re.findall(r"SB-[A-Z]+", row["behavior_id"]):
            runtime_routes[behavior_id] = (
                row["workflow_id"].strip("`"),
                row["write_policy"].strip("`"),
            )
    assert runtime_routes == formal_routes


def test_flow_task_015_is_registered_as_closed_after_local_commit() -> None:
    task = read(".factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-015.md")
    queue = read(".factory/workitems/FLOW-CONTRACT-001/implementation-queue.md")
    ledger = read(".factory/workitems/FLOW-CONTRACT-001/ledger.jsonl")
    tests_summary = read(".factory/memory/tests.summary.md")
    events = [json.loads(line) for line in ledger.splitlines() if '"task":"FLOW-TASK-015"' in line]
    latest_status = events[-1]["status"]

    assert "完整软件项目会话行为与工作流归因契约" in task
    assert "状态：`completed_local_commit_created`" in task
    assert "`FLOW-TASK-015`" in queue
    assert f"- 当前阶段：`FLOW-TASK-015_{latest_status}`" in queue
    task_row = next(line for line in queue.splitlines() if "| 15 |" in line)
    assert f"`{latest_status}`" in task_row
    assert "pending_human_confirmation" not in task_row
    assert "FLOW-TASK-015" in tests_summary
    assert "57 passed" in tests_summary


def test_delivery_stage_gate_bug_loop_and_release_receipt_are_closed() -> None:
    formal = read(FORMAL_CONTRACT_PATH)
    router = read("skills/using-shanforge/SKILL.md")
    debugging = read("skills/systematic-debugging/SKILL.md")
    tdd = read("skills/tdd-workflow/SKILL.md")
    api = read("skills/api-design/SKILL.md")
    verification = read("skills/verification-before-completion/SKILL.md")
    test_plan = read("docs/06-delivery/test-plan.md")
    report_template = read("skills/document-templates/assets/templates/05-quality/test-report.md")
    release = read("skills/release-deployment/SKILL.md")

    for phrase in (
        "设计 -> 开发 -> 测试 -> 发布 -> 生产观察",
        "stale",
        "revalidated",
        "superseded",
    ):
        assert phrase in formal
    for phrase in (
        "业务目标、范围或验收标准变化",
        "测试预期、夹具或脚本错误",
        "release-deployment",
    ):
        assert phrase in router
    for phrase in ("fault_owner", "低、中风险不新增人工 Gate", "高风险依次等待"):
        assert phrase in debugging
    assert "单次缺陷修复不默认运行全仓测试" in tdd
    assert "参数 / body fixture" in api
    assert "最终候选，再运行一次完整必需发布测试" in verification
    assert "轻量测试闭环（2026-08-08 已批准生效）" in test_plan
    assert "不得记录完整内部 URL、IP、端口、凭证、令牌、DSN" in report_template
    for phrase in ("显式人工授权", "released | rolled_back | blocked", "不发明脚本"):
        assert phrase in release
