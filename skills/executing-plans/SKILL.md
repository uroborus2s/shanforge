---
name: executing-plans
description: 有 written implementation plan 但不使用子 agent，或需要在当前会话 inline 执行 Shanforge work item plan 时使用；先 review plan，再逐步执行任务并设置 review checkpoint。
---

# 执行实施计划

本 skill 是 inline 执行者。它在当前会话中执行已批准计划。

## 触发

- 已有 `.factory/workitems/<WORKITEM-ID>/plan.md`。
- 用户要求在当前会话继续执行计划。
- 当前平台不能或不应使用子 agent。
- 任务强耦合，不适合隔离派发。

## 输入

- 主计划：`.factory/workitems/<WORKITEM-ID>/plan.md`
- 任务 ledger：`.factory/workitems/<WORKITEM-ID>/ledger.jsonl`
- 子任务 brief：`.factory/workitems/<WORKITEM-ID>/task-briefs/`
- evidence：`.factory/workitems/<WORKITEM-ID>/evidence/`
- reports：`.factory/workitems/<WORKITEM-ID>/reports/`
- reviews：`.factory/workitems/<WORKITEM-ID>/reviews/`

## 任务 gate

- 执行前必须确认当前 task brief 是已授权的唯一任务；不并发、不跳号、不提前进入后续任务。
- 缺设计方案、接口设计、UI 或 N/A 原因、测试设计时，不得开始执行；状态回写 `blocked`，并说明缺口。
- 缺 verification evidence、evidence、implementer report、review checkpoint 或 ledger 事件时，不得把任务推进到 `ready_for_review`。
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
9. 每个任务后写 evidence。
10. 每个任务后写 implementer report。
11. 每个任务后设置 review checkpoint。
12. 写入状态回写包，说明 outputs、evidence、ledger event 和 `needs`。
13. 更新 `.factory/workitems/<WORKITEM-ID>/ledger.jsonl`，状态只能是 `ready_for_review`、`blocked` 或 `needs_user_input`。
14. 更新 `.factory/memory/tasks.summary.md`、`tests.summary.md` 和必要 summary。
15. 所有任务完成后，交还 `using-shanforge` 判断验证、评审、人工确认、提交或 PR 闭环。

## Inline 执行规则

- 逐步执行，不跳过验证。
- 计划里的命令必须真实运行，或记录未运行原因。
- 发现 plan 错误时，写 `needs: plan_rewrite`，交还流程总控。
- 遇到 review feedback 时，写 `needs: review_feedback_handling`，交还流程总控。
- 任务完成声明必须有 evidence。

## STOP 条件

出现以下情况立即 STOP：

- plan 有 critical gap，无法开始。
- 指令不清楚。
- 缺依赖或缺文件。
- 验证反复失败。
- 发现当前任务会越过分层或文件边界。
- 需要用户产品决策。
- 当前分支是 main/master 且用户未明确允许直接开发。
- 任务进入 `BLOCKED`。

STOP 后写清楚 blocker、已尝试动作、下一步需要什么。禁止猜测。

## Review Checkpoint

每个任务至少需要一个 review checkpoint：

- 自检：实现者检查 spec、测试、文件范围和 memory sync。
- 独立 review 输入：task brief、diff 摘要、evidence、implementer report、风险和未决问题。
- review 通过前，任务不能写成 `approved`。

如果只有单一主线程可用，必须先写 review input package，并交还 `using-shanforge` 重新进入独立 review 环节。

## 流程边界

- 本 skill 不判断前置环节是否完成；输入包必须由 `using-shanforge` 或当前会话提供。
- 本 skill 不决定完成后交给谁；只写状态、产物、证据和 `needs`。
- 本 skill 不执行独立 review；只准备 review input package。
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

本 skill 的输出不是口头“完成”。必须有：

- evidence。
- implementer report。
- review checkpoint。
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
