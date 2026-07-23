# 任务简报

## 工作项

- 工作项：`PROJECT-ARTIFACTS-001`
- 任务：`T02` OpenAPI 详细合同
- 状态：`approved`
- 上游计划：`.factory/workitems/PROJECT-ARTIFACTS-001/plan.md`
- 流水账：`.factory/workitems/PROJECT-ARTIFACTS-001/ledger.jsonl`

## 目标

为当前四个 HTTP route 交付详细 OpenAPI 3.1 合同，并把设计资产和 API 操作提取为
稳定 source contribution；本任务不承担 HTML。

## 允许修改

- `contracts/openapi/openapi.yaml`
- `contracts/schemas/openapi-shanforge-rules.schema.json`
- `src/domain/project_artifacts/validation.py`
- `src/runtime/project_artifacts/yaml_extractor.py`
- `src/settings/project_artifacts/source_registry.py`
- `.factory/project-knowledge/artifact-source-registry.json`
- `src/settings/composition/project_knowledge.py`（只装配扩展 registry/extractor）
- `tests/test_project_artifact_contracts.py`
- `tests/test_project_artifact_extractor.py`
- `docs/05-design/api-design.md`
- `docs/04-product/prd.md`（只补 OpenAPI 已引用既有需求的稳定 section marker）

## 禁止修改

- HTTP route 的业务实现。
- 与当前 route 不一致的想象接口。

## 验证命令

```bash
uv run pytest -q tests/test_project_artifact_contracts.py -k openapi
uv run pytest -q tests/test_project_artifact_extractor.py::test_design_manifest_has_stable_entities_locators_and_contains_relations
uv run pytest -q tests/test_project_artifact_extractor.py::test_openapi_operations_have_stable_entities_locators_and_relations
PYTHONPATH=src .venv/bin/python -m settings.composition.project_knowledge api validate --json
```

期望：三条 pytest 均 exit 0，两个 extractor node 各实际执行 1 test；CLI exit 0，回执
`data.valid=true`、`subject_count=4`。

## 实施步骤

1. Red：中文、错误响应、示例、追踪和 route 集合各写一个失败断言。
2. Green：按计划锁定规则实现 `validate_openapi`。
3. 写当前四条 `build_runtime_routes()` 的完整 OpenAPI 3.1 合同。
4. Red：YAML 未产生 `api_operation`、locator 与关系。
5. Green：自包含 extractor 生成 operation 实体和 `CONTAINS/SATISFIES`。
6. 定向测试期望 0 failed；CLI 回执 `valid=true, subject_count=4`。
7. 写 `evidence/task-2.md`、`reports/task-2.md` 和 ledger 事件。

## 完成口径

代码 route 与 OpenAPI method/path 集合精确一致，全部操作通过详细合同校验，
设计/API 实体、locator 和关系提取通过；HTML 展示由 T04 验收。
