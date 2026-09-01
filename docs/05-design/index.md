# 软件技术设计入口

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `DOC-NAV-DESIGN-001` |
| 正式版本 | `v1.3.0` |
| 来源候选 | `SOFTWARE-LIFECYCLE-GOVERNANCE-001` |
| 负责人 | `HUMAN_ARCHITECTURE_DOMAIN_LEAD` |
| 修改 / 审核 / 批准 | `uroborus` / `uroborus` / `uroborus` |
| 状态 | 已批准并生效 |
| 上游 | `docs/index.md`、`PRD` |
| 下游 | 适用于本项目的技术设计 owner |

## 本目录是给谁看的

`05-design` 只保存人类需要长期阅读、评审和维护的技术设计。架构师用它判断系统边界，开发者用它找到实现契约，测试人员用它找到可验证行为，产品和项目负责人用它理解方案影响。机器 Catalog、缓存和生成 HTML 不属于本目录。

## 当前 Skill-first 设计文档

本目录各文档共同构成当前 Skill-first 设计基线：系统架构定义产品边界，其他设计 owner
分别定义交付治理、技术选择、模块、事实、宿主契约、快照、体验、恢复与追踪。

| 文档 | 中文名称 | 主要读者 | 解决的问题 | 何时需要 |
|---|---|---|---|---|
| [solution-overview.md](./solution-overview.md) | 总体方案与协作治理设计 | 项目负责人、架构 | Skill-first 交付边界与协作治理 | 调整协作边界或治理时 |
| [technical-selection.md](./technical-selection.md) | 技术选型与工程规则 | 架构、维护者 | Skill、确定性脚本与工程约束 | 选择工具或维护工程规则时 |
| [system-architecture.md](./system-architecture.md) | Skill-first 系统架构 | 架构、开发、运维、安全 | 当前产品边界、skill 交付、项目事实与快照脚本 | 修改执行入口或目录边界时 |
| [module-domain-design.md](./module-domain-design.md) | 模块与领域设计 | 架构、测试 | Skill、事实、辅助脚本与测试责任 | 调整职责或测试边界时 |
| [data-design.md](./data-design.md) | Skill 与项目事实数据边界 | 架构、开发、测试 | Git 事实、work item 与可重建缓存的边界 | 修改事实或缓存时 |
| [api-design.md](./api-design.md) | 接口与事件设计 | 架构、集成方 | 宿主与 Skill 的文件、状态包契约 | 修改宿主交接或状态包时 |
| [frontend-design.md](./frontend-design.md) | 前端架构与页面设计 | 前端、架构、UX | 静态项目快照的前端边界 | 修改快照界面或验证时 |
| [ux-ui-design.md](./ux-ui-design.md) | 用户体验、交互与 UI 设计 | 产品、UX、UI | 快照的信息优先级与目标项目 UI 方法 | 设计快照或目标项目 UI 时 |
| [workflow-execution-design.md](./workflow-execution-design.md) | 会话、任务与工作流执行设计 | 项目负责人、开发、测试 | skill-first 生命周期、Gate、模型路由和过程数据边界 | 项目化 AI 协作、交付或恢复时 |
| [memory-design.md](./memory-design.md) | 记忆系统设计 | 架构、维护者 | 恢复摘要与正式/执行事实边界 | 修改恢复或事实边界时 |
| [interface-matrix.md](./interface-matrix.md) | 接口与字段追踪矩阵 | 架构、维护者 | 当前契约的 consumer、owner、路径与验证 | 追踪契约或定向测试时 |

## 创建与维护规则

- 这些是可选文档类型，不是每个项目都必须创建。项目初始化根据产品形态、模块数、持久化、接口、前端、合规和运维复杂度选择需要的 owner；没有适用内容就不创建。
- 同一事实领域只有一个正式 owner。新需求、新方案和修复优先原位修改 owner，并在其正式版本历史中说明；只有现有 owner 无法承载独立事实领域时才允许新增文档。
- 实时任务、进度、评审和证据进入目标项目 `.factory/workitems/`；HTML 只保留最后有效快照。
- `ai-sdlc-catalog.source.json` 已迁至 `.factory/catalog/`，供固定 Builder 和索引器使用；发布 manifest 进入 WorkItem evidence。两者都不是给普通读者阅读的设计文档。

## 正式版本历史（仅已发布）

| 版本 | 日期 | 变更内容 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v1.3.0` | 2026-09-01 | 同步当前 Skill-first 设计目录与生命周期执行设计入口 | `AI_EXECUTOR` | 集中质量门 | `uroborus` |
| `v1.2.0` | 2026-07-28 | 系统架构切换为 skill-first，旧平台设计降为历史 | `uroborus` | `uroborus` | `uroborus` |
| `v1.0.0` | 2026-07-18 | 建立软件技术设计入口 | `uroborus` | `uroborus` | `uroborus` |
| `v1.1.0` | 2026-07-22 | 增加中文名称、读者、用途和适用条件；明确按项目自适应建文档，并移除机器 Catalog 导航 | `uroborus` | `uroborus` | `uroborus` |

[返回文档总入口](../index.md)。
