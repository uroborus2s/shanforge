# 分层领域与接口总表

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

| 层 | 作用 | owner 逻辑 | 下行依赖 |
|---|---|---|---|
| 用户界面层 | Web、CLI Host、人机交互 | 页面、命令体验、交互编排 | 接口/网关层 API/CLI Gateway |
| 接口/网关层 | API、CLI 命令网关、协议收口 | 请求绑定、协议转换、出入参归一化 | 业务调度层应用用例 |
| 业务调度层 | 用例编排、事务边界、流程协同 | run app、describe workflow、query session | 业务模型层领域服务 |
| 业务模型层 | 平台业务规则与领域逻辑 | 记忆、会话、流程、上下文、审批、委派、响应 | 基础能力层统一能力 |
| 基础能力层 | 通用技术能力抽象 | 文件、存储、检索、模型、工具、规则源、时间、工作区等能力编排 | 基础设置层 provider |
| 基础设置层 | 真实实现 | 文件系统、数据库、SDK、外部系统、容器装配 | 无 |

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
| `runtime_gateway` | 运行 Agent/App/Workflow 的统一入口 | `src/access/api/`, `src/access/cli/` |
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
- `skill_catalog`
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
| `skill_source` | skill 索引与正文加载 | `src/runtime/` 目标模块 |
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
  - `MemorySkillCatalogPort`
  - `MemoryReasoningPort`
  - `MemorySemanticSearchPort`

### 5.5 `context` 领域

- 上行实现：`ContextDomainService`
- 下行能力：
  - `ContextRuleBundlePort`
  - `ContextSkillContentPort`
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
