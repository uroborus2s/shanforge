from __future__ import annotations

import re
from pathlib import Path

from test_remaining_skill_project_status_contract import (
    PROJECT_CONTRACT_LINK,
    STATUS_FACTS,
    WORK_SKILLS,
    read_skill,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
SHARED_CONTRACT = (
    REPO_ROOT / "skills" / "using-shanforge" / "references" / "work-skill-return-contract.md"
)

def test_work_skills_keep_professional_content_before_the_shared_contract() -> None:
    separator = f"\n{PROJECT_CONTRACT_LINK}"
    for name in sorted(WORK_SKILLS):
        skill = read_skill(name)
        assert skill.count(separator) <= 1, name
        professional_prefix = skill.split(separator, maxsplit=1)[0]
        frontmatter = professional_prefix.split("---", 2)[1]
        headings = re.findall(r"^## .+", professional_prefix, re.MULTILINE)
        list_items = re.findall(r"^(?:- |\d+\. )", professional_prefix, re.MULTILINE)

        assert f"name: {name}" in frontmatter, name
        assert "description:" in frontmatter, name
        assert len(headings) >= 3, name
        assert len(list_items) >= 5, name
        assert skill.count(PROJECT_CONTRACT_LINK) == 1, name

    modified_skill_anchors = {
        "art-asset-pipeline": ("## 工作流程", "manifest.json"),
        "brainstorming": ("## 默认流程", "Brief 模板"),
        "document-templates": ("## 默认工作流", "## 新项目回退布局"),
        "requirements-engineering": ("## Shanforge 默认流程", "analysis_mode"),
    }
    for name, anchors in modified_skill_anchors.items():
        skill = read_skill(name)
        assert all(anchor in skill for anchor in anchors), name


def test_shared_contract_separates_local_results_from_project_envelope() -> None:
    contract = SHARED_CONTRACT.read_text(encoding="utf-8")

    assert "task_id/task_type 表示正式任务身份" in contract
    assert "skill 表示执行者身份" in contract
    assert "不得统一或改写工作 Skill 的既有专业输出" in contract
    assert "工作 Skill 本职结果包" in contract
    assert "项目状态信封" in contract
    assert "direct_answer" in contract
    assert "lightweight_analysis" in contract
    for fact in STATUS_FACTS:
        assert contract.count(fact) == 1


def test_work_skill_return_contract_exposes_consumable_facts_without_owning_progress() -> None:
    contract = SHARED_CONTRACT.read_text(encoding="utf-8")

    for field in (
        "human_summary",
        "progress_delta",
        "verification_summary",
        "defect_summary",
    ):
        assert f"- {field}:" in contract

    for phrase in (
        "按适用性提供",
        "不得推断 WBS 分母、产品功能完成度或项目完成层级",
        "项目完成层级仍由 `using-shanforge`",
    ):
        assert phrase in contract


def test_test_work_returns_structured_verification_facts() -> None:
    contract = SHARED_CONTRACT.read_text(encoding="utf-8")
    verification = contract.split("## 测试类 verification_summary", maxsplit=1)[1].split(
        "\n## ", maxsplit=1
    )[0]

    for row in (
        "- total: <number>",
        "- passed: <number>",
        "- failed: <number>",
        "- error: <number>",
        "- blocked: <number>",
        "- skipped: <number>",
        "- not_run: <number>",
        "- cancelled: <number>",
        "- covered_scope: <本轮覆盖范围>",
        "- uncovered_scope: <未覆盖范围>",
        "- failed_or_error_cases: <TEST-ID、关联功能、现象、归因；无则 none>",
    ):
        assert row in verification

    assert "非测试工作可以使用通用 verification_summary" in contract


def test_using_shanforge_is_the_project_envelope_owner() -> None:
    controller = read_skill("using-shanforge")
    section = controller.split("## 工作 skill 状态回写协议", maxsplit=1)[1]
    section = section.split("\n## ", maxsplit=1)[0]
    work_result = section.split("项目状态信封：", maxsplit=1)[0]
    project_envelope = section.split("项目状态信封：", maxsplit=1)[1]

    assert "references/work-skill-return-contract.md" in section
    assert "工作 Skill 本职结果包：" in work_result
    for field in ("project_position", "completion_level", "stop_reason", "scope_remaining"):
        assert field not in work_result
        assert field in project_envelope
    assert "next_required_action" in project_envelope


def test_local_status_and_needs_are_forwarded_without_normalization() -> None:
    controller = read_skill("using-shanforge")
    contract = SHARED_CONTRACT.read_text(encoding="utf-8")
    formal_design = (REPO_ROOT / "docs" / "05-design" / "workflow-execution-design.md").read_text(
        encoding="utf-8"
    )
    formal_package = formal_design.split("## 统一任务包", maxsplit=1)[1]
    formal_package = formal_package.split("\n## 六类任务", maxsplit=1)[0]

    for owner_contract in (controller, contract, formal_package):
        assert "status: <该 Skill 的既有本地状态>" in owner_contract
        assert "needs: <该 Skill 的既有本地 needs>" in owner_contract

    representative_local_contracts = {
        "api-design": (
            "status: passed | partial | failed | blocked",
            "none | product_decision | compatibility_review | tests | human_confirmation",
        ),
        "systematic-debugging": (
            "status: root_cause_found | blocked | needs_user_input",
            "human_confirmation | more_information | more_diagnostics | architecture_decision",
        ),
        "writing-plans": (
            "status: plan_ready | ready_for_review | not_applicable | blocked | needs_user_input",
            "plan_review | human_confirmation | none",
        ),
    }
    for name, local_fields in representative_local_contracts.items():
        skill = read_skill(name)
        for local_field in local_fields:
            assert local_field in skill


def test_shared_contract_is_markdown_not_a_runtime_skill_manager() -> None:
    assert SHARED_CONTRACT.suffix == ".md"
    assert not (REPO_ROOT / "src" / "runtime" / "skills").exists()
    assert not (REPO_ROOT / "src" / "settings" / "skills").exists()


def test_repair_locations_are_structured_and_do_not_invent_symbols() -> None:
    contract = SHARED_CONTRACT.read_text(encoding="utf-8")
    repair_contract = contract.split("## 修复位置与代码形状", maxsplit=1)[1].split(
        "\n## ", maxsplit=1
    )[0]
    status_path = (
        REPO_ROOT / "skills" / "using-shanforge" / "references" / "human-readable-status.md"
    )
    status = status_path.read_text(encoding="utf-8")
    repair_status = status.split("### Bug / 修复", maxsplit=1)[1].split("\n### ", maxsplit=1)[0]

    for content in (repair_contract, repair_status):
        for field in ("file", "symbol", "change", "reason", "verification"):
            assert field in content
    assert "模块、配置项或文档章节" in repair_contract


def test_result_package_reports_code_shape_compliance() -> None:
    contract = SHARED_CONTRACT.read_text(encoding="utf-8")
    result_section = contract.split("## 工作 Skill 本职结果包", maxsplit=1)[1]
    package = result_section.split("\n## ", maxsplit=1)[0]

    assert "code_shape_check: passed | failed | not_applicable" in package
    assert "只有本轮没有修改代码时才可 `not_applicable`" in package
    assert "凡修改源码或测试代码不得用 N/A" in package


def test_shared_contract_keeps_evidence_tiers_aligned() -> None:
    contract = SHARED_CONTRACT.read_text(encoding="utf-8")

    for phrase in (
        "普通低、中风险 TaskCard 使用可回读的新鲜命令回执，不强制单独落盘。",
        "批次、里程碑、高风险专项，以及任何阶段、项目或关闭声明必须落盘 evidence。",
    ):
        assert phrase in contract
