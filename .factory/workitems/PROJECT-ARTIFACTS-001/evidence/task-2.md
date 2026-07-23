# T02 OpenAPI 与 YAML 索引验证证据

## Red

- YAML extractor 测试最初 collection 失败：
  `ModuleNotFoundError: runtime.project_artifacts`。
- 组合 registry 测试最初 collection 失败：
  `ModuleNotFoundError: settings.project_artifacts.source_registry`。
- OpenAPI 稳定 ID、重复/非法追踪四个负例最初均被误判为 `valid=true`。
- 首次真实 `project index rebuild --json` 原子失败：
  `missing relation endpoint: REQ-002`，未发布悬空关系。

## Green

```bash
uv run pytest -q tests/test_project_artifact_contracts.py -k openapi
```

结果：exit `0`，`8 passed, 30 deselected`。

```bash
uv run pytest -q tests/test_project_artifact_extractor.py::test_design_manifest_has_stable_entities_locators_and_contains_relations
uv run pytest -q tests/test_project_artifact_extractor.py::test_openapi_operations_have_stable_entities_locators_and_relations
uv run pytest -q tests/test_project_artifact_extractor.py::test_composite_registry_discovers_human_docs_and_machine_artifacts
```

结果：三条命令均 exit `0`，各执行 `1 passed`。

```bash
PYTHONPATH=src .venv/bin/python -m settings.composition.project_knowledge api validate --json
```

结果：exit `0`，`valid=true`，`subject_count=4`，`issues=[]`。

## 真实 SQLite 集成

为 OpenAPI 已引用的七个既有 PRD 标题补同名稳定 section marker，并把表格态
`REQ-VIS-*` 引用改为已有稳定 `REQ-PKI-009` 后：

```bash
PYTHONPATH=src .venv/bin/python -m settings.composition.project_knowledge project index rebuild --json
```

结果：exit `0`，source `621`，parsed `621`，新 generation 原子发布。

SQLite 检查：

- `api_operation`：4
- API `SATISFIES` 强关系：11
- YAML path locator：12

## 静态检查

- 限定 Ruff：exit `0`，`All checks passed!`
- 限定 Mypy：exit `0`，8 个源文件无问题
- 限定 `git diff --check`：exit `0`
