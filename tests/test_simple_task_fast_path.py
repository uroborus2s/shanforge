from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_controller_classifies_before_project_memory_recovery() -> None:
    controller = read("skills/using-shanforge/SKILL.md")

    classify = "先根据当前消息判定处理模式"
    recover = "再使用 `project-memory` 恢复项目上下文"

    assert classify in controller
    assert recover in controller
    assert controller.index(classify) < controller.index(recover)
    assert "先使用 `project-memory` 恢复最小上下文" not in controller


def test_direct_and_lightweight_fast_path_excludes_project_state() -> None:
    controller = read("skills/using-shanforge/SKILL.md")

    for phrase in (
        "简单任务快速通道",
        "只使用当前消息、当前对话和完成答案所需的直接文件",
        "不得读取 `.factory/memory/agent-session.md`",
        "不得读取 work item ledger",
        "不创建 WorkItem、TaskCard、ledger、evidence、review 或 memory",
        "不输出项目位置快照",
        "不返回工作 skill 状态包",
    ):
        assert phrase in controller


def test_fast_path_has_explicit_upgrade_signals() -> None:
    controller = read("skills/using-shanforge/SKILL.md")

    for phrase in (
        "继续或恢复既有任务",
        "查询当前项目状态",
        "包含 WorkItem / TaskCard ID",
        "修改项目事实",
        "创建、更新或保存任何仓内文件",
        "要求追踪、验收、review、提交或发布",
        "升级为项目化流程",
    ):
        assert phrase in controller


def test_fast_path_never_persists_repository_files() -> None:
    controller = read("skills/using-shanforge/SKILL.md")
    memory = read("skills/project-memory/SKILL.md")

    assert "快速通道不得写任何仓内文件" in controller
    assert "只返回当前会话答案或结构化分析" in controller
    assert "用户明确要求保存指定结果时，只写用户指定的交付物" not in controller
    assert "除非用户要求保存，否则不落盘" not in controller

    assert "不得写任何仓内文件、memory、ledger 或 summary" in memory
    assert "除非用户明确要求保存" not in memory


def test_agents_entry_matches_fast_path_order() -> None:
    agents = read("AGENTS.md")

    assert "先根据当前消息判定处理模式" in agents
    assert "无项目影响的直接回答和轻量分析不读取 `.factory/memory/`" in agents
    assert "项目状态查询、任务延续、项目事实修改或仓内持久化" in agents
    assert "默认只读 `.factory/memory/agent-session.md`" not in agents


def test_project_memory_rejects_fast_path_invocation() -> None:
    memory = read("skills/project-memory/SKILL.md")

    for phrase in (
        "不用于无项目影响的 `direct_answer` 或 `lightweight_analysis`",
        "只有项目状态查询、任务延续、上下文恢复或项目化流程",
        "不得先读 memory 再判断请求是否简单",
    ):
        assert phrase in memory


def test_formal_session_contract_classifies_before_conditional_restore() -> None:
    for path in (
        "docs/05-design/workflow-execution-design.md",
        "docs/05-design/api-design.md",
        "docs/05-design/system-architecture.md",
    ):
        design = read(path)
        assert "classifying → restoring_if_projectized → routing → scoping" in design
        assert "restoring → classifying → routing" not in design
        assert "classifying → routing → restoring_if_projectized" not in design

    prd = read("docs/04-product/prd.md")
    classify = "classify_processing_mode_from_current_message"
    restore = "restore_current_facts [projectized]"
    assert classify in prd
    assert restore in prd
    assert "direct_handoff_without_project_restore" in prd
    assert prd.index(classify) < prd.index(restore)
    for stale in (
        "AI 先恢复当前事实和 Gate，再展示路由包",
        "接收 → 恢复 → 分类 → 路由",
        "会话开始先恢复最小事实",
    ):
        assert stale not in prd
