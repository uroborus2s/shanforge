# 追踪规则、阶段关口与重构流程

## 每份正式文档的最小元数据

建议每份正式文档开头至少写明：

- 项目名称
- 文档状态：草稿 | 评审中 | 已批准 | 已发布 | 已废弃
- 负责人
- 主要读者
- 上游输入
- 下游输出
- 关联追踪 ID
- 最后更新时间

## 核心稳定 ID

默认优先使用项目级稳定 ID：

| 前缀 | 含义 |
|---|---|
| `REQ-*` | 功能需求 |
| `NFR-*` | 非功能需求 |
| `ARCH-*` | 架构设计项 |
| `MOD-*` | 模块或组件边界 |
| `API-*` | API / CLI / 接口项 |
| `DATA-*` | 数据实体、表、迁移项 |
| `UI-*` | 页面、交互、用户旅程项 |
| `TASK-*` | 实施任务 |
| `TEST-*` | 测试用例 |
| `CR-*` | 变更请求 |
| `BUG-*` | 缺陷 |
| `REL-*` | 发布项 |
| `OPS-*` | 运维项 |

如果项目已经在用扩展前缀，可以兼容保留，例如 `BIZ-*`、`RISK-*`、`DOC-*`、`UAT-*`、`ADR-*`，但不要让扩展前缀替代核心稳定 ID。

规则：

- 同一项目内按前缀递增
- 废弃编号不回收
- 需求、设计、测试、发布和运维文档尽量引用编号而不是只有自然语言标题

## 4 大模块和旧目录的映射

| 旧目录 | 新路径 |
|---|---|
| `00-governance` | `04-project-development/01-governance` |
| `01-discovery` | `04-project-development/02-discovery` |
| `02-requirements` | `04-project-development/03-requirements` |
| `03-solution` | `04-project-development/04-design` |
| `04-delivery` | `04-project-development/05-development-process` |
| `05-quality` | `04-project-development/06-testing-verification` |
| `06-release` | `04-project-development/07-release-delivery` |
| `07-operations` | `04-project-development/08-operations-maintenance` |
| `08-handover` | `02-user-guide` |
| `09-evolution` | `04-project-development/09-evolution` |
| `traceability` | `04-project-development/10-traceability` |

## 追踪矩阵至少覆盖什么

最小矩阵至少回答：

- `REQ/NFR -> ARCH/MOD/API/DATA/UI`
- `REQ/NFR -> TASK`
- `REQ/NFR -> TEST`
- `REQ/NFR -> REL`
- `MOD/API -> OPS`

每条需求还必须带需求或变更版本、页面/接口/任务/测试关联、设计/实现/集成/验收状态和证据。对完整批准需求及变更逐项核对未映射、未实现、未验证、阻塞和延期；不能只数已拆任务。

如果存在稳定对外接口，再补：

- `API -> 提供方/消费方`
- `API -> 版本/兼容策略`
- `API -> 监控与告警`

## 阶段关口

### 立项 -> 调研 / 需求

至少准备：

- `04-project-development/01-governance/project-charter.md`
- 必要时的职责和风险文档

通过标准：

- 目标、范围、负责人、成功标准明确
- 高风险点已经登记

### 调研 -> 需求

至少准备：

- `04-project-development/02-discovery/index.md`
- 当前正式调研报告或 work item brief

通过标准：

- 当前事实、约束和候选方案明确
- 能判断下一步是补需求、纳管还是直接维护

### 需求 -> 设计

至少准备：

- `04-project-development/03-requirements/prd.md`
- `04-project-development/03-requirements/requirements-verification.md`
- 需求包中的 `analysis_mode = embedded | standalone`
- 能回读分析内容的 `analysis_locator`

`embedded` 时分析内容位于 PRD 或已批准需求包；`standalone` 时才要求
`04-project-development/03-requirements/requirements-analysis.md`。Gate 校验内容和定位，
不再无条件要求 `requirements-analysis.md`。

建议同时准备：

- `nfr-catalog.md`
- `acceptance-criteria.md`

通过标准：

- 需求优先级明确
- 分析内容覆盖依赖、可行性、风险以及对设计和测试的影响
- 非功能要求可被设计与测试引用
- 变更入口清晰

### 设计 -> 开发实施

至少准备：

- `04-project-development/04-design/technical-selection.md`
- `04-project-development/04-design/system-architecture.md`
- `04-project-development/04-design/module-boundaries.md`
- `04-project-development/04-design/api-design.md`
- `04-project-development/05-development-process/implementation-plan.md`

通过标准：

- 模块职责、接口语义和依赖方向明确
- 可以据此拆任务、写代码、写测试

### 开发实施 -> 测试 / 验收

至少准备：

- `04-project-development/06-testing-verification/test-plan.md`
- 必要时的测试用例、缺陷日志
- 可追踪到需求的任务状态

通过标准：

- 每个高优先级需求都有验证路径
- 已知风险有对应测试覆盖

### 测试 / 验收 -> 发布

至少准备：

- `04-project-development/06-testing-verification/test-report.md`
- `04-project-development/07-release-delivery/release-notes.md`
- 自托管或关键系统时补 `rollback-plan.md`

通过标准：

- 残留问题被接受或关闭
- 失败时有清晰回退路径

### 发布 -> 运维 / 交接

至少准备：

- `04-project-development/08-operations-maintenance/deployment-guide.md`
- `04-project-development/08-operations-maintenance/operations-runbook.md`
- `02-user-guide/user-guide.md`
- 有管理员角色时补 `02-user-guide/admin-guide.md`

通过标准：

- 接手团队能独立完成部署、巡检和基础排障
- 用户或实施方知道如何完成主要操作

## 文档重构 / 升级流程

### 1. 先识别项目状态

| 场景 | 推荐入口 | 说明 |
|---|---|---|
| 空目录新项目 | `using-shanforge` -> `document-templates` | 判断项目状态后创建最小治理骨架和新结构 |
| 历史未纳管项目 | 先交给 `using-shanforge` 判断是否需要项目纳管，再用 `document-templates` skill | 先建真实状态基线，再重构文档 |
| 已纳管但旧目录结构 | `document-templates` skill + `docs-stratego source validate` | 直接按 4 大模块重构并校验 |
| 只有需求文档落后 | `requirements-engineering` + `document-templates` | 只升级需求文档，不替代整套重构 |

### 2. docs 标准升级主路径

优先使用 skill + CLI 主路径：

1. 用 `document-templates` skill 按 4 大模块重构 `docs/`
2. 明确根 `docs/index.md` 是唯一导航与权限事实源
3. 执行 `uvx --from docs-stratego docs-stratego source validate --repo-path .`
4. 如需接入 `docs-stratego` 聚合站点，再执行 `docs-stratego source add/remove/scaffold-notify/sync/build`

说明：

- 文档重构本身由 `document-templates` skill 承担
- `docs-stratego source validate` 是当前唯一正式的源仓校验入口
- 旧的 `factory-docs-*` 迁移、刷新、升级脚本已退场，不再作为正式流程

### 3. 历史项目纳管后的收口

历史项目至少确认：

- 已建立 `current-state-analysis.md`
- 已补齐项目章程、PRD、技术选型、架构、模块边界、API 设计
- 已补齐用户指南与运维手册
- 再执行一次 `docs-stratego source validate`

### 4. 对接 `docs-stratego` 的额外约束

- 根 `docs/index.md` 是唯一导航与权限事实源
- 页面节点 `access` 才决定 `public/private`
- 子目录 `index.md` 不再维护导航树
- 契约文件不能放在 `assets/`

## 推荐写法

- 把 Gate 写成“缺哪份文档就不能稳妥交接”的形式
- 把升级流程写成“先重构、再校验、再接入聚合站点”的形式
- 把根索引视为导航事实源，而不是普通首页正文
