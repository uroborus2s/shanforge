# 项目压缩运行卡

- 生成时间：2026-04-21 00:00:00
- 负责人：Codex
- 项目：shanforge
- 当前阶段：IMPLEMENTATION
- 当前模式：cli_direct
- 技术画像：抽象 Agent 平台规划画像
- 技术栈：Python 3.14+ / uv / Markdown docs / .factory memory / typed contracts / settings-layer composition
- 活跃工作项：3
- 阻塞项：0
- 开放风险：0
- 最近交接包：无
- 最近快照：memory governance 已继续从“可审核 queue”推进到“可解释 reviewer resolution + 可直接消费的 audit/queue read model”。`update_lifecycle_queue(..., resolution=...)` 现可显式持久化人工 review resolution，`reopen_lifecycle_queue(...)` 回到 `pending` 时会清空 resolution；`load_lifecycle_audit(...)` 已支持按 `queue_review_status / resolution` 过滤，并新增 `latest_per_record_only` 视图；`lifecycle_audit_summary.latest_entries` 也已改成真正的最新优先，同时新增 `latest_by_record`。同一轮里，`MemoryLifecycleQueueItem` 还开始直接投影 `resolution_required`、推荐 `resolution_options` 和建议 note 模板，让 reviewer 面不必自己维护 conflict/decay 文案。此前发现的 settings 层 durable store 缺口也已补齐：`JsonlMemoryLifecycleQueueStore` 与 `JsonlMemoryLifecycleAuditStore` 现在都能完整 round-trip `review_resolution / resolution`，跨 container reopen 后 resolution 会被正确清空。相关专项回归 `20 passed`。
- 备注：Hermes-inspired abstract agent platform

## AI 最小读取顺序

1. 先读本文件 `/.factory/memory/runtime-brief.md`
2. 再读 `/.factory/memory/role-charter.project.md`
3. 再读 `/.factory/memory/doc-map.md`
4. 再读 `/.factory/project.json`、`/.factory/memory/project-index.md`、`/.factory/memory/current-state.md`
5. 再读 `/.factory/memory/motivation-state.md`、`/.factory/memory/autonomy-rules.md`、`/.factory/memory/evolution-baseline.md`
6. 再读当前阶段相关 summary；禁止默认直读阶段 `docs/`
7. 只有当 summary 不足以支撑当前任务时，才允许按 `doc-map.md` 单文件回源正式文档

## 当前阶段优先摘要

- `.factory/memory/traceability.summary.md`
- `.factory/memory/graph/traceability.json`

## 当前焦点

- `v2` 被定义为全新的抽象 Agent 平台，不再继承旧版本需求叙事。
- Hermes 核心能力：Agent 主循环、Capability Registry、Session / Memory、Context Engine、Delegation、Gateway。
- 业务目标：通过 Business Agent App、Workflow DSL、ModelPolicy 和 Capability Registry 快速装配业务流。
- 大模型解耦：模型交互统一通过 LLM Runtime、LLMProviderPort、Response Normalizer 完成。
- 当前交付优先级：trace-first 的跨 backend explainability 已贯通 provider manager、preview 回读和 session/manifest 落盘链；`apply_lifecycle()` 已接上 provider-aware `lifecycle_apply` 写回通道，lifecycle review queue 也已具备正式 durable `pending / dismissed / applied` review state，并新增独立 lifecycle audit trail 记录 review/apply 历史；当前又把 `queue_filter` 驱动的 batch `dismiss / reopen`、reviewer resolution taxonomy、更明确的 audit read model 和 queue guidance 一并收口进显式 review workflow。下一步优先补更完整的人工审核闭环和 reviewer-facing 运维能力，而不是继续扩 file-based test transport。

## 必要时回源的正式文档

- `docs/04-project-development/09-evolution/retrospective.md`
- `docs/04-project-development/10-traceability/requirements-matrix.md`

## 必守规则

- 不跳阶段。
- 代码类工作必须走 PR 闭环后再关单。
- 任何已接受变更都要同步代码、文档、测试、`.factory/memory/`。
- 遇到阻塞、空转或质量漂移时，优先执行 `factory-dispatch recovery`。
- 发现问题时优先做模式级修复，再把有效做法沉淀到 `evolution-baseline.md`。
- 任务单位是人天，最小精度 0.5，但不是默认拆分步长。
- 禁止默认把阶段 `docs/` 列入“先读”。
- 禁止每次开工都全文读取 `docs/`、`user-guide`、演进长文或设计长文。
- 禁止跳过 `.factory/memory/*` 而直接回源人类文档。
- 禁止把正式文档回源候选理解为默认运行时输入。
- 禁止把 skill 当成动作注册表或命令目录；命令执行统一走 `factory-dispatch`、`action-registry` 和 `scripts/factory-*`。
- 进入实现前必须回源核对 `docs/04-project-development/04-design/technical-selection.md` 的正式事实。

## 当前推荐动作

- `python3 scripts/factory-dispatch session --project "." --owner "Codex"`
- `python3 scripts/factory-dispatch board --project "." --owner "Codex" --focus "当前协作焦点"`
- `python3 scripts/factory-dispatch doctor --project "." --owner "Codex" --scope full`
