---
name: project-memory
description: 每次 Shanforge 会话恢复、上下文压缩后继续工作、同步 .factory/memory 或 work item ledger 时使用；限制读取范围、生成会话卡、写入 ledger，并防止重复执行。
---

# 项目记忆

本 skill 负责把一次会话恢复到可执行状态。它不替代具体开发 skill，也不调度实现。

## 触发

- 新会话开始。
- 上下文压缩后继续同一任务。
- 需要确认当前阶段、work item、读取范围或禁止动作。
- 需要更新 `.factory/memory/`、会话卡或 work item ledger。
- 用户提到继续、恢复、同步记忆、ledger、current-state、work item 状态。

## 目标

- 先复用已有会话卡和压缩记忆，再判断还需要哪些 summary。
- 默认只读与当前任务相关的文件。
- 输出压缩后的会话卡，并写清本轮排除的背景文件。
- 明确当前阶段、当前 work item、待决事项和禁止动作。
- 写入会话 ledger 或 work item ledger，避免重复执行已完成动作。
- 同步 `.factory/memory/current-state.md`、`tasks.summary.md`、`tests.summary.md` 等摘要时，只写已观察到的事实。

## 含义保留清单

- 会话入口来自 `.factory/memory/`，不是阶段 `docs/` 长文。
- `project-memory` 接管会话恢复、读取范围、会话卡和 ledger 模板。
- 旧会话脚本只作为已迁移来源记录，不再作为目标入口继续增强。
- 具体开发动作仍由 `brainstorming`、`writing-plans`、`executing-plans`、`tdd-workflow`、`requesting-code-review` 等 skill 执行。
- 实现者不能自批完成；完成状态必须依赖验证、评审和 memory sync 证据。

## 默认流程

1. 先看当前对话是否已有可用会话卡、当前阶段、work item 和禁止动作。
2. 若已有同一 work item 的新鲜会话卡，复用它；不要重复读取源 summary。
3. 若缺少会话卡，读取 `.factory/memory/agent-session.md`；只在它缺失、过期或与当前任务不匹配时继续读取。
4. 仍缺关键事实时，按最小集合读取 `.factory/memory/runtime-brief.md` 和 `.factory/memory/current-state.md`。
5. 只有需要定位正式事实源时，才读取 `.factory/memory/doc-map.md`。
6. 只有当前任务需要角色协作事实时，才读取 `.factory/memory/role-charter.project.md`。
7. 只有需要项目元数据时，才读取 `.factory/project.json`。
8. 按 `references/relevance-gate.md` 判断是否读取任务相关 summary。
9. 需要实现前，再按项目规则回源技术设计事实。
10. 读取 work item ledger；`status=approved|done|passed` 且 `idempotency_key` 相同的动作不得重复执行。
11. 输出压缩会话卡：当前阶段、work item、已读上下文、明确排除项、禁止动作和待决事项。
12. 需要落盘时，按 references 模板更新会话卡、ledger 和 `.factory/memory/`。

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
- PM generated 非事实源；不得把 `.factory/pm/generated/status-dashboard.html` 作为唯一事实源。
- summary 或 PM view 与正式文档、ledger 冲突时，以正式文档和 ledger 为准。

## 输出

简短输出即可：

```text
阶段：IMPLEMENTATION
工作项：SF-SP-002
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
- 不得因为上下文不足而散读整仓文档。
- 不得把实现者自评写成 `approved` 或 `done`。

## 完成状态

本 skill 自身只负责恢复和同步。若当前会话产出代码、skill 或文档改动，作者只能把对应任务推进到 `ready_for_review`，再交给独立 review task。
