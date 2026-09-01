# 数据与存储设计

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `DESIGN-DATA-001` |
| 正式版本 | `v2.1.0` |
| 状态 | 已批准并生效 |
| 负责人 | `HUMAN_DATABASE_LEAD` |
| 上游 | `PRD-SHANFORGE-001`、`DESIGN-ARCH-001` |
| 下游 | project-memory、快照、测试 |

## 文档职责

- 定义当前文件型事实及其唯一 owner。
- 不定义关系数据库、ORM、迁移或运行时存储服务。

## 当前设计

| 数据 | owner | 写入规则 | 消费者 |
|---|---|---|---|
| `docs/` | 正式文档 | 保存稳定、可审计事实 | 人类和专项 skill。 |
| `ledger.jsonl` | WorkItem | 追加任务状态、证据和 Gate | using-shanforge、快照。 |
| `.factory/memory/` | project-memory | 有界摘要；不覆盖 docs 或 ledger | 会话恢复。 |
| `.factory/cache/` | 所属脚本 | 可删除重建投影 | 静态只读快照。 |

解析失败、关系不闭合或事实冲突时失败关闭；修复对应 owner，不能以缓存或摘要覆盖源事实。

## 适用验证

- `uv run pytest tests/test_lifecycle_governance.py -q`
- 快照脚本相关定向测试。

## 正式版本历史

| 版本 | 日期 | 变更 |
|---|---|---|
| `v2.1.0` | 2026-09-01 | 明确 docs、ledger、memory 与缓存的当前文件型边界。 |
| `v2.0.0` | 2026-07-28 | 收口旧持久化方案。 |
