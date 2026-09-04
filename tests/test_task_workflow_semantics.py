from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_flow_controller_defines_processing_modes_before_skill_routing() -> None:
    skill = read("skills/using-shanforge/SKILL.md")

    for phrase in (
        "处理模式判定",
        "概念边界",
        "direct_answer",
        "lightweight_analysis",
        "project_workitem",
        "tracked_task",
        "Method",
        "Workflow 内部的做法、检查清单或分析技术",
        "Tool",
        "工具调用只记录 event / evidence，不等于 TaskCard",
        "gate",
        "event",
        "只要一个答案",
        "会影响后续项目状态",
        "需要跨会话继续",
        "需要依赖、并行、评审或验收",
        "任务卡不是因为这也是任务才创建",
        "先根据当前消息判定处理模式",
        "再使用 `project-memory` 恢复项目上下文",
        "简单任务快速通道",
    ):
        assert phrase in skill

    assert skill.index("先根据当前消息判定处理模式") < skill.index(
        "再使用 `project-memory` 恢复项目上下文"
    )


def test_direct_analysis_and_tracked_task_share_output_contract() -> None:
    brainstorming = read("skills/brainstorming/SKILL.md")
    requirements = read("skills/requirements-engineering/SKILL.md")

    for phrase in (
        "没有项目化意图时，只做会话澄清或轻量分析",
        "不落盘、不创建 work item、不写 ledger",
    ):
        assert phrase in brainstorming

    for phrase in (
        "轻量需求分析",
        "项目化需求任务",
        "输出契约一致",
        "目标",
        "用户角色",
        "主流程",
        "异常流程",
        "业务规则",
        "安全 / 权限要求",
        "验收标准",
        "未决问题",
    ):
        assert phrase in requirements


def test_task_card_granularity_parallelism_and_bug_confirmation_gates() -> None:
    writing_plans = read("skills/writing-plans/SKILL.md")
    subagent = read("skills/subagent-driven-development/SKILL.md")
    debugging = read("skills/systematic-debugging/SKILL.md")
    tdd = read("skills/tdd-workflow/SKILL.md")

    assert "推荐粒度是 2-5 分钟" not in writing_plans
    for phrase in (
        "任务卡粒度是一个可验收交付物",
        "步骤粒度留在 task 内部 checklist",
        "读文件、运行命令、写失败测试、记录 evidence 不是任务卡",
    ):
        assert phrase in writing_plans

    for phrase in (
        "可并行任务卡",
        "dependencies 已完成",
        "无文件冲突",
        "无未确认 Gate",
        "每张可并行任务卡创建一个独立子任务",
    ):
        assert phrase in subagent

    for phrase in (
        "root_cause_found",
        "fault_owner",
        "低、中风险不新增人工 Gate",
        "高风险依次等待根因确认",
        "不能复现时先要求更多信息",
    ):
        assert phrase in debugging

    for phrase in (
        "低、中风险不新增人工 Gate",
        "高风险必须先通过根因确认和修复方案确认 Gate",
        "单次缺陷修复不默认运行全仓测试",
    ):
        assert phrase in tdd


def test_flow_controller_routes_simple_code_changes_without_formal_plan() -> None:
    controller = read("skills/using-shanforge/SKILL.md")

    for phrase in (
        "简单代码变更直接实施",
        "局部代码修改加对应单测",
        "不得路由到 `writing-plans`",
        "直接进入 `tdd-workflow`",
        "全量测试不是简单任务的默认步骤",
        "用户明确要求正式计划时，覆盖简单代码变更判定",
        "公共接口、跨层边界、数据 schema、迁移、依赖、安全权限、外部系统或发布方式",
        "再升级到正式计划流程",
    ):
        assert phrase in controller

    simple_route = next(
        line for line in controller.splitlines() if line.startswith("| 需求明确的简单代码变更 |")
    )
    assert "用户未明确要求正式计划" in simple_route


def test_frontend_patterns_work_item_status_uses_design_decision_as_need() -> None:
    skill = read("skills/frontend-patterns/SKILL.md")

    for phrase in (
        "- status: ready_for_review | blocked | needs_user_input",
        "- ledger_event: <event id>",
        "design_decision",
        "`design_decision` 只是 `needs` 值，不是状态",
        "status: needs_user_input",
    ):
        assert phrase in skill


def test_art_asset_pipeline_skill_outputs_confirmed_assets_only() -> None:
    skill = read("skills/art-asset-pipeline/SKILL.md")

    for phrase in (
        "美术方向 + 资源管线",
        "独立美术样张",
        "用户确认美术方向",
        "资源清单",
        "独立美术资源包",
        "游戏开发资源包",
        "候选图跨会话保留",
        "等待用户选择时不得删除",
        "删除未被选中的候选图",
        "最终资源包只包含用户确认过的图",
        "candidates/",
        "tmp/",
        "approved/",
        "manifest.json",
        "imagegen",
        "remove_chroma_key.py",
    ):
        assert phrase in skill

    assert "所有候选图先放 `tmp/`" not in skill
    assert "全部写入 `tmp/`" not in skill
    assert "不属于 UI 项目流程的独立美术或游戏资源" in skill
    assert "不承接 UI 项目中的素材阶段" in skill
    assert "UI 美术图" not in skill
    assert "art-asset-pipeline 承接 UI 项目素材" not in skill


def test_black_box_eval_covers_task_card_creation_boundaries() -> None:
    reference = read("skills/using-shanforge/references/black-box-flow-eval.md")

    for phrase in (
        "FLOW-S6-direct-analysis-no-task-card",
        "分析系统登录的需求",
        "不创建任务卡",
        "FLOW-S7-decomposed-analysis-requires-task-card",
        "分析本项目的登录能力，将结果写入当前 WorkItem，并创建登录需求 TaskCard，"
        "作为后续需求、设计和验收的正式输入",
        "必须创建任务卡",
        "核心输出契约一致",
    ):
        assert phrase in reference


def test_bug_fix_routes_by_owner_and_only_high_risk_uses_two_gates() -> None:
    controller = read("skills/using-shanforge/SKILL.md")
    reference = read("skills/using-shanforge/references/black-box-flow-eval.md")

    for phrase in (
        "发现 Bug 或验证失败",
        "`systematic-debugging`",
        "`root_cause_found`",
        "低、中风险 Bug 根因已定位",
        "高风险 Bug 根因已定位",
        "高风险 Bug 根因和修复方案均已确认",
        "`tdd-workflow`",
    ):
        assert phrase in controller

    for phrase in (
        "FLOW-S4-fix-bug-root-cause",
        "归因和风险 Gate",
        "低、中风险不新增人工 Gate",
        "只有高风险才依次设置根因确认和修复方案确认 Gate",
        "未为低、中风险制造人工确认 Gate",
        "不默认全仓测试",
    ):
        assert phrase in reference
