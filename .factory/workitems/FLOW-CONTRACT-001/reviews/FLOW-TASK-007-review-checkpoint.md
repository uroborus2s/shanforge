# FLOW-TASK-007 Review Checkpoint

- Work item：`FLOW-CONTRACT-001`
- Task：`FLOW-TASK-007`
- Author：Codex
- 时间：2026-07-06T20:49:25+08:00
- 状态：`ready_for_review`

## Review 输入

- Task brief：`.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-007.md`
- Implementation queue：`.factory/workitems/FLOW-CONTRACT-001/implementation-queue.md`
- Implementer report：`.factory/workitems/FLOW-CONTRACT-001/reports/FLOW-TASK-007-implementer-report.md`
- Evidence：`.factory/workitems/FLOW-CONTRACT-001/evidence/FLOW-TASK-007-verification.md`

## Diff 摘要

- `writing-plans` 主 skill 明确只生成候选执行输入，不执行代码。
- work item plan 模板和 task brief 模板增加设计方案、接口设计、UI 或 `N/A`、测试设计、开发、单测、review、集成测试。
- 模板增加缺测试设计、UI N/A 缺原因和占位语失败断言。
- 结构测试覆盖上述规则。

## Reviewer 检查点

- 是否满足 `FLOW-TASK-007`，且未越过 `FLOW-TASK-008`。
- 任务模板是否强制包含设计方案、接口设计、UI 或 `N/A`、测试设计、开发、单测、review 和集成测试。
- UI 写 `N/A` 是否必须写原因。
- 是否包含缺测试设计、UI N/A 缺原因和占位语失败断言。
- `writing-plans` 是否仍只生成候选执行输入，不执行代码。
- 验证命令结果是否支持 `ready_for_review`。

## 作者自检

- `FLOW-TASK-006` 已人工确认。
- 验证命令已新鲜运行并通过。
- 作者未写 `approved`。

## 需要

- 独立 review。
