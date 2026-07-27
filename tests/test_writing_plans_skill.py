from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "skills" / "writing-plans"


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_writing_plans_skill_localizes_superpowers_semantics() -> None:
    skill = read("skills/writing-plans/SKILL.md")

    assert "name: writing-plans" in skill
    assert "多步骤任务" in skill
    assert "动代码前" in skill
    assert "已批准的 spec、需求、设计或 work item brief" in skill
    assert ".factory/workitems/<WORKITEM-ID>/plan.md" in skill
    assert ".factory/workitems/<WORKITEM-ID>/task-briefs/" in skill
    assert "docs/superpowers/plans" not in skill

    for phrase in (
        "先锁定文件结构",
        "每个文件只有一个清晰职责",
        "一个任务卡对应一个可验收交付物",
        "一个任务必须能独立产生可测试结果",
        "任务内部 checklist",
        "Red",
        "Green",
        "精确文件路径",
        "真实命令",
        "期望输出",
        "禁止占位符",
        "计划自审",
        "plan review",
        "本 skill 不写下一步 skill",
        "只写 plan、task brief、review handoff 和状态回写",
        "needs:",
    ):
        assert phrase in skill

    assert "执行阶段交给 `subagent-driven-development`" not in skill
    assert "## 执行交接" not in skill
    assert "推荐粒度是 2-5 分钟" not in skill
    assert "一步只做一个动作" not in skill


def test_writing_plans_excludes_simple_code_and_unit_test_changes() -> None:
    skill = read("skills/writing-plans/SKILL.md")
    metadata = read("skills/writing-plans/agents/openai.yaml")

    for phrase in (
        "简单任务不触发",
        "局部代码修改加对应单测",
        "不创建 plan、task brief 或计划评审",
        "定向测试和必要静态检查",
        "不得因为已有已批准输入或尚无 plan 就强制触发",
        "用户明确要求正式计划时，覆盖简单任务判定",
        "公共接口、跨层边界、数据 schema、迁移、依赖、安全权限、外部系统或发布方式",
        "出现影响扩大的证据时再升级验证范围",
        "实现阶段是否记录 ledger 和 evidence 由流程总控及实现工作流决定",
        "`outputs`、`evidence` 和 `ledger_event` 为空",
    ):
        assert phrase in skill

    assert "简单任务不触发" in metadata
    assert "局部代码修改加对应单测" in metadata
    assert "用户明确要求正式计划" in metadata


def test_writing_plans_references_define_plan_and_task_templates() -> None:
    expected = {
        "skills/writing-plans/references/workitem-plan-template.md": (
            "# <功能名称> 实施计划",
            "给执行者",
            "交还 `using-shanforge` 流程总控判断下一步",
            "目标：",
            "架构：",
            "技术栈：",
            "## 输入",
            "## 范围",
            "| 类型 | 路径 | 职责 |",
            "任务 N",
            "- [ ]",
            "步骤 1：红灯，编写失败测试",
            "步骤 2：运行测试并确认失败",
            "运行命令",
            "期望输出",
            "步骤 5：证据和记忆同步",
            ".factory/memory/",
            "## 计划自审",
        ),
        "skills/writing-plans/references/task-brief-template.md": (
            "# 任务简报",
            "## 工作项",
            "目标",
            "输入",
            "已批准计划",
            "相关规格 / 需求 / 设计",
            "允许修改",
            "禁止修改",
            "写红灯测试",
            "验证命令",
            "输出报告",
            "验证证据：",
            "实现报告：",
            "评审输入简报：",
        ),
        "skills/writing-plans/references/plan-review-template.md": (
            "# 计划评审",
            "## 输入",
            "## 检查项",
            "| 类别 | 检查内容 |",
            "完整性",
            "规格一致性",
            "任务拆分",
            "可构建性",
            "**状态：** 通过 | 发现问题",
            "下一步由 `using-shanforge` 流程总控判断",
        ),
    }

    for path, phrases in expected.items():
        content = read(path)
        for phrase in phrases:
            assert phrase in content

    workitem_plan = read("skills/writing-plans/references/workitem-plan-template.md")
    plan_review = read("skills/writing-plans/references/plan-review-template.md")
    assert "REQUIRED NEXT SKILL" not in workitem_plan
    assert "subagent-driven-development` or `executing-plans" not in workitem_plan
    assert "计划可交给 `subagent-driven-development`" not in plan_review

    all_references = "\n".join(read(path) for path in expected)
    for phrase in (
        "# <Feature Name> Implementation Plan",
        "**Goal:**",
        "**Architecture:**",
        "**Tech Stack:**",
        "## Inputs",
        "## Scope",
        "## Files",
        "## Tasks",
        "Run:",
        "Expected output:",
        "# Task brief",
        "## Work item",
        "# Plan Review",
        "## What to Check",
        "## Output Format",
        "**Status:** Approved | Issues Found",
        "Recommendations",
        "Completeness",
        "Spec Alignment",
        "Task Decomposition",
        "Buildability",
        "checkbox",
        "memory sync",
        "FAIL with the missing behavior or contract error",
        "<command>",
        "<expected output>",
    ):
        assert phrase not in all_references


def test_writing_plan_templates_require_design_test_and_review_slices() -> None:
    skill = read("skills/writing-plans/SKILL.md")
    workitem_plan = read("skills/writing-plans/references/workitem-plan-template.md")
    task_brief = read("skills/writing-plans/references/task-brief-template.md")

    assert "计划只能生成候选执行输入，不执行代码" in skill

    for phrase in (
        "设计方案",
        "接口设计",
        "UI 或 `N/A`",
        "UI 写 `N/A` 时必须写原因",
        "测试设计",
        "开发",
        "单测",
        "review",
        "集成测试",
        "缺测试设计则失败",
        "UI 写 `N/A` 但无原因则失败",
        "发现占位语则失败",
    ):
        assert phrase in workitem_plan
        assert phrase in task_brief


def test_writing_plans_openai_metadata_is_chinese() -> None:
    metadata_path = SKILL_DIR / "agents" / "openai.yaml"
    metadata = metadata_path.read_text(encoding="utf-8")

    assert 'display_name: "编写实施计划"' in metadata
    assert "work item plan" in metadata
    assert "任务 brief" in metadata
