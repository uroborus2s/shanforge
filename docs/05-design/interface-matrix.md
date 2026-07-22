# 接口与字段追踪矩阵

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `TRACE-API-001` |
| 正式版本 | `v3.1.0` |
| 来源候选 | `TASK-DESIGN-001-R019` |
| 发布事务 | `DESIGN-RELEASE-TX-R019-G001` |
| 负责人 | `HUMAN_API_INTEGRATION_LEAD` |
| 修改 / 审核 / 批准 | `uroborus` / `uroborus` / `uroborus` |
| 状态 | 已批准并生效 |
| 上游 | `module-domain-design`、`data-design`、`api-design`、`frontend-design`、`测试证据` |
| 下游 | `一致性 Gate`、`兼容分析`、`发布` |

## 文档职责

- 允许保存：业务字段到数据、接口、页面、组件、权限、校验和测试的关系。
- 禁止保存：接口完整 schema；设计正文；实现日志。
- 主要读者：架构、数据、API、前端、测试。

## 正式内容

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

**项目名称：** 山海工枢 / shanforge
**文档状态：** `v2` 接口基线
**负责人：** 仓库维护者
**主要读者：** 架构 | 平台开发 | 测试 | 适配器维护者
**上游输入：** 记忆运行时设计 | 记忆系统详细设计方案
**下游输出：** 代码实现 | 契约测试
**关联 ID：** `REQ-006`, `API-006`, `API-007`, `MOD-007`
**最后更新：** 2026-04-20

## 1. 目标

本文件只回答一个问题：在新分层口径下，`memory` 领域相关的稳定接口有哪些，以及接口 owner 在哪一层。

它不描述内部算法细节，只描述：

- 接口/网关层如何发起记忆查询
- 业务调度层如何调用记忆领域服务
- 业务模型层如何向下声明基础能力需求
- 基础能力层如何向下声明 provider 需求
- explainability、archive query 与 external provider 应如何收口

## 2. 接口/网关层接口

### `MemoryInspectionUseCase`

```text
recall(query) -> RecallBundle
preview_recall(session_id, limit=None) -> RecallPreview
```

语义：

- 支持独立调试、测试和网关查询
- `preview_recall` 当前通过独立治理接口暴露 session 对应的 recall query / plan / bundle 预览
- 不暴露领域内部编排步骤，也不把 `preview_recall` 混进 session archive inspection 门面

代码位置：

- `src/access/ports/application_use_cases.py`

### `MemoryGovernanceUseCase`

```text
review_lifecycle(session_id) -> MemoryLifecycleReviewResult
load_lifecycle_queue(session_id, queue_filter=None) -> MemoryLifecycleQueue
reopen_lifecycle_queue(session_id, actor, record_ids=None, queue_filter=None, note=None) -> MemoryLifecycleQueueUpdateResult
load_lifecycle_audit(session_id, audit_filter=None) -> MemoryLifecycleAuditLog
update_lifecycle_queue(session_id, actor, review_status, record_ids=None, queue_filter=None, note=None, resolution=None) -> MemoryLifecycleQueueUpdateResult
apply_lifecycle(session_id, actor, record_ids=None, queue_filter=None) -> MemoryLifecycleApplyResult
```

语义：

- `review_lifecycle`
  - 暴露 session scope 下的完整 lifecycle review 结果
  - 不直接改写 store，只返回 `effective_status / reason / hidden`
- `load_lifecycle_queue`
  - 将 lifecycle review 投影为产品可消费的 durable queue 读模型
  - 默认只返回 `allowed + status_changed + review_status=pending` 的 actionable items
  - 支持通过 `queue_filter` 按 `reason / current_status / effective_status / hidden / review_status` 做过滤
  - 每个 queue item 还会给出 `resolution_required`、推荐 `resolution_options` 和建议 note 模板，供 reviewer 面直接消费
- `reopen_lifecycle_queue`
  - 将 queue item 恢复为 `pending`
  - 适用于人工复核重新打开，而不是复用普通 status update 语义
  - 当未显式给出 `record_ids` 时，可通过 `queue_filter` 批量选中匹配的 queue item
- `load_lifecycle_audit`
  - 返回 durable 审计轨迹，回答谁在什么时候把 queue/review/apply 改成了什么
  - 支持通过 `audit_filter` 按 `action / record_id / actor / queue_review_status / resolution` 过滤
  - 支持 `latest_per_record_only`，用于直接读取每条 memory 最近一次人工处理结果
- `update_lifecycle_queue`
  - 持久化人工 review 状态 `pending / dismissed / applied`
  - 不直接改写 memory record，只更新 queue entry 的 review metadata
  - 可显式写入 reviewer resolution taxonomy；当 `reopen_lifecycle_queue` 把 item 恢复到 `pending` 时，已记录 resolution 会被清空
  - 当 review status 不变但 note 变化时，会留下 `review_note_updated` 审计动作
  - 当未显式给出 `record_ids` 时，可通过 `queue_filter` 对过滤命中的 queue item 做批量 review
- `apply_lifecycle`
  - 对选中的 record 应用已评审 lifecycle decision
  - 当未显式给出 `record_ids` 时，可通过 `queue_filter` 按 queue 选择批量 apply
  - 持久化写回仍通过 `MemoryRecordRepositoryPort`，业务规则 owner 继续在 `domain.memory`
  - 已执行的 queue item 会同步标记为 `review_status=applied`
  - 当 provider governance 允许时，application/use case 链路会把领域决策后的 `lifecycle_apply` 结果继续交给 external provider writeback，并把刷新后的 session durable 保存回 `SessionLedgerPort`

### `SessionInspectionUseCase`

```text
get_session(session_id) -> AgentSession | None
```

用于 explainability、回放和档案相关入口。

## 3. 业务调度层接口

### `MemoryDomainService`

```text
prepare_session(session, app, workflow) -> RecallBundle
recall(query) -> RecallBundle
preview_recall(session, limit=None) -> RecallPreview
distill_session(session) -> DistillationResult
explain_session_memory(session) -> Mapping[str, Any]
review_lifecycle(session) -> MemoryLifecycleReviewResult
load_lifecycle_queue(session, queue_filter=None) -> MemoryLifecycleQueue
reopen_lifecycle_queue(session, actor, record_ids=None, queue_filter=None, note=None) -> MemoryLifecycleQueueUpdateResult
load_lifecycle_audit(session, audit_filter=None) -> MemoryLifecycleAuditLog
update_lifecycle_queue(session, actor, review_status, record_ids=None, queue_filter=None, note=None, resolution=None) -> MemoryLifecycleQueueUpdateResult
apply_lifecycle(session, actor, record_ids=None, queue_filter=None) -> MemoryLifecycleApplyResult
```

语义：

- `prepare_session`
  - 在 workflow 执行前调用
  - 负责本轮装配与 recall
- `distill_session`
  - 在 session 完成后调用
  - 负责 evidence、candidate、promotion 和记忆沉淀
- `recall`
  - 支持独立调试、测试和网关查询复用
- `preview_recall`
  - 负责基于已冻结的 session assembly / augmentation 事实生成 recall 预览
  - 只读，不应触发新的 provider 写副作用
- `explain_session_memory`
  - 负责解释本轮记忆装配与来源
  - 当前应至少稳定投影 recalled memory 状态、promotion reasons、冻结的 recall plan、memory provider binding，以及 scoped records 的 `lifecycle_evaluations / lifecycle_queue_summary / lifecycle_audit_summary`
- `review_lifecycle`
  - 负责返回 session scope 下的完整 lifecycle review 结果
- `load_lifecycle_queue`
  - 负责把 review 结果投影为 durable queue 读模型和默认 batch selection
- `reopen_lifecycle_queue`
  - 负责把已关闭的 review item 恢复到 `pending`
  - 若 `record_ids` 为空，则可按 `queue_filter` 批量恢复匹配 queue item
- `load_lifecycle_audit`
  - 负责读取 durable 审计轨迹，不直接参与业务决策
  - 当前 audit read model 已保证 `latest_entries` 为最新优先，并额外提供 `latest_by_record`
- `update_lifecycle_queue`
  - 负责持久化人工 review 状态，不直接改写 memory record
  - 可显式持久化 reviewer resolution；当 queue item 被 reopen 回 `pending` 时，resolution 会被清空
  - 当仅更新 note 时，仍由 memory domain 决定审计动作类型
  - 若 `record_ids` 为空，则可按 `queue_filter` 对匹配 queue item 做批量 review
- `apply_lifecycle`
  - 负责将已允许的 lifecycle decision durable 写回 memory store
  - 若 `record_ids` 为空，则可消费 queue filter 做批量选择
  - 已执行的 queue item 会同步标记为 `applied`
  - 当 provider governance 允许 lifecycle writeback 时，会继续触发专门的 external `lifecycle_apply` 通道，并刷新 session explainability 事实

代码位置：

- `src/application/ports/domain_services.py`

## 4. 业务模型层下行接口

`memory` 领域向基础能力层声明的接口如下：

### `MemoryRecordRepositoryPort`

```text
save_memory_record(record) -> None
scan_memory_records(scope_filters, allowed_statuses) -> tuple[MemoryRecord, ...]
query_memory_records(query) -> tuple[MemoryRecord, ...]
```

约束：

- `scan_memory_records` 是当前正式 owner，用于把持久化扫描与 recall 排序拆开
- `query_memory_records` 只保留给兼容适配器或独立调试场景，不能再承载 recall budget / rank owner

### `EvidenceRepositoryPort`

```text
save_evidence(record) -> None
list_evidence(session_id) -> tuple[EvidenceRecord, ...]
```

### `MemoryDatasetRepositoryPort`

```text
save_sample(sample) -> None
list_samples(session_id) -> tuple[MemoryDistillationSample, ...]
```

### `MemoryLifecycleQueueRepositoryPort`

```text
list_lifecycle_queue_entries(session_id) -> tuple[MemoryLifecycleQueueEntry, ...]
replace_lifecycle_queue_entries(session_id, entries) -> None
```

约束：

- 只持久化 lifecycle review queue 的 durable state，不主导 lifecycle 业务决策
- entry 至少保留 `record_id / reason / effective_status / review_status / reviewed_by / reviewed_at / review_note`
- `domain.memory` 负责决定 queue 里出现什么以及何时从 `pending` 进入 `dismissed / applied`

### `MemoryLifecycleAuditRepositoryPort`

```text
list_lifecycle_audit_entries(session_id) -> tuple[MemoryLifecycleAuditEntry, ...]
append_lifecycle_audit_entries(session_id, entries) -> None
```

约束：

- 只持久化 lifecycle 审计轨迹，不主导 queue/review/apply 业务决策
- entry 至少保留 `record_id / actor / action / current_status / effective_status / queue_review_status / created_at`
- `domain.memory` 负责决定什么时候记审计以及 metadata 里带哪些治理解释

### `MemoryArchiveQueryPort`

```text
search_archive(app_id, query_text, limit=20) -> tuple[Mapping[str, Any], ...]
```

### `MemoryProfileResolverPort`

```text
resolve_profile(session, app_id, workflow_id) -> Mapping[str, Any]
```

### `MemoryRuleBundlePort`

```text
load_rule_bundle(workspace_root, profile_id) -> Mapping[str, Any]
```

### `MemoryReasoningPort`

```text
summarize_evidence(session, evidence_records) -> SummaryResult
extract_candidates(session, evidence_records, summary) -> CandidateDrafts
```

### `MemorySemanticSearchPort`

```text
semantic_search(namespace, query_text, limit=8, filters=None) -> tuple[Mapping[str, Any], ...]
```

### `RecallPlannerPort`

```text
plan(decision) -> RecallPlan
```

语义：

- 根据 `RecallGovernanceDecision` 物化本轮 recall 的 `scope_budgets`
- 保留领域已决定的 `scope_filters`、`allowed_statuses`、`ranking_strategy` 与显式排序指令
- 不直接读 store，也不直接做排序

### `RecallRankerPort`

```text
rank(plan, records, augmentation=None) -> tuple[MemoryRecord, ...]
```

语义：

- 基于 `RecallPlan` 执行预算裁剪、显式 bucket 排序和 top-k 收口
- 当前排序 owner 已从 store 查询中拆出，不再让 `MemoryStorePort.search()` 同时承担 scan 与 rank

代码位置：

- `src/domain/memory/ports.py`

## 5. 已落地的读模型与档案查询界面（首轮）

为满足 `MEM-BIZ-006` 和 `MEM-BIZ-008`，当前已在统一门面旁边补三组只读接口：

### `MemoryAssemblyQueryPort`

```text
get_session(session_id) -> AgentSession | None
search_session_archive(query, profile_id, limit=10) -> tuple[SessionArchiveHit, ...]
load_session_slice(session_id, cursor, limit) -> SessionTranscriptSlice
explain_session_assembly(session_id) -> SessionAssemblyManifest
```

### `SessionArchiveQueryPort`

```text
search_session_archive(query, profile_id, limit=10) -> tuple[SessionArchiveHit, ...]
get_session_summary(session_id) -> str | None
```

### `SessionTranscriptSlicePort`

```text
load_session_slice(session_id, cursor, limit) -> SessionTranscriptSlice
```

语义：

- `MemoryAssemblyQueryPort` 当前负责统一暴露 session inspection 读门面
- `SessionArchiveQueryPort` 负责回答“以前发生过什么”
- `SessionTranscriptSlicePort` 负责回答“历史会话具体片段怎么回放”
- `SessionAssemblyManifest` 当前已包含 `child_session_ids + child_digests + selected_model + model_bindings + backend_bindings`，用于回答“有哪些子任务摘要已经回收到父会话、默认装配选择了哪个模型/后端、这些绑定来自哪里，以及执行时实际用了哪些模型”
- `backend_bindings` 当前不仅覆盖 `llm_provider / memory_store`，也会投影 `capability_registry / approval_policy / delegation_transport` 的业务选择、Hermes bridge 契约元数据，以及 `binding_source / source_path / requested_binding_id` 这类 backend 来源治理信息
- `selected_model` 当前保持 session-start 默认 provider/model 选择及其治理元数据；`model_bindings` 负责记录 step 级真实调用轨迹，不再覆盖默认装配解释
- 这两类查询都不应借道长期记忆存储接口

## 6. Context 领域消费界面

### `RecallBundle`

```text
RecallBundle
- pinned_records
- retrieved_records
- evidence_refs
- diagnostics
```

约束：

- `Context Engine` 只能消费 `accepted` records
- `draft/rejected/superseded` 不默认进入上下文
- `diagnostics` 必须包含命中数量、过滤原因和预算信息；当前主链还会补 `scanned_count`、`recall_plan` 与 `external_augmentation_present`

### `RecallPreview`

```text
RecallPreview
- session_id
- query
- plan
- bundle
- scope_breakdowns
- record_rankings
- augmentation_preview
- memory_provider_binding
- external_recall_block
- metadata
```

约束：

- `RecallPreview` 属于独立治理读模型，不替代 `RecallBundle`
- 它回答的是“按当前冻结装配与当前 store 状态看，recall 会怎么执行”，而不是“真实执行时已经注入了什么”
- `scope_breakdowns` 必须显式给出每个 scope 的 budget、扫描集合、命中集合与 overflow 集合
- `record_rankings` 必须把 `scan -> rank -> select` 的排序轨迹显式化，区分 `scope_budget`、`overflow_candidate` 与 `overflow_fill`
- `augmentation_preview` 必须解释 external memory augmentation 的 provider/source/namespace，以及 recall block 是否存在、来自哪里
- `query` 当前也会携带 `query_text`，供 external/vector provider 在不越过 domain owner 的前提下做 provider-owned retrieval

## 7. 蒸馏与晋升界面

### `DistillationResult`

```text
DistillationResult
- evidence_records
- candidates
- promotion_decisions
- promoted_records
```

### `PromotionDecision`

```text
PromotionDecision
- candidate_id
- status
- reason
- supporting_refs
```

### `MemoryPromotionPolicy`

```text
evaluate(candidate) -> (status, reason)
```

语义：

- 独立负责 confidence threshold、allowed scope 和 default draft kinds
- 不直接写 store
- 由 `memory` 领域在蒸馏流程中调用
- 首版允许通过 settings / env 外置化

## 8. 基础能力层与基础设置层界面

这里不再让业务层直接面向具体存储实现，而是统一经过基础能力层 provider 接口：

```text
StructuredStoreProviderPort
SearchIndexProviderPort
VectorIndexProviderPort
RuleSourceProviderPort
ProfileSourceProviderPort
EmbeddingProviderPort
```

这些接口由基础能力层定义，由基础设置层实现。

## 9. Summarizer / Extractor / Provider 界面

### `MemorySummarizerPort`

```text
summarize_evidence(payload) -> SummaryResult
extract_candidates(payload) -> CandidateDrafts
```

约束：

- Summarizer 只返回候选草案
- 不直接写 memory store
- 不直接决定 promotion status
- 首版默认可用 `null summarizer` 占位；是否启用 LLM 总结器不影响 deterministic gate 生效
- 当容器显式配置 `memory_summarizer_provider/model` 时，可启用 `LLMMemorySummarizer`
- `LLMMemorySummarizer` 当前严格要求 extraction 输出至少包含 `title` 和 `body`
- `kind / scope / confidence` 由运行时配置控制，模型输出中的同名字段默认忽略

### `MemoryProviderPort`

当前正式落点：

- 接口 owner：`src/domain/memory/ports.py`
- 协调器：`src/runtime/memory/provider_manager.py`
- 基础设置实现：`src/settings/memory/provider.py`

```text
initialize(binding, session_id) -> None
prefetch(query, session_id) -> str
sync_turn(session_id, latest_events) -> None
on_session_end(session_id, distillation_result) -> None
on_lifecycle_apply(session_id, apply_result) -> None
on_delegation(digest) -> None
```

约束：

- built-in local memory store 永远存在，external provider 只是 augmentation
- 同时只允许 1 个 external provider 激活，避免 schema 膨胀与可解释性退化
- provider 返回的 recall block 只能作为附加上下文，不得绕过 promotion / evidence 真相源
- provider 返回的 recall block 必须带显式 context fence / system note，并在注入前做 sanitize
- provider manager 现在直接消费 `MemoryProviderGovernanceDecision`；`writable`、delegation shared-write 等门槛由 `domain.memory` 先决策，再由 service 决定是否调用 manager
- `apply_lifecycle` 不复用 `session_end` 写回语义；provider 现在拥有专门的 `on_lifecycle_apply()` 通道，用于同步 lifecycle review/apply 结果
- provider manager 当前会合并 `contract_metadata()` 与可选 `prefetch_diagnostics()`，并在 runtime 边界直接输出 compact 的 canonical explainability，而不是继续平铺 legacy 顶层 alias
- 当前基础设置实现已提供 `none / in_memory / jsonl / jsonl_vector / remote_http` 五档；其中 `jsonl` 会把 provider-owned snapshot / turn / digest state 落到独立 JSONL root，`jsonl_vector` 会基于 `query_text` 对这些 provider-owned state 做向量式 rank/prefetch，并在 lifecycle apply 时同步移除 `superseded / forgotten` snapshot，`remote_http` 则通过 settings-layer `http_client` 的 `file:// + http(s)` JSON transport 拉取远端 recall block 与 hits，并可选写回 `sync / session_end / lifecycle_apply / delegation` 事件；当前 binding metadata 还可声明 `metadata_file`、`request_headers / bearer_token(_env|_file) / signature_secret(_env|_file) / signature_key_id / retry_status_codes / max_retries / timeout_seconds`、canonical `hmac-sha256` 签名串、`prefetch_response_validation`、`*_failure_policy` 与 `secret_catalog_file`，其中 `RemoteHttpMetadataResolver` 会把 `recall / sync / session_end / lifecycle_apply / delegation` 的 endpoint、response contract、response validation、failure policy、canonical `bearer_token*` 以及 legacy alias fallback 收口到统一解析路径，并投影为 `RemoteHttpRequestGovernance`；当前 preview diagnostics 已跨 `jsonl / jsonl_vector / remote_http` 对齐 `query_terms / source_breakdown / result_truncated / budget_trace / rank_trace / hit_provenance / contract_trace / access_trace / writeback_trace`，并由 provider manager、stored replay、domain preview 回读和 session/manifest 落盘共用的 normalize/compact/project-stored/preview-project 路径统一兼容 legacy 输入；其中 preview 顶层现已完全保留 canonical 诊断，不再暴露 `legacy_aliases`；stored replay 现还会基于 `provider_id` 推断默认 contract metadata，并基于 `memory_provider_binding.metadata.recall_endpoint_url` 恢复 remote access 默认值，因此 `bridge_kind / provider_kind / storage_kind / retrieval_kind / response_contract / response_contract_source / endpoint_url` 这组 legacy 顶层键已经不再需要作为输入事实源；`access_trace` 现承载 transport auth、retry/timeout、secret selection 与 catalog source，`contract_trace` 现承载 prefetch `response_validation_error`，`writeback_trace` 现承载 `successes / response_oks / response_statuses / response_messages / response_report_ids / failure_policies / response_validation_errors` 这组稳定 outcome 摘要，而 `detail_reports` 已成为 canonical drill-down 字段，仅在存在实际写回明细时才保留；旧的 `reports` 只作为 replay/normalize 输入兼容；`budget_trace` 现继续承载 `selected_hit_count / selected_hit_ids / query_text_present`，旧的 `hit_count / hit_ids / query_text_present` 仅在 normalize/backfill 阶段作为兼容输入

## 10. 外部适配器可见数据

对外 adapter 可稳定读取：

- `AgentSession.recalled_memories`
- `AgentSession.memory_candidates`

---

本目录负责把需求、接口、文档和验证结果串起来，避免“代码变了但不知道该改哪些文档”。

## 1. 推荐阅读顺序

1. [需求追踪矩阵](../04-product/requirements-matrix.md)
2. [接口追踪矩阵](./interface-matrix.md)
3. [文档索引](../document-index.md)

## 2. 使用规则

- 需求变化先改需求矩阵
- 接口和函数变化先改接口矩阵
- 新增正式文档要登记到文档索引

---

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

---

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

<!-- sf:section-id=PROJECT-KNOWLEDGE-TRACE -->
## 项目知识接口追踪增补

关系图的默认类型为 `CONTAINS`、`SATISFIES`、`IMPLEMENTS`、`VERIFIES`、`BLOCKS`、`SUPERSEDES`、`DEPENDS_ON`、`EVIDENCES`、`RELEASES` 和 `MENTIONS`。强关系只来自 `.factory/project-knowledge/relation-declarations.json`、正式 ID 引用或可证明结构关系；全文搜索最多产生弱 `MENTIONS`，不得升级为完成或验证事实。

从需求到设计、代码和测试的边保持来源 ID、强度、置信度和可选 evidence locator；同一关系由不同来源声明时分别保留。`trace` 默认深度 2、上限 100 节点/200 边，断链必须给诊断，不能静默丢弃。

## 正式版本历史（仅已发布）

| 版本 | 日期 | 变更 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v3.0.0` | 2026-07-18 | 基于 `TASK-DESIGN-001-R019` 正式落档 | `uroborus` | `uroborus` | `uroborus` |
| `v3.1.0` | 2026-07-22 | 增补需求、设计、实现、测试的关系类型、来源和查询边界 | `uroborus` | `uroborus` | `uroborus` |
