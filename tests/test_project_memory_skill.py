from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "project-memory"


def read_skill_file(path: str) -> str:
    return (SKILL_ROOT / path).read_text(encoding="utf-8")


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
        "SQLite、HTML 和 cache 都是可重建投影",
        (
            "不得把 `.factory/index/project-knowledge.sqlite3` 或 "
            "`.factory/cache/site/current/index.html` 作为正式事实源"
        ),
    ):
        assert phrase in content

    for phrase in (
        "summary 不复制完整正文",
        "summary 与正式文档冲突时，以正式文档和 ledger 为准",
        "SQLite、HTML 和 cache 都是非事实投影",
    ):
        assert phrase in relevance_gate
        assert phrase in update_checklist

    for phrase in (
        "事实源优先级",
        "正式文档和 work item ledger 高于 memory summary",
        "SQLite、HTML 和 cache 是可重建投影",
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
        "写 work item ledger、必要 evidence/report",
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
