# 测试摘要

- 更新时间：2026-04-14 00:40:00
- 当前验证重点：`v2` 平台契约、文档结构、JSON 结构和 Python 回归测试

## 当前质量门

- `docs-stratego source validate --repo-path .`
- `.factory/project.json` JSON 解析
- `.factory/memory/graph/traceability.json` JSON 解析
- `uv lock --check`
- `uv run pytest`
- `git diff --check`

## 新增验证方向

- REQ / MOD / API / TASK 编号一致
- Workflow DSL、ModelPolicy、Capability 和 AgentResponse schema 可校验
- 业务 App 不直接依赖基础设施 adapter
- 高风险执行必须经过 approval / sandbox
- Session ledger 是第一事实源，memory promotion 不能覆盖原始 evidence
- recall 只消费 accepted memory，并保留 source refs 与 diagnostics

## 最近验证结果

- 2026-04-14：`uv run pytest tests/test_memory_runtime.py tests/test_context_engine.py tests/test_platform_scaffold.py` 通过，覆盖 evidence 投影、candidate promotion gate、context long-term memory segment 和跨 session recall。
- 2026-04-14：`uv run ruff check src/domain/memory src/runtime/memory src/infrastructure/persistence/memory_store.py src/domain/session/models.py src/application/ports.py src/application/execution_service.py src/bootstrap/container.py src/runtime/engine/context_engine.py tests/test_memory_runtime.py tests/test_context_engine.py tests/test_platform_scaffold.py` 通过。
- 2026-04-14：新增验证点覆盖 summarizer 草案接入、`candidate -> decision` dataset 样本沉淀、以及 `JSONL-backed` store 的跨容器持久化 recall。
- 2026-04-14：新增验证点覆盖自定义 `MemoryPromotionPolicy` 拒绝低置信 declarative candidate，以及容器在 mock provider 下启用 `LLMMemorySummarizer`。
- 2026-04-14：新增验证点覆盖 `LLMMemorySummarizer` 对 invalid candidate schema 的拒绝，以及对模型 `kind/scope/confidence` override 的忽略。
- 2026-04-14：新增验证点覆盖同一 session repeated distill 的幂等性，以及容器按 settings 应用自定义 promotion policy。
- 2026-04-14：仓库全量 `uv run pytest` 通过，`105 passed`，记忆系统收口未引入跨模块回归。
- 2026-04-15：新增 `tests/test_infrastructure_scaffold.py`，覆盖 Hermes bridge config、Hermes-backed container switch 和 gateway round-trip；仓库全量 `uv run pytest` 通过，`109 passed`。
