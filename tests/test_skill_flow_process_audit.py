from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKITEM = REPO_ROOT / ".factory" / "workitems" / "SKILL-FLOW-AUDIT-001"


def read(path: str | Path) -> str:
    target = path if isinstance(path, Path) else REPO_ROOT / path
    return target.read_text(encoding="utf-8")


def test_skill_flow_audit_workitem_files_define_subtasks() -> None:
    brief = read(WORKITEM / "brief.md")
    plan = read(WORKITEM / "plan.md")
    language_task = read(WORKITEM / "task-briefs" / "language-prompt-review.md")
    flow_task = read(WORKITEM / "task-briefs" / "skill-flow-test.md")

    assert "SKILL-FLOW-AUDIT-001" in brief
    assert "不复用 `SF-SP-011` 编号" in brief
    assert "中文语言专家" in brief
    assert "测试子任务" in brief

    for phrase in (
        "Task 1：恢复流程事实",
        "Task 2：创建两个独立子任务",
        "Task 3：输出完整流程说明",
        "Task 4：验证新增产物",
        "self_check_passed",
        "needs_independent_review",
    ):
        assert phrase in plan

    for phrase in (
        "中文语言专家 + prompt 专家",
        "skills/*/SKILL.md",
        "每个 skill 按 100 分评估",
        "低于 90 分",
        "Top 10 问题模式",
        "019f3329-655c-7a83-84b7-40d8b461b0f6",
    ):
        assert phrase in language_task

    for phrase in (
        "Skill 流程测试工程师",
        "流程矩阵",
        "新功能 / 一句话需求",
        "Bug 修复",
        "Review 反馈",
        "压缩恢复",
        "完成声明 / 收尾",
        "自评隔离",
        "019f3329-96f2-7340-8e8d-620329e378db",
    ):
        assert phrase in flow_task


def test_process_report_covers_development_and_skill_execution_flow() -> None:
    report = read(WORKITEM / "reports" / "software-development-and-skill-flow.md")

    for section in (
        "## 软件开发完整过程",
        "### 1. 会话启动",
        "### 2. 意图澄清",
        "### 3. 需求与验收标准",
        "### 4. 设计与边界",
        "### 5. 实施计划",
        "### 6. 开发执行",
        "### 7. TDD 与 Bug 修复",
        "### 8. 完成前验证",
        "### 9. 独立评审",
        "### 10. 评审反馈处理",
        "### 11. 人工确认门",
        "### 12. 提交与 PR 闭环",
        "### 13. 发布、维护和复盘",
        "## Skill 调用完整流程",
        "## 任务执行完整流程",
        "## 本轮创建的子任务",
    ):
        assert section in report

    for phrase in (
        "`using-shanforge`",
        "`project-memory`",
        "`writing-plans`",
        "`subagent-driven-development`",
        "`executing-plans`",
        "`tdd-workflow`",
        "`systematic-debugging`",
        "`verification-before-completion`",
        "`requesting-code-review`",
        "`receiving-code-review`",
        "`gitcommitzh`",
        "工作 skill 只完成自己的专业任务，不决定下一个 skill",
        "输出统一状态包",
        "完成声明只能在验证、评审、人工确认和 memory sync 齐备后给出",
    ):
        assert phrase in report


def test_core_workflow_skills_expose_required_gates() -> None:
    expected = {
        "skills/using-shanforge/SKILL.md": (
            "流程总控 / CTO",
            "选择唯一下一步 skill",
            "工作 skill 状态回写协议",
            "pending_human_confirmation",
            "references/remote-pr-handoff.md",
        ),
        "skills/project-memory/SKILL.md": (
            "会话恢复",
            "读取范围",
            ".factory/memory/runtime-brief.md",
            "ledger",
        ),
        "skills/writing-plans/SKILL.md": (
            ".factory/workitems/<WORKITEM-ID>/plan.md",
            "task-briefs",
            "review gate",
            "工作结果：",
        ),
        "skills/subagent-driven-development/SKILL.md": (
            "task brief",
            "evidence",
            "ready_for_review",
            "工作结果：",
        ),
        "skills/executing-plans/SKILL.md": (
            "先批判性 review plan",
            "evidence",
            "review checkpoint",
            "工作结果：",
        ),
        "skills/tdd-workflow/SKILL.md": (
            "测试先于代码",
            "Bug 根因先于修复",
            "RED",
            "GREEN",
        ),
        "skills/systematic-debugging/SKILL.md": (
            "根因调查",
            "禁止猜测式补丁",
            "修复必须针对根因",
            "ledger",
        ),
        "skills/verification-before-completion/SKILL.md": (
            "没有新鲜验证证据，不得声明完成",
            "exit code",
            "evidence",
            "工作结果：",
        ),
        "skills/requesting-code-review/SKILL.md": (
            "独立 reviewer",
            "Spec Review",
            "Quality Review",
            "pending_human_confirmation",
        ),
        "skills/receiving-code-review/SKILL.md": (
            "先核实反馈再修改",
            "禁止盲改",
            "每项修复后都要验证",
            "response 已写入",
        ),
        "skills/gitcommitzh/SKILL.md": (
            "审查 Git 工作区",
            "提交前必须先核对",
            "work item ledger",
            "gitcommitzh 不负责创建、推送或合并 PR",
        ),
    }

    for path, phrases in expected.items():
        content = read(path)
        for phrase in phrases:
            assert phrase in content, f"{path} missing {phrase}"


def test_iteration_4_flow_completeness_artifacts_do_not_reintroduce_old_factory_gate() -> None:
    paths = (
        "skills/using-shanforge/SKILL.md",
        "skills/using-shanforge/references/black-box-flow-eval.md",
        "skills/using-shanforge/references/remote-pr-handoff.md",
        WORKITEM / "evidence" / "iteration-4-s1-s6-dry-run-transcript.md",
    )
    combined = "\n".join(read(path) for path in paths)

    for phrase in (
        "factory-dispatch loop-gate",
        "factory-workitem-loop-gate",
        "scripts/factory-workitem-loop-gate",
    ):
        assert phrase not in combined

    assert "factory-pr-remote-open" not in combined
    assert "factory-pr-remote-merge" not in combined


def test_brainstorming_reports_status_while_using_shanforge_owns_routing() -> None:
    brainstorming = read("skills/brainstorming/SKILL.md")
    openai_metadata = read("skills/brainstorming/agents/openai.yaml")
    reviewer_prompt = read("skills/brainstorming/spec-document-reviewer-prompt.md")
    using_shanforge = read("skills/using-shanforge/SKILL.md")

    for phrase in (
        "流程路由由 `using-shanforge` 根据阶段、work item 状态和 ledger 判断",
        "本 skill 只回写 brief、批准状态、outputs、evidence、ledger_event 和 `needs`",
        "工作结果：",
        "skill: brainstorming",
        "approval:",
        "ledger_event:",
        "`needs` 只是状态回写，不是 skill 路由决策",
    ):
        assert phrase in brainstorming

    for phrase in (
        "下一步 skill：",
        "给出下一步 skill",
        "handed_off",
        "再交给对应下一步 skill",
    ):
        assert phrase not in brainstorming
        assert phrase not in openai_metadata

    assert "是否写清下一步 skill" not in reviewer_prompt
    assert "批准状态、产物路径、证据、ledger_event、needs" in reviewer_prompt
    assert "避免替流程总控指定 skill" in reviewer_prompt

    assert "选择唯一下一步 skill" in using_shanforge
    assert "工作 skill 完成时只返回状态包，不写下一步 skill" in using_shanforge
