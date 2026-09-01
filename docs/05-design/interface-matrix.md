# 接口与字段追踪矩阵

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `TRACE-API-001` |
| 正式版本 | `v4.0.0` |
| 状态 | 已批准并生效 |
| 负责人 | `HUMAN_API_INTEGRATION_LEAD` |
| 上游 | `DESIGN-API-001`、`DESIGN-DATA-001` |
| 下游 | 接口参考、定向测试 |

## 文档职责

- 登记当前真实契约的 consumer、owner、路径和验证。
- 不复制 schema 正文，也不登记已废止服务或候选附件。

## 当前接口矩阵

| 契约 | consumer | owner | 路径 | 验证 |
|---|---|---|---|---|
| 请求分类与路由包 | 代理宿主、专项 skill | `using-shanforge` | `skills/using-shanforge/SKILL.md` | 控制面 pytest。 |
| 专项 skill 状态包 | `using-shanforge` | 各 `SKILL.md` | `skills/<name>/SKILL.md` | 对应 skill pytest。 |
| WorkItem / TaskCard / ledger | 控制面、快照 | `.factory/workitems/` | `.factory/workitems/<ID>/` | 生命周期 pytest。 |
| 恢复摘要 | `project-memory`、控制面 | `.factory/memory/` | `.factory/memory/` | 恢复与边界 pytest。 |
| 子代理派发 receipt | 控制面 | 代理宿主工具 | `skills/using-shanforge/references/codex-tools.md` | 路由/派发 pytest。 |
| 快照 receipt | 用户和控制面 | `project_snapshot.py` | `skills/using-shanforge/scripts/` | 快照脚本 pytest。 |

## 维护规则

路径、owner 或 consumer 变更时，同时更新所属正式设计与定向测试。机器 schema 仅在有当前消费者时登记为独立附件；本矩阵只保留引用。

## 适用验证

- `uv run pytest tests/test_lifecycle_governance.py -q`
- 受影响 owner 的定向 pytest。

## 正式版本历史

| 版本 | 日期 | 变更 |
|---|---|---|
| `v4.0.0` | 2026-09-01 | 只登记当前 Skill-first 契约及其 owner。 |
| `v3.1.0` | 2026-07-28 | 历史：旧平台接口和字段追踪。 |
