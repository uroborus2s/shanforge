---
name: executing-plans
description: 有 written implementation plan 但不使用子 agent，或需要在当前会话 inline 执行 Shanforge work item plan 时使用；先自检计划，再连续开发，并在批次或里程碑末集中验证和评审。
---

# 执行实施计划

本 skill 是 inline 执行者。它在当前会话中执行已批准计划。

## v1.2.0 运行时路由合同

- `SB-EXECUTE` 进入 `execution-workflow`，`write_policy: source_or_test_write`。
- 写入前，route 必须有已存在且非空的 `work_item_id`、`task_card_id`，以及精确 `allowed_paths`、
  `forbidden_actions`、`current_gate`、`write_policy`；只改 allowlist 内源码、Skill、测试和任务证据。
- 返回 `status`、`outputs`、`evidence`、`ledger_event`、`gate` 和本地 `needs`；实现最多推进到
  `ready_for_review`，不得把 Green 写成 Review、Verification、项目状态或人工批准。

## 触发

- 已有 `.factory/workitems/<WORKITEM-ID>/plan.md`。
- 用户要求在当前会话继续执行计划。
- 当前平台不能或不应使用子 agent。
- 任务强耦合，不适合隔离派发。

## 输入

- 主计划：`.factory/workitems/<WORKITEM-ID>/plan.md`
- 任务 ledger：`.factory/workitems/<WORKITEM-ID>/ledger.jsonl`
- 子任务 brief：`.factory/workitems/<WORKITEM-ID>/task-briefs/`
- 批次收口产物：`.factory/workitems/<WORKITEM-ID>/{evidence,reports,reviews}/`

## 授权执行包

开始前把用户已批准输入固化为授权执行包：目标、任务集合、允许文件、允许动作、禁止动作、验证命令、同范围整改边界和真实人工 Gate。

- 授权执行包覆盖的任务按依赖顺序连续执行；不要逐项请求继续。
- 普通 task checkpoint 不是人工 Gate，也不是质量 Gate。完成必要定向检查后继续批次内剩余任务。
- 授权范围不得扩大。新目标、新文件范围、新系统写入或新风险处置必须停止并报告。
- 独立评审、验证和同范围整改是否继续，由授权执行包和流程总控判断；本 skill 不自行扩大权限。

## 任务 gate

- 执行前必须确认当前 task brief 是已授权的唯一任务；不并发、不跳号、不提前进入后续任务。
- 缺目标、验收标准、依赖、允许文件或必要验证命令时不得开始执行；不强制无关设计章节或 `N/A` 占位。
- 单个低、中风险任务不要求 verification evidence、implementer report 或 review checkpoint；需要恢复时只写紧凑 ledger checkpoint。
- 批次 / 里程碑缺最终验证证据、实现摘要、review input 或 ledger event 时，不得推进到 `ready_for_review`。
- 发现 task brief 允许文件范围不足、测试命令缺失、验收口径缺失或计划与代码事实冲突时，停止并回写 `blocked` 或 `needs_user_input`。
- 完成状态只能回写为：`ready_for_review`、`blocked` 或 `needs_user_input`。

## 默认流程

1. 宣告正在使用 `executing-plans` 执行计划。
2. 读取 plan 和 ledger。
3. 先批判性 review plan。
4. 如果计划缺关键路径、测试、文件范围或验收，先停止并修 plan。
5. 如果没有阻塞，建立当前任务清单。
6. 跳过 ledger 中已 `approved` 或 `done` 的任务。
7. 对每个任务逐步执行 plan 中的步骤。
8. 任务执行中严格按 task brief，不做额外功能。
9. 每个低、中风险任务完成必要定向测试或静态检查后继续下一任务，不生成独立 evidence、report 或 review input。
10. 高风险任务按授权包执行专项验证或 review checkpoint。
11. 若授权执行包仍有无阻塞任务，继续执行，不向用户逐项请求确认。
12. 全部任务或里程碑完成后，生成一套实现摘要、最终验证证据、review input 和 ledger event。
13. 批次完成、出现真实 blocker 或需要人类决策时，写入本职结果包，说明 outputs、evidence、ledger event 和 `needs`。
14. 仅在批次质量候选完成时写 `ready_for_review`；其他终态是 `blocked` 或 `needs_user_input`。
15. 只在批次状态变化或跨会话恢复需要时更新 `.factory/memory/`。
16. 所有任务完成后，交还 `using-shanforge` 判断集中验证、评审、人工确认、提交或 PR 闭环。

## Inline 执行规则

- 逐步执行，不跳过验证。
- 计划里的命令必须真实运行，或记录未运行原因。
- 发现 plan 错误时，写 `needs: plan_rewrite`，交还流程总控。
- 遇到 review feedback 时，写 `needs: review_feedback_handling`，交还流程总控。
- 单个任务只报告实现和定向检查事实；批次完成声明必须有最终 evidence。

## STOP 条件

出现以下情况立即 STOP：

- plan 有 critical gap，无法开始。
- 指令不清楚。
- 缺依赖或缺文件。
- 验证反复失败。
- 发现当前任务会越过分层或文件边界。
- 需要人类产品决策、需求取舍、风险接受或授权扩展。
- 超出允许文件范围、目标范围或已批准任务集合。
- 将执行破坏性或外部动作，但授权执行包没有明确授权。
- 当前分支是 main/master 且用户未明确允许直接开发。
- 任务进入 `BLOCKED`。

STOP 后写清楚 blocker、已尝试动作、下一步需要什么。禁止猜测。

定向验证或普通 task checkpoint 完成不是 STOP 条件。只要仍在授权执行包内且没有真实 blocker，就继续内部流程。

## 集中质量 Checkpoint

默认只在全部任务或里程碑完成后设置一个质量 checkpoint：

- 开发期：实现者检查目标、必要测试和文件范围。
- 批次收口：汇总目标、diff、最终验证摘要、风险和未决问题。
- review 通过前，任务不能写成 `approved`。

高风险任务可以提前设置专项 checkpoint。低、中风险任务不得逐项生成 review input package。

## 流程边界

- 本 skill 不判断前置环节是否完成；输入包必须由 `using-shanforge` 或当前会话提供。
- 本 skill 不决定完成后交给谁；只写状态、产物、证据和 `needs`。
- 本 skill 不执行独立 review；只准备批次或高风险专项 review input。
- 本 skill 不执行最终完成声明；只说明是否有足够 evidence。
- 本 skill 不执行提交；只说明是否产生了可提交改动。
- 如发现需要调试、计划重写、评审、验证、人工确认或提交，只在状态包写入 `needs`，不直接调用其他 skill。

## 禁止

- 禁止不 review plan 就执行。
- 禁止跳过 plan 中的验证步骤。
- 禁止把失败验证写成通过。
- 禁止用“继续试试”替代根因定位。
- 禁止在 blocker 下硬推进。
- 禁止自动 commit；本 skill 只记录是否需要提交。

## 完成状态

本 skill 的批次收口必须有：

- evidence。
- implementer report。
- 一个集中质量 checkpoint。
- ledger 事件。
- `.factory/memory/` 同步。

状态包格式：

```text
工作结果：
- work_item: <ID>
- skill: executing-plans
- status: ready_for_review | blocked | needs_user_input
- outputs:
  - <path>
- evidence:
  - <path>
- ledger_event: <event id>
- needs:
  - review | verification | human_confirmation | commit | plan_rewrite | debugging | none
```
