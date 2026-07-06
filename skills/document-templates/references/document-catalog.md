# 软件项目文档清单（4 大模块版）

## 使用方式

- 先判断当前项目需要哪些顶层模块，再决定模块内部补哪些文档。
- `04-project-development/` 内部仍按阶段组织，但它只是第 4 个模块，不是顶层唯一入口。
- `必备` 表示大多数正式维护项目默认应该有。
- `条件` 表示只有在复杂度、风险、协作面或交付方式达到阈值时才补齐。

## 1. `01-getting-started`

| 文档 | 默认性 | 主要读者 | 主要作用 |
|---|---|---|---|
| `index.md` | 必备 | 所有新读者 | 给出本模块边界和推荐阅读顺序 |
| `project-overview.md` | 必备 | 新维护者、管理者、协作者 | 说明项目定位、边界、目标读者和推荐阅读路径 |
| `quick-start.md` | 必备 | 新维护者、使用者 | 提供最小启动步骤和常用命令 |
| `document-map.md` | 必备 | 新维护者、文档维护者 | 解释 4 大模块分别解决什么问题 |

最小交付：

- `project-overview.md`
- `quick-start.md`
- `document-map.md`

## 2. `02-user-guide`

| 文档 | 默认性 | 主要读者 | 主要作用 |
|---|---|---|---|
| `index.md` | 必备 | 用户、协作者 | 说明使用边界与阅读顺序 |
| `user-guide.md` | 必备 | 最终用户、维护者 | 讲清日常使用、关键任务和常见问题 |
| `admin-guide.md` | 条件 | 管理员、实施者 | 讲清配置、权限、初始化和升级维护 |
| `installation.md` | 条件 | 用户、实施者 | 说明安装、前置条件和环境准备 |
| `configuration.md` | 条件 | 管理员、实施者 | 说明配置项、密钥、差异和修改方法 |
| `usage.md` | 条件 | 用户、实施者 | 补充按场景组织的使用说明 |
| `prompt-templates.md` | 条件 | AI 协作者 | 提供 Prompt 模板和使用时机 |

最小交付：

- `index.md`
- `user-guide.md`

以下场景建议补充：

- 自托管或实施交付：补 `installation.md`、`configuration.md`、`admin-guide.md`
- 强依赖 AI 协作：补 `prompt-templates.md`

## 3. `03-developer-guide`

只有存在稳定开发或集成面时才默认需要。

| 文档 | 默认性 | 主要读者 | 主要作用 |
|---|---|---|---|
| `index.md` | 必备（启用时） | 开发者、集成方 | 说明开发者入口和边界 |
| `application-development.md` | 条件 | 应用开发者 | 讲清如何扩展当前应用或工程 |
| `development-setup.md` | 条件 | 开发者 | 讲清本地环境、依赖和调试入口 |
| `function-reference.md` | 条件 | 集成者、开发者 | 固定函数/CLI/能力入口的调用说明 |
| `interface-reference.md` | 条件 | 集成者、开发者 | 对外接口、协议和兼容约束 |
| `plugin-development.md` | 条件 | 插件开发者 | 讲清插件机制、生命周期和交付方式 |
| `openapi/*` | 条件 | API 集成方 | 存放公开 OpenAPI 契约和说明页 |
| `tools/*` | 条件 | Agent / MCP 集成方 | 存放公开 MCP tools 快照和说明页 |

启用信号：

- 有公开 API、SDK、MCP tools 或函数入口
- 有插件机制、模块扩展点或二次开发场景
- 需要对外发布稳定契约，而不是只留在内部设计文档中

## 4. `04-project-development`

这是内部项目事实源，按阶段列出。

### `01-governance`

| 文档 | 默认性 | 主要作用 |
|---|---|---|
| `project-charter.md` | 必备 | 明确目标、范围、成功标准和里程碑 |
| `stakeholders-raci.md` | 条件 | 明确职责与审批边界 |
| `risk-register.md` | 条件 | 让高风险点在设计和测试中被显式覆盖 |
| `glossary.md` | 条件 | 统一术语 |
| `roadmap.md` | 条件 | 说明阶段性规划 |

### `02-discovery`

| 文档 | 默认性 | 主要作用 |
|---|---|---|
| `input.md` | 必备 | 固化原始创意、背景、约束和启动输入 |
| `brainstorm-record.md` | 必备 | 保留问题空间、方案比较和决策过程 |
| `current-state-analysis.md` | 条件 | 历史项目现状基线 |
| `business-flow.md` | 条件 | 说明业务流程或用户旅程 |
| `scope-outline.md` | 条件 | 列清范围内/范围外 |

### `03-requirements`

| 文档 | 默认性 | 主要作用 |
|---|---|---|
| `prd.md` | 必备 | 正式功能需求与业务目标 |
| `requirements-analysis.md` | 必备 | 依赖、优先级、可行性与风险分析 |
| `requirements-verification.md` | 必备 | 校验 PRD、分析、字段与追踪覆盖 |
| `changelog.md` | 条件 | 记录需求级变更历史 |
| `nfr-catalog.md` | 条件 | 固化非功能要求 |
| `acceptance-criteria.md` | 条件 | 明确“什么算完成” |
| `change-requests.md` | 条件 | 管控 `CR-*` 变更入口 |

### `04-design`

| 文档 | 默认性 | 主要作用 |
|---|---|---|
| `technical-selection.md` | 必备 | 固化技术栈、工程规则和必装模块 |
| `system-architecture.md` | 必备 | 描述系统上下文、分层和关键组件 |
| `module-boundaries.md` | 必备 | 明确职责、数据所有权和耦合边界 |
| `api-design.md` | 必备 | 统一 API / CLI / 契约语义 |
| `backend-design.md` | 条件 | 细化服务、任务、幂等和可观测性 |
| `database-design.md` | 条件 | 定义实体、关系、索引和迁移 |
| `security-design.md` | 条件 | 说明安全控制和威胁模型 |
| `deployment-architecture.md` | 条件 | 描述环境拓扑和部署约束 |
| `ux-ui-design.md` | 条件 | 说明交互、页面和设计交付物 |
| `contracts/*` | 条件 | 放内部接口、事件、Schema 和契约说明 |

### `05-development-process`

| 文档 | 默认性 | 主要作用 |
|---|---|---|
| `software-development-process.md` | 必备 | 说明阶段顺序、输入输出和准入准出 |
| `implementation-plan.md` | 必备 | 把设计转成实施波次和顺序 |
| `task-breakdown.md` | 条件 | 形成任务颗粒和依赖 |
| `wbs.md` | 条件 | 给出工作分解结构 |
| `execution-log.md` | 条件 | 留存推进日志和回写记录 |
| `iteration-plan.md` | 条件 | 管理迭代或冲刺 |
| `migration-plan.md` | 条件 | 迁移、切换、回滚规划 |
| `historical-project-onboarding-checklist.md` | 条件 | 历史项目纳管收口清单 |

### `06-testing-verification`

| 文档 | 默认性 | 主要作用 |
|---|---|---|
| `test-strategy.md` | 条件 | 定义测试层次和自动化策略 |
| `test-plan.md` | 必备 | 定义测试范围、环境和入口/出口条件 |
| `test-cases.md` | 条件 | 需求到验证步骤的映射 |
| `test-data.md` | 条件 | 说明测试数据和准备方式 |
| `defect-log.md` | 条件 | 跟踪缺陷状态和优先级 |
| `test-report.md` | 必备 | 汇总通过情况、遗留问题和风险 |
| `uat-report.md` | 条件 | 业务验收结果 |

### `07-release-delivery`

| 文档 | 默认性 | 主要作用 |
|---|---|---|
| `acceptance-checklist.md` | 条件 | 上线前验收项与签字结果 |
| `delivery-package.md` | 条件 | 汇总代码、文档和交接资产 |
| `release-checklist.md` | 条件 | 上线动作检查清单 |
| `release-notes.md` | 必备 | 对外说明变更和影响 |
| `rollback-plan.md` | 条件 | 上线失败恢复方案 |
| `stage-check-report.md` | 条件 | 阶段 Gate 判断 |
| `quality-check-report.md` | 条件 | 质量总检 |

### `08-operations-maintenance`

| 文档 | 默认性 | 主要作用 |
|---|---|---|
| `deployment-guide.md` | 必备 | 定义部署步骤、依赖和验证动作 |
| `operations-runbook.md` | 必备 | 定义巡检、启停、故障处理入口 |
| `monitoring-alerting.md` | 条件 | 指标、阈值和告警路由 |
| `incident-playbook.md` | 条件 | 重大故障处理流程 |
| `backup-dr.md` | 条件 | 备份与灾备策略 |
| `support-handbook.md` | 条件 | 支持团队操作和升级路径 |
| `configuration-matrix.md` | 条件 | 汇总环境变量、密钥和差异 |

### `09-evolution`

| 文档 | 默认性 | 主要作用 |
|---|---|---|
| `skill-evolution-plan.md` | 条件 | 记录技能和流程演进方案 |
| `retrospective.md` | 条件 | 迭代或阶段回顾 |
| `postmortem.md` | 条件 | 事故复盘 |
| `deprecation-plan.md` | 条件 | 退役和替换规划 |

### `10-traceability`

| 文档 | 默认性 | 主要作用 |
|---|---|---|
| `requirements-matrix.md` | 必备 | 覆盖需求到设计/任务/测试/发布 |
| `interface-matrix.md` | 条件 | 覆盖接口到责任方/版本/验证 |
| `document-index.md` | 条件 | 总览正式文档现状 |

## 最小文档包建议

### 小型内部 CLI / 工具

- `01-getting-started/*`
- `02-user-guide/index.md`
- `02-user-guide/user-guide.md`
- `04-project-development` 内的项目章程、输入、PRD、需求分析、需求校验、技术选型、架构、模块边界、API 设计、实施计划、测试计划、发布说明、部署说明、运维手册、需求追踪矩阵

### 公开 API / 集成型项目

在“小型内部 CLI / 工具”基础上，额外补：

- `03-developer-guide/index.md`
- `03-developer-guide/interface-reference.md`
- `03-developer-guide/openapi/*`
- `03-developer-guide/tools/*`
- `04-project-development/04-design/contracts/*`

### 历史项目纳管

最先补齐：

- `04-project-development/02-discovery/current-state-analysis.md`
- `04-project-development/01-governance/project-charter.md`
- `04-project-development/03-requirements/prd.md`
- `04-project-development/04-design/system-architecture.md`
- `04-project-development/04-design/module-boundaries.md`
- `04-project-development/04-design/technical-selection.md`
- `04-project-development/04-design/api-design.md`
- `04-project-development/08-operations-maintenance/operations-runbook.md`
- `02-user-guide/user-guide.md`

### 自托管 / 实施交付型系统

额外补：

- `02-user-guide/admin-guide.md`
- `02-user-guide/installation.md`
- `02-user-guide/configuration.md`
- `04-project-development/08-operations-maintenance/configuration-matrix.md`
- `04-project-development/07-release-delivery/rollback-plan.md`

## 推荐做法

- 先判断是否需要启用 `03-developer-guide/`，不要机械生成。
- 稳定对外事实放公开模块；内部过程和决策放 `04-project-development/`。
- 文档写成“下一个人拿到就能继续工作”的形式，而不是只做归档。
