# T01 评审整改验证

## 定向回归

```bash
uv run pytest -q tests/test_project_artifact_contracts.py -k 'design or repository_rejects or keeps_existing'
```

结果：exit `0`，`15 passed, 15 deselected`。

## 真实 CLI

```bash
PYTHONPATH=src .venv/bin/python -m settings.composition.project_knowledge design validate --json
```

结果：exit `0`，`valid=true`，`subject_count=7`，`issues=[]`。

## 静态检查

```bash
uv run ruff check src/domain/project_artifacts src/application/project_artifacts src/settings/project_artifacts tests/test_project_artifact_contracts.py src/access/project_cli.py src/application/project_knowledge/query_service.py src/settings/composition/project_knowledge.py
uv run mypy src/domain/project_artifacts src/application/project_artifacts src/settings/project_artifacts
```

结果：Ruff exit `0`；Mypy exit `0`，7 个源文件无问题。

## Iteration 2 完整回归

```bash
uv run pytest -q tests/test_project_artifact_contracts.py
PYTHONPATH=src .venv/bin/python -m settings.composition.project_knowledge design validate --json
uv run ruff check src/domain/project_artifacts src/application/project_artifacts src/settings/project_artifacts tests/test_project_artifact_contracts.py
uv run mypy src/domain/project_artifacts src/application/project_artifacts src/settings/project_artifacts
```

结果：pytest exit `0`，`33 passed`；真实 CLI exit `0` 且 `valid=true`；
Ruff exit `0`；Mypy exit `0`。

## 边界

- 未创建 `.penpot`。
- 未提交 SQLite、HTML 或缓存。
- 未把 `v1.2.0` 记录为已经审核或批准的正式版本。
