# T06 迁移激活与对账证据

**迁移 Job：** `TASK-IMPLEMENT-003-T06`
**迁移包：** `.factory/cache/project-knowledge/migration/TASK-IMPLEMENT-003-T06/after-images/migration-plan.json`（本地 cache，可删除）
**结论：** 15 项逐一处置，强关系 `20 -> 20`，丢失 `0`。

## Catalog

| 源 | 处置 | 最终目标 | before SHA-256 |
|---|---|---|---|
| `docs/05-design/ai-sdlc-catalog.source.json` | 迁出人类文档目录 | `.factory/catalog/ai-sdlc-catalog.source.json` | `ff1d322682a8…` |
| `docs/05-design/ai-sdlc-catalog.manifest.json` | 归档历史发布回执 | `.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-DESIGN-001-R019-ai-sdlc-catalog-release-manifest.json` | `813e56f54489…` |

固定 Builder 已改为读取 `.factory/catalog/ai-sdlc-catalog.source.json`。真实构建返回 `workflow_count=123`、`application_reads=1`、`network_reads=0`、`child_processes=0`。

## legacy PM

以下 13 个文件完成 owner 对账后删除，旧 `.factory/pm` 不再保存事实：

- `README.md`、`project-brief.md`、`team-raci.md`、`milestones.md`、`wbs.md`
- `risk-register.jsonl`、`communication-plan.md`、`change-register.jsonl`、`closure-report.md`、`dashboard.md`
- `meeting-notes/2026-07-05-pm-control-plane.md`
- `status-reports/2026-07-05.md`、`status-reports/2026-07-06.md`

这些内容要么已由正式文档/work item ledger 承载，要么可由当前索引确定性投影。旧 generated HTML 同样退役，当前入口统一为 `.factory/cache/site/current/index.html`。

## 回滚

迁移包为每项保存 before Hash、原路径 rollback 文件和 disposition。cache 按维护策略会被清理，因此长期审计依据是本证据、历史 manifest、Git 历史和正式 owner，不把 cache 当永久事实。
