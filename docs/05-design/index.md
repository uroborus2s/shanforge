# 软件技术设计入口

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `DOC-NAV-DESIGN-001` |
| 正式版本 | `v1.2.0` |
| 来源候选 | `SKILL-FIRST-PM-001` |
| 负责人 | `HUMAN_ARCHITECTURE_DOMAIN_LEAD` |
| 修改 / 审核 / 批准 | `uroborus` / `uroborus` / `uroborus` |
| 状态 | 已批准并生效 |
| 上游 | `docs/index.md`、`PRD` |
| 下游 | 适用于本项目的技术设计 owner |

## 本目录是给谁看的

`05-design` 只保存人类需要长期阅读、评审和维护的技术设计。架构师用它判断系统边界，开发者用它找到实现契约，测试人员用它找到可验证行为，产品和项目负责人用它理解方案影响。机器 Catalog、缓存和生成 HTML 不属于本目录。

## 当前项目的设计目录

当前实现合同只以 `system-architecture.md` 和 `data-design.md` 为准。旧 Python 平台的
技术选型、模块、API、前端、UX、memory 与接口矩阵只保留为历史决策记录；其中出现的
`src/`、SQLite、DI 或平台服务不得用于当前实现。

| 文档 | 中文名称 | 主要读者 | 解决的问题 | 何时需要 |
|---|---|---|---|---|
| [solution-overview.md](./solution-overview.md) | 历史平台调研与协作治理设计 | 项目负责人、架构 | 旧平台方向的来源记录；当前实现边界以系统架构为准 | 追溯历史决策时 |
| [technical-selection.md](./technical-selection.md) | 历史平台技术选型 | 架构、维护者 | 旧 Python 平台选型记录 | 追溯历史决策时 |
| [system-architecture.md](./system-architecture.md) | Skill-first 系统架构 | 架构、开发、运维、安全 | 当前产品边界、skill 交付、项目事实与快照脚本 | 修改执行入口或目录边界时 |
| [module-domain-design.md](./module-domain-design.md) | 历史平台模块设计 | 架构、测试 | 旧 Python 平台模块记录，不是当前实现合同 | 追溯历史决策时 |
| [data-design.md](./data-design.md) | Skill 与项目事实数据边界 | 架构、开发、测试 | Git 事实、work item 与可重建缓存的边界 | 修改事实或缓存时 |
| [api-design.md](./api-design.md) | 历史平台接口设计 | 架构、集成方 | 旧平台 API 与事件记录 | 追溯历史决策时 |
| [frontend-design.md](./frontend-design.md) | 历史平台前端设计 | 前端、架构、UX | 旧平台页面与状态绑定记录 | 追溯历史决策时 |
| [ux-ui-design.md](./ux-ui-design.md) | 历史平台 UX/UI 设计 | 产品、UX、UI | 旧项目站点体验记录 | 追溯历史决策时 |
| [workflow-execution-design.md](./workflow-execution-design.md) | 会话、任务与工作流执行设计 | 项目负责人、平台开发、测试 | 主任务、异步投影、状态流转和执行边界 | 有 AI/自动化工作流时 |
| [memory-design.md](./memory-design.md) | 历史平台记忆设计 | 架构、维护者 | 旧 runtime memory 记录；当前流程见 `project-memory` skill | 追溯历史决策时 |
| [interface-matrix.md](./interface-matrix.md) | 历史平台接口矩阵 | 架构、维护者 | 旧平台跨层字段记录 | 追溯历史决策时 |

## 创建与维护规则

- 这些是可选文档类型，不是每个项目都必须创建。项目初始化根据产品形态、模块数、持久化、接口、前端、合规和运维复杂度选择需要的 owner；没有适用内容就不创建。
- 同一事实领域只有一个正式 owner。新需求、新方案和修复优先原位修改 owner，并在其正式版本历史中说明；只有现有 owner 无法承载独立事实领域时才允许新增文档。
- 实时任务、进度、评审和证据进入目标项目 `.factory/workitems/`；HTML 只保留最后有效快照。
- `ai-sdlc-catalog.source.json` 已迁至 `.factory/catalog/`，供固定 Builder 和索引器使用；发布 manifest 进入 WorkItem evidence。两者都不是给普通读者阅读的设计文档。

## 正式版本历史（仅已发布）

| 版本 | 日期 | 变更内容 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v1.2.0` | 2026-07-28 | 系统架构切换为 skill-first，旧平台设计降为历史 | `uroborus` | `uroborus` | `uroborus` |
| `v1.0.0` | 2026-07-18 | 建立软件技术设计入口 | `uroborus` | `uroborus` | `uroborus` |
| `v1.1.0` | 2026-07-22 | 增加中文名称、读者、用途和适用条件；明确按项目自适应建文档，并移除机器 Catalog 导航 | `uroborus` | `uroborus` | `uroborus` |

[返回文档总入口](../index.md)。
