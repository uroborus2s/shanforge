from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def table_rows(content: str, heading: str) -> list[tuple[str, ...]]:
    section = content.split(heading, maxsplit=1)[1]
    ends = [position for marker in ("\n### ", "\n## ") if (position := section.find(marker)) >= 0]
    if ends:
        section = section[: min(ends)]
    lines = [line for line in section.splitlines() if line.startswith("|")]
    return [
        tuple(cell.strip().strip("`") for cell in line.strip("|").split("|"))
        for line in lines[2:]
    ]


def test_sol_owns_classification_and_worker_selection() -> None:
    formal = read("docs/05-design/workflow-execution-design.md")
    controller = read("skills/using-shanforge/SKILL.md")

    for content in (formal, controller):
        for phrase in (
            "control_model: gpt-5.6-sol",
            "task_complexity: simple | standard | complex",
            "risk_level: low | medium | high",
            "execution_model: gpt-5.6-luna | gpt-5.6-terra",
            "execution_authorized: true | false",
            "Sol 是唯一总体设计、任务分级和模型路由 owner",
            "Terra 和 Luna 不得重新分级",
        ):
            assert phrase in content


def test_deterministic_route_maps_only_simple_low_work_to_luna() -> None:
    controller = read("skills/using-shanforge/SKILL.md")

    assert "`simple + low`" in controller
    assert "`gpt-5.6-luna`" in controller
    assert "`standard | complex | medium | high`" in controller
    assert "`gpt-5.6-terra`" in controller
    assert "信息不足时按 `complex`" in controller
    assert "高风险 Gate 未闭合时 `execution_authorized: false`" in controller


def test_route_matrix_and_escalations_are_fail_closed() -> None:
    controller = read("skills/using-shanforge/SKILL.md")
    executor = read("skills/subagent-driven-development/SKILL.md")

    assert table_rows(controller, "### 执行模型决策表") == [
        ("simple", "low", "gpt-5.6-luna"),
        ("*", "*", "gpt-5.6-terra"),
    ]
    assert table_rows(controller, "### 执行授权决策表") == [
        ("closed", "complete", "true", "dispatch"),
        ("*", "*", "false", "do_not_dispatch"),
    ]
    assert table_rows(executor, "### 升级信号决策表") == [
        (signal, "stop_and_return_to_sol")
        for signal in (
            "scope_expanded",
            "input_conflict",
            "risk_increased",
            "verification_failed_twice",
            "human_gate",
        )
    ]
    assert "execution_authorized != true -> do_not_dispatch" in executor
    assert "standard + low -> gpt-5.6-luna" not in controller


def test_route_package_is_persisted_without_worker_reclassification() -> None:
    planner = read("skills/writing-plans/SKILL.md")
    template = read("skills/writing-plans/references/task-brief-template.md")
    executor = read("skills/subagent-driven-development/SKILL.md")

    for phrase in (
        "control_model",
        "task_complexity",
        "risk_level",
        "execution_model",
        "execution_authorized",
        "route_reason",
        "escalation_triggers",
    ):
        assert phrase in template

    assert "原样复制模型路由字段，不重新计算" in planner
    assert "Terra/Luna 只消费已授权路由包" in executor
    assert "scope_expanded" in executor
    assert "input_conflict" in executor
    assert "risk_increased" in executor
    assert "verification_failed_twice" in executor
    assert "human_gate" in executor


def test_user_guide_and_skill_metadata_disclose_host_capability_boundary() -> None:
    guide = read("docs/02-user-guide/user-guide.md")
    metadata = read("skills/using-shanforge/agents/openai.yaml")

    for phrase in (
        "gpt-5.6-sol",
        "gpt-5.6-terra",
        "gpt-5.6-luna",
        "当前 Codex 宿主能力",
        "不代表公开 API 型号、价格或可用性承诺",
    ):
        assert phrase in guide

    assert "Sol 控制并分级" in metadata
    assert "Terra/Luna 执行" in metadata
