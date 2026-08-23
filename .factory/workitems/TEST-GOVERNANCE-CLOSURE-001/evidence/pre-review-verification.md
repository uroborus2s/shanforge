# TEST-GOVERNANCE-CLOSURE-001 预评审验证

## 范围

- 候选：基于 `28b82dd` 的当前 WorkItem 精确 diff。
- 并行范围：`SKILL-FULL-OPTIMIZATION-001` 及其 Skill/测试改动全部排除。
- 已知 Gate：`test_test_governance_revision_is_formally_published` 必须在独立评审返回后才能由红转绿。

## Red

- 命令：`uv run pytest -q tests/test_project_test_governance.py`
- 结果：exit code `1`，`6 failed, 9 passed`。
- 失败对应：正式 `v3.2.0`、正式案例目录、校验脚本、失效入口负例、报告聚合负例和模板校验入口均尚未实现。

## 实现候选

- 定向治理测试（排除发布 Gate）：`14 passed, 1 deselected`，exit code `0`。
- 相邻工作 Skill 合同：`5 passed`，exit code `0`。
- 正式案例校验：`catalog: valid (4 cases)`，exit code `0`。
- 完整 pytest：`1 failed, 245 passed, 4 subtests passed`，exit code `1`；唯一失败为独立评审后才能落档的正式发布状态。
- Ruff：`All checks passed!`，exit code `0`。
- `document-templates`、`verification-before-completion` Skill validator：均为 `Skill is valid!`，exit code `0`。
- `git diff --check`：exit code `0`。

## 负例证据

- 将登记的 pytest 节点改为不存在名称：校验器 exit code `1`，报告 `automation target does not exist`。
- 将全通过计数配成 `failed` 批次结论：校验器 exit code `1`，报告 `batch verdict does not match result counts`。

## 未运行项

- 网络 API、动态 UI、性能、安全专项：Shanforge 当前没有对应运行时暴露面，不为补表制造测试。
