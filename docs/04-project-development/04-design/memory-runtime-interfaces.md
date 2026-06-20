# 记忆领域接口视图

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

### `MemorySkillCatalogPort`

```text
list_skill_index(app_id, workflow_id) -> tuple[Mapping[str, Any], ...]
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
SkillSourceProviderPort
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
