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
    assert (
        "不得把旧中心命令、动作注册表或全局脚本当成新流程主控"
        in content
    )


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
    doc_map = (REPO_ROOT / ".factory" / "memory" / "doc-map.md").read_text(
        encoding="utf-8"
    )

    for phrase in (
        "事实源优先级",
        "正式文档和 work item ledger 高于 memory summary",
        "summary 不复制完整正文",
        "PM generated 非事实源",
        "不得把 `.factory/pm/generated/status-dashboard.html` 作为唯一事实源",
    ):
        assert phrase in content

    for phrase in (
        "summary 不复制完整正文",
        "summary 与正式文档冲突时，以正式文档和 ledger 为准",
        "PM generated 非事实源",
    ):
        assert phrase in relevance_gate
        assert phrase in update_checklist

    for phrase in (
        "事实源优先级",
        "正式文档和 work item ledger 高于 memory summary",
        "PM generated 非事实源",
        "不作为事实源",
    ):
        assert phrase in doc_map


def test_project_memory_openai_metadata_is_chinese() -> None:
    content = read_skill_file("agents/openai.yaml")

    for phrase in (
        'display_name: "项目记忆"',
        "恢复 Shanforge 项目上下文",
        "使用 $project-memory",
        "限制读取范围并更新 ledger",
    ):
        assert phrase in content
