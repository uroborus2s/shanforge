# 需求追踪矩阵

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `TRACE-REQ-001` |
| 正式版本 | `v5.0.0` |
| 来源候选 | `MODEL-ROUTING-001` |
| 变更等级 | `MAJOR` |
| 状态 | 已批准并生效 |
| 负责人 / 变更 / 审核 / 批准 | `uroborus` |
| 最近更新 | 2026-08-23 |

## 当前需求映射

| 需求 ID | 设计 owner | 实现 owner | 当前任务 | 验证 | 状态 |
|---|---|---|---|---|---|
| `REQ-SF-001` | `workflow-execution-design.md` | `skills/using-shanforge` | `MODEL-ROUTING-001` | 流程合同测试 | 当前有效 |
| `REQ-SF-002` | `system-architecture.md` | `skills/*` | `MODEL-ROUTING-001` | Skill 合同测试 | 当前有效 |
| `REQ-SF-003` | `system-architecture.md` | `docs/`、`.factory/` | `MODEL-ROUTING-001-T01` | memory / ledger 合同 | 当前有效 |
| `REQ-SF-004` | `test-plan.md` | `tests/`、`pyproject.toml` | `MODEL-ROUTING-001-T01` | pytest / Ruff / JSON / Git | 当前有效 |
| `REQ-SF-005` | `prd.md` | Artifact 留存规则 | `MODEL-ROUTING-001-T01` | 清理 manifest / 恢复校验 | 当前有效 |
| `REQ-SF-006` | `system-architecture.md` | Skill-local scripts | 按所属 skill | 脚本合同测试 | 当前有效 |
| `REQ-SF-007` | `pm-dashboard-rendering.md` | `project_snapshot.py` | `PM-DASHBOARD-005-T01` | 快照合同测试 | 当前有效 |
| `REQ-SF-008` | `workflow-execution-design.md` | `using-shanforge` / 执行 skills | `MODEL-ROUTING-001-T02` | 模型路由合同测试 | 待 T02 实现 |
| `REQ-SF-009` | `workflow-execution-design.md` | 宿主权限与项目 Gate | 按工作项 | 负向权限测试 | 当前有效 |

## 追踪规则

- 正式需求只在本矩阵登记当前有效集合。
- `v4.2.0` 及更早平台运行时需求只存在于 Git 历史，不参与当前完成度或任务路由。
- 任务简报通过强关系 `IMPLEMENTS` 指向需求；缺少关系时进入待治理，不自动补造。
- Review、verification 和人工确认必须分别登记，彼此不能替代。
- 测试定义不等于测试执行；只有绑定当前候选的结果证据才可写为通过。

## 正式版本历史

| 版本 | 变更 | 日期 | 修改 / 审核 / 批准 |
|---|---|---|---|
| `v5.0.0` | 只保留 skill-first 当前需求映射，移除旧平台运行时矩阵 | 2026-08-23 | `uroborus` |
| `v4.2.0` | 历史：项目知识与状态站点需求矩阵 | 2026-07-28 | `uroborus` |
