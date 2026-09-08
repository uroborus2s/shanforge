# 最终验证

- 完整回归：`UV_CACHE_DIR=/private/tmp/shanforge-uv-cache uv run pytest -q --ignore=tests/test_dynamic_model_dispatch.py`，exit 0，418 passed / 11 subtests passed。
- 定向回归：五组任务测试，49 passed。
- Ruff：五份受影响 Python 测试通过。
- 历史证据：manifest SHA-256 为 `3e86f667d21da7aac61aaa388fd9f642a233e3d12714ae47ea7a761c074ae4dc`，与历史 review brief 一致。
- JSONL：当前 WorkItem ledger、派发回执和全局 review ledger 均逐行解析通过。
- `git diff --check`：通过。
- 排除：并发 `MODEL-DYNAMIC-DISPATCH-001` 工作项与 `tests/test_dynamic_model_dispatch.py` 不属于本任务，未纳入验证。
