# PM 控制面

本目录承载 shanforge 的项目管理控制面。

它吸收项目管理 Excel 模板的理念，但不照搬 Excel 形态。Excel 的价值是目标、WBS、责任、风险、沟通、状态、变更和复盘的管理闭环；仓库内的事实源仍是 Markdown、JSONL、work item ledger、evidence 和 review 文件。

## 事实源和展示层

- `dashboard.md`：人类和 AI 都可快速读取的项目管理摘要。
- `generated/status-dashboard.html`：人类浏览器状态页，内含需求实时跟踪表，不作为事实源。
- `generated/requirements-lifecycle.html`：需求到关联任务的生命周期详情页，不作为事实源。
- `wbs.md`：WBS 到 work item 的映射。
- `risk-register.jsonl`：风险台账。
- `change-register.jsonl`：变更台账。
- `team-raci.md`、`project-brief.md`、`milestones.md`、`communication-plan.md`、`closure-report.md`：承载 Excel 十表理念中的稳定管理事实。
- `meeting-notes/`、`status-reports/`：承载周期性管理记录。

## 读取规则

- `using-shanforge` 可以在会话启动时读取 `dashboard.md`。
- AI 默认不读取 `generated/status-dashboard.html`。
- 风险、变更、WBS 只在任务相关时读取。
- 执行事实仍以 `.factory/workitems/<ID>/ledger.jsonl` 为准。
- 人类要求查看状态时，由 `using-shanforge` 按 `skills/using-shanforge/references/pm-dashboard-rendering.md` 渲染 HTML。
