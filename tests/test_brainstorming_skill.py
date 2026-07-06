from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "brainstorming"


def test_brainstorming_skill_is_chinese_and_shanforge_state_driven() -> None:
    content = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")

    frontmatter = content.split("---", 2)[1]
    assert "基于 shanforge 当前阶段、work item 状态和用户意图" in frontmatter
    assert "You MUST use this" not in content
    assert "Brainstorming Ideas Into Designs" not in content
    assert "Anti-Pattern" not in content
    assert "User Review Gate" not in content
    assert "保存到 `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`" not in content
    assert "只调用 `writing-plans`" not in content
    assert "默认只读压缩入口和当前任务直接相关文件" not in content

    for phrase in (
        "先看当前阶段和 work item，再决定是否需要头脑风暴",
        "不靠提示词硬门控项目流转",
        "本 skill 默认**不直接展开读取项目背景文件清单**",
        "优先使用当前对话、`project-memory` 输出的会话卡",
        "缺上下文时先交给 `project-memory`",
        "不得为了“稳妥”读取",
        "流程路由由 `using-shanforge` 根据阶段、work item 状态和 ledger 判断",
        "本 skill 只回写 brief、批准状态、outputs、evidence、ledger_event 和 `needs`",
        ".factory/workitems/<WORKITEM-ID>/brief.md",
        ".factory/workitems/<WORKITEM-ID>/ledger.jsonl",
        "docs/04-project-development/02-discovery/brainstorm-record.md",
        "docs/04-project-development/04-design/assets/",
        "shanforge 正式产物统一使用本节列出的 work item",
        "作者自检不能把状态推进到 `approved` 或 `done`",
        "工作结果：",
        "skill: brainstorming",
        "ledger_event:",
        "`needs` 只是状态回写，不是 skill 路由决策",
        "`skills/brainstorming/visual-companion.md`",
    ):
        assert phrase in content

    for phrase in (
        "下一步 skill：",
        "给出下一步 skill",
        "handed_off",
        "唯一只能调用",
    ):
        assert phrase not in content


def test_brainstorming_openai_metadata_uses_work_item_routing() -> None:
    content = (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")

    assert 'display_name: "头脑风暴"' in content
    assert "基于当前阶段和 work item" in content
    assert "按 shanforge 路径保存" in content
    assert "状态回写包" in content
    assert "只回写 status、outputs、approval、evidence、ledger_event 和 needs" in content
    assert "流程路由由 using-shanforge 判断" in content
    assert "最后只调用 writing-plans" not in content
    assert "下一步 skill" not in content


def test_brainstorming_reviewer_prompt_matches_shanforge_paths() -> None:
    content = (SKILL_ROOT / "spec-document-reviewer-prompt.md").read_text(encoding="utf-8")

    assert "Spec Document Reviewer Prompt Template" not in content
    assert "You are a spec document reviewer" not in content

    for phrase in (
        "Brief / 设计输入评审提示模板",
        "确认头脑风暴产物完整、一致，可进入需求、设计或计划阶段",
        ".factory/workitems/<WORKITEM-ID>/brief.md",
        "流程一致性",
        "保存位置",
        "批准状态、产物路径、证据、ledger_event、needs",
        "避免替流程总控指定 skill",
        "**状态：**通过 | 发现问题",
    ):
        assert phrase in content

    assert "是否写清下一步 skill" not in content


def test_visual_companion_is_chinese_and_uses_work_item_storage() -> None:
    content = (SKILL_ROOT / "visual-companion.md").read_text(encoding="utf-8")

    assert "# 可视化伴侣指南" in content
    assert "--workitem-id WORKITEM-ID" in content
    assert ".factory/workitems/<WORKITEM-ID>/design-assets/brainstorm" in content
    assert "持久化文件统一保存到当前 work item 的 `design-assets/brainstorm/` 目录" in content
    assert (
        "被采纳的设计交付物需要同步登记到 `docs/04-project-development/04-design/assets/`"
        in content
    )
    assert "Visual Companion Guide" not in content
    assert "When to Use" not in content


def test_visual_companion_helper_uses_shanforge_storage_and_branding() -> None:
    start_server = (SKILL_ROOT / "scripts" / "start-server.sh").read_text(encoding="utf-8")
    stop_server = (SKILL_ROOT / "scripts" / "stop-server.sh").read_text(encoding="utf-8")
    server = (SKILL_ROOT / "scripts" / "server.cjs").read_text(encoding="utf-8")
    frame = (SKILL_ROOT / "scripts" / "frame-template.html").read_text(encoding="utf-8")

    assert "--workitem-id <id>" in start_server
    assert "--workitem-id is required with --project-dir" in start_server
    assert ".factory/workitems/${WORKITEM_ID}/design-assets/brainstorm" in start_server
    assert "Persistent shanforge work item directories" in stop_server
    assert "Shanforge 头脑风暴伴侣" in server
    assert "Shanforge 头脑风暴伴侣" in frame
    assert "primeradiant.com/brand/superpowers" not in server
