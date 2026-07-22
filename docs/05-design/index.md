# 软件技术设计入口

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `DOC-NAV-DESIGN-001` |
| 正式版本 | `v1.1.0` |
| 来源候选 | `TASK-IMPLEMENT-003-P001` |
| 负责人 | `HUMAN_ARCHITECTURE_DOMAIN_LEAD` |
| 修改 / 审核 / 批准 | `uroborus` / `uroborus` / `uroborus` |
| 状态 | 已批准并生效 |
| 上游 | `docs/index.md`、`PRD` |
| 下游 | 适用于本项目的技术设计 owner |

## 本目录是给谁看的

`05-design` 只保存人类需要长期阅读、评审和维护的技术设计。架构师用它判断系统边界，开发者用它找到实现契约，测试人员用它找到可验证行为，产品和项目负责人用它理解方案影响。机器 Catalog、SQLite、缓存和生成 HTML 不属于本目录。

## 当前项目的设计目录

| 文档 | 中文名称 | 主要读者 | 解决的问题 | 何时需要 |
|---|---|---|---|---|
| [solution-overview.md](./solution-overview.md) | 总体方案与协作治理设计 | 项目负责人、产品、架构、全体协作者 | 系统总体目标、关键选择和协作边界 | 中大型或跨角色项目 |
| [technical-selection.md](./technical-selection.md) | 技术选型与工程规则 | 架构、开发、测试、维护者 | 技术栈、运行环境、持久化与工程约束 | 有技术实现时 |
| [system-architecture.md](./system-architecture.md) | 系统架构设计 | 架构、开发、运维、安全 | 系统上下文、分层、部署与质量属性 | 多模块或有重要 NFR 时 |
| [module-domain-design.md](./module-domain-design.md) | 模块与领域设计 | 架构、前后端、测试 | 模块职责、领域对象、依赖方向 | 有模块边界时 |
| [data-design.md](./data-design.md) | 数据与存储设计 | 架构、后端、数据、测试 | 表、字段、约束、索引、事务、迁移与生命周期 | 有持久化数据时 |
| [api-design.md](./api-design.md) | 接口与事件设计 | 后端、前端、集成方、测试 | 命令/API/事件的请求、响应、错误和版本 | 有跨模块或外部接口时 |
| [frontend-design.md](./frontend-design.md) | 前端架构与页面设计 | 前端、架构、UX、测试 | 路由、页面、组件、状态、权限和字段绑定 | 有用户界面时 |
| [ux-ui-design.md](./ux-ui-design.md) | 用户体验、交互与 UI 设计 | 产品、UX、UI、前端、测试 | 信息架构、任务流、视觉规则、响应式与可访问性 | 有人机交互时 |
| [workflow-execution-design.md](./workflow-execution-design.md) | 会话、任务与工作流执行设计 | 项目负责人、平台开发、测试 | 主任务、异步投影、状态流转和执行边界 | 有 AI/自动化工作流时 |
| [memory-design.md](./memory-design.md) | 记忆系统设计 | 架构、平台开发、测试 | 会话恢复、最小读取、压缩、晋升与淘汰 | 需要跨会话记忆时 |
| [interface-matrix.md](./interface-matrix.md) | 接口与字段追踪矩阵 | 架构、数据、API、前端、测试 | 关键字段和接口跨层如何贯通 | 跨层字段较多或审计要求高时 |

## 创建与维护规则

- 这些是可选文档类型，不是每个项目都必须创建。项目初始化根据产品形态、模块数、持久化、接口、前端、合规和运维复杂度选择需要的 owner；没有适用内容就不创建。
- 同一事实领域只有一个正式 owner。新需求、新方案和修复优先原位修改 owner，并在其正式版本历史中说明；只有现有 owner 无法承载独立事实领域时才允许新增文档。
- 实时任务、进度、评审和证据进入 `.factory/workitems/`；当前可查询关系进入可重建 SQLite；HTML 只保留最后有效快照。
- `ai-sdlc-catalog.source.json` 已迁至 `.factory/catalog/`，供固定 Builder 和索引器使用；发布 manifest 进入 WorkItem evidence。两者都不是给普通读者阅读的设计文档。

## 正式版本历史（仅已发布）

| 版本 | 日期 | 变更内容 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v1.0.0` | 2026-07-18 | 建立软件技术设计入口 | `uroborus` | `uroborus` | `uroborus` |
| `v1.1.0` | 2026-07-22 | 增加中文名称、读者、用途和适用条件；明确按项目自适应建文档，并移除机器 Catalog 导航 | `uroborus` | `uroborus` | `uroborus` |

[返回文档总入口](../index.md)。
