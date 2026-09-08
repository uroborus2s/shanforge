# 实现与定向验证

- 候选：工作树 diff `c6de645995b2b7c852e48c17f9c16776da4e5cb6be755e7b4025f472a5daf491`
- 范围：主会话模型选择与子任务派发控制职责解耦。
- RED（worker 回执）：`uv run pytest -q tests/test_model_tier_routing.py`，exit 1，7 passed / 2 failed；旧用户指南与模型固定合同触发预期失败。
- GREEN（父会话新鲜复核）：`UV_CACHE_DIR=/private/tmp/shanforge-uv-cache uv run pytest -q tests/test_model_tier_routing.py`，exit 0，11 passed。
- 静态检查：`UV_CACHE_DIR=/private/tmp/shanforge-uv-cache uv run ruff check tests/test_model_tier_routing.py`，exit 0，All checks passed。
- diff：`git diff --check`，exit 0。
- 兼容性：保留 `sol_source_writes` 机器字段，明确其语义为主会话源码写入。
- 排除：`.factory/workitems/MODEL-DYNAMIC-DISPATCH-001/` 与 `tests/test_dynamic_model_dispatch.py` 属于并行任务，未读取、修改或计入本结果。
