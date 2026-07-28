# 项目概览

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `DOC-PROJECT-OVERVIEW-001` |
| 正式版本 | `v1.1.0` |
| 来源候选 | `SKILL-FIRST-PM-001` |
| 发布事务 | `N/A：用户直接批准 skill-first 边界收口` |
| 负责人 | `HUMAN_PROJECT_OWNER` |
| 修改 / 审核 / 批准 | `uroborus` / `uroborus` / `uroborus` |
| 状态 | 已批准并生效 |
| 上游 | `.factory/project.json`、`project-charter` |
| 下游 | `quick-start`、`用户指南`、`开发者指南`、`产品需求`、`技术设计` |

## 文档职责

- 允许保存：项目定位；范围；角色；六类阅读入口。
- 禁止保存：需求明细；架构实现细节；执行状态。
- 主要读者：新维护者、管理者、协作者。

## 正式内容

**项目名称：** 山海工枢 / shanforge
**文档状态：** `skill-first` 产品概览
**主要读者：** 项目维护者 | 协作者 | AI 工程使用者
**最后更新：** 2026-07-28

## 1. 项目定位

山海工枢是一套面向 Codex、Gemini CLI 等代理宿主的 `skill-first` 软件工厂资产。

它通过 skills、正式文档模板、项目规则和 `.factory/` 执行事实约束 AI 协作交付；
不提供需要目标项目导入的 Agent 平台运行时。

## 2. 平台核心

- `using-shanforge` 统一判断项目流程位置。
- 专项 skill 承担需求、设计、实现、评审、验证和提交方法。
- `.factory/` 保存项目自己的 work item、ledger、evidence 和压缩记忆。
- 确定性辅助能力随所属 skill 放在 `scripts/`，不依赖 Shanforge 源码仓。

## 3. 推荐阅读顺序

1. [快速开始](./quick-start.md)
2. [文档地图](../index.md)
3. [总体方案与协作总览](../05-design/solution-overview.md)
4. [Skill-first 架构](../05-design/system-architecture.md)

## 4. 与其他资产的边界

- `docs/`：正式的人类文档事实源
- `scripts/`：仓库级 skill 同步工具
- `skills/`：AI 协作规则、专项方法及其自带确定性脚本
- `.factory/`：运行时状态、压缩记忆和过程资产

目标项目不调用 Shanforge 仓库的 `src/`、虚拟环境或绝对路径。

## 5. 变更记录

| 日期 | 变更内容 | 变更人 |
|---|---|---|
| 2026-07-28 | 收口为 skill-first 产品，删除平台 runtime 依赖 | 项目负责人 |
| 2026-04-13 | 按 `v2` 抽象 Agent 平台方向重写项目概览 | 项目负责人 |

## 正式版本历史（仅已发布）

| 版本 | 日期 | 变更 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v1.1.0` | 2026-07-28 | 确立 skill-first 产品与 skill-local script 边界 | `uroborus` | `uroborus` | `uroborus` |
| `v1.0.0` | 2026-07-18 | 基于 `TASK-DESIGN-001-R019` 正式落档 | `uroborus` | `uroborus` | `uroborus` |
