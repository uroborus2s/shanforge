# 记忆领域接口视图

**项目名称：** 山海工枢 / shanforge  
**文档状态：** `v2` 接口基线  
**负责人：** 仓库维护者  
**主要读者：** 架构 | 平台开发 | 测试 | 适配器维护者  
**上游输入：** 记忆运行时设计 | 记忆系统详细设计方案  
**下游输出：** 代码实现 | 契约测试  
**关联 ID：** `REQ-006`, `API-006`, `API-007`, `MOD-007`  
**最后更新：** 2026-04-15

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
```

语义：

- 支持独立调试、测试和网关查询
- 只暴露 recall 读能力，不暴露领域内部编排步骤

代码位置：

- `src/access/ports/application_use_cases.py`

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
distill_session(session) -> DistillationResult
explain_session_memory(session) -> Mapping[str, Any]
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
- `explain_session_memory`
  - 负责解释本轮记忆装配与来源

代码位置：

- `src/application/ports/domain_services.py`

## 4. 业务模型层下行接口

`memory` 领域向基础能力层声明的接口如下：

### `MemoryRecordRepositoryPort`

```text
save_memory_record(record) -> None
query_memory_records(query) -> tuple[MemoryRecord, ...]
```

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

代码位置：

- `src/domain/memory/ports.py`

## 5. 建议新增的读模型与档案查询界面

为满足 `MEM-BIZ-006` 和 `MEM-BIZ-008`，建议在统一门面旁边补两组只读接口：

### `MemoryAssemblyQueryPort`

```text
explain_session_assembly(session_id) -> SessionAssemblyManifest
list_sub_agent_digests(session_id) -> tuple[SubAgentDigest, ...]
```

### `SessionArchiveQueryPort`

```text
search(query, profile_id, limit) -> tuple[SessionArchiveHit, ...]
get_session_summary(session_id) -> str | None
```

语义：

- `MemoryAssemblyQueryPort` 负责回答“当前装配了什么”
- `SessionArchiveQueryPort` 负责回答“以前发生过什么”
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
- `diagnostics` 必须包含命中数量、过滤原因和预算信息

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

```text
initialize(binding, session_id) -> None
prefetch(query, session_id) -> str
sync_turn(session_id, latest_events) -> None
on_session_end(session_id, distillation_result) -> None
on_delegation(digest) -> None
```

约束：

- built-in local memory store 永远存在，external provider 只是 augmentation
- 同时只允许 1 个 external provider 激活，避免 schema 膨胀与可解释性退化
- provider 返回的 recall block 只能作为附加上下文，不得绕过 promotion / evidence 真相源
- provider 返回的 recall block 必须带显式 context fence / system note，并在注入前做 sanitize
- child agent 默认不持有 shared provider write capability

## 10. 外部适配器可见数据

对外 adapter 可稳定读取：

- `AgentSession.recalled_memories`
- `AgentSession.memory_candidates`
