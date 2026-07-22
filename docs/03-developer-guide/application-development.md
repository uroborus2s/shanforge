# 应用开发

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `DOC-APPLICATION-DEVELOPMENT-001` |
| 正式版本 | `v1.0.0` |
| 来源候选 | `TASK-DESIGN-001-R019` |
| 发布事务 | `DESIGN-RELEASE-TX-R019-G001` |
| 负责人 | `HUMAN_DEVELOPMENT_EXECUTOR` |
| 修改 / 审核 / 批准 | `uroborus` / `uroborus` / `uroborus` |
| 状态 | 已批准并生效 |
| 上游 | `system-architecture`、`module-domain-design`、`development-setup` |
| 下游 | `interface-reference`、`plugin-development` |

## 文档职责

- 允许保存：扩展流程；代码入口；分层约束；测试入口。
- 禁止保存：内部执行证据；过期架构副本。
- 主要读者：应用开发者。

## 正式内容

## 1. 开发入口

应用开发以仓库内的 `skills/`、`docs/` 和 `.factory/memory/` 为主要协作面。

AI 运行时会维护自己的内部控制面，但那不是开发者默认阅读入口；开发者默认看正式文档、代码和命令入口。

开发前建议先读：

1. [总体方案与协作总览](../05-design/solution-overview.md)
2. [技术选型与工程规则](../05-design/technical-selection.md)
3. [系统架构设计](../05-design/system-architecture.md)
4. [模块边界文档](../05-design/module-domain-design.md)

## 2. 开发原则

- 需求未确认，不直接写实现。
- 设计未落文档，不直接扩边界。
- 代码变更要同步测试、文档和必要的运行摘要。
- 公开函数和接口变更，要同步更新开发者文档。

## 3. 推荐工作流

1. 确认需求与设计基线。
2. 拆任务。
3. 编码与测试。
4. 更新文档。
5. 进入 PR 闭环。

## 正式版本历史（仅已发布）

| 版本 | 日期 | 变更 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v1.0.0` | 2026-07-18 | 基于 `TASK-DESIGN-001-R019` 正式落档 | `uroborus` | `uroborus` | `uroborus` |
