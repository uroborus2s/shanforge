---
name: project-memory
description: 项目状态查询、任务延续、会话恢复、上下文压缩后继续工作，或同步 .factory/memory / work item ledger 时使用；限制读取范围、生成会话卡、写入 ledger，并防止重复执行。不用于无项目影响的直接回答或轻量分析。
---

# 项目记忆

本 skill 负责把一次会话恢复到可执行状态。它不替代具体开发 skill，也不调度实现。

## v1.2.0 运行时路由合同

- `SB-STATUS` 与 `SB-RESUME` 都使用 `status-memory-workflow`；前者 `write_policy: no_project_write`，
  后者 `write_policy: state_or_gate_write`。
- `SB-RESUME` 写入前，route 必须有已存在且非空的 `work_item_id`、`task_card_id`，以及精确
  `allowed_paths`、`forbidden_actions`、`current_gate`、`write_policy`；memory summary 不能单独证明身份。
- 只读状态查看不写 ledger；恢复写入必须有 readback evidence 和 ledger event。读取回执（receipt）只说明读了什么、为何扩展和明确未读项，不是项目事实写入。
- 无活动 WorkItem 的纯 `SB-STATUS` / `no_project_write` 请求跳过 work-item ledger，不因缺少 TaskCard/WBS 返回 `blocked`，不写项目事实。
- 返回 `status`、`outputs`、`evidence`、`ledger_event` 和 `gate`；缺事实或身份时返回 `blocked`，不猜测。
  项目级下一动作由 `using-shanforge` 生成，本 skill 只恢复或同步既有事实。

## 触发

- 新会话开始。
- 上下文压缩后继续同一任务。
- 需要确认当前阶段、work item、读取范围或禁止动作。
- 需要更新 `.factory/memory/`、会话卡或 work item ledger。
- 用户提到继续、恢复、同步记忆、ledger、current-state、work item 状态。

## 排除与进入条件

- 本 skill 不用于无项目影响的 `direct_answer` 或 `lightweight_analysis`。
- 只有项目状态查询、任务延续、上下文恢复或项目化流程才能进入本 skill。
- 入口必须先由当前消息完成处理模式判定；不得先读 memory 再判断请求是否简单。
- 若被错误路由到快速通道请求，立即返回调用方，不读取 `.factory/memory/`，不写 ledger 或会话卡。

## 目标

- 先复用已有会话卡和压缩记忆，再判断还需要哪些 summary。
- 默认只读与当前任务相关的文件。
- 输出压缩后的会话卡，并写清本轮排除的背景文件。
- 明确当前阶段、当前 work item、待决事项和禁止动作。
- 把项目是否完成、总体阶段与当前活动、本批剩余、已批准产品剩余、未知/未验证与未开始、当前任务、停止原因和唯一下一动作放在恢复输出头部；缺完整基线写未知，不估算。
- 写入会话 ledger 或 work item ledger，避免重复执行已完成动作。
- 同步 `.factory/memory/current-state.md`、`tasks.summary.md`、`tests.summary.md` 等摘要时，只写已观察到的事实。

## 含义保留清单

- 会话入口来自 `.factory/memory/`，不是阶段 `docs/` 长文。
- `project-memory` 接管会话恢复、读取范围、会话卡和 ledger 模板。
- 旧会话脚本只作为已迁移来源记录，不再作为目标入口继续增强。
- 具体开发动作仍由 `brainstorming`、`writing-plans`、`executing-plans`、`tdd-workflow`、`requesting-code-review` 等 skill 执行。
- 实现者不能自批完成；完成状态必须依赖验证、评审和 memory sync 证据。

## 条件读取链

- 读取目标是恢复当前任务，不是加载固定文件清单；每一级够用即停。
- 当前对话中的新鲜会话卡足够时，读取 memory 文件数必须为 0。
- 当前对话不足时只读 `.factory/memory/agent-session.md` 的当前卡；若它新鲜且匹配当前 work item，不再读取其他 memory。
- 会话卡缺失、过期或不匹配时，每次扩展读取前先写明事实缺口，一次只读取一个最小片段，并在补足后立即停止。
- 不能只读 `.factory/memory/current-state.md` 就判断权威状态；任务 Gate 必须回到当前 TaskCard 和 work item ledger。
- 不得固定读取 `agent-session.md`、`runtime-brief.md`、`current-state.md` 三件套；`runtime-brief.md`、`current-state.md`、summary、`doc-map.md` 都只能由明确缺口触发。
- 读取 receipt 必须列出已读文件、每次扩展原因和明确未读文件，防止压缩记忆再次扩张。

## 默认流程

1. 确认调用方已把请求判定为项目状态查询、任务延续、上下文恢复或项目化流程；否则按“排除与进入条件”退出。
2. 先看当前对话是否已有可用会话卡、当前阶段、work item 和禁止动作。
3. 若已有同一 work item 的新鲜会话卡，复用它；不要重复读取源 summary。
4. 若缺少会话卡，读取 `.factory/memory/agent-session.md`；先读取当前状态头部，再把后续带日期条目视为历史。只在会话卡缺失、过期或与当前任务不匹配时继续读取。
5. 仍缺关键事实时，从 `.factory/memory/runtime-brief.md` 或 `.factory/memory/current-state.md` 二选一，只读取能补足当前缺口的最小片段；够用即停。
6. 只有需要定位正式事实源时，才读取 `.factory/memory/doc-map.md`。
7. 只有当前任务需要角色协作事实时，才读取 `.factory/memory/role-charter.project.md`。
8. 只有需要项目元数据时，才读取 `.factory/project.json`。
9. 按 `references/relevance-gate.md` 判断是否读取任务相关 summary。
10. 需要实现前，再按项目规则回源技术设计事实。
11. 对有活动 WorkItem 的恢复请求读取 work item ledger；以最新有效事件核对当前 Gate，`status=approved|done|passed` 且 `idempotency_key` 相同的动作不得重复执行。无活动 WorkItem 的纯 `SB-STATUS` / `no_project_write` 请求跳过 work-item ledger。
12. 输出压缩会话卡：项目是否完成、总体阶段与当前活动、本批剩余、已批准产品剩余、未知/未验证与未开始、当前任务、停止原因、唯一下一动作、已读上下文、明确排除项和禁止动作；缺完整基线写未知，不估算。
13. 需要落盘时，按 references 模板更新会话卡、ledger 和 `.factory/memory/`。

## 当前态生命周期

- `current-state.md` 只保留活跃任务、真实阻塞项、最近事实、唯一下一动作和历史回源入口，不保存完整任务流水。
- 已关闭任务在下一次 memory sync 从 `current-state.md` 降级到 `tasks.summary.md` 或其 work item ledger；最近事实最多保留 5 条。
- `current-state.md` 不超过 16 KiB 和 80 行；超过任一阈值必须在本次 memory sync 压缩后再交接。
- 降级只改变恢复投影，不改变审计事实；ledger、evidence、review 和 report 永不因降级删除。
- summary 只保存可定位摘要；需要细节时先查索引，再定向读取 ledger 或正式来源。

## 当前态恢复不变量

- 当前状态头部优先于历史条目；正式文档和 ledger 仍是更高事实源。
- 历史条目中的“当前”“下一步”不得覆盖头部，只表示记录发生时的状态。
- 必须按最新 ledger 事件确认 Gate 是否仍有效；不得恢复已撤销、已取代或已关闭的 Gate。
- 会话卡头部必须包含项目是否完成、总体阶段与当前活动、本批剩余、已批准产品剩余、未知/未验证与未开始、当前任务、停止原因和唯一下一动作。
- 当前任务已完成但项目未完成时，必须分别记录任务完成态与项目剩余步骤。
- 没有活动任务、人工 Gate 或后台动作时，明确写“当前无活动任务”“停止原因：无”，不要伪造等待状态。

## 读取门

- 禁止默认读取阶段 `docs/` 长文。
- 禁止用“稳妥”作为散读理由。
- 当前任务直接修改正式文档时，可以读取该文件。
- 进入实现前必须回源技术选型和相关架构边界。
- summary 不足以回答当前任务时，按 `.factory/memory/doc-map.md` 单文件回源。

## 事实源优先级

- 正式文档和 work item ledger 高于 memory summary。
- `docs/` 承载人类可审计正式事实。
- `.factory/workitems/<ID>/ledger.jsonl`、`evidence/`、`reviews/` 和 `reports/` 承载执行事实。
- `.factory/memory/*.summary.md` 只写 ID、状态、当前 gate、关键约束和索引；summary 不复制完整正文。
- HTML 和 cache 都是可重建投影；不得把 `.factory/cache/site/current/index.html` 作为正式事实源。
- summary、索引或站点视图与正式文档、ledger 冲突时，以正式文档和 ledger 为准，并重建派生物。

## 写入边界

- `direct_answer` 和 `lightweight_analysis` 不进入本 skill，不得写任何仓内文件、memory、ledger 或 summary；用户要求持久化时必须先升级为项目化流程。
- `project_workitem` 和 `tracked_task` 发生状态变化、gate 切换、上下文压缩恢复、关闭前验证或提交前检查时，才同步 memory。
- memory 只写 work item / task ID、状态、当前 gate、关键约束、禁止动作、总控已生成的项目状态信封，以及 outputs / evidence / review / report 路径索引；不得自行推导项目级下一动作。
- 正式需求、设计、API、UI、用户指南或开发者指南的稳定事实写入 `docs/`；memory 只保留索引和摘要。
- 命令全文、临时推理、当前会话答复、子 agent 完整输出和正式文档正文不得写入 memory。
- 子 agent 或自循环完成后，先把状态包交回主流程；是否写 memory 由 `using-shanforge` 根据状态和 gate 判断。

## 输出

简短输出即可：

```text
阶段：IMPLEMENTATION
工作项：SF-SP-002
项目整体进度：第 5/8 步，开发实现
当前任务：项目记忆 Skill；ready_for_review
停止原因：无
唯一下一动作：完成既有授权范围内的独立只读评审
已读：agent-session、workitem ledger
未读/排除：role-charter、doc-map、阶段 docs、user-guide
禁止：散读 docs、重复执行已通过 ledger 事件、自批 done
待决：交回 `using-shanforge` 判断下一步动作
```

需要写文件时使用：

- `references/session-card-template.md`
- `references/memory-ledger-event-template.md`
- `references/current-state-update-checklist.md`

## 禁止

- 不得把旧中心命令、动作注册表或全局脚本当成新流程主控。
- 不得把旧会话脚本的推荐命令照搬为新入口。
- 不得把计划中未执行的动作写成完成事实。
- 不得用历史条目复活已关闭 Gate，或把内部 checkpoint 写成人工待办。
- 不得因为上下文不足而散读整仓文档。
- 不得把实现者自评写成 `approved` 或 `done`。

## 完成状态

本 skill 自身只负责恢复和同步。若当前会话产出代码、skill 或文档改动，作者只能把对应任务推进到 `ready_for_review`，再交给独立 review task。
