# FLOW-TASK-008 升级执行类 skill

## 工作项

- 工作项：`FLOW-CONTRACT-001`
- 任务：`FLOW-TASK-008`
- 状态：`draft`
- 上游计划：`.factory/workitems/FLOW-CONTRACT-001/plan.md`
- 流水账：`.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`

## 目标

让 `executing-plans` 和 `subagent-driven-development` 按任务 gate 执行，缺设计、测试或 evidence 时阻塞。

## 输入

- `skills/executing-plans/SKILL.md`
- `skills/subagent-driven-development/SKILL.md`
- 流程契约实施方案。

## 允许修改

- `skills/executing-plans/SKILL.md`
- `skills/subagent-driven-development/SKILL.md`
- `tests/test_execution_workflow_skills.py`

## 验证命令

```bash
uv run pytest tests/test_execution_workflow_skills.py
```

期望输出：

```text
通过；新增缺 gate 阻塞和子 agent 不路由断言。
```

## 完成口径

执行类 skill 只能输出 `ready_for_review`、`blocked` 或 `needs_user_input`。
