---
name: systematic-debugging
description: 遇到 bug、测试失败、构建失败、性能异常或任何意外行为时使用；修复前必须先完成根因调查，禁止猜测式补丁和未验证兜底。
---

# 系统化调试

本 skill 用于处理技术问题。目标是找到真实根因，再做最小修复。

## 触发

- 测试失败。
- 用户报告 bug。
- 构建、lint、集成或运行时异常。
- 性能、并发、时序或环境问题。
- 已经尝试修复但问题仍然存在。
- 想要“快速改一下”但还没有证据。

## 输入

- 错误输出、日志、截图或用户症状。
- 复现步骤。
- 最近 diff、配置变化和环境变化。
- 相关测试、调用链和数据流。

## 输出

- 根因调查：`.factory/workitems/<WORKITEM-ID>/evidence/`
- 调试报告：`.factory/workitems/<WORKITEM-ID>/reports/`
- 修复验证：`.factory/workitems/<WORKITEM-ID>/evidence/`
- ledger：`.factory/workitems/<WORKITEM-ID>/ledger.jsonl`

## 含义保留清单

- 修复前必须先完成根因调查。
- 禁止先猜修复。
- 禁止在不理解问题时堆补丁。
- 必须完整读取错误和堆栈。
- 必须尝试稳定复现。
- 必须检查最近变化。
- 多组件系统必须在边界收集证据。
- 深层错误必须沿调用链反向追踪。
- 修复必须针对根因，不是症状。
- 修 Bug 必须有失败测试、复现脚本或明确验收用例。
- 3 次修复失败后停止，质疑架构或请求人工决策。

## 默认流程

### Phase 1：根因调查

1. 完整读取错误、堆栈、日志和失败输出。
2. 复现问题；不能复现时先增加诊断，不修行为。
3. 检查最近 diff、依赖、配置和环境变化。
4. 多组件系统按边界记录输入、输出、配置和状态。
5. 深层错误按 [data-flow-tracing-guide.md](references/data-flow-tracing-guide.md) 反向追踪。
6. 按 [root-cause-investigation-template.md](references/root-cause-investigation-template.md) 记录直接原因和根源原因。

### Phase 2：模式分析

1. 找同仓库中可工作的相似实现。
2. 对照参考实现，不跳读关键路径。
3. 列出工作实现与失败实现的差异。
4. 确认依赖、配置、状态和假设。

### Phase 3：假设与最小验证

1. 写出单一假设：我认为根因是 X，因为 Y。
2. 用最小诊断或最小实验验证假设。
3. 一次只改变一个变量。
4. 假设失败就回到 Phase 1，不叠加补丁。

### Phase 4：根因修复

1. 先创建失败测试、复现脚本或验收用例。
2. 只修改导致根因的路径。
3. 对无效输入或危险操作补防御式校验，参考 [defense-in-depth-checklist.md](references/defense-in-depth-checklist.md)。
4. 对时序问题使用条件等待，参考 [condition-based-waiting-guide.md](references/condition-based-waiting-guide.md)，不要猜时间。
5. 运行定向验证和相关回归。
6. 如果 3 次修复失败，停止继续补丁，质疑架构并输出决策需求。

## 禁止

- 禁止没有根因就提修复方案。
- 禁止“试试看”式修改。
- 禁止多个修复一起改。
- 禁止用宽松解析、默认成功、空结果或静默忽略掩盖问题。
- 禁止只修报错点，不追踪坏数据来源。
- 禁止在 3 次失败后继续补第四个补丁。

## 状态包

```text
工作结果：
- work_item: <ID>
- skill: systematic-debugging
- status: root_cause_found | fixed | blocked | needs_user_input
- outputs:
  - <report path>
- evidence:
  - <reproduction and verification path>
- ledger_event: <event id>
- needs:
  - none | more_diagnostics | architecture_decision | human_confirmation
```
