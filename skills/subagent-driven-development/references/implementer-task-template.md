# Implementer Task

用于派发单个实现任务。控制器负责填充，不要求实现者自己读取完整 plan。

## Dispatch

```markdown
你正在实现 Task N：<task name>

## 完整 task brief

<粘贴 .factory/workitems/<WORKITEM-ID>/task-briefs/task-N.md 的完整内容>

## Work item

- Work item：<WORKITEM-ID>
- Plan：.factory/workitems/<WORKITEM-ID>/plan.md
- Ledger：.factory/workitems/<WORKITEM-ID>/ledger.jsonl
- Worktree / directory：<cwd>

## Context

- 这个任务在整体计划中的位置：
- 必要架构边界：
- 允许读取：
- 禁止读取：
- 允许修改：
- 禁止修改：

## Before You Begin

如果需求、验收标准、依赖、路径或实现策略不清楚，先提问。
不要猜。

## Your Job

1. 按完整 task brief 实现。
2. 按 TDD 写 Red，再写 Green。
3. 运行指定验证命令。
4. 写 evidence 到 `.factory/workitems/<WORKITEM-ID>/evidence/task-N.md`。
5. 写 implementer report 到 `.factory/workitems/<WORKITEM-ID>/reports/task-N.md`。
6. 自检，但不要批准自己的任务。

## Report Format

- Status：DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
- Implemented：
- Tests：
- Files changed：
- evidence：
- implementer report：
- Self-review：
- Concerns：
```

## 状态含义

- `DONE`：实现、验证和报告已完成，可进入 review。
- `DONE_WITH_CONCERNS`：完成了，但对正确性、范围、可维护性或测试有疑问。
- `NEEDS_CONTEXT`：缺少信息，不能安全实现。
- `BLOCKED`：当前任务无法完成，需要控制器改变上下文、拆任务、改计划或升级给用户。

实现者不能写 `approved`。实现者最多进入 `ready_for_review`。
