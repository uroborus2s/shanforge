# shanforge PM Dashboard

- 更新时间：2026-07-06 11:45:00 +0800
- 当前阶段：`IMPLEMENTATION`
- 总体状态：流程契约 `FLOW-CONTRACT-001` 已通过实施前独立评审，当前停在 `pending_human_confirmation`；`SKILL-FLOW-AUDIT-001` 仍有 flow completeness 反馈待修；Superpowers `SF-SP-001` 到 `SF-SP-010` 已完成本地提交闭环，但没有 push / PR / merge 证据。
- 管理口径：PM 控制面负责目标、WBS、状态、风险、变更和人类查看；work item ledger、review ledger 和 git log 负责执行事实。
- 展示页：`generated/status-dashboard.html` 作为人类查看层，不作为事实源。

## 当前管理门禁

| 门禁 | 状态 | 说明 |
|---|---|---|
| 项目目标 | 已定义 | 抽象 Agent 平台，当前重点是流程契约、记忆、评审、验证和 PM 控制面 |
| WBS | 已刷新 | 当前包含 PM 控制面、Superpowers 本地闭环、流程契约和 skill-flow audit |
| 执行证据 | 建立中 | work item ledger 和 review ledger 已形成主链 |
| 独立评审 | 部分满足 | `FLOW-CONTRACT-001` 实施前评审 `approved / 94`；`SKILL-FLOW-AUDIT-001` flow completeness 仍为 `changes_requested / 86` |
| 人工确认 | 阻塞推进 | `FLOW-CONTRACT-001` 必须等用户确认后才能进入实施 |
| PM 状态页 | 已刷新 | `generated/status-dashboard.html`、`pm-details.html`、`workitems.html`、`requirements-lifecycle.html` 已按需重刷 |

## 当前 WBS / Work Item

| WBS | Work item | 管理目标 | 当前状态 | 下一动作 |
|---|---|---|---|---|
| PM-001 | PM 控制面 | 将项目管理 Excel 理念融入 shanforge 流程与文档 | `done` | 按需查看 HTML 页面 |
| FLOW-001 | `FLOW-CONTRACT-001` | 把流程契约需求与实施方案转入 skill 实施前 gate | `pending_human_confirmation` | 用户确认后进入实施 |
| AUDIT-001 | `SKILL-FLOW-AUDIT-001` | 清理 skill 入口语言、prompt 和流程契约完整性 | `changes_requested` | 修 flow completeness Critical / Important |
| SF-SP | `SF-SP-001`..`SF-SP-010` | Superpowers workflow cleanup / skill-first 迁移链 | `local_commit_closed` | 如需远端闭环，单独 push / PR / merge |
| MG | `MG-WP-001`..`MG-WP-005` | 记忆治理模型、recall/provider/lifecycle/explainability 收口 | `in_progress` | 继续 lifecycle review queue 与 explainability 收敛 |
| TASK | `TASK-016`、`TASK-017`、`TASK-020` | Session search、基础能力层、外部 DI / provider governance | `in_progress` | 继续 provider profile 化和 legacy diagnostics 去重 |

## 当前风险

| 风险 | 等级 | 状态 | 缓解措施 |
|---|---|---|---|
| 工作 skill 重新承担流程路由 | 高 | 开放 | `using-shanforge` 作为唯一流程总控，工作 skill 只输出状态包 |
| PM 状态页与 ledger 不一致 | 中 | 开放 | HTML 只做展示；本轮已按 ledger、memory summary 和 git log 刷新 |
| `FLOW-CONTRACT-001` 未经人工确认直接实施 | 高 | 开放 | 当前 gate 明确为 `pending_human_confirmation` |
| `SKILL-FLOW-AUDIT-001` flow completeness Critical 未修 | 高 | 开放 | 先修 Critical / Important，再重新评审 |

## 最近状态报告

- 已完成：`SF-SP-001` 到 `SF-SP-007` 本地提交为 `efac627`，`SF-SP-008=e048784`，`SF-SP-009=9296f58`，`SF-SP-010=3b0e9a5`。
- 已完成：旧全局流程脚本和旧入口已清理；活跃入口改为 `using-shanforge` + `project-memory` + 具体工作 skill。
- 当前阻塞：`FLOW-CONTRACT-001` 等待人工确认；`SKILL-FLOW-AUDIT-001` 等待修复 flow completeness 复测发现。
- 未完成：远端 push / PR / merge 没有证据；PM 自动渲染 helper 暂不做。
- 下一步：先处理 `FLOW-CONTRACT-001` 人工确认或修改意见；并行上修 `SKILL-FLOW-AUDIT-001` Critical / Important。
