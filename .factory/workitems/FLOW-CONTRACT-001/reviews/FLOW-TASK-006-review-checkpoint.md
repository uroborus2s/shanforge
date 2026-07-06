# FLOW-TASK-006 Review Checkpoint

- Work item：`FLOW-CONTRACT-001`
- Task：`FLOW-TASK-006`
- Author：Codex
- 时间：2026-07-06T20:37:18+08:00
- 状态：`ready_for_review`

## Review 输入

- Task brief：`.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-006.md`
- Implementation queue：`.factory/workitems/FLOW-CONTRACT-001/implementation-queue.md`
- Implementer report：`.factory/workitems/FLOW-CONTRACT-001/reports/FLOW-TASK-006-implementer-report.md`
- Evidence：`.factory/workitems/FLOW-CONTRACT-001/evidence/FLOW-TASK-006-verification.md`

## Diff 摘要

- `project-memory` 主 skill 增加事实源优先级。
- `project-memory` references 固定 summary 不复制正式正文，summary 冲突时以正式文档和 ledger 为准。
- `doc-map.md` 增加 docs、work item、memory summary、PM generated 的事实源边界。
- 结构测试覆盖任务卡要求。

## Reviewer 检查点

- 是否满足 `FLOW-TASK-006`，且未越过 `FLOW-TASK-007`。
- facts source priority 是否清楚：正式文档和 work item ledger 高于 memory summary。
- summary 是否明确不复制完整正文。
- `.factory/pm/generated/status-dashboard.html` 是否明确只是展示视图，不是唯一事实源。
- 验证命令结果是否支持 `ready_for_review`。

## 作者自检

- `FLOW-TASK-005` 已人工确认。
- 验证命令已新鲜运行并通过。
- 作者未写 `approved`。

## 需要

- 独立 review。
