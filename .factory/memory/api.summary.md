# API 摘要

- 更新时间：2026-04-15 00:10:00
- 当前版本线：`v2` / `0.2.0.dev0`
- 摘要焦点：记忆系统独立化后的上下文与状态契约

## 核心结论

- `API-006` 被明确为 `Context Package & Recall Contract`，`Context Engine` 只能消费 `RecallBundle`，不能绕过记忆运行时直接拼长期记忆。
- `API-007` 被明确为 `Session / Event / Memory Ledger Contract`，event 与 evidence 是第一事实源，memory record 是带来源 refs 的派生资产。
- recall 与 promotion 正式解耦；命中 recall 不等于晋升长期记忆。
- 长期记忆写入必须带 evidence refs 和 promotion decision，缺失证据时必须结构化拒绝。
- 对外实现界面已经收口为 `prepare_session(session, app_id, workflow_id)`、`distill_session(session)`、`recall(query)`，并由 `AgentSession.recalled_memories / memory_candidates / promotion_decisions` 提供 adapter 可观察状态。
- 业务驱动详细设计新增了 explainability 读模型口径：建议补 `MemoryAssemblyQueryPort.explain_session_assembly(session_id)`，把 `profile / cwd / project rules / skills / memory sources / child digests` 暴露为一等查询对象。
- 新增 archive query 口径：建议补 `SessionArchiveQueryPort.search(query, profile_id, limit)`，把历史会话回查从长期记忆检索中剥离出来。
- 样本沉淀界面已补为 `MemoryDatasetStorePort`；首版默认保留 `MemorySummarizerPort` 但允许用 `null summarizer` 运行，不阻塞 deterministic gate。
- promotion gate 已补为独立 `MemoryPromotionPolicy`；当设置显式给出 summarizer provider/model 时，容器可接入 `LLMMemorySummarizer`。
- `LLMMemorySummarizer` 当前 schema 已收口为：summary 阶段读取 `summary`，candidate 阶段必须返回 `title/body`，而 `kind/scope/confidence` 由运行时配置掌控。
- `MemoryPromotionPolicy` 已支持从 settings / env 注入；repeated distill 的写入链路已具备幂等更新约束。
- 下一阶段建议新增的基础设施端口包括：`ProfileResolverPort`、`WorkspaceRuleBundlePort`、`SkillCatalogPort`、`RecallPlannerPort`、`RecallRankerPort`、`SessionAssemblyStorePort`、`DelegationDigestStorePort`。
- 吸收 Hermes Agent 后，下一阶段建议新增的基础设施端口再扩为：`SessionArchiveQueryPort`、`MemoryProviderPort` 与 `provider_manager`。
- external memory provider 的推荐边界已经明确：built-in local store 永远保留，同时最多只激活 1 个 external provider，且其结果只作为 augmentation。
- 分层接口口径已收口为：
  - access 应用用例接口：`MemoryInspectionUseCase`、`SessionInspectionUseCase`
  - application 领域服务接口：`MemoryDomainService`
  - domain 下行能力接口：`MemoryRecordRepositoryPort`、`EvidenceRepositoryPort`、`MemoryDatasetRepositoryPort`
  - runtime provider 接口：`StructuredStoreProviderPort`、`SearchIndexProviderPort`、`VectorIndexProviderPort`、`RuleSourceProviderPort`、`ProfileSourceProviderPort`
- 下一轮需要正式化的治理与通道端口包括：`ApprovalPolicyPort`、`SandboxPolicyPort`、`DelegationTransportPort`、`EventLogPort`、`ArtifactBlobStorePort` 和 `GatewayPort`。
