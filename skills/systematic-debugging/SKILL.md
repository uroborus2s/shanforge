---
name: systematic-debugging
description: 遇到 bug、测试失败、构建失败、性能异常或任何意外行为时使用；修复前必须先完成根因调查，禁止猜测式补丁和未验证兜底。
---

# 系统化调试

本 skill 用于处理技术问题。目标是稳定复现，取得诊断证据，定位直接原因、根源原因和事实 owner，并按风险决定是否需要人工 Gate。

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

- 低、中风险默认在当前任务状态包中保存紧凑调查结论，不单独生成报告。
- 高风险、真实阻塞或需要跨会话恢复时，才写 `.factory/workitems/<WORKITEM-ID>/evidence/` 或 `reports/`。
- 项目化任务按流程总控要求追加最小 ledger 事件。

## 含义保留清单

- 修复前必须先完成根因调查。
- Investigation Task 只做复现、诊断、直接原因和根源原因。
- Investigation Task 完成时只能输出 `root_cause_found`、`blocked` 或 `needs_user_input`。
- `root_cause_found` 表示根因、事实 owner、影响范围和风险已形成。
- 低、中风险不新增人工 Gate，直接交给 owner Skill 修复受影响范围。
- 高风险依次等待根因确认和最小修复方案确认，两个 Gate 通过后才修复。
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
6. 记录直接原因、根源原因、影响范围和 `fault_owner = requirement | design | implementation | test | configuration | environment | production`。

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

### Phase 4：风险分级与交接

1. 输出调查结论，明确复现结果、直接原因、根源原因、事实 owner、影响范围和证据。
2. 若根因成立，状态写为 `root_cause_found`。
3. 若不能复现，状态写为 `needs_user_input`，列出缺少的信息。
4. 若证据不足，状态写为 `blocked`，只补诊断需求。
5. 低、中风险写 `needs: owner_fix`，交给事实 owner 直接修复，并只复测失败案例、根因案例和受影响调用方 / 契约。
6. 高风险写 `needs: human_confirmation`；根因确认后只形成最小修复方案，第二次确认前不得改实现。

## 禁止

- 禁止没有根因就提修复方案。
- 禁止“试试看”式修改。
- 禁止多个修复一起改。
- 禁止用宽松解析、默认成功、空结果或静默忽略掩盖问题。
- 禁止只修报错点，不追踪坏数据来源。
- 禁止在 3 次失败后继续补第四个补丁。
- 禁止跳过风险分级；高风险根因和修复方案未获确认前不得进入修复。

## 状态包

```text
工作结果：
- work_item: <ID>
- skill: systematic-debugging
- status: root_cause_found | blocked | needs_user_input
- outputs:
  - <report path or inline summary>
- evidence:
  - <reproduction and diagnosis path or command receipt>
- fault_owner: requirement | design | implementation | test | configuration | environment | production
- risk: low | medium | high
- impacted_tests: <failed case, root-cause case, affected callers/contracts>
- ledger_event: <event id>
- needs:
  - owner_fix | human_confirmation | more_information | more_diagnostics | architecture_decision
```

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。
