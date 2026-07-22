# T01 合同内核与 39 表 Schema Red/Green 证据

- Work item：`FLOW-CONTRACT-001`
- Task：`TASK-IMPLEMENT-003-P001-T01`
- Actor：`AI_EXECUTOR`
- 日期：2026-07-22
- 状态：`green`

## Red

```bash
UV_CACHE_DIR=/tmp/shanforge-pki-uv-cache PYTHONPATH=src uv run pytest \
  tests/test_project_knowledge_schema.py \
  tests/test_project_knowledge_contracts.py -q
```

真实结果：2 个 collection error，exit 2。`domain.project_knowledge` 与 `settings.project_knowledge` 尚不存在，与新功能预期失败原因一致。

## Green

```bash
UV_CACHE_DIR=/tmp/shanforge-pki-uv-cache PYTHONPATH=src uv run pytest \
  tests/test_project_knowledge_schema.py \
  tests/test_project_knowledge_contracts.py -q
UV_CACHE_DIR=/tmp/shanforge-pki-uv-cache uv run ruff check \
  src/domain/project_knowledge src/application/project_knowledge \
  src/settings/project_knowledge tests/test_project_knowledge_schema.py \
  tests/test_project_knowledge_contracts.py
UV_CACHE_DIR=/tmp/shanforge-pki-uv-cache uv run mypy \
  src/domain/project_knowledge src/application/project_knowledge \
  src/settings/project_knowledge
```

真实结果：`9 passed in 0.03s`；Ruff `All checks passed!`；mypy `Success: no issues found in 6 source files`；总 exit 0。失败 0，错误 0，跳过 0，未运行项 0。

## 结论

T01 实现证据足以进入 `ready_for_review`；不代表后续 T02–T06 完成。
