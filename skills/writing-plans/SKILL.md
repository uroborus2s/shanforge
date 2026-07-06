---
name: writing-plans
description: 有已批准的 spec、需求、设计或 work item brief，且多步骤任务动代码前需要生成实施计划时使用；输出 Shanforge work item plan、task brief、验证策略和 review gate。
---

# 编写实施计划

本 skill 把已批准输入转成可执行计划。它只负责编写计划，不直接改代码。
计划只能生成候选执行输入，不执行代码。

## 触发

- 用户已有明确 spec、需求、设计或 work item brief。
- 任务需要多步骤实现。
- 任务动代码前需要拆出文件结构、测试策略、文档同步和 memory 同步。
- 用户要求“写计划”“拆任务”“生成实施计划”“plan”。

## 输入

优先使用当前对话和 `project-memory` 会话卡。缺少关键信息时，读取：

- `.factory/workitems/<WORKITEM-ID>/brief.md`
- `.factory/workitems/<WORKITEM-ID>/ledger.jsonl`
- 相关 `.factory/memory/*summary.md`
- 必要时按 `.factory/memory/doc-map.md` 单文件回源正式文档

已批准的 spec、需求、设计或 work item brief 是进入本 skill 的前提。未批准的创意输入先交给 `brainstorming`。

## 输出位置

- 主计划：`.factory/workitems/<WORKITEM-ID>/plan.md`
- 子任务：`.factory/workitems/<WORKITEM-ID>/task-briefs/`
- 证据目录：`.factory/workitems/<WORKITEM-ID>/evidence/`
- 实现报告：`.factory/workitems/<WORKITEM-ID>/reports/`
- 评审输出：`.factory/workitems/<WORKITEM-ID>/reviews/`
- 任务 ledger：`.factory/workitems/<WORKITEM-ID>/ledger.jsonl`

如果用户明确指定其他路径，先说明偏离原因，再按用户路径写入。

## 含义保留清单

- 多步骤任务动代码前先写计划。
- 计划必须让不了解当前代码库的人也能执行。
- 先锁定文件结构，再拆任务。
- 每个文件只有一个清晰职责。
- 一个任务必须能独立产生可测试结果。
- 每个任务包含 Red 和 Green 步骤。
- 每个任务必须包含设计方案、接口设计、UI 或 `N/A`、测试设计、开发、单测、review 和集成测试。
- 每个代码步骤写精确文件路径、实际内容、真实命令和期望输出。
- 计划必须禁止占位符。
- 计划完成后做计划自审，再请求 plan review。
- 执行阶段由流程总控判断；本 skill 不写下一步 skill。

## 默认流程

1. 宣告正在使用 `writing-plans` 生成实施计划。
2. 确认输入已批准；未批准时停止并交回 `brainstorming` 或需求 skill。
3. 确认 work item id；没有 id 时先用当前任务名生成稳定临时 id，并写入计划头部。
4. 做范围检查：如果输入覆盖多个独立子系统，建议拆成多个 work item plan。
5. 先锁定文件结构：列出 create、modify、test、docs、memory 文件。
6. 对每个文件说明职责、owner、所属层、接口边界和禁止耦合。
7. 把计划拆成小任务；每个任务必须能独立验证。
8. 每个任务写 Red、Green、review、memory sync 步骤。
9. 每个任务写设计方案、接口设计、UI 或 `N/A`、测试设计、开发、单测、review 和集成测试。
10. UI 写 `N/A` 时必须写原因；缺测试设计则失败，UI 写 `N/A` 但无原因则失败，发现占位语则失败。
11. 每步写真实命令和期望输出；代码步骤必须写实际代码或明确补丁形状。
12. 写测试策略：定向测试、邻近回归、全量回归和不运行项。
13. 写文档同步和 `.factory/memory/` 同步要求。
14. 写 review gate：implementer 只能到 `ready_for_review`，通过必须来自独立 review。
15. 按 [workitem-plan-template.md](references/workitem-plan-template.md) 保存计划。
16. 按 [task-brief-template.md](references/task-brief-template.md) 生成任务 brief。
17. 按 [plan-review-template.md](references/plan-review-template.md) 做自审和 review handoff。

## 任务粒度

- 一步只做一个动作。
- 推荐粒度是 2-5 分钟。
- 典型顺序：写失败测试、运行确认失败、最小实现、运行确认通过、记录 evidence、请求 review。
- 提交不是每个小步骤的硬要求；本 skill 只在计划中说明“是否形成可提交工作单元”，不决定提交 skill。

## 禁止占位符

计划里不得出现这些交付：

- 只写“后续实现”“补充测试”“添加适当错误处理”。
- 只写“类似上一任务”。
- 只写“写测试”，但不给测试目标、命令和期望输出。
- 引用尚未在前置任务定义的函数、类型或文件。
- 把未执行的验证写成已经通过。

## 计划自审

保存计划前必须自审：

1. Spec coverage：每条需求能否指向具体任务。
2. Placeholder scan：是否存在占位符、泛化步骤或未定义对象。
3. Type consistency：后续任务使用的函数、类型、字段是否与前序定义一致。
4. Buildability：工程师按计划执行时是否会卡在缺文件、缺命令、缺上下文。
5. Shanforge gate：是否包含 evidence、review、PR、memory sync 和 ledger 更新。

发现问题时先修计划，再请求 review。不要把有缺口的计划交给执行者。

## Plan Review

计划完成后必须生成 review 请求。review 输入至少包含：

- work item plan。
- 原始 spec、需求、设计或 brief。
- 文件结构清单。
- 测试策略。
- `.factory/memory/` 同步要求。

review 输出写入 `.factory/workitems/<WORKITEM-ID>/reviews/plan-review.md`。

## 流程边界

- 本 skill 不判断前置环节是否完成；输入包必须由 `using-shanforge` 或当前会话提供。
- 本 skill 不决定计划通过后交给谁；只写 plan、task brief、review handoff 和状态回写。
- 本 skill 不执行代码、不执行 review、不执行提交。
- 如发现输入未批准、需要拆 work item、需要人工决策或计划需要 review，只在状态包写入 `needs`，不直接调用其他 skill。

状态包格式：

```text
工作结果：
- work_item: <ID>
- skill: writing-plans
- status: ready_for_review | blocked | needs_user_input
- outputs:
  - .factory/workitems/<WORKITEM-ID>/plan.md
  - .factory/workitems/<WORKITEM-ID>/task-briefs/
- evidence:
  - <path>
- ledger_event: <event id>
- needs:
  - plan_review | human_confirmation | none
```

## 完成状态

本 skill 只把计划推进到 `ready_for_review`。`approved` 必须来自 plan review。代码实现、任务评审、提交和 PR 闭环由流程总控另行判断。
