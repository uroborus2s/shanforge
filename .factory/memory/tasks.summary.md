# 任务摘要

- 当前阶段：`IMPLEMENTATION`
- 当前焦点：在完成 `src/runtime/` 支撑能力包收口、`src/settings/` 骨架清单化、`TASK-016` explainability 投影增强、Hermes-backed governance adapter 契约测试、durable `memory_provider:jsonl / jsonl_vector / remote_http`、recall planner/ranker 拆分，以及 `preview_recall` 的 budget/ranking/provenance explainability 之后，开始按 `memory-governance-design.md` 与 `memory-governance-implementation-plan.md` 收口记忆治理 owner

## 进行中

- `MG-WP-001`：记忆治理模型显式化
  - 当前已完成：`src/domain/memory/governance.py` 已落地 `RecallGovernancePolicy / MemoryProviderGovernancePolicy / MemoryLifecyclePolicy` 与对应 decision 模型；`DefaultMemoryDomainService` 现会先生成 recall/provider 领域决策，再分别驱动 `RecallPlannerPort` 与 provider manager；`DefaultRecallPlanner` 已改成只把 `RecallGovernanceDecision` 物化成带预算的 `RecallPlan`
- `MG-WP-002 / MG-WP-003`：Recall / Provider 治理继续收口
  - 当前已完成：`RecallPlan` 现已冻结 `within_scope_order / overflow_order / overflow_fill_enabled` 这组显式排序指令，`DefaultRecallRanker` 与 `DefaultMemoryDomainService.preview_recall()` 已按 plan 执行同一套 bucket/overflow 顺序；`MemoryProviderManagerPort` 与 `DefaultMemoryProviderManager` 现已直接消费 `MemoryProviderGovernanceDecision`，manager 本身不再持有 writable / delegation gate
  - 当前缺口：继续把 preview explainability 里的排序原因命名、以及 manager diagnostics 中仍残留的 provider-local 策略痕迹进一步收口到更纯的执行语义
- `MG-WP-004`：Lifecycle Governance 补齐
  - 当前已完成：`MemoryLifecyclePolicy` 现已补齐最小正式状态机、conflict supersede、forced manual override 与 metadata-driven decay forget；`DefaultMemoryDomainService.explain_session_memory()` 也已开始输出 scoped `lifecycle_evaluations` 与 `lifecycle_queue_summary`，能回答 memory 为什么 retained / superseded / forgotten；同时 `review_lifecycle / load_lifecycle_queue / apply_lifecycle` 已通过 `MemoryGovernanceService + MemoryAPI` 暴露成最小 review queue / batch apply 闭环
  - 当前已继续推进：`apply_lifecycle()` 现已按 `MemoryProviderGovernanceDecision.allow_lifecycle_writeback` 触发专门的 `lifecycle_apply` provider 通道，并把刷新后的 diagnostics / assembly manifest durable 保存回 session ledger
  - 当前已继续推进：lifecycle review queue 现已从 explainability 投影升级为 durable queue object；新增 `MemoryLifecycleQueueRepositoryPort` 与 `update_lifecycle_queue(...)`，queue entry 正式持久化 `pending / dismissed / applied` review state，`apply_lifecycle()` 成功后会同步把对应 entry 标记为 `applied`
  - 当前已继续推进：lifecycle review/apply 现已新增独立 audit trail；`MemoryLifecycleAuditRepositoryPort`、`load_lifecycle_audit(...)` 与 `lifecycle_audit_summary` 已落地，能回读 `review_status_updated / lifecycle_applied` 的 actor/action/status 历史
  - 当前已继续推进：显式 review workflow 已开始成形；`reopen_lifecycle_queue(...)` 已落地，且同状态 note update 现会被收口为独立 `review_note_updated` 审计动作，不再混入 status update
  - 当前已继续推进：queue 运维已开始支持 `queue_filter` 驱动的批量 review；`update_lifecycle_queue(...)` 与 `reopen_lifecycle_queue(...)` 都可直接按 filter 命中 queue item 全集做 `dismiss / reopen`，不再只接受显式 `record_ids`
  - 当前已继续推进：review workflow 现已补 reviewer resolution taxonomy；`update_lifecycle_queue(..., resolution=...)` 可持久化人工结论，`reopen_lifecycle_queue(...)` 回到 `pending` 时会清空 resolution，queue/audit summary 也开始稳定投影 `resolution_counts`
  - 当前已继续推进：audit read model 已开始面向 reviewer 收口；`MemoryLifecycleAuditFilter.latest_per_record_only` 已落地，`lifecycle_audit_summary.latest_entries` 改成真正的最新优先，同时新增 `latest_by_record`
  - 当前已继续推进：queue projection 已开始直接给 reviewer guidance；`MemoryLifecycleQueueItem` 现会投影 `resolution_required`、推荐 `resolution_options` 与建议 note 模板
  - 当前缺口：仍未引入更完整的人工复核流程与专门的审核运维能力
- `MG-WP-005`：记忆治理专项回归与 explainability 校验
  - 当前已完成：新增 `tests/test_memory_governance_regression.py`，将 `TC-013 ~ TC-016` 收口为独立治理回归入口；`TC-015` 对应的最小 lifecycle 事实现已补到 `MemoryStatus.FORGOTTEN` 与默认状态机，`explain_session_memory()` 也已稳定投影 `promotion_reasons / promotion_decisions / recalled_memory_statuses / memory_provider_binding / recall_plan / lifecycle_queue_summary`
  - 当前已继续推进：provider-aware lifecycle writeback 的领域级、执行级与容器级回归已补齐，`preview_recall().augmentation_preview.diagnostics.writeback_trace.detail_reports.lifecycle_apply` 现可稳定回读；queue review state 的 durable JSONL / container persistence 回归也已补齐；audit trail 的 JSONL / access-application / container persistence 回归也已补齐；显式 `reopen / review_note_updated / review_resolution` 语义也已纳入专项回归
  - 当前缺口：后续主要剩更完整的人工审核流与跨 provider 的更细粒度回放断言

- `TASK-017`：基础能力层具体函数实现阶段
  - 当前已完成：`file_access`、`skills`、`session_search` 的本地最小可用行为，`web_access`、`terminal`、`browser` 的首轮 local bridge 与治理接线，以及 `profile_source`、`rule_source`、`clock_identity` 的正式实现和 runtime-to-domain 适配
  - 当前缺口：补强 `web / terminal / browser` 的治理细节、provider profile 化与更真实 backend
- `TASK-016`：Session Search 与装配解释查询框架
  - 当前已完成：`SessionArchiveHit` / `SessionTranscriptSlice` / `SessionAssemblyManifest` / `SubAgentDigest` 已形成正式读模型；`SessionArchiveQueryPort`、`SessionTranscriptSlicePort`、`SessionAssemblyQueryPort`、`MemoryAssemblyQueryPort`、`SessionAssemblyStorePort`、`DelegationDigestStorePort`、`SessionInspectionService`、`MemoryAPI` 与 `SessionSearchQueryAdapter` 已接线；`prepare_session` 现在会把 assembly snapshot 同时写入 session context 与专门 `SessionAssemblyStorePort`；`SessionAssemblyManifest` 现已暴露 `selected_model / model_bindings / backend_bindings`，并能区分默认装配选择与 step 级实际模型调用历史；`RecallPlannerPort / RecallRankerPort` 已落地，recall 主链现已改为 `RecallGovernancePolicy -> plan -> scan -> rank`；`preview_recall` 现已通过独立 `MemoryInspectionService` 落地，并由 `MemoryAPI` 聚合暴露；`RecallPreview` 现已显式给出 `scope_breakdowns / record_rankings / augmentation_preview`
  - 当前已完成：`preview_recall` 的 augmentation diagnostics 已统一补到 `jsonl / jsonl_vector / remote_http`，当前可稳定回读 `query_terms / source_breakdown / result_truncated / budget_trace / rank_trace / hit_provenance / contract_trace / access_trace / writeback_trace`；`DefaultMemoryProviderManager` 现已在 runtime 输出侧直接使用 compact canonical diagnostics，而 `DefaultMemoryDomainService` 仍会在读取冻结的 session/manifest augmentation diagnostics 时复用同一套 trace-first normalizer，并把落盘 diagnostics 压成 compact trace-first 口径；本轮进一步把 stored replay 的 legacy 输入过滤也收口到 `project_stored_augmentation_diagnostics()`，不再在 service 内维护单独 `allowed_keys`，并开始基于 `provider_id` 推断默认 contract metadata、基于 `memory_provider_binding.metadata.recall_endpoint_url` 恢复 access 默认值，使 `bridge_kind / provider_kind / storage_kind / retrieval_kind / response_contract / response_contract_source / endpoint_url` 不再需要继续作为 replay 顶层输入；preview diagnostics 继续保持 canonical trace-first 字段，不再输出 `legacy_aliases`；`signature/bearer selection`、`retry/timeout`、`secret catalog source`、prefetch `response_validation_error` 与 writeback `successes / response_oks / response_statuses / response_messages / response_report_ids / failure_policies / response_validation_errors` 摘要继续并回 `access_trace / contract_trace / writeback_trace`，同时把 canonical drill-down 字段正式定为 `detail_reports`，旧的 `reports` 仅作为 replay/normalize 输入兼容，并把 `hit_count / hit_ids / query_text_present` 进一步并入 `budget_trace.selected_hit_count / selected_hit_ids / query_text_present`
  - 当前缺口：继续减少 legacy 输入兼容面，优先评估 `writeback_reports` 这批 replay alias 是否也能逐步下沉到 trace 默认值或更稳定的写回摘要
- `TASK-020`：外部 DI 技术库接入与容器收敛
  - 当前已完成：`shanforge-di` 依赖接入、`component_bindings.py` 业务绑定、本地 thin container、composition 回归测试、`workspace/file/git/shell/web/browser` 首轮 local bridge 接线、settings layer catalog 与 `embedding/http/blob/search/vector` 骨架入口、workspace profile/backend/provider catalogs 及其对默认容器的 provider/backend 选择接线、access 层协议 owner 与本地 CLI launcher 的边界收口、`capability_registry / approval_policy / delegation_transport` 的 Hermes-backed adapter 契约测试与 assembly explainability 投影、settings/composition 的 provider binding manager，以及 external `memory_provider` family 的首轮装配治理；`memory_provider:jsonl / jsonl_vector / remote_http` 现已作为 external backend/source 接入默认容器，其中 `remote_http` 已支持真实 `HTTP/file` 读桥、`metadata_file` durable source、签名类 auth、retry/timeout 治理、`prefetch_response_validation`、canonical 签名串、`secret_catalog_file` 驱动的 key rotation、内建 `remote_memory_prefetch_v1 / remote_memory_writeback_ack_v1` response contract、secret selection-source audit，以及稳定的 `writeback_reports` 成功/失败读模型；上一轮已把 durable secret 选择逻辑抽成 `src/settings/workspace/secret_catalog.py` 的 `LocalSecretCatalogProvider` 并注册为 `secret_catalog` family，本轮又把 `recall/sync/session_end/delegation` 的 endpoint、request_options、response_contract、response_validation_mode、failure_policy 与 legacy alias fallback 统一抽成 `src/settings/memory/remote_http_metadata.py` 的 `RemoteHttpRequestGovernance`，并把 `query_terms / source_breakdown / result_truncated / budget_trace / rank_trace / hit_provenance / contract_trace / access_trace / writeback_trace` 进一步对齐到 `jsonl / jsonl_vector / remote_http`；与此同时，`DefaultMemoryProviderManager` 与 `DefaultMemoryDomainService` 现会共用一套 augmentation diagnostics normalizer，并把 session/context 与 manifest diagnostics 落盘压成 compact trace-first 口径，`remote_http` provider 自身开始去掉重复顶层 diagnostics
  - 当前缺口：继续减少 recall 读取与 normalize 阶段仍保留的 legacy 顶层诊断重复，并把 provider-specific 治理信息继续压进统一 trace

## 已完成里程碑

- `M2`：平台主闭环、基础能力骨架和 `file / skills / session_search` 首轮可用实现已稳定
- `M3`：行动平面首轮实现已可运行，`web / terminal / browser / session_search` 均已接上最小可用 bridge，并通过回归测试

## 下一顺位

- 优先考虑 lifecycle review queue 的人工审核闭环：把当前已完成的 durable queue/audit/update/apply/provider-writeback 语义继续接到更完整的 review 操作面与审计模型
- 优先补 `TASK-020` 后续治理项：在现有 `profiles.json + backend-bindings.json + provider-bindings.json + memory_provider:jsonl / jsonl_vector / remote_http + preview_recall` 基础上，继续把 normalize/backfill 阶段仍保留的 legacy 顶层键压缩到最小集合
- 紧接补 `TASK-016` 后续项：在现有 `scope_breakdowns / record_rankings / augmentation_preview` 之上，继续减少仍散落在 top-level 或 report-only 的 provider-specific explainability
- 完成后再进入 promotion policy、dataset 筛选和真实 summarizer/provider 的进一步治理
