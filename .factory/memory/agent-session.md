# Agent 会话卡

- 生成时间：2026-07-23 09:50 +0800
- 项目：`shanforge`
- 当前阶段：`TASK-IMPLEMENT-003-P001 / KANBAN REMEDIATION INDEPENDENTLY APPROVED`
- 当前状态：`completed / independently_approved / ready_for_exact_local_commit`
- 当前焦点：项目快照任务状态与中文敏捷看板修复已完成
- 下一动作：完成本次精确范围本地提交；不执行 Push、PR、Merge 或部署

## 当前事实

- 项目总览已改为六列中文敏捷看板：待开始、进行中、测试中、待评审/待确认、阻塞、已完成。
- 看板卡片只显示中文任务标题；每列默认显示最近 10 条，使用“更多”展开；点击卡片进入带返回按钮的独立详情页。
- “暂无数据源”只表示该管理项没有登记权威事实源，不表示任务阻塞；“已有数据 / 待补充 / 暂无数据源 / 不适用”四态已写入页面说明。
- 旧 ledger 事件即使没有 `event_uid` 或 `idempotency_key` 也会生成确定性派生 ID，不再丢失后续评审、批准和完成状态。
- 任务状态按机器 ID 去重；父任务只在父子时间都有效且父事件不早于子事件时继承完成态；时间比较统一为带时区的绝对时间。
- SQLite 增量更新在实体或 locator 被其他记录引用时自动回退完整投影，避免外键失败；SQLite、HTML、FTS、cache 和浏览器截图仍是可重建投影，不提交 Git。
- 第五轮独立终审：`approved / 96 / C0-I0-M0`，`human_confirmation_required=false`。
- 最新验证：项目知识与站点相关回归 `102 passed`；Ruff、mypy `279 source files`、Chromium 桌面/移动端看板与详情页检查全部通过。
- 固定 CLI：`PYTHONPATH=src uv run python -m settings.composition.project_knowledge project snapshot --html --json`；输入未变时直接返回最后有效 `.factory/cache/site/current/index.html`。

## 最小读取顺序

1. 本文件。
2. `.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-IMPLEMENT-003-P001-review-remediation.md`。
3. `docs/05-design/frontend-design.md` 的“只读项目站点前端增补”。
4. 需要查事实时先用 `project find/show/trace/context`；只按 locator 单文件回源。

## 当前 Gate

实现、验证、自动独立 Review 和记忆同步已完成；当前仅剩 `gitcommitzh` 精确范围本地提交。远端、PR、Merge 和部署未授权。`TASK-IMPLEMENT-002-R001` 仍保持冻结且不属于本任务。
