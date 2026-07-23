# T03 验证证据

## 合同与投影测试

```bash
uv run pytest -q tests/test_project_artifact_contracts.py \
  tests/test_project_artifact_extractor.py \
  tests/test_project_artifact_index.py
```

结果：exit `0`，`68 passed`。

覆盖：

- 测试案例 catalog 的追踪、步骤/预期、优先级、数据与自动化字段；
- 单次结果七态、逐步结果、证据路径包含与 SHA-256；
- 报告只能引用已验证结果，汇总必须与结果逐项一致；
- 通过结果不能含失败步骤，且必须由每个步骤引用真实登记证据；
- catalog ID、JSON 标量/对象测试数据和报告同一 run ID 失败关闭；
- 三份 Schema 与 domain 使用同一组 Draft 2020-12 正反样例；
- YAML 容器执行环检测和 64 层深度门；对象内部合法 JSON 数组可用；
- catalog 投影为 `definition:<status>`，不能冒充执行结果；
- 非法外键使同一事务回滚，旧 generation 与旧 `pk_test` 保持不变。

## 固定 CLI

```bash
PYTHONPATH=src uv run python -m settings.composition.project_knowledge \
  test-cases validate --json
```

结果：exit `0`，`valid=true`，`catalog_count=1`，`subject_count=4`。

## 真实索引

```bash
PYTHONPATH=src uv run python -m settings.composition.project_knowledge \
  project index rebuild --json
```

结果：exit `0`，`parsed_count=623`，`source_count=623`。

SQLite 查询结果：

- 4 条稳定测试定义，状态均为 `definition:active`；
- 4 条定义的 `last_evidence_entity_id` 均为空；
- 当前索引共有 28 条 `VERIFIES` 强关系。

## 静态检查

```bash
uv run ruff check src/domain/project_artifacts src/application/project_artifacts \
  src/runtime/project_artifacts src/settings/project_artifacts \
  tests/test_project_artifact_contracts.py \
  tests/test_project_artifact_extractor.py \
  tests/test_project_artifact_index.py
uv run mypy src/domain/project_artifacts src/application/project_artifacts \
  src/runtime/project_artifacts src/settings/project_artifacts
```

结果：Ruff exit `0`；Mypy exit `0`。
