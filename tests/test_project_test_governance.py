from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = (
    REPO_ROOT
    / "skills"
    / "document-templates"
    / "scripts"
    / "validate_test_documents.py"
)


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def section(content: str, heading: str) -> str:
    start = content.index(heading)
    level = len(heading) - len(heading.lstrip("#"))
    match = re.search(
        rf"\n#{{1,{level}}}\s",
        content[start + len(heading) :],
    )
    if match is None:
        return content[start:]
    return content[start : start + len(heading) + match.start()]


def table_rows(content: str, heading: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section(content, heading).splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip("|").split("|")]
        if cells and set("".join(cells)) <= {"-", ":"}:
            continue
        rows.append(cells)
    return rows


def test_verification_skill_defines_project_level_test_governance() -> None:
    skill = read("skills/verification-before-completion/SKILL.md")

    for phrase in (
        "项目级测试治理",
        "整体黑盒",
        "UI",
        "API",
        "发布回归",
        "TEST-BB-*",
        "TEST-REL-*",
        "需求 -> 任务 -> 测试 -> 证据",
        "启动命令",
        "端口",
        "健康检查",
        "关闭方式",
        "N/A",
    ):
        assert phrase in skill


def test_webapp_testing_requires_a_reproducible_environment_contract() -> None:
    skill = read("skills/webapp-testing/SKILL.md")

    for phrase in (
        "TEST-UI-*",
        "启动命令",
        "端口",
        "健康检查",
        "关闭方式",
        "静态 HTML",
        "N/A",
        "不得写“待补充”",
    ):
        assert phrase in skill


def test_api_design_requires_contract_test_traceability() -> None:
    skill = read("skills/api-design/SKILL.md")

    for phrase in (
        "TEST-API-*",
        "需求 -> 任务 -> 测试 -> 证据",
        "schema/contract test",
        "进程内",
        "N/A",
        "不得写“待补充”",
    ):
        assert phrase in skill


def test_reusable_test_environment_template_has_no_ambiguous_placeholders() -> None:
    skill = read("skills/document-templates/SKILL.md")
    template = read("skills/document-templates/references/test-environment-template.md")

    assert "references/test-environment-template.md" in skill
    for phrase in (
        "适用性",
        "启动命令",
        "端口",
        "健康检查",
        "关闭方式",
        "测试数据与隔离",
        "TEST-*",
        "需求 ID",
        "任务 ID",
        "证据",
        "N/A",
    ):
        assert phrase in template
    assert "待补充" not in template


def run_validator(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), *arguments],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_test_governance_revision_is_formally_published() -> None:
    plan = read("docs/06-delivery/test-plan.md")
    controls = {
        row[0]: row[1] for row in table_rows(plan, "## 文档控制") if len(row) == 2
    }

    assert controls["正式版本"] == "v3.2.0"
    assert controls["当前修订"] == "无"
    assert controls["审核 / 批准"] == "独立 Reviewer / uroborus"
    assert controls["状态"] == "已批准并生效"
    published_history = section(plan, "## 正式版本历史（仅已发布）")
    assert "v3.2.0" in published_history


def test_test_registry_has_executable_traceability() -> None:
    plan = read("docs/06-delivery/test-plan.md")
    rows = table_rows(plan, "### 4.1 测试登记")
    assert rows[0] == [
        "测试 ID",
        "人类可读名称",
        "需求 ID",
        "任务 ID",
        "可执行入口",
        "Evidence",
        "结果",
        "环境 ID",
    ]
    records = rows[1:]
    assert {record[0] for record in records} == {
        "TEST-BB-001",
        "TEST-UI-001",
        "TEST-API-001",
        "TEST-REL-001",
    }

    prd = read("docs/04-product/prd.md")
    ledgers = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (REPO_ROOT / ".factory" / "workitems").glob("*/ledger.jsonl")
    )
    environments = {
        row[0] for row in table_rows(plan, "### 4.2 当前测试环境基线")[1:]
    }
    for record in records:
        test_id, _, requirement_id, task_id, command, evidence, result, env_id = (
            record
        )
        assert re.fullmatch(r"TEST-(?:BB|UI|API|REL)-\d{3}", test_id)
        assert re.fullmatch(r"(?:REQ|NFR)-[A-Z0-9-]+", requirement_id)
        assert requirement_id in prd
        assert task_id in ledgers
        assert command.startswith((".venv/bin/", "uv "))
        assert " 加" not in command
        assert evidence.startswith(".factory/workitems/")
        assert (REPO_ROOT / evidence).is_file()
        assert result.startswith("passed")
        assert env_id in environments


def test_current_environment_rows_are_exact_or_reasoned_na() -> None:
    plan = read("docs/06-delivery/test-plan.md")
    rows = table_rows(plan, "### 4.2 当前测试环境基线")
    assert rows[0] == [
        "环境 ID",
        "场景",
        "启动命令",
        "端口",
        "健康检查",
        "关闭方式",
    ]
    records = rows[1:]
    assert {record[0] for record in records} == {
        "TEST-ENV-PYTEST",
        "TEST-ENV-STATIC",
    }
    forbidden_placeholders = (
        "记录运行时",
        "使用项目声明",
        "对健康",
        "实际监听",
        "<",
    )
    for record in records:
        assert len(record) == 6
        assert not any(
            placeholder in cell
            for placeholder in forbidden_placeholders
            for cell in record
        )
        for cell in record[2:]:
            if "N/A" in cell:
                assert "：" in cell
                assert len(cell.split("：", 1)[1].strip()) >= 4


def test_task_inputs_and_scope_resolve_to_current_paths() -> None:
    brief = read(
        ".factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-013.md"
    )
    assert "docs/04-product/prd.md" in brief
    assert "docs/03-requirements/prd.md" not in brief
    assert "skills/document-templates/SKILL.md" in brief
    assert "docs/04-project-development" not in brief
    for path in (
        "docs/04-product/prd.md",
        "docs/05-design/workflow-execution-design.md",
        "docs/06-delivery/test-plan.md",
        "skills/document-templates/SKILL.md",
    ):
        assert (REPO_ROOT / path).exists()


def test_formal_test_plan_has_no_ambiguous_placeholder() -> None:
    plan = read("docs/06-delivery/test-plan.md")
    assert "待补充" not in plan


def test_formal_test_references_resolve_to_current_test_files() -> None:
    sources = [
        REPO_ROOT / "docs/06-delivery/test-plan.md",
        REPO_ROOT / "docs/06-delivery/test-cases.md",
    ]
    sources.extend(
        sorted((REPO_ROOT / "tests/specifications").glob("*.testcases.yaml"))
    )
    referenced = {
        match
        for source in sources
        for match in re.findall(
            r"tests/test_[a-z0-9_]+\.py", source.read_text(encoding="utf-8")
        )
    }
    missing = sorted(path for path in referenced if not (REPO_ROOT / path).is_file())

    assert missing == []


def test_formal_case_catalog_passes_automated_validity_check() -> None:
    catalog = REPO_ROOT / "docs/06-delivery/test-cases.md"

    assert VALIDATOR.is_file()
    assert catalog.is_file()
    result = run_validator(
        "--repo-root",
        str(REPO_ROOT),
        "--catalog",
        str(catalog),
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "catalog: valid" in result.stdout


def test_catalog_validator_rejects_a_missing_automation_node(tmp_path: Path) -> None:
    catalog = read("docs/06-delivery/test-cases.md")
    invalid_catalog = tmp_path / "test-cases.md"
    invalid_variants = (
        (
            catalog.replace("完整会话路由合同", "索引名称漂移", 1),
            "index/detail name mismatch",
        ),
        (
            catalog.replace(
                "test_candidate_behavior_map_is_complete_and_each_mapping_is_unique",
                "test_missing_automation_node",
            ),
            "automation target does not exist",
        ),
        (
            catalog.replace("### 后置条件与清理", "### 缺少后置条件", 1),
            "missing section: ### 后置条件与清理",
        ),
        (
            catalog.replace("### 标签", "### 缺少标签", 1),
            "missing section: ### 标签",
        ),
    )
    for invalid_document, expected_error in invalid_variants:
        invalid_catalog.write_text(invalid_document, encoding="utf-8")
        result = run_validator(
            "--repo-root",
            str(REPO_ROOT),
            "--catalog",
            str(invalid_catalog),
        )
        assert result.returncode == 1
        assert expected_error in result.stderr


def test_report_validator_checks_counts_verdict_and_release_advice(
    tmp_path: Path,
) -> None:
    valid_report = """# 测试报告

## 1. 报告控制

| 字段 | 内容 |
|---|---|
| 精确候选 | abcdef1 |
| 批次验证结论 | passed |

## 5. 结果汇总

| 总数 | 通过 | 失败 | 错误 | 阻塞 | 跳过 | 未运行 | 取消 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |

## 9. 发布建议

- 建议：GO
"""
    report = tmp_path / "test-report.md"
    report.write_text(valid_report, encoding="utf-8")
    valid = run_validator("--report", str(report))
    assert valid.returncode == 0, valid.stdout + valid.stderr
    assert "report: valid" in valid.stdout

    invalid_variants = (
        (
            valid_report.replace("| 4 | 4 | 0 |", "| 4 | 5 | -1 |"),
            "result summary counts cannot be negative",
        ),
        (
            valid_report.replace("| 4 | 4 |", "| 5 | 4 |"),
            "result total does not equal seven-state counts",
        ),
        (
            valid_report.replace(
                "| 批次验证结论 | passed |",
                "| 批次验证结论 | failed |",
            ),
            "batch verdict does not match result counts",
        ),
        (
            valid_report.replace("- 建议：GO", "- 建议：NO-GO"),
            "release advice does not match batch verdict",
        ),
    )
    for invalid_report, expected_error in invalid_variants:
        report.write_text(invalid_report, encoding="utf-8")
        invalid = run_validator("--report", str(report))
        assert invalid.returncode == 1
        assert expected_error in invalid.stderr


def test_documented_validator_commands_use_the_project_python_runtime() -> None:
    paths = (
        "docs/06-delivery/test-plan.md",
        "docs/06-delivery/test-cases.md",
        "skills/document-templates/assets/templates/05-quality/test-plan.md",
        "skills/document-templates/assets/templates/05-quality/test-cases.md",
        "skills/document-templates/assets/templates/05-quality/test-report.md",
    )
    for path in paths:
        document = read(path)
        validator_command = (
            "uv run python "
            "skills/document-templates/scripts/validate_test_documents.py"
        )
        assert validator_command in document
        assert not re.search(
            r"(?<!uv run )python skills/document-templates/scripts/validate_test_documents.py",
            document,
        )


def test_reusable_case_and_report_templates_define_complete_human_outputs() -> None:
    skill = read("skills/document-templates/SKILL.md")
    cases_path = (
        REPO_ROOT
        / "skills/document-templates/assets/templates/05-quality/test-cases.md"
    )
    assert cases_path.is_file()
    cases = cases_path.read_text(encoding="utf-8")
    report = read("skills/document-templates/assets/templates/05-quality/test-report.md")

    assert "assets/templates/05-quality/test-cases.md" in skill
    for phrase in (
        "案例 ID",
        "需求 / 验收标准",
        "风险等级",
        "前置条件",
        "测试数据 / fixture",
        "操作步骤",
        "预期结果",
        "自动化入口",
        "证据要求",
        "validate_test_documents.py",
    ):
        assert phrase in cases
    for phrase in (
        "报告 ID",
        "上游测试计划",
        "准入条件",
        "准出条件",
        "错误",
        "取消",
        "未运行 / 跳过原因",
        "环境健康与清理",
        "需求覆盖",
        "GO | NO-GO",
        "评审与批准",
        "版本历史",
        "validate_test_documents.py",
    ):
        assert phrase in report


def test_case_results_and_batch_verdicts_have_distinct_status_contracts() -> None:
    verification = read("skills/verification-before-completion/SKILL.md")
    environment = read(
        "skills/document-templates/references/test-environment-template.md"
    )

    assert (
        "案例运行结果：`passed | failed | error | blocked | skipped | not_run | "
        "cancelled`" in verification
    )
    assert "批次验证结论：`passed | partial | failed | blocked`" in verification
    assert (
        "passed / failed / error / blocked / skipped / not_run / cancelled"
        in environment
    )
