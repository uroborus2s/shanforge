# 基础设置层与外部资源设计

**项目名称：** 山海工枢 / shanforge  
**文档状态：** `v2` 基础设置层详细设计基线  
**负责人：** 仓库维护者  
**主要读者：** 架构 | 平台开发 | 适配器维护者 | 测试  
**上游输入：** PRD | 需求分析 | 系统架构 | 模块边界 | 核心领域与能力清单  
**下游输出：** 端口实现 | 适配器实现 | 契约测试 | 实施计划  
**关联 ID：** `REQ-001`, `REQ-004`, `REQ-005`, `REQ-006`, `REQ-007`, `REQ-008`, `NFR-001`, `NFR-002`, `NFR-003`, `NFR-004`, `MOD-005`, `MOD-006`, `MOD-007`, `MOD-008`, `MOD-009`, `MOD-010`, `MOD-012`, `MOD-013`, `API-004`, `API-006`, `API-007`, `API-008`, `API-009`, `API-010`, `API-012`, `API-013`  
**最后更新：** 2026-04-17

## 1. 目标

本文件只回答 4 个问题：

1. 六层架构里的“基础设置层”到底是什么。
2. 它和“基础能力层”如何明确分开。
3. 当前代码里哪些目录属于基础设置层。
4. 基础设置层应该如何实现上层 provider 接口，并优先复用 Hermes 的成熟实现。

## 2. 正式定义

基础设置层是平台对真实资源、真实系统和真实装配方式的统一实现区。

这里的“设置”不是指业务参数，而是指：

- 文件系统与工作区资源
- 本地持久化与外部数据库
- 模型供应商 SDK 与远程服务
- 远程或遗留外部系统
- 容器装配、实现切换和运行配置

因此，基础设置层不等于基础能力层。

### 2.1 基础能力层和基础设置层的分工

| 层 | 回答的问题 | 当前代码 |
|---|---|---|
| 基础能力层 | “平台对上提供什么统一技术能力” | `src/runtime/` |
| 基础设置层 | “这些能力背后由什么真实资源和实现来支撑” | `src/settings/` |

正式定稿：

- 文件访问、结构化存储、检索、向量、模型调用、规则源、技能源、profile 源、审批通道、委派通道属于基础能力层。
- 文件系统、外部数据库、provider SDK、Hermes bridge、JSONL store、container 装配属于基础设置层。

## 3. 代码边界

基础设置层现在只有一个正式代码根：`src/settings/`。

层内再按实现领域与支撑模块组织：

| 组别 | 目录 | 作用 |
|---|---|---|
| 模型与 provider | `src/settings/model/` | 模型供应商实现与注册 |
| 持久化与档案 | `src/settings/memory/`、`src/settings/session/` | memory、evidence、dataset、session、artifact、archive 实现 |
| 本地资源与目录 | `src/settings/workspace/`、`src/settings/skills/` | 工作区、技能目录、本地源数据实现 |
| 治理与桥接 | `src/settings/approval/`、`src/settings/delegation/`、`src/settings/gateway/`、`src/settings/capability_registry/`、`src/settings/hermes/` | approval、delegation、gateway、registry 与 Hermes bridge |
| 装配与共享支撑 | `src/settings/composition/`、`src/settings/shared/` | settings、container、JSONL 等层内公共基础设施 |

这些都属于基础设置层的层内分域，不是新增层次。

## 4. 设计原则

### 4.1 消费者拥有接口

基础设置层不能拥有上层接口，只能实现它们。

统一规则：

```text
上层声明需要什么；基础设置层负责满足它。
```

因此：

- 接口/网关层拥有应用用例接口，例如 `RuntimeExecutionUseCase`。
- 业务调度层拥有领域服务接口，例如 `MemoryDomainService`。
- 业务模型层拥有对基础能力层的下行接口，例如 `MemoryRecordRepositoryPort`、`CapabilityExecutionPort`。
- 基础能力层拥有对基础设置层的 provider 接口，例如 `LLMProviderPort`、`StructuredStoreProviderPort`、`RuleSourceProviderPort`。
- 基础设置层负责实现 domain-owned 持久化端口和 runtime-owned provider 接口，并完成最终装配。

### 4.2 不承载业务规则

基础设置层不能决定：

- workflow 如何编排
- memory 是否应该晋升
- approval 是否应该放行
- response 如何向业务解释

这些都属于业务调度层或业务模型层。

### 4.3 只返回领域契约或 provider 语义

基础设置层对上只能返回领域对象、协议对象和稳定错误语义，不能直接向上暴露：

- SDK 原始对象
- 数据库游标
- HTTP client 原始响应
- shell 内部执行细节

### 4.4 可替换实现

每个基础设置接口都应支持：

- 至少一个 `in-memory / local` 实现
- 至少一个真实外部或持久化实现

当前仓库已初步做到：

- `in-memory`
- `JSONL-backed`
- `Hermes-backed scaffold`

## 5. 基础设置层实现清单

### 5.1 模型供应商实现

| 能力 | 上层接口 | 当前实现 |
|---|---|---|
| 模型生成 | `LLMProviderPort` | `src/settings/model/mock_provider.py`、`openai_provider.py`、`anthropic_provider.py` |
| 向量生成 | `EmbeddingProviderPort` | `src/settings/model/embedding_provider.py` 的首轮 skeleton，后续再绑定真实 embedding backend |

这里的 provider adapter 属于基础设置层，因为它们封装的是具体 SDK 与供应商差异。

### 5.2 源数据与执行 backend 实现

| 能力 | 上层接口 | 当前实现 |
|---|---|---|
| 规则源 | `RuleSourceProviderPort` | `src/settings/workspace/` 或未来 `src/settings/rules/` |
| skill 源 | `SkillSourceProviderPort` | `src/settings/skills/` |
| profile 源 | `ProfileSourceProviderPort` | `src/settings/workspace/source_provider.py` + `profile_catalog.py` + `backend_catalog.py` + `provider_catalog.py`；支持 workspace `profiles.json`、专门 `backend-bindings.json`、`provider-bindings.json`、profile-specific override 与 default profile |
| web search / document | `WebSearchProviderPort`、`WebDocumentProviderPort` | `src/settings/shared/web_provider.py` 的首轮 local bridge，后续可升格到专门分域或 Hermes-assisted provider |
| 浏览器自动化 | `BrowserAutomationProviderPort` | `src/settings/shared/browser_provider.py` 的首轮 local bridge，后续可升格到专门分域 |
| 审批后端 | `ApprovalBackendPort` | `src/settings/approval/` |
| 委派后端 | `DelegationBackendPort` | `src/settings/delegation/` |
| workspace / shell / git / http | `WorkspaceProviderPort`、`ShellCommandProviderPort`、`GitProviderPort`、`HttpClientProviderPort` | `src/settings/workspace/` 的首轮 local bridge、workspace profile/backend/provider catalogs 与 profile-scoped override，`src/settings/gateway/http_client.py` 的 `file:// + http(s)` JSON transport，以及 `src/settings/gateway/` 的宿主适配 |

### 5.3 持久化实现

| 能力 | 上层接口 | 当前实现 |
|---|---|---|
| 文件系统 | `FileSystemProviderPort` | `src/settings/workspace/` 或未来 `src/settings/file_access/` |
| 结构化存储 | `StructuredStoreProviderPort` | `src/settings/shared/`、`src/settings/session/`、`src/settings/memory/` |
| blob 存储 | `BlobStoreProviderPort` | `src/settings/session/blob_store.py` 的首轮 in-memory skeleton |
| 搜索索引 | `SearchIndexProviderPort` | `src/settings/session/search_index.py` 的稳定入口，当前 archive-backed 实现仍落在 `src/settings/session/archive.py` |
| 向量索引 | `VectorIndexProviderPort` | `src/settings/session/vector_index.py` 的空实现骨架 |

### 5.4 装配实现

| 能力 | 代码位置 | 作用 |
|---|---|---|
| settings layer catalog | `src/settings/catalog.py` | 作为基础设置层功能域、能力清单和模块入口的稳定事实源 |
| runtime settings | `src/settings/composition/settings.py` | 读取环境配置与实现开关 |
| provider manager | `src/settings/composition/provider_manager.py` | 解析 `llm_provider` 的业务选择、provider readiness 与 fallback explainability |
| default container | `src/settings/composition/container.py` | 按配置装配基础能力层与基础设置层 |
| business bindings | `src/settings/composition/component_bindings.py` | 把 `shanforge` 的业务 ID 绑定到本仓真实实现 |
| external DI kernel | `../shanforge-di`（通过 `pyproject.toml` + `uv` 依赖） | 提供注解注册、受控反射、registry、resolver、container 等纯技术能力 |

### 5.5 外部 DI 技术库

为避免把实现选择规则继续写死在 `shanforge` 仓内，基础设置层正式改为依赖外部技术库 `shanforge-di`。该库只负责注册、受控反射与依赖注入；`shanforge` 自己只保留业务绑定与默认容器。

正式目标：

- 让前端、用户配置和 profile 只面向稳定的业务字符串，例如 `provider_id`、`backend_id`、`profile_id`。
- 让 `src/settings/composition/container.py` 收敛为薄装配门面。
- 让 `src/settings/composition/component_bindings.py` 只表达“业务 ID -> 本仓实现”的绑定，不再承载技术内核。
- 让反射加载、实现注册、工厂实例化、生命周期管理和 allowlist 安全边界统一收口在外部 `shanforge-di`。

明确非目标：

- 不让 `shanforge` 仓内重新复制一套 `loader / registry / resolver` 内核。
- 不让 `application / domain / runtime` 普遍直接依赖 `shanforge-di`。
- 不把 `class_path`、`module_path` 暴露给前端、用户入参或业务配置。
- 不用该技术库承载业务编排本身；业务编排仍在各层自己的正式 owner 中完成。

### 5.6 业务字符串与技术字符串边界

基础设置层装配框架必须区分两类字符串：

| 类型 | 例子 | 谁可见 | 规则 |
|---|---|---|---|
| 业务字符串 | `provider_id=\"openai\"`、`backend_id=\"jsonl\"`、`profile_id=\"local-dev\"` | 前端、用户配置、业务层策略对象 | 允许进入上层，但只表达业务选择，不表达 Python 实现细节 |
| 技术字符串 | `module_path`、`class_path`、`callable_path` | 外部 `shanforge-di` 与极薄的本地集成层 | 只允许存在于外部 DI 技术库或其受控集成点中，禁止外露到业务层 |

正式规则：

- 业务层最多保留业务 ID，不接触技术字符串。
- 技术字符串只能由外部 `shanforge-di` 解释。
- 业务 ID 必须稳定，允许底层实现类名和路径变更而不影响上层。

### 5.7 框架结构与运行机制

当前正式结构分成“外部技术内核 + 本地业务绑定”两部分：

| 模块 | 责任 |
|---|---|
| `shanforge-di.decorators/contracts` | 定义组件元数据、依赖引用、生命周期 |
| `shanforge-di.loader/registry/resolver/container` | 提供受控反射、业务名注册、依赖解析与统一门面 |
| `src/settings/composition/component_bindings.py` | 声明 `llm_provider / memory_store / approval_policy / delegation_transport / web_search / web_document / shell_command / git / browser_automation` 等业务绑定 |
| `src/settings/composition/container.py` | 读取 settings、选择业务 ID、把解析结果接成平台对象图 |

推荐运行链：

```text
profile_id / provider_id / backend_id
  -> workspace profile/backend/provider catalogs / env settings
  -> provider_manager resolve(default provider/model + readiness)
  -> component_bindings
  -> shanforge-di registry lookup
  -> shanforge-di reflection / factory instantiate
  -> shanforge-di lifecycle cache(singleton / transient)
  -> container thin wiring
```

### 5.8 生命周期、安全与契约校验

首版正式支持两种生命周期：

- `singleton`
- `transient`

`session` 级生命周期暂不进入首版正式范围。

首版强制安全边界：

- 只允许加载 allowlist 内的模块和对象。
- 禁止 `eval`、`exec` 或用户直接传任意 class path。
- 先校验注册元数据和实例契约，再校验实例是否满足指定接口或构造约束。
- `shanforge-di` 只允许由 `src/settings/composition/` 集成使用。

### 5.9 与现有容器的对接原则

`build_default_container()` 后续按以下原则收敛：

- 继续保留为默认容器入口。
- 不再持有反射 / registry / resolver 技术内核。
- 继续手写创建稳定编排对象，例如 `ExecutionService`、`AgentKernel`、`ContextEngine`、`ResponseNormalizer`、领域服务对象。
- provider、store、Hermes-backed adapter、profile 绑定等实现选择，改由 `component_bindings + shanforge-di` 驱动。

正式定稿：

- `src/settings/composition/` 继续作为 `shanforge` 本地唯一 composition root。
- 当前不新增顶层 `src/composition/`。
- DI 技术内核已外置到独立库 `shanforge-di`，`shanforge` 仓内不再保留同类自研实现。

## 6. 对上服务方式

基础设置层对上的正式服务对象只有一类：

| 服务对象 | 上层角色 | 例子 |
|---|---|---|
| 基础能力层 | 需要 provider、store、source、backend 等真实实现 | `LLMProviderPort`、`StructuredStoreProviderPort`、`RuleSourceProviderPort` |

注意：

- 业务调度层原则上不直接碰基础设置层。
- 业务模型层也不直接触碰基础设置实现。
- 所有真实资源都要先经过基础能力层的 provider 接口收口。
- `shanforge-di` 只允许 composition root 和本地业务绑定层集成使用；业务层和普通 runtime service 不得自行解析实现。

## 7. Hermes 复用策略

Hermes 的复用只允许发生在基础设置层实现区。

### 7.1 复用原则

- 先有 `shanforge` 自己的领域契约和端口。
- 再用 Hermes 的成熟模块去实现这些端口。
- 不能为了复用 Hermes 而反向改写本仓的层边界。

### 7.2 当前映射

| `shanforge` 目标 | 优先复用的 Hermes 位置 | 当前落点 |
|---|---|---|
| 规则 / skill / profile 源适配 | `gateway/session.py`、相关加载逻辑 | `src/settings/workspace/`、`src/settings/skills/` 及后续分域 |
| 能力注册表适配 | `tools/registry.py`、`model_tools.py` | `src/settings/capability_registry/hermes_registry.py` |
| 审批后端 | `tools/approval.py` | `src/settings/approval/hermes_policy.py` |
| 委派后端 | `tools/delegate_tool.py` | `src/settings/delegation/hermes_transport.py` |
| 外部桥接适配 | `gateway/platforms/base.py`、`gateway/session_context.py` | `src/settings/gateway/`、`src/settings/hermes/` |

### 7.3 明确禁止

禁止把 Hermes 的以下内容直接拉进上层：

- 顶层 agent loop
- 产品级 prompt 拼装
- Hermes 私有 session 协议
- 任何要求上层直接持有 Hermes 内部对象的路径

### 7.4 当前已落地的 Hermes adapter 契约收口

- `capability_registry / approval_policy / delegation_transport` 的 Hermes-backed adapter 已补统一 `contract_metadata()`，至少暴露 `bridge_modules`、`bridge_repo_root`、`contract_ready` 与 `fallback_class`
- 默认容器现会先合并 workspace `backend-bindings.json`、profile-specific backend override 与 legacy settings fallback，再把 governance adapter 的实际选择写入 `backend_ids`
- 默认容器现也会先合并 workspace `provider-bindings.json`、profile-specific provider override 与 legacy settings fallback，再由 `provider_manager` 选择“当前可运行的默认 provider/model”
- `SessionAssemblyManifest.backend_bindings` 现在不只记录 `llm_provider / memory_store`，也会投影 `capability_registry / approval_policy / delegation_transport` 的绑定、`binding_source / source_path` 这类来源元数据，以及 `requested_binding_id` 导致的 fallback 解释
- `SessionAssemblyManifest.selected_model` 当前保持 session-start 默认装配选择；实际 prompt step 调用轨迹继续落在 `model_bindings`
- 默认容器现也会把 `memory_provider` 纳入 `backend-bindings.json` 治理来源，通过 `src/runtime/memory/provider_manager.py` 协调 single external provider；`SessionAssemblyManifest` 会冻结 `memory_provider_binding`，session context 会注入带显式 fence 的 `external_memory_recall_block`
- `src/settings/memory/provider.py` 现已提供 `memory_provider:jsonl / jsonl_vector / remote_http`；其中 `jsonl / jsonl_vector` 把 provider-owned snapshot / turn / digest state 落到 profile-scoped JSONL root，`jsonl_vector` 会基于 `RecallQuery.query_text` 做 provider-owned rank/prefetch，`remote_http` 则通过 settings-layer `http_client` 的 `file:// + http(s)` JSON transport 拉取远端 recall block/hits，并支持 `request_headers / bearer_token(_env|_file) / signature_secret(_env|_file) / signature_key_id / retry_status_codes / max_retries / timeout_seconds`、`method + path + query + body_sha256 + timestamp` 的 canonical `hmac-sha256` 签名串、内建 `remote_memory_prefetch_v1 / remote_memory_writeback_ack_v1` response contract 投影，以及由 `src/settings/workspace/secret_catalog.py` 统一承载的 durable secret governance provider；该 provider 负责 `secret_catalog_file` 的加载、相对路径解析、`default_signature_key_id / signature_keys / default_bearer_token_id / bearer_tokens` 的 key rotation 选择、selection-source audit，以及 metadata-only secret id fallback。与此同时，`src/settings/memory/remote_http_metadata.py` 新增 `RemoteHttpMetadataResolver + RemoteHttpRequestGovernance`，把 `recall_endpoint_url / sync_endpoint_url / session_end_endpoint_url / delegation_endpoint_url`、`recall_response_contract / sync_response_contract / session_end_response_contract / delegation_response_contract`、`recall_response_validation / sync_response_validation / session_end_response_validation / delegation_response_validation`、`sync_failure_policy / session_end_failure_policy / delegation_failure_policy`、canonical `bearer_token*` 键，以及 legacy `endpoint_url / prefetch_response_contract / writeback_response_contract / prefetch_response_validation / writeback_response_validation / writeback_failure_policy / auth_bearer_token*` alias fallback，统一投影为 provider 可直接消费的 request governance 读模型。当前 `jsonl / jsonl_vector / remote_http` 也已对齐一组共有 explainability 诊断：`query_terms / source_breakdown / result_truncated / budget_trace / rank_trace / hit_provenance / contract_trace / access_trace / writeback_trace`；`src/runtime/memory/provider_manager.py` 与 `src/domain/memory/service.py` 现会共用 `src/domain/memory/augmentation_diagnostics.py` 的 trace-first normalizer，但 runtime provider manager 自身已在输出侧直接压成 compact canonical diagnostics，不再主动平铺 `bridge_kind / retrieval_kind / endpoint_url / response_contract / attempt_count / writeback_enabled / writeback_reports` 这类 legacy 顶层键；这些 alias 仅在读取冻结的 legacy diagnostics 时作为 normalize 输入兼容，而 `DefaultMemoryDomainService` 的 stored replay 过滤也已收口到同一模块的 `project_stored_augmentation_diagnostics()`，不再在 service 内部硬编码一份独立 `allowed_keys`。同时，stored replay 现会基于 `memory_provider_binding.provider_id` 推断默认 `bridge_kind / provider_kind / storage_kind / retrieval_kind / response_contract / response_contract_source`，并基于 `memory_provider_binding.metadata.recall_endpoint_url` 恢复 remote access 默认值，所以这组 legacy 顶层键已不再需要继续保留在 replay 输入白名单里。与此同时，`prepare_session / distill_session / _refresh_session_assembly_manifest()` 已把 session/context 与 manifest diagnostics 的落盘口径压成 compact trace-first 版本，而 `preview_recall()` 现已完全只暴露 canonical trace-first 诊断，不再输出 `legacy_aliases`。当前 transport auth、retry/timeout、secret selection 与 catalog source 已统一进入 `access_trace`，prefetch `response_validation_error` 已进入 `contract_trace`，writeback 的 `successes / response_oks / response_statuses / response_messages / response_report_ids / failure_policies / response_validation_errors` 摘要则进入 `writeback_trace`，而 `detail_reports` 已成为 canonical drill-down 字段，仅在存在实际写回明细时才保留；旧的 `reports` 只作为 replay/normalize 输入兼容；`budget_trace` 现继续承载 `selected_hit_count / selected_hit_ids / query_text_present`，`writeback_reports` 则仍稳定回读 `request_kind / response_ok / response_status / response_message / response_report_id` 等细节。
- workspace `backend_binding_metadata` 现还支持 `metadata_file`，把远端 endpoint、secret source 和 failure policy 从主 catalog 内联 JSON 提升成更稳定的 settings source；`metadata_file` 中的相对 `*_file` 路径会按源文件目录解析成稳定绝对路径
- 对应契约测试已落在 `tests/test_composition_container.py`、`tests/test_composition_resolver.py`、`tests/test_infrastructure_scaffold.py`、`tests/test_platform_scaffold.py`

## 8. 下一批基础设置工作

下一轮基础设置层优先补齐：

- 外部数据库或更稳定本地持久化实现
- 把 `workspace / file / git / shell` 的 local bridge 扩成 profile 化、可远端化的正式 backend
- 把 `web_search / web_document / browser_automation` 从首轮 local bridge 扩成更稳定的专门实现
- gateway 的真实多宿主适配
- 在已落地 `none / in_memory / jsonl / jsonl_vector / remote_http` 的基础上，继续把 budget/rank explainability 统一到跨 backend 语义，并继续减少 provider-specific 诊断字段碎片
- 与 `shanforge-di` 的 profile / source / contract 对齐
- 让 `container.py` 继续保持只做薄装配和对象接线的 composition root

## 9. 一句话定稿

基础设置层的正式定义是：

```text
为平台提供文件、数据库、provider、外部系统和装配实现的统一实现区。
```

当前代码中：

- `src/settings/` 是基础设置层唯一正式代码根
- `src/settings/` 内部按实现领域和支撑模块分域
- `src/settings/composition/` 负责 settings、container、本地业务绑定与唯一 composition root
- `shanforge-di` 负责外部反射 / registry / resolver / lifecycle 等纯技术内核

基础设置层只服务于基础能力层和上层声明的端口，不反向主导业务调度层和业务模型层。
