# 推荐文档目录结构

## 设计原则

- 顶层按 4 大模块单轴组织，不再把生命周期目录直接铺在 `docs/` 根下。
- 公开稳定说明和内部项目过程文档分层维护。
- 根 `docs/index.md` 是唯一导航与权限事实源。
- 子目录 `index.md` 只做正文首页和目录边界说明。
- 稳定公共接口尽量放在 `03-developer-guide/`；内部设计期契约放在 `04-project-development/04-design/contracts/`。
- 仓内链接统一使用相对路径，不写机器绝对路径。

## 推荐目录

```text
docs/
├── index.md
├── 01-getting-started/
│   ├── index.md
│   ├── project-overview.md
│   ├── quick-start.md
│   └── document-map.md
├── 02-user-guide/
│   ├── index.md
│   ├── user-guide.md
│   ├── admin-guide.md
│   ├── installation.md
│   ├── configuration.md
│   ├── usage.md
│   └── prompt-templates.md
├── 03-developer-guide/
│   ├── index.md
│   ├── application-development.md
│   ├── development-setup.md
│   ├── function-reference.md
│   ├── interface-reference.md
│   ├── plugin-development.md
│   ├── openapi/
│   │   ├── index.md
│   │   └── public-v1.openapi.yaml
│   └── tools/
│       ├── index.md
│       └── public-agent.mcp-tools.yaml
├── 04-project-development/
│   ├── index.md
│   ├── 01-governance/
│   │   ├── index.md
│   │   ├── project-charter.md
│   │   ├── stakeholders-raci.md
│   │   ├── risk-register.md
│   │   ├── glossary.md
│   │   └── roadmap.md
│   ├── 02-discovery/
│   │   ├── index.md
│   │   └── hermes-agent-source-analysis-report.md
│   ├── 03-requirements/
│   │   ├── index.md
│   │   ├── prd.md
│   │   ├── requirements-analysis.md
│   │   ├── requirements-verification.md
│   │   ├── changelog.md
│   │   ├── nfr-catalog.md
│   │   ├── acceptance-criteria.md
│   │   └── change-requests.md
│   ├── 04-design/
│   │   ├── index.md
│   │   ├── solution-overview.md
│   │   ├── technical-selection.md
│   │   ├── system-architecture.md
│   │   ├── agent-platform-architecture.md
│   │   ├── layered-domain-interface-catalog.md
│   │   ├── module-boundaries.md
│   │   ├── infrastructure-layer-design.md
│   │   ├── api-design.md
│   │   ├── memory-runtime-design.md
│   │   ├── memory-system-detailed-design.md
│   │   ├── memory-runtime-interfaces.md
│   │   ├── memory-session-ledger-design.md
│   │   ├── memory-promotion-design.md
│   │   ├── memory-recall-design.md
│   │   ├── memory-distillation-learning-design.md
│   │   ├── ai-drama-production-skill-system.md
│   │   ├── v2-architecture-pages.md
│   │   └── assets/
│   ├── 05-development-process/
│   │   ├── index.md
│   │   ├── implementation-plan.md
│   │   └── task-execution-contract.md
│   ├── 06-testing-verification/
│   │   ├── index.md
│   │   ├── test-plan.md
│   │   ├── test-report.md
│   ├── 07-release-delivery/
│   │   ├── index.md
│   │   ├── release-notes.md
│   ├── 08-operations-maintenance/
│   │   ├── index.md
│   │   ├── deployment-guide.md
│   │   └── operations-runbook.md
│   ├── 09-evolution/
│   │   └── index.md
│   └── 10-traceability/
│       ├── index.md
│       ├── requirements-matrix.md
│       ├── interface-matrix.md
│       └── document-index.md
└── .factory/
    ├── README.md
    ├── project.json
    ├── project.lock
    ├── tech-profile.json
    ├── memory/
    ├── pm/
    └── workitems/
```

## 根 `docs/index.md` 的职责

根 `docs/index.md` 必须同时承担两件事：

1. 首页正文
2. 全站导航与权限清单

最小示例：

```md
---
title: 项目名称
mkdocs:
  home_access: public
  nav:
    - title: 入门说明
      children:
        - title: 概览
          path: 01-getting-started/index.md
          access: public
    - title: 用户指南
      children:
        - title: 概览
          path: 02-user-guide/index.md
          access: public
    - title: 项目开发文档（内）
      children:
        - title: 概览
          path: 04-project-development/index.md
          access: private
---
# 项目名称
```

规则：

- `mkdocs.home_access` 只允许 `public` 或 `private`
- 页面节点只允许 `title`、`path`、`access`
- 目录节点只允许 `title`、`children`
- `path` 只能写相对根 `docs/` 的路径

## 各模块职责

### `01-getting-started/`

面向第一次接触项目的读者，回答：

- 这是什么
- 先看什么
- 怎么开始

### `02-user-guide/`

面向实际使用者、管理员、实施和支持角色，回答：

- 怎么安装、配置、操作和排错
- 哪些流程是正式使用路径

### `03-developer-guide/`

面向需要扩展、集成或二次开发的人，回答：

- 稳定开发入口是什么
- 公共函数、接口、插件和契约怎么用

如果项目没有稳定的开发者暴露面，这个模块可以省略。

### `04-project-development/`

面向内部项目协作者，按阶段组织治理、需求、设计、计划、测试、发布、运维和追踪矩阵。

## 契约与资源放置规则

- `assets/` 只能放图片、附件、示意图、原型等资源文件
- Markdown 页面和契约文件不能放在 `assets/`
- 公开契约优先放在 `03-developer-guide/openapi/` 或 `03-developer-guide/tools/`
- 内部契约优先放在 `04-project-development/04-design/contracts/`

## 旧结构到新结构的映射

```text
00-governance  -> 04-project-development/01-governance
01-discovery   -> 04-project-development/02-discovery
02-requirements -> 04-project-development/03-requirements
03-solution    -> 04-project-development/04-design
04-delivery    -> 04-project-development/05-development-process
05-quality     -> 04-project-development/06-testing-verification
06-release     -> 04-project-development/07-release-delivery
07-operations  -> 04-project-development/08-operations-maintenance
08-handover    -> 02-user-guide
09-evolution   -> 04-project-development/09-evolution
traceability   -> 04-project-development/10-traceability
```

## 组织规则

- 新项目优先按 4 大模块直接建目录，不要再落旧生命周期顶层结构
- 历史项目优先走升级命令，不手工大搬家
- 任何页面新增、删除或移动后，同步刷新根 `docs/index.md` 与相关目录首页
- 新增正式页面后，同步根 `docs/index.md`；需要 AI 恢复时同步 `.factory/memory/doc-map.md`
- 临时过程材料不得放入 `docs/`
- 正式文档模板必须包含中文 `版本信息` 和 `版本历史`

## 模板资产与输出路径

内部模板资产可以继续按旧阶段分组命名，但输出路径必须落到 4 大模块结构。

常用映射：

- 根索引：`assets/templates/00-root/docs-index.md` -> `docs/index.md`
- 入门概览：`assets/templates/01-getting-started/project-overview.md` -> `docs/01-getting-started/project-overview.md`
- 快速开始：`assets/templates/01-getting-started/quick-start.md` -> `docs/01-getting-started/quick-start.md`
- 用户指南：`assets/templates/08-handover/user-guide.md` -> `docs/02-user-guide/user-guide.md`
- 管理员指南：`assets/templates/08-handover/admin-guide.md` -> `docs/02-user-guide/admin-guide.md`
- PRD：`assets/templates/02-requirements/prd.md` -> `docs/04-project-development/03-requirements/prd.md`
- 技术选型：`assets/templates/03-solution/technical-selection.md` -> `docs/04-project-development/04-design/technical-selection.md`
- 系统架构：`assets/templates/03-solution/system-architecture.md` -> `docs/04-project-development/04-design/system-architecture.md`
- API 设计：`assets/templates/03-solution/api-design.md` -> `docs/04-project-development/04-design/api-design.md`
- 测试计划：`assets/templates/05-quality/test-plan.md` -> `docs/04-project-development/06-testing-verification/test-plan.md`
- 发布说明：`assets/templates/06-release/release-notes.md` -> `docs/04-project-development/07-release-delivery/release-notes.md`
- 运维手册：`assets/templates/07-operations/operations-runbook.md` -> `docs/04-project-development/08-operations-maintenance/operations-runbook.md`
- 需求追踪矩阵：`assets/templates/traceability/requirements-matrix.md` -> `docs/04-project-development/10-traceability/requirements-matrix.md`
