# API 设计文档

**项目名称：** 山海工枢 / shanforge
**文档状态：** `v2` 契约基线
**负责人：** 仓库维护者
**主要读者：** 架构 | 平台开发 | 业务 Agent 开发 | 测试
**上游输入：** PRD | 系统架构 | 模块边界
**下游输出：** 接口实现 | 契约测试 | Mock provider
**最后更新：** 2026-04-15

## 1. 契约目录

| API ID | 契约 | 类型 | 关联需求 | 说明 |
|---|---|---|---|---|
| `API-001` | Agent App Manifest Contract | Business Contract | `REQ-002`, `REQ-010` | 定义业务 App 的声明入口 |
| `API-002` | Workflow DSL Contract | Workflow Contract | `REQ-003`, `REQ-010` | 定义 workflow、step、条件、输出 |
| `API-003` | ModelPolicy Contract | Runtime Policy Contract | `REQ-004` | 定义 provider、model、预算、fallback 等 |
| `API-004` | LLMProviderPort Contract | Port Contract | `REQ-004` | 统一供应商调用接口 |
| `API-005` | Capability Contract | Capability Contract | `REQ-005`, `REQ-007` | 定义工具输入输出、写集、风险和证据要求 |
| `API-006` | Context Package & Recall Contract | Runtime Context Contract | `REQ-006` | 定义运行时最小上下文与 recall bundle |
| `API-007` | Session / Event / Memory Ledger Contract | State Contract | `REQ-001`, `REQ-006`, `REQ-009` | 定义会话、事件、evidence 和蒸馏输入 |
| `API-008` | Approval Decision Contract | Policy Contract | `REQ-007` | 定义审批结果与执行许可 |
| `API-009` | ExecutionPort Contract | Port Contract | `REQ-005`, `REQ-007` | 定义能力执行与沙箱边界 |
| `API-010` | Delegation Contract | Coordination Contract | `REQ-008` | 定义 worker 任务、写集和验收 |
| `API-011` | AgentResponse Contract | Response Contract | `REQ-009` | 定义标准输出结构 |
| `API-012` | Gateway Entry Contract | Adapter Contract | `REQ-008` | 定义 UI 宿主与 access 网关之间的请求/响应适配 |
| `API-013` | Settings Adapter Bridge Contract | Adapter Contract | `REQ-001`, `REQ-005` | 定义基础设置层对外部系统和遗留资源的桥接边界 |

## 2. 接口 owner 规则

当前正式接口口径遵循“消费者定义向下依赖接口”：

| 层 | 拥有的接口类型 | 示例 |
|---|---|---|
| 接口/网关层 | 应用用例接口 | `RuntimeExecutionUseCase` |
| 业务调度层 | 领域服务接口 | `MemoryDomainService` |
| 业务模型层 | 基础能力接口 | `MemoryRecordRepositoryPort` |
| 基础能力层 | provider / backend 接口 | `LLMProviderPort`, `StructuredStoreProviderPort` |
| 基础设置层 | 不拥有上层逻辑接口，只做实现 | provider、store、bridge、container |

## 3. 关键契约

### `API-001` Agent App Manifest

核心字段：

- `id`
- `domain`
- `description`
- `workflows`
- `capabilities`
- `default_model_policy`
- `output_schemas`

约束：

- 不允许声明基础设置实现路径
- 只能引用已注册 capability 和 model policy

### `API-002` Workflow DSL

核心字段：

- `workflow.id`
- `workflow.inputs`
- `workflow.steps`
- `step.uses`
- `step.model_policy`
- `step.approval`
- `step.output_schema`
- `step.retry_policy`

约束：

- step 要么引用 capability，要么引用 llm task type
- 每个 step 必须有稳定输出 schema

### `API-003` ModelPolicy

核心字段：

- `provider`
- `model`
- `reasoning`
- `temperature`
- `budget`
- `fallback`
- `privacy`

约束：

- 业务层不得绕过 model policy 直接指定 provider SDK 参数

### `API-004` LLMProviderPort

必备方法：

- `validate_capability(policy)`
- `generate(request)`
- `stream(request)`
- `estimate_cost(request)`

约束：

- 返回值必须映射到统一 `LLMResponse`

### `API-005` Capability Contract

核心字段：

- `id`
- `input_schema`
- `output_schema`
- `writeset`
- `risk_level`
- `approval_required`
- `evidence_required`

### `API-006` Context Package & Recall Contract

核心字段：

- `recall_query.session_id`
- `recall_query.workflow_id`
- `recall_query.step_id`
- `recall_query.scope_filters`
- `recall_query.budget`
- `recall_bundle.pinned_records`
- `recall_bundle.retrieved_records`
- `recall_bundle.evidence_refs`
- `context_envelope.memory_segments`
- `context_envelope.evidence_segments`

约束：

- `Context Engine` 只能消费 `RecallBundle`，不能绕过记忆运行时直接拼长期记忆
- recall 结果必须保留来源 ref 与 diagnostics
- recall 的业务 owner 在 `MemoryDomainService` / `domain/memory`，`runtime` 只负责技术能力与 provider 接口

### `API-007` Session / Event / Memory Ledger Contract

核心字段：

- `session.id`
- `event.id`
- `event.type`
- `event.payload`
- `evidence.id`
- `evidence.source_ref`
- `memory_candidate.source_event_ids`
- `memory_candidate.evidence_ids`
- `memory_record.supporting_refs`
- `promotion_decision.status`

约束：

- event 与 evidence 是第一事实源
- memory record 必须带来源 refs，不能无证据写入长期层
- promotion 与 recall 必须解耦，不能因为 recall 命中就自动晋升长期记忆

### `API-011` AgentResponse

核心字段：

- `summary`
- `structured_output`
- `tool_calls`
- `evidence`
- `next_actions`
- `usage`

约束：

- 所有模型和工具结果最终都必须转换为该结构或其可验证子集

## 4. 错误与异常约束

- Provider 错误必须先标准化再向上抛出
- schema 校验失败必须返回结构化失败原因
- 高风险能力未获批准时返回 `approval_required`
- evidence 缺失导致的长期记忆写入必须返回结构化拒绝原因
- 写集冲突返回 `writeset_conflict`

## 5. 版本策略

- 契约优先保证字段稳定和可扩展
- 不允许在业务 App 中散落未登记的隐式契约
- 契约变化必须同步更新测试计划和接口矩阵

## 6. 版本记录

| 版本 | 日期 | 变更内容 |
|---|---|---|
| `v2.0` | 2026-04-13 | 重写 API 设计，将接口中心切换为平台契约、ports 和业务装配协议 |
| `v2.1` | 2026-04-14 | 扩展 `API-006` / `API-007`，正式纳入 recall bundle 与 memory ledger 契约 |
| `v2.2` | 2026-04-15 | 补齐六层架构下的接口 owner 规则，重命名 `API-012` / `API-013` 的正式语义 |
