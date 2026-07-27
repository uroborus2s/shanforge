import copy
import hashlib
import json
from pathlib import Path

contract = (
    Path(__file__).parents[1]
    / "reports"
    / "EAD-TASK-002-enterprise-delivery-data-contract.md"
).read_text()

models = {
    "requirement_intake",
    "development_ready_package",
    "estimate_breakdown",
    "acceptance_record",
    "defect_closure",
    "weekly_dashboard",
}
agents = {
    "需求准入 Agent",
    "开发就绪 Agent",
    "估算辅助 Agent",
    "验收设计 Agent",
    "缺陷闭环 Agent",
    "周报汇总 Agent",
}
audit_fields = {
    "schema_version",
    "record_id",
    "record_revision_id",
    "previous_revision_id",
    "content_digest",
    "owner_actor_ref",
    "reviewer_actor_refs",
    "audit_events",
    "decided_by_actor_ref",
    "reviewed_revision_id",
    "reviewed_content_digest",
    "data",
}

assert all(f"`{value}`" in contract for value in models)
assert all(value in contract for value in agents)
assert all(f"`{value}`" in contract for value in audit_fields)
assert "人工上传或下载的脱敏文档" in contract
assert "Agent 不返回 `approved`" in contract
assert "数据库：无" in contract and "API：无" in contract and "UI：无" in contract

transitions = set()
for line in contract.splitlines():
    if not line.startswith("| `"):
        continue
    cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
    if len(cells) == 5 and cells[0] in models:
        transitions.add((cells[0], cells[1], cells[2], cells[4]))

required_transitions = {
    ("requirement_intake", "ready_for_business_review", "accept", "accepted"),
    (
        "development_ready_package",
        "ready_for_joint_review",
        "accept_for_estimation",
        "accepted_for_estimation",
    ),
    ("estimate_breakdown", "ready_for_technical_review", "confirm", "confirmed"),
    ("acceptance_record", "ready_for_result_review", "accept", "accepted"),
    ("acceptance_record", "rejected", "revise", "draft"),
    ("defect_closure", "closed", "reopen", "reopened"),
    ("defect_closure", "reopened", "resume_fix", "fixing"),
    ("weekly_dashboard", "ready_for_owner_review", "publish", "published"),
}
assert required_transitions <= transitions
assert {row[0] for row in transitions} == models
assert len(transitions) >= 40


def transition_allowed(model: str, source: str, event: str, target: str) -> bool:
    return (model, source, event, target) in transitions


state_negative_cases = [
    ("defect_closure", "closed", "close", "closed"),
    ("weekly_dashboard", "published", "return", "draft"),
    ("acceptance_record", "draft", "accept", "accepted"),
    ("estimate_breakdown", "draft", "confirm", "confirmed"),
]
assert all(not transition_allowed(*case) for case in state_negative_cases)
assert "INVALID_STATE" in contract
assert "UNREDACTED_INPUT" in contract


def digest(record: dict) -> str:
    payload = {
        key: record[key]
        for key in (
            "schema_version",
            "record_id",
            "record_revision_id",
            "previous_revision_id",
            "record_type",
            "source_ref",
            "source_version",
            "redaction_status",
            "owner_role",
            "owner_actor_ref",
            "related_ids",
            "evidence_refs",
            "data",
        )
    }
    payload["related_ids"] = sorted(set(payload["related_ids"]))
    payload["evidence_refs"] = sorted(set(payload["evidence_refs"]))
    # The fixture contains no floats; sorted compact JSON is its RFC 8785 byte form.
    canonical = json.dumps(
        payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode()
    return "sha256:" + hashlib.sha256(canonical).hexdigest()


def governance_error(record: dict, decision: dict) -> str | None:
    if record["redaction_status"] != "redacted_confirmed":
        return "UNREDACTED_INPUT"
    if not record.get("owner_actor_ref"):
        return "MISSING_ACTOR_ID"
    if any(not value.startswith("human:") for value in record["reviewer_actor_refs"]):
        return "AI_REVIEWER_FORBIDDEN"
    if record["version"] != "0.1.0" and not record.get("previous_revision_id"):
        return "BROKEN_REVISION_CHAIN"
    current_digest = digest(record)
    if (
        record["content_digest"] != current_digest
        or decision["reviewed_revision_id"] != record["record_revision_id"]
        or decision["reviewed_content_digest"] != current_digest
    ):
        return "REVISION_DIGEST_MISMATCH"
    return None


sample = {
    "schema_version": "ead-delivery-contract/v1",
    "record_id": "REQ-20260727-001",
    "record_revision_id": "REQ-20260727-001@0.2.0",
    "previous_revision_id": "REQ-20260727-001@0.1.0",
    "record_type": "requirement_intake",
    "source_ref": "redacted-input.xlsx#requirements",
    "source_version": "batch-1",
    "redaction_status": "redacted_confirmed",
    "owner_role": "business",
    "owner_actor_ref": "human:pilot:actor-001",
    "reviewer_actor_refs": ["human:pilot:actor-002"],
    "related_ids": [],
    "evidence_refs": ["evidence/redacted-001"],
    "data": {"business_goal": "降低需求澄清时间"},
    "status": "ready_for_business_review",
    "audit_events": [],
    "version": "0.2.0",
}
sample["content_digest"] = digest(sample)
assert (
    sample["content_digest"]
    == "sha256:da62145fcaffa8f551b082fe2f0e4c31822ecca2a962c63807b746d8b4afdcd8"
)
decision = {
    "reviewed_revision_id": sample["record_revision_id"],
    "reviewed_content_digest": sample["content_digest"],
}
assert governance_error(sample, decision) is None

with_audit = copy.deepcopy(sample)
with_audit["audit_events"].append({"event": "reviewed"})
assert digest(with_audit) == sample["content_digest"]

changed_content = copy.deepcopy(sample)
changed_content["data"]["business_goal"] = "改变后的业务目标"
assert digest(changed_content) != sample["content_digest"]

governance_negative_cases = []
for mutate, expected in (
    (lambda value: value.update(owner_actor_ref=""), "MISSING_ACTOR_ID"),
    (
        lambda value: value.update(reviewer_actor_refs=["agent:run:001"]),
        "AI_REVIEWER_FORBIDDEN",
    ),
    (lambda value: value.update(previous_revision_id=""), "BROKEN_REVISION_CHAIN"),
    (
        lambda value: value.update(redaction_status="not_confirmed"),
        "UNREDACTED_INPUT",
    ),
):
    candidate = copy.deepcopy(sample)
    mutate(candidate)
    governance_negative_cases.append(governance_error(candidate, decision))

bad_decision = copy.deepcopy(decision)
bad_decision["reviewed_content_digest"] = "sha256:" + "0" * 64
governance_negative_cases.append(governance_error(sample, bad_decision))
assert governance_negative_cases == [
    "MISSING_ACTOR_ID",
    "AI_REVIEWER_FORBIDDEN",
    "BROKEN_REVISION_CHAIN",
    "UNREDACTED_INPUT",
    "REVISION_DIGEST_MISMATCH",
]

print(
    "contract_check=passed "
    f"models={len(models)} agents={len(agents)} audit_fields={len(audit_fields)} "
    f"transitions={len(transitions)} "
    f"state_negative_cases={len(state_negative_cases)} "
    f"governance_negative_cases={len(governance_negative_cases)}"
)
