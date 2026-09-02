---
name: agent-harness-construction
description: 设计并优化 AI 代理的行动空间、工具定义和观察格式，以提高任务完成率。
---

# 代理工具链构建 (Agent Harness Construction)

当你需要改进代理的规划、工具调用、错误恢复以及任务收敛能力时，请使用此技能。

## 适用边界

适用于设计或评审 agent harness、工具 schema、观察格式、恢复路径和上下文预算。

不适用于：

- 普通业务功能实现。
- 只需要使用现有工具完成任务的场景。
- Shanforge 阶段路由、review gate、人工确认或提交流程；这些由流程总控处理。
- Codex skill 文本、触发、评估或打包；这些交给 `skill-creator`。
- 没有明确 agent、工具或观察面要改造的泛架构讨论。

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
- `next_actions`: 仅为内部候选的后续动作，不直接面向用户
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

## 输出契约

交付时输出一份可落地的 harness 设计或评审包，至少包含：

- 目标 agent / workflow。
- 需要新增、修改或删除的工具清单。
- 每个工具的输入 schema、输出 schema 和错误恢复语义。
- 观察格式样例。
- 最小评估指标和验证方式。
- 风险、取舍和不做事项。

若在 Shanforge work item 中使用，只回写状态包：

```text
工作结果：
- work_item: <WORKITEM-ID or none>
- skill: agent-harness-construction
- status: ready_for_review | blocked | needs_user_input
- outputs:
  - <path 或 inline summary>
- evidence:
  - <path 或验证说明>
- ledger_event: <event id or none>
- needs:
  - review | verification | user_input | none
```

项目化用户输出仍只有一个 `next_required_action`，由 `using-shanforge` 总控生成；不得把 `next_actions` 候选当作多个用户动作。

## 失败语义

`blocked` 用于缺少真实目标 agent、工具调用约束、失败样本、安全边界或可验证指标，导致无法判断 harness 是否正确的情况。

`needs_user_input` 用于必须由用户决定目标 agent、工具权限、安全边界、成本上限或评估目标的情况。

不要把“还可以继续优化”写成 `blocked`；保守给出当前最小可行设计，并把后续增强列为不做事项。

## 反面模式 (Anti-Patterns)

- 语义重叠的工具过多。
- 工具输出不透明，且没有恢复提示。
- 仅输出错误，而没有后续步骤。
- 上下文过载，包含无关的引用。

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。
