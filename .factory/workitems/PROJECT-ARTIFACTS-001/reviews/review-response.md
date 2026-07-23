# T01 Review Response

## Fixed

- `T01-C1`：补齐 manifest 根字段、数组类型、稳定 ID、source 必填字段和未知字段校验。
- `T01-I1`：在 `resolve()` 前逐段检查仓内路径链，拒绝文件或父目录 symlink。
- `T01-I2`：新增独立 `DesignTokens/v1` validator；repository 对 Token 执行严格
  JSON 解析和 4 MiB 限制，application 将 Token 结果并入固定设计校验命令。
- `T01-I3`：Schema 新增等待连接、ready/deprecated 两组 `if/then` 条件，并收紧
  Penpot、Token 和导出文件路径。
- `T01-I4`：新增缺字段/错误 ID、symlink、损坏/超大 Token、Token 领域合同和
  `project find` 根命令回归。
- `T01-I5`：正式版本恢复为 `v1.1.0`，`v1.2.0` 明确标记为待评审候选。
- `T01-M1`：验证证据已替换为完整命令。
- `T01-R2-C1`：组件 states 现在拒绝非字符串、空字符串、重复值和 enum 外值。
- `T01-R2-I1`：集成 fixture 改为完整合法 `DesignTokens/v1`，并改跑整个合同测试文件。
- `T01-R2-I2`：三个路径正则增加点段否定条件，Schema 自身拒绝 `.` 和 `..` 路径段。

## Verified

- `uv run pytest -q tests/test_project_artifact_contracts.py -k 'design or repository_rejects or keeps_existing'`
  → `15 passed, 15 deselected`
- `PYTHONPATH=src .venv/bin/python -m settings.composition.project_knowledge design validate --json`
  → exit `0`，`valid=true`，`subject_count=7`
- 限定 Ruff → `All checks passed!`
- 限定 Mypy → `Success: no issues found in 7 source files`

Iteration 2 完整验证：

- `uv run pytest -q tests/test_project_artifact_contracts.py`
  → `33 passed`
- 真实 `design validate --json` → exit `0`，`valid=true`，`subject_count=7`
- 限定 Ruff → `All checks passed!`
- 限定 Mypy → `Success: no issues found in 7 source files`
