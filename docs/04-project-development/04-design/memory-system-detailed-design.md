# 记忆系统详细设计方案

**项目名称：** 山海工枢 / shanforge  
**文档状态：** `v0.2` 业务驱动详细设计  
**负责人：** 仓库维护者  
**主要读者：** 架构 | 平台开发 | 业务 Agent 开发 | 测试 | 运营协作者  
**上游输入：** [记忆系统业务需求文档](../03-requirements/memory-system-business-requirements.md) | [记忆运行时设计](./memory-runtime-design.md) | [记忆系统对外界面](./memory-runtime-interfaces.md) | [架构分层与代码映射说明](./architecture-layer-code-mapping.md) | [Hermes Agent 源码与实现原理调研报告](../02-discovery/hermes-agent-source-analysis-report.md)  
**下游输出：** 代码实现 | 追踪矩阵 | 测试计划 | `.factory/memory` 摘要  
**关联 ID：** `REQ-006`, `MOD-007`, `MOD-010`, `API-006`, `API-007`, `MEM-BIZ-001` ~ `MEM-BIZ-008`  
**最后更新：** 2026-04-19

## 1. 这份文档解决什么问题

现有 `memory-runtime-design.md` 文件已经回答了“记忆为什么要成为平台一级能力专题、recall / promotion / distill 怎么分层、当前实现闭环怎么落地”。
治理边界、分层 owner 与开发分阶段收口，现由 [记忆治理专项设计方案](./memory-governance-design.md) 单独说明。
本文件进一步回答业务侧真正关心的 8 个问题：

1. 会话启动时，哪一层负责决定长期记忆域、项目规则和技能装配。
2. 不同生产线、混合技术栈项目和多 Agent 协作场景下，记忆系统如何避免污染。
3. 记忆系统在平台分层中的正式位置，以及与 `Context Engine`、`Session Store`、`Skill` 的边界。
4. 领域模型如何把“长期记忆、会话档案、项目规则、Skill、子 Agent 汇总”严格区分。
5. 存储系统如何在 `local-first` 前提下做到隔离、可审计、可解释和可演进。
6. 当前代码骨架基础上，下一步应该新增哪些端口、读模型和源代码落点。
7. `hermes-agent` 的记忆系统设计精华里，哪些适合直接吸收，哪些只适合抽象借鉴。
8. 主 Agent 从业务角度看，当前方案最该优先补什么，哪些能力必须延后。

这份文档的定位不是替代 `memory-runtime-design.md`，而是为其补上“业务装配治理 + 详细工程落点 + Hermes 启发吸收”。

## 2. 业务约束到设计原则的映射

| 业务约束 | 设计原则 | 设计结果 |
|---|---|---|
| `MEM-BIZ-001` 会话启动必须路由到正确长期记忆域 | 长期记忆域由显式 `profile` 或等价入口决定，`cwd` 不负责切脑子 | 引入 `ProfileMemoryDomain` 与 `ProfileResolverPort` |
| `MEM-BIZ-002` 不同生产线长期记忆隔离 | 长期记忆至少按 `profile` 分桶，不默认全局共池 | 记忆存储按 `profile_id` 物理或逻辑分区 |
| `MEM-BIZ-003` 混合技术栈项目要“单项目记忆 + 多 skill 按需加载” | 项目记忆与技能装配分层治理 | 引入 `SessionAssemblyManifest`，将项目记忆、项目规则、skills 分开记录 |
| `MEM-BIZ-004` skill 必须索引先行、正文按需加载 | skill 属于流程资产，不属于事实记忆 | 引入 `SkillCatalogPort`；上下文只放激活 skill，不全量放 skill 正文 |
| `MEM-BIZ-005` 长期记忆自动维护但保持小而精 | recall、promotion、merge、decay 分离治理 | 引入 `RecallPlannerPort` / `RecallRankerPort` 与 retention policy |
| `MEM-BIZ-006` 会话档案与长期记忆分层 | session ledger 是第一事实源，memory record 是二级蒸馏资产，历史回查走独立 archive query | append-only 会话档案、独立 evidence store、独立 memory store、独立 `SessionArchiveQueryPort` |
| `MEM-BIZ-007` 多 Agent 协作由主 Agent 串联 | 子 Agent 默认只产出 digest，不直接改写共享长期记忆 | 引入 `SubAgentDigest`、`DelegationDigestStorePort` 与 child-isolated memory policy |
| `MEM-BIZ-008` 当前装配结果必须可解释 | “装配了什么”必须成为一等读模型，且 session-start snapshot 要稳定 | 引入 `SessionAssemblyManifest`、`MemoryAssemblyQueryPort` 与 `AssemblySnapshotPolicy` |

## 3. 系统分层

### 3.1 领域定位

记忆是业务模型层中的核心领域，不再用“跨层子系统 owner”描述。

在六层架构内，记忆领域内部仍然可以拆成两个协作平面 + 一个支撑查询面：

- 装配平面：解决“这次会话该带什么脑子、哪些规则、哪些 skill、哪些子 Agent 摘要、哪些增强 provider”。
- 记忆平面：解决“把哪些事实蒸馏成长期资产，以及如何被后续会话 recall”。
- 档案查询面：解决“历史细节怎么回查”，只服务会话档案与 explainability，不把旧日志伪装成长期记忆。

Hermes Agent 的源码结论进一步验证了这个分拆方向：它把 bounded built-in memory、外部 memory provider、session search 和 delegation 隔离成不同能力面，而不是让一个 memory store 同时承担全部职责。`shanforge` 应吸收这种边界，而不是照搬其 monolithic runtime 组织方式。

### 3.2 记忆领域在六层架构中的正式落点

| 架构层 | 代码落点 | 对记忆系统的责任 | 不能做什么 |
|---|---|---|---|
| 用户界面层 | 仓外 Web 项目、外部 CLI 前台 | 承载用户交互与调试入口 | 直接操作 memory store |
| 接口 / 网关层 | `src/access/` | 接收运行请求、调试查询和未来 explainability 查询入口 | 越过应用门面直连基础设置实现 |
| 业务调度层 | `src/application/` | 组织 `prepare -> run -> distill -> persist` 会话生命周期，并通过 `MemoryDomainService` 调用记忆领域 | 直接决定 store / provider 实现细节 |
| 业务模型层 | `src/domain/memory/`、相关 assembly/archive 模型 | 定义 `RecallQuery`、`RecallBundle`、`MemoryRecord`、`SessionAssemblyManifest` 等稳定契约，并持有记忆业务逻辑 | 持有外部 SDK 或数据库驱动细节 |
| 基础能力层 | `src/runtime/ports/` 及未来实现模块 | 提供 recall、assembly、promotion、archive query 所需的检索、规则、profile、skill、推理和存储能力 | 主导记忆业务语义 |
| 基础设置层 | `src/settings/session/`、`src/settings/memory/`、`src/settings/model/`、`src/settings/composition/`、sibling `shanforge-di` | 提供 session ledger、evidence、memory、dataset、archive、provider、本地 business bindings 与装配实现 | 主导业务路由或改写领域规则 |

补充约束：

- `src/runtime/memory/assembly.py`、`provider_manager.py` 这类新增文件如果落地，仍然属于基础能力层内部模块，不是新的架构层。
- `src/settings/` 是基础设置层唯一正式代码根；`session / memory / model / skills / workspace / approval / delegation / gateway / capability_registry / hermes` 是层内实现领域。

### 3.3 记忆系统主链路

```text
外部 UI / 前台
  -> 接口 / 网关层
  -> 业务调度层
  -> 业务模型层 memory
  -> 基础能力层 recall / assembly / archive / context capability
  -> 基础设置层 Memory / Evidence / Dataset / Archive / Provider 实现
```

### 3.4 五个必须坚持的边界

- `cwd` 只决定“现场规则”，不决定“长期脑子是谁”。
- `skill` 是流程资产，只能按需装配，不进入长期事实记忆池。
- 子 Agent 结果默认先进入 `digest` 区，不直接晋升全局长期记忆。
- 会话档案回查走 archive query，不借道 `MemoryStorePort.search()`。
- built-in local memory 始终保留；external provider 只能做 augmentation，不得覆盖 evidence / memory 的主事实链。

## 4. 领域模型建模

### 4.1 现有模型继续保留

以下模型已经在代码中存在，继续作为正式核心契约：

- `SessionEvent`
- `SessionArtifact`
- `AgentSession`
- `EvidenceRecord`
- `MemoryCandidate`
- `PromotionDecision`
- `MemoryRecord`
- `RecallQuery`
- `RecallBundle`
- `DistillationResult`
- `MemoryDistillationSample`

### 4.2 新增业务装配模型

| 模型 | 建议落点 | 作用 |
|---|---|---|
| `ProfileMemoryDomain` | `src/domain/memory/assembly_models.py`（新增） | 标识当前长期记忆域，包含 `profile_id`、默认 `scope`、默认 recall policy、默认 skill 集合 |
| `ProjectRuleBundle` | `src/domain/session/assembly_models.py`（新增） | 表达当前仓库加载到的规则文件、规则来源、版本摘要 |
| `SkillDescriptor` | `src/domain/context/skill_models.py`（新增） | 只描述 skill 索引，不承载 skill 正文 |
| `SkillActivation` | `src/domain/context/skill_models.py`（新增） | 描述本会话已激活的 skill、来源和加载原因 |
| `SessionAssemblyManifest` | `src/domain/session/assembly_models.py`（新增） | 一次会话最终装配结果的读模型，记录 profile、cwd、规则、skills、recall plan、memory sources、backend bindings、默认 selected model 与实际 model invocation history |
| `SubAgentDigest` | `src/domain/session/delegation_models.py`（新增） | 子 Agent 产出摘要、责任范围、证据来源、主 Agent 吸收状态 |
| `RecallPlan` | `src/domain/memory/assembly_models.py`（新增） | 记录本轮 recall 的 scopes、预算、排序策略和过滤原因 |
| `MemoryProviderBinding` | `src/domain/memory/assembly_models.py`（新增） | 描述本轮启用的 built-in / external provider、命名空间与注入模式 |
| `SessionArchiveHit` | `src/domain/session/archive_models.py`（新增） | 历史会话检索命中项，只作为回查读模型，不进入长期记忆聚合 |

### 4.3 Working Memory 的正式定位

`working memory` 不应被建模成可持久化的 `MemoryRecord`。它属于当前 session / 当前 step 的运行时状态，应继续驻留在：

- `AgentSession.context`
- `ContextEnvelope.values`
- `ContextSegmentType.WORKING_MEMORY`

结论是：

- 持久化长期记忆只有 `episodic / declarative / procedural / reflective`
- `working memory` 是会话级运行时对象，不进入长期记忆存储

### 4.4 聚合关系

```text
AgentSession
  -> SessionEvent*
  -> SessionArtifact*
  -> SessionAssemblyManifest (1)
  -> SubAgentDigest*
  -> DistillationResult (0..1)

DistillationResult
  -> EvidenceRecord*
  -> MemoryCandidate*
  -> PromotionDecision*
  -> MemoryRecord*

SessionArchiveHit
  -> session_id
  -> matched_event_refs*
  -> summary
  -> score
```

### 4.5 生命周期规则

| 对象 | 生命周期 | 默认去向 |
|---|---|---|
| `SessionEvent` / `SessionArtifact` | 会话执行期间持续追加 | session ledger |
| `EvidenceRecord` | session 结束后保留，可重建 | evidence store |
| `MemoryCandidate` | 短期可审计资产 | dataset store + session state |
| `MemoryRecord` | 跨会话长期资产 | memory store |
| `SkillActivation` | 仅本会话有效 | assembly manifest |
| `SubAgentDigest` | 默认待主 Agent 吸收 | digest store |
| `MemoryProviderBinding` | session-start 冻结，session-end 关闭 | assembly manifest + provider manager state |
| `SessionArchiveHit` | 按查询即时生成 | archive query result |

## 5. 存储系统设计

### 5.1 存储职责拆分

| 存储 | 当前状态 | 下一步职责 |
|---|---|---|
| `Session Ledger Store` | 目前由 `AgentSession` + `SessionStore` 承接，持久化能力不足 | 负责 append-only 事件、artifact、会话摘要留档 |
| `Evidence Store` | 已有 `InMemory/JsonlEvidenceStore` | 保存事实投影，供审计、追溯和 candidate 支撑引用 |
| `Memory Store` | 已有 `InMemory/JsonlMemoryStore` | 保存 `accepted/draft/superseded` 记忆，按 `profile_id + scope + scope_key` 分区 |
| `Dataset Store` | 已有 `InMemory/JsonlMemoryDatasetStore` | 保存 `candidate -> decision -> supporting refs` 样本链 |
| `Assembly Store` | 已有 `InMemory/JsonlSessionAssemblyStore` | 保存 `SessionAssemblyManifest`，支撑“当前装配了什么”的解释与调试 |
| `Digest Store` | 已有 `InMemory/JsonlDelegationDigestStore` | 保存子 Agent 输出摘要和主 Agent 吸收决策 |
| `Session Archive Index` | 缺失 | 为历史会话建立 `session/event/artifact` 检索索引，专门服务回查 |

### 5.2 推荐的本地目录布局

`local-first` 版本建议采用按 `profile` 与 `session` 双主键拆分，而不是继续把所有记忆放在一个共享文件里：

```text
<memory_root>/
  profiles/
    <profile_id>/
      memory-records.jsonl
      memory-dataset.jsonl
      profile-config.json
      memory-provider/
        memory-provider-snapshots.jsonl
        memory-provider-turns.jsonl
        memory-provider-digests.jsonl
  sessions/
    <session_id>/
      session-events.jsonl
      evidence-records.jsonl
      assembly-manifest.json
      sub-agent-digests.jsonl
  indexes/
    session-archive.sqlite
```

### 5.3 分桶策略

| 资产 | 主分桶键 | 次分桶键 | 说明 |
|---|---|---|---|
| 长期记忆 | `profile_id` | `scope/scope_key` | 保证不同生产线、不同项目默认隔离 |
| 会话档案 | `session_id` | `event kind` | 事实源按 session 保留 |
| 样本数据 | `profile_id` | `session_id` | 训练与分析按长期脑子归档 |
| 装配读模型 | `session_id` | 无 | 专供 explainability |
| 子 Agent 摘要 | `parent_session_id` | `child_session_id` | 支撑主从协作收口 |
| 会话检索索引 | `profile_id` | `session_id` | 支撑历史回查，不替代长期记忆 |

### 5.4 检索与持久化分离

当前这条链已经从“设计要求”进入“正式实现”，主链已拆成：

- `MemoryStorePort`：负责持久化与按分区扫描；当前正式 owner 是 `scan_memory_records()`
- `RecallGovernancePolicy`：负责确定查询 scope、状态过滤与 augmentation 参与条件
- `RecallPlannerPort`：负责把 `RecallGovernanceDecision` 物化为带预算的 `RecallPlan`
- `RecallRankerPort`：负责排序、去重、pinned 优先级和 top-k 裁剪
- `SessionArchiveQueryPort`：负责在 session ledger / archive index 上做历史回查，不污染长期记忆入口
- `provider_manager`：负责把 built-in snapshot 与单个 external provider augmentation 编织到本轮装配中

这样可以避免未来把向量检索、关键词检索、规则过滤和 external augmentation 全部塞进 store。

### 5.5 清理与维护规则

长期记忆自动维护必须有明确预算，而不是停留在原则层：

- `accepted` 记录进入 recall 候选
- `draft` 记录默认不进入 recall，但保留复核价值
- `superseded` 记录保留追溯链，不参与默认 recall
- 同 `scope + title` 冲突时优先生成 `supersedes` 链，而不是直接覆盖
- 当分区达到预算上限时，优先执行 merge / supersede / decay，再考虑淘汰
- session-start snapshot 一旦生成，本轮只允许追加 durable state，不允许隐式改写已注入上下文
- external provider 的 recall block 属于 augmentation，不写回 session ledger 正文

## 6. 源代码骨架

### 6.1 当前已存在的正式骨架

| 路径 | 状态 | 责任 |
|---|---|---|
| `src/domain/memory/models.py` | 已存在 | 记忆领域核心模型 |
| `src/domain/session/models.py` | 已存在 | session / event / artifact 契约 |
| `src/domain/context/models.py` | 已存在 | 上下文段、预算和 envelope 契约 |
| `src/application/ports/domain_services.py` | 已存在 | 应用层对记忆领域的正式服务接口定义 |
| `src/application/execution/service.py` | 已存在 | `prepare -> run -> distill` 主链路 |
| `src/domain/memory/service.py` | 已存在 | recall / distill / explainability 领域实现 |
| `src/domain/memory/ports.py` | 已存在 | 记忆领域向基础能力层声明的下行接口 |
| `src/domain/memory/policy.py` | 已存在 | promotion policy 领域规则 |
| `src/runtime/context/engine.py` | 已存在 | 消费 recalled memory 编译上下文 |
| `src/runtime/ports/*.py` | 已存在 | provider、store、source、backend ports |
| `src/settings/memory/store.py` | 已存在 | memory store 实现 |
| `src/settings/memory/evidence_store.py` | 已存在 | evidence store 实现 |
| `src/settings/memory/dataset_store.py` | 已存在 | dataset store 实现 |
| `src/settings/composition/container.py` | 已存在 | 默认容器装配 |
| `src/settings/composition/component_bindings.py` | 已存在 | 记忆相关 store/provider 的本地 business bindings |

迁移说明：

- 旧的 `src/runtime/memory/runtime.py` 与 `src/runtime/memory/policy.py` 已在 2026-04-18 退役；记忆主链只保留 `src/domain/memory/service.py`、`src/domain/memory/policy.py` 与 runtime 侧的 planner/ranker/provider_manager/summarizer 支撑模块。

### 6.2 建议新增的骨架

| 路径 | 状态 | 责任 |
|---|---|---|
| `src/domain/memory/assembly_models.py` | 新增 | `ProfileMemoryDomain`、`RecallPlan`、`MemoryProviderBinding` |
| `src/domain/session/assembly_models.py` | 新增 | `ProjectRuleBundle`、`SessionAssemblyManifest` |
| `src/domain/session/delegation_models.py` | 已落地 | `SubAgentDigest` |
| `src/domain/session/archive_models.py` | 新增 | `SessionArchiveHit` |
| `src/domain/context/skill_models.py` | 新增 | `SkillDescriptor`、`SkillActivation` |
| `src/application/ports/memory_assembly.py` | 新增 | `MemoryAssemblyQueryPort` |
| `src/access/api/memory_api.py` | 新增 | 读写分离的 memory / assembly 调试与运维入口 |
| `src/runtime/memory/assembly.py` | 新增 | `profile + rules + skill + digest` 装配服务 |
| `src/runtime/memory/provider_manager.py` | 已落地 | 编排 built-in local memory 与单个 external memory provider |
| `src/runtime/memory/recall_planner.py` | 已落地 | recall plan 生成与预算裁剪 |
| `src/runtime/ports/profile_resolver.py` | 新增 | 显式入口 -> profile domain |
| `src/runtime/ports/workspace_rule_bundle.py` | 新增 | 从 `cwd` 加载项目规则摘要 |
| `src/runtime/ports/skill_catalog.py` | 新增 | 暴露 skill 索引与按需加载能力 |
| `src/domain/memory/ports.py` | 已扩展 | `MemoryProviderPort` / `MemoryProviderManagerPort` 的 consumer-owned 接口定义 |
| `src/runtime/memory/recall_ranker.py` | 已落地 | recall 结果排序与裁剪 |
| `src/domain/session/ports.py` | 已落地 | `SessionAssemblyStorePort`，承载 assembly manifest 的 durable snapshot 契约 |
| `src/runtime/ports/delegation_digest_store.py` | 新增 | 子 Agent digest 持久化 |
| `src/runtime/ports/session_archive_query.py` | 新增 | 历史会话检索与摘要回查 |
| `src/settings/memory/provider.py` | 已落地 | external memory provider 的 `none / in_memory / jsonl` 基础设置实现 |
| `src/settings/session/assembly_store.py` | 已落地 | assembly store 的 `in-memory / JSONL` 实现 |
| `src/settings/delegation/digest_store.py` | 新增 | digest store 的 `in-memory / JSONL` 实现 |
| `src/settings/session/archive_index.py` | 新增 | session archive query 的 `SQLite FTS / JSONL` 实现 |

### 6.3 与当前实现的关键对齐结论

- `ExecutionService -> SessionDomainService / MemoryDomainService -> domain ports -> stores / reasoning capability` 已经是真实主链路，不再以 `MemoryRuntime` 作为正式业务 owner。
- `project_scope_key="shanforge"` 这类静态配置已从默认容器迁出；当前默认装配已改为通过 `ProfileSourceService + RuleSourceService` 生成 `profile_id` 与 `project_scope_key`，并随 `SessionAssemblyManifest` 持久化。
- `ContextSegmentType` 已预留 `SKILL` / `EVIDENCE`，但当前上下文引擎尚未把 skill 正文和 evidence 段正式产出；详细设计应明确这部分是下一阶段补位。
- `DefaultMemoryDomainService` 当前已承接 recall / distill / promotion 主逻辑；其中 recall 已改为 `RecallGovernancePolicy -> RecallPlannerPort -> scan_memory_records() -> RecallRankerPort` 的独立协作链，不再回塞到 legacy runtime shim 或 store 查询里。
- external `MemoryProviderPort + provider_manager` 已从首轮边界推进到 durable backend/source：domain owner 定义 `MemoryProviderPort / MemoryProviderManagerPort`，runtime `DefaultMemoryProviderManager` 负责 single-provider lifecycle + sanitize fence，settings `memory_provider` family 已提供 `none / in_memory / jsonl / jsonl_vector / remote_http` 实现，`SessionAssemblyManifest` 现会冻结 `memory_provider_binding`。
- `JsonlAugmentationMemoryProvider` 会把 provider-owned snapshot / turn / digest state 落到 profile-scoped JSONL root，保证 built-in local memory 与 external augmentation 的 durable state 仍然分仓治理。
- `RemoteAugmentationMemoryProvider` 现已通过 settings-layer `http_client` 支持 `file:// + http(s)` JSON transport，并可选写回 `sync / session_end / lifecycle_apply / delegation` 事件；binding metadata 还可声明 `metadata_file`、`request_headers / bearer_token(_env|_file) / signature_secret(_env|_file) / signature_key_id / retry_status_codes / max_retries / timeout_seconds`、canonical `hmac-sha256` 签名串、`prefetch_response_validation`、`*_failure_policy` 与 `secret_catalog_file`；其中 `secret_catalog_file` 可提供 `default_signature_key_id / signature_keys / default_bearer_token_id / bearer_tokens`，把 key rotation 与 durable secret governance 留在 settings 层，而 `RemoteHttpMetadataResolver` 会把 `recall / sync / session_end / lifecycle_apply / delegation` 的 endpoint、response contract、response validation、failure policy、canonical `bearer_token*` 与 legacy alias fallback 统一收口到同一条解析路径，并投影为 `RemoteHttpRequestGovernance` 读模型供 provider 直接消费；当前 `jsonl / jsonl_vector / remote_http` 也已统一把 `query_terms / source_breakdown / result_truncated / budget_trace / rank_trace / hit_provenance / contract_trace / access_trace / writeback_trace` 回收到 preview explainability，`src/domain/memory/augmentation_diagnostics.py` 则把 provider manager、stored replay、domain preview 回读和 session/manifest 落盘统一到同一套 normalize/compact/project-stored/preview-project 路径上；其中 runtime provider manager 现已直接输出 compact canonical diagnostics，不再主动展开 legacy 顶层 alias，而读取冻结的旧 diagnostics 时仍可经 normalize 把这些 legacy 顶层键并回 trace，且 `DefaultMemoryDomainService` 不再单独维护一份 service-local `allowed_keys`。与此同时，stored replay 现还会基于 `provider_id` 推断基础 contract defaults，并基于 `memory_provider_binding.metadata.recall_endpoint_url` 恢复 access 默认值，使 `bridge_kind / provider_kind / storage_kind / retrieval_kind / response_contract / response_contract_source / endpoint_url` 不再需要继续作为 legacy 顶层输入。preview 现已完全只暴露 canonical trace-first 字段，不再输出 `legacy_aliases`。`remote_http` provider 自身则继续移除重复顶层 diagnostics，并把 transport auth、retry/timeout、secret selection、catalog source、prefetch validation 与 writeback outcome/error 摘要分别统一回收到 `access_trace / contract_trace / writeback_trace`；其中 `writeback_trace` 现会稳定暴露 `successes / response_oks / response_statuses / response_messages / response_report_ids / failure_policies / response_validation_errors`，并以 `detail_reports` 作为 canonical drill-down 字段；旧的 `reports` 只在 replay/normalize 阶段作为兼容输入，`hit_count / hit_ids / query_text_present` 这组跨 backend 命中摘要也已继续并入 `budget_trace.selected_hit_count / selected_hit_ids / query_text_present`。`apply_lifecycle()` 现还会在本地 memory store durable 更新后，按 `MemoryProviderGovernanceDecision.allow_lifecycle_writeback` 决定是否继续触发 provider-aware lifecycle writeback。
- Hermes 的 `MemoryManager + MemoryProvider` 模式可直接复用为 shanforge 的“增强 provider 插槽”，但 evidence / accepted memory 仍必须由本仓的 local-first stores 主导。

## 7. 对外服务界面

### 7.1 平台内部统一门面

正式目标是由 `MemoryDomainService` 承担应用编排层对记忆领域的统一门面：

```text
prepare_session(session, app, workflow) -> RecallBundle
recall(query) -> RecallBundle
distill_session(session) -> DistillationResult
explain_session_memory(session) -> Mapping[str, Any]
review_lifecycle(session) -> MemoryLifecycleReviewResult
load_lifecycle_queue(session, queue_filter=None) -> MemoryLifecycleQueue
reopen_lifecycle_queue(session, actor, record_ids=None, queue_filter=None, note=None) -> MemoryLifecycleQueueUpdateResult
load_lifecycle_audit(session, audit_filter=None) -> MemoryLifecycleAuditLog
update_lifecycle_queue(session, actor, review_status, record_ids=None, queue_filter=None, note=None, resolution=None) -> MemoryLifecycleQueueUpdateResult
apply_lifecycle(session, actor, record_ids=None, queue_filter=None) -> MemoryLifecycleApplyResult
```

解释：

- `prepare_session` 内部应先完成 `SessionAssemblyManifest` 解析，再执行 recall
- `recall` 保持可独立调试和测试
- `distill_session` 负责 evidence 投影、candidate 提取、promotion、sample 写入
- `explain_session_memory` 负责 explainability 读模型收口，并稳定给出 recall plan、memory provider binding、promotion reasons、recalled memory lifecycle 状态，以及 scoped records 的 `lifecycle_evaluations / lifecycle_queue_summary / lifecycle_audit_summary`；其中 audit summary 会把 `latest_entries` 固化为最新优先，并额外给出 `latest_by_record`
- `review_lifecycle` 负责返回 session scope 下的完整 lifecycle review 结果
- `load_lifecycle_queue` 负责把 review 结果投影为产品可消费的 durable queue 读模型，并给出默认 batch selection；默认只返回 `pending` 的 actionable items
- `load_lifecycle_queue` 对 actionable item 还会投影 reviewer guidance，包括 `resolution_required`、推荐 `resolution_options` 和建议 note 模板
- `reopen_lifecycle_queue` 负责把已 dismiss/applied 的 review item 恢复到 `pending`
- 当未显式给出 `record_ids` 时，`reopen_lifecycle_queue` 可按 `queue_filter` 批量恢复命中的 queue item
- `load_lifecycle_audit` 负责读取 durable 审计轨迹，回答 queue review/apply 的 actor/action/status/resolution 变化，并支持按 `queue_review_status / resolution` 过滤；当 `audit_filter.latest_per_record_only=True` 时，可直接返回每条 record 最近一次人工处理事件
- `update_lifecycle_queue` 负责持久化人工 review 状态 `pending / dismissed / applied`，不直接改写 memory record；当状态不变但 note 变化时，会落为独立 `review_note_updated` 审计动作
- `update_lifecycle_queue` 也可显式持久化 reviewer resolution taxonomy；当 queue item 被 `reopen` 回 `pending` 时，已记录 resolution 会被清空
- 当未显式给出 `record_ids` 时，`update_lifecycle_queue` 可按 `queue_filter` 批量更新命中的 queue item；这里的 filter 语义是“命中队列项全集”，与 `apply_lifecycle` 的默认选中子集不同
- `apply_lifecycle` 负责将已允许的 lifecycle decision durable 写回 memory store；当未显式给出 `record_ids` 时，可直接消费 queue filter 做批量 apply；成功 apply 后，对应 queue item 会同步标记为 `applied`；当 provider governance 允许时，还会继续通过专门的 `lifecycle_apply` 通道把结果同步给 external provider

兼容说明：

- 旧版单独 `memory_system.py` 口径已经废弃。
- 正式架构 owner 以 `src/application/ports/domain_services.py` 和 `src/domain/memory/ports.py` 为准。

### 7.2 可解释性查询门面

首轮已落地的读模型门面 `MemoryAssemblyQueryPort`：

```text
get_session(session_id) -> AgentSession | None
search_session_archive(query, profile_id, limit) -> tuple[SessionArchiveHit, ...]
load_session_slice(session_id, cursor, limit) -> SessionTranscriptSlice
explain_session_assembly(session_id) -> SessionAssemblyManifest
```

目的：

- 让 CLI / HTTP / 测试可直接看见“当前装配了什么”
- 将“路由错了、规则错了、skill 装错了、记忆召回错了、历史回查错了”五类问题区分开

当前落地说明：

- 默认容器已接线 `MemoryAPI -> SessionInspectionService -> SessionSearchQueryAdapter -> SessionSearchService`
- 默认容器现还额外接线 `MemoryInspectionService -> DefaultMemoryDomainService.preview_recall()`，把 recall 预览作为独立治理接口暴露给 `MemoryAPI`
- `prepare_session` 会把 assembly snapshot 写入 `AgentSession.context["assembly_manifest"]`，并同步保存到专门 `SessionAssemblyStorePort`
- `SubAgentDigest` 与 `DelegationDigestStorePort` 已落地，`prepare_session` 会把 child digests 合并进 `SessionAssemblyManifest`
- `ExecutionService` 现会在 session 打开后注入稳定的 `session_context_defaults`，把本轮 profile/backend/model 默认绑定冻结进 session context
- `CapabilityExecutor` 现会把每个 prompt step 的实际 `provider/model` 调用记录回 `SessionAssemblyManifest.model_bindings`
- `SessionAssemblyManifest` 现已显式暴露 `backend_bindings`、`selected_model` 与 `model_bindings`，用于区分“装配默认选择”“这些绑定来自哪个 profile/backend/provider 来源”以及“执行时实际使用”；`selected_model` 继续保留默认装配元数据，不再被 step 级真实调用覆盖

### 7.3 Access 层推荐服务

`src/access/api/memory_api.py` 已提供首轮 `MemoryAPI`，用于调试、诊断与治理，而不是替代 `RuntimeAPI`：

```text
get_session(session_id) -> AgentSession | None
search_session_archive(query, profile_id, limit) -> tuple[SessionArchiveHit, ...]
load_session_slice(session_id, cursor, limit) -> SessionTranscriptSlice
explain_session_assembly(session_id) -> SessionAssemblyManifest
preview_recall(session_id, limit=None) -> RecallPreview
```

其中：

- `search_session_archive` 只回查历史，不把旧日志晋升为长期记忆
- `load_session_slice` 只回放 archive facts，不改变长期记忆
- `preview_recall` 已作为独立治理接口落到 `MemoryInspectionService`，通过 `MemoryAPI` 聚合暴露，但没有写回 `SessionInspectionService`
- 当前 `preview_recall` 会显式返回 `scope_breakdowns`、`record_rankings` 与 `augmentation_preview`，用来回答 recall budget 如何分配、哪些记录因 overflow 被淘汰、external augmentation provenance 从哪里来
- 后续如果补 digest 吸收和 backend 列表，也应继续沿独立治理接口扩展，不与当前 inspection facade 混写

## 8. 需要接入的基础设施能力界面定义

### 8.1 装配与路由接口

```text
ProfileResolverPort.resolve(profile_hint, cwd) -> ProfileMemoryDomain
WorkspaceRuleBundlePort.load(cwd) -> ProjectRuleBundle
SkillCatalogPort.list_index(profile_id) -> tuple[SkillDescriptor, ...]
SkillCatalogPort.load_body(skill_id) -> str
```

要求：

- `ProfileResolverPort` 只能基于显式入口、配置或用户选择路由，不得偷偷由 `cwd` 猜 profile
- `WorkspaceRuleBundlePort` 只读取项目规则文件，不回写长期记忆
- `SkillCatalogPort` 启动阶段只暴露索引，正文按需加载

### 8.2 Recall 与治理接口

```text
RecallGovernancePolicy.decide(session, app_id, workflow_id, profile_id, project_scope_key, provider_decision, default_limit=None) -> RecallGovernanceDecision
RecallPlannerPort.plan(decision) -> RecallPlan
RecallRankerPort.rank(records, plan) -> tuple[MemoryRecord, ...]
MemoryPromotionPolicy.evaluate(candidate) -> (status, reason)
```

要求：

- `RecallGovernancePolicy` 决定本轮查哪些 `scope`、接受哪些 `status`，以及 external augmentation 能否参与
- `RecallPlannerPort` 只负责把领域决策转成预算化且带显式排序指令的 `RecallPlan`
- `RecallRankerPort` 只负责执行 `RecallPlan` 中的 bucket/overflow 排序与 top-k 收口
- `MemoryPromotionPolicy` 继续独立，不进入 store
- 若启用 external memory provider，其 augmentation 结果只能作为 ranker 的额外输入，不得绕过 built-in policy 直接注入 accepted memory

### 8.3 存储接口

```text
MemoryStorePort.save(record) -> None
MemoryStorePort.list_by_scope(scope, scope_key) -> tuple[MemoryRecord, ...]
MemoryStorePort.search(query) -> tuple[MemoryRecord, ...]

EvidenceStorePort.save_evidence(record) -> None
EvidenceStorePort.list_by_session(session_id) -> tuple[EvidenceRecord, ...]

MemoryDatasetStorePort.save_entry(entry) -> None
MemoryDatasetStorePort.list_by_session(session_id) -> tuple[MemoryDistillationSample, ...]

SessionAssemblyStorePort.save(manifest) -> None
SessionAssemblyStorePort.get(session_id) -> SessionAssemblyManifest | None

DelegationDigestStorePort.save(digest) -> None
DelegationDigestStorePort.list_by_session(session_id) -> tuple[SubAgentDigest, ...]

SessionArchiveQueryPort.search_session_archive(query, profile_id, limit) -> tuple[SessionArchiveHit, ...]
SessionArchiveQueryPort.get_session_summary(session_id) -> str | None
SessionTranscriptSlicePort.load_session_slice(session_id, cursor, limit) -> SessionTranscriptSlice
```

### 8.4 模型与技能提炼接口

```text
MemorySummarizerPort.summarize_evidence(session, evidence_records) -> SummaryResult
MemorySummarizerPort.extract_candidates(session, evidence_records, summary) -> CandidateDrafts
```

要求：

- summarizer 只能生成候选草案
- `kind / scope / confidence` 继续由运行时控制
- procedural memory 可产生 skill 候选，但 skill 发布必须走独立治理流，不直接把 memory record 当正式 skill

### 8.5 记忆增强提供方接口

Hermes Agent 最值得吸收的是“内建 bounded memory 永远保留，external provider 按需增强且同时只激活一个”的接口组织方式。落到 shanforge，建议在 runtime ports 中新增：

```text
MemoryProviderPort.initialize(binding, session_id) -> None
MemoryProviderPort.prefetch(query, session_id) -> str
MemoryProviderPort.sync_turn(session_id, latest_events) -> None
MemoryProviderPort.on_session_end(session_id, distillation_result) -> None
MemoryProviderPort.on_delegation(digest) -> None
```

要求：

- built-in local memory store 永远存在，external provider 只是 augmentation
- 同时只允许 1 个 external provider 激活，避免 schema 膨胀和解释困难
- provider 只能写自己的后端，不得改写本地 evidence / memory / dataset 真相源
- provider 返回的 recall block 必须带显式 context fence / system note，并在注入前做 sanitize，避免被误当作新 user input
- child agent 默认不持有 shared provider write capability，只回传 `SubAgentDigest`

## 9. 业务评估与改进方案

### 9.1 主 Agent 评估结论

从业务视角看，当前 `v1` 设计已经把“记忆不是日志、记忆不能覆盖事实、recall / promotion 必须解耦”这三件最关键的事做对了。  
真正的缺口不在 `distill_session()` 算法，而在会话装配治理、历史回查治理和增强 provider 治理：

- 还没有把 `profile`、项目规则、skills、子 Agent digest 正式建模成装配对象
- 还没有把“当前装配了什么”做成独立读模型
- 还没有把 recall 规划从静态 `APP + PROJECT` 查询扩成可配置策略
- 还存在静态 `project_scope_key` 这类会限制多 profile / 多项目落地的硬编码
- 还没有把历史会话回查从长期记忆入口中拆出来，`MEM-BIZ-006` 仍缺一条独立查询链
- 还没有建立 built-in + single external provider 的增强接口边界，后续若直接接云 memory SDK 会很快污染主链路

换句话说，现有实现已经具备“记忆核心”，但还没有形成“业务可控的记忆系统产品”。

### 9.2 优先级最高的改进项

1. 先补 `SessionAssemblyManifest`，把 `profile / cwd / rules / skills / recall sources / child digests / provider bindings` 变成一等对象。
2. 先补 `ProfileResolverPort` 与 `WorkspaceRuleBundlePort`，切断 `cwd` 与长期脑路由的耦合。
3. 先补 `SkillCatalogPort` 与 `SkillActivation`，把“skill 索引先行、正文按需加载”固化到运行时。
4. `SessionAssemblyStorePort`、`DelegationDigestStorePort`、`MemoryAssemblyQueryPort` 与 `SessionArchiveQueryPort` 已进入首轮实现；下一轮继续补 provider bindings 治理。
5. 先补 `MemoryProviderPort + provider_manager`，明确 built-in local memory 与单个 external provider 的职责边界。
6. 先把 `project_scope_key` 从硬编码改成装配输入，避免后续多项目和多 profile 迁移返工。

### 9.3 应延后处理的改进项

以下能力重要，但不应抢在装配治理之前：

- 向量检索或远程 memory provider
- 更复杂的 LLM candidate 生成策略
- 训练专用 memory model
- 管理后台 UI
- vendor-specific memory SDK 全量接入

原因很直接：如果装配分层和解释模型没立住，后续引入更强检索只会更难定位错误来源。

### 9.4 推荐实施顺序

| 阶段 | 目标 | 主要产出 |
|---|---|---|
| `P0` | 建立业务可控的装配治理 | `SessionAssemblyManifest`、`ProfileResolverPort`、`WorkspaceRuleBundlePort`、`SkillCatalogPort` |
| `P1` | 建立 explainability、archive query 与主从协作闭环 | `MemoryAssemblyQueryPort`、`SessionAssemblyStorePort`、`DelegationDigestStorePort`、`SessionArchiveQueryPort` |
| `P2` | 建立 built-in + external provider augmentation 边界 | `MemoryProviderPort`、`provider_manager`、`provider bindings`、durable `memory_provider:jsonl / jsonl_vector / remote_http` |
| `P3` | 扩 recall 规划与检索能力 | `RecallPlannerPort`、`RecallRankerPort`、向量/远程检索适配器 |
| `P4` | 扩长期治理与训练化 | retention policy、dataset 审核流、训练样本治理 |

当前实现状态：

- `P2` 已落地，并已补到 durable `jsonl / jsonl_vector / remote_http`；其中 `remote_http` 已支持真实 `HTTP/file` transport 与可选远端写回
- `P3` 的 `RecallPlannerPort / RecallRankerPort`、`preview_recall` 与 provider provenance explainability 已落地；当前剩余的是跨 backend 的统一 recall diagnostics，以及 `remote_http` 的 response schema contract、secret rotation audit 与统一 durable secret governance provider

## 10. Hermes-Agent 可复用能力

本轮通过子 agent 精读 `/Users/uroborus/AiProject/hermes-agent`，确认最值得吸收的是结构而不是供应商适配器：

| 类别 | Hermes 精华 | shanforge 采用方式 | 结论 |
|---|---|---|---|
| 直接复用 | `MemoryProvider` 抽象 + `MemoryManager` 单点编排 | 落为 `MemoryProviderPort + provider_manager` | 直接吸收 |
| 直接复用 | built-in bounded memory 始终保留、external provider 同时只启用一个 | built-in local stores 始终保留，external provider 只做 augmentation | 直接吸收 |
| 直接复用 | session archive / session search 与长期 memory 分离 | 增加 `SessionArchiveQueryPort`，不经 `MemoryStorePort.search()` | 直接吸收 |
| 直接复用 | 子 Agent 默认禁止写共享 memory，只回传摘要 | `SubAgentDigest + child-isolated memory policy` | 直接吸收 |
| 适配复用 | Holographic 的 `SQLite + FTS5 + 分桶 + trust` 检索结构 | 作为 `session archive index` / 本地 recall index 的优先实现蓝本 | 适配吸收 |
| 适配复用 | frozen snapshot + live durable write | 落为 `AssemblySnapshotPolicy`，保证 session-start 注入稳定 | 适配吸收 |
| 适配复用 | skill 目录化资产（`SKILL.md + references/templates/scripts/assets`） | 作为 `SkillCatalogPort` 背后的 skill package 组织方式 | 适配吸收 |
| 不建议直搬 | Honcho / Hindsight / Mem0 / OpenViking / ByteRover / Supermemory 等 vendor SDK | 只保留统一 port，不把第三方语义写进主流程 | 不直接复用 |
| 不建议直搬 | monolithic `run_agent.py` 把 prompt、tools、memory、providers 全绑在一个 runtime | 继续坚持 shanforge 的单向分层领域架构 | 不直接复用 |

主 Agent 的业务判断是：Hermes 的价值在于证明“bounded local memory + optional external augmentation + archive search + delegation isolation”这套组合是可运行的；而 shanforge 的优势应当体现在把这套组合拆成更可审计、更可测试的正式分层接口。

## 11. 归档说明

本次归档形成的正式事实是：

- 记忆系统的业务驱动详细设计主文档已经建立
- 业务需求与现有 `domain/memory` / `MemoryDomainService` / `ContextEngine` / `storage` 骨架已完成对齐
- 已吸收 Hermes Agent 的 `provider manager / bounded local memory / archive search / delegation isolation` 设计精华
- 下一轮实现不应直接继续堆 recall 算法，而应优先补 `profile/rules/skill/digest/provider/archive` 装配治理与可解释性

## 12. 版本记录

| 版本 | 日期 | 变更内容 |
|---|---|---|
| `v0.1` | 2026-04-15 | 基于 `memory-system-business-requirements.md`、现有记忆设计与代码骨架，新增业务驱动的记忆系统详细设计方案 |
| `v0.2` | 2026-04-15 | 吸收 `hermes-agent` 记忆系统设计精华，补充 provider manager、archive query、snapshot policy、可复用能力与主 Agent 业务改进方案 |
