"""Cross-document guards for the Skill-first lifecycle baseline."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DESIGN = DOCS / "05-design"
INDEX = DOCS / "document-index.md"
REQUIREMENTS = DOCS / "04-product" / "requirements-matrix.md"
WORKFLOW = DESIGN / "workflow-execution-design.md"
REGISTRY = ROOT / ".factory/project-knowledge/artifact-source-registry.json"
CURRENT_DESIGN = (
    DESIGN / "index.md",
    DESIGN / "solution-overview.md",
    DESIGN / "technical-selection.md",
    DESIGN / "module-domain-design.md",
    DESIGN / "data-design.md",
    DESIGN / "api-design.md",
    DESIGN / "frontend-design.md",
    DESIGN / "ux-ui-design.md",
    DESIGN / "memory-design.md",
    DESIGN / "interface-matrix.md",
    WORKFLOW,
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def markdown_table(document: str, heading: str) -> list[list[str]]:
    section = document.split(heading, 1)[1].split("\n## ", 1)[0]
    return [
        [cell.strip() for cell in line.strip("|").split("|")]
        for line in section.splitlines()
        if line.startswith("|") and not set(line.replace("|", "").strip()) <= {"-", ":"}
    ]


def assert_lifecycle_matrix(rows: list[list[str]]) -> None:
    assert rows[0] == [
        "阶段",
        "触发",
        "权威输入",
        "准入",
        "活动",
        "输出",
        "保存位置",
        "owner / 模型",
        "验证",
        "退出 Gate",
        "回流",
    ]
    stages = {row[0]: row for row in rows[1:]}
    required_stages = {
        "分类与恢复",
        "发现与 Spike",
        "需求",
        "设计",
        "计划与任务",
        "实现",
        "Bug 根因",
        "测试与定向回归",
        "批次 Review",
        "最终候选验证",
        "本地提交与远端交付",
        "发布与运维",
    }
    assert required_stages <= stages.keys()
    assert all(len(row) == 11 and all(cell for cell in row) for row in rows[1:])
    required_semantics = {
        "发现与 Spike": ("不把原型当交付", "原型不得越级发布"),
        "计划与任务": ("不得跳过 WorkItem 身份、TDD 和定向验证",),
        "实现": ("TDD",),
        "Bug 根因": ("根因", "禁止猜测式补丁"),
        "批次 Review": ("独立只读 Review",),
        "最终候选验证": ("新鲜完整候选测试", "不得用旧输出宣称通过"),
        "本地提交与远端交付": ("按授权远端交接", "无授权停止"),
        "发布与运维": ("人工授权", "回滚"),
    }
    for stage, terms in required_semantics.items():
        row = " ".join(stages[stage])
        assert all(term in row for term in terms), (stage, terms)
    forbidden_semantics = {
        "发现与 Spike": (
            "原型可作为交付",
            "原型可以作为交付",
            "原型可越级发布",
            "原型可以越级发布",
        ),
        "计划与任务": (
            "可跳过 WorkItem 身份",
            "可以跳过 WorkItem 身份",
            "可跳过 TDD",
            "可以跳过 TDD",
            "可跳过定向验证",
            "可以跳过定向验证",
        ),
        "Bug 根因": ("允许猜测式补丁",),
        "批次 Review": ("作者自批",),
        "最终候选验证": ("可用旧输出替代", "可以用旧输出替代", "可以用旧输出"),
        "本地提交与远端交付": ("无授权仍可", "无授权提交", "无授权远端"),
        "发布与运维": ("无需人工授权", "不需要人工授权", "无人工授权可发布"),
    }
    for stage, terms in forbidden_semantics.items():
        row = " ".join(stages[stage])
        assert not any(term in row for term in terms), (stage, terms)


def test_formal_baseline_versions_match_document_control() -> None:
    rows = re.findall(
        (
            r"^\| `(?P<path>docs/[^`]+)` \| .*? \| `formal_baseline` \| .*? "
            r"\| `(?P<version>v[^`]+)` \|$"
        ),
        read(INDEX),
        re.MULTILINE,
    )
    mismatches = []
    for relative_path, indexed_version in rows:
        controlled_version = re.search(
            r"\| (?:正式版本|当前正式版本) \| `?(?P<version>v\d+\.\d+\.\d+)",
            read(ROOT / relative_path),
        )
        actual = controlled_version.group("version") if controlled_version else "missing"
        if actual != indexed_version:
            mismatches.append(f"{relative_path}: index={indexed_version}, control={actual}")
    assert rows, "document index must register formal_baseline documents"
    assert not mismatches, "formal_baseline version drift: " + "; ".join(mismatches)


def test_skill_first_design_has_no_current_python_platform_paths() -> None:
    legacy_paths = (
        "src/access",
        "src/application",
        "src/domain",
        "src/runtime",
        "src/settings",
    )
    findings = [
        f"{path.relative_to(ROOT)}: {legacy_path}"
        for path in CURRENT_DESIGN
        for legacy_path in legacy_paths
        if legacy_path in read(path)
    ]
    assert not findings, "legacy Python platform remains in current design: " + "; ".join(findings)


def test_retired_api_and_design_attachments_are_not_active() -> None:
    retired_paths = (
        "contracts/openapi/openapi.yaml",
        "contracts/schemas/openapi-shanforge-rules.schema.json",
        "contracts/schemas/design-artifact-manifest.schema.json",
        "design/ux-ui/design-manifest.yaml",
        "design/ux-ui/*.penpot",
        "design/ux-ui/tokens.json",
        "design/ux-ui/exports/",
    )
    findings = [
        f"{path.relative_to(ROOT)}: {retired_path}"
        for path in (INDEX, *CURRENT_DESIGN)
        for retired_path in retired_paths
        if retired_path in read(path)
    ]
    existing = [
        str(path.relative_to(ROOT))
        for retired_path in retired_paths
        for path in ROOT.glob(retired_path)
    ]
    registry = json.loads(read(REGISTRY))
    active_roots = [
        root
        for source in registry["sources"]
        for root in source["roots"]
        if root in {"contracts/openapi", "design/ux-ui"}
    ]
    assert not findings and not existing and not active_roots, (
        "retired OpenAPI/design attachment remains active: "
        + "; ".join([*findings, *existing, *active_roots])
    )


def test_req_sf_008_is_current_and_not_deferred_to_t02() -> None:
    row = next(
        (line for line in read(REQUIREMENTS).splitlines() if "`REQ-SF-008`" in line), ""
    )
    assert row, "REQ-SF-008 must remain registered"
    assert "当前有效" in row and "待 T02 实现" not in row, (
        "REQ-SF-008 must be current, not deferred: " + row
    )


def test_lifecycle_matrix_declares_required_controls_and_distinctions() -> None:
    assert_lifecycle_matrix(markdown_table(read(WORKFLOW), "## 统一生命周期矩阵"))


def test_lifecycle_matrix_rejects_keyword_complete_semantic_inversion() -> None:
    rows = markdown_table(read(WORKFLOW), "## 统一生命周期矩阵")
    inverted = [row.copy() for row in rows]
    spike_row = next(row for row in inverted if row[0] == "发现与 Spike")
    spike_row[-1] += "；原型可以作为交付并可越级发布"
    plan_row = next(row for row in inverted if row[0] == "计划与任务")
    plan_row[-1] += "；简单任务可跳过 WorkItem 身份、TDD 和定向验证"
    candidate_row = next(row for row in inverted if row[0] == "最终候选验证")
    candidate_row[-1] += "；可用旧输出替代"
    release_row = next(row for row in inverted if row[0] == "发布与运维")
    release_row[-1] += "；发布无需人工授权"
    try:
        assert_lifecycle_matrix(inverted)
    except AssertionError:
        return
    raise AssertionError("semantic inversion must be rejected")


def test_tasks_summary_has_no_undated_legacy_current_block() -> None:
    summary = read(ROOT / ".factory/memory/tasks.summary.md")
    assert not re.search(r"^## (进行中|下一顺位)$", summary, re.MULTILINE)
    assert "src/domain" not in summary and "src/settings" not in summary


def test_design_index_lists_current_skill_first_designs() -> None:
    source = read(DESIGN / "index.md")
    current_documents = (
        "solution-overview.md",
        "api-design.md",
        "frontend-design.md",
        "ux-ui-design.md",
        "memory-design.md",
        "interface-matrix.md",
    )
    historical_rows = [
        line
        for line in source.splitlines()
        if any(document in line for document in current_documents)
        and ("历史" in line or "旧平台" in line)
    ]
    missing = [document for document in current_documents if document not in source]
    assert "当前 Skill-first 设计文档" in source and not missing and not historical_rows, (
        "design index must list current Skill-first designs, not historical platform rows: "
        + "; ".join([*missing, *historical_rows])
    )


def test_changed_governance_documents_name_this_work_item_as_source() -> None:
    expected_sources = {
        REQUIREMENTS: "SOFTWARE-LIFECYCLE-GOVERNANCE-001",
        DESIGN / "index.md": "SOFTWARE-LIFECYCLE-GOVERNANCE-001",
    }
    mismatches = [
        str(path.relative_to(ROOT)) for path, source_id in expected_sources.items()
        if f"| 来源候选 | `{source_id}` |" not in read(path)
    ]
    assert not mismatches, (
        "current governance documents do not declare their current source: " + ", ".join(mismatches)
    )
    index = read(INDEX)
    source = re.search(r"^\| 来源候选 \| `(?P<source>[^`]+)` \|$", index, re.MULTILINE)
    version = re.search(r"^\| 正式版本 \| `(?P<version>v\d+\.\d+\.\d+)` \|$", index, re.MULTILINE)
    assert source and source.group("source")
    assert version
    history_versions = re.findall(r"^\| `(v\d+\.\d+\.\d+)` \|", index, re.MULTILINE)
    assert tuple(map(int, version.group("version")[1:].split("."))) == max(
        tuple(map(int, value[1:].split("."))) for value in history_versions
    )
    index_row = next(line for line in index.splitlines() if "`docs/document-index.md`" in line)
    assert f"| `{version.group('version')}` |" in index_row


def test_lifecycle_governance_test_documents_have_current_controls() -> None:
    expected_controls = {
        DOCS / "06-delivery" / "test-plan.md": "v3.3.0",
        DOCS / "06-delivery" / "test-cases.md": "v1.1.0",
    }
    for path, version in expected_controls.items():
        source = read(path)
        assert f"| 正式版本 | `{version}` |" in source
        assert "| 来源候选 | `SOFTWARE-LIFECYCLE-GOVERNANCE-001` |" in source
    assert "| 最后更新 | 2026-09-01 |" in read(
        DOCS / "06-delivery" / "test-cases.md"
    )


def test_lifecycle_governance_case_is_registered() -> None:
    plan = read(DOCS / "06-delivery" / "test-plan.md")
    cases = read(DOCS / "06-delivery" / "test-cases.md")
    node = "tests/test_lifecycle_governance.py"
    assert "`TEST-BB-002`" in plan and node in plan
    assert "`TEST-BB-002`" in cases and node in cases
