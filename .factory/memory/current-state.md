# 当前状态

- 当前模式：`codex_desktop`
- 当前阶段：`MODEL-ROUTING-001 / CLOSED`
- 活跃任务数：0
- 阻塞项数：0
- 当前 Gate：`none`

## 活跃任务

- 当前无活动任务。

## 阻塞项

- 无。

## 最近事实

- 用户已授权先完成事实源和干净克隆收口，再实现 Sol 控制、Terra/Luna 执行的模型路由。
- 当前架构事实源是 `docs/05-design/system-architecture.md`：仓库不提供 `src/` 平台运行时。
- 历史大型候选、原始证据和截图已备份到 `/tmp/shanforge-model-routing-001-untracked-backup-20260823.tar.gz` 后清理。
- 清理前失败均已定位；T01 基线提交 `9245946` 的干净克隆为 `228 passed / 4 subtests passed`，Ruff、JSON/JSONL 和 Git 门通过。
- T02 已固化 Sol 唯一控制、Terra/Luna 受控执行合同；独立复审 `approved / 98 / C0-I0-M0`，
  路由提交 `c9f02cb` 的干净克隆为 `233 passed / 4 subtests passed`，工作项已关闭。

## 唯一下一动作

- 本任务无待办。

## 历史回源

- 通用执行事实：`.factory/workitems/<WORKITEM-ID>/ledger.jsonl`
- 非活跃任务摘要：`.factory/memory/tasks.summary.md`
- WorkItem：`.factory/workitems/MODEL-ROUTING-001/`
- 当前计划：`.factory/workitems/MODEL-ROUTING-001/plan.md`
- 正式架构：`docs/05-design/system-architecture.md`

> 本文件只是有界当前态投影，不替代正式文档和 ledger。
