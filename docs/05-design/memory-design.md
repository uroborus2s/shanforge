# 记忆系统设计

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `DESIGN-MEMORY-001` |
| 正式版本 | `v4.0.0` |
| 状态 | 已批准并生效 |
| 负责人 | `HUMAN_ARCHITECTURE_DOMAIN_LEAD` |
| 上游 | `PRD-SHANFORGE-001`、`DESIGN-DATA-001` |
| 下游 | `project-memory`、快照、测试 |

## 文档职责

- 定义项目恢复摘要与正式/执行事实的边界。
- 不定义运行时记忆服务、向量检索、训练或持久化平台。

## 当前设计

`project-memory` 只在项目化请求的上下文恢复、状态查询或必要同步中按需读取 `.factory/memory/`。会话卡优先，摘要不足时才按最小范围回源正式文档或 WorkItem ledger。memory 只保存活动任务、当前 Gate、关键约束、已验证输出索引和恢复所需摘要；不复制正式正文、完整日志或秘密。

事实优先级为：正式文档和 WorkItem ledger 高于 memory，memory 高于缓存投影。当前态保持有界；历史详情通过正式 owner 或 ledger 回源。冲突必须修复 owner，不能由摘要覆盖。

## 适用验证

- project-memory 和生命周期定向 pytest。
- 检查当前态行数、大小和恢复读取范围。

## 正式版本历史

| 版本 | 日期 | 变更 |
|---|---|---|
| `v4.0.0` | 2026-09-01 | 用当前有界恢复设计替换旧 runtime memory 方案。 |
| `v3.1.0` | 2026-07-28 | 历史：旧记忆系统设计。 |
