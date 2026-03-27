---
name: agent-harness-construction
description: 设计并优化 AI 代理的行动空间、工具定义和观察格式，以提高任务完成率。
---

# 代理工具链构建 (Agent Harness Construction)

当你需要改进代理的规划、工具调用、错误恢复以及任务收敛能力时，请使用此技能。

## 核心模型

代理的输出质量受以下因素制约：
1. 行动空间质量 (Action space quality)
2. 观察质量 (Observation quality)
3. 恢复质量 (Recovery quality)
4. 上下文预算质量 (Context budget quality)

## 行动空间设计

1. 使用稳定且明确的工具名称。
2. 坚持“模式优先”(Schema-first) 且精简的输入。
3. 返回确定性的输出结构。
4. 除非无法隔离，否则避免使用“万能工具”。

## 粒度规则

- **微工具 (Micro-tools)**：用于高风险操作（部署、迁移、权限）。
- **中型工具 (Medium tools)**：用于常见的编辑/读取/搜索循环。
- **宏工具 (Macro-tools)**：仅在往返开销（Round-trip overhead）成为主要成本时使用。

## 观察设计 (Observation Design)

每个工具的响应都应包含：
- `status`: success (成功) | warning (警告) | error (错误)
- `summary`: 一行结果摘要
- `next_actions`: 可执行的后续动作
- `artifacts`: 文件路径 / ID

## 错误恢复契约

对于每个错误路径，需包含：
- 根因提示 (Root cause hint)
- 安全重试指令 (Safe retry instruction)
- 明确的终止条件 (Explicit stop condition)

## 上下文预算管理

1. 保持系统提示词 (System Prompt) 最小化且不变量。
2. 将大型指南移动到按需加载的技能 (Skills) 中。
3. 优先引用文件，而非内联长文档。
4. 在阶段边界（Phase boundaries）进行压缩，而非基于任意的 Token 阈值。

## 架构模式指南

- **ReAct**: 最适合路径不确定的探索性任务。
- **函数调用 (Function-calling)**: 最适合结构化的确定性流程。
- **混合模式 (推荐)**: ReAct 规划 + 类型化工具执行。

## 基准测试

跟踪指标：
- 完成率 (Completion rate)
- 每个任务的重试次数
- pass@1 和 pass@3
- 每个成功任务的成本

## 反面模式 (Anti-Patterns)

- 语义重叠的工具过多。
- 工具输出不透明，且没有恢复提示。
- 仅输出错误，而没有后续步骤。
- 上下文过载，包含无关的引用。
