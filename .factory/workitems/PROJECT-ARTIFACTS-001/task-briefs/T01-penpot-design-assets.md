# 任务简报

## 工作项

- 工作项：`PROJECT-ARTIFACTS-001`
- 任务：`T01` Penpot 设计资产合同
- 状态：`approved`
- 上游计划：`.factory/workitems/PROJECT-ARTIFACTS-001/plan.md`
- 流水账：`.factory/workitems/PROJECT-ARTIFACTS-001/ledger.jsonl`

## 目标

提供不伪造 `.penpot` 的设计资产合同、严格仓库读取和固定校验命令。

## 允许修改

- `src/domain/project_artifacts/__init__.py`
- `src/domain/project_artifacts/models.py`
- `src/domain/project_artifacts/validation.py`
- `src/application/project_artifacts/__init__.py`
- `src/application/project_artifacts/service.py`
- `src/settings/project_artifacts/__init__.py`
- `src/settings/project_artifacts/local_repository.py`
- `src/access/project_cli.py`（仅新 root 命令）
- `src/application/project_knowledge/query_service.py`（仅三个校验回调）
- `src/settings/composition/project_knowledge.py`（仅装配校验服务）
- `pyproject.toml`、`uv.lock`（仅 PyYAML 运行时依赖）
- `design/ux-ui/`
- `contracts/schemas/design-artifact-manifest.schema.json`
- `docs/05-design/ux-ui-design.md`
- `tests/test_project_artifact_contracts.py`
- 本工作项 evidence/report/ledger。

## 禁止修改

- 用户已有未归属本任务的脏改动。
- 未经 Penpot MCP 连接产生的 `.penpot` 文件。
- SQLite、HTML 和缓存产物的 Git 跟踪规则。

## 验证命令

```bash
uv run pytest -q tests/test_project_artifact_contracts.py -k design
PYTHONPATH=src .venv/bin/python -m settings.composition.project_knowledge design validate --json
```

期望：pytest exit 0；CLI exit 0，回执 `data.valid=true`。

## 实施步骤

1. Red：缺模块时测试 collection 失败；记录 exit code 2。
2. Green：实现 report、五个纯 validator、application port 和严格 repository。
3. Red：三条新 CLI 命令返回 `INVALID_INPUT`。
4. Green：只扩展 parser、command service 与 composition 回调。
5. Red/Green：ready 无 `.penpot`、`..` 路径和假导出文件均被拒绝。
6. 写实际 waiting manifest 与 Token，不创建 `.penpot`。
7. 用同一正负样本断言 JSON Schema required/enum 与 domain validator 一致。
8. 运行定向测试，期望 0 failed；命令回执 `data.valid=true`。
9. 写 `evidence/task-1.md`、`reports/task-1.md` 和 ledger 事件。

## 完成口径

合同、repository、manifest、Token 和 CLI 独立通过；SQLite/HTML 由后续 T02/T04
负责。实现者只能写 `ready_for_review`；真实 Penpot 文件仍需用户打开 Penpot 文件
并加载插件后生成。
