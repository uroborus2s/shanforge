from pathlib import Path

base = Path(__file__).parents[1]
report = (base / "reports" / "EAD-TASK-003-raci-and-gate-contract.md").read_text()
t02_report = (
    base / "reports" / "EAD-TASK-002-enterprise-delivery-data-contract.md"
).read_text()

roles = {
    "business_owner",
    "operations_owner",
    "project_owner",
    "development_owner",
    "test_owner",
    "release_owner",
}


def cells(line: str) -> list[str]:
    return [value.strip().strip("`") for value in line.strip().strip("|").split("|")]


raci_rows = [
    cells(line) for line in report.splitlines() if line.startswith("| RAC-")
]
assert len(raci_rows) == 14
for row in raci_rows:
    assignments = row[2:]
    assert len(assignments) == 6
    assert sum("A" in value.split("/") for value in assignments) == 1
    assert sum("R" in value.split("/") for value in assignments) >= 1

gate_rows = [
    row
    for line in report.splitlines()
    if line.startswith("| GATE-")
    and len(row := cells(line)) == 8
]
assert len(gate_rows) == 6
assert {row[0] for row in gate_rows} == {
    "GATE-REQ",
    "GATE-EST",
    "GATE-TEST",
    "GATE-REL",
    "GATE-DEF",
    "GATE-WEEK",
}
assert all(row[4] in roles for row in gate_rows)
assert all("REVISION_DIGEST_MISMATCH" in row[7] for row in gate_rows)
assert "校验 `A` 和所需 `R` 的 `human:*` actor 映射" in report

t02_transitions = {
    (row[0], row[1], row[2], row[4])
    for line in t02_report.splitlines()
    if line.startswith("| `")
    and len(row := cells(line)) == 5
    and row[0]
    in {
        "requirement_intake",
        "development_ready_package",
        "estimate_breakdown",
        "acceptance_record",
        "defect_closure",
        "weekly_dashboard",
    }
}
gate_transitions = {(row[1], row[2], row[3], row[6]) for row in gate_rows}
assert len(t02_transitions) == 45
assert len(gate_transitions) == 6
assert gate_transitions <= t02_transitions


def raci_error(assignments: list[str]) -> str | None:
    if sum("A" in value.split("/") for value in assignments) != 1:
        return "ROLE_CONFLICT"
    if sum("R" in value.split("/") for value in assignments) < 1:
        return "ROLE_CONFLICT"
    return None


required_roles = {
    "GATE-REQ": {"business_owner", "development_owner", "test_owner"},
    "GATE-EST": {"development_owner", "project_owner"},
    "GATE-TEST": {"development_owner", "test_owner"},
    "GATE-REL": {"business_owner", "test_owner", "release_owner"},
    "GATE-DEF": {"development_owner", "test_owner", "release_owner"},
    "GATE-WEEK": {"project_owner", "operations_owner"},
}
separation_pairs = {
    "GATE-TEST": {("development_owner", "test_owner")},
    "GATE-REL": {
        ("business_owner", "test_owner"),
        ("business_owner", "release_owner"),
    },
    "GATE-DEF": {
        ("release_owner", "development_owner"),
        ("release_owner", "test_owner"),
    },
}


def gate_authority_error(
    gate: str, actor_map: dict[str, str], *, customer_confirmed: bool
) -> str | None:
    if not customer_confirmed:
        return "ROLE_AUTHORITY_UNCONFIRMED"
    actors = {role: actor_map.get(role, "") for role in required_roles[gate]}
    if not all(actors.values()):
        return "ROLE_AUTHORITY_UNCONFIRMED"
    if not all(actor.startswith("human:") for actor in actors.values()):
        return "AI_DECISION_FORBIDDEN"
    if any(
        actors[left] == actors[right]
        for left, right in separation_pairs.get(gate, set())
    ):
        return "SEGREGATION_OF_DUTIES_VIOLATION"
    return None


human_actor_map = {role: f"human:pilot:{index:03}" for index, role in enumerate(roles)}
assert all(
    gate_authority_error(gate, human_actor_map, customer_confirmed=True) is None
    for gate in required_roles
)

separation_cases = []
for gate, pairs in separation_pairs.items():
    for left, right in pairs:
        actor_map = human_actor_map | {right: human_actor_map[left]}
        separation_cases.append(
            gate_authority_error(gate, actor_map, customer_confirmed=True)
        )
assert separation_cases == ["SEGREGATION_OF_DUTIES_VIOLATION"] * 5


negative_cases = [
    raci_error(["A", "A", "R", "C", "I", "I"]),
    raci_error(["A", "C", "C", "C", "I", "I"]),
    gate_authority_error("GATE-TEST", human_actor_map, customer_confirmed=False),
    gate_authority_error(
        "GATE-TEST",
        {"test_owner": human_actor_map["test_owner"]},
        customer_confirmed=True,
    ),
    gate_authority_error(
        "GATE-TEST",
        human_actor_map | {"test_owner": "agent:run:001"},
        customer_confirmed=True,
    ),
]
assert negative_cases == [
    "ROLE_CONFLICT",
    "ROLE_CONFLICT",
    "ROLE_AUTHORITY_UNCONFIRMED",
    "ROLE_AUTHORITY_UNCONFIRMED",
    "AI_DECISION_FORBIDDEN",
]

assert "pending_customer_confirmation" in report
assert "AI Agent 不可以" in report
assert "不得作为真实授权执行生产动作" in report
assert "正式启用前只需客户确认以下 6 项" in report
for rule in (
    "`development_owner != test_owner`",
    "`business_owner != test_owner`",
    "`business_owner != release_owner`",
    "`release_owner != development_owner`",
    "`release_owner != test_owner`",
):
    assert rule in report

print(
    "raci_gate_check=passed "
    f"roles={len(roles)} raci_rows={len(raci_rows)} gates={len(gate_rows)} "
    f"t02_transitions={len(t02_transitions)} "
    f"gate_transitions={len(gate_transitions)} "
    f"negative_cases={len(negative_cases)} "
    f"separation_cases={len(separation_cases)}"
)
