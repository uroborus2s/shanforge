---
name: subagent-driven-development
description: 有已批准的 Shanforge work item plan，且任务相对独立、适合用独立子 agent 或同层并行实现时使用；按 task brief 连续开发，并在批次或里程碑末集中验证和评审。
---

# 子代理驱动开发

本 skill 只负责已批准计划的 `worker` 隔离实现、必要定向检查和批次状态回写；独立只读 review 是按 Codex
工具合同派发的 `reviewer` 分支，不进入本 skill。

## v1.2.0 运行时路由合同

- `SB-EXECUTE` 进入 `execution-workflow`，`write_policy: source_or_test_write`；子 agent 不重新选择工作流。
- 每个派发 route 必须有已存在且非空的 `work_item_id`、`task_card_id`，以及精确 `allowed_paths`、
  `forbidden_actions`、`current_gate`、`write_policy`；只允许该 TaskCard 的隔离写集。
- 子 agent 返回 `status`、`outputs`、`evidence`、`ledger_event`、`gate` 和本地 `needs`；主控汇总
  执行事实，项目级后续动作由 `using-shanforge` 决定，子 agent 不自批 Review 或扩大范围。

## 触发

- 已有 `.factory/workitems/<WORKITEM-ID>/plan.md`。
- 计划中的任务相对独立。
- 计划包含独立任务，可以逐个实现、逐个 review。
- 用户要求继续执行计划、分任务执行、派发子 agent 或按 task brief 推进。
- 当前平台允许子 agent，或需要用独立 review task fallback 模拟隔离。

## 目标

- 为每个任务提供完整 task brief。
- 让实现者只拿必要上下文，不继承控制器的整段历史。
- 低、中风险任务执行后直接汇总最小结果并继续批次。
- 对同一依赖层中满足并行条件的任务卡，逐张创建独立子任务并行执行，完成后由主控汇总。
- 只有批次最终 evidence、实现摘要和状态回写齐全，才把批次推进到 `ready_for_review`。
- 在一次已授权输入包范围内连续执行，不在每个任务之间问“是否继续”。

## 输入

- 主计划：`.factory/workitems/<WORKITEM-ID>/plan.md`
- 子任务：`.factory/workitems/<WORKITEM-ID>/task-briefs/`
- 任务 ledger：`.factory/workitems/<WORKITEM-ID>/ledger.jsonl`
- 证据目录：`.factory/workitems/<WORKITEM-ID>/evidence/`
- 实现报告：`.factory/workitems/<WORKITEM-ID>/reports/`
- 评审输出：`.factory/workitems/<WORKITEM-ID>/reviews/`

## 授权执行包

主控必须先把用户批准范围固化为授权执行包：目标、任务集合、依赖层、允许文件、共享契约、允许动作、禁止动作、验证命令、同范围整改边界和真实人工 Gate。

worker Terra/Luna 只消费已授权路由包；`execution_authorized` 不为 `true` 时不得派发。执行者不得重算或改写
`control_model`、`task_complexity`、`risk_level`、`execution_model`、`dispatch_required`、`dispatch_mode`、
`dispatch_role`、`requested_reasoning_effort`、`fork_turns`、`route_reason` 和 `escalation_triggers`。
命中 `scope_expanded`、`input_conflict`、`risk_increased`、`verification_failed_twice` 或 `human_gate` 时，
立即停止当前执行并把事实交还 Sol；不得自行换模型或扩大授权。

`execution_authorized != true -> do_not_dispatch`

worker 派发条件、非授权关闭条件和 reviewer 分支均以 `using-shanforge` 的“子代理严格派发判定”为唯一规范定义；本 skill 只引用该判定。授权 worker 实现只能调用已暴露的 `spawn_agent`：`model` 必须等于
`execution_model`，Luna 使用 `low`、Terra 使用 `medium`，且 `fork_turns="none"`；`message` 必须包含完整 task brief、精确写集、禁令和验证命令。
父 Sol 必须在调用前生成稳定 `dispatch_id` 并保存工具成功返回的 `task_card_id`、`requested_model`、`requested_reasoning_effort`、`fork_turns`、
`agent_id` 或 canonical task、`status: accepted`、`source: parent_tool_receipt`；`accepted` 不是子代理完成态。任一工具/模型/回执/模型一致性检查失败，置
`dispatch_failed` 或 `worker_unavailable` 并交还 Sol，不得静默代写或换模型。

### 升级信号决策表

| signal | action |
|---|---|
| `scope_expanded` | `stop_and_return_to_sol` |
| `input_conflict` | `stop_and_return_to_sol` |
| `risk_increased` | `stop_and_return_to_sol` |
| `verification_failed_twice` | `stop_and_return_to_sol` |
| `human_gate` | `stop_and_return_to_sol` |

- 批次内任务按依赖层连续推进；不要逐项请求继续。
- 普通 task checkpoint 不是人工 Gate，也不是质量 Gate。子任务返回最小结果后继续，不生成逐任务 evidence、report 或 review input。
- 授权范围不得扩大。子 agent 和主控都不能从“继续执行”推导新文件、新系统或新外部动作权限。
- 只有需要人类产品决策、超出允许文件范围、需要风险接受，或将执行未授权的破坏性或外部动作时，才停止并升级。

## 任务 gate

- 执行前必须确认 task brief 已授权；不跳过 dependencies，不提前进入后续依赖层。
- 只有同一依赖层中 dependencies 已完成、无文件冲突、无未确认 Gate、共享契约已定的任务卡，才允许并行派发。
- 每张可并行任务卡创建一个独立子任务并行执行；不满足并行条件时按依赖顺序执行。
- 缺目标、验收标准、依赖、允许文件或必要验证命令时不得开始执行；不强制无关设计章节或 `N/A` 占位。
- 单个低、中风险任务不要求 verification evidence、implementer report 或 review checkpoint。
- 批次 / 里程碑缺最终验证证据、实现摘要、review input 或 ledger event 时，不得推进到 `ready_for_review`。
- 发现 task brief 允许文件范围不足、测试命令缺失、验收口径缺失或计划与代码事实冲突时，停止并回写 `blocked` 或 `needs_user_input`。
- 完成状态只能回写为：`ready_for_review`、`blocked` 或 `needs_user_input`（此处完成状态仅指批次控制器状态）。

### worker 回执到控制器处理

worker 回执是 TaskCard 层事实，不是批次控制器状态；控制器逐值按下表处理，不把任一值直接改写成
`ready_for_review`：

| worker 回执 | 唯一控制器处理 |
|---|---|
| `DONE` | 当前 TaskCard 实现结束；继续当前批次，不写批次状态 |
| `DONE_WITH_CONCERNS` | 先处理 concerns；非阻塞时继续当前批次，不写批次状态 |
| `NEEDS_CONTEXT` | 补最小上下文并重派；无法补足时写 `needs_user_input` |
| `BLOCKED` | 写 `blocked` 并交还 Sol |

`DONE` 只表示该 TaskCard 的实现工作结束，不代表批次、产品或项目完成；不得从单个 worker `DONE` 推导 `ready_for_review`。
只有集中 evidence、实现摘要、review input 和 ledger event 齐全的批次候选才可写 `ready_for_review`。

## 子 agent 边界

- 子 agent 不决定下一步 skill；只执行分配给它的 task brief，不判断后续 skill，不进入下一任务决策。
- 子 agent 不读取完整 plan；控制器只提供当前任务必要上下文、允许文件范围、验证命令和回写要求。
- 子 agent 的输出只包含状态、outputs、evidence、ledger event、needs 和未决问题。

## 含义保留清单

- 每个相互独立且值得隔离的任务使用独立执行者；简单同层任务可以由同一执行者连续完成。
- 控制器构造上下文，执行者不继承整段会话历史。
- 不要让子 agent 自己读完整 plan；控制器提供完整 task brief 和必要文件。
- 实现者状态只能是 `DONE`、`DONE_WITH_CONCERNS`、`NEEDS_CONTEXT`、`BLOCKED`。
- 实现者不得自批 `approved`；只有批次或高风险专项候选进入 `ready_for_review`。
- review 顺序由流程总控和评审 skill 决定；本 skill 只准备集中评审输入。
- reviewer 发现问题后，由流程总控决定是否重新进入本 skill 修复。
- 同一依赖层中满足条件的任务卡可以并行；每张任务卡一个独立子任务，完成后主控汇总。
- 存在文件冲突、未确认 Gate、未定共享契约或未完成 dependencies 时，不并行。
- 不能忽略实现者提问、担忧或 blocker。
- 不写“下一步应该调用哪个 skill”；只写 `needs` 状态。

## 默认流程

1. 宣告正在使用 `subagent-driven-development` 执行计划。
2. 读取 work item plan 和 ledger。
3. 只跳过 TaskCard 生命周期为 `completed` 或 `closed` 的任务；`review_status=approved` 不作为跳过依据，包括 TaskCard 仍为 `active` 或 `ready_for_review`。
4. 提取所有待执行 task brief。
5. 为每个任务确认 dependencies、影响文件、共享契约、Gate、测试命令、文档同步和 memory 同步。
6. 按依赖层分批；同层任务卡满足并行 gate 时并行派发，否则按依赖顺序执行。
7. 给实现者提供 [implementer-task-template.md](references/implementer-task-template.md)。
8. 如果实现者返回 `NEEDS_CONTEXT`，补充最小上下文后重新派发。
9. 如果实现者返回 `BLOCKED`，按 [status-handling-checklist.md](references/status-handling-checklist.md) 判断是补上下文、拆任务或向 Sol 升级；不得自行换模型。
10. 如果实现者返回 `DONE_WITH_CONCERNS`，先读 concerns；若涉及正确性或范围，先处理再 review。
11. 实现者只返回实现内容、测试结果、文件和 concerns；低、中风险任务不落盘独立过程材料。
12. 并行批次或里程碑完成后，由主控生成一套实现摘要、最终 evidence 和 review input package。
13. 仅在批次质量候选完成时写 `ready_for_review`；其他终态是 `blocked` 或 `needs_user_input`。
14. 只在批次状态变化或跨会话恢复需要时更新 `.factory/memory/`。
15. 输出状态回写包，交还 `using-shanforge` 判断下一步。
16. 如果输入包已经明确授权一批待执行任务，且当前任务没有 `blocked` 或 `needs_user_input`，继续执行同一批次下一个任务；不要逐项请求继续。
17. 如果下一任务超出输入包范围、触碰新文件范围、需要新决策，或当前批次候选为 `blocked` 或 `needs_user_input`，停止并交还 `using-shanforge` 重新路由。

## 流程边界

- 本 skill 不判断前置环节是否完成；输入包必须由 `using-shanforge` 或当前会话提供。
- 本 skill 不决定完成后交给谁；只写状态、产物、证据和 `needs`。
- 本 skill 不执行独立 review；只准备集中评审输入。
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

- 禁止跳过批次最终代码审查和适用的 API、服务、集成测试。
- 高风险专项 review 必须在对应风险扩散前完成。
- 禁止把准备好的 review input package 写成 review 已通过。
- 禁止接受“差不多符合 spec”作为 `ready_for_review` 之外的状态。
- 禁止让实现者自评替代独立 review。
- 禁止把未验证的 report 写成完成事实。
- 禁止在 main/master 上开始代码实现，除非用户明确允许当前分支直接开发。
- 禁止自动 commit；本 skill 只记录是否需要提交。

## 输出

普通低、中风险 TaskCard 使用可回读的新鲜命令回执，不强制单独落盘；批次、里程碑、高风险专项，以及任何阶段、项目或关闭声明必须落盘 evidence。
每个低、中风险任务只返回内存中的最小状态；批次或里程碑只产生一套：

- `.factory/workitems/<WORKITEM-ID>/evidence/<batch>.md`
- `.factory/workitems/<WORKITEM-ID>/reports/<batch>.md`
- `.factory/workitems/<WORKITEM-ID>/reviews/<batch>-review-input.md`
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

本 skill 的批次完成条件是：全部授权任务已有真实实现和必要定向检查，一套实现摘要、验证证据、
review input 和 ledger event 已生成，状态回写为 `ready_for_review`。质量结论由流程总控根据集中评审和
最终验证判断；只有 `human_confirmation_required: true` 且有完整 `gate_reason` 时人工确认才参与收口，
普通授权任务不得额外制造人工 Gate，也不得制造逐任务评审。
