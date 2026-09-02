from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_subagent_driven_development_skill_is_shanforge_localized() -> None:
    skill = read("skills/subagent-driven-development/SKILL.md")

    assert "name: subagent-driven-development" in skill
    assert "独立任务" in skill
    assert ".factory/workitems/<WORKITEM-ID>/plan.md" in skill
    assert ".factory/workitems/<WORKITEM-ID>/task-briefs/" in skill
    assert ".factory/workitems/<WORKITEM-ID>/ledger.jsonl" in skill
    assert "不要让子 agent 自己读完整 plan" in skill
    assert "本 skill 只准备集中评审输入" in skill
    assert "实现者不得自批 `approved`" in skill
    assert "DONE_WITH_CONCERNS" in skill
    assert "NEEDS_CONTEXT" in skill
    assert "BLOCKED" in skill
    for phrase in (
        "同一依赖层中 dependencies 已完成",
        "无文件冲突",
        "无未确认 Gate",
        "共享契约已定",
        "每张可并行任务卡创建一个独立子任务并行执行",
        "完成后由主控汇总",
    ):
        assert phrase in skill
    assert "禁止并行派发多个实现子 agent" not in skill
    assert "不并发、不跳号" not in skill
    assert "工作结果：" in skill
    assert "needs:" in skill
    assert "本 skill 不决定完成后交给谁" in skill
    assert "只写状态、产物、证据和 `needs`" in skill
    assert "docs/superpowers" not in skill
    assert "finishing-a-development-branch" not in skill
    assert "## 与其他 skill 的关系" not in skill
    assert "requesting-code-review" not in skill
    assert "verification-before-completion" not in skill
    assert "gitcommitzh" not in skill


def test_execution_skills_block_when_task_gate_inputs_are_missing() -> None:
    expected_phrases = (
        "任务 gate",
        "缺目标、验收标准、依赖、允许文件或必要验证命令时不得开始执行",
        "单个低、中风险任务不要求 verification evidence、implementer report 或 review checkpoint",
        "批次 / 里程碑缺最终验证证据、实现摘要、review input 或 ledger event 时",
        "不得推进到 `ready_for_review`",
        "完成状态只能回写为：`ready_for_review`、`blocked` 或 `needs_user_input`",
    )

    for path in (
        "skills/executing-plans/SKILL.md",
        "skills/subagent-driven-development/SKILL.md",
    ):
        skill = read(path)
        for phrase in expected_phrases:
            assert phrase in skill


def test_subagent_driven_development_does_not_route_next_skill() -> None:
    skill = read("skills/subagent-driven-development/SKILL.md")

    for phrase in (
        "子 agent 不决定下一步 skill",
        "只执行分配给它的 task brief",
        "不判断后续 skill",
        "不进入下一任务决策",
        "不反向决定流程路由",
    ):
        assert phrase in skill


def test_subagent_execution_skips_only_completed_or_closed_taskcards() -> None:
    skill = read("skills/subagent-driven-development/SKILL.md")

    assert "只跳过 TaskCard 生命周期为 `completed` 或 `closed` 的任务" in skill
    assert "`review_status=approved` 不作为跳过依据" in skill
    assert "TaskCard 仍为 `active` 或 `ready_for_review`" in skill
    assert "跳过 ledger 中已经 `approved` 或 `done` 的任务" not in skill


def test_worker_statuses_have_one_controller_disposition() -> None:
    skill = read("skills/subagent-driven-development/SKILL.md")

    for row in (
        "| `DONE` | 当前 TaskCard 实现结束；继续当前批次，不写批次状态 |",
        "| `DONE_WITH_CONCERNS` | 先处理 concerns；非阻塞时继续当前批次，不写批次状态 |",
        "| `NEEDS_CONTEXT` | 补最小上下文并重派；无法补足时写 `needs_user_input` |",
        "| `BLOCKED` | 写 `blocked` 并交还 Sol |",
    ):
        assert row in skill

    assert "`DONE` 只表示该 TaskCard 的实现工作结束" in skill
    assert "不得从单个 worker `DONE` 推导 `ready_for_review`" in skill
    assert (
        "只有集中 evidence、实现摘要、review input 和 ledger event 齐全的批次候选才可写 "
        "`ready_for_review`"
    ) in skill


def test_subagent_references_define_handoff_and_review_templates() -> None:
    expected = {
        "skills/subagent-driven-development/references/implementer-task-template.md": (
            "Implementer Task",
            "完整 task brief",
            "Work item",
            "DONE",
            "DONE_WITH_CONCERNS",
            "BLOCKED",
            "NEEDS_CONTEXT",
            "不要生成逐任务 evidence、report 或 review input",
            "可继续当前批次",
        ),
        "skills/subagent-driven-development/references/spec-review-template.md": (
            "Spec Review",
            "不要相信实现报告",
            "读取实际 diff",
            "缺失需求",
            "额外工作",
            "file:line",
        ),
        "skills/subagent-driven-development/references/quality-review-template.md": (
            "Quality Review",
            "只在 Spec Review 通过后执行",
            "Critical",
            "Important",
            "Minor",
            "分层",
            "Assessment",
        ),
        "skills/subagent-driven-development/references/status-handling-checklist.md": (
            "DONE_WITH_CONCERNS",
            "NEEDS_CONTEXT",
            "BLOCKED",
            "不生成逐任务 review input",
            "needs: review",
        ),
    }

    for path, phrases in expected.items():
        content = read(path)
        for phrase in phrases:
            assert phrase in content

    status_checklist = read(
        "skills/subagent-driven-development/references/status-handling-checklist.md"
    )
    assert "进入 Spec Review" not in status_checklist
    assert "Review 状态回流" not in status_checklist
    assert "收到 Spec Review" not in status_checklist
    assert "收到 Quality Review" not in status_checklist
    assert "收到 reviewer `approved`" not in status_checklist


def test_execution_workflow_docs_do_not_keep_stale_review_state() -> None:
    contract = read("docs/05-design/workflow-execution-design.md")
    codex_tools = read("skills/using-shanforge/references/codex-tools.md")

    assert "Review 不能替代 verification" in contract
    assert "Verification 不能替代 human confirmation" in contract
    assert "作者只能推进到 `ready_for_review`" in contract
    assert "finishing-a-development-branch" not in contract
    assert "finishing-a-development-branch" not in codex_tools
    assert "gitcommitzh" in codex_tools


def test_development_loop_separates_test_code_verification_and_review_tasks() -> None:
    contract = read("docs/05-design/workflow-execution-design.md")

    for phrase in (
        "开发",
        "测试",
        "Review 不能替代 verification",
        "缺 evidence、implementer report、review input package 或 ledger event",
        "作者只能推进到 `ready_for_review`",
    ):
        assert phrase in contract


def test_executing_plans_skill_is_inline_fallback() -> None:
    skill = read("skills/executing-plans/SKILL.md")

    assert "name: executing-plans" in skill
    assert "written implementation plan" in skill
    assert ".factory/workitems/<WORKITEM-ID>/plan.md" in skill
    assert ".factory/workitems/<WORKITEM-ID>/ledger.jsonl" in skill
    assert "先批判性 review plan" in skill
    assert "逐步执行" in skill
    assert "不生成独立 evidence、report 或 review input" in skill
    assert "集中质量 Checkpoint" in skill
    assert "工作结果：" in skill
    assert "needs:" in skill
    assert "本 skill 不决定完成后交给谁" in skill
    assert "只写状态、产物、证据和 `needs`" in skill
    assert "STOP" in skill
    assert "BLOCKED" in skill
    assert "禁止猜测" in skill
    assert "docs/superpowers" not in skill
    assert "finishing-a-development-branch" not in skill
    assert "## 与其他 skill 的关系" not in skill
    assert "requesting-code-review" not in skill
    assert "verification-before-completion" not in skill
    assert "receiving-code-review" not in skill
    assert "gitcommitzh" not in skill


def test_using_shanforge_is_flow_controller_and_owns_skill_routing() -> None:
    skill = read("skills/using-shanforge/SKILL.md")
    metadata = read("skills/using-shanforge/agents/openai.yaml")

    for phrase in (
        "流程总控 / CTO",
        "选择唯一下一步 skill",
        "工作 skill 不决定前置、后置或下一步 skill",
        "路由表",
        "pending_human_confirmation",
        "工作 skill 状态回写协议",
        "工作 skill 完成时只返回状态包，不写下一步 skill",
        "人工确认门",
    ):
        assert phrase in skill

    for phrase in (
        "判断请求是否影响项目",
        "选择唯一下一步 skill",
        "工作 skill 只回写状态、证据和 needs",
    ):
        assert phrase in metadata


def test_execution_workflow_openai_metadata_is_chinese() -> None:
    subagent_metadata = read("skills/subagent-driven-development/agents/openai.yaml")
    executing_metadata = read("skills/executing-plans/agents/openai.yaml")

    assert 'display_name: "子代理驱动开发"' in subagent_metadata
    assert "批次末集中验证和评审" in subagent_metadata
    assert "不要逐任务落盘过程材料" in subagent_metadata

    assert 'display_name: "执行实施计划"' in executing_metadata
    assert "批次末集中验证和评审" in executing_metadata
    assert "不要逐任务写 evidence、report 或 review input" in executing_metadata
