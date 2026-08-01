from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "project-memory"


def read_skill_file(path: str) -> str:
    return (SKILL_ROOT / path).read_text(encoding="utf-8")


def markdown_section(content: str, heading: str) -> str:
    start = content.index(heading)
    match = re.search(r"\n## ", content[start + len(heading) :])
    if match is None:
        return content[start:]
    return content[start : start + len(heading) + match.start()]


def test_project_memory_skill_declares_session_recovery_scope() -> None:
    content = read_skill_file("SKILL.md")
    frontmatter = content.split("---", 2)[1]

    assert "name: project-memory" in frontmatter
    assert "会话恢复" in frontmatter
    assert ".factory/memory/runtime-brief.md" in content
    assert ".factory/memory/current-state.md" in content
    assert ".factory/memory/doc-map.md" in content
    assert "先复用已有会话卡和压缩记忆" in content
    assert "输出压缩后的会话卡，并写清本轮排除的背景文件" in content
    assert "若已有同一 work item 的新鲜会话卡，复用它" in content
    assert "禁止默认读取阶段 `docs/` 长文" in content
    assert "旧会话脚本只作为已迁移来源记录" in content
    assert "不得把旧中心命令、动作注册表或全局脚本当成新流程主控" in content
    assert "不用于无项目影响的 `direct_answer` 或 `lightweight_analysis`" in content
    assert "只有项目状态查询、任务延续、上下文恢复或项目化流程" in content
    assert "不得先读 memory 再判断请求是否简单" in content


def test_project_memory_references_capture_migrated_session_rules() -> None:
    expected_files = {
        "references/session-start-checklist.md": (
            "目标是生成压缩会话卡",
            "若已有同一 work item 的新鲜会话卡，复用它",
            "才读取 `.factory/memory/runtime-brief.md`",
            "明确排除项",
            "写入会话 ledger 事件",
        ),
        "references/relevance-gate.md": (
            "默认只读 summary",
            "当前任务直接修改的正式文档",
            "进入实现前必须回源技术选型",
            "禁止用“稳妥”作为散读理由",
        ),
        "references/session-card-template.md": (
            "## 本轮目标",
            "## 已读取上下文",
            "## 未读 / 已排除上下文",
            "## 禁止动作",
            "## 待决事项",
            "交回 using-shanforge 判断",
        ),
        "references/current-state-update-checklist.md": (
            "只写已观察到的事实",
            "同步 `tasks.summary.md`",
            "同步 `tests.summary.md`",
            "不要把计划中未执行的动作写成已完成",
        ),
    }

    for path, phrases in expected_files.items():
        content = read_skill_file(path)
        for phrase in phrases:
            assert phrase in content


def test_session_start_uses_a_conditional_read_chain_and_stops_when_sufficient() -> None:
    skill = read_skill_file("SKILL.md")
    checklist = read_skill_file("references/session-start-checklist.md")

    for content in (skill, checklist):
        for phrase in (
            "条件读取链",
            "够用即停",
            "当前对话中的新鲜会话卡足够时，读取 memory 文件数必须为 0",
            "不能只读 `.factory/memory/current-state.md`",
            "不得固定读取 `agent-session.md`、`runtime-brief.md`、`current-state.md` 三件套",
            "每次扩展读取前先写明事实缺口",
            "一次只读取一个最小片段",
        ):
            assert phrase in content
    assert (
        "按最小集合读取 `.factory/memory/runtime-brief.md` 和 `.factory/memory/current-state.md`"
    ) not in skill
    assert "二选一" in skill
    assert "二选一" in checklist


def test_current_state_is_a_bounded_current_projection() -> None:
    state_path = REPO_ROOT / ".factory" / "memory" / "current-state.md"
    state = state_path.read_text(encoding="utf-8")
    tasks_summary = (REPO_ROOT / ".factory" / "memory" / "tasks.summary.md").read_text(
        encoding="utf-8"
    )

    assert len(state.encode("utf-8")) <= 16 * 1024
    assert len(state.splitlines()) <= 80
    for heading in (
        "## 活跃任务",
        "## 阻塞项",
        "## 最近事实",
        "## 唯一下一动作",
        "## 历史回源",
    ):
        assert heading in state
    assert "TASK-DESIGN-001 / R019" not in state
    assert "TASK-DESIGN-001" in tasks_summary
    assert ".factory/workitems/<WORKITEM-ID>/ledger.jsonl" in state
    assert ".factory/memory/tasks.summary.md" in state
    recent = markdown_section(state, "## 最近事实")
    assert len(re.findall(r"^- ", recent, flags=re.MULTILINE)) <= 5

    active = markdown_section(state, "## 活跃任务")
    blockers = markdown_section(state, "## 阻塞项")
    if "- 活跃任务数：0" in state:
        assert re.search(r"- 当前阶段：`[^`]+ / CLOSED`", state)
        assert "- 当前无活动任务。" in active
        assert "- 当前 Gate：`none`" in state
        assert "- 无。" in blockers
    else:
        stage_match = re.search(
            r"- 当前阶段：`(?P<work_item>[A-Z0-9-]+) / (?P<task>[A-Z0-9-]+)`",
            state,
        )
        assert stage_match
        work_item = stage_match.group("work_item")
        active_task = stage_match.group("task")
        assert f"`{active_task}`" in active
        ledger = REPO_ROOT / ".factory" / "workitems" / work_item / "ledger.jsonl"
        assert ledger.is_file()
        assert active_task in ledger.read_text(encoding="utf-8")
        assert "- 当前 Gate：`none`" not in state

    blocker_count = re.search(r"- 阻塞项数：(?P<count>\d+)", state)
    assert blocker_count
    assert ("- 无。" in blockers) == (int(blocker_count.group("count")) == 0)


def test_memory_sync_downgrades_inactive_tasks_without_deleting_audit_facts() -> None:
    skill = read_skill_file("SKILL.md")
    checklist = read_skill_file("references/current-state-update-checklist.md")

    for content in (skill, checklist):
        for phrase in (
            "已关闭任务在下一次 memory sync",
            "从 `current-state.md` 降级",
            "最近事实最多保留 5 条",
            "`current-state.md` 不超过 16 KiB 和 80 行",
            "ledger、evidence、review 和 report 永不因降级删除",
        ):
            assert phrase in content

    work_item = REPO_ROOT / ".factory" / "workitems" / "FLOW-CONTRACT-001"
    active = markdown_section(
        (REPO_ROOT / ".factory/memory/current-state.md").read_text(encoding="utf-8"),
        "## 活跃任务",
    )
    assert "FLOW-TASK-012" not in active
    assert '"task":"FLOW-TASK-012"' in (work_item / "ledger.jsonl").read_text(encoding="utf-8")
    for path in (
        work_item / "evidence/FLOW-TASK-012-review-fix-verification.md",
        work_item / "reviews/FLOW-TASK-012-independent-rereview-iteration-3.md",
        work_item / "reports/FLOW-TASK-012-implementer-report.md",
    ):
        assert path.is_file(), path


def test_project_memory_ledger_schema_prevents_repeat_work() -> None:
    content = read_skill_file("references/memory-ledger-event-template.md")

    for phrase in (
        '"event_id"',
        '"idempotency_key"',
        '"session_start"',
        '"workitem_event"',
        "status=approved|done|passed",
        "不得重复执行",
        ".factory/workitems/<WORKITEM-ID>/ledger.jsonl",
        ".factory/memory/session-ledger.jsonl",
        '"next_status"',
        '"next_required_action"',
    ):
        assert phrase in content

    assert '"next_skill"' not in content


def test_project_memory_declares_fact_source_priority_and_summary_limits() -> None:
    content = read_skill_file("SKILL.md")
    relevance_gate = read_skill_file("references/relevance-gate.md")
    update_checklist = read_skill_file("references/current-state-update-checklist.md")
    doc_map = (REPO_ROOT / ".factory" / "memory" / "doc-map.md").read_text(encoding="utf-8")

    for phrase in (
        "事实源优先级",
        "正式文档和 work item ledger 高于 memory summary",
        "summary 不复制完整正文",
        "HTML 和 cache 都是可重建投影",
        "不得把 `.factory/cache/site/current/index.html` 作为正式事实源",
    ):
        assert phrase in content

    for phrase in (
        "summary 不复制完整正文",
        "summary 与正式文档冲突时，以正式文档和 ledger 为准",
        "HTML 和 cache 都是非事实投影",
    ):
        assert phrase in relevance_gate
        assert phrase in update_checklist

    for phrase in (
        "事实源优先级",
        "正式文档和 work item ledger 高于 memory summary",
        "HTML 和 cache 是可重建投影",
        "不作为事实源",
    ):
        assert phrase in doc_map


def test_completion_output_persistence_contract_is_explicit() -> None:
    memory = read_skill_file("SKILL.md")
    controller = (REPO_ROOT / "skills" / "using-shanforge" / "SKILL.md").read_text(encoding="utf-8")
    contract = (REPO_ROOT / "docs" / "05-design" / "workflow-execution-design.md").read_text(
        encoding="utf-8"
    )
    factory_readme = (REPO_ROOT / ".factory" / "README.md").read_text(encoding="utf-8")

    for phrase in (
        "完成输出与持久化契约",
        "当前会话可见性协议",
        "`direct_answer` / `lightweight_analysis`",
        "默认不落盘、不写 ledger、不写 memory",
        "开发期只写必要 checkpoint；批次收口写一套 ledger、evidence/report",
        "当前会话必须能看见收口状态",
        "子 agent 或自循环完成后不得只静默写文件",
        "任务开始",
        "阶段切换",
        "文件编辑前",
        "关键命令前后",
        "阻塞 gate",
    ):
        assert phrase in controller

    for phrase in (
        "写入边界",
        "状态变化、gate 切换、上下文压缩恢复、关闭前验证或提交前检查",
        "outputs / evidence / review / report 路径索引",
        "命令全文、临时推理、当前会话答复、子 agent 完整输出和正式文档正文不得写入 memory",
    ):
        assert phrase in memory

    for phrase in (
        "统一任务包",
        "落盘规则",
        "Review 不能替代 verification",
        "Verification 不能替代 human confirmation",
        "缺 evidence、implementer report、review input package 或 ledger event 时",
    ):
        assert phrase in contract

    for phrase in (
        "破坏性迁移规则",
        "只保留最新正式资产和正式内容",
        "执行审计事实",
    ):
        assert phrase in factory_readme


def test_project_memory_openai_metadata_is_chinese() -> None:
    content = read_skill_file("agents/openai.yaml")

    for phrase in (
        'display_name: "项目记忆"',
        "恢复 Shanforge 项目上下文",
        "使用 $project-memory",
        "限制读取范围并更新 ledger",
    ):
        assert phrase in content
