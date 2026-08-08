---
name: writing-plans
description: 仅在已批准的 spec、需求、设计或 work item brief 需要拆成多个可验收交付物、跨模块协调或明确正式计划时使用；输出最小 Shanforge work item plan、task brief 和批次质量门。局部代码修改加对应单测即可完成的简单任务不触发。
---

# 编写实施计划

本 skill 把已批准输入转成可执行计划。它只负责编写计划，不直接改代码。
计划只能生成候选执行输入，不执行代码。

## v1.2.0 运行时路由合同

- `SB-PLAN` 进入 `planning-workflow`，`write_policy: project_fact_write`。
- 写入前，route 必须有已存在且非空的 `work_item_id`、`task_card_id`，以及精确 `allowed_paths`、
  `forbidden_actions`、`current_gate`、`write_policy`；只写 allowlist 内 plan、TaskCard 和计划证据。
- 返回 `status`、`outputs`、`evidence`、`ledger_event`、`gate`、`next_required_action`；本 skill 不执行计划，
  不自批 Review。

## 触发

已有批准输入，并满足以下任一条件时才触发：

- 任务包含多个可独立验收的交付物，需要明确依赖、顺序或并行关系。
- 任务跨模块、跨层或跨系统，需要先锁定接口、数据、迁移、发布或回滚策略。
- 任务需要跨会话追踪，或需要多人、子 agent 分工和独立验收。
- 用户明确要求“写正式计划”“拆任务”“生成实施计划”或 `plan`。

不得因为已有已批准输入或尚无 plan 就强制触发。

## 简单任务不触发

同时满足以下条件时，视为简单任务：

- 用户未明确要求正式计划。
- 需求和验收结果明确，不需要产品、设计或架构取舍。
- 用一次局部代码修改加对应单测即可完成。
- 不改变公共接口、跨层边界、数据 schema、迁移、依赖、安全权限、外部系统或发布方式。
- 不需要拆成多个可独立验收交付物，也不需要跨会话、并行或多人协调。

简单任务交回流程总控直接实现。默认只运行对应定向测试和必要静态检查；出现影响扩大的证据时再升级验证范围。全量测试不是每个简单修改的默认步骤。

用户明确要求正式计划时，覆盖简单任务判定，本 skill 正常生成计划。

简单任务不创建 plan、task brief 或计划评审。实现阶段是否记录 ledger 和 evidence 由流程总控及实现工作流决定，不属于本 skill 的职责。若本 skill 被误触发，立即停止且不生成计划文件，返回 `status: not_applicable` 和 `reason: simple_change`，由流程总控直接进入实现。

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
- 批次证据、实现摘要和评审输出：仅在批次 / 里程碑收口时写入
  `.factory/workitems/<WORKITEM-ID>/{evidence,reports,reviews}/`
- 任务 ledger：`.factory/workitems/<WORKITEM-ID>/ledger.jsonl`

如果用户明确指定其他路径，先说明偏离原因，再按用户路径写入。

## 含义保留清单

- 只有需要拆分和协调的多步骤任务动代码前才写计划。
- 简单任务不触发；局部代码修改加对应单测可以直接实现和定向验证。
- 计划必须让不了解当前代码库的人也能执行。
- 先锁定文件结构，再拆任务。
- 每个文件只有一个清晰职责。
- 一个任务卡对应一个可验收交付物，不对应单个 2-5 分钟动作。
- 一个任务必须能独立产生可测试结果。
- 每个任务只写目标、依赖、精确路径、最小实现、验收结果和必要的定向测试。
- Red / Green 只在新增行为、Bug 或有回归风险时要求；已有测试足以覆盖时直接复用。
- 设计方案、接口设计和 UI 只在任务实际涉及时写，不生成 `N/A` 占位。
- review、服务测试、API 测试和集成测试默认放在批次质量任务，不复制到每张任务卡。
- 每个代码步骤写精确文件路径、实际内容、真实命令和期望输出。
- 计划必须禁止占位符。
- 计划完成后做一次计划自审；只有高风险、公共契约、跨服务、不可逆变更或用户明确要求时才请求独立 plan review。
- 执行阶段由流程总控判断；本 skill 不写下一步 skill。

## 默认流程

1. 宣告正在使用 `writing-plans` 生成实施计划。
2. 先应用“简单任务不触发”判定；命中时不生成任何计划产物，返回 `not_applicable`。
3. 确认输入已批准；未批准时停止并交回流程总控。
4. 确认 work item id；没有 id 时先用当前任务名生成稳定临时 id，并写入计划头部。
5. 做范围检查：如果输入覆盖多个独立子系统，建议拆成多个 work item plan；实现前确认设计输入已同时给出开发设计和
   测试设计（验收、层级、角色 / 接口案例、环境数据、自动化入口、进入 / 退出条件和报告结构）。缺项回设计，不在计划中猜补。
6. 先锁定文件结构：列出 create、modify、test、docs、memory 文件。
7. 对每个文件说明职责、owner、所属层、接口边界和禁止耦合。
8. 把计划拆成任务卡；每张任务卡必须交付一个可验收交付物，并能独立验证。
9. 每张任务卡只写最小执行 checklist：读取必要文件、实现、定向检查和紧凑状态回写。
10. 为全部开发任务增加一个批次质量任务，覆盖集中代码审查、API 契约测试、服务测试和集成测试；
    按风险增加 E2E、安全或性能测试。质量任务包含“首个候选完整必需测试 -> 缺陷定向修复 / 复测 -> 最终候选完整必需测试”，
    不为每个 Bug 新建计划或全仓测试任务。生产上线在范围内时，再增加一个消费最终候选和测试报告的发布任务。
11. 每步写真实命令和期望输出；代码步骤必须写实际补丁形状，禁止占位语。
12. 写文档同步要求；memory 只在需要跨会话恢复或批次状态变化时同步。
13. 标记风险：低、中风险任务连续开发；高风险任务可提前设置专项 review gate。
14. 按 [workitem-plan-template.md](references/workitem-plan-template.md) 保存计划。
15. 按 [task-brief-template.md](references/task-brief-template.md) 生成最小任务 brief。
16. 做一次计划自审；仅在高风险或用户明确要求时按 [plan-review-template.md](references/plan-review-template.md) 生成 review handoff。

## 任务粒度

- 任务卡粒度是一个可验收交付物。
- 步骤粒度留在 task 内部 checklist。
- 读文件、运行命令、写失败测试、记录 evidence 不是任务卡。
- 一张任务卡只交付一个可验收交付物。
- 任务卡必须能独立实现并做定向检查；质量结论在批次或里程碑集中产生。
- 2-5 分钟动作只作为任务内部 checklist，不单独拆成任务卡。
- 内部 checklist 至少覆盖：读必要文件、最小实现、必要测试或静态检查、真实结果。
- 提交不是每个小步骤的硬要求；本 skill 只在计划中说明“是否形成可提交工作单元”，不决定提交 skill。

## 任务层级与关联

每张正式任务卡都声明 `task_scope`，且只允许：
`project | requirement | cross_cutting | system`。`task_scope` 是业务层级，
不得复用 `task_kind` 表达 `task_scope`。

- `requirement` 至少强关联一个 `REQ-*` 或 `NFR-*`，使用从任务到需求的强
  `IMPLEMENTS` 关系。
- `cross_cutting` 强关联一个或多个 `REQ-*` / `NFR-*`，允许一项任务横跨多个需求。
- `project` 关联项目基线、项目章程或设计项，不强制关联单个需求；使用强
  `IMPLEMENTS` 或 `DEPENDS_ON` 关系。
- `system` 对产品进度贡献为零，只用于治理、同步、审计等系统工作。

关联沿用现有关系图，不在 task brief、SQLite 或 PM 层另建平行关联表。计划自审和
plan review 必须拒绝缺少层级、缺少该层级所需关联或把 `system` 计入产品进度的任务。

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
5. Quality convergence：是否有一个批次质量任务，并按风险覆盖 review、API、服务、集成和必要专项测试。

发现问题时先修计划，再请求 review。不要把有缺口的计划交给执行者。

## Plan Review

计划默认只做一次作者自审。出现高风险、公共契约、跨服务、数据迁移、不可逆变更，或用户明确要求时，
才生成独立 review 请求。输入只包含：

- work item plan。
- 原始 spec、需求、设计或 brief。
- 文件结构清单。
- 测试策略。
- 风险与集中质量策略。

review 输出写入 `.factory/workitems/<WORKITEM-ID>/reviews/plan-review.md`。

## 流程边界

- 本 skill 不判断前置环节是否完成；输入包必须由 `using-shanforge` 或当前会话提供。
- 本 skill 不决定计划通过后交给谁；只写 plan、task brief、适用的 review handoff 和状态回写。
- 本 skill 不执行代码、不执行 review、不执行提交。
- 简单任务误触发时必须以 `not_applicable` 退出，不得为了满足流程形式生成空计划或治理产物。
- 如发现输入未批准、需要拆 work item、需要人工决策或高风险计划需要 review，只在状态包写入 `needs`，不直接调用其他 skill。

状态包格式：

```text
工作结果：
- work_item: <ID>
- skill: writing-plans
- status: plan_ready | ready_for_review | not_applicable | blocked | needs_user_input
- outputs:
  - .factory/workitems/<WORKITEM-ID>/plan.md
  - .factory/workitems/<WORKITEM-ID>/task-briefs/
- evidence:
  - <path>
- ledger_event: <event id>
- needs:
  - plan_review | human_confirmation | none
```

`not_applicable` 只用于命中“简单任务不触发”规则，必须同时返回 `reason: simple_change`，且 `outputs`、`evidence` 和 `ledger_event` 为空。

## 完成状态

低、中风险计划自审后输出 `plan_ready`。高风险或用户明确要求独立评审时输出 `ready_for_review`；
`approved` 仍必须来自真实 plan review。代码实现、批次质量评审、提交和 PR 闭环由流程总控另行判断。

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。
