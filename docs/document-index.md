# 文档索引与变更记录

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `TRACE-DOC-001` |
| 正式版本 | `v2.5.0` |
| 当前修订 | 无 |
| 来源候选 | `MODEL-ORCHESTRATOR-SELECTION-001` |
| 发布事务 | `N/A（本次索引同步不产生发布事务）` |
| 负责人 | `HUMAN_PROJECT_OWNER` |
| 修改 / 审核 / 批准 | `uroborus` / `uroborus` / `uroborus` |
| 状态 | 已批准并生效 |
| 上游 | `DOCS-IA-SHANFORGE-001`、`released event` |
| 下游 | `docs/index`、`doc-map`、`文档治理 Gate` |

## 目标文档登记

| 路径 | 文档 ID | 标题 | 类型 | Owner | 正式版本 |
|---|---|---|---|---|---|
| `docs/index.md` | `DOC-NAV-ROOT-001` | 文档总入口 | `navigation` | `HUMAN_PROJECT_OWNER` | `v1.2.0` |
| `docs/document-index.md` | `TRACE-DOC-001` | 文档索引与变更记录 | `traceability` | `HUMAN_PROJECT_OWNER` | `v2.5.0` |
| `docs/01-getting-started/index.md` | `DOC-NAV-GETTING-001` | 项目概览入口 | `navigation` | `HUMAN_PROJECT_OWNER` | `v1.0.0` |
| `docs/01-getting-started/project-overview.md` | `DOC-PROJECT-OVERVIEW-001` | 项目概览 | `guide` | `HUMAN_PROJECT_OWNER` | `v1.1.0` |
| `docs/01-getting-started/project-charter.md` | `DOC-PROJECT-CHARTER-001` | 项目章程 | `formal_baseline` | `HUMAN_PROJECT_OWNER` | `v3.0.0` |
| `docs/01-getting-started/quick-start.md` | `DOC-QUICK-START-001` | 快速开始 | `guide` | `HUMAN_DEVELOPMENT_EXECUTOR` | `v1.0.0` |
| `docs/02-user-guide/index.md` | `DOC-NAV-USER-001` | 用户指南入口 | `navigation` | `HUMAN_PRODUCT_ANALYST` | `v1.0.0` |
| `docs/02-user-guide/user-guide.md` | `DOC-USER-GUIDE-001` | 使用指南 | `guide` | `HUMAN_PRODUCT_ANALYST` | `v1.4.0` |
| `docs/02-user-guide/prompt-templates.md` | `DOC-PROMPT-GUIDE-001` | 提示词速查 | `guide` | `HUMAN_PRODUCT_ANALYST` | `v1.0.0` |
| `docs/03-developer-guide/index.md` | `DOC-NAV-DEVELOPER-001` | 开发者指南入口 | `navigation` | `HUMAN_ARCHITECTURE_DOMAIN_LEAD` | `v1.0.0` |
| `docs/03-developer-guide/development-setup.md` | `DOC-DEVELOPMENT-SETUP-001` | 开发环境 | `guide` | `HUMAN_DEVELOPMENT_EXECUTOR` | `v1.0.0` |
| `docs/03-developer-guide/application-development.md` | `DOC-APPLICATION-DEVELOPMENT-001` | 应用开发 | `guide` | `HUMAN_DEVELOPMENT_EXECUTOR` | `v1.0.0` |
| `docs/03-developer-guide/interface-reference.md` | `DOC-INTERFACE-REFERENCE-001` | 接口与函数参考 | `reference` | `HUMAN_API_INTEGRATION_LEAD` | `v2.0.0` |
| `docs/03-developer-guide/plugin-development.md` | `DOC-PLUGIN-DEVELOPMENT-001` | 插件开发 | `guide` | `HUMAN_DEVELOPMENT_EXECUTOR` | `v1.0.0` |
| `docs/04-product/index.md` | `DOC-NAV-PRODUCT-001` | 产品与需求入口 | `navigation` | `HUMAN_REQUIREMENTS_LEAD` | `v1.0.0` |
| `docs/04-product/prd.md` | `PRD-SHANFORGE-001` | 产品需求文档 | `formal_baseline` | `HUMAN_REQUIREMENTS_LEAD` | `v5.1.0` |
| `docs/04-product/requirements-matrix.md` | `TRACE-REQ-001` | 需求追踪矩阵 | `traceability` | `HUMAN_REQUIREMENTS_LEAD` | `v5.1.0` |
| `docs/05-design/index.md` | `DOC-NAV-DESIGN-001` | 软件技术设计入口 | `navigation` | `HUMAN_ARCHITECTURE_DOMAIN_LEAD` | `v1.3.0` |
| `docs/05-design/solution-overview.md` | `DESIGN-SOLUTION-001` | 总体方案与协作治理设计 | `formal_baseline` | `HUMAN_ARCHITECTURE_DOMAIN_LEAD` | `v4.0.0` |
| `docs/05-design/technical-selection.md` | `DESIGN-TECH-001` | 技术选型与工程规则 | `formal_baseline` | `HUMAN_ARCHITECTURE_DOMAIN_LEAD` | `v4.0.0` |
| `docs/05-design/system-architecture.md` | `DESIGN-ARCH-001` | Skill-first 系统架构 | `formal_baseline` | `HUMAN_ARCHITECTURE_DOMAIN_LEAD` | `v4.0.0` |
| `docs/05-design/module-domain-design.md` | `DESIGN-MODULE-001` | 模块与领域设计 | `formal_baseline` | `HUMAN_ARCHITECTURE_DOMAIN_LEAD` | `v4.0.0` |
| `docs/05-design/data-design.md` | `DESIGN-DATA-001` | 数据与存储设计 | `formal_baseline` | `HUMAN_DATABASE_LEAD` | `v2.1.0` |
| `docs/05-design/api-design.md` | `DESIGN-API-001` | 接口与事件设计 | `formal_baseline` | `HUMAN_API_INTEGRATION_LEAD` | `v4.0.0` |
| `docs/05-design/frontend-design.md` | `DESIGN-FRONTEND-001` | 前端架构与页面设计 | `formal_baseline` | `HUMAN_DEVELOPMENT_EXECUTOR` | `v2.0.0` |
| `docs/05-design/ux-ui-design.md` | `DESIGN-UX-UI-001` | 用户体验、交互与 UI 设计 | `formal_baseline` | `HUMAN_UX_LEAD` | `v2.0.0` |
| `docs/05-design/workflow-execution-design.md` | `PROC-TASK-EXECUTION-001` | 会话、任务与工作流执行设计 | `formal_baseline` | `HUMAN_PROJECT_OWNER` | `v2.1.0` |
| `docs/05-design/memory-design.md` | `DESIGN-MEMORY-001` | 记忆系统设计 | `formal_baseline` | `HUMAN_ARCHITECTURE_DOMAIN_LEAD` | `v4.0.0` |
| `docs/05-design/interface-matrix.md` | `TRACE-API-001` | 接口与字段追踪矩阵 | `traceability` | `HUMAN_API_INTEGRATION_LEAD` | `v4.0.0` |
| `docs/06-delivery/index.md` | `DOC-NAV-DELIVERY-001` | 质量、发布与运维入口 | `navigation` | `HUMAN_RELEASE_OPERATIONS_LEAD` | `v1.2.0` |
| `docs/06-delivery/test-plan.md` | `TEST-PLAN-001` | 测试策略与质量门 | `formal_baseline` | `HUMAN_QUALITY_SECURITY_LEAD` | `v3.3.0` |
| `docs/06-delivery/test-cases.md` | `TEST-CATALOG-SHANFORGE-001` | Shanforge 正式测试案例目录 | `test_catalog` | `HUMAN_QUALITY_SECURITY_LEAD` | `v1.1.0` |
| `docs/06-delivery/release-notes.md` | `RELEASE-NOTES-001` | 发布说明 | `formal_baseline` | `HUMAN_RELEASE_OPERATIONS_LEAD` | `v3.1.0` |
| `docs/06-delivery/deployment-guide.md` | `OPS-DEPLOYMENT-GUIDE-001` | Skill 交付手册 | `formal_baseline` | `HUMAN_RELEASE_OPERATIONS_LEAD` | `v4.0.0` |
| `docs/06-delivery/operations-runbook.md` | `OPS-RUNBOOK-001` | 运维手册 | `formal_baseline` | `HUMAN_RELEASE_OPERATIONS_LEAD` | `v4.0.0` |

## 68 个正式前像处置

| 原路径 | 处置 | 当前 owner | 原因 |
|---|---|---|---|
| `docs/01-getting-started/document-map.md` | `conditional_retire_after_integrated_formal_release` | `docs/index.md`<br>`docs/document-index.md` | 旧文档地图并入六类根入口和唯一文档索引 |
| `docs/01-getting-started/index.md` | `retain_and_integrate_registered_owner` | `docs/01-getting-started/index.md` | 保留为目标树中的登记 owner 或导航、策略文件 |
| `docs/01-getting-started/project-overview.md` | `retain_and_integrate_registered_owner` | `docs/01-getting-started/project-overview.md` | 保留为目标树中的登记 owner 或导航、策略文件 |
| `docs/01-getting-started/quick-start.md` | `retain_and_integrate_registered_owner` | `docs/01-getting-started/quick-start.md` | 保留为目标树中的登记 owner 或导航、策略文件 |
| `docs/02-user-guide/index.md` | `retain_and_integrate_registered_owner` | `docs/02-user-guide/index.md` | 保留为目标树中的登记 owner 或导航、策略文件 |
| `docs/02-user-guide/prompt-templates.md` | `retain_and_integrate_registered_owner` | `docs/02-user-guide/prompt-templates.md` | 保留为目标树中的登记 owner 或导航、策略文件 |
| `docs/02-user-guide/user-guide.md` | `retain_and_integrate_registered_owner` | `docs/02-user-guide/user-guide.md` | 保留为目标树中的登记 owner 或导航、策略文件 |
| `docs/03-developer-guide/application-development.md` | `retain_and_integrate_registered_owner` | `docs/03-developer-guide/application-development.md` | 保留为目标树中的登记 owner 或导航、策略文件 |
| `docs/03-developer-guide/development-setup.md` | `retain_and_integrate_registered_owner` | `docs/03-developer-guide/development-setup.md` | 保留为目标树中的登记 owner 或导航、策略文件 |
| `docs/03-developer-guide/function-reference.md` | `conditional_retire_after_integrated_formal_release` | `docs/03-developer-guide/interface-reference.md` | 函数与接口共同由一个稳定参考页负责 |
| `docs/03-developer-guide/index.md` | `retain_and_integrate_registered_owner` | `docs/03-developer-guide/index.md` | 保留为目标树中的登记 owner 或导航、策略文件 |
| `docs/03-developer-guide/interface-reference.md` | `retain_and_integrate_registered_owner` | `docs/03-developer-guide/interface-reference.md` | 保留为目标树中的登记 owner 或导航、策略文件 |
| `docs/03-developer-guide/plugin-development.md` | `retain_and_integrate_registered_owner` | `docs/03-developer-guide/plugin-development.md` | 保留为目标树中的登记 owner 或导航、策略文件 |
| `docs/04-project-development/01-governance/index.md` | `conditional_retire_after_integrated_formal_release` | `docs/01-getting-started/index.md` | 治理导航并入项目概览入口 |
| `docs/04-project-development/01-governance/project-charter.md` | `conditional_retire_after_integrated_formal_release` | `docs/01-getting-started/project-charter.md` | 项目章程移到项目概览模块，内容和文档 ID 延续 |
| `docs/04-project-development/02-discovery/hermes-agent-source-analysis-report.md` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/solution-overview.md` | 长篇源码调研作为历史任务证据归档，已采用结论进入总体设计 |
| `docs/04-project-development/02-discovery/index.md` | `conditional_retire_after_integrated_formal_release` | `docs/04-product/index.md`<br>`docs/05-design/index.md` | 调研过程不再设正式目录；结论分别融入需求或设计，原始材料进入 WorkItem |
| `docs/04-project-development/03-requirements/index.md` | `conditional_retire_after_integrated_formal_release` | `docs/04-product/index.md` | 需求入口迁移到独立产品模块 |
| `docs/04-project-development/03-requirements/prd.md` | `conditional_retire_after_integrated_formal_release` | `docs/04-product/prd.md` | PRD 迁移到独立产品模块，文档 ID 延续 |
| `docs/04-project-development/03-requirements/requirements-analysis.md` | `conditional_retire_after_integrated_formal_release` | `docs/04-product/prd.md` | 分析结论必须融合进正式 PRD，不保留补丁页 |
| `docs/04-project-development/03-requirements/requirements-verification.md` | `conditional_retire_after_integrated_formal_release` | `docs/04-product/requirements-matrix.md` | 某次验证结果进入 WorkItem evidence，稳定关系由需求追踪矩阵负责 |
| `docs/04-project-development/04-design/agent-platform-architecture.md` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/system-architecture.md` | 平台架构与系统架构重复且保留旧分层表达 |
| `docs/04-project-development/04-design/ai-drama-production-skill-system.md` | `conditional_retire_after_integrated_formal_release` | - | 专题业务方案不属于当前 shanforge 核心正式基线，无活跃 owner |
| `docs/04-project-development/04-design/api-design.md` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/api-design.md` | 接口设计迁移到独立技术设计模块，文档 ID 延续 |
| `docs/04-project-development/04-design/assets/v2-architecture-pages/01-系统分层总览.drawio` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/system-architecture.md` | 旧架构图被当前系统架构和机器追踪取代 |
| `docs/04-project-development/04-design/assets/v2-architecture-pages/02-平台核心能力分解.drawio` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/system-architecture.md` | 旧架构图被当前系统架构和机器追踪取代 |
| `docs/04-project-development/04-design/assets/v2-architecture-pages/03-业务运行链路图.drawio` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/system-architecture.md` | 旧架构图被当前系统架构和机器追踪取代 |
| `docs/04-project-development/04-design/assets/v2-architecture-pages/04-功能模块清单图.drawio` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/system-architecture.md` | 旧架构图被当前系统架构和机器追踪取代 |
| `docs/04-project-development/04-design/assets/v2-architecture-pages/05-数据与存储架构图.drawio` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/system-architecture.md` | 旧架构图被当前系统架构和机器追踪取代 |
| `docs/04-project-development/04-design/assets/v2-architecture-pages/06-层间依赖图.drawio` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/system-architecture.md` | 旧架构图被当前系统架构和机器追踪取代 |
| `docs/04-project-development/04-design/assets/v2-architecture-pages/07-分层接口总表图.drawio` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/system-architecture.md` | 旧架构图被当前系统架构和机器追踪取代 |
| `docs/04-project-development/04-design/assets/v2-architecture-pages/08-子系统定义图.drawio` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/system-architecture.md` | 旧架构图被当前系统架构和机器追踪取代 |
| `docs/04-project-development/04-design/assets/v2-architecture-pages/09-记忆系统跨层调用图.drawio` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/system-architecture.md` | 旧架构图被当前系统架构和机器追踪取代 |
| `docs/04-project-development/04-design/assets/v2-architecture-views.drawio` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/system-architecture.md` | 旧合并架构图被当前系统架构取代 |
| `docs/04-project-development/04-design/index.md` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/index.md` | 技术设计改为独立顶层入口 |
| `docs/04-project-development/04-design/infrastructure-layer-design.md` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/system-architecture.md`<br>`docs/05-design/data-design.md` | 基础设施边界并入系统架构，存储部分进入数据设计 |
| `docs/04-project-development/04-design/layered-domain-interface-catalog.md` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/module-domain-design.md`<br>`docs/05-design/api-design.md`<br>`docs/05-design/interface-matrix.md` | 层与模块进入模块领域设计，接口和字段关系进入接口设计与追踪矩阵 |
| `docs/04-project-development/04-design/memory-distillation-learning-design.md` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/memory-design.md` | 蒸馏与学习并入唯一记忆系统设计 |
| `docs/04-project-development/04-design/memory-promotion-design.md` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/memory-design.md` | 晋升规则并入唯一记忆系统设计 |
| `docs/04-project-development/04-design/memory-recall-design.md` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/memory-design.md` | 召回规则并入唯一记忆系统设计 |
| `docs/04-project-development/04-design/memory-runtime-design.md` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/memory-design.md` | 记忆运行时与领域接口合并成一份记忆系统设计 |
| `docs/04-project-development/04-design/memory-runtime-interfaces.md` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/memory-design.md`<br>`docs/05-design/interface-matrix.md` | 记忆端口进入记忆系统设计，接口关系进入追踪矩阵 |
| `docs/04-project-development/04-design/memory-session-ledger-design.md` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/memory-design.md`<br>`docs/05-design/workflow-execution-design.md` | 会话账本由记忆系统和工作流执行设计共同负责 |
| `docs/04-project-development/04-design/memory-system-detailed-design.md` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/memory-design.md` | 旧详细方案含过时骨架，稳定内容并入唯一记忆系统设计 |
| `docs/04-project-development/04-design/module-boundaries.md` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/module-domain-design.md` | 模块边界扩展为模块、领域和纵向业务流设计 |
| `docs/04-project-development/04-design/solution-overview.md` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/solution-overview.md` | 总体方案迁移到独立技术设计模块，文档 ID 延续 |
| `docs/04-project-development/04-design/system-architecture.md` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/system-architecture.md` | 系统架构迁移到独立技术设计模块，文档 ID 延续 |
| `docs/04-project-development/04-design/technical-selection.md` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/technical-selection.md` | 技术选型迁移到独立技术设计模块，文档 ID 延续 |
| `docs/04-project-development/04-design/v2-architecture-pages.md` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/system-architecture.md` | 旧架构图索引被当前系统架构取代 |
| `docs/04-project-development/05-development-process/implementation-plan.md` | `conditional_retire_after_integrated_formal_release` | - | 实施计划是具体 WorkItem 的执行材料，后续只允许保存于 .factory/workitems/<WORKITEM-ID>/plan.md |
| `docs/04-project-development/05-development-process/index.md` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/workflow-execution-design.md` | 正式设计只保留执行规则；项目过程入口和当前状态归 WorkItem |
| `docs/04-project-development/05-development-process/task-execution-contract.md` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/workflow-execution-design.md` | 稳定执行规则迁移到技术设计，单任务状态仍留在 .factory |
| `docs/04-project-development/06-testing-verification/index.md` | `conditional_retire_after_integrated_formal_release` | `docs/06-delivery/index.md` | 测试入口并入质量与交付模块 |
| `docs/04-project-development/06-testing-verification/test-plan.md` | `conditional_retire_after_integrated_formal_release` | `docs/06-delivery/test-plan.md` | 稳定测试策略迁移到质量与交付模块 |
| `docs/04-project-development/06-testing-verification/test-report.md` | `conditional_retire_after_integrated_formal_release` | `docs/06-delivery/test-plan.md` | 某轮测试结果进入 WorkItem evidence，不作为长期正式页 |
| `docs/04-project-development/07-release-delivery/index.md` | `conditional_retire_after_integrated_formal_release` | `docs/06-delivery/index.md` | 发布入口并入质量与交付模块 |
| `docs/04-project-development/07-release-delivery/release-notes.md` | `conditional_retire_after_integrated_formal_release` | `docs/06-delivery/release-notes.md` | 发布说明迁移到统一交付模块 |
| `docs/04-project-development/08-operations-maintenance/deployment-guide.md` | `conditional_retire_after_integrated_formal_release` | `docs/06-delivery/deployment-guide.md` | 部署手册迁移到统一交付模块 |
| `docs/04-project-development/08-operations-maintenance/index.md` | `conditional_retire_after_integrated_formal_release` | `docs/06-delivery/index.md` | 运维入口并入质量与交付模块 |
| `docs/04-project-development/08-operations-maintenance/operations-runbook.md` | `conditional_retire_after_integrated_formal_release` | `docs/06-delivery/operations-runbook.md` | 运维手册迁移到统一交付模块 |
| `docs/04-project-development/09-evolution/index.md` | `conditional_retire_after_integrated_formal_release` | - | 复盘和演进提案属于 WorkItem；批准后的稳定变化直接修改原正式 owner 文档 |
| `docs/04-project-development/10-traceability/document-index.md` | `conditional_retire_after_integrated_formal_release` | `docs/document-index.md` | 文档索引迁移到根入口，便于所有维护者查找 |
| `docs/04-project-development/10-traceability/index.md` | `conditional_retire_after_integrated_formal_release` | `docs/document-index.md`<br>`docs/04-product/requirements-matrix.md`<br>`docs/05-design/interface-matrix.md` | 三份追踪材料分别放到文档根、产品需求和技术设计，不再单建目录 |
| `docs/04-project-development/10-traceability/interface-matrix.md` | `conditional_retire_after_integrated_formal_release` | `docs/05-design/interface-matrix.md` | 接口矩阵升级为数据、接口、页面和 UI 字段追踪矩阵 |
| `docs/04-project-development/10-traceability/requirements-matrix.md` | `conditional_retire_after_integrated_formal_release` | `docs/04-product/requirements-matrix.md` | 需求追踪矩阵迁移到产品需求模块 |
| `docs/04-project-development/index.md` | `conditional_retire_after_integrated_formal_release` | `docs/index.md`<br>`docs/04-product/index.md`<br>`docs/05-design/index.md`<br>`docs/06-delivery/index.md` | 取消混合项目开发目录，稳定事实分流到产品、技术设计和交付入口 |
| `docs/index.md` | `retain_and_integrate_registered_owner` | `docs/index.md` | 保留为目标树中的登记 owner 或导航、策略文件 |
| `docs/publication-policy.json` | `moved_machine_config_out_of_docs` | `.factory/catalog/document-publication-policy.json` | docs 只保留人类文档；机器发布策略进入稳定 Catalog 配置 |

## 发布记录

| 日期 | 任务 | 候选 | 事务 | 结果 | 批准 |
|---|---|---|---|---|---|
| 2026-07-18 | `TASK-DESIGN-001` | `TASK-DESIGN-001-R019` | `DESIGN-RELEASE-TX-R019-G001` | 37 文件 / 7 目录正式设计基线 | `uroborus` |
| 2026-07-22 | `TASK-IMPLEMENT-003` | `TASK-IMPLEMENT-003-P001` | `PROJECT-KNOWLEDGE-ACTIVATION-T06` | 34 份人类 Markdown；机器 JSON 移至 `.factory/catalog` 或 WorkItem evidence | `uroborus` |

## 维护规则

正式事实优先写入登记的唯一 owner；新增 Markdown 默认拒绝。候选、评审、evidence、ledger 和机器配置不进入 `docs/`。

## 正式版本历史（仅已发布）

| 版本 | 日期 | 变更内容 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v2.5.0` | 2026-09-08 | 同步主会话模型解耦相关正式文档版本与来源 | `AI_EXECUTOR` | 集中质量门 | `uroborus` |
| `v2.4.0` | 2026-09-01 | 同步生命周期基线、T02 设计版本及交付文档控制版本 | `AI_EXECUTOR` | 集中质量门 | `uroborus` |
| `v2.3.0` | 2026-08-23 | 正式登记测试案例目录、测试计划与交付导航新版本 | `AI_EXECUTOR` | 独立 Reviewer | `uroborus` |
| `v2.2.0` | 2026-07-28 | 登记 skill-first 架构与 skill 自带快照入口 | `uroborus` | `uroborus` | `uroborus` |
| `v2.0.0` | 2026-07-18 | 发布重构后的文档索引与前像处置 | `uroborus` | `uroborus` | `uroborus` |
| `v2.1.0` | 2026-07-22 | 登记 34 份人类文档，移出机器 JSON，并同步项目知识设计版本 | `uroborus` | `uroborus` | `uroborus` |
