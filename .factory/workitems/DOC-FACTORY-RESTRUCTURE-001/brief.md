# DOC-FACTORY-RESTRUCTURE-001 Brief

## 当前状态

- 工作项状态：`completed_superseded_by_formal_baseline`
- 收口日期：2026-07-23
- 收口结论：原迁移任务已完成；`TASK-002` 的旧目录草案已被后续正式 PRD、设计基线和项目知识实现取代，不再执行旧草案中的第二次目录迁移。
- 当前事实源：`docs/index.md`、`docs/document-index.md`、`docs/04-product/prd.md`、`docs/05-design/solution-overview.md`、`docs/05-design/workflow-execution-design.md`、`docs/05-design/memory-design.md`。

## 目标

将 `docs/04-project-development` 和 `.factory` 改造为破坏性重做型全量文档结构迁移：删除旧资产、旧结构、旧过程页和旧生成内容，只保留当前正式文档、必要设计资产、执行审计事实和最新恢复摘要。

## 非目标

- 不迁移、删除或重命名历史 work item 的 evidence、reports、reviews 或 ledger。
- 不修改业务代码。
- 不把当前作者自检写成独立 review approved。
- 不恢复旧中心命令、动作注册表、`factory-*` 或旧全局流程脚本。

## 背景与当前状态

`docs/04-project-development` 已有 10 个阶段目录，但混有旧调研输入、旧需求、旧设计专题、旧流程集成方案、旧演进材料和旧静态原型。`.factory` 同时存在当前 memory/workitem/PM 事实和旧 process、旧 generated、旧 history 快照。用户已明确要求旧资产旧结构都删除，只保留最新正式资产和正式内容；正式文档不得署名为 `Codex`。

## 已批准方案

采用破坏性全量迁移：

- 新增并登记 `docs/04-project-development/05-development-process/task-execution-contract.md`。
- 将 `docs/04-project-development/04-design/assets/v2-architecture-pages/index.md` 迁移为正式页面 `docs/04-project-development/04-design/v2-architecture-pages.md`，让 `assets/` 只保留 draw.io 资产。
- 删除旧 discovery / requirements / design / development-process / evolution 页面和旧静态原型。
- 删除 `.factory/process/`、`.factory/memory/history/`、`.factory/pm/generated/`、空资产索引和临时备份资产。
- 重写根导航、目录首页、文档索引、追踪矩阵和 `.factory/memory/doc-map.md`，仅保留存在的正式路径。
- 新增 `.factory/README.md`，固化破坏性迁移规则、事实边界和 work item 标准结构。
- 创建本 work item 的标准 brief、plan、task brief、evidence、reports、reviews 和 ledger。
- 增加结构测试固定新契约、删除清单、无断链和无错误署名。

## 成功标准

- 新任务执行契约在根导航、项目开发首页、开发过程首页、文档索引和 doc-map 中可追踪。
- `docs/04-project-development` 的正式入口不再引用已删除文档。
- `.factory` 根目录职责、事实边界和破坏性迁移规则明确。
- 旧结构目录和旧生成资产被物理删除。
- 正式文档版本历史和执行人字段不署名为 `Codex`。
- 结构测试、文档校验和 `git diff --check` 有新鲜结果。

## 影响范围

- `docs/index.md`
- `docs/04-project-development/index.md`
- `docs/04-project-development/02-discovery/hermes-agent-source-analysis-report.md`
- `docs/04-project-development/04-design/index.md`
- `docs/04-project-development/04-design/v2-architecture-pages.md`
- `docs/04-project-development/04-design/solution-overview.md`
- `docs/04-project-development/04-design/memory-system-detailed-design.md`
- `docs/04-project-development/05-development-process/index.md`
- `docs/04-project-development/05-development-process/implementation-plan.md`
- `docs/04-project-development/05-development-process/task-execution-contract.md`
- `docs/04-project-development/06-testing-verification/test-report.md`
- `docs/04-project-development/10-traceability/document-index.md`
- `docs/04-project-development/10-traceability/requirements-matrix.md`
- `.factory/README.md`
- `.factory/project.json`
- `.factory/tech-profile.json`
- `.factory/multi-agent-board.json`
- `.factory/memory/doc-map.md`
- `.factory/memory/tasks.summary.md`
- `.factory/memory/current-state.md`
- `.factory/memory/tests.summary.md`
- `.factory/workitems/implementation/README.md`
- `.factory/workitems/DOC-FACTORY-RESTRUCTURE-001/`
- `tests/test_doc_factory_restructure.py`

## 删除范围

- 旧 04 项目开发文档页面和旧静态原型。
- `.factory/process/`
- `.factory/memory/history/`
- `.factory/pm/generated/`
- `.factory/design-assets.json`
- draw.io 临时备份文件。

## 未决问题

- 无。本工作项的历史草案和执行证据保留在原 WorkItem 中，仅作审计，不再作为当前目录基线。
