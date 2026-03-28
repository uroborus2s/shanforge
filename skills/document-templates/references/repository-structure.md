# 推荐文档目录结构

## 设计原则

- 按生命周期分层，方便阶段性交付与审查。
- 把“架构说明”和“接口契约文件”放在同一阶段目录，方便联查。
- 把“发布/部署”和“运行/支持”分开，避免上线前文档与长期运维文档混杂。
- 把“用户指南”和“管理员/实施指南”分开，避免不同读者互相干扰。
- `docs/index.md` 作为人类入口页，供仓内阅读和 `docs-stratego` 聚合站点共同复用。
- 根 `docs/index.md` 是唯一的导航清单文件，用 YAML front matter 中的 `mkdocs.home_access` 和 `mkdocs.nav` 声明全站目录树、页面路径和页面权限。
- `docs/` 下每个文档目录仍保留自己的 `index.md`，但它们只作为正文首页和资源权限锚点，不再声明 `mkdocs.nav`。
- 仓内链接统一使用相对路径，不写机器绝对路径。

## 推荐目录

```text
docs/
├── index.md
├── 00-governance/
│   ├── index.md
│   ├── project-charter.md
│   ├── stakeholders-raci.md
│   ├── risk-register.md
│   ├── glossary.md
│   └── roadmap.md
├── 01-discovery/
│   ├── index.md
│   ├── input.md
│   ├── brainstorm-record.md
│   ├── current-state-analysis.md
│   ├── business-flow.md
│   └── scope-outline.md
├── 02-requirements/
│   ├── index.md
│   ├── prd.md
│   ├── requirements-analysis.md
│   ├── requirements-verification.md
│   ├── nfr-catalog.md
│   ├── acceptance-criteria.md
│   └── change-requests.md
├── 03-solution/
│   ├── index.md
│   ├── technical-selection.md
│   ├── system-architecture.md
│   ├── module-boundaries.md
│   ├── api-design.md
│   ├── backend-design.md
│   ├── database-design.md
│   ├── security-design.md
│   ├── deployment-architecture.md
│   ├── ux-ui-design.md
│   ├── assets/
│   ├── adr/
│   │   ├── index.md
│   │   └── ADR-001-<title>.md
│   └── contracts/
│       ├── index.md
│       ├── api/
│       │   ├── index.md
│       │   └── openapi.yaml
│       ├── events/
│       │   ├── index.md
│       │   ├── event-overview.md
│       │   ├── asyncapi.yaml
│       │   └── schemas/
│       └── internal/
│           ├── index.md
│           ├── interface-catalog.md
│           └── schemas/
├── 04-delivery/
│   ├── index.md
│   ├── wbs.md
│   ├── implementation-plan.md
│   ├── task-breakdown.md
│   ├── iteration-plan.md
│   ├── migration-plan.md
│   ├── execution-log.md
│   ├── daily-status.md
│   ├── risk-register.md
│   ├── multi-agent-board.md
│   ├── role-assignments.md
│   ├── role-handoffs.md
│   ├── role-sync.md
│   ├── team-sync.md
│   ├── chat-bootstrap.md
│   ├── pull-requests.md
│   ├── pr-board.md
│   ├── pr-handovers.md
│   ├── remote-prs.md
│   ├── role-retrospectives/
│   │   ├── index.md
│   │   └── README.md
│   ├── team-retro.md
│   └── dev-setup.md
├── 05-quality/
│   ├── index.md
│   ├── test-strategy.md
│   ├── test-plan.md
│   ├── test-cases.md
│   ├── test-data.md
│   ├── defect-log.md
│   ├── test-report.md
│   └── uat-report.md
├── 06-release/
│   ├── index.md
│   ├── acceptance-checklist.md
│   ├── pr-check-report.md
│   ├── stage-check-report.md
│   ├── quality-check-report.md
│   ├── state-doctor-report.md
│   ├── delivery-package.md
│   ├── release-checklist.md
│   ├── release-notes.md
│   ├── rollback-plan.md
│   ├── production-readiness-review.md
│   ├── role-reviews.md
│   ├── role-closeouts.md
│   └── team-closeouts.md
├── 07-operations/
│   ├── index.md
│   ├── deployment-guide.md
│   ├── operations-runbook.md
│   ├── monitoring-alerting.md
│   ├── incident-playbook.md
│   ├── backup-dr.md
│   ├── support-handbook.md
│   └── configuration-matrix.md
├── 08-handover/
│   ├── index.md
│   ├── user-guide.md
│   ├── admin-guide.md
│   ├── training-guide.md
│   ├── faq-troubleshooting.md
│   └── handover-memo.md
├── 09-evolution/
│   ├── index.md
│   ├── retrospective.md
│   ├── postmortem.md
│   └── deprecation-plan.md
├── traceability/
│   ├── index.md
│   ├── requirements-matrix.md
│   ├── interface-matrix.md
│   └── document-index.md
└── .factory/
    ├── project.json
    ├── memory/
    │   ├── project-index.md
    │   ├── requirements.summary.md
    │   ├── architecture.summary.md
    │   ├── interfaces.summary.md
    │   ├── release.summary.md
    │   └── operations.summary.md
    ├── process/
    │   ├── execution-log.md
    │   ├── stage-check-report.md
    │   └── quality-check-report.md
    └── workitems/
        ├── implementation/
        ├── changes/
        └── bugs/
```

## 各目录的作用

### `00-governance/`

放管理者和项目负责人最早需要看的材料。这里回答“为什么做、谁负责、边界在哪”。

### `01-discovery/`

放调研和问题空间材料。这里回答“现在是什么样、问题是什么、有哪些候选方案”。

### `02-requirements/`

放已经确认的需求、验收标准和变更控制材料。这里回答“系统必须做什么、什么算完成”。

### `03-solution/`

放技术方案和边界文档。这里回答“准备怎么做、模块怎么拆、接口怎么约束、数据怎么流转”。

### `04-delivery/`

放实施组织材料。这里回答“先做什么、谁来做、分几波做、怎么落地”。

### `05-quality/`

放测试策略、执行结果和质量结论。这里回答“怎么验证、验证到了什么程度、剩下什么风险”。

### `06-release/`

放发布动作本身的材料。这里回答“何时发、发什么、失败怎么办”。

### `07-operations/`

放系统上线后的运行材料。这里回答“怎么部署、怎么监控、出问题怎么办、谁来支持”。

### `08-handover/`

放最终给用户、管理员、实施和支持团队阅读的内容。这里回答“怎么用、怎么管、怎么交接”。

### `09-evolution/`

放长期演进材料，如复盘、事故总结和退役计划。这里回答“后续如何改进、如何退出”。

### `traceability/`

放跨阶段引用关系。这里不要堆正文，而是放索引、矩阵和覆盖视图。

### `docs/index.md`

放项目文档首页，面向人类读者解释：

- 文档区覆盖哪些阶段
- 每个分区解决什么问题
- 与 `docs-stratego` 聚合站点的关系
- 根目录 `mkdocs.nav` 如何把各级目录和页面按中文名组织出来

### 各目录 `index.md`

每个文档目录都要有自己的 `index.md`，至少包含：

- 一个一级标题 `# 标题`
- 目录说明
- 推荐阅读顺序或页面分组提示

这些目录首页只负责承载目录正文，不再声明导航树；实际左侧目录和页面权限全部来自根 `docs/index.md`。
`assets/` 目录只能放资源文件，不能放 Markdown 页面。

### `.factory/`

放隐藏的控制面资产。这里统一容纳 AI 压缩记忆、过程文档、工作项、运行状态和协作中间产物，不替代正式文档。

### `.factory/memory/`

放 AI 友好的压缩摘要、索引和图谱，用来减少运行时上下文成本。

### `.factory/process/`

放执行日志、检查报告、协作看板、角色交接和其他过程控制文档。

### `.factory/workitems/`

放 `TASK`、`CR`、`BUG` 等过程执行单元。

## 组织规则

### 1. 接口目录与契约文件并存

如果项目存在对外 API、事件流、内部 RPC 或跨服务接口：

- 在 `03-solution/contracts/` 中同时放阅读说明和机器契约
- 说明文档先解释业务语义、调用边界、依赖关系
- 契约文件再承载字段级定义

### 2. 高风险项目增加专门子目录

以下情况建议在相应阶段下增设子目录：

- 安全敏感：`03-solution/security/`
- 数据迁移复杂：`04-delivery/migrations/`
- 多环境复杂：`07-operations/environments/`
- 合规要求强：`00-governance/compliance/`

### 3. 不创建空目录来假装完整

只在当前项目确实需要该阶段内容时创建目录和文档。目录结构是推荐骨架，不是强制一次性铺满。

## 初始化建议

初始化文档体系时，先创建以下目录与文件：

- `docs/index.md`
- `docs/04-project-development/01-governance/index.md`
- `docs/04-project-development/02-discovery/index.md`
- `docs/04-project-development/03-requirements/index.md`
- `docs/04-project-development/04-design/index.md`
- `docs/04-project-development/05-development-process/index.md`
- `docs/04-project-development/06-testing-verification/index.md`
- `docs/04-project-development/07-release-delivery/index.md`
- `docs/04-project-development/08-operations-maintenance/index.md`
- `docs/02-user-guide/index.md`
- `docs/04-project-development/09-evolution/index.md`
- `docs/04-project-development/10-traceability/index.md`
- `00-governance/project-charter.md`
- `01-discovery/input.md`
- `01-discovery/brainstorm-record.md`
- `02-requirements/prd.md`
- `02-requirements/requirements-verification.md`
- `03-solution/technical-selection.md`
- `03-solution/system-architecture.md`
- `03-solution/module-boundaries.md`
- `03-solution/api-design.md`
- `04-delivery/implementation-plan.md`
- `.factory/process/execution-log.md`
- `05-quality/test-plan.md`
- `06-release/release-notes.md`
- `07-operations/deployment-guide.md`
- `08-handover/user-guide.md`
- `traceability/requirements-matrix.md`
