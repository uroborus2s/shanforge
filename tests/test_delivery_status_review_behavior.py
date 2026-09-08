"""Closed structural checks for independently collected behavior observations."""

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
CASES = REPO_ROOT / "tests/fixtures/delivery-status-review-cases.json"
OBSERVATIONS = (
    REPO_ROOT / ".factory/workitems/FLOW-STATUS-REVIEW-001/evidence/behavior-observations-v3.json"
)
EVIDENCE = REPO_ROOT / ".factory/workitems/FLOW-STATUS-REVIEW-001/evidence"
V1 = EVIDENCE / "behavior-observations.json"
RAW_INPUTS = EVIDENCE / "raw-behavior-inputs.json"
MANIFEST = EVIDENCE / "candidate-sha256.txt"
REVIEW_BRIEF = REPO_ROOT / ".factory/workitems/FLOW-STATUS-REVIEW-001/reviews/review-brief.md"


def fixture() -> dict[str, Any]:
    return json.loads(CASES.read_text(encoding="utf-8"))


def observations_by_case(
    observations: object, expected_case_ids: set[str]
) -> dict[str, dict[str, Any]] | None:
    if not isinstance(observations, list):
        return None
    found: dict[str, dict[str, Any]] = {}
    for observation in observations:
        if not isinstance(observation, dict):
            return None
        case_id = observation.get("case_id")
        if not isinstance(case_id, str) or case_id in found:
            return None
        found[case_id] = observation
    return found if set(found) == expected_case_ids else None


def valid(case: dict[str, Any], oracle: dict[str, Any], observation: dict[str, Any]) -> bool:
    allowed = {
        "case_id",
        "candidate_id",
        "original_response",
        "project_completion",
        "overall_phase",
        "current_activity",
        "scope_remaining",
        "approved_product_remaining",
        "unknown_unverified_or_not_started",
        "unmapped_requirements",
        "review_decision",
        "finding_ids",
        "new_findings",
        "delta_reason",
        "scope_reconciliation",
        "next_action",
        "excerpts",
    }
    if set(observation) - allowed or observation.get("case_id") != case["id"]:
        return False
    if observation.get("candidate_id") != case["facts"]["candidate_id"]:
        return False
    response = observation.get("original_response")
    if not isinstance(response, str) or not response:
        return False
    excerpts = observation.get("excerpts")
    if not isinstance(excerpts, dict) or not all(
        isinstance(value, str) and value and value in response for value in excerpts.values()
    ):
        return False
    for field, expected in oracle["exact"].items():
        if observation.get(field) != expected:
            return False
        if not excerpts.get(field):
            return False
    for field, expected in oracle.get("one_of", {}).items():
        if observation.get(field) not in expected or not excerpts.get(field):
            return False
    if not case["facts"].get("review_requested"):
        for field in ("overall_phase", "current_activity", "scope_reconciliation", "next_action"):
            value = observation.get(field)
            if not isinstance(value, str) or not value or not excerpts.get(field):
                return False
        if observation["overall_phase"] == observation["current_activity"]:
            return False
        # Core declaration guard for these eight controlled cases only; it is not NLP
        # or a substitute for independent semantic review. Expand only after review.
        completion = excerpts.get("project_completion", "")
        if observation["project_completion"] == "complete":
            if completion not in {"可以宣布产品完成", "产品已完成", "项目已完成"}:
                return False
            if (
                f"不{completion}" in response
                or f"不能{completion}" in response
                or f"并非{completion}" in response
            ):
                return False
        elif observation["project_completion"] == "incomplete":
            if completion not in {"项目尚未完成", "项目未完成", "产品尚未完成", "产品尚不能交付"}:
                return False
        elif observation["project_completion"] == "unknown":
            if completion not in {
                "项目完成状态无法确认",
                "产品完成状态无法确认",
                "产品整体完成状态无法确认",
            }:
                return False
        else:
            return False
        if not excerpts.get("scope_remaining", "").startswith(("本批", "本轮")):
            return False
        if not excerpts.get("approved_product_remaining", "").startswith(
            ("完整产品", "已批准产品")
        ):
            return False
    for field in (
        "scope_remaining",
        "approved_product_remaining",
        "unknown_unverified_or_not_started",
        "unmapped_requirements",
        "finding_ids",
        "new_findings",
    ):
        value = observation.get(field)
        if field == "approved_product_remaining" and value == "未知":
            continue
        if value is not None and (
            not isinstance(value, list)
            or not all(isinstance(item, str) and item for item in value)
            or len(value) != len(set(value))
        ):
            return False
    for field in oracle.get("nonempty", []):
        value = observation.get(field)
        if (
            not isinstance(value, list if field == "new_findings" else str)
            or not value
            or not excerpts.get(field)
        ):
            return False
    return True


def test_cases_keep_raw_prompts_separate_from_closed_oracles() -> None:
    data = fixture()
    assert len(data["raw_cases"]) >= 8
    assert {case["id"] for case in data["raw_cases"]} == set(data["expected_oracles"])
    for case in data["raw_cases"]:
        assert "expected" not in case and "prompt" in case and "facts" in case


def test_real_independent_observations_match_closed_facts() -> None:
    data = fixture()
    assert OBSERVATIONS.exists(), (
        "RED: await independent raw-response observations; do not invent them"
    )
    observations = json.loads(OBSERVATIONS.read_text(encoding="utf-8"))
    assert isinstance(observations, list)
    assert len(observations) == len(data["expected_oracles"])
    found = observations_by_case(observations, set(data["expected_oracles"]))
    assert found is not None
    for case in data["raw_cases"]:
        assert valid(case, data["expected_oracles"][case["id"]], found[case["id"]])


def test_historical_candidate_manifest_binds_current_evidence() -> None:
    data = fixture()
    manifest = {
        path: digest
        for line in MANIFEST.read_text(encoding="utf-8").splitlines()
        if line
        for digest, path in [line.split("  ", maxsplit=1)]
    }
    review_brief = REVIEW_BRIEF.read_text(encoding="utf-8")
    recorded_manifest = re.search(
        r"candidate_fingerprint：evidence/candidate-sha256\.txt，复审清单 SHA-256 `([0-9a-f]{64})`",
        review_brief,
    )
    assert recorded_manifest
    assert hashlib.sha256(MANIFEST.read_bytes()).hexdigest() == recorded_manifest.group(1)
    paths = (
        ".factory/workitems/FLOW-STATUS-REVIEW-001/evidence/raw-behavior-inputs.json",
        ".factory/workitems/FLOW-STATUS-REVIEW-001/evidence/behavior-observations-v3.json",
    )
    for path in paths:
        assert manifest.get(path) == hashlib.sha256((REPO_ROOT / path).read_bytes()).hexdigest()
    assert json.loads(RAW_INPUTS.read_text(encoding="utf-8")) == data["raw_cases"]


def test_mutations_fail_closed() -> None:
    data = fixture()
    case = data["raw_cases"][5]
    oracle = data["expected_oracles"][case["id"]]
    observation = {
        "case_id": case["id"],
        "candidate_id": "FIXTURE-CANDIDATE-REVIEW-02",
        "original_response": (
            "保留 FIND-7；新增发现：邮箱向非本人暴露。日志补充后确认差异，下一步处理评审发现。"
        ),
        "review_decision": "changes_requested",
        "finding_ids": ["FIND-7"],
        "new_findings": ["邮箱向非本人暴露"],
        "delta_reason": "日志补充后确认差异",
        "excerpts": {
            "review_decision": "新增发现",
            "finding_ids": "保留 FIND-7",
            "new_findings": "邮箱向非本人暴露",
            "delta_reason": "日志补充后确认差异",
        },
    }
    assert valid(case, oracle, observation)
    for field, value in (
        ("candidate_id", "OTHER"),
        ("finding_ids", []),
        ("new_findings", []),
        ("delta_reason", ""),
        ("new_findings", True),
        ("finding_ids", ["FIND-7", "FIND-7"]),
    ):
        mutated = copy.deepcopy(observation)
        mutated[field] = value
        assert not valid(case, oracle, mutated)
    mutated = copy.deepcopy(observation)
    mutated["review_score"] = 100
    assert not valid(case, oracle, mutated)

    status_case = data["raw_cases"][3]
    status_oracle = data["expected_oracles"][status_case["id"]]
    status = {
        "case_id": "SR-04",
        "candidate_id": "CANDIDATE-STATUS-04",
        "original_response": (
                "项目未完成。总体阶段无法确认，当前 bug 修复；"
                "本批剩余真实接口联调、bug 修复；完整产品剩余未知；"
                "范围剩余真实接口联调、bug 修复；下一步完成联调。"
        ),
        "project_completion": "incomplete",
        "overall_phase": "无法确认",
        "current_activity": "bug 修复",
        "scope_remaining": ["真实接口联调", "bug 修复"],
        "approved_product_remaining": "未知",
        "unknown_unverified_or_not_started": ["真实接口联调"],
        "scope_reconciliation": "范围剩余真实接口联调、bug 修复",
        "next_action": "完成联调",
        "finding_ids": [],
        "new_findings": [],
        "excerpts": {
            "project_completion": "项目未完成",
            "overall_phase": "无法确认",
            "current_activity": "bug 修复",
            "scope_remaining": "本批剩余真实接口联调、bug 修复",
            "approved_product_remaining": "完整产品剩余未知",
            "unknown_unverified_or_not_started": "真实接口联调",
            "scope_reconciliation": "范围剩余真实接口联调、bug 修复",
            "next_action": "完成联调",
        },
    }
    assert valid(status_case, status_oracle, status)
    for field, value in (
        ("project_completion", "complete"),
        ("unknown_unverified_or_not_started", []),
        ("scope_remaining", ["真实接口联调"]),
        ("scope_remaining", ["真实接口联调", "bug 修复", "X"]),
        ("overall_phase", "开发"),
        ("overall_phase", "bug 修复"),
        ("scope_remaining", True),
        ("next_action", ""),
    ):
        mutated = copy.deepcopy(status)
        mutated[field] = value
        assert not valid(status_case, status_oracle, mutated)
    mutated = copy.deepcopy(status)
    mutated["excerpts"].pop("next_action")
    assert not valid(status_case, status_oracle, mutated)

    sr01_case = data["raw_cases"][0]
    sr01 = copy.deepcopy(status)
    sr01.update(
        {
            "case_id": "SR-01",
            "candidate_id": "CANDIDATE-STATUS-01",
            "project_completion": "unknown",
            "current_activity": "状态复核",
            "scope_remaining": [],
            "unknown_unverified_or_not_started": ["完整登录流程", "账号管理", "权限"],
            "scope_reconciliation": "基线存在但未提供完整映射核对结果",
            "next_action": "核对完整登录流程、账号管理和权限",
        }
    )
    sr01["original_response"] = (
        "项目完成状态无法确认；总体阶段无法确认，当前状态复核；本批没有剩余；完整产品剩余未知；"
        "完整登录流程、账号管理和权限仍未验证；基线存在但未提供完整映射核对结果；"
        "下一步核对完整登录流程、账号管理和权限。"
    )
    sr01["approved_product_remaining"] = "未知"
    sr01["excerpts"] = {
        "project_completion": "项目完成状态无法确认",
        "overall_phase": "总体阶段无法确认",
        "current_activity": "当前状态复核",
        "scope_remaining": "本批没有剩余",
        "approved_product_remaining": "完整产品剩余未知",
        "unknown_unverified_or_not_started": "完整登录流程、账号管理和权限仍未验证",
        "scope_reconciliation": "基线存在但未提供完整映射核对结果",
        "next_action": "下一步核对完整登录流程、账号管理和权限",
    }
    assert valid(sr01_case, data["expected_oracles"]["SR-01"], sr01)
    mutated = copy.deepcopy(sr01)
    mutated["approved_product_remaining"] = []
    assert not valid(sr01_case, data["expected_oracles"]["SR-01"], mutated)

    sr08_case = data["raw_cases"][7]
    sr08 = copy.deepcopy(sr01)
    sr08.update(
        {
            "case_id": "SR-08",
            "candidate_id": "CANDIDATE-STATUS-06",
            "project_completion": "complete",
            "overall_phase": "交付收口",
            "approved_product_remaining": [],
            "unknown_unverified_or_not_started": [],
        }
    )
    sr08["original_response"] = (
        "可以宣布产品完成；总体阶段交付收口；当前状态复核；本批无剩余；已批准产品无剩余；"
        "无未知项；已核对完整基线；下一步本任务无待办。"
    )
    sr08["scope_reconciliation"] = "已核对完整基线"
    sr08["next_action"] = "本任务无待办"
    sr08["excerpts"] = {
        "project_completion": "可以宣布产品完成",
        "overall_phase": "总体阶段交付收口",
        "current_activity": "当前状态复核",
        "scope_remaining": "本批无剩余",
        "approved_product_remaining": "已批准产品无剩余",
        "unknown_unverified_or_not_started": "无未知项",
        "scope_reconciliation": "已核对完整基线",
        "next_action": "下一步本任务无待办",
    }
    assert valid(sr08_case, data["expected_oracles"]["SR-08"], sr08)
    for phase in ("设计", "开发", "已发布"):
        mutated = copy.deepcopy(sr08)
        mutated["overall_phase"] = phase
        assert not valid(sr08_case, data["expected_oracles"]["SR-08"], mutated)

    mutated = copy.deepcopy(sr01)
    mutated["original_response"] = mutated["original_response"].replace(
        "项目完成状态无法确认；", ""
    )
    mutated["excerpts"]["project_completion"] = "总体阶段无法确认"
    assert not valid(sr01_case, data["expected_oracles"]["SR-01"], mutated)

    mutated = copy.deepcopy(status)
    mutated["original_response"] = mutated["original_response"].replace(
        "项目未完成", "可以宣布产品完成"
    )
    mutated["excerpts"]["project_completion"] = "可以宣布产品完成"
    assert not valid(status_case, status_oracle, mutated)

    mutated = copy.deepcopy(status)
    mutated["excerpts"]["approved_product_remaining"] = "本批剩余真实接口联调、bug 修复"
    assert not valid(status_case, status_oracle, mutated)

    mutated = copy.deepcopy(sr08)
    mutated["original_response"] = mutated["original_response"].replace(
        "可以宣布产品完成", "不可以宣布产品完成"
    )
    assert not valid(sr08_case, data["expected_oracles"]["SR-08"], mutated)


def test_missing_or_duplicate_cases_are_rejected() -> None:
    expected = {"SR-01", "SR-02"}
    complete = [{"case_id": "SR-01"}, {"case_id": "SR-02"}]

    assert observations_by_case(complete, expected) is not None
    assert observations_by_case(complete[:1], expected) is None
    assert observations_by_case([complete[0], complete[0]], expected) is None


def test_v1_missing_v2_fields_is_rejected() -> None:
    assert V1.exists(), "historical v1 observation file must remain available for rejection"
    data = fixture()
    records = json.loads(V1.read_text(encoding="utf-8"))
    found = observations_by_case(records, {case["id"] for case in data["raw_cases"]})
    assert found is not None
    assert not valid(data["raw_cases"][0], data["expected_oracles"]["SR-01"], found["SR-01"])
