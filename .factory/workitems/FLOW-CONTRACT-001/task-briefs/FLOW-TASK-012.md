# FLOW-TASK-012 增加黑盒流程 eval

## 工作项

- 工作项：`FLOW-CONTRACT-001`
- 任务：`FLOW-TASK-012`
- 状态：`draft`
- 上游计划：`.factory/workitems/FLOW-CONTRACT-001/plan.md`
- 流水账：`.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`

## 目标

验证 AI 不跳步、不省略、不自批，覆盖四类场景、baseline 任务、N/A、缺 evidence、缺 review 和直接提交诱导。

## 输入

- `skills/using-shanforge/references/black-box-flow-eval.md`
- `tests/test_black_box_workflow_eval.py`
- 流程契约需求和实施方案。

## 允许修改

- `skills/using-shanforge/references/black-box-flow-eval.md`
- `tests/test_black_box_workflow_eval.py`
- eval evidence 模板。

## 验证命令

```bash
uv run pytest tests/test_black_box_workflow_eval.py
```

期望输出：

```text
通过；critical assertion 任一失败则整体失败。
```

## 完成口径

eval 只验证 workflow 行为，不替代独立 review、人工确认、提交或 PR 闭环。
