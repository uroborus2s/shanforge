# TEST-GOVERNANCE-CLOSURE-001 Review 整改验证

## 反馈复现 Red

- 命令：治理测试排除正式发布 Gate。
- 结果：`3 failed, 12 passed, 1 deselected`，exit code `1`。
- 失败：索引/详情名称漂移未拒绝、负数计数错误类型不符、正式文档未使用 `uv run python`。
- 环境核实：`command -v python` 无输出；Reviewer 的 exit 127 结论成立。

## 整改 Green

- 治理测试排除正式发布 Gate：`15 passed, 1 deselected`，exit code `0`。
- Ruff（校验器和治理测试）：`All checks passed!`，exit code `0`。
- 正式案例命令：`uv run python ... --catalog docs/06-delivery/test-cases.md` 返回 `catalog: valid (4 cases)`，exit code `0`。

## 关闭内容

- I1：正式计划、案例和三份模板统一使用项目 `uv run python` 入口；测试拒绝裸 `python`。
- I2：校验索引/详情名称、需求、层级、优先级、风险和入口；检查前置、fixture、步骤、后置清理、标签；拒绝负数七态计数。
- 负例同时覆盖名称漂移、失效节点、缺少后置/标签、负数、总数不等、批次结论和 GO/NO-GO 漂移。

正式发布 Gate 仍保持未切换，等待同一 Reviewer 复审。
