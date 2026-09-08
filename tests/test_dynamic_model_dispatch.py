from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIELDS = (
    "dispatch_role",
    "task_complexity",
    "risk_level",
    "reasoning_demand",
    "execution_model",
    "requested_reasoning_effort",
)
CASES = (
    (
        {
            "dispatch_role": "worker",
            "task_complexity": "simple",
            "risk_level": "low",
            "reasoning_demand": "routine",
        },
        ("gpt-5.6-luna", "low"),
    ),
    (
        {
            "dispatch_role": "worker",
            "task_complexity": "standard",
            "risk_level": "medium",
            "reasoning_demand": "routine",
        },
        ("gpt-5.6-terra", "medium"),
    ),
    (
        {
            "dispatch_role": "worker",
            "task_complexity": "complex",
            "risk_level": "medium",
            "reasoning_demand": "judgment",
        },
        ("gpt-6-astra", "high"),
    ),
    (
        {
            "dispatch_role": "worker",
            "task_complexity": "simple",
            "risk_level": "high",
            "reasoning_demand": "routine",
        },
        ("gpt-6-astra", "xhigh"),
    ),
    (
        {
            "dispatch_role": "reviewer",
            "task_complexity": "simple",
            "risk_level": "low",
            "reasoning_demand": "routine",
        },
        ("gpt-5.6-terra", "high"),
    ),
    (
        {
            "dispatch_role": "reviewer",
            "task_complexity": "simple",
            "risk_level": "high",
            "reasoning_demand": "routine",
        },
        ("gpt-6-astra", "xhigh"),
    ),
    (
        {
            "dispatch_role": "reviewer",
            "task_complexity": "standard",
            "risk_level": "medium",
            "reasoning_demand": "deep",
        },
        ("gpt-6-astra", "xhigh"),
    ),
    (
        {
            "dispatch_role": "worker",
            "task_complexity": "standard",
            "risk_level": "medium",
            "reasoning_demand": "deep",
        },
        ("gpt-6-astra", "xhigh"),
    ),
    (
        {
            "dispatch_role": "worker",
            "task_complexity": "standard",
            "risk_level": "medium",
            "reasoning_demand": "extreme",
        },
        ("gpt-6-astra", "max"),
    ),
)


def decision_table() -> tuple[tuple[str, ...], tuple[tuple[str, ...], ...]]:
    content = (ROOT / "skills/using-shanforge/SKILL.md").read_text(encoding="utf-8")
    section = content.split("### 子任务模型决策表", maxsplit=1)[1].split("\n### ", maxsplit=1)[0]
    table = [line for line in section.splitlines() if line.startswith("|")]
    header = tuple(cell.strip().strip("`") for cell in table[0].strip("|").split("|"))
    rows = tuple(
        tuple(cell.strip().strip("`") for cell in line.strip("|").split("|")) for line in table[2:]
    )
    return header, rows


def select(rows: tuple[tuple[str, ...], ...], **request: str) -> tuple[str, str]:
    allowed = {
        "dispatch_role": {"worker", "analyst", "reviewer"},
        "task_complexity": {"simple", "standard", "complex"},
        "risk_level": {"low", "medium", "high"},
        "reasoning_demand": {"routine", "judgment", "deep", "extreme"},
    }
    assert all(request.get(field) in values for field, values in allowed.items())
    for row in rows:
        values = dict(zip(FIELDS, row, strict=True))
        if all(values[field] in ("*", request[field]) for field in FIELDS[:4]):
            return values["execution_model"], values["requested_reasoning_effort"]
    raise AssertionError("missing fallback row")


def assert_cases(rows: tuple[tuple[str, ...], ...]) -> None:
    for request, expected in CASES:
        assert select(rows, **request) == expected


def test_dynamic_model_decision_table_has_first_match_routes() -> None:
    header, rows = decision_table()
    assert header == FIELDS
    assert_cases(rows)
    with pytest.raises(AssertionError):
        select(
            rows,
            dispatch_role="worker",
            task_complexity="unknown",
            risk_level="unknown",
            reasoning_demand="unknown",
        )
    with pytest.raises(AssertionError):
        select(
            rows,
            dispatch_role="none",
            task_complexity="simple",
            risk_level="low",
            reasoning_demand="routine",
        )


def test_lowering_high_risk_or_reviewer_rows_fails_the_shared_oracle() -> None:
    _, rows = decision_table()
    high_risk_mutation = list(rows)
    high_risk_index = next(index for index, row in enumerate(rows) if row[2] == "high")
    high_risk_mutation[high_risk_index] = (
        *high_risk_mutation[high_risk_index][:2],
        "low",
        *high_risk_mutation[high_risk_index][3:],
    )
    with pytest.raises(AssertionError):
        assert_cases(tuple(high_risk_mutation))

    reviewer_mutation = list(rows)
    reviewer_index = next(index for index, row in enumerate(rows) if row[0] == "reviewer")
    reviewer_mutation[reviewer_index] = (
        *reviewer_mutation[reviewer_index][:4],
        "gpt-5.6-luna",
        "low",
    )
    with pytest.raises(AssertionError):
        assert_cases(tuple(reviewer_mutation))
