# FLOW-TASK-011 升级 PM 视图

## 工作项

- 工作项：`FLOW-CONTRACT-001`
- 任务：`FLOW-TASK-011`
- 状态：`draft`
- 上游计划：`.factory/workitems/FLOW-CONTRACT-001/plan.md`
- 流水账：`.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`

## 目标

让 PM 看板按 Project、Baseline、Requirement、Task、Gate、Evidence 展示状态，并继续声明 HTML 不是事实源。

## 输入

- `skills/using-shanforge/references/pm-dashboard-rendering.md`
- `.factory/pm/`
- 流程契约实施方案。

## 允许修改

- `skills/using-shanforge/references/pm-dashboard-rendering.md`
- PM 生成逻辑或测试。
- `.factory/pm/generated/` 输出。

## 验证命令

```bash
uv run pytest tests/test_project_management_control_plane.py
```

期望输出：

```text
通过；新增 baseline work item 和缺 evidence blocked 展示断言。
```

## 完成口径

PM 视图只能展示从 docs、ledger 和 summary 汇总出的事实。
