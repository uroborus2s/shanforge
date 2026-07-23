# T01 Penpot 设计资产合同验证证据

## Red

- 命令：`uv run pytest -q tests/test_project_artifact_contracts.py`
- 结果：exit 2；collection 因 `application.project_artifacts` 不存在而失败。
- 第二次 Red：合同模块完成后 13 passed、3 failed；三条 CLI 仍返回 exit 2，
  证明固定命令尚未接入。

## Green

- 命令：`uv run pytest -q tests/test_project_artifact_contracts.py -k design`
- 结果：exit 0；4 passed、13 deselected。
- 命令：`PYTHONPATH=src .venv/bin/python -m settings.composition.project_knowledge design validate --json`
- 结果：exit 0；`valid=true`、`subject_count=7`、`issues=[]`。
- 命令：`uv run ruff check src/domain/project_artifacts src/application/project_artifacts src/settings/project_artifacts tests/test_project_artifact_contracts.py src/access/project_cli.py src/application/project_knowledge/query_service.py src/settings/composition/project_knowledge.py`
- 结果：首次发现 composition import order；修复后 exit 0，`All checks passed!`。
- 命令：`uv run mypy src/domain/project_artifacts src/application/project_artifacts src/settings/project_artifacts`
- 结果：exit 0；10 个源文件无类型问题。

## 边界

- 没有创建 `.penpot`。
- manifest 明确为 `awaiting_penpot_connection`，`source.file=null`。
- 没有运行真实 Penpot 文件读取、画布修改、导出或视觉验收，因为用户尚未在具体
  Penpot 文件中加载本地插件。
- SQLite、HTML 和缓存未进入 Git。
