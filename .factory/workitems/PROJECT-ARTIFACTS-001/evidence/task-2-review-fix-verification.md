# T02 评审整改验证

```bash
uv run pytest -q tests/test_project_artifact_contracts.py tests/test_project_artifact_extractor.py tests/test_project_artifact_index.py
```

结果：exit `0`，`48 passed`。其中包含：

- Schema 与 domain 规则字段断言；
- 英文 OpenAPI summary 被 extractor 拒绝；
- 伪造同 source ID、不同路径的定义被组合 registry 拒绝；
- 四路由、稳定 locator、强关系和真实 catalog 投影。

```bash
uv run ruff check src/domain/project_artifacts src/runtime/project_artifacts src/settings/project_artifacts src/settings/project_knowledge/sqlite_index.py src/settings/composition/project_knowledge.py tests/test_project_artifact_contracts.py tests/test_project_artifact_extractor.py tests/test_project_artifact_index.py
uv run mypy src/domain/project_artifacts src/runtime/project_artifacts src/settings/project_artifacts
```

结果：Ruff exit `0`；Mypy exit `0`，8 个源文件无问题。

## Iteration 2

```bash
uv run pytest -q tests/test_project_artifact_contracts.py -k openapi
```

结果：exit `0`，`11 passed, 32 deselected`。

新增样例直接使用 `jsonschema.Draft202012Validator`：

- `206 + 418`：Schema 与 domain 均接受；
- `"中" + 19 个空格`：Schema 与 domain 均拒绝；
- 只有 `206` 或只有 `418`：Schema 与 domain 均拒绝。

```bash
uv run ruff check src/domain/project_artifacts/validation.py tests/test_project_artifact_contracts.py
uv run mypy src/domain/project_artifacts
```

结果：Ruff exit `0`；Mypy exit `0`。

## Iteration 3

新增合法成功/错误响应同时混入非法键的回归：

- `206 + 418 + 2XX`：Schema 与 domain 均拒绝；
- `206 + 418 + 600`：Schema 与 domain 均拒绝；
- `default` 保持可登记，但不参与成功/错误响应计数。
