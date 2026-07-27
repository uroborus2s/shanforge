---
name: subagent-driven-development
description: 有已批准的 Shanforge work item plan，且任务相对独立、适合用独立子 agent 或独立执行任务逐项或同层并行实现时使用；按 task brief、ledger、evidence、Spec Review 和 Quality Review 连续推进。
---

# 子代理驱动开发

本 skill 用于执行已批准计划。它只负责执行任务、生成 evidence、写 report 和回写状态。

## v1.2.0 运行时路由合同

- `SB-EXECUTE` 进入 `execution-workflow`，`write_policy: source_or_test_write`；子 agent 不重新选择工作流。
- 每个派发 route 必须有已存在且非空的 `work_item_id`、`task_card_id`，以及精确 `allowed_paths`、
  `forbidden_actions`、`current_gate`、`write_policy`；只允许该 TaskCard 的隔离写集。
- 子 agent 返回 `status`、`outputs`、`evidence`、`ledger_event`、`gate`、`next_required_action`；主控汇总
  并决定后续节点，子 agent 不自批 Review 或扩大范围。

## 触发

- 已有 `.factory/workitems/<WORKITEM-ID>/plan.md`。
- 计划中的任务相对独立。
- 计划包含独立任务，可以逐个实现、逐个 review。
- 用户要求继续执行计划、分任务执行、派发子 agent 或按 task brief 推进。
- 当前平台允许子 agent，或需要用独立 review task fallback 模拟隔离。

## 目标

- 为每个任务提供完整 task brief。
- 让实现者只拿必要上下文，不继承控制器的整段历史。
- 每个任务执行后生成 review 所需输入包。
- 对同一依赖层中满足并行条件的任务卡，逐张创建独立子任务并行执行，完成后由主控汇总。
- 只有 evidence、report 和状态回写齐全，才把任务推进到 `ready_for_review`。
- 在一次已授权输入包范围内连续执行，不在每个任务之间问“是否继续”。

## 输入

- 主计划：`.factory/workitems/<WORKITEM-ID>/plan.md`
- 子任务：`.factory/workitems/<WORKITEM-ID>/task-briefs/`
- 任务 ledger：`.factory/workitems/<WORKITEM-ID>/ledger.jsonl`
- 证据目录：`.factory/workitems/<WORKITEM-ID>/evidence/`
- 实现报告：`.factory/workitems/<WORKITEM-ID>/reports/`
- 评审输出：`.factory/workitems/<WORKITEM-ID>/reviews/`

## 任务 gate

- 执行前必须确认 task brief 已授权；不跳过 dependencies，不提前进入后续依赖层。
- 只有同一依赖层中 dependencies 已完成、无文件冲突、无未确认 Gate、共享契约已定的任务卡，才允许并行派发。
- 每张可并行任务卡创建一个独立子任务并行执行；不满足并行条件时按依赖顺序执行。
- 缺设计方案、接口设计、UI 或 N/A 原因、测试设计时，不得开始执行；状态回写 `blocked`，并说明缺口。
- 缺 verification evidence、evidence、implementer report、review checkpoint 或 ledger 事件时，不得把任务推进到 `ready_for_review`。
- 发现 task brief 允许文件范围不足、测试命令缺失、验收口径缺失或计划与代码事实冲突时，停止并回写 `blocked` 或 `needs_user_input`。
- 完成状态只能回写为：`ready_for_review`、`blocked` 或 `needs_user_input`。

## 子 agent 边界

- 子 agent 不决定下一步 skill；只执行分配给它的 task brief，不判断后续 skill，不进入下一任务决策。
- 子 agent 不读取完整 plan；控制器只提供当前任务必要上下文、允许文件范围、验证命令和回写要求。
- 子 agent 的输出只包含状态、outputs、evidence、ledger event、needs 和未决问题。

## 含义保留清单

- 每个任务使用新的隔离执行者。
- 控制器构造上下文，执行者不继承整段会话历史。
- 不要让子 agent 自己读完整 plan；控制器提供完整 task brief 和必要文件。
- 实现者状态只能是 `DONE`、`DONE_WITH_CONCERNS`、`NEEDS_CONTEXT`、`BLOCKED`。
- 实现者只能进入 `ready_for_review`，不得自批 `approved`。
- review 顺序由流程总控和评审 skill 决定；本 skill 只准备评审输入。
- reviewer 发现问题后，由流程总控决定是否重新进入本 skill 修复。
- 同一依赖层中满足条件的任务卡可以并行；每张任务卡一个独立子任务，完成后主控汇总。
- 存在文件冲突、未确认 Gate、未定共享契约或未完成 dependencies 时，不并行。
- 不能忽略实现者提问、担忧或 blocker。
- 不写“下一步应该调用哪个 skill”；只写 `needs` 状态。

## 默认流程

1. 宣告正在使用 `subagent-driven-development` 执行计划。
2. 读取 work item plan 和 ledger。
3. 跳过 ledger 中已经 `approved` 或 `done` 的任务。
4. 提取所有待执行 task brief。
5. 为每个任务确认 dependencies、影响文件、共享契约、Gate、测试命令、文档同步和 memory 同步。
6. 按依赖层分批；同层任务卡满足并行 gate 时并行派发，否则按依赖顺序执行。
7. 给实现者提供 [implementer-task-template.md](references/implementer-task-template.md)。
8. 如果实现者返回 `NEEDS_CONTEXT`，补充最小上下文后重新派发。
9. 如果实现者返回 `BLOCKED`，按 [status-handling-checklist.md](references/status-handling-checklist.md) 判断是补上下文、拆任务、换更强模型还是向用户升级。
10. 如果实现者返回 `DONE_WITH_CONCERNS`，先读 concerns；若涉及正确性或范围，先处理再 review。
11. 实现者完成后，生成 evidence 和 implementer report；并行批次完成后由主控汇总状态、产物、风险和未决问题。
12. 生成 review input package，必须包含 task brief、diff 摘要、evidence、implementer report、风险和未决问题。
13. 写入 `.factory/workitems/<WORKITEM-ID>/ledger.jsonl`，状态只能是 `ready_for_review`、`blocked` 或 `needs_user_input`。
14. 更新 `.factory/memory/tasks.summary.md`、`tests.summary.md` 和必要 summary。
15. 输出状态回写包，交还 `using-shanforge` 判断下一步。
16. 如果输入包已经明确授权一批待执行任务，且当前任务没有 `blocked` 或 `needs_user_input`，继续执行同一批次下一个任务；不要逐项请求继续。
17. 如果下一任务超出输入包范围、触碰新文件范围、需要新决策，或当前任务状态不是 `ready_for_review`，停止并交还 `using-shanforge` 重新路由。

## 流程边界

- 本 skill 不判断前置环节是否完成；输入包必须由 `using-shanforge` 或当前会话提供。
- 本 skill 不决定完成后交给谁；只写状态、产物、证据和 `needs`。
- 本 skill 不执行独立 review；只准备评审输入。
- 本 skill 不执行完成声明；只说明是否有足够 evidence。
- 本 skill 不执行提交；只说明是否产生了可提交改动。
- 如发现需要计划重写、额外验证、人工确认或提交，只在状态包写入 `needs`，不直接调用其他 skill。
- `using-shanforge` 负责选择是否进入本 skill；本 skill 只消费已给出的输入包，不反向决定流程路由。

## 停止条件

只在这些情况下停止：

- 计划缺关键事实，无法开始。
- 实现者连续返回同一 `BLOCKED`，且控制器无法补充上下文。
- review 发现计划本身错误。
- 测试失败且需要重新设计。
- 用户要求暂停。

不要因为“一个任务完成了”就停下来问是否继续。

## blocked 语义

`blocked` 只用于执行者无法靠补充最小上下文继续推进的情况，例如 task brief 缺关键事实、允许文件范围冲突、测试命令不可运行、实现者连续返回同一 blocker，或计划本身与代码事实冲突。

能通过补一个文件、一个命令输出或一个明确约束继续时，先补上下文再重试；不要把普通疑问直接升级为 `blocked`。

## 禁止

- 禁止跳过 Spec Review 或 Quality Review。
- 禁止 Quality Review 早于 Spec Review。
- 禁止把准备好的 review input package 写成 review 已通过。
- 禁止接受“差不多符合 spec”作为 `ready_for_review` 之外的状态。
- 禁止让实现者自评替代独立 review。
- 禁止把未验证的 report 写成完成事实。
- 禁止在 main/master 上开始代码实现，除非用户明确允许当前分支直接开发。
- 禁止自动 commit；本 skill 只记录是否需要提交。

## 输出

每个任务至少产生：

- `.factory/workitems/<WORKITEM-ID>/evidence/task-N.md`
- `.factory/workitems/<WORKITEM-ID>/reports/task-N.md`
- `.factory/workitems/<WORKITEM-ID>/reviews/task-N-review-input.md`
- `.factory/workitems/<WORKITEM-ID>/ledger.jsonl`

状态包格式：

```text
工作结果：
- work_item: <ID>
- skill: subagent-driven-development
- status: ready_for_review | blocked | needs_user_input
- outputs:
  - <path>
- evidence:
  - <path>
- ledger_event: <event id>
- needs:
  - review | verification | human_confirmation | commit | plan_rewrite | none
```

## 完成状态

本 skill 的单任务完成条件是：实现报告存在，验证证据存在，review input package 存在，ledger 和 memory 已同步，状态已回写为 `ready_for_review`。`approved` 和 `done` 由流程总控、独立评审、验证和人工确认共同决定。
