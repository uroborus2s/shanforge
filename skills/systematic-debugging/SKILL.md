---
name: systematic-debugging
description: 遇到 bug、测试失败、构建失败、性能异常或任何意外行为时使用；修复前必须先完成根因调查，禁止猜测式补丁和未验证兜底。
---

# 系统化调试

本 skill 用于处理技术问题。目标是完成 Investigation Task：稳定复现、诊断证据、直接原因和根源原因。根因报告获人工确认前，不进入修复；根因确认后也只能进入修复方案 / 修复任务确认 Gate，不能直接改实现。

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
- ledger：`.factory/workitems/<WORKITEM-ID>/ledger.jsonl`

## 含义保留清单

- 修复前必须先完成根因调查。
- Investigation Task 只做复现、诊断、直接原因和根源原因。
- Investigation Task 完成时只能输出 `root_cause_found`、`blocked` 或 `needs_user_input`。
- `root_cause_found` 表示根因报告已形成，下一步是人工确认，不是修复。
- 根因报告获人工确认前不得进入修复。
- 根因报告获人工确认后，必须先形成修复方案或修复任务并再次等待人工确认。
- 不能复现时先要求更多信息，不改行为。
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
2. 复现问题；不能复现时停止并要求更多信息，不修行为。
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

### Phase 4：确认 Gate / 根因确认 Gate

1. 输出根因报告，明确复现结果、直接原因、根源原因和证据。
2. 若根因成立，状态写为 `root_cause_found`，needs 写为 `human_confirmation`。
3. 若不能复现，状态写为 `needs_user_input`，列出缺少的信息。
4. 若证据不足，状态写为 `blocked`，只补诊断需求。
5. 人工确认根因报告前，不写测试、不改实现、不进入修复。
6. 根因确认后，只输出修复方案或一个 / 多个修复任务；修复方案确认 Gate 通过前仍不得改实现。

## 禁止

- 禁止没有根因就提修复方案。
- 禁止“试试看”式修改。
- 禁止多个修复一起改。
- 禁止用宽松解析、默认成功、空结果或静默忽略掩盖问题。
- 禁止只修报错点，不追踪坏数据来源。
- 禁止在 3 次失败后继续补第四个补丁。
- 禁止在根因报告获人工确认前进入修复。

## 状态包

```text
工作结果：
- work_item: <ID>
- skill: systematic-debugging
- status: root_cause_found | blocked | needs_user_input
- outputs:
  - <report path>
- evidence:
  - <reproduction and diagnosis path>
- ledger_event: <event id>
- needs:
  - human_confirmation | more_information | more_diagnostics | architecture_decision
```

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。
