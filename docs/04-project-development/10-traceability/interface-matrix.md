# 接口追踪矩阵

## 1. 文档目标

集中登记 `v2` 平台契约、提供方、消费方和测试覆盖。

## 2. 当前接口矩阵

| 接口编号 | 接口类型 | 提供方 | 消费方 | 关联需求 | 测试覆盖 | 负责人 |
|---|---|---|---|---|---|---|
| `API-001` | Access Use Case Contract | `AgentAppMaterializationUseCase` | API / CLI gateway | `REQ-002`, `REQ-010` | Manifest contract | 架构维护者 |
| `API-002` | Access Use Case Contract | `WorkflowDescriptionUseCase`、`RuntimeExecutionUseCase` | API / CLI gateway | `REQ-003`, `REQ-010` | Workflow / execution contract | 平台开发者 |
| `API-003` | Domain Policy Contract | `ModelDomainService`、`ModelPolicy` | 应用编排、模型相关领域 | `REQ-004` | ModelPolicy tests | 平台开发者 |
| `API-004` | Provider Contract | `LLMProviderPort`、`EmbeddingProviderPort` | 基础能力层模型能力 | `REQ-004` | Mock provider tests | 平台开发者 |
| `API-005` | Domain Capability Contract | `CapabilityDomainService`、`Capability*Port` | 应用编排、能力领域 | `REQ-005`, `REQ-007` | Capability contract | 平台开发者 |
| `API-006` | Context & Memory Contract | `ContextDomainService`、`MemoryDomainService` | 应用编排、网关查询 | `REQ-006` | Context / memory tests | 平台开发者 |
| `API-007` | Session & Evidence Contract | `SessionDomainService`、`SessionLedgerPort`、`EvidenceRepositoryPort` | 应用编排、memory 领域、审计 | `REQ-001`, `REQ-006`, `REQ-009` | Session replay tests | 平台开发者 |
| `API-008` | Approval Contract | `ApprovalDomainService`、`Approval*Port` | 应用编排、approval 领域 | `REQ-007` | Approval policy tests | 平台维护者 |
| `API-009` | Execution Backend Contract | `ToolExecutionProviderPort`、`WorkspaceProviderPort`、`ShellCommandProviderPort`、`GitProviderPort`、`HttpClientProviderPort` | 基础能力层执行能力 | `REQ-005`, `REQ-007` | Sandbox / tool backend tests | 平台维护者 |
| `API-010` | Delegation Contract | `DelegationDomainService`、`Delegation*Port`、`DelegationBackendPort` | 应用编排、delegation 领域 | `REQ-008` | Writeset conflict tests | 平台维护者 |
| `API-011` | Response Contract | `ResponseDomainService`、`Response*Port` | 应用编排、网关输出 | `REQ-009` | AgentResponse schema tests | QA |
| `API-012` | Gateway Binding Contract | `GatewayPort`、access gateways | CLI、HTTP、MCP、automation host | `REQ-008` | Gateway integration tests | 平台维护者 |
| `API-013` | Settings Provider Contract | `StructuredStoreProviderPort`、`SearchIndexProviderPort`、`VectorIndexProviderPort`、`RuleSourceProviderPort`、`ProfileSourceProviderPort` | 基础能力层 | `REQ-001`, `REQ-005`, `REQ-006` | Provider contract tests | 平台维护者 |

## 3. 维护规则

- 契约字段变更必须同步更新 `api-design.md` 与测试计划。
- 任何新的 provider、adapter 或 business app 接入，都必须声明其消费的 API 编号。
- 未登记的隐式接口不允许进入正式实现范围。
