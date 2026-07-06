# 文档压缩映射

## 读取规则

- 人类文档保留为正式说明层。
- AI 默认先读压缩文档与 summary，再按需回看正式文档。
- 禁止默认全文加载 `docs/`。
- 禁止在没有事实缺口时回源人类长文档。
- 禁止一次性并行加载多个阶段的正式文档。
- 需要回源时，只允许按当前任务单文件回源。

## 事实源优先级

- `docs/` 是人类可审计正式事实源。
- `.factory/workitems/<ID>/ledger.jsonl`、`evidence/`、`reviews/` 和 `reports/` 是执行事实源。
- 正式文档和 work item ledger 高于 memory summary。
- `.factory/memory/*.summary.md` 只存摘要和索引，不能复制完整正式正文。
- PM generated 非事实源；`.factory/pm/generated/status-dashboard.html` 是可覆盖生成的展示视图，不作为事实源。
- 若 summary 或 PM view 与正式文档、ledger 冲突，以正式文档和 ledger 为准。

## 映射表

- `docs/01-getting-started/document-map.md` -> `.factory/memory/runtime-brief.md`
- `docs/01-getting-started/index.md` -> `.factory/memory/runtime-brief.md`
- `docs/01-getting-started/project-overview.md` -> `.factory/memory/runtime-brief.md`
- `docs/01-getting-started/quick-start.md` -> `.factory/memory/runtime-brief.md`
- `docs/02-user-guide/index.md` -> `.factory/memory/runtime-brief.md`
- `docs/02-user-guide/prompt-templates.md` -> `.factory/memory/runtime-brief.md`
- `docs/02-user-guide/user-guide.md` -> `.factory/memory/runtime-brief.md`
- `docs/03-developer-guide/application-development.md` -> `.factory/memory/runtime-brief.md`
- `docs/03-developer-guide/development-setup.md` -> `.factory/memory/runtime-brief.md`
- `docs/03-developer-guide/function-reference.md` -> `.factory/memory/runtime-brief.md`
- `docs/03-developer-guide/index.md` -> `.factory/memory/runtime-brief.md`
- `docs/03-developer-guide/interface-reference.md` -> `.factory/memory/runtime-brief.md`
- `docs/03-developer-guide/plugin-development.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/01-governance/index.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/01-governance/project-charter.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/02-discovery/brainstorm-record.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/02-discovery/hermes-agent-source-analysis-report.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/02-discovery/index.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/02-discovery/input.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/03-requirements/index.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/03-requirements/prd.md` -> `.factory/memory/prd.summary.md`, `.factory/memory/requirements-verification.summary.md`
- `docs/04-project-development/03-requirements/process-workflow-contract-requirements.md` -> `.factory/memory/tasks.summary.md`, `.factory/memory/skill-updates.summary.md`, `.factory/memory/runtime-brief.md`
- `docs/04-project-development/03-requirements/requirements-analysis.md` -> `.factory/memory/requirements-verification.summary.md`
- `docs/04-project-development/03-requirements/memory-system-business-requirements.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/03-requirements/requirements-verification.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/04-design/agent-platform-architecture.md` -> `.factory/memory/architecture.summary.md`, `.factory/memory/runtime-brief.md`
- `docs/04-project-development/04-design/ai-drama-production-skill-system.md` -> `.factory/memory/architecture.summary.md`, `.factory/memory/skill-updates.summary.md`
- `docs/04-project-development/04-design/basic-capability-layer-design.md` -> `.factory/memory/architecture.summary.md`, `.factory/memory/api.summary.md`
- `docs/04-project-development/04-design/infrastructure-layer-design.md` -> `.factory/memory/architecture.summary.md`, `.factory/memory/api.summary.md`
- `docs/04-project-development/04-design/memory-system-detailed-design.md` -> `.factory/memory/architecture.summary.md`, `.factory/memory/api.summary.md`
- `docs/04-project-development/04-design/memory-governance-design.md` -> `.factory/memory/architecture.summary.md`, `.factory/memory/api.summary.md`
- `docs/04-project-development/04-design/memory-runtime-design.md` -> `.factory/memory/architecture.summary.md`
- `docs/04-project-development/04-design/memory-runtime-interfaces.md` -> `.factory/memory/api.summary.md`
- `docs/04-project-development/04-design/memory-session-ledger-design.md` -> `.factory/memory/architecture.summary.md`
- `docs/04-project-development/04-design/memory-promotion-design.md` -> `.factory/memory/architecture.summary.md`
- `docs/04-project-development/04-design/memory-recall-design.md` -> `.factory/memory/architecture.summary.md`, `.factory/memory/api.summary.md`
- `docs/04-project-development/04-design/memory-distillation-learning-design.md` -> `.factory/memory/architecture.summary.md`
- `docs/04-project-development/04-design/api-design.md` -> `.factory/memory/api.summary.md`
- `docs/04-project-development/04-design/backend-design.md` -> `.factory/memory/architecture.summary.md`
- `docs/04-project-development/04-design/database-design.md` -> `.factory/memory/architecture.summary.md`
- `docs/04-project-development/04-design/deployment-architecture.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/04-design/evaluation-summary-and-approval-reporting.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/04-design/index.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/04-design/module-boundaries.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/04-design/solution-overview.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/04-design/system-architecture.md` -> `.factory/memory/architecture.summary.md`
- `docs/04-project-development/04-design/technical-selection.md` -> `.factory/memory/tech-stack.summary.md`
- `docs/04-project-development/04-design/ux-ui-design.md` -> `.factory/memory/ui.summary.md`, `.factory/memory/design-assets.summary.md`
- `docs/04-project-development/05-development-process/implementation-plan.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/05-development-process/memory-governance-implementation-plan.md` -> `.factory/memory/tasks.summary.md`, `.factory/memory/runtime-brief.md`
- `docs/04-project-development/05-development-process/process-workflow-contract-implementation-plan.md` -> `.factory/memory/tasks.summary.md`, `.factory/memory/skill-updates.summary.md`, `.factory/memory/runtime-brief.md`
- `docs/04-project-development/05-development-process/project-management-control-plane.md` -> `.factory/memory/tasks.summary.md`, `.factory/memory/current-state.md`
- `docs/04-project-development/05-development-process/superpowers-workflow-integration-plan.md` -> `.factory/memory/tasks.summary.md`, `.factory/memory/skill-updates.summary.md`, `.factory/memory/runtime-brief.md`
- `docs/04-project-development/05-development-process/index.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/05-development-process/software-development-process.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/06-testing-verification/index.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/06-testing-verification/test-plan.md` -> `.factory/memory/tests.summary.md`
- `docs/04-project-development/06-testing-verification/test-report.md` -> `.factory/memory/tests.summary.md`
- `docs/04-project-development/07-release-delivery/index.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/07-release-delivery/release-notes.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/08-operations-maintenance/deployment-guide.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/08-operations-maintenance/index.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/08-operations-maintenance/operations-runbook.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/09-evolution/agent-motivation-autonomy-integration.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/09-evolution/index.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/09-evolution/retrospective.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/09-evolution/skill-evolution-plan.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/10-traceability/document-index.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/10-traceability/index.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/10-traceability/interface-matrix.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-project-development/10-traceability/requirements-matrix.md` -> `.factory/memory/traceability.summary.md`, `.factory/memory/graph/traceability.json`
- `docs/04-project-development/index.md` -> `.factory/memory/runtime-brief.md`
- `docs/index.md` -> `.factory/memory/runtime-brief.md`
