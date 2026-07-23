# Agent 会话卡

- 生成时间：2026-07-23 12:22 +0800
- 项目：`shanforge`
- 当前阶段：`PK-SOURCE-MIGRATION-001-T03 UI FOLLOW-UP / INDEPENDENTLY APPROVED`
- 当前状态：`completed / independently_approved / ready_for_exact_local_commit`
- 当前焦点：任务详情内部定位信息移除，需求与设计追踪深链已落地
- 下一动作：完成本次精确范围本地提交；不执行 Push、PR、Merge 或部署

## 当前事实

- `docs/04-product/prd.md` 是当前需求唯一正式事实源；当前投影为 16 个 REQ、
  64 个 AC、11 个 NFR。
- R009 requirement contract 仍保留为冻结历史证据，但已退出当前 source registry；
  R009 PM map、R014 合同和 final manifest 仍保留。
- SQLite 只保存可重建索引、关系、章节定位和代码地图；正文继续按 locator 回源，
  SQLite、HTML、FTS 和 cache 不提交 Git。
- 需求、任务、代码、测试和文档详情使用独立静态页面与返回按钮；需求按中文能力分类，
  AC 嵌套在所属需求，任务显示中文标题并保留 canonical 编号。
- 九个任务端点与 88 条 `Task --IMPLEMENTS--> Requirement/NFR` 强关系完整。
  八个历史 ledger 任务有旧 ID alias；task-brief-only 的 T05 没有虚构 alias。
- HTML 由固定 CLI 增量生成；当前 1892 页，输入未变化时 `cache_hit=true`，
  `rendered_pages=0`。
- 任务业务详情不再展示 locator、Hash、内部 document ID 或追踪 DTO；任务详情分为
  关联需求、相关设计、代码测试与交付三个中文区域。
- 相关设计只通过 outgoing strong Task→Requirement 与 Requirement 侧 incoming strong
  `SATISFIES` Design 确定性推导；弱关系、错误类型和直接 Task→Design 均被拒绝。
- `FLOW-TASK-011` 可点击进入 `REQ-PKI-008` 和 `DESIGN-FRONTEND-001`。
- UI follow-up 独立复审：`approved / 99 / C0-I0-M0`。
- 原独立实现复审：`approved / 96 / C0-I0-M1`；Minor 为
  `pk_work_item.task_kind` 后续应改从机器字段派生，当前无消费者，不阻塞。
- 最新验证：目标回归 `62 passed`；Ruff 通过；Mypy `279 source files` 0 问题；
  全仓 `1342 passed, 3 failed`，三项均为已有范围外 Skill 合同失败。

## 最小读取顺序

1. 本文件。
2. `.factory/workitems/PK-SOURCE-MIGRATION-001/evidence/implementation-verification.md`。
3. `.factory/workitems/PK-SOURCE-MIGRATION-001/reviews/implementation-rereview-decision.md`。
4. 需要查事实时先用 `project find/show/trace/context`；只按 locator 单文件回源。

## 当前 Gate

实现、验证、独立 Review 和记忆同步已完成；当前仅剩 `gitcommitzh` 精确范围本地提交。
远端、PR、Merge 和部署未授权。
## 本轮恢复点：PROJECT-ARTIFACTS-001

- 四项任务均已实现并通过独立评审：T01 `97`、T02 `99`、T03 `98`、T04 `96`。
- 已交付 Penpot 资产 manifest/Token、OpenAPI 3.1、测试案例/结果/报告合同、
  SQLite 确定性投影和单一“项目文档”静态站点。
- 本机 Penpot MCP 已安装并注册，`4400–4403` 正在监听；仓库仍无伪 `.penpot`，
  下一步由用户在真实 Penpot 文件加载 `http://localhost:4400/manifest.json`。
- 当前唯一内部动作是干净候选验证与 `gitcommitzh` 精确范围提交；不改变
  `PK-SOURCE-MIGRATION-001-T04`、`FLOW-TASK-015` 的既有人工 Gate。
