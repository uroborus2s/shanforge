# 接口与函数参考

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `DOC-INTERFACE-REFERENCE-001` |
| 正式版本 | `v2.0.0` |
| 状态 | 已批准并生效 |
| 负责人 | `HUMAN_API_INTEGRATION_LEAD` |
| 上游 | `DESIGN-API-001`、`TRACE-API-001` |
| 下游 | Skill 使用者、维护者 |

## 文档职责

- 为维护者索引当前可调用的 Skill 和脚本入口。
- 不提供网络 API、SDK 或已废止平台函数参考。

## 当前接口

| 入口 | 用途 | 输入/输出 |
|---|---|---|
| `skills/using-shanforge/SKILL.md` | 项目化请求的分类、恢复和唯一 skill 路由 | 当前消息与项目事实 → 路由包/人类可读状态。 |
| `skills/<name>/SKILL.md` | 专项任务合同 | 授权输入 → 专业产物、证据和 needs。 |
| `skills/using-shanforge/scripts/project_snapshot.py` | 生成只读项目快照 | 目标项目根目录 → `SkillProjectSnapshotReceipt/v1`。 |
| `.factory/workitems/<ID>/ledger.jsonl` | 读取任务执行事实 | 追加事件 → 可审计状态。 |

脚本不是服务入口；由代理宿主或已引用的 skill 按其参数合同调用。变更入口时同步所属 `SKILL.md`、接口矩阵和定向测试。

## 适用验证

- 受影响 skill 或脚本的 pytest。
- `uv run pytest tests/test_lifecycle_governance.py -q`。

## 正式版本历史

| 版本 | 日期 | 变更 |
|---|---|---|
| `v2.0.0` | 2026-09-01 | 收口为当前 Skill 和快照脚本参考。 |
| `v1.0.0` | 2026-07-28 | 历史：旧接口与函数参考。 |
