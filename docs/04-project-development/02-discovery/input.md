# 项目输入

**项目名称：** 山海工枢 / shanforge
**负责人：** 仓库维护者
**主要读者：** 产品 | 需求分析 | 架构
**下游输出：** 头脑风暴记录 | 项目章程 | PRD
**最后更新：** 2026-04-13

## 1. 原始目标

- 将 `v2` 重新定义为全新的抽象 Agent 平台
- 完整吸收 Hermes Agent 的能力结构与架构思路
- 让未来开发重点只停留在业务流，而不是底层模型、上下文、工具和执行细节

## 2. 关键输入

- 用户明确要求彻底抛弃旧版本包袱
- Hermes 核心价值在于主循环、工具治理、会话记忆、委派和协议扩展
- 平台必须回答三个核心问题：
  - 业务流在哪里处理
  - 大模型交互在哪里解耦
  - 用户如何快速构建工作流

## 3. 当前边界

- 业务开发面：Agent App Manifest + Workflow DSL
- 模型解耦面：ModelPolicy + LLM Runtime + LLMProviderPort
- 治理面：Capability Registry + Approval / Sandbox + Evidence
- 扩展面：Delegation + Gateway + Presentation Adapters

## 4. 当前最重要决策

- `v2` 是新产品，不是旧版本续写
- 旧实现只作为 adapter 事实，不再进入主需求
- 需求、设计、实施和测试全部改按纯平台编号重排
