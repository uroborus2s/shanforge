# FLOW-CONTRACT-001 顺序实施队列

## 状态

- 当前阶段：`FLOW-TASK-015_completed_local_commit_created`
- 本会话是否实施：否；15/15 项已完成并关闭
- 例外记录：`FLOW-TASK-015` 曾按用户变更指令提前形成方案候选；当前前置任务已全部关闭，恢复顺序执行
- 执行方式：按任务号顺序逐项实施
- 并发规则：禁止并发实施；同一时间只允许一个 active task
- 下一任务：无

## 执行规则

- `FLOW-TASK-001` 和 `FLOW-TASK-002` 已作为实施前评审输入通过独立评审和人工确认，不在本队列重复实施。
- 从 `FLOW-TASK-003` 开始，每个任务必须先读取自己的 task brief。
- 每个任务完成后必须产出 evidence、implementer report 和 review checkpoint。
- 实现者只能把任务写到 `ready_for_review`，不得自批 `approved`。
- 独立 review 和人工确认通过后，才能进入下一任务。
- 本队列只记录顺序和状态，事实源仍是 task brief、ledger、evidence、report 和 review 文件。

## 队列

| 顺序 | 任务 | 名称 | 状态 | 前置 | 任务卡 |
|---:|---|---|---|---|---|
| 1 | `FLOW-TASK-001` | 固化流程契约需求 | `pre_review_approved` | 无 | `.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-001.md` |
| 2 | `FLOW-TASK-002` | 固化流程契约实施方案 | `pre_review_approved` | `FLOW-TASK-001` | `.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-002.md` |
| 3 | `FLOW-TASK-003` | 升级文档治理规则 | `human_approved` | `FLOW-TASK-002` | `.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-003.md` |
| 4 | `FLOW-TASK-004` | 升级需求工程流程 | `human_approved` | `FLOW-TASK-003` | `.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-004.md` |
| 5 | `FLOW-TASK-005` | 升级流程总控 | `human_approved` | `FLOW-TASK-004` | `.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-005.md` |
| 6 | `FLOW-TASK-006` | 升级项目记忆 | `human_approved` | `FLOW-TASK-005` | `.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-006.md` |
| 7 | `FLOW-TASK-007` | 升级计划编写 | `human_approved` | `FLOW-TASK-006` | `.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-007.md` |
| 8 | `FLOW-TASK-008` | 升级执行类 skill | `human_approved` | `FLOW-TASK-007` | `.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-008.md` |
| 9 | `FLOW-TASK-009` | 升级 review 和 verification | `human_approved` | `FLOW-TASK-008` | `.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-009.md` |
| 10 | `FLOW-TASK-010` | 增加 baseline 设计模板 | `human_approved` | `FLOW-TASK-009` | `.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-010.md` |
| 11 | `FLOW-TASK-011` | 升级 PM 视图 | `completed_independently_approved` | `FLOW-TASK-010` | `.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-011.md` |
| 12 | `FLOW-TASK-012` | 增加黑盒流程 eval | `completed_independently_approved` | `FLOW-TASK-011` | `.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-012.md` |
| 13 | `FLOW-TASK-013` | 增加项目级测试治理 | `completed_independently_approved` | `FLOW-TASK-012` | `.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-013.md` |
| 14 | `FLOW-TASK-014` | 增加启动记忆和非活跃任务降级规则 | `completed_independently_approved` | `FLOW-TASK-013` | `.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-014.md` |
| 15 | `FLOW-TASK-015` | 重塑完整软件项目会话行为与工作流归因契约 | `completed_local_commit_created` | `FLOW-TASK-014` | `.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-015.md` |
