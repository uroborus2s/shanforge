# PM WBS

- 更新时间：2026-07-06 11:45:00 +0800

本文件只记录管理级工作分解。执行细节在 `.factory/workitems/<WORKITEM-ID>/`，提交事实以 `git log` 为准。

| WBS | Work item | 目标 | 输出 | 当前状态 |
|---|---|---|---|---|
| PM-001 | PM 控制面 | 将项目管理 Excel 理念转成 shanforge PM 控制面 | 方案文档、`.factory/pm/`、HTML 状态页 | `done` |
| FLOW-001 | `FLOW-CONTRACT-001` | 建立流程契约需求、实施方案和任务卡，并通过实施前 gate | 需求文档、实施方案、任务卡、pre-review | `pending_human_confirmation` |
| AUDIT-001 | `SKILL-FLOW-AUDIT-001` | 修正 skill 语言 / prompt / flow completeness 缺口 | review 报告、修复报告、验证证据 | `changes_requested` |
| SF-SP | `SF-SP-001`..`SF-SP-010` | Superpowers workflow cleanup 与 skill-first 迁移 | skills、references、review/evidence、memory sync、本地提交 | `local_commit_closed` |
| MG | `MG-WP-001`..`MG-WP-005` | 记忆治理模型、recall/provider/lifecycle/explainability 收口 | domain/runtime/settings 代码与治理测试 | `in_progress` |
| TASK | `TASK-016`、`TASK-017`、`TASK-020` | Session search、基础能力层和外部 DI/provider governance | session/search、runtime bridges、composition/provider governance | `in_progress` |

## 管理规则

- WBS 只描述管理边界，不写实现步骤。
- 每个 WBS 条目必须能映射到 work item、正式文档、代码任务或 PM 控制面产物。
- 状态以对应 ledger、review ledger、memory summary 和 git log 的最新有效事实校准。
- dashboard 可以摘录 WBS，但不替代本文件和 work item ledger。
