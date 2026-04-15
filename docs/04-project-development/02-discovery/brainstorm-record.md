# 头脑风暴记录

**项目名称/主题：** 山海工枢 `v2` 抽象 Agent 平台
**文档状态：** 已确认
**参与者：** 用户 | Codex
**主要读者：** 产品 | 需求 | 架构 | 项目负责人
**下游输出：** PRD | 方案设计输入
**最后更新：** 2026-04-13

## 1. 背景与问题

- 用户要求 `v2` 完全按新平台目标重建。
- Hermes Agent 被选为主要架构输入，而不是局部功能参考。
- 最关键的问题不再是“如何整理旧流程”，而是“如何建立一个以后只需要关注业务的 Agent 平台”。

## 2. 讨论结论

- 选择高度抽象化平台路线，而不是在旧命令体系外包一层薄 runtime。
- 业务流放在 Business Agent App 和 Workflow DSL 中处理。
- 大模型交互在 `LLM Runtime + LLMProviderPort + ModelPolicy` 层解耦。
- 平台对外输出统一 `AgentResponse`。

## 3. 最终设计方向

- 架构风格：DDD / Hexagonal
- 平台核心：Kernel、Workflow Runtime、LLM Runtime、Capability Registry、Context Engine、Policy / Sandbox、Delegation / Gateway
- 业务开发面：Manifest、Workflow DSL、ModelPolicy、Capability 引用、output schema
- 适配器策略：遗留脚本和文件合同下沉为基础设施适配器

## 4. 推荐实施顺序

1. 先重写需求、设计、计划和追踪基线
2. 再实现平台契约和最小主闭环
3. 最后用 demo Agent App 验证编码流和写作流
