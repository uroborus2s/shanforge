# 任务简报

## 工作项

- 工作项：`PROJECT-ARTIFACTS-001`
- 任务：`T03` 测试案例、结果与报告合同
- 状态：`approved`
- 上游计划：`.factory/workitems/PROJECT-ARTIFACTS-001/plan.md`
- 流水账：`.factory/workitems/PROJECT-ARTIFACTS-001/ledger.jsonl`

## 目标

建立稳定案例、单次结果、聚合报告三类分离合同，并让案例在同一事务进入 SQLite
测试索引与关系投影；本任务不承担质量页 HTML。

## 允许修改

- `tests/specifications/`
- `contracts/schemas/test-case-catalog.schema.json`
- `contracts/schemas/test-run-result.schema.json`
- `contracts/schemas/test-report.schema.json`
- `src/domain/project_artifacts/validation.py`
- `src/runtime/project_artifacts/yaml_extractor.py`
- `src/settings/project_knowledge/sqlite_index.py`（仅同一事务内合并 contribution.tests 的最小 hunk）
- `src/settings/composition/project_knowledge.py`（只装配扩展 index）
- `tests/test_project_artifact_contracts.py`
- `tests/test_project_artifact_extractor.py`
- `tests/test_project_artifact_index.py`
- `docs/06-delivery/test-plan.md`

## 禁止修改

- 把历史测试结果写入稳定测试定义。
- 一条测试一个文件。
- 把 `not_run` 或 `blocked` 显示成通过。

## 验证命令

```bash
uv run pytest -q tests/test_project_artifact_contracts.py -k test tests/test_project_artifact_extractor.py tests/test_project_artifact_index.py
PYTHONPATH=src .venv/bin/python -m settings.composition.project_knowledge test-cases validate --json
```

期望：pytest exit 0；CLI exit 0，回执 `data.valid=true`；原子失败测试证明旧 generation
和旧 `pk_test` 不变。

## 实施步骤

1. Red：缺追踪、缺 expected、非法定义状态和重复 ID 必须失败。
2. Green：实现 catalog validator 和固定 YAML catalog。
3. Red：七态 result 与 report 错误聚合测试。
4. Green：实现 result/report validator 和三份 JSON Schema；不登记运行实例为 source。
5. Red：catalog 未产生 `test` 实体、VERIFIES 边和 `pk_test` 定义状态。
6. Green：扩展 extractor/index，状态固定 `definition:<status>`。
7. 定向测试期望 0 failed；CLI 回执 `valid=true`。
8. 写 `evidence/task-3.md`、`reports/task-3.md` 和 ledger 事件。

## 完成口径

稳定测试 ID、步骤/预期、追踪、七态结果、报告聚合和 SQLite 原子投影全部由代码
验证；质量页和双向 HTML 访问由 T04 验收。
