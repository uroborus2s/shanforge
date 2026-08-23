# 当前状态

- 当前模式：`codex_desktop`
- 当前阶段：`MODEL-ROUTING-001 / MODEL-ROUTING-001-T01`
- 活跃任务数：1
- 阻塞项数：0
- 当前 Gate：`T01_post_review_full_verification_and_baseline_commit`

## 活跃任务

- `MODEL-ROUTING-001-T01`：统一 skill-first 事实、清理历史过程资产并恢复可复现测试基线。

## 阻塞项

- 无。

## 最近事实

- 用户已授权先完成事实源和干净克隆收口，再实现 Sol 控制、Terra/Luna 执行的模型路由。
- 当前架构事实源是 `docs/05-design/system-architecture.md`：仓库不提供 `src/` 平台运行时。
- 历史大型候选、原始证据和截图已备份到 `/tmp/shanforge-model-routing-001-untracked-backup-20260823.tar.gz` 后清理。
- 清理前工作区完整测试为 `220 passed / 8 failed / 4 subtests`；失败均已定位为旧断言或需求 Skill 缺失明确根因门。

## 唯一下一动作

- 运行复审后的完整验证，形成本地基线提交，再从该提交执行干净克隆复验。

## 历史回源

- 通用执行事实：`.factory/workitems/<WORKITEM-ID>/ledger.jsonl`
- 非活跃任务摘要：`.factory/memory/tasks.summary.md`
- WorkItem：`.factory/workitems/MODEL-ROUTING-001/`
- 当前计划：`.factory/workitems/MODEL-ROUTING-001/plan.md`
- 正式架构：`docs/05-design/system-architecture.md`

> 本文件只是有界当前态投影，不替代正式文档和 ledger。
