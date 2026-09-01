# 模块与领域设计

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `DESIGN-MODULE-001` |
| 正式版本 | `v4.0.0` |
| 状态 | 已批准并生效 |
| 负责人 | `HUMAN_ARCHITECTURE_DOMAIN_LEAD` |
| 上游 | `DESIGN-ARCH-001`、`PRD-SHANFORGE-001` |
| 下游 | 专项 skill、接口矩阵、测试 |

## 文档职责

- 划分当前仓库中的技能、事实、辅助脚本和测试责任。
- 不保留已废止的平台层、端口或领域对象模型。

## 当前设计

| 模块 | owner | 责任 | 输出 |
|---|---|---|---|
| `using-shanforge` | 流程控制面 | 分类、恢复、路由和 Gate 解释 | 路由包与人类可读状态。 |
| 专项 skills | 对应专业域 | 在授权范围内执行需求、设计、实现、测试、评审或发布动作 | 本职状态包与证据。 |
| `.factory/workitems/` | WorkItem ledger | 任务身份、状态、证据、Gate | 追加式执行事实。 |
| `.factory/memory/` | project-memory | 有界恢复投影 | 当前会话所需摘要。 |
| skill `scripts/` | 所属 skill | 可重复确定性辅助 | 可验证的 receipt 或生成物。 |
| `tests/` | 测试 owner | 回归 skill 合同和脚本行为 | pytest 结果。 |

依赖方向固定为：宿主加载控制 skill，控制 skill 选择一个专项 skill，专项 skill 使用宿主工具操作目标项目。正式文档和 ledger 不互相替代，脚本不成为流程主控。

## 适用验证

- `tests/test_lifecycle_governance.py` 验证当前设计未保留旧平台路径。
- 相应 skill 的定向 pytest 验证其合同。

## 正式版本历史

| 版本 | 日期 | 变更 |
|---|---|---|
| `v4.0.0` | 2026-09-01 | 删除旧平台模块拓扑，登记当前 Skill-first owner。 |
| `v3.1.0` | 2026-04-15 | 历史：旧平台模块与领域设计。 |
