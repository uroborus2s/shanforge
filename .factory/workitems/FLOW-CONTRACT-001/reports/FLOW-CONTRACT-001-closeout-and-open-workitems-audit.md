# FLOW-CONTRACT-001 收口与未关闭 WorkItem 盘点

## 审计结论

- `FLOW-CONTRACT-001` 的顺序实施队列已完成 15/15 项。
- `FLOW-TASK-015` 已由本地提交
  `f21654d082f8e5ca4fba41372ccf66e1865fdbcd` 固化。
- 独立实现复审为 `approved / 98 / C0-I0-M0`，没有开放 Finding。
- 本 WorkItem 可以关闭；这不等于 Shanforge 项目整体完成。
- 当前共有 23 个带 ledger 的 WorkItem；除本 WorkItem 外，其余 22 个中有 2 个已显式终态、
  8 个仍有实际后续动作、12 个已有提交证据但缺 ledger 显式关闭事件。

## 盘点方法

- 逐个读取 `.factory/workitems/*/ledger.jsonl` 的最新有效事件。
- 仅在 ledger 与已提交事实不一致时，使用 `.factory/memory/tasks.summary.md`
  和 Git 提交记录做状态校准。
- 不把历史 `ready_for_review` 事件覆盖在更晚的批准、提交或纠正事件之上。
- 没有显式 `closed`、`committed` 或等价终态证据的 WorkItem 不计为已关闭。

## 仍有实际后续动作的 WorkItem

| WorkItem | 最新有效状态 | 唯一后续动作 |
|---|---|---|
| `ENTERPRISE-AI-DELIVERY-001` | `ready_for_review` | 独立评审 `EAD-TASK-001` |
| `GO-BACKEND-SKILL-001` | `pending_human_confirmation` | 先完成最终验证，再提交人工确认 |
| `PK-SOURCE-MIGRATION-001` | 已纠正误路由、旁路暂停 | 恢复时重新确认 T04 预览 |
| `PM-DASHBOARD-003` | `prototype_updated_ready_for_human_visual_rereview` | 人工视觉复审或确认本地服务验证方式 |
| `SKILL-CLEANUP-001` | `ready_for_review` | 独立只读评审 |
| `SKILL-FLOW-AUDIT-001` | `changes_requested` | 修复 iteration-6 Review feedback |
| `TASK-WORKFLOW-SEMANTICS-001` | `pending_human_confirmation` | 完成人工确认后关闭 |
| `UI-UX-FULL-EXAMPLE-001` | `T06 in_progress` | 完成资源生成、manifest、预览与 Penpot 同步 |

## 仅需 ledger 终态补记

`SF-SP-001` 至 `SF-SP-009` 已在任务摘要中记录本地提交证据，但各自 ledger
最新事件仍停在 `human_approved` 或 `commit` 前状态。它们不需要重新实施，
只需在独立状态治理任务中核对真实 commit 后补显式关闭事件：

- `SF-SP-001..007`：提交 `efac627`
- `SF-SP-008`：提交 `e048784`
- `SF-SP-009`：提交 `9296f58`
- `PM-DASHBOARD-002`：提交 `b63990c`
- `PROJECT-ARTIFACTS-001`：提交 `f3c6c70`
- `UI-DESIGN-SKILL-001`：提交 `d609757`

## 已显式终态的其他 WorkItem

- `DOC-FACTORY-RESTRUCTURE-001`：`completed_superseded_by_formal_baseline`
- `SF-SP-010`：`committed`

## 边界

- 本盘点不修改上述其他 WorkItem。
- 本盘点不从本地提交推导 Push、PR、Merge、部署或项目整体完成。
- 下一项工作必须由用户选择后，再按对应 ledger 最新事件恢复。
