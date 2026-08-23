# 接口与事件设计

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `DESIGN-API-001` |
| 正式版本 | `v3.1.0`（`v3.2.0` 候选修订待评审） |
| 来源候选 | `TASK-DESIGN-001-R019` |
| 发布事务 | `DESIGN-RELEASE-TX-R019-G001` |
| 负责人 | `HUMAN_API_INTEGRATION_LEAD` |
| 修改 / 审核 / 批准 | `uroborus` / `uroborus` / `uroborus` |
| 状态 | `v3.1.0` 已批准并生效；`v3.2.0` 候选修订待评审 |
| 上游 | `system-architecture`、`module-domain-design`、`data-design`、`PRD` |
| 下游 | `interface-reference`、`frontend-design`、`contract tests` |

## 文档职责

- 允许保存：API；命令；事件；请求响应字段；错误；权限；幂等；兼容。
- 禁止保存：公共使用教程；实现日志；数据库反向定义业务语义。
- 主要读者：架构、后端、前端、测试、集成方。

## 正式内容

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

---

**项目名称：** 山海工枢 / shanforge
**文档状态：** `v2` 架构细化总表
**负责人：** 仓库维护者
**主要读者：** 架构 | 平台开发 | 业务 Agent 开发 | 测试
**上游输入：** 系统架构 | 平台架构设计 | 模块边界
**下游输出：** 接口骨架 | 模块实现 | 测试计划
**最后更新：** 2026-04-15

## 1. 定稿原则

这份文档是当前分层、领域归属和接口 owner 的唯一细化入口。

正式依赖链只有一条：

```text
用户界面层 -> 接口/网关层 -> 业务调度层 -> 业务模型层 -> 基础能力层 -> 基础设置层
```

正式 owner 规则只有一条：

```text
每一层只拥有自己的业务逻辑；调用下层时，由调用方定义接口。
```

因此：

- 接口/网关层定义它依赖的应用用例接口。
- 业务调度层定义它依赖的领域服务接口。
- 业务模型层定义它依赖的基础能力接口。
- 基础能力层定义它依赖的基础设置 provider 接口。
- 基础设置层只做实现，不拥有上层逻辑和接口。

## 2. 六层总表

| 层      | 作用                | owner 逻辑                                | 下行依赖                   |
| ------ | ----------------- | --------------------------------------- | ---------------------- |
| 用户界面层  | Web、CLI Host、人机交互 | 页面、命令体验、交互编排                            | 接口/网关层 API / Protocol Gateway |
| 接口/网关层 | API 与协议收口 | 请求绑定、协议转换、出入参归一化                        | 业务调度层应用用例              |
| 业务调度层  | 用例编排、事务边界、流程协同    | run app、describe workflow、query session | 业务模型层领域服务              |
| 业务模型层  | 平台业务规则与领域逻辑       | 记忆、会话、流程、上下文、审批、委派、响应                   | 基础能力层统一能力              |
| 基础能力层  | 通用技术能力抽象          | 文件、存储、检索、模型、工具、规则源、时间、工作区等能力编排          | 基础设置层 provider         |
| 基础设置层  | 真实实现              | 文件系统、数据库、SDK、外部系统、容器装配                  | 无                      |

## 3. 每层领域模块细化

### 3.1 用户界面层

本仓当前不实现完整 UI，但正式宿主域要明确：

| 领域模块 | 说明 |
|---|---|
| `web_console` | Web 项目中的页面、会话交互、结果展示 |
| `cli_frontend` | 最终用户命令体验、参数组织、输出排版 |
| `automation_host` | 自动化触发界面、定时任务宿主 |

### 3.2 接口/网关层

| 领域模块 | 说明 | 代码落点 |
|---|---|---|
| `runtime_gateway` | 运行 Agent/App/Workflow 的统一入口 | `src/access/api/` |
| `app_gateway` | app materialize / describe 入口 | `src/access/api/` |
| `workflow_gateway` | workflow describe / choose 入口 | `src/access/api/` |
| `session_gateway` | session 查询与调试入口 | `src/access/api/` 目标接口 |
| `memory_gateway` | recall / explain / archive query 入口 | `src/access/api/` 目标接口 |
| `capability_gateway` | capability catalog / inspection 入口 | `src/access/api/` 目标接口 |
| `gateway_binding` | 原始协议与内部请求的绑定 | `src/access/ports/` |

### 3.3 业务调度层

| 领域模块 | 说明 | 当前或目标落点 |
|---|---|---|
| `app_application` | 编译、加载、校验 app | `src/application/app_compilation/` |
| `workflow_application` | workflow 选择、描述、入口编排 | `src/application/workflow_resolution/` |
| `session_application` | session 打开、恢复、查询、结束编排 | `src/application/session/` 目标细化 |
| `memory_application` | 调用 memory 领域服务完成 prepare / distill / explain | `src/application/` 目标细化 |
| `capability_application` | capability 查询与运行用例编排 | `src/application/` 目标细化 |
| `approval_application` | 高风险动作审批流程编排 | `src/application/` 目标细化 |
| `delegation_application` | 子任务委派和结果汇总编排 | `src/application/` 目标细化 |
| `response_application` | 最终输出装配与查询编排 | `src/application/` 目标细化 |
| `execution_application` | 组合上面各领域服务完成最终运行 | `src/application/execution/` |

### 3.4 业务模型层

这里是平台自身的业务逻辑 owner 层。

| 领域模块 | 说明 | 当前或目标落点 |
|---|---|---|
| `agent_app` | AgentApp、Manifest、业务声明 | `src/domain/agent_app/` |
| `workflow` | WorkflowDefinition、step 规则、状态推进 | `src/domain/workflow/` |
| `session` | session 生命周期、ledger、artifact 归属 | `src/domain/session/` |
| `memory` | recall、promotion、distill、archive、explainability | `src/domain/memory/` |
| `context` | 上下文组装规则、segment 规划、预算裁剪策略 | `src/domain/context/` |
| `model` | ModelPolicy、模型选择规则、推理预算策略 | `src/domain/model/` 与 `src/domain/agent_app/policies.py` |
| `capability` | capability 声明、风险级别、输入输出契约 | `src/domain/capability/` |
| `approval` | 审批规则、permit 判定、审计语义 | `src/domain/approval/` |
| `delegation` | 子任务语义、child result 合并规则 | `src/domain/delegation/` |
| `response` | 平台统一响应、结构化结果、evidence 输出 | `src/domain/response/` |

业务模型层的补充子域，当前先作为上面领域内部细化，不单独拉新大目录：

- `profile_resolution`
- `workspace_rule_bundle`
- `session_archive`
- `memory_dataset`
- `artifact_reference`

### 3.5 基础能力层

基础能力层不拥有平台业务逻辑，只拥有通用能力抽象。

| 领域模块 | 说明 | 当前或目标落点 |
|---|---|---|
| `file_access` | 文本、JSON、目录、路径资源访问 | `src/runtime/` 目标模块 |
| `structured_storage` | 结构化记录读写、分页查询、按键查找 | `src/runtime/` 目标模块 |
| `blob_storage` | 大对象或附件读写 | `src/runtime/` 目标模块 |
| `search_index` | 结构化搜索、全文检索、归档查询 | `src/runtime/` 目标模块 |
| `vector_index` | 语义检索、向量召回 | `src/runtime/` 目标模块 |
| `llm_gateway` | 文本生成、结构化生成、模型路由 | `src/runtime/llm/` |
| `embedding_gateway` | 向量化能力 | `src/runtime/` 目标模块 |
| `tool_execution` | 通用工具/能力执行 | `src/runtime/capability/` 目标收口 |
| `workspace_access` | workspace root、路径白名单、资源定位 | `src/runtime/ports/workspace.py` 目标扩展 |
| `rule_source` | 规则文件与工作区规则加载 | `src/runtime/` 目标模块 |
| `profile_source` | profile 解析与加载 | `src/runtime/` 目标模块 |
| `approval_channel` | 人工审批通道、审批后端适配 | `src/runtime/` 目标模块 |
| `delegation_transport` | worker/backend 派发与回收 | `src/runtime/delegation/` |
| `shell_gateway` | shell 执行能力 | `src/runtime/` 目标模块 |
| `git_gateway` | git 读写能力 | `src/runtime/` 目标模块 |
| `http_gateway` | 对外 HTTP 调用能力 | `src/runtime/` 目标模块 |
| `clock_identity` | 时间、ID、trace 生成 | `src/runtime/` 目标模块 |

### 3.6 基础设置层

| 实现分区 | 说明 | 当前落点 |
|---|---|---|
| `provider_adapters` | OpenAI、Anthropic、HTTP、shell、git、workspace 等外部实现 | `src/adapters/` |
| `storage_backends` | JSONL、数据库、索引、blob storage 等持久化实现 | `src/storage/` |
| `container_bootstrap` | settings、provider 选择、实现装配 | `src/bootstrap/` |

## 4. 接口 owner 总表

### 4.0 用户界面层消费的契约

用户界面层不向下定义本仓代码接口，但必须消费下列稳定入口：

| UI 宿主契约 | 说明 | 对应下层接口 |
|---|---|---|
| `RuntimeGatewayClient` | 发起运行、读取执行结果 | `RuntimeExecutionUseCase` |
| `WorkflowGatewayClient` | 查看 workflow 描述与可选项 | `WorkflowDescriptionUseCase` |
| `SessionGatewayClient` | 查询 session、回放、诊断 | `SessionInspectionUseCase` |
| `MemoryGatewayClient` | 查询 recall 和 explainability | `MemoryInspectionUseCase` |
| `CapabilityGatewayClient` | 查看 capability 目录与风险级别 | `CapabilityCatalogUseCase` |
| `PlatformHealthClient` | 健康检查、就绪性检查 | `PlatformHealthUseCase` |

### 4.1 接口/网关层拥有的接口

这些接口描述 access 对 application 的依赖。

| 接口 | 作用 | 代码文件 |
|---|---|---|
| `AgentAppMaterializationUseCase` | materialize app | `src/access/ports/application_use_cases.py` |
| `WorkflowDescriptionUseCase` | describe workflow | `src/access/ports/application_use_cases.py` |
| `RuntimeExecutionUseCase` | run app / run manifest | `src/access/ports/application_use_cases.py` |
| `SessionInspectionUseCase` | query session | `src/access/ports/application_use_cases.py` |
| `MemoryInspectionUseCase` | memory recall / explain | `src/access/ports/application_use_cases.py` |
| `CapabilityCatalogUseCase` | list capabilities | `src/access/ports/application_use_cases.py` |
| `PlatformHealthUseCase` | health / readiness | `src/access/ports/application_use_cases.py` |

### 4.2 业务调度层拥有的接口

这些接口描述 application 对 domain 的依赖。

| 接口 | 作用 | 代码文件 |
|---|---|---|
| `AgentAppDomainService` | app 编译/校验 | `src/application/ports/domain_services.py` |
| `WorkflowDomainService` | workflow 选择与状态入口 | `src/application/ports/domain_services.py` |
| `SessionDomainService` | open / complete / fail session | `src/application/ports/domain_services.py` |
| `MemoryDomainService` | prepare / recall / distill / explain | `src/application/ports/domain_services.py` |
| `ContextDomainService` | compile context | `src/application/ports/domain_services.py` |
| `ModelDomainService` | model policy resolve | `src/application/ports/domain_services.py` |
| `CapabilityDomainService` | capability catalog / invoke | `src/application/ports/domain_services.py` |
| `ApprovalDomainService` | approval / sandbox decision | `src/application/ports/domain_services.py` |
| `DelegationDomainService` | plan / dispatch / collect / merge | `src/application/ports/domain_services.py` |
| `ResponseDomainService` | normalize response | `src/application/ports/domain_services.py` |

### 4.3 业务模型层拥有的接口

这些接口描述 domain 对基础能力层的依赖。

| 领域 | 主要下行接口文件 |
|---|---|
| `agent_app` | `src/domain/agent_app/ports.py` |
| `workflow` | `src/domain/workflow/ports.py` |
| `session` | `src/domain/session/ports.py` |
| `memory` | `src/domain/memory/ports.py` |
| `context` | `src/domain/context/ports.py` |
| `model` | `src/domain/model/ports.py` |
| `capability` | `src/domain/capability/ports.py` |
| `approval` | `src/domain/approval/ports.py` |
| `delegation` | `src/domain/delegation/ports.py` |
| `response` | `src/domain/response/ports.py` |

### 4.4 基础能力层拥有的接口

这些接口描述 runtime/basic-capability 对基础设置 provider 的依赖。

| provider 接口分组 | 代码文件 |
|---|---|
| 数据访问 provider | `src/runtime/ports/data_access.py` |
| AI provider | `src/runtime/ports/ai_backends.py` |
| 源数据 provider | `src/runtime/ports/source_backends.py` |
| 执行 backend provider | `src/runtime/ports/execution_backends.py` |

### 4.5 基础设置层实现责任

基础设置层不再新增上层逻辑接口，但会实现两类接口：

- domain-owned 持久化端口：例如 session / artifact / memory / evidence / dataset 相关仓储接口
- runtime-owned provider 接口：数据访问、AI、源数据、执行 backend 等 provider 接口

## 5. 领域接口清单

### 5.1 `agent_app` 领域

- 上行实现：`AgentAppDomainService`
- 下行能力：
  - `AgentAppCatalogPort`
  - `AgentAppSchemaValidationPort`

### 5.2 `workflow` 领域

- 上行实现：`WorkflowDomainService`
- 下行能力：
  - `WorkflowDefinitionCatalogPort`
  - `WorkflowRuleEvaluationPort`
  - `WorkflowInstructionRenderPort`

### 5.3 `session` 领域

- 上行实现：`SessionDomainService`
- 下行能力：
  - `SessionLedgerPort`
  - `SessionArtifactStorePort`
  - `SessionClockPort`
  - `SessionIdentityPort`

### 5.4 `memory` 领域

- 上行实现：`MemoryDomainService`
- 下行能力：
  - `MemoryRecordRepositoryPort`
  - `EvidenceRepositoryPort`
  - `MemoryDatasetRepositoryPort`
  - `MemoryArchiveQueryPort`
  - `MemoryProfileResolverPort`
  - `MemoryRuleBundlePort`
  - `MemoryReasoningPort`
  - `MemorySemanticSearchPort`

### 5.5 `context` 领域

- 上行实现：`ContextDomainService`
- 下行能力：
  - `ContextRuleBundlePort`
  - `ContextTokenEstimationPort`
  - `ContextRenderingPort`

### 5.6 `model` 领域

- 上行实现：`ModelDomainService`
- 下行能力：
  - `ModelInvocationPort`
  - `ModelMetadataPort`
  - `EmbeddingGenerationPort`

### 5.7 `capability` 领域

- 上行实现：`CapabilityDomainService`
- 下行能力：
  - `CapabilityCatalogPort`
  - `CapabilityExecutionPort`
  - `CapabilityWorkspacePort`
  - `CapabilityHttpPort`
  - `CapabilityShellPort`
  - `CapabilityGitPort`

### 5.8 `approval` 领域

- 上行实现：`ApprovalDomainService`
- 下行能力：
  - `ApprovalRequestPort`
  - `ApprovalDecisionQueryPort`
  - `ApprovalAuditPort`

### 5.9 `delegation` 领域

- 上行实现：`DelegationDomainService`
- 下行能力：
  - `DelegationWorkerDispatchPort`
  - `DelegationResultCollectionPort`
  - `DelegationWorkspacePort`

### 5.10 `response` 领域

- 上行实现：`ResponseDomainService`
- 下行能力：
  - `ResponseSchemaValidationPort`
  - `ResponseArtifactResolverPort`
  - `ResponseUsageAccountingPort`

## 6. 当前实现迁移原则

当前仓库已经存在一批实现代码，但从现在开始，目标结构按这份总表收口：

- 不再把记忆、上下文、审批、委派这类平台业务逻辑放在基础能力层 owner 位置。
- 基础能力层只保留通用技术能力抽象与实现编排。
- 业务逻辑 owner 一律回到业务模型层。
- 这轮先立接口，不做实现迁移。

## 7. 本轮交付范围

本轮只做两件事：

1. 用这份文档把层、领域、接口 owner 一次定稿。
2. 在代码里新增接口契约骨架，不写任何实现。

---

## 16. WP-03 确定性路由、运行状态机和 Gate

### 16.1 生命周期阶段登记

Catalog 以 `LC-00` 至 `LC-13` 的 14 条 `lifecycle_stage` 记录保存阶段事实。每条记录都具有进入条件、必做工作、阶段输出、退出 Gate、允许回退目标、负责人和来源需求。阶段不是只能向前的瀑布：新事实必须通过变更 Workflow 回到有事实所有权的上游阶段，并把受影响下游标为待复核或失效。

| 阶段组 | 阶段 | 确定性边界 |
|---|---|---|
| 会话与基线 | `LC-00`、`LC-01` | 所有项目消息先经过治理；缺项目 Baseline 时不能直接进入需求、设计或实现 |
| 发现与产品 | `LC-02`、`LC-03` | 调研事实和正式需求分离；需求只有发布后才能作为设计权威输入 |
| 体验与设计 | `LC-04` 至 `LC-08` | UX、UI、架构、数据和 API 各有独立输入输出与 review Gate，不互相隐式替代 |
| 计划与交付 | `LC-09` 至 `LC-12` | 计划、实现、测试、独立 review、人工确认和高风险交付逐节点推进 |
| 运行演进 | `LC-13` | 运行事实、事件、变更、迁移和退役受生产权限与人工 Gate 约束 |

阶段完成必须同时满足：必需 Artifact 存在且 schema 合法、追踪闭合、新鲜验证通过、独立 review 关闭阻断项、适用人工决定有效、状态与版本同步。文件存在、模型声明或旧证据不能完成阶段。

### 16.2 RouteInput 与候选信号

`RouteInput` 是规则系统的唯一入参，至少包含：

| 字段组 | 必填字段 | 规则 |
|---|---|---|
| 身份与版本 | `route_request_id`、`session_id`、`project_id`、`catalog_revision`、`catalog_sha256`、`evaluated_at` | Catalog 版本/hash 不一致时拒绝裁决 |
| 当前执行位置 | `current_stage_id`、`current_workflow_run_id`、`current_node_run_id`、`work_item_id`、`task_card_id` | 不存在时显式为 `null`，不能靠聊天记忆补齐 |
| 当前 Gate | `pending_gate`、`pending_gate.subject_ref/hash`、`resume_target` | Gate 绑定对象变化后旧决定失效 |
| 模型候选 | `candidate_signals`、`target_artifact_class`、`target_scope`、`change_kind`、`message_relation` | 模型只提取候选，不得写最终 rule/workflow/node |
| 项目影响 | `project_effect`、`risk_level`、`requested_action_kind` | 枚举分别约束无影响、候选事实、正式事实、运行事实及风险级别 |
| 权限与事实 | `authorization_refs`、`role_assignment_ref`、`fact_snapshot_refs`、`fact_conflict` | 调用方自称“已授权/最新”不产生资格 |

候选信号保留提取器 ID、来源片段 hash、值和置信信息，供审计和澄清使用；置信度不参与最终优先级。`model_selected_rule_id`、`model_selected_workflow_id` 等字段即使出现也必须被忽略并记录为越界候选。

### 16.3 RouteDecision 与固定裁决算法

`RouteDecision` 必须保存输入 hash、规则集版本/hash、裁决结果、命中 rule、Workflow/Node、允许 ActionSpec、WorkItem/TaskCard 策略、拒绝候选及原因、允许读写集、Gate、幂等键和规则系统主体。结果枚举为 `selected`、`needs_user_input`、`blocked`、`needs_human_decision`；不存在模型自由文本结果。

固定优先级如下：

| 优先级 | RouteRule | 命中条件 | 目标解析 |
|---:|---|---|---|
| 700 | `RR-PENDING-HUMAN-GATE-001` | 存在待决人工 Gate；批准、退回、暂停或新请求都先做 Gate 响应分类 | 只恢复 Gate 指定 Workflow/Node |
| 600 | `RR-CURRENT-TASK-NODE-001` | 当前 TaskCard 有未完成 Node，消息是继续、反馈或状态控制 | 只恢复 TaskCard 登记位置 |
| 500 | `RR-BUG-FAILURE-001` | 报告失败、异常、测试失败或运行事故 | 由 Catalog 的 bug/failure trigger 唯一选择 |
| 400 | `RR-EXPLICIT-CHANGE-001` | 明确新增、变更、删除、迁移、弃用或退役 | 按变更类型和事实 owner 唯一选择 |
| 300 | `RR-TARGET-ARTIFACT-001` | 目标产物明确且无更高优先级命中 | 按 Artifact Class、目标范围和项目影响选择 |
| 200 | `RR-LIFECYCLE-STAGE-001` | 目标阶段明确 | 只选择该阶段允许进入的 Workflow |
| 100 | `RR-DIRECT-ANSWER-001` | 项目影响为 `none` 且只需解释/建议 | 固定 `WF-CTL-002`，不建任务、不写项目事实 |
| 0 | `RR-UNCLASSIFIED-GUARD-001` | 前七层没有唯一结果 | 缺字段进入 `WF-CTL-003`；无登记动作进入 `WF-CTL-008` |

规则系统按以下顺序执行，不允许模型改序：

1. 校验 RouteInput schema、Catalog hash、当前状态和事实快照；事实冲突立即 `blocked_by_fact_conflict`。
2. 按优先级从高到低计算普通规则；同层恰好一个命中才成为候选，高层唯一候中后低层只记录为 rejected candidate。
3. 同层多命中返回 `blocked/route_conflict`；零命中根据缺失字段进入澄清，已知动作不在 Catalog 则进入扩展阻断。
4. 解析目标 Workflow/Node 后核对 WorkItem/TaskCard 归属、ActionSpec 登记、Role Assignment、允许读写集和 Gate。
5. 高风险、远端、PR、merge、生产、不可逆和正式批准缺精确人工授权时返回 `needs_human_decision`，写入次数为 0。
6. 生成不可变 RouteDecision；只有 `selected` 且所有进入条件通过时才能创建 WorkflowRun。

### 16.4 WorkItem、TaskCard 和执行归属

| 项目影响 | WorkItem | TaskCard | Ledger/文件 |
|---|---|---|---|
| `none` | 不创建 | 不创建 | 不写项目事实 |
| 影响后续项目事实 | 创建或复用唯一 owner | 仅在跨会话、依赖、验收或 review 时创建/复用 | 只写当前 WorkItem 的允许位置 |
| 当前 TaskCard 内部工作包/步骤 | 复用 | 复用，不建“落档/版本/复审”孤岛任务 | 写 NodeRun、ActionRun、evidence、draft/report/review |
| 找到多个 owner 或没有 owner | 不猜测 | 不创建 | 阻断并列候选与恢复条件 |

TaskCard 目标覆盖候选、验证、review、人工批准、正式发布、版本同步和草案处置的完整生命周期。Session、工作包、方法步骤、工具调用、Gate 和文件编辑是 Node/ActionRun/Event，不因“也是工作”自动升级为 TaskCard。

### 16.5 四级运行状态机

运行状态只由 `SYSTEM_RULE_ENGINE` 根据合法输入、当前状态和证据推进；人类、AI 和 Reviewer 产生决定或执行证据，但不能直接改状态字段。

| 状态机 | 初态/终态 | 关键主链 | 主要异常分支 |
|---|---|---|---|
| `SM-SESSION-001` | `received` / `stopped|waiting_user|waiting_review|blocked|failed|cancelled` | classifying → restoring_if_projectized → routing → scoping → announcing → executing → validating → persisting → handoff | `classifying` 只使用当前消息和当前对话；direct/lightweight 从 classifying 直接到 handoff，不进入 restoring/routing；项目化请求恢复后才完成路由；所有失败也先进入 handoff 再停止，保证用户可见 |
| `SM-WORKFLOW-RUN-001` | `received` / `closed|cancelled` | routed → scoped → prepared → executing → validating → reviewing → pending_human_confirmation → formalizing_or_delivering → closed | needs_user_input、blocked、failed、changes_requested、paused 均有显式恢复或取消边 |
| `SM-NODE-RUN-001` | `pending` / `completed|cancelled` | ready → executing → validating → output_ready → completed | waiting_review、waiting_human、changes_requested、needs_user_input、blocked、failed、paused、compensating |
| `SM-ACTION-RUN-001` | `prepared` / `committed|duplicate_noop|conflict_blocked|compensated|cancelled` | authorized → executing → succeeded → committed | failed、uncertain、compensating；未知副作用不得直接重试 |

每条转换具有唯一 transition ID、from/to、触发事件、所需证据、guard 和结果原因码。Validator 对每个运行状态机验证：初态存在、所有状态可达、非终态可到终态、终态无出边、引用无孤立、转换 ID 唯一。

`restoring_if_projectized` 是条件节点：`classifying` 初判为项目状态查询、任务延续、项目事实变更或仓内持久化后，才允许读取 `.factory/memory/` 和当前 work item ledger，再用恢复后的事实完成 routing。`direct_answer` / `lightweight_analysis` 且 `project_effect=none` 时必须跳过恢复与完整路由，也不得写项目文件或项目状态。

### 16.6 GateDecision、ReviewDecision 和 HumanDecision

三种决定不能复用同一状态词或互相推导：

| 对象 | 合法主体 | 结果 | 能做什么 | 不能做什么 |
|---|---|---|---|---|
| `GateDecision` | `SYSTEM_RULE_ENGINE` | `pass|deny|blocked|needs_user_input|needs_human_decision` | 根据 schema、权限、证据和状态确定能否前进 | 生成业务批准或风险接受 |
| `ReviewDecision` | `HUMAN_REVIEWER` 或 `AI_INDEPENDENT_REVIEWER` | `approved|changes_requested` | 对绑定变更包给出发现和评审结论 | 修改对象、正式批准、创建 PR、生产授权 |
| `HumanDecision` | 具有对应专有权利的 `human` 实例 | `approved|changes_requested|paused|risk_accepted|authorized|rejected` | 对精确对象/hash、范围和下一动作作最终决定 | 覆写已发生 ActionRun、测试或生产观测 |

固定 Gate 类型为：`entry`、`output_contract`、`verification`、`independent_review`、`human_decision`、`explicit_authorization`、`formalization_release`。每个决定都绑定 subject ID/hash、WorkflowRun/NodeRun、角色/主体实例、证据、时间、有效期、幂等键和 supersedes/corrects 关系。

`ReviewDecision=approved` 只能把 WorkflowRun 推到 `pending_human_confirmation`；不能产生 `HumanDecision`。Critical/Important 未关闭时，除非人类以绑定对象的 `risk_accepted` 明确接受，人工批准 Gate 必须拒绝。人工退回后旧 review 只保留历史资格，任何对象 hash 变化都要求重新验证和 review。

PR 授权必须明确包含 `action_kind=create_pull_request`、仓库、源/目标分支、草稿状态、授权人、绑定提交/evidence、有效期和单次/重复策略。“继续”“任务完成”“已提交”“review approved”均不能推导 PR 授权；push、PR、merge 各自是独立授权对象。

### 16.7 幂等、恢复和补偿

Action 幂等键由 `project/work_item/task_card/workflow/node/action_spec/normalized_input_hash/target_identity` 规范化生成，不使用 Session ID 作为唯一键。重复执行按追加式 ActionRun 决定：

| 已有记录 | 新请求 | 决定 |
|---|---|---|
| 无 | schema、权限和 Gate 通过 | `execute` |
| 同键、同 payload，原结果已 committed | 任意 Session 重放 | `duplicate_noop`，返回原 ActionRun，不重复写 |
| 同键、不同 payload | 任意 | `conflict_blocked`，要求新键或人工纠正 |
| 原状态 `uncertain` | 重试 | `reconcile_required`，先读取目标副作用和幂等回执 |
| 原状态 failed 且明确可重试 | 重试预算未耗尽 | 创建带 `retry_of` 的新 ActionRun |
| 补偿失败或不可逆副作用未知 | 任意 | `blocked`，进入人工恢复 |

Session 恢复只读取会话卡、当前 TaskCard、ledger 中最新有效 RouteDecision/ActionRun/GateDecision 及其直接证据。恢复点是最后一个 `committed` ActionRun；`executing`、`uncertain`、半行、hash 冲突或目标读回不唯一时不能自动重放。

失败处理固定为：缺输入不写项目事实并等待用户；路由冲突/事实冲突/越权阻断；验证失败保留候选和新鲜证据但正式写入为 0；执行前失败按重试策略处理；执行后未知先 reconcile；可逆副作用按 ActionSpec 逆序补偿；不可逆或补偿失败由人工决定。用户新消息改变方向时，只取消尚未开始的后续 Action，已完成事实和证据保留，正在执行动作先到安全停止点并记录状态。

### 16.8 WP-03 可执行验证

WP-03 使用持久 validator 的 `cp02 --phase wp03` 阶段校验；该命令只证明 WP-03 完整，不声称 CP-02 已到达。至少执行以下真实求值：

- 路由：唯一命中、零命中、同层多命中、缺字段、当前 Gate 优先、当前 Task 优先、Bug 优先、直接咨询不落盘、事实冲突、模型越界候选和 PR 未授权。
- Gate：review approved 只能进入人工确认、作者不能独立 review、AI 不能产生 HumanDecision、对象 hash 漂移使决定失效、显式 PR 授权通过。
- 幂等：首次执行、同 payload 重放 no-op、同键不同 payload 冲突、uncertain 必须 reconcile、可重试失败和补偿失败阻断。
- 状态机：4/4 运行状态机图闭合，所有 transition ID 唯一，所有停止与继续分支有原因码和恢复条件。
- 回归：`cp01@0.5.0` 的 56 条共享规则 hash、17 类 Artifact、96 条转换正例及既有负例保持通过。

WP-03 的 UI 适用性为 `N/A`：它不交付图形控制台。替代验收机制是机器状态转换表、RouteDecision/GateDecision 记录和会话可见性要求；具体中文回复模板由 WP-06 交付。P002 已接受该 N/A，WP-03 未改变其原因、影响或替代机制。

### 16.9 需求覆盖与下一停止点

WP-03 结算 `REQ-AI-WORKFLOW-001`、`002`、`015`、`033`、`046` 和 `NFR-AI-WORKFLOW-006`、`007`、`009` 共 8 条覆盖记录。它们分别落到 `TOP-SPEC-WORK-SESSION-001`、`SM-WORKFLOW-RUN-001` 及同组路由/运行对象，并绑定 `TASK-DESIGN-001-verification.md#wp-03`。

WP-03 完成后的唯一下一工作包是 WP-04：生成 123 条 Workflow 与 597 个 ActionSpec，并解析 1359 个待设计槽。只有 WP-04 完成、`cp02` 完整 profile 通过并冻结当前设计/Catalog/validator hash 后，才到 CP-02 独立只读评审；本节不能提前产生 CP-02 approved、人工批准或正式发布资格。

## 17. WP-04 123 条工作流程与原子动作规范设计

### 17.1 转换边界和机器事实源

WP-04 不人工重抄 123 份流程正文。生成器只读取已冻结的 R006 工作流程映射，以 `workflow_id` 选择一条 JSONL 记录，再按该记录内的 RFC 6901 JSON Pointer 读取字段。机器目录是完整定义；本中文候选只解释公共规则和代表性流程。

| 上游库存 | 数量 | WP-04 目标 |
|---|---:|---|
| 工作流程身份 | 123 | 123 条 `workflow`，标题、阶段、目标和触发语义不变 |
| 动作位置 | 597 | 每个源位置唯一解析到一条源 `action_spec`；复合高风险动作还必须拆为独立 operation ActionSpec |
| 黑盒场景身份 | 369 | 每条流程各有正常、缺输入、越权或冲突三类 `test_case` |
| 方法引用 | 123 | 解析到稳定 Method ID，定义责任人为 WP-05 |
| 工具策略引用 | 384 | 解析到 4 个稳定 ToolPolicy ID，定义责任人为 WP-06 |
| 输出契约 | 209 组 | 每组 schema、路径、验证和保留四类引用均解析 |
| 元数据待设计槽 | 16 | 14 个 Artifact 路径、ActionSpec Registry 和精确路径 Registry 均解析 |

源值只允许保留在 `source_binding` 或迁移记录的 `source_value` 中作为审计证据。任何运行字段、目标字段或解析后的引用仍含 `design_required`、为空或指向不存在对象，都视为未完成。

### 17.2 工作流程图契约

每条 `Workflow` 至少保存：稳定 ID/版本、生命周期阶段、目标、触发、受控意图码、规范绑定、角色、输入、输出、节点、边、ActionSpec 引用、RouteRule、Method/ToolPolicy 绑定、失败分支、Gate、停止与恢复规则、回复模板和场景 ID。

`WorkflowNode` 只描述图位置、顺序、主体选择器和 `ActionRef`；动作如何执行由 `ActionSpec` 单独定义。相邻源动作转为显式有向边，只有当前动作已提交且节点输出门通过时才能前进。失败分支优先于正常边，最终节点完成后仍需计算工作流程级 Gate，不能因“最后一个动作已运行”直接完成。

流程图属于机器目录的生成投影：Mermaid 或其他可视化必须从节点和边生成并绑定当前 Catalog SHA-256；手工流程图不是事实源。这样既能查看全图，也避免维护 123 份会漂移的 Markdown。

### 17.3 原子动作规范

597 条源 `ActionSpec` 与源工作流程节点一一对应。复合高风险源节点可以引用多个 operation ActionSpec，但父动作本身不得直接产生副作用；每个 operation 只对应一种动作和一个可观察结果。公共字段如下：

| 契约 | 规则 |
|---|---|
| 主体 | 固定人类、固定 AI、固定规则系统，或确定性独立 Reviewer 选择器；必须先通过 Role Assignment |
| 输入 | 当前 Workflow 声明输入、前一动作输出和直接权威证据；禁止隐式扩大读取范围 |
| 输出 | 中间动作只产生本任务证据；末动作产生工作流程声明输出；Reviewer 和人工决定写入各自专用 Artifact |
| 方法与工具 | 引用稳定 ID 和要求版本；未到定义工作包时必须登记 owner 和 `deferred_until_wp`，不得留空 |
| 原子性 | 一条 ActionSpec 只能产生一个可观察结果，不能捆绑无关工作，空结果不能算成功 |
| 验证 | 核对主体、输入绑定、输出 schema、路径范围、hash 回读和 Gate 结果 |
| 幂等 | 键由项目、WorkItem、TaskCard、Workflow、Node、ActionSpec、规范化输入 hash 和目标身份组成 |
| 补偿 | 读取/决定类动作追加纠正记录；可逆写入按前像逆序恢复；副作用不确定时停止并核对，禁止盲重试 |
| 继续 | 成功进入唯一下一节点或工作流程 Gate；失败选择显式失败分支；不确定进入人工恢复 |

每条工作流程固定包含五类失败分支：缺输入、路由或事实冲突、权限或角色拒绝、工具或验证失败、评审退回。每个分支都声明允许写入数、结果状态和恢复位置。

### 17.4 确定性路由和主体选择

123 条工作流程级 RouteRule 在全局八层路由规则完成分类后参与目标解析。候选提取器可以提出受控 `INTENT-<WORKFLOW-ID>`，但 `WORKFLOW-TARGET-EVALUATOR-001` 必须同时验证精确意图、生命周期阶段、工作流程存在性和同层唯一性。零匹配要求澄清，多匹配阻断；模型直接写入的 workflow ID 没有最终权威。

R006 中 30 个 `one_of` Reviewer 动作统一转换为 `REVIEWER-INDEPENDENCE-001`：候选只能是人类 Reviewer 或独立 AI Reviewer，当前作者实例必须排除，角色绑定必须有效，一次评审不能混用两类主体。读取评审输入、执行评审、给出发现和输出结论均受同一 Reviewer assignment 约束；作者不能自批。

### 17.5 输出契约注册表

17 类 Artifact 各登记四种稳定引用，共 68 个引用：

1. `schema_ref`：要求 Artifact ID、主类别、事实域、状态、内容 hash 和来源引用。
2. `path_mapping_ref`：复用 Artifact Registry 的唯一 resolver、位置键和无法解析时的阻断结果。
3. `validation_ref`：校验 schema、主类别、事实域、状态、路径、内容 hash 和事实资格；文件存在或空内容不足以通过。
4. `retention_ref`：复用该 Artifact 的保留、归档、删除和 legal hold 契约。

209 组输出必须逐字段引用该注册表。源输出的标签、主类别、事实域和成功状态保持不变；路径和 schema 等设计字段必须替换为可解析目标。

### 17.6 逐指针迁移与防伪完成

每条迁移记录保存源 Catalog/修订、源记录 ID、源 JSON Pointer、源值及其 SHA-256、目标记录/字段、迁移类别、解析状态、后续 owner 和验证证据。唯一键是 `source_record_id + source_json_pointer`。

| 迁移类别 | 数量 | 验收 |
|---|---:|---|
| 身份迁移 | 1089 | 123 工作流程 + 597 ActionSpec + 369 test_case；目标值必须与源身份完全相同 |
| 待设计槽迁移 | 1359 | 123 Method + 384 ToolPolicy + 836 输出引用 + 16 元数据槽；目标不得为空或仍含待设计标记 |
| 总计 | 2448 | 每个源指针恰好一条记录，每个目标可读取，无多余、遗漏或孤立记录 |

验证器内置删除工作流程、删除迁移记录、只重命名源待设计标记、把目标引用置空四类反例。四类都必须失败，防止通过删字段或改字符串制造“已完成”。

### 17.7 高风险、评审和代表性语义检查

高风险工作流程由源 Gate 判定，共 15 条。每条必须同时存在：固定 `HUMAN_APPROVER` 人类节点、`GATE-HUMAN-DECISION-001`、`GATE-EXPLICIT-AUTHORIZATION-001`，以及绑定动作种类、目标、范围、有效期和重复策略的决定。分支、Push、PR、Merge、部署、回滚、数据修正和退役之间不能复用授权；PR 仍须每次由人类明确确认。

CP-02 语义抽查覆盖 14 个生命周期阶段，并固定检查：`WF-CTL-002` 只读咨询、`WF-CTL-008` Catalog 扩展治理、`WF-CTL-009` 正式文档治理、`WF-DEL-002` 独立评审，以及全部 15 条高风险流程。旧测试中不存在的 `WF-TEST-009` 已纠正为真实目录目标 `WF-QA-009`；路由目标不在当前 Catalog 时必须阻断。

### 17.8 受控后续定义和检查点

WP-04 为后续 owner 建立的是稳定身份，不是完成声明：14 个生命周期 Method 由 WP-05 扩展成 17 个封闭方法域并绑定 Skill；4 个 ToolPolicy 和 7 个 ResponseTemplate 由 WP-06 完整定义；369 个源场景由 WP-08 增加可执行 fixture 和完整负例。除这三类已登记延期外，WP-01 至 WP-04 的字段不得延期。

R001 的 `cp02` 作者验证曾通过 123/123 工作流程、597/597 源 ActionSpec、369/369 源 test_case 和 2448/2448 迁移，但独立对抗评审发现路由和高风险授权存在假阳性，因此 R001 已失效。R002 必须同时验证 597 条源 ActionSpec、29 条高风险 operation ActionSpec、15 条高风险流程和 30 个独立 Reviewer 节点，才能重新冻结复审。

## 20. WP-05 全生命周期方法卡与 Skill 映射

### 20.1 十七个封闭方法域

方法域固定为：项目基线、发现/调研/Spike、需求、UX、UI、架构/领域/模块、数据/数据库、API/集成、计划/任务、实现/多端交付、测试/调试/根因、安全/隐私/合规、性能/可靠性/可观察性、Review/Verification/人工确认、Git/PR/发布/部署/回滚、运维/事件/问题/备份恢复、变更/迁移/弃用/退役。每个 Method 都有版本、适用 Workflow、权威输入、五步执行法、输出契约、Review Rubric、SkillBinding、PromptTemplate、失败回退和能力缺口。

123 条 Workflow 按业务语义绑定主方法，不只按生命周期阶段机械归类。例如安全架构、数据隐私和安全测试进入安全方法；性能架构、查询容量和负载测试进入可靠性方法；数据迁移、依赖升级和 API 弃用进入变更方法；本地提交到生产回滚进入 Git/发布方法。17 个方法均至少被一条 Workflow 使用，未绑定 Workflow 为 0。

### 20.2 本地 Skill 绑定与缺口

代理宿主直接从当前 `skills/*/SKILL.md` 的目录与 frontmatter 发现能力；该文件系统是唯一能力清单，正式设计不冻结数量、文件哈希或另建 SkillBinding 目录。Workflow 只在任务命中具体 Skill 的触发边界时读取其合同，不把同一 Method 涉及的全部 Skill 无差别加载。

`gitcommitzh` 只绑定本地提交工作流程 `WF-DEL-004`，只产出本地 commit SHA、中文提交说明和提交范围验证；分支、Push、PR、Merge、发布和部署均在其禁止范围内。`requesting-code-review` 只组织评审，`verification-before-completion` 只产生新鲜验证证据；二者即使服务发布流程也不能执行远端或生产副作用。Skill 只执行方法内动作，不能替代确定性路由、角色授权、独立 Review 或 HumanDecision。

数据库、安全/SRE、远程 PR/部署和生产运维缺少可独立承担专业裁决的本地 Skill，分别登记到 `HUMAN_DATABASE_LEAD`、`HUMAN_QUALITY_SECURITY_LEAD` 和 `HUMAN_RELEASE_OPERATIONS_LEAD`。这些缺口允许 AI 准备材料和运行已授权工具，但禁止 AI 假装已完成专业审核或生产授权。

### 20.3 项目资料交互方法

项目资料收集先回读 `.factory/project.json` 和已确认事实，已知字段不重复询问；缺失字段按每批最多三个问题交互。必须覆盖真实人员与角色、产品表面、服务、环境、质量、安全、合规和确认记录。人员姓名、审核人、批准人取不到时必须询问，不能写 AI 产品名或模型名代替。每轮回复列出已确认、仍缺失、阻断项和保存位置。

### 20.4 UX、UI、数据库和 API 专门方法

- UX：从 Persona/Jobs、真实场景和内容形成旅程、服务蓝图、信息架构、任务流、线框/原型及可用性/A11y 验收。
- UI：输出设计系统/Token、页面和组件清单、完整状态矩阵、响应式/A11y、真实视觉资产、桌面/移动截图验证和开发交接；实现提示必须沿用项目框架与组件库，不能用营销页面代替实际工作界面。
- 数据库：从 BusinessField、领域规则、查询和事务推导 ERD、字段字典、主外键/唯一/检查约束、查询-索引矩阵、容量、迁移/回填/校验/回滚和数据库 Review Rubric。
- API：先列消费者、用例、资源/操作和权限边界，再定义 endpoint/event、请求响应 schema、稳定错误 code、分页/过滤/幂等/限流、兼容/弃用、OpenAPI 和 Contract Test。

数据库列、API 字段和 UI 控件仍必须引用同一 BusinessField ID；具体跨层字段结构和断链验证由 WP-07 完成，WP-05 不提前伪造追踪结果。

### 20.5 PromptTemplate 与执行规则

WP-05 定义项目资料收集、通用方法执行、UX、UI 生成、数据库、API 和独立评审七类中文 PromptTemplate。每个模板都有独立的版本化变量和机器产物 schema：UI 必须产出页面/组件、Token、状态矩阵、响应式/A11y、资产和截图证据；数据库必须产出 ERD、字段字典、约束、查询索引和迁移回滚；API 必须产出 endpoint/event、OpenAPI、错误、权限、幂等兼容和契约测试。八字段会话回复由 ResponseTemplate 负责，不再冒充 Prompt 的专业输出契约。

PromptTemplate 只组织方法输入、动作和专业产物，不授予文件、网络、Git、PR 或生产权限；具体 ToolPolicy 由 WP-06 负责。任何方法遇到关键输入缺失、事实冲突、无 owner 缺口、验证失败、Review 退回或人工 Gate 时，停在当前步骤并返回可恢复状态。

## 21. WP-06 工具策略、会话回复与人机交接

### 21.1 工具分类与默认拒绝

工具注册表包含 13 类：文件读取、文件写入、命令与进程、浏览器、网络、图像、文档与表格、外部连接器、独立子代理、本地 Git、远端 Git/PR、构建发布部署、生产操作。工具是否安装、当前是否可调用、AI 是否知道调用方法，都不等于已获授权。

`TOOL-PERMISSION-EVALUATOR-001` 固定按以下顺序求值：工具类别已知、可信 RouteDecision、可信 RoleAssignmentEvaluation、ActionSpec 引用该 ToolPolicy、可信 ScopeEvaluation 与路径规范化、可信 Artifact Gate、可信 OperationRequest、需要时的可信人类授权和可信消费回执、证据与补偿已准备。可信事实只能由 `TRUSTED-RUNTIME-FACT-LOADER-001` 从追加 ledger 或 hash 绑定快照加载；工具请求只提交事实 ID，不能提交 `route_and_action_current=true` 等布尔值自证权限。

Route、角色、scope、Artifact、操作请求、授权和消费记录都必须校验自身 canonical SHA-256，并绑定同一 ActionSpec、actor、subject/hash、目标和求值时间。仓库路径必须是相对路径，规范化后仍位于 ScopeEvaluation 的允许前缀；`..` 逃逸、损坏 hash、缺 owner 或缺可信记录一律拒绝。任一步失败立即返回具名原因码；模型推荐的工具只能是候选，不能覆盖规则决定。

单条事实的自哈希只证明该对象内部一致，不能证明它来自已登记来源。来源登记由 `settings` 装配的只读快照端口从追加 ledger 头或冻结快照加载；动作求值函数只接收事实 ID 和来源登记 ID，不接收可由调用方构造的登记对象。求值器加载登记后，再验证 `LoaderAttestation`、逐事实唯一 `FactSourceBinding`、独立来源记录 hash 和当前事实 hash；来源记录 hash 必须由来源记录封套计算且不能等于事实自哈希。登记不存在、ID 不匹配、同一事实零条或多条绑定、来源记录未纳入快照时全部拒绝。普通权限和 29 个高风险 ActionSpec 都执行同一规则。

### 21.2 四个 ToolPolicy

| ToolPolicy | 用途 | 关键允许条件 | 典型拒绝 |
|---|---|---|---|
| 最小必要读取 | 文件、命令、浏览器、网络、文档、连接器和只读子代理 | 目标属于 ActionSpec 读集，来源有效，敏感信息已脱敏 | 默认读归档、原始秘密、模型扩大读集、只读名义下委派写入 |
| 受控 Artifact 写入 | 候选文件、生成资产、命令写入、浏览器/连接器变更和有写集的子代理 | 输出契约、路径 resolver、精确写集、前像/追加规则和当前 Gate 同时通过 | 讨论直接写 `docs/`、未登记路径、无发布门改正式文档、隐式 commit |
| 输出验证与回读 | 测试、构建检查、hash 回读、浏览器验收、外部状态回读 | 当前输出 hash 与验证目标一致，命令和期望退出码已声明，验证无未声明副作用 | 只凭文件存在宣称完成、无新鲜退出码宣称测试通过、隐藏截断输出、作者自审冒充独立评审 |
| 高风险逐项人工授权 | 本地 commit、分支、Push、PR、Merge、发布、部署、数据和生产操作 | 固定 human 授权逐值匹配 ActionSpec、action/tool/operation kind、参数 hash、目标、scope、subject/hash、assignment、有效期和 ActionRun；单次消费回执先于副作用 | AI 生成授权、跨工具/动作复用、空 scope、缺参数、缺消费回执、未确认即开 PR、未知副作用盲重试 |

四个策略都产生追加式 `ToolEvent`，记录 ActionRun、策略、工具类别、操作、目标、参数 hash、权限决定、开始/结束时间、结果码、输出引用/hash、副作用、脱敏和补偿引用。原始 secret 不得进入 ToolEvent；缺输出、截断输出或不确定副作用不能写成成功。

### 21.3 PR、提交和生产动作

`local_commit`、`create_branch`、`push`、`create_pull_request`、`merge`、签名、版本写入、部署、回滚、数据变更和生产操作均是独立高风险 ActionSpec。每个 ActionSpec 固定唯一 ToolKind、OperationKind 和参数 schema。创建 PR 每一次都必须由人类明确授权，并绑定 ActionSpec、OperationRequest、ActionRun、远端 Git ToolKind、`create_pull_request` OperationKind、repository、head/base branch、draft、commit、参数 hash 和 subject hash；空 scope、跨生产工具复用或缺任一字段均拒绝。

授权在副作用前以稳定键 append/fsync/readback，形成绑定当前 ActionRun 的 `AuthorizationConsumptionReceipt`；只有 append 已提交、fsync 成功、readback 精确匹配、消费次数为 1 且副作用尚未开始时才允许执行。重复策略只允许 `single_use`。目标、scope、subject、assignment、工具、操作、参数或动作种类不一致时拒绝；授权过期时重新请求人类决定；执行结果不确定时先回读远端或生产状态，禁止盲重试。

### 21.4 会话中间更新

项目化会话在任务开始、Workflow/工作包切换、文件编辑前、关键命令前后、子代理派发或返回、自动整改轮次变化、阻断或范围变化时必须给用户短更新。持续执行期间最长静默时间为 30 秒；更新至少说明当前目的、正在做什么、观察到的进度和下一动作。

中间更新不是最终回复，不能宣称任务完成，也不能只把结果写入文件后让会话无回执。子代理或自动 loop 返回后，主 AI 必须把评审结论、当前状态和下一步带回当前会话。

### 21.5 七类中文最终回复

所有项目化会话最终回复固定按八个字段组织：本轮目的、已经完成、产物与路径、验证结果、当前状态、用户需要做什么、明确未做、下一步。字段不得省略；确实没有内容时必须写“无（原因）”。机器 ID、WP/CP 编号和状态码首次出现时必须同时给出中文名称或用途，禁止只返回一串编号和链接。

`RESPONSE-CONTENT-EVALUATOR-001` 还必须绑定当前 subject/hash、真实状态、已登记 Artifact refs、验证 evidence refs 和正式发布状态。`artifacts=有`、`verification=已通过`、无证据的 `done`，以及“候选已获人工批准并正式生效”等同义假报均拒绝；验证必须给出命令/证据引用和退出码/结果，未运行时必须写原因。

“引用格式像路径”不等于引用已登记。回复求值器按 `reference_registry_id` 从 `settings` 只读快照端口加载 `ReferenceRegistry`，调用方不能直接传入登记对象；上下文 ID 必须与加载结果完全一致。每个 Artifact/Verification 记录必须恰有一条独立来源绑定，来源记录 hash 不能等于记录自哈希。Verification 还必须保存 `expected_exit_code` 并执行结果矩阵：退出码 0 才能是 `passed`；非零且期望为 0 才能是 `failed`；非零退出码与已登记预期值相同才能是 `expected_red`。ID、subject/hash、来源绑定、命令、退出码、结果或 evidence 任一不一致均拒绝。

| 模板 | 使用场景 | 附加内容 |
|---|---|---|
| 直接咨询与解释 | 无项目副作用的回答 | 答案、依据/假设、无项目写入、可选后续 |
| 缺少输入 | 关键输入缺失或无效 | 已知事实、每批最多三个问题、阻断原因、恢复节点 |
| 阶段或动作完成 | 节点、工作包或任务完成并在本轮停止 | 中文工作流名称、完成范围、新鲜验证、继续或停止位置 |
| 独立评审交接 | 等待评审或评审退回 | 对象/目的、修订/hash、Reviewer 和只读范围、发现与待处理项 |
| 人工确认 | 人工决定或显式授权 Gate | 待确认对象/hash、允许决定、影响/风险、未决定前禁止动作 |
| 阻断/失败/取消 | 权限、事实、验证、范围、未知副作用或取消 | 第一失败条件、已尝试动作、副作用/未写入、恢复条件 |
| 高风险动作结果 | 高风险动作已执行、被拒绝或状态不确定 | 授权绑定、真实工具结果、目标回读、副作用、补偿/回滚 |

`RESPONSE-TEMPLATE-SELECTOR-001` 按高风险结果、人工确认、评审、缺输入、阻断、直接回答、普通完成的优先级唯一选模板；零匹配进入阻断模板，模型不能自行改选。Session 的 `stopped/waiting_user/waiting_review/blocked/failed/cancelled` 和 Workflow 的人工确认、缺输入、评审、退回、暂停、阻断、失败状态均有确定模板。

### 21.6 继续、停止与 HandoffPackage

当前 Action 已提交、下一动作已在既有授权内、没有人工/评审 Gate、没有关键输入缺失、事实或范围冲突、验证失败或不确定副作用时，AI 应在同一会话继续，不能仅因“刚创建计划”“刚创建任务卡”“完成一个内部工作包”或“一个工具调用返回”随意停下。

缺输入、独立评审 Gate、人工决定 Gate、显式高风险授权 Gate、范围变化、事实冲突、权限拒绝、验证失败、不确定副作用、loop 上限或用户暂停/取消时必须停止。停止前生成 `HandoffPackage`：绑定项目、WorkItem、TaskCard、WorkflowRun、当前 Workflow/Node、封闭 Session/Workflow 状态、八项回复内容、待决 Gate、第一失败条件、subject/hash、`reference_registry_id` 和恢复点。Artifact/verification 必须通过该 ID 从只读快照端口加载并解析为当前 subject/hash 的登记记录，调用方传入的登记对象无效；`current_status` 必须等于 Workflow 状态，`subject_sha256` 和创建时间必须合法，最后以 canonical payload 计算 `handoff_sha256`。Memory 只保存该包的精简投影和引用，不复制正式文档正文或秘密；直接咨询且 `project_effect=none` 时只在会话返回，不写项目状态。

### 21.7 WP-06 适用性与下一步

WP-06 的图形 UI 适用性为 `N/A`，因为交付的是会话文字和结构化交接契约。替代验收是中文字段顺序、模板确定性选择、全部停止状态覆盖、工具权限真实求值以及未授权文件写入、网络、子代理、Git、PR、部署和生产动作负例。

CP-03 R004 已把来源登记移出动作求值输入，并要求唯一来源绑定和独立来源记录 hash；同一 Reviewer Russell 对 CP-03 R004 给出 `approved / 100`，对 CP-02 R008 当前候选影响给出 `approved`。用户已确认关闭 CP-03 并进入 WP-08；该确认仍不授权正式落档、提交、PR、Merge 或部署。

## 22. WP-07 交付拓扑、纵向切片与 BusinessField 追踪

### 22.1 树负责归属，边负责矩阵关系

目录和导航必须是一棵树，否则人和 AI 都难以确定唯一 owner；软件关系本身是矩阵，不能靠复制目录表达。`TOPOLOGY-DELIVERABLE-001` 因此同时定义：

1. 每个 DeliverableNode 只有一个 `canonical_parent_node_id`，用于导航、owner、路径和版本归属。
2. 产品表面消费服务、服务实现领域、模块实现领域、模块参与切片等多对多关系使用类型化 DependencyEdge，不复制节点或文档。
3. Project → Product Surface → Service → Domain → Module → Vertical Slice → Task 是端到端业务路径的类型链，不强制把同一服务复制到每个前端目录下。

Project 可直接拥有产品表面、服务、领域、纵向切片和横向基线；产品表面拥有前端模块，服务拥有后端模块，领域可拥有纯领域模块，纵向切片拥有 TaskCard。所有跨树关系通过 `consumes/realizes/implements/contributes_to/decomposes_to/depends_on/shares_baseline/publishes_contract/owns_data/verifies` 等边表达。

DeliverableNode 只保存所有节点共有字段，不能代替类型详情。`typed_detail_binding_contract` 要求每个 ProductSurface、Service、Module、VerticalSlice、Task 和 HorizontalBaseline 节点恰好解析到一个同 ID、同类型的 detail 记录；反向也要求每个 detail 恰好对应一个现存节点。缺 detail 只允许一个绑定该 node ID、含原因、影响、替代方案、owner 和 ReviewerDecision 的结构化 N/A。每个 `na_id` 必须唯一，每条 N/A 必须被恰好一个适用节点消费，且该节点不能同时存在 detail；整体省略、重复、孤立、ID/类型错配、未被节点消费或与 detail 并存都拒绝。

### 22.2 领域和模块不是固定上下级

Domain 是业务语义、术语、不变量和所有权边界，不等于代码目录、微服务或前端工程。Module 是某个产品表面、服务或领域中的实现单元，必须引用一个主领域，可通过受控引用关联次领域。

- 后端模块说明所属服务、主领域、职责、不变量、应用用例、接口 owner、依赖、数据所有权、错误和测试边界。
- 前端模块说明所属产品表面、主领域、业务能力、页面/路由、组件边界、状态来源、API 契约、共享策略和测试边界。
- 共享模块使用结构化创建契约，必须已有至少两个登记消费者、稳定契约引用、owner assignment 和版本策略引用；“以后可能复用”不足以创建共享层。
- 跨模块调用必须使用受控接口；共享数据库列或隐式全局状态不能充当接口。

因此后端和前端都分模块，但分法不同：后端围绕领域、用例、服务和适配器；前端先按产品表面，再按业务能力/领域组织页面、状态和组件。

### 22.3 产品表面和服务分别登记

Web、移动 App、小程序、每个管理后台和 CLI 都是独立 ProductSurface；多个管理后台必须使用不同稳定 ID、受众、权限、页面能力、构建和验收。后端服务、API 服务、网关、worker、定时任务和集成适配器都是独立 Service，分别登记职责、领域、模块、数据 owner、接口、依赖、部署、监控、恢复和发布状态。五类产品表面、六类服务和第二个管理后台都必须有可执行登记正例；未知 subtype 必须拒绝。

每个产品表面和服务可以独立设计、计划、实现、测试和发布，同时通过 BusinessField、API、权限、设计系统和纵向切片保持共同需求一致。最终交付报告必须按这些节点分别列完成、未完成、验证、版本和发布状态。

### 22.4 任务以纵向业务切片为主

VerticalSlice 从用户或业务结果开始，贯通 Requirement、UX、UI、ProductSurface、API、Application、Domain、Database、Permission、Test 和 Release。先创建可独立验收的切片，再在同一 TaskCard 的 ActionSpec 中安排数据库、接口、前端、多端、测试、文档和发布动作。

禁止先建立“全部数据库任务”“全部 API 任务”“全部 UI 任务”三棵互不验收的树。读文件、运行命令、写测试和记录 evidence 是 Action，不单独创建 TaskCard。P0/P1 切片的适用层必须完整；N/A 需保存层、原因、替代验证、Reviewer 决定和当前 subject hash。

任务目录按 `WorkItem → VerticalSlice/TaskCard → drafts/evidence/reviews/reports` 归属，不按数据库/API/UI 建业务任务目录。产品源码仍可按真实前端表面和后端服务建立模块目录，但每个模块必须反向引用 `module_id/domain_id/slice_id`。

### 22.5 横向基线与全局文档关系

横向基线包含项目、领域、架构、数据、API、UI 设计系统、质量、安全隐私和发布运维。它们服务多个纵向切片，不被复制进每个模块目录。基线变更可以有独立 TaskCard，但必须生成 BaselineImpact，列出受影响产品表面、服务、领域、模块、切片、BusinessField、失效 Artifact 和必需任务。

正式 `docs/` 只保留登记 owner 的最小文档；全局文档通过 Catalog ID、Requirement ID、Domain/Module ID、Slice ID 和 BusinessField ID 与具体模块设计关联。讨论不能为了表达一个矩阵关系就新增 Markdown；完整拓扑和关系矩阵以机器 Catalog 为唯一事实源，Markdown 只解释阅读方式和关键取舍。

### 22.6 BusinessField 唯一规范定义

`FIELD-TRACE-BUSINESS-001` 要求每个 BusinessField 保存稳定 ID、业务名称和含义、owner、需求、规范类型、格式/单位/精度、枚举、可空、默认、来源、敏感级别、生命周期、校验、权限、各层映射、变更历史和证据。技术名称可以不同，但必须引用同一 BusinessField ID。

必需追踪层为：Requirement、Domain、Database、API/Event、UI、Validation、Permission、Log/Audit、Test。兼容校验必须从每层真实 `technical_type`、必填/可空值、owner Artifact、默认、约束、权限和 validation refs 推导规范值，再和 BusinessField 比较；`normalized_contract` 只是非权威派生摘要，不能掩盖实际字段漂移。数据库结构不能反向定义公共 API 语义，UI 标签也不能代替业务含义。

### 22.7 字段变更和 TraceBreak

字段新增、删除、改名、改类型、改枚举、改权限或改敏感级别时生成 BusinessFieldImpact。七类 change kind 分别使用封闭影响集合，ImpactList 强制绑定旧/新 contract hash、受影响映射和 Artifact、失效批准、任务、迁移/兼容、Review 和验证；删除任一必填字段都必须失败。稳定 BusinessField ID 在技术改名时不变。

缺映射、含义漂移、类型/可空/默认/枚举不一致、校验变弱、权限扩大、敏感级别丢失、日志脱敏缺失、测试缺失或未经评审的 N/A 都形成 TraceBreak。P0/P1 进入实现前，未解释或无 owner TraceBreak 必须为 0。

### 22.8 完整字段链参考

CP-03 使用 `BF-HIGH-RISK-AUTH-VALID-UNTIL-001` 作为完整参考链：

| 层 | 映射 | 必须保持的语义 |
|---|---|---|
| Requirement | 高风险/PR 授权有效期 | 每次人类明确授权，严格晚于求值时刻 |
| Domain | `HumanAuthorization.validUntil` / `OffsetDateTime` | 必填、明确时区、不能由 AI 生成 |
| Database | `human_authorization.valid_until` / 带时区时间戳 | NOT NULL，晚于授权时间，支持活动未消费授权查询 |
| API | `valid_until` / `string date-time` | 必填，拒绝无时区和可解析但非 ISO 值 |
| UI | “授权有效期”时区感知输入/只读显示 | 人类批准前可编辑，授权后只读，显示时区和过期状态 |
| Validation | `parseStrictTimezoneIso8601` | 合法日历、偏移不超过 14:00、精确解析、未来比较 |
| Permission | `HUMAN_APPROVER.write_valid_until` | 只有有效人类批准人可写，AI 只能读取候选决定 |
| Log/Audit | 授权过期求值事件 | 追加授权 ID、求值时刻、结果和 hash，不记录 secret |
| Test | high-risk authorization 边界矩阵 | 未来 ISO 允许；过期等待；非 ISO、无时区、非法日期/偏移拒绝 |

该参考链是运行时实现的设计契约，不冒充当前已经存在数据库或 UI；它证明同一字段如何在未来实现中保持一致，并直接复用 CP-02 R005 的严格时间对抗测试。

### 22.9 覆盖闭合与 CP-03

WP-07 同步核对前序覆盖，发现 WP-04 至 WP-06 的需求覆盖仍保留占位或 deferred 状态。43 条 WP-04 至 WP-07 覆盖现已逐项指向真实 metadata、Method、ToolPolicy、ResponseTemplate、Topology 或 FieldTrace 对象；能力缺口保留“已登记人工 owner”语义，不伪称专业 Skill 已实现。

CP-03 R001 独立评审发现 3 Critical、6 Important、1 Minor，结论为 `changes_requested / 30`。第 1 轮整改要求：裸布尔权限自证、跨工具 PR 授权、伪造 normalized 字段、通用 Skill/Prompt、回复假报、拓扑/影响 schema 清空和 stdout 截断都必须有真实负例。完整 `cp03@0.3.0`、受影响 `cp02`、WP-05/WP-06 阶段和输出管道验证全部通过后，才能冻结 R002 并由同一 Reviewer Russell 只读复审。作者 Green 不等于 CP-03 或 CP-02 恢复通过，当前也没有人工设计批准或正式发布资格。

R002 复审关闭了 6 项，仍以 `changes_requested / 58` 保留 `CP03-C-001`、`CP03-I-003`、`CP03-I-004`、`CP03-M-001`，CP-02 R006 当前候选影响也因同一来源根问题退回。第 2 轮整改增加外部 TrustAnchorRegistry 和来源根 attestation、真实 Artifact/Verification ReferenceRegistry、拓扑节点与 typed-detail 双向一一绑定，并把状态证据更新到当前轮次。R003 是本检查点最后一个自动复审候选；若同一 Reviewer 再次退回，必须停止交人工决定。作者 Green、R003 冻结或 CP-02 R007 影响快照都不等于 Reviewer approved、人工设计批准或正式发布。

R003 最终自动复审为 `changes_requested / 64`，关闭 `CP03-M-001`，仍开放来源登记同调用边界、引用登记/退出码结果不一致和孤立 Reviewer N/A 三项。R004 定向整改把三项全部关闭，同一 Reviewer Russell 给出 `approved / 100`，CP-02 R008 当前候选影响也通过；用户随后确认关闭 CP-03 并授权执行 WP-08 到下一人工确认门。

## 23. WP-08 验证器和黑盒测试设计

### 23.1 五个验证接口

WP-08 在 Catalog 的 `wp08_scope.interface_contracts` 中定义五个结构化接口，Markdown 不复制第二套字段定义：

| 接口 | 用途 | 核心字段 |
|---|---|---|
| `ValidationResult` | 一次 profile 求值的完整结果 | profile、阶段、状态、是否有效、检查点资格、Finding、覆盖、兼容结果和输入/验证器 hash |
| `Finding` | 可定位的验证问题 | 稳定 ID、严重度、原因码、消息、对象引用和证据引用 |
| `CoverageMetric` | 分子/分母可重算的覆盖结果 | 指标 ID、分子、分母、状态和来源 |
| `NegativeCase` | 真实内存变异负例 | 负例 ID、变异类型、目标指针、期望决定、原因模式和 runner |
| `CompatibilityResult` | 正式输入只读兼容检查 | 来源路径、预期/实际 hash、兼容决定和变化类别 |

`cp04` 和 `final` 的命令输出保留原有 `errors/metrics`，同时输出符合 `ValidationResult` 的结构化 envelope。Finding 由实际错误确定性生成，不能预填“通过”；CoverageMetric 和 CompatibilityResult 来自本次真实运行。

### 23.2 369 个流程级可执行夹具

123 个 Workflow 各有三个固定场景，共 369 个：

1. `happy_path`：唯一 RouteRule 命中，权威输入、角色绑定、事实和权限有效；实际求值必须完成声明动作引用并进入 `closed`。
2. `missing_input`：删除必需权威输入；必须在入口节点进入 `needs_user_input`，项目写入为 0，并保留恢复节点。
3. `unauthorized_or_conflict`：高风险流程删除人工授权时进入 `pending_human_confirmation`；普通流程注入事实冲突时进入 `blocked`；项目写入均为 0。

实际结果分布必须固定为：123 个 `complete`、123 个 `needs_user_input`、15 个高风险 `needs_human_decision` 和 108 个普通冲突 `blocked`。只核对场景总数而不核对分支结果，不能通过 CP-04。

每个 test_case 保存输入夹具、独立 oracle、oracle hash、证据字段、正式输入兼容引用和负例引用。test_case、fixture 和 oracle 必须逐行绑定同一组 `test_case_id / workflow_id / scenario_kind / source_binding_sha256`；fixture 的路由信号、生命周期阶段、角色分配、权威输入、缺失键、冲突标志、事实状态和权限状态必须与该 Workflow 和场景类型完全一致。求值器只接收 fixture，不接收 test_case 或 oracle；它先从 Catalog 的 RouteRule、Workflow、ActionSpec、Method、ToolPolicy 和 ResponseTemplate 推导实际结果，再读取 oracle 比较。全部运行在内存副本中，产品和项目事实写入为 0。

### 23.3 Catalog 完整性与真实负例

`TEST-CATALOG-INTEGRITY-001` 负责 Catalog 级完整性。它登记并实际运行 16 类变异：

- 删除 test_case、恢复延期状态、复制 fixture ID。
- 删除路由信号、把缺输入伪写成功、让未授权场景产生项目写入。
- 指向未知 Workflow、删除证据字段、使用非法初始状态。
- 破坏源场景指针、删除负例登记、把已完成 WP-08 coverage 恢复为延期。
- 在同一 Workflow 内交换正常场景与缺输入场景的 fixture/oracle。
- 跨 Workflow 交换高风险缺授权场景与普通事实冲突场景的 fixture/oracle。
- 伪造正式输入兼容路径、篡改负例的变异类型/目标指针/预期原因。

验证器内只有一份封闭的负例注册表。Catalog 登记必须逐字段与它一致；执行器按同一登记的 `mutation_kind` 选择处理器，并按同一登记的 `expected_reason_pattern` 判断结果。每个变异都在内存副本上重新调用同一 `validateWp08`，只有命中预期错误模式才算负例通过。删除数据、篡改登记或直接写一个 `rejected=true` 布尔值都不能满足验收。

### 23.4 覆盖与兼容边界

- 77 条需求覆盖和 2448 条源指针迁移合计 2525 条；原覆盖与新增 `REQ-CHANGE-WF-CTL-010-001` 均绑定可执行测试。
- WP-08 完成后只允许 WP-09 的 3 条发布事务覆盖保持延期；WP-01 至 WP-08 的延期数必须为 0。
- PRD、需求矩阵、文档索引和 R006 Workflow 映射按四个冻结 SHA-256 做只读兼容检查。`source_key / source_path / expected_sha256` 必须同时与验证器内可信来源和 Catalog metadata 绑定完全一致；CompatibilityResult 只输出可信路径，不回显未经核对的路径。实际 hash 或来源绑定任一漂移都使 `cp04` 失败。
- WP-08 只新增此前明确归属 WP-08 的 test_case、`cp04` 和 `final` 路径，不改变 CP-01 至 CP-03 共享规则；仍必须重跑三个 profile，并由 CP-04 Reviewer 核对影响集合为空。

### 23.5 R017 对旧 final/WP-09 合同的继承资格

R006 至 R016 中关于 68→43、107/158 个发布目标、仓外对象存储、逐文件归档 payload 和四层存储的 final/WP-09 合同均已被正式 PRD v3.3.0 取代，执行资格为 false。可继承内容只限于 123 条 Workflow、方法、角色、字段追踪、会话回复和验证思想；任何机器消费者不得从历史计数恢复发布动作。

### 23.6 当前 final 验证边界

R019 的 68/17 前像、37/7 后像和 38 个发布目标作为历史发布合同保留在 Git 与 evidence；T06 当前基线把 docs 收敛为 34 份人类 Markdown，Catalog 源迁至 `.factory/catalog/ai-sdlc-catalog.source.json`，稳定 Builder 继续保留。

## 34. R019：项目执行位置与停止可见性统一设计

### 34.1 单一快照事实链（REQ-VIS-002、REQ-VIS-004、NFR-VIS-002）

R019 新增且只允许一条位置事实链：

```text
EventLog(H) -> ProjectProgressReducer/v2 -> validated/authorized ProjectProgressSnapshot/v2
            -> PositionViewPort -> PositionViewAdapter/v1 -> ProjectExecutionPosition/v1
            -> ResponseAssemblyPort -> REQ-ASYNC-016 v4.0.0 renderer
```

`application` 是端口调用方和合同 owner；`runtime` 只提供纯 reducer、canonical hash 和资格求值；`settings` 实现读取/渲染适配器并只在 `src/settings/composition/` 装配。依赖方向仍是 `access -> application -> domain -> runtime -> settings`。`access` 不得越过 application 读取 projection store，`settings` 不得重新定义上层 port，仓内不得重建 DI resolver、loader、registry、factory 或 manifest 内核。

三个入口——会话首轮恢复、用户主动查询项目状态、任务节点完成后的主动回复——都必须先捕获同一固定高水位 `H`。本轮计算期间出现的 H+1 只进入下一快照，不能改变本轮 N/M、当前节点、Gate 或回复。若某字段来自 P<H、P>H 或未授权 projection，整个位置绑定失败关闭。

`ProjectExecutionPosition/v1` 必须逐字节绑定 validated/authorized `ProjectProgressSnapshot/v2` 的九个字段：`project_id`、`snapshot_id`、`snapshot_sha256`、`as_of_H`、`registry_sha256`、`event_schema_sha256`、`reducer_sha256`、`snapshot_schema_sha256`、`authorization_digest`。任一字段 missing 或 drift 均返回专用失败码 `project_progress_binding_conflict`，不能折叠为 lifecycle 失败。失败路径上 `PositionViewAdapter/v1` 的 event-log read / event reduce / Gate advance 调用计数必须严格为 `0/0/0`。因此 adapter 只能投影已验证快照，不能偷偷成为第二 reducer，也没有推进 Gate 的能力。

快照通过 `SnapshotQualification/v2` 校验 schema/hash、registry generation、reducer generation、授权摘要和 fixed H。校验顺序为 schema → 九字段完整性 → hash → authorization → H → adapter；任何一步失败都不继续。`NFR-VIS-002` 的一致性因此由同一快照和禁止第二 reducer 的能力边界保证，而不是靠文字约定。

### 34.2 生命周期 N/M 绑定（REQ-VIS-001）

整体路线来自恰好一个 active `LifecyclePlanBinding/v1`，AI 不能从当前目录或局部任务计划自行挑选分母。绑定必填十字段为：`artifact_id`、`artifact_version`、`artifact_sha256`、`binding_status`、`effective_scope`、`authorization_digest`、`stage_map_id`、`stage_map_version`、`stage_map_sha256`、`as_of_H`。

`LifecycleBindingPort` 在 H 上读取只读注册表；`domain` 的 binding evaluator 要求 active cardinality 恰好为 1。零个、多个、inactive、hash drift、stage map 冲突和权限拒绝分别返回：`lifecycle_binding_missing`、`multiple_active_lifecycle_bindings`、`lifecycle_binding_inactive`、`lifecycle_hash_mismatch`、`stage_map_conflict`、`lifecycle_permission_denied`。失败时整体 N/M 不得从当前 WorkItem 或最后一次回复猜测，而是进入 `blocked/fact_conflict`。

N/M 的分母是 active binding 的全局 stage map；支线、回退、review loop 和局部 WorkItem plan 只显示为当前 stage 内的节点或分支，不能增减 M。阶段完成仅由 stage completion policy 与正式事件决定；“文件已写”“作者自报完成”或“子任务已返回”都不能直接推进 N。这样当前的整体坐标始终类似“3/8 设计重基线”，不会被“T02 2/6”替代。

### 34.3 四维状态与七种互斥处置（REQ-VIS-003）

系统分开保存 `workflow_run_state`、`completion_state`、`reply_state` 和派生 `execution_disposition`。前面三维是输入事实，`execution_disposition` 是纯函数结果，不能反向覆盖输入。处置规则使用七个 mutually-exclusive selector；每个 selector 对其他 selector 都有 forbids：

| disposition | required selector | 必须禁止的其他 selector | 责任含义 |
|---|---|---|---|
| `running` | `run_active=true` | 其余六个为 false | 当前执行器正在运行 |
| `auto_continuing` | `auto_authorized=true` | 其余六个为 false | 当前节点完成后授权范围内自动进入下一节点 |
| `waiting_ai_execution` | `ai_ready=true` | 其余六个为 false | AI 已具备执行条件但尚未取得运行槽 |
| `waiting_independent_review` | `review_dispatched=true` | 其余六个为 false | 已有真实 dispatch/submission/task ID，责任人为独立 Reviewer |
| `waiting_human` | `human_gate_pending=true` | 其余六个为 false | 恰好一个人工计划 Gate 真正需要用户动作 |
| `blocked` | `terminal_or_fact_conflict=true` | 其余六个为 false | 缺工具、事实冲突或不可自动恢复失败 |
| `completed` | `task_complete=true` | 其余六个为 false | 当前任务或当前 stage 已满足其完成定义 |

零条或多条命中都返回 `blocked/fact_conflict`，不能用优先级掩盖事实冲突。`waiting_independent_review` 只有在 dispatch/outbox 持久化并回读成功后成立；“准备派发”仍是 `auto_continuing` 或 `waiting_ai_execution`。`waiting_human` 也只能来自未满足的人工 Gate，不得用它表达 AI 正在做事、等待测试或一般不确定性。

### 34.4 固定 H、会话恢复和节点绑定（REQ-VIS-004）

每次 projection request 生成 `ProjectionReadContext/v1`，冻结 `project_id + as_of_H + authorization_digest + request_id`。会话恢复、状态查询和节点完成回复把该 context 传给 snapshot、lifecycle、task、review 和 authorization readers；reader 不能自行刷新 H。若任一依赖只能提供 H+1，当前请求返回一致性阻断并建议下一轮重试，不把两代事实拼在同一回复里。

节点绑定包含全局 stage、当前 WorkItem、TaskCard、task node、gate generation 和 responsible actor。局部任务状态只能补充“当前任务/当前节点”，不能覆盖“项目总路线/当前坐标”。恢复时 Memory 只提供定位线索，正式坐标必须由 event ledger 与 snapshot 重算；Memory 中的旧 N/M、旧 stop reason 或旧 next action 一律不具备事实资格。

### 34.5 Evidence observation、执行身份和正式 CAS（REQ-VIS-005）

`EvidenceObservationPort` 的顺序固定为 canonical payload → authorization/Gate/generation 校验 → append-only observation → fsync/readback → 五字段 CAS。未经登记的文件、旧 generation、错误 actor、错误 artifact root、错误 test plan 或晚到 attempt 只保留审计，不推进 Gate。

执行前 `EvidenceExecutionIdentity/v1` 只含 15 个可事先知道的字段，顺序固定为：`gate_id`、`artifact_or_candidate_root_sha256`、`impact_policy_version`、`test_selection_plan_sha256`、`required_test_set_sha256`、`test_source_sha256`、`fixture_sha256`、`config_sha256`、`runner_name`、`runner_version`、`runner_sha256`、`dependency_lock_sha256`、`normalized_command`、`environment_attestation_sha256`、`external_dependency_fingerprint`。按该顺序编码 compact canonical JSON，并以 domain separator `shanforge:EvidenceExecutionIdentity/v1\n` 计算 `evidence_execution_identity_sha256`。request 只冻结这 15 项及其 hash，禁止预测测试 outcome。

Worker 结束后才追加五个真实结果字段：`passed_count`、`failed_count`、`skipped_count`、`not_run_count`、`evidence_time`，形成 20 字段 `EvidenceReuseKey/v1`。只有 execution status 为 passed、全部 required tests 实际运行且 failed/skipped/not_run 都为 0，20 字段逐一可复算时才能复用。`artifact_or_candidate_root_sha256` 必须等于 `CandidateArtifactSetRoot/R019`；`test_selection_plan_sha256` 必须等于 request 的 `test_plan_hash`。

正式 Gate CAS 仍是 `parent_task_id + gate_id + artifact_hash + test_plan_hash + gate_generation` 五字段。`artifact_hash` 必须字节等于当前 candidate root。CAS 只从当前合法前态推进一次；wrong parent/gate/hash/plan/generation、retry superseded、迟到 result、未登记 observation 全部失败关闭。

### 34.6 权限视图与侧信道控制（REQ-VIS-006、NFR-VIS-003）

`AuthorizationViewPort` 不改变真实全局分母，但会把无权查看的节点内容替换为固定 label。默认拒绝字段为 `task_title`、`task_path`、`risk_text`、`approval_text`、`adjacent_stage_name`。受限用户只能看到固定长度类别、当前位置是否可执行及允许动作；不能从字符串长度、hash、子项计数、排序、错误差异或响应时延推断秘密文本。

权限过滤在 renderer 前完成，renderer 只消费 `AuthorizedPositionView/v1`。禁止先渲染秘密文本再遮罩，也禁止用无权字段参与摘要 hash、分母、branch count 或“是否影响下一项工作”的文案。权限不足返回稳定 `lifecycle_permission_denied` 或 position authorization failure，不能回显目标路径和隐藏 stage 名称。

### 34.7 唯一十五行响应合同（REQ-VIS-007、REQ-ASYNC-016、NFR-VIS-001）

`ResponseAssemblyPort` 的唯一 producer/owner 是 `REQ-ASYNC-016` v4.0.0。renderer 必须按下列精确顺序输出恰好十五个 label，每个 label 只出现一次：

1. `项目总路线`
2. `当前坐标`
3. `当前任务`
4. `当前节点`
5. `本轮做了什么`
6. `完成了什么`
7. `验证情况`
8. `没有运行什么`
9. `后台任务`
10. `当前状态`
11. `为什么停下`
12. `是否影响下一项工作`
13. `下一责任人`
14. `需要你做什么`
15. `下一步`

行值来自同一 H 的 position/lifecycle/task/review/authorization view。未停止时“为什么停下”必须明确为“未停止，授权范围内继续”；不需要用户动作时“需要你做什么”必须明确为“无需操作”。后台任务只有真实 durable task ID 才能写“已派发”。这样用户不必从零散的工具日志推断状态，也不会把每个 AI 内部步骤误认为人工确认门。

v3.x 九行 consumer 属于 MAJOR 迁移：当前会话 renderer、项目状态查询、Memory 恢复回复、Review/人工 Gate 确认包、测试夹具和文档 owner 都必须登记 parser 从 `v3.x-nine-line` 到 `v4.0.0-fifteen-line` 的迁移、负例、rollback condition 和 generation。任一 strict nine-line parser 仍在活动路径时阻断 release_ready；系统不提供双 renderer 或兼容别名。

### 34.8 人工 Gate 与旧资格拒绝（REQ-VIS-008）

人工 Gate 仅有六类：`business_decision`、`risk_acceptance`、`candidate_approval`、`formal_action_authorization`、`credential_or_permission_grant`、`irreversible_action_confirmation`。普通编制、作者验证、已授权范围内复审整改、只读检查和可逆本地步骤不是人工 Gate。每个 `waiting_human` 必须给出 gate type、精确对象/hash、未满足原因、责任人和批准后下一动作。

R019 generation 中以下十类资格固定为 false：`P017_plan_author_validation`、`P017_independent_review`、`P017_human_plan_approval`、`P017_execution_authorization`、`R017_design_author_validation`、`R017_independent_review`、`R017_human_candidate_approval`、`R017_formalization_eligibility`、`R017_release_eligibility`、`R017_commit_or_remote_authorization`。它们即使拥有完整旧 evidence 也不能迁移。资格求值器必须比较正式 requirements hash、P022 plan hash、candidate root 和 `TASK-DESIGN-001-R019-G001`；任一不等即拒绝。

当前授权允许 R019 候选编制、作者验证、独立只读复审及同范围必要整改循环；唯一人工停止点是 R019 精确 candidate root 批准。正式发布、Git index/commit 和远端操作仍无授权。

### 34.9 Candidate root、写集和控制平面证明（REQ-VIS-009）

`CandidateArtifactSetRoot/R019` 的成员和顺序固定为：design、catalog_source、information_architecture、builder、validator、verification_runner。每个成员编码为只含 `artifact_id`、`path`、`sha256`、`bytes` 的 JSON object，键顺序即此顺序；路径是仓根相对 POSIX，UTF-8、LF、无 BOM、无额外空白。六对象按上述顺序组成 compact JSON array。domain separator 精确为 `shanforge:CandidateArtifactSetRoot/R019:v1\n`；root 为 `SHA-256(separator bytes || canonical array bytes)`。

manifest 排除在六成员之外，避免自引用。任一 schema 如保留 `candidate_sha256`，它必须与 `candidate_set_root` 字节相等，否则返回 `candidate_identity_conflict`。单文件 hash、manifest hash 或旧五成员 root 都不得称为 candidate hash。

27 条 canonical registry 由 P022 scope anchor 冻结。`HygienePhaseManifest/v2` 只能由 registry、Owner/Gate 和 `async_branch` 派生有序且不相交的 present/absent partition：transfer pre-T06 24/3、final 27/0；no_transfer pre-T06 21/6、final 24/3。两数组并集必须严格等于 27 条。实际 R019 选择 no_transfer，因此 regression request/outbox/result 三路径在 final 仍必须 absent。

每个文件写完后，控制平面向 work ledger 追加 `ArtifactWriteAttestation/v1`。schema 精确包含 `schema_version`、`event_id`、`actor_id`、`actor_type`、`execution_or_review_task_id`、`dispatch_receipt_id`、`authorization_event_id`、`authorized_write_set_sha256`、`target_path`、`expected_owner`、`gate_id`、`gate_generation`、`artifact_sha256`、`artifact_bytes`、`written_at`、`tool_receipt_sha256`、`ledger_prefix_sha256`。候选文件内自报的 actor/reviewer 不具备证明力；validator 必须从 authorization event 与 review ledger 的真实 dispatch 回读 actor/task/dispatch/write-set/owner/Gate，按 attestation 所在字节位置重算 ledger prefix，核对 tool receipt 与当前 hash/bytes，并拒绝 wrong actor、wrong task、fake reviewer、缺失或过期 dispatch、伪 prefix、未 readback 和过期 attestation。

`FinalHygieneReceipt/v2` 位于 27 路径集合外，只能在 final hygiene 后向 work ledger 追加一次。它精确包含 `schema_version`、`receipt_id`、`async_branch`、`canonical_registry_sha256`、`phase_manifest_sha256`、`validator_sha256`、`normalized_command`、顶层 `execution_id`、`gate_generation`、`present_entries[{path,sha256,bytes,attestation_event_id}]`、`expected_present_set_root`、`absent_proofs[{path,checked_at,absence_code,validator_execution_id}]`、`expected_absent_proof_root`、计数、`failed=0` 和 `finished_at`。phase manifest、validator、command、execution、generation 必须与每个 present/absence proof 同一执行绑定；旧 proof、跨 branch/generation replay 或 receipt 后 expected-present 漂移/expected-absent 出现都会立即撤销 Gate 资格。

其中集合和计数字段名固定为 `present_entries`、`absent_proofs`、`present_count`、`absent_count`、`passed_count`、`failed`；每个 absence proof 的四个字段名固定为 `path`、`checked_at`、`absence_code`、`validator_execution_id`。不得用 `present_artifacts`、`command`、`observed_at` 或不带 execution binding 的 `{path,exists}` 兼容别名。

### 34.10 Session-level V4 验证与性能（REQ-ASYNC-015、NFR-VIS-004）

`QuickVerificationSession/v1` 使用 monotonic clock，单一 session deadline 为 60,000ms，dispatch reserve 为 5,000ms，inline cutoff 为 start+55,000ms，策略版本为 `R019-quick-session-v1`。每个 L1–L4 required test 启动前用 remaining budget 做 admission，不能按测试或 retry 重置。预计时间超过 remaining window 时直接 transfer；已运行 attempt 到 cutoff 必须取消并在 reserve 内原子提交 durable request/outbox/parent Gate 与 readback。

`no_transfer` 要求全部 required tests 在 cutoff 前真实完成，四计数中 failed/skipped/not_run 都为 0，Worker 完全不运行，三份 async 文件不存在。`transfer` 至少有一项因预计超预算或实际到 cutoff 转移，才允许 `RegressionTaskRequest/v3`、outbox、`RegressionTaskResult/v3` 存在；request 固定 `fork_context=false`，只绑定执行前 identity，不预测 outcome。

预算边界必须覆盖 54s/55s/56s、59s/60s/61s、59s+59s、30s+31s，以及取消、事务、readback、回复时间和 clock drift。54 秒可以在完全空白窗口内启动，55 秒及以上必须 transfer；组合测试始终按累计 remaining budget 判断。事务失败也必须在绝对 deadline 前回复 `blocked/durable_dispatch_not_committed`，不能延长时钟。

性能基线使用 10,000 tasks、100,000 events；投影读取 hard cap 为 1,000 rows、8MiB、3,000ms。测试需证明新增九字段 binding、lifecycle lookup、permission filtering 和十五行 renderer 没有额外全库扫描，且 adapter 禁止直接读 event log。

### 34.11 R019 接口与 owner 总表

| 合同 | 定义方 | 实现方 | 关键限制 |
|---|---|---|---|
| `ProjectProgressSnapshot/v2` / `ProjectProgressPort` | `application` | `settings` projection adapter | validated/authorized、固定 H、九字段完整 |
| `PositionViewPort` | `application` | `settings` 的 `PositionViewAdapter/v1` | 只能消费 snapshot；禁止 read/reduce/Gate advance |
| `LifecycleBindingPort` | `application` | `settings` readonly registry adapter | H 上恰好一个 active binding |
| `DispositionEvaluator` | `domain` | `runtime` pure evaluator | 七条互斥；零/多命中失败关闭 |
| `ResponseAssemblyPort` | `application` | `settings` renderer | `REQ-ASYNC-016` 唯一 owner，严格十五行 |
| `EvidenceObservationPort` | `application` | `settings` append-only store | 先验证后 observation，再正式五字段 CAS |
| `QualificationEvaluator` | `domain` | `runtime` pure evaluator | 比较 requirements/plan/root/generation，旧资格拒绝 |
| `AuthorizationViewPort` | `application` | `settings` authorization adapter | 保留真实分母、固定受限标签、禁止侧信道 |
| `CandidateArtifactSetRoot/R019` | `application` 调用侧 | `runtime` canonical hash | 六成员固定顺序；manifest 排除 |
| `EvidenceExecutionIdentity/v1` | `application` 调用侧 | `runtime` canonical hash | 15 个执行前字段，不含预测 outcome |
| `EvidenceReuseKey/v1` | `application` 调用侧 | `runtime` equality evaluator | 15+5 全字段相等且全测试真实通过 |
| `QuickVerificationSession/v1` | `application` 调用侧 | `runtime` budget evaluator | 单 session 60s、5s reserve、monotonic |
| `RegressionTaskRequest/v3` / `RegressionTaskResult/v3` | `application` 调用侧 | `settings` durable queue/worker | 仅 transfer；两维状态与正式 CAS |
| `ArtifactWriteAttestation/v1` | control plane | `settings` work ledger | 真实 writer receipt，artifact 自报无效 |
| `HygienePhaseManifest/v2` / `FinalHygieneReceipt/v2` | `application` 调用侧 | `runtime` + `settings` ledger | branch-aware，receipt 在 registry 外 |

### 34.12 需求追踪与攻击矩阵

| 需求 | 设计 owner | 必需攻击 |
|---|---|---|
| `REQ-VIS-001` | §34.2 lifecycle binding | 零/多个 active、inactive、hash/stage map/权限漂移、支线改变分母 |
| `REQ-VIS-002` | §34.1 snapshot/position | 九字段逐一 missing/drift、第二 reducer、adapter `0/0/0` |
| `REQ-VIS-003` | §34.3 disposition | selector 全组合、零命中、多命中、伪 waiting 状态 |
| `REQ-VIS-004` | §34.4 fixed H | H+1、P<H、P>H、三个入口不同 H |
| `REQ-VIS-005` | §34.5 evidence/CAS | 未登记 observation、旧 generation、actor/hash/plan/CAS/late attempt |
| `REQ-VIS-006` | §34.6 authorization | secret text、长度/hash/计数/排序/错误/时延侧信道 |
| `REQ-VIS-007` | §34.7 renderer | 行数、行序、重复 label、缺字段、strict nine-line parser |
| `REQ-VIS-008` | §34.8 qualification | 十类旧 evidence 逐项注入、旧 root/plan/generation |
| `REQ-VIS-009` | §34.9 write/provenance | 27 路径、owner、branch partition、假 writer、receipt 后漂移 |
| `NFR-VIS-001` | §34.7 | 十五行可理解性与无需用户动作明确性 |
| `NFR-VIS-002` | §34.1 | 快照一致性与禁止第二 reducer |
| `NFR-VIS-003` | §34.5–§34.9 | 权限、证据、资格、writer 和 Gate 安全负例 |
| `NFR-VIS-004` | §34.10 | 10k/100k、1000 rows/8MiB/3000ms、无全库扫描 |

受影响的既有治理需求 `REQ-AI-WORKFLOW-008`、`REQ-AI-WORKFLOW-042`、`REQ-AI-WORKFLOW-045`、`REQ-AI-WORKFLOW-046`、`REQ-AI-WORKFLOW-047`、`REQ-AI-WORKFLOW-054`、`REQ-ASYNC-015`、`REQ-ASYNC-016` 均由上述合同吸收，不新增同义 Workflow。原 123 Workflow 身份保持不变；主要 owner 仍是 `WF-CTL-001` 和 `WF-CTL-010`。

### 34.13 当前候选 Gate 与停止规则

R019 作者只能把 T01–T06 产物标记为 `ready_for_review`。完整 profile 要求 assertions 至少 120，required tests 的 failed/skipped/not_run 均为 0，no_transfer 分支的 async 三路径保持 absent，pre-T06 hygiene 为 21/6。独立 Reviewer 必须未参与编制，只写唯一 Decision；Critical/Important 都为 0 才能进入人工候选批准。

独立评审出现同范围 Finding 时，作者依据 Finding 整改、重新生成受影响 root/manifest/evidence、重新派发同一 Reviewer 复审，期间不停止向用户索要确认。只有复审通过、final hygiene 24/3、Decision provenance 和 final receipt 都有效后，状态才变为 `waiting_human/candidate_approval`，并向 uroborus 展示精确 `CandidateArtifactSetRoot/R019`、manifest hash、Decision hash、正式 requirements hash、P022 hash 与 generation。

该人工批准只授权进入后续正式需求设计发布事务的资格判断；本次执行不包含正式发布、Git index/commit、远端操作或部署。未得到新的明确授权前，上述动作的执行次数必须保持 0。

### 34.14 R018 正式发布预检三项 Critical 的 R019 闭包

`R018-RELEASE-C-001` 的 37 docs + Builder 写集是历史发布合同；T06 激活后当前 docs 只登记 34 份人类 Markdown，机器源登记为 `.factory/catalog/ai-sdlc-catalog.source.json`。

`R018-RELEASE-C-002` 的确定性验证保留；稳定 Builder 当前默认读取 `.factory/catalog/ai-sdlc-catalog.source.json`，隔离候选仍只接受登记 basename，非法输入继续失败关闭。

`R018-RELEASE-C-003` 由当前正式前像闭合：IA baseline、三项 disposition、55 项 `source_preimage_disposition_refs` 中对应的活动记录和 target source-preimage binding 必须分别绑定 PRD `v4.0.0 / 648db794…`、需求矩阵 `v4.0.0 / 375ed02f…`、文档索引 `v2.0.0 / 2bc0cb84…` 的真实 hash/bytes。55 项 disposition ref 必须通过 disposition ID、source path 与 source hash 一一绑定，不允许活动表保留另一组前像。三份 target 的 current/candidate version 保持相等且 `change_level=NONE`；任何旧 `v3.1.0/v1.1.0` 或旧 hash 进入任一 CAS / disposition ref 都必须阻断，并由 required seed 的旧 hash mutation 明确证明拒绝。

<!-- sf:section-id=PROJECT-KNOWLEDGE-CLI -->
## 项目知识 CLI 契约增补

公开命令面只有一套：`project index refresh|check|rebuild`、`project snapshot --html [--check|--rebuild] [--profile ...]`、`project find`、`project show`、`project trace`、`project context`、`project sync enqueue|head` 和 `project maintain --dry-run|--apply`。第一版只生成静态文件，不提供 `--open`、`--serve` 或常驻服务。每个命令返回稳定 JSON receipt 和简短人类摘要；查询默认只读，只有刷新、重建、维护和后台 worker 可写各自登记的派生路径。

退出码固定为：`0` 成功，`2` 参数/契约错误，`3` 未找到，`4` locator 歧义或失效，`5` freshness/完整性失败，`6` 权限拒绝，`7` 并发切换忙。`context` 只返回最多四个文件、总计 32 KiB 的读取计划，不直接扩散读取正文。

## 35. OpenAPI 机器合同与统一阅读

本文件继续负责解释接口为什么存在、消费者是谁、权限和兼容策略如何决定；当前
HTTP 请求响应的可执行机器合同统一保存在 `contracts/openapi/openapi.yaml`，不在
`docs/` 再维护第二份字段副本。两者通过文档 ID `DESIGN-API-001` 和每个 operation 的
稳定 `x-shanforge-id` 关联。

当前 OpenAPI 3.1 精确覆盖代码已经声明的四条 route：

| Operation ID | 方法与路径 | 中文用途 |
|---|---|---|
| `API-HTTP-RUN-APP` | `POST /apps/{app_id}/run` | 执行一个已注册 Agent App |
| `API-HTTP-RUN-MANIFEST` | `POST /manifests/run` | 校验并执行调用方提交的 Manifest |
| `API-HTTP-GET-SESSION` | `GET /sessions/{session_id}` | 查询当前调用方可见的会话摘要 |
| `API-HTTP-PROJECT-STATUS` | `GET /projects/{project_id}/status` | 只读查询同一快照下的项目状态 |

每个 operation 必须有中文摘要和详细说明、`operationId`、参数/请求/响应/字段说明、
成功与错误响应、示例、Owner、需求和测试追踪。Shanforge 不再提供仓内 API
validator；目标项目使用自身合同测试验证这些字段。

校验时方法和路径集合必须与目标项目真实 runtime routes 完全一致；多一条或少一条都失败。
OpenAPI 中的需求引用形成 `SATISFIES` 强关系；引用目标没有稳定实体时，SQLite 原子
发布失败，不能留下悬空链接。

只读站点最终只保留“项目文档”一个入口：进入本文件即可阅读正文和 OpenAPI 操作卡；
不会再提供内容重复的独立“设计”入口。OpenAPI 原文件仍保存在仓库，供生成客户端、
Mock、契约测试和第三方工具使用。

## 正式版本历史（仅已发布）

| 版本 | 日期 | 变更 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v3.0.0` | 2026-07-18 | 基于 `TASK-DESIGN-001-R019` 正式落档 | `uroborus` | `uroborus` | `uroborus` |
| `v3.1.0` | 2026-07-22 | 固化项目知识查询、快照、同步与维护命令及退出码 | `uroborus` | `uroborus` | `uroborus` |

候选修订：`v3.2.0` 增补 OpenAPI 3.1 机器合同、四条现有 route、稳定操作 ID、
需求/测试追踪和统一文档阅读规则，并将 Skill 清单改为文件系统动态发现；当前尚未进入正式版本历史，待独立评审和用户确认。
