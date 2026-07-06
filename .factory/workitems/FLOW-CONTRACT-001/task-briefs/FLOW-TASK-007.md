# FLOW-TASK-007 升级计划编写

## 工作项

- 工作项：`FLOW-CONTRACT-001`
- 任务：`FLOW-TASK-007`
- 状态：`draft`
- 上游计划：`.factory/workitems/FLOW-CONTRACT-001/plan.md`
- 流水账：`.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`

## 目标

让 `writing-plans` 的任务模板强制包含设计方案、接口设计、UI 或 N/A、测试设计、开发、单测、review 和集成测试。

## 输入

- `skills/writing-plans/SKILL.md`
- `skills/writing-plans/references/workitem-plan-template.md`
- `skills/writing-plans/references/task-brief-template.md`

## 允许修改

- `skills/writing-plans/SKILL.md`
- `skills/writing-plans/references/*.md`
- `tests/test_writing_plans_skill.py`

## 验证命令

```bash
uv run pytest tests/test_writing_plans_skill.py
```

期望输出：

```text
通过；新增缺测试设计、UI N/A 缺原因和占位语失败断言。
```

## 完成口径

计划只能生成候选执行输入，不执行代码。
