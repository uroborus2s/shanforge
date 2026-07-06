# FLOW-TASK-005 Review Checkpoint

- Work item：`FLOW-CONTRACT-001`
- Task：`FLOW-TASK-005`
- Author：Codex
- 时间：2026-07-06T20:19:16+08:00
- 状态：`ready_for_review`

## Review 输入

- Task brief：`.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-005.md`
- Implementation queue：`.factory/workitems/FLOW-CONTRACT-001/implementation-queue.md`
- Implementer report：`.factory/workitems/FLOW-CONTRACT-001/reports/FLOW-TASK-005-implementer-report.md`
- Evidence：`.factory/workitems/FLOW-CONTRACT-001/evidence/FLOW-TASK-005-verification.md`

## Diff 摘要

- `using-shanforge` 主 skill 增加四类场景路由、baseline work item 规则、缺 evidence 阻塞关闭和人工确认包审计问题报告要求。
- 黑盒流程 eval reference 增加 5 个 FLOW-CONTRACT 场景，覆盖新项目、增需、变需、修 bug 和缺 evidence 阻塞关闭。
- 结构测试覆盖新增流程契约，并同步既有 `SF-SP-009` 计划断言口径。

## Reviewer 检查点

- 是否满足 `FLOW-TASK-005`，且未越过 `FLOW-TASK-006`。
- `using-shanforge` 是否是四类场景、baseline work item、gate 和关闭规则的唯一流程 owner。
- 四类场景是否覆盖 `new_project`、`add_requirement`、`change_requirement`、`fix_bug`。
- baseline work item 和缺 evidence 阻塞关闭规则是否清楚。
- 人工确认输出是否包含最终审计问题报告，而不是只输出评分。
- `using-shanforge` 是否仍只做路由和 gate，不写需求、代码或评审结论。
- 验证命令结果是否支持 `ready_for_review`。

## 作者自检

- `FLOW-TASK-004` 已人工确认。
- 验证命令已新鲜运行并通过。
- 作者未写 `approved`。

## 需要

- 独立 review。
