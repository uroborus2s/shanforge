# FLOW-TASK-014 增加启动记忆和非活跃任务降级规则

## 工作项

- 工作项：`FLOW-CONTRACT-001`
- 任务：`FLOW-TASK-014`
- 状态：`draft`
- 上游计划：`.factory/workitems/FLOW-CONTRACT-001/plan.md`
- 流水账：`.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`

## 目标

让 `project-memory` 固定条件读取链，并把非活跃任务从 `current-state.md` 降级到 summary 或 history。

## 输入

- `skills/project-memory/SKILL.md`
- `skills/project-memory/references/session-start-checklist.md`
- `skills/project-memory/references/current-state-update-checklist.md`
- `.factory/memory/current-state.md`
- `.factory/memory/tasks.summary.md`

## 允许修改

- `skills/project-memory/SKILL.md`
- `skills/project-memory/references/session-start-checklist.md`
- `skills/project-memory/references/current-state-update-checklist.md`
- `.factory/memory/current-state.md`
- `.factory/memory/tasks.summary.md`
- 相关测试。

## 禁止修改

- work item ledger、evidence、review 和 report 的历史事实。
- 与会话恢复无关的 skill。

## 验证命令

```bash
uv run pytest tests/test_project_memory_skill.py
```

期望输出：

```text
通过；新增启动不能只读 current-state、不能固定读取三件套、已关闭任务不占 active tasks、ledger 不删除断言。
```

## 完成口径

`current-state.md` 只保留活跃任务、阻塞项、最近事实和下一动作；历史事实保留在 ledger、summary 或 history。
