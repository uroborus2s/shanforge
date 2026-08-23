#!/usr/bin/env python3
"""Validate human-readable test case catalogs and aggregate test reports."""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

CASE_ID = re.compile(r"TEST-[A-Z0-9-]+")
DETAIL_HEADING = re.compile(r"^## 案例：`(?P<case_id>TEST-[A-Z0-9-]+)`$", re.MULTILINE)
ALLOWED_DEFINITION_STATES = {"draft", "active", "deprecated", "retired"}
ALLOWED_PRIORITIES = {"P0", "P1", "P2"}
ALLOWED_RISKS = {"high", "medium", "low"}
ALLOWED_AUTOMATION = {"automated", "manual", "planned"}
ALLOWED_VERDICTS = {"passed", "partial", "failed", "blocked"}
SUMMARY_HEADERS = ["总数", "通过", "失败", "错误", "阻塞", "跳过", "未运行", "取消"]


class ValidationError(ValueError):
    """Raised when a test document violates its public contract."""


def section(document: str, heading: str) -> str:
    marker = f"{heading}\n"
    if marker not in document:
        raise ValidationError(f"missing section: {heading}")
    body = document.split(marker, 1)[1]
    level = len(heading) - len(heading.lstrip("#"))
    next_heading = re.search(rf"\n#{{1,{level}}}\s", body)
    return body if next_heading is None else body[: next_heading.start()]


def table(document: str, heading: str) -> list[dict[str, str]]:
    lines = [line for line in section(document, heading).splitlines() if line.startswith("|")]
    if len(lines) < 3:
        raise ValidationError(f"missing table rows: {heading}")
    headers = [cell.strip() for cell in lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in lines[2:]:
        values = [cell.strip().strip("`") for cell in line.strip("|").split("|")]
        if len(values) != len(headers):
            raise ValidationError(f"invalid table row in {heading}: {line}")
        rows.append(dict(zip(headers, values, strict=True)))
    return rows


def control_values(document: str, heading: str) -> dict[str, str]:
    rows = table(document, heading)
    try:
        return {row["字段"]: row["内容"] for row in rows}
    except KeyError as error:
        raise ValidationError(f"{heading} must use 字段/内容 columns") from error


def field(block: str, label: str) -> str:
    match = re.search(rf"^- {re.escape(label)}：(.+)$", block, re.MULTILINE)
    if match is None:
        raise ValidationError(f"missing case field: {label}")
    value = match.group(1).strip().strip("`")
    if not value or "<" in value or ">" in value:
        raise ValidationError(f"empty or placeholder case field: {label}")
    return value


def case_blocks(document: str) -> dict[str, str]:
    matches = list(DETAIL_HEADING.finditer(document))
    blocks: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(document)
        case_id = match.group("case_id")
        if case_id in blocks:
            raise ValidationError(f"duplicate case detail: {case_id}")
        blocks[case_id] = document[match.start() : end]
    if not blocks:
        raise ValidationError("catalog has no case details")
    return blocks


def validate_node(repo_root: Path, node_id: str) -> None:
    parts = node_id.strip("`").split("::")
    source = repo_root / parts[0]
    if not source.is_file():
        raise ValidationError(f"automation target does not exist: {node_id}")
    if len(parts) == 1:
        return
    nodes: list[ast.AST] = list(ast.parse(source.read_text(encoding="utf-8")).body)
    for raw_name in parts[1:]:
        name = raw_name.split("[", 1)[0]
        match = next(
            (
                node
                for node in nodes
                if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
                and node.name == name
            ),
            None,
        )
        if match is None:
            raise ValidationError(f"automation target does not exist: {node_id}")
        nodes = list(getattr(match, "body", []))


def validate_catalog(path: Path, repo_root: Path) -> int:
    document = path.read_text(encoding="utf-8")
    index_rows = table(document, "## 案例索引")
    if "案例 ID" not in index_rows[0]:
        raise ValidationError("案例索引 must include 案例 ID")
    index_ids = [row["案例 ID"] for row in index_rows]
    if len(index_ids) != len(set(index_ids)):
        raise ValidationError("duplicate case ID in index")
    if not all(CASE_ID.fullmatch(case_id) for case_id in index_ids):
        raise ValidationError("invalid case ID in index")

    blocks = case_blocks(document)
    if set(index_ids) != set(blocks):
        raise ValidationError("case index and detail IDs do not match")

    required_fields = (
        "名称",
        "版本",
        "定义状态",
        "测试目标",
        "需求 / 验收标准",
        "关联设计 / API / UI / 任务",
        "测试类型与层级",
        "优先级",
        "风险等级",
        "Owner",
        "环境别名",
        "自动化状态",
        "自动化入口",
    )
    index_by_id = {row["案例 ID"]: row for row in index_rows}
    for case_id, block in blocks.items():
        values = {label: field(block, label) for label in required_fields}
        index_row = index_by_id[case_id]
        if index_row.get("名称") != values["名称"]:
            raise ValidationError(f"index/detail name mismatch: {case_id}")
        for label in ("优先级", "风险等级", "自动化入口"):
            if index_row.get(label) != values[label]:
                raise ValidationError(f"index/detail {label} mismatch: {case_id}")
        if index_row.get("需求 / 验收标准", "") not in values["需求 / 验收标准"]:
            raise ValidationError(f"index/detail requirement mismatch: {case_id}")
        if index_row.get("层级", "") not in values["测试类型与层级"]:
            raise ValidationError(f"index/detail level mismatch: {case_id}")
        if values["定义状态"] not in ALLOWED_DEFINITION_STATES:
            raise ValidationError(f"invalid definition state: {case_id}")
        if values["优先级"] not in ALLOWED_PRIORITIES:
            raise ValidationError(f"invalid priority: {case_id}")
        if values["风险等级"] not in ALLOWED_RISKS:
            raise ValidationError(f"invalid risk: {case_id}")
        if values["自动化状态"] not in ALLOWED_AUTOMATION:
            raise ValidationError(f"invalid automation state: {case_id}")
        if values["自动化状态"] == "automated":
            validate_node(repo_root, values["自动化入口"])
        elif not values["自动化入口"].startswith("N/A："):
            raise ValidationError(f"manual/planned automation needs reasoned N/A: {case_id}")
        preconditions = section(block, "### 前置条件")
        if not re.search(r"^\d+\.\s+\S", preconditions, re.MULTILINE):
            raise ValidationError(f"case needs a concrete precondition: {case_id}")
        fixtures = table(block, "### 测试数据 / fixture")
        fixture_fields = {"数据 / fixture", "用途", "敏感", "准备 / 复位方式"}
        if not fixture_fields.issubset(fixtures[0]):
            raise ValidationError(f"invalid fixture table: {case_id}")
        if any(
            not value or "<" in value or ">" in value
            for fixture in fixtures
            for value in fixture.values()
        ):
            raise ValidationError(f"empty or placeholder fixture: {case_id}")
        steps = table(block, "### 步骤与判定")
        for step in steps:
            for label in ("操作步骤", "预期结果", "证据要求"):
                value = step.get(label, "")
                if not value or "<" in value or ">" in value:
                    raise ValidationError(f"invalid {label}: {case_id}")
        for heading in ("### 后置条件与清理", "### 标签"):
            content = section(block, heading)
            if not re.search(r"^-\s+\S", content, re.MULTILINE):
                raise ValidationError(f"empty section: {heading} ({case_id})")
    return len(blocks)


def expected_verdict(counts: dict[str, int]) -> str:
    if counts["失败"] or counts["错误"]:
        return "failed"
    if counts["阻塞"] and counts["通过"] == 0:
        return "blocked"
    if any(counts[label] for label in ("阻塞", "跳过", "未运行", "取消")):
        return "partial"
    return "passed"


def validate_report(path: Path) -> None:
    document = path.read_text(encoding="utf-8")
    controls = control_values(document, "## 1. 报告控制")
    candidate = controls.get("精确候选", "").strip("`")
    verdict = controls.get("批次验证结论", "").strip("`")
    if not re.fullmatch(r"[0-9a-f]{7,64}", candidate):
        raise ValidationError("report needs an immutable candidate")
    if verdict not in ALLOWED_VERDICTS:
        raise ValidationError("invalid batch verdict")

    rows = table(document, "## 5. 结果汇总")
    if list(rows[0]) != SUMMARY_HEADERS:
        raise ValidationError("result summary headers do not match the seven-state contract")
    if len(rows) != 1:
        raise ValidationError("result summary must contain exactly one aggregate row")
    try:
        counts = {label: int(rows[0][label]) for label in SUMMARY_HEADERS}
    except ValueError as error:
        raise ValidationError("result summary counts must be integers") from error
    if any(value < 0 for value in counts.values()):
        raise ValidationError("result summary counts cannot be negative")
    if counts["总数"] != sum(counts[label] for label in SUMMARY_HEADERS[1:]):
        raise ValidationError("result total does not equal seven-state counts")
    if verdict != expected_verdict(counts):
        raise ValidationError("batch verdict does not match result counts")

    advice_match = re.search(r"^- 建议：`?(GO|NO-GO)`?$", document, re.MULTILINE)
    if advice_match is None:
        raise ValidationError("report needs a concrete GO or NO-GO recommendation")
    expected_advice = "GO" if verdict == "passed" else "NO-GO"
    if advice_match.group(1) != expected_advice:
        raise ValidationError("release advice does not match batch verdict")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--catalog", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if args.catalog is None and args.report is None:
        parser.error("at least one of --catalog or --report is required")

    try:
        if args.catalog is not None:
            count = validate_catalog(args.catalog, args.repo_root.resolve())
            print(f"catalog: valid ({count} cases)")
        if args.report is not None:
            validate_report(args.report)
            print("report: valid")
    except (OSError, ValidationError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
