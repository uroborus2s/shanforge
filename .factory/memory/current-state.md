# 当前状态

- 当前模式：`codex_desktop`
- 当前阶段：`MODEL-DYNAMIC-DISPATCH-001 / MODEL-DYNAMIC-DISPATCH-001-T00`
- 本批阶段：验证通过，进入本地提交；产品总体阶段未重新核对
- 活跃任务数：1
- 阻塞项数：0
- 当前 Gate：`commit`

## 活跃任务

- `MODEL-DYNAMIC-DISPATCH-001-T00`：动态模型合同的最终质量收口。

## 阻塞项

- 无。

## 最近事实

- 子任务模型/effort按唯一表独立选择并显式传递；风险下限、只读权限和失败重派均有合同。
- v5独立批准20文件；完整420 passed / 11 subtests passed，Ruff及三个skill校验通过。
- 新task-reader只做静态验证，宿主加载/执行未实测；12个独立场景为路由模拟。
- 前置任务已提交1b64734 / 242af89，用户并发值10和历史证据保持。
- 旧UI批次与主会话解耦批次历史记录保留在tasks.summary。

## 唯一下一动作

- `create_exact_local_commit`

## 历史回源

- 最近 WorkItem：`.factory/workitems/MODEL-DYNAMIC-DISPATCH-001/`
- Ledger：`.factory/workitems/MODEL-DYNAMIC-DISPATCH-001/ledger.jsonl`
- 稳定 Ledger 索引：`.factory/workitems/<WORKITEM-ID>/ledger.jsonl`
- 非活跃任务摘要：`.factory/memory/tasks.summary.md`

> 本文件只是有界当前态投影，不替代正式文档和ledger。
