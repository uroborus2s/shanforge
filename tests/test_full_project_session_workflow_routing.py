from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_task_execution_contract_defines_full_project_session_routing() -> None:
    contract = read("docs/05-design/workflow-execution-design.md")

    for phrase in (
        "完整软件项目会话归因模型",
        "当前消息 -> 会话行为 -> 工作流 -> 节点 -> 允许动作 -> 状态包",
        "所有完整软件项目会话必须先归因，再执行",
        "未归因前不得写文件、创建孤立方案、执行任务、提交或关闭 work item",
        "影响源代码、skill、测试、正式文档或流程状态的会话必须绑定 WorkItem / TaskCard",
    ):
        assert phrase in contract


def test_task_execution_contract_lists_session_behaviors_and_workflows() -> None:
    contract = read("docs/05-design/workflow-execution-design.md")

    for behavior in (
        "解释问答",
        "需求澄清",
        "需求新增",
        "需求变更",
        "方案设计",
        "计划分解",
        "执行开发",
        "Bug 调查",
        "Review 处理",
        "验证收口",
        "提交发布",
        "状态恢复",
        "暂停废弃",
    ):
        assert behavior in contract

    for workflow in (
        "direct-answer-workflow",
        "requirements-workflow",
        "change-control-workflow",
        "design-workflow",
        "planning-workflow",
        "execution-workflow",
        "debugging-workflow",
        "review-workflow",
        "verification-workflow",
        "commit-workflow",
        "status-memory-workflow",
    ):
        assert workflow in contract


def test_task_execution_contract_blocks_silent_modification() -> None:
    contract = read("docs/05-design/workflow-execution-design.md")

    for phrase in (
        "静默修改",
        "非静默修改",
        "路由包",
        "处理模式",
        "所属 WorkItem / TaskCard",
        "允许修改范围",
        "当前 gate",
        "讨论结论如果影响项目事实",
        "需求、设计、计划、任务或 ledger",
    ):
        assert phrase in contract


def test_flow_task_015_is_registered_as_pending_formal_scheme_work() -> None:
    task = read(".factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-015.md")
    queue = read(".factory/workitems/FLOW-CONTRACT-001/implementation-queue.md")
    ledger = read(".factory/workitems/FLOW-CONTRACT-001/ledger.jsonl")

    assert "完整软件项目会话行为与工作流归因契约" in task
    assert "状态：`draft`" in task
    assert "`FLOW-TASK-015`" in queue
    assert '"task":"FLOW-TASK-015"' in ledger
