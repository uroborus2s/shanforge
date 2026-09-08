import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def read_toml(path: str) -> dict[str, object]:
    with (ROOT / path).open("rb") as file:
        return tomllib.load(file)


def ledger_events() -> list[dict[str, object]]:
    ledger = read(".factory/workitems/MODEL-DISPATCH-RUNTIME-001/ledger.jsonl")
    return [json.loads(line) for line in ledger.splitlines() if line]


def section(content: str, heading: str) -> str:
    content = content.split(heading, maxsplit=1)[1]
    ends = [
        position
        for marker in ("\n### ", "\n## ")
        if (position := content.find(marker)) >= 0
    ]
    return content[: min(ends)] if ends else content


def markdown_table_rows_containing(content: str, marker: str) -> list[tuple[str, ...]]:
    lines = content.splitlines()
    start = next(index for index, line in enumerate(lines) if marker in line)
    while start and lines[start - 1].startswith("|"):
        start -= 1
    end = start
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    table = lines[start:end]
    return [
        tuple(cell.strip() for cell in line.strip("|").split("|"))
        for line in table[2:]
    ]


def routing_fields(path: str) -> dict[str, str]:
    fields = {}
    for line in section(read(path), "## 模型路由").splitlines():
        if line.startswith("- ") and ": " in line:
            key, value = line[2:].split(": ", maxsplit=1)
            fields[key] = value.strip("`")
    return fields


def verification_commands(path: str) -> list[str]:
    commands = section(read(path), "## 验证命令")
    if "```bash" in commands:
        commands = commands.split("```bash", maxsplit=1)[1].split("```", maxsplit=1)[0]
        return [line for line in commands.splitlines() if line]
    return [
        line.removeprefix("- ").strip("`")
        for line in commands.splitlines()
        if line.startswith("- `")
    ]


def test_host_model_configuration_declares_the_three_runtime_roles() -> None:
    config = read_toml(".codex/config.toml")
    assert "model" not in config
    assert "model_reasoning_effort" not in config
    assert config["agents"] == {"enabled": True, "max_concurrent_threads_per_session": 10}

    expected_agents = {
        "luna-worker": ("gpt-5.6-luna", "low", "workspace-write"),
        "terra-worker": ("gpt-5.6-terra", "medium", "workspace-write"),
        "terra-reviewer": ("gpt-5.6-terra", "high", "read-only"),
    }
    for agent, (model, effort, sandbox) in expected_agents.items():
        settings = read_toml(f".codex/agents/{agent}.toml")
        assert settings["name"] == agent
        assert settings["description"]
        assert settings["developer_instructions"]
        actual = (
            settings["model"],
            settings["model_reasoning_effort"],
            settings["sandbox_mode"],
        )
        assert actual == (model, effort, sandbox)

    task_reader = read_toml(".codex/agents/task-reader.toml")
    assert task_reader["name"] == "task-reader"
    assert task_reader["description"]
    assert task_reader["developer_instructions"]
    assert task_reader["sandbox_mode"] == "read-only"
    assert "model" not in task_reader
    assert "model_reasoning_effort" not in task_reader


def test_current_contract_uses_parent_session_without_sol_owner_binding() -> None:
    worker_text = read(".codex/agents/luna-worker.toml") + read(".codex/agents/terra-worker.toml")
    contract = read("skills/using-shanforge/SKILL.md") + read(
        "skills/using-shanforge/references/codex-tools.md"
    )
    assert "父会话" in worker_text
    assert "父 Sol" not in worker_text
    assert "主会话" in contract
    assert "交还 Sol" not in contract
    executor = read("skills/subagent-driven-development/SKILL.md")
    assert executor.count("stop_and_return_to_parent_session") == 5
    assert "stop_and_return_to_sol" not in executor
    assert "改写主会话的裁决" in read("skills/writing-plans/SKILL.md")
    assert "改写 Sol 的裁决" not in read("skills/writing-plans/SKILL.md")


def test_formal_document_versions_match_current_work_item() -> None:
    index = read("docs/document-index.md")
    documents = (
        (
            "docs/04-product/prd.md",
            "PRD-SHANFORGE-001",
            "v5.2.0",
            "当前正式版本",
        ),
        (
            "docs/05-design/workflow-execution-design.md",
            "PROC-TASK-EXECUTION-001",
            "v2.2.0",
            "正式版本",
        ),
        (
            "docs/02-user-guide/user-guide.md",
            "DOC-USER-GUIDE-001",
            "v1.5.0",
            "正式版本",
        ),
    )
    for path, document_id, version, version_label in documents:
        content = read(path)
        assert f"`{document_id}`" in content
        assert f"| {version_label} | `{version}` |" in content
        assert "| 来源候选" in content
        assert "`MODEL-DYNAMIC-DISPATCH-001`" in content
        assert f"| `{version}` |" in content
        assert f"| `{path}` | `{document_id}` |" in index
        assert f"| `{version}` |" in next(
            line for line in index.splitlines() if f"| `{path}` |" in line
        )


def test_strict_dispatch_table_requires_workflow_policy_and_authorization_together() -> None:
    controller = read("skills/using-shanforge/SKILL.md")
    tools_contract = read("skills/using-shanforge/references/codex-tools.md")

    rows = markdown_table_rows_containing(controller, "workflow_id=execution-workflow")
    assert [row[1] for row in rows] == [
        "`none`",
        "`worker`",
        "`reviewer`",
        "`analyst`",
        "`none`",
    ]
    assert rows[1][2:] == ("`true / subagent`", "按子任务模型决策表；精确写集")
    assert rows[2][2:] == ("`true / subagent`", "按子任务模型决策表；只读")
    assert rows[3][2:] == ("`true / subagent`", "按子任务模型决策表；只读")
    assert all(term in rows[3][0] for term in ("project_workitem", "tracked_task", "父阶段"))
    conflict_row = rows[0]
    assert all(
        term in " ".join(conflict_row) for term in ("input_conflict", "do_not_dispatch", "主会话")
    )
    assert "input_conflict, do_not_dispatch" in tools_contract


def test_route_packages_require_write_policy_gate_and_dispatch_role() -> None:
    for content in (
        read("docs/05-design/workflow-execution-design.md"),
        read("skills/writing-plans/references/task-brief-template.md"),
    ):
        for field in ("write_policy", "current_gate", "dispatch_role"):
            assert f"{field}:" in content


def test_task_briefs_follow_the_worker_and_reviewer_dispatch_contracts() -> None:
    briefs = {
        "T01": (
            ".factory/workitems/MODEL-DISPATCH-RUNTIME-001/task-briefs/"
            "MODEL-DISPATCH-RUNTIME-001-T01-codex-model-config.md"
        ),
        "T02": (
            ".factory/workitems/MODEL-DISPATCH-RUNTIME-001/task-briefs/"
            "MODEL-DISPATCH-RUNTIME-001-T02-dispatch-contract.md"
        ),
        "T03": (
            ".factory/workitems/MODEL-DISPATCH-RUNTIME-001/task-briefs/"
            "MODEL-DISPATCH-RUNTIME-001-T03-routing-tests.md"
        ),
        "T04": (
            ".factory/workitems/MODEL-DISPATCH-RUNTIME-001/task-briefs/"
            "MODEL-DISPATCH-RUNTIME-001-T04-quality.md"
        ),
    }
    expected_routes = {
        "T01": ("source_or_test_write", "worker", "true", "subagent"),
        "T02": ("source_or_test_write", "worker", "true", "subagent"),
        "T03": ("source_or_test_write", "worker", "true", "subagent"),
        "T04": ("state_or_gate_write", "reviewer", "true", "subagent"),
    }
    for task, expected in expected_routes.items():
        fields = routing_fields(briefs[task])
        actual = tuple(
            fields[field]
            for field in (
                "write_policy",
                "dispatch_role",
                "dispatch_required",
                "dispatch_mode",
            )
        )
        assert actual == expected

    for task, path in briefs.items():
        content = read(briefs[task])
        commands = verification_commands(path)
        assert "## 验证命令" in content
        assert routing_fields(path)["current_gate"]
        assert commands and commands[0].startswith("uv run ")
        assert "<命令>" not in content
        assert "<期望输出>" not in content


def test_spawn_contract_binds_the_authorized_route_to_a_parent_receipt() -> None:
    tools_contract = read("skills/using-shanforge/references/codex-tools.md")
    executor = read("skills/subagent-driven-development/SKILL.md")

    for phrase in (
        "父会话生成稳定 `dispatch_id`",
        (
            "message: <dispatch_id + 完整子任务 brief + allowed_paths + forbidden_actions + "
            "verification commands + status return format>"
        ),
        "model: <execution_model>",
        "reasoning_effort: <requested_reasoning_effort>",
        'fork_turns: "none"',
        "`status: accepted` 只表示宿主接受了该请求，不是子代理完成态，",
        "source: parent_tool_receipt",
    ):
        assert phrase in tools_contract

    assert "不证明底层模型内部身份" in tools_contract
    assert "不得省略 `model` 或 `reasoning_effort`" in tools_contract
    assert "角色不可用或固定值冲突" in tools_contract
    assert "followup_task` 只能在同模型、同强度、同角色下补充上下文" in tools_contract
    assert "父会话必须在调用前生成稳定 `dispatch_id`" in executor
    assert "`accepted` 不是子代理完成态" in executor


def test_dispatch_failures_are_closed_without_model_substitution_or_inline_work() -> None:
    tools_contract = read("skills/using-shanforge/references/codex-tools.md")
    assert "结果只能是 `dispatch_failed` 或 `worker_unavailable` 并交还主会话" in tools_contract
    assert "禁止由主会话代写 worker、代替 reviewer、静默替换模型" in tools_contract


def test_ledger_records_direct_creation_worker_dispatches_and_independent_review() -> None:
    events = ledger_events()
    first_event = events[0]
    assert first_event["event_type"] == "work_item_created_and_plan_ready"
    assert {
        field: first_event[field]
        for field in ("write_policy", "dispatch_role", "dispatch_required", "dispatch_mode")
    } == {
        "write_policy": "project_fact_write",
        "dispatch_role": "none",
        "dispatch_required": False,
        "dispatch_mode": "direct",
    }

    receipts = {
        event["task_card_id"]: event
        for event in events
        if event["event_type"] == "subagent_dispatch_accepted"
    }
    expected = {
        "MODEL-DISPATCH-RUNTIME-001-T01": (
            "MODEL-DISPATCH-RUNTIME-001:T01:1",
            "gpt-5.6-luna",
            "low",
        ),
        "MODEL-DISPATCH-RUNTIME-001-T02": (
            "MODEL-DISPATCH-RUNTIME-001:T02:1",
            "gpt-5.6-terra",
            "medium",
        ),
        "MODEL-DISPATCH-RUNTIME-001-T03": (
            "MODEL-DISPATCH-RUNTIME-001:T03:1",
            "gpt-5.6-terra",
            "medium",
        ),
    }
    for task_card_id, (dispatch_id, model, effort) in expected.items():
        receipt = receipts[task_card_id]
        assert receipt["dispatch_id"] == dispatch_id
        assert receipt["requested_model"] == model
        assert receipt["requested_reasoning_effort"] == effort
        assert receipt["fork_turns"] == "none"
        assert receipt["agent_id"]
        assert receipt["status"] == "accepted"
        assert receipt["source"] == "parent_tool_receipt"

    review_receipt = next(
        event
        for event in events
        if event["event_type"] == "independent_review_dispatch_accepted"
    )
    assert review_receipt["requested_model"] == "gpt-5.6-terra"
    assert review_receipt["requested_reasoning_effort"] == "high"
    assert review_receipt["fork_turns"] == "none"
    assert review_receipt["agent_id"]
    assert review_receipt["status"] == "accepted"
    assert review_receipt["source"] == "parent_tool_receipt"
    assert review_receipt["reviewer_type"] == "independent_subagent"
    assert review_receipt["reviewer_independence_evidence"]


def test_user_guide_discloses_the_host_configuration_boundary() -> None:
    guide = read("docs/02-user-guide/user-guide.md")
    for phrase in (
        "用户所选主会话负责总体设计、任务复杂度/风险分级及最终路由",
        "子任务模型决策表",
        "当前工具能力来源",
        "TOML 校验不代表当前会话已加载该角色",
        "Ultra 是编排模式",
    ):
        assert phrase in guide


def test_user_guide_and_design_distinguish_independent_review_from_direct_work() -> None:
    guide = read("docs/02-user-guide/user-guide.md")
    design = read("docs/05-design/workflow-execution-design.md")

    assert "worker 执行已授权源码或测试写集" in guide
    assert "analyst 只在已有项目任务内回答明确的只读问题" in guide
    assert "reviewer 独立只读评审，实现者不能自批" in guide
    assert "普通 `direct_answer` / `lightweight_analysis` 不创建身份或 ledger" in design
    assert "`dispatch_role: worker, dispatch_required: true, dispatch_mode: subagent`" in design
    assert "`dispatch_role: none, false, direct`" in design
