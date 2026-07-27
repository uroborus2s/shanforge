# FLOW-CONTRACT-001 收口审查反馈分诊

## FLOW-CLOSEOUT-I1

- 来源：独立任务审查
- 严重度：Important
- 反馈：`PM-DASHBOARD-002`、`PROJECT-ARTIFACTS-001`、`UI-DESIGN-SKILL-001`
  已有真实本地提交，不应计入仍需实施的 WorkItem。
- 核实：正确。Git 中分别存在提交 `b63990c`、`f3c6c70`、`d609757`。
- 决定：Fixed。
- 修复：盘点从 `11 + 9` 更正为 `8 + 12`，并同步报告、evidence、ledger
  与当前状态投影。

## FLOW-CLOSEOUT-I2

- 来源：同一独立任务 Reviewer
- 严重度：Important
- 反馈：移除 mixed T14 测试中的零活动分支会使当前工作树规定组合退化为
  `1 failed, 56 passed`。
- 核实：正确。失败断言仍要求存在活动 `FLOW-TASK`，与合法的 `CLOSED / 0 active`
  投影冲突。
- 决定：Fixed。
- 修复：恢复 mixed T14 文件的零活动分支，但不把该文件纳入收口提交；收口提交由
  `test_full_project_session_workflow_routing.py` 的 4 条断言独立覆盖零活动状态。
- 验证：规定组合 `57 passed in 0.15s`；Ruff `All checks passed!`。
