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
    assert config["model"] == "gpt-5.6-sol"
    assert config["model_reasoning_effort"] == "high"
    assert config["agents"] == {"enabled": True, "max_concurrent_threads_per_session": 3}

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


def test_strict_dispatch_table_requires_workflow_policy_and_authorization_together() -> None:
    controller = read("skills/using-shanforge/SKILL.md")
    tools_contract = read("skills/using-shanforge/references/codex-tools.md")

    rows = markdown_table_rows_containing(controller, "workflow_id=execution-workflow")
    assert rows == [
        (
            "`workflow_id` / `write_policy` 与声明分支不匹配，或多个分支可命中",
            "`none`",
            "`false / direct`；`input_conflict, do_not_dispatch`",
            "N/A，交还 Sol",
        ),
        (
            (
                "`workflow_id=execution-workflow`、`write_policy=source_or_test_write` 且 "
                "`execution_authorized=true`"
            ),
            "`worker`",
            "`true / subagent`",
            "`simple + low` 为 Luna/`low`；其余为 Terra/`medium`",
        ),
        (
            "`workflow_id=review-workflow`、`write_policy=state_or_gate_write`、`reviewer_type=independent_subagent`、身份/范围完整且实现/验证完成",
            "`reviewer`",
            "`true / subagent`",
            "Terra/`high`，只读",
        ),
        ("`*`", "`none`", "`false / direct`", "N/A，仍由 Sol 控制"),
    ]
    conflict_row = rows[0]
    assert all(
        term in " ".join(conflict_row)
        for term in ("input_conflict", "do_not_dispatch", "Sol")
    )
    assert "`workflow_id` / `write_policy` 与声明分支不匹配，或多个分支可命中" in tools_contract


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
        "父 Sol 先生成稳定 `dispatch_id`",
        (
            "message: <dispatch_id + 完整 task brief + allowed_paths + forbidden_actions + "
            "verification commands + status return format>"
        ),
        "model: <execution_model>",
        "reasoning_effort: <requested_reasoning_effort>",
        'fork_turns: "none"',
        "`status: accepted` 只表示工具调用已成功接受，不是子代理完成态。",
        "source: parent_tool_receipt",
    ):
        assert phrase in tools_contract

    assert "不得虚构模型内部身份" in tools_contract
    assert "父 Sol 必须在调用前生成稳定 `dispatch_id`" in executor
    assert "`accepted` 不是子代理完成态" in executor


def test_dispatch_failures_are_closed_without_model_substitution_or_inline_work() -> None:
    tools_contract = read("skills/using-shanforge/references/codex-tools.md")
    checklist = read("skills/subagent-driven-development/references/status-handling-checklist.md")

    assert "结果只能是 `dispatch_failed` 或 `worker_unavailable` 并交还 Sol" in tools_contract
    assert "禁止用 Sol\n代写、替换模型" in tools_contract
    assert "不得换模型或由 Sol 代写" in checklist
    assert "fallback" not in checklist.lower()


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
        "gpt-5.6-sol",
        "gpt-5.6-terra",
        "gpt-5.6-luna",
        "当前 Codex 宿主能力",
        "不代表公开 API 型号、价格或可用性承诺",
    ):
        assert phrase in guide


def test_user_guide_and_design_distinguish_independent_review_from_direct_work() -> None:
    guide = read("docs/02-user-guide/user-guide.md")
    design = read("docs/05-design/workflow-execution-design.md")

    assert "真实子代理派发有两个互斥分支" in guide
    assert "已授权源码或测试写入是 worker" in guide
    assert "独立只读 review 是 reviewer，固定 Terra（high）" in guide
    assert "非独立 review、Gate 和最终收口仍由 Sol 控制" in guide
    assert "派发分支按顺序互斥" in design
    assert "`dispatch_role: worker, dispatch_required: true, dispatch_mode: subagent`" in design
    assert "`dispatch_role: reviewer, true, subagent`" in design
    assert "`dispatch_role: none, false, direct`" in design
