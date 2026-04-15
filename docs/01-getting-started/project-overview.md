# 项目概览

**项目名称：** 山海工枢 / shanforge
**文档状态：** `v2` 产品概览
**主要读者：** 项目维护者 | 协作者 | 业务 Agent 开发者 | 平台开发者
**最后更新：** 2026-04-13

## 1. 项目定位

山海工枢 `v2` 是一个面向业务装配的抽象 Agent 平台。

它的目标不是堆叠命令或脚本入口，而是建立一套统一的运行时、工作流 DSL、模型策略、能力注册和证据闭环，让不同业务可以通过 Agent App 低成本构建自己的工作流。

## 2. 平台核心

- 统一 Agent Platform Kernel
- Business Agent App 与平台内核隔离
- Workflow DSL 与 step 级模型策略
- LLM Runtime 与 Provider 解耦
- Capability Registry 与 Approval / Sandbox
- AgentResponse 与 Evidence 标准化

## 3. 推荐阅读顺序

1. [快速开始](./quick-start.md)
2. [文档地图](./document-map.md)
3. [总体方案与协作总览](../04-project-development/04-design/solution-overview.md)
4. [系统架构设计](../04-project-development/04-design/system-architecture.md)
5. [抽象 Agent 平台架构](../04-project-development/04-design/agent-platform-architecture.md)

## 4. 与其他资产的边界

- `docs/`：正式的人类文档事实源
- `scripts/`：当前可复用的执行与适配能力
- `skills/`：AI 协作规则和专项方法
- `.factory/`：运行时状态、压缩记忆和过程资产

## 5. 变更记录

| 日期 | 变更内容 | 变更人 |
|---|---|---|
| 2026-04-13 | 按 `v2` 抽象 Agent 平台方向重写项目概览 | Codex |
