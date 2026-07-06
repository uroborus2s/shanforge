# FLOW-TASK-005 升级流程总控

## 工作项

- 工作项：`FLOW-CONTRACT-001`
- 任务：`FLOW-TASK-005`
- 状态：`draft`
- 上游计划：`.factory/workitems/FLOW-CONTRACT-001/plan.md`
- 流水账：`.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`

## 目标

让 `using-shanforge` 成为四类场景、baseline work item、gate 和关闭规则的唯一路由 owner。

## 输入

- `skills/using-shanforge/SKILL.md`
- `skills/using-shanforge/references/black-box-flow-eval.md`
- 流程契约实施方案。

## 允许修改

- `skills/using-shanforge/SKILL.md`
- `skills/using-shanforge/references/*.md`
- `tests/test_black_box_workflow_eval.py`

## 验证命令

```bash
uv run pytest tests/test_black_box_workflow_eval.py
```

期望输出：

```text
通过；覆盖新项目、增需、变需、修 bug 和缺 evidence 阻塞。
```

## 完成口径

`using-shanforge` 仍只路由，不写需求、代码或评审结论。
