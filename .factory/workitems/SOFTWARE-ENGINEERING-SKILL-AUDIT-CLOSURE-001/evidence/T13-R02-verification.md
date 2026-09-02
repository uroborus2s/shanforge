# T13-R02 计划模板与依赖 DAG 验证

- 根因修复位置：
  - `workitem-plan-template.md`：计划前输入改为“验收标准”，计划任务加入 owner/depends_on，明确 WBS 与 TaskCard 两套状态词表。
  - `task-brief-template.md`：加入稳定 owner/depends_on。
  - `plan-review-template.md`：要求可执行 DAG 校验。
  - `validate_task_graph.py::main`：拒绝缺 owner、未知依赖、自依赖、环和跨模板 owner/depends_on 不一致。
  - `test_plan_template_task_card_ledger_and_snapshot_are_connected`：实例化 plan 和 TaskCard 两个正式模板后接 ledger/snapshot。
- RED：首轮 `4 failed, 24 passed, 4 subtests passed`；父级发现菱形误报和重复合同覆盖后，新增检查 RED `2 failed, 1 passed`。
- GREEN：父级新鲜复验 `30 passed, 4 subtests passed`。
- Ruff、代码形态与 `git diff --check` 通过；无函数套函数或无职责单调用公共 helper。
