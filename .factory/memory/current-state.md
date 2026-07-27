# 当前状态

- 当前模式：`codex_desktop`
- 当前阶段：`FLOW-CONTRACT-001 / FLOW-TASK-015`
- 活跃任务数：1
- 阻塞项数：0
- 当前 Gate：`approved_ready_for_exact_local_commit`
- 停止原因：无

## 活跃任务

- `FLOW-TASK-015`：重塑完整软件项目会话行为与工作流归因契约。
  - 状态：`approved_ready_for_exact_local_commit`
  - 目标：实现复审 `approved / 98 / C0-I0-M0`，当前只执行按 hunk 精确本地提交。
  - TaskCard：`.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-015.md`
  - Ledger：`.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`

## 阻塞项

- 无。

## 最近事实

- 用户已批准冻结候选 SHA-256 `3d5f4cba…` 进入正式发布、runtime Skill 同步、验证、独立实现 Review 和精确本地提交。
- 唯一正式文档已在工作树原位晋升为 v1.2.0，9 个 runtime Skills 已同步最小路由合同；定向 Red/Green 为 `1 failed -> 8 passed`。
- `FLOW-TASK-015` 三轮方案 Review 最终 `approved / 98 / C0-I0-M1`；全部语义 finding 关闭，唯一计数 Minor 已修正。
- `FLOW-TASK-014` 已通过同一独立 Reviewer 复审：`approved / 98 / C0-I0-M0`。
- `FLOW-TASK-013` 已通过同一独立 Reviewer 复审：`approved / 98 / C0-I0-M0`；项目级测试治理候选仍明确为未发布，不伪造正式批准。

## 唯一下一动作

- 按 hunk 精确暂存 FLOW-TASK-015，核对 staged diff 后执行已授权本地提交。

## 历史回源

- 任务执行事实：`.factory/workitems/<WORKITEM-ID>/ledger.jsonl`
- 非活跃任务摘要：`.factory/memory/tasks.summary.md`
- 测试摘要：`.factory/memory/tests.summary.md`
- Review 索引：`.factory/memory/review-ledger.jsonl`
- 正式事实定位：`.factory/memory/doc-map.md`

> 本文件只是有界当前态投影，不是正式事实源。历史任务详情继续保留在 ledger、evidence、review、report 和 summary 中。
