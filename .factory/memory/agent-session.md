# Agent 会话卡

- 生成时间：2026-09-05
- 项目：`shanforge`
- 项目整体进度：`UI-VISUAL-QUALITY-001` 已完成 3/3 个 TaskCard
- 当前工作项：`UI-VISUAL-QUALITY-001`
- 当前任务：`UI-VISUAL-QUALITY-001-T03`
- 当前 WBS：`WBS-UI-VISUAL-QUALITY-03`
- 当前状态：`closed`
- 当前 Gate：`closed`
- 停止原因：无
- 下一动作：`none`

## 当前事实

- 用户授权候选检索、平台适配、美术学习与截图质量流程重构。
- 独立计划评审 approved；两个隔离 Terra/medium worker 已完成脚本与设计规则并闭合作者自检。
- 首轮独立评审 3 个 Important 已关闭，另恢复 UTF-8 CLI；全仓 403 passed / 11 subtests passed，同 reviewer 复审 approved / 96 / C0-I0-M0。
- 真实 12 组产品 UI 截图 A/B 不在本轮执行范围，不能声称已验证普遍美观。
- 保留 UI 与非 UI 素材职责边界，不修改批准的设计或素材。

## 已读取上下文

- `.factory/memory/agent-session.md`：确认上一工作项已关闭，无可复用活动身份。
- `.factory/workitems/UI-VISUAL-QUALITY-001/`：本次身份、计划与真实派发回执。
- `skills/ui-ux-pro-max/`、`skills/art-asset-pipeline/`、`skills/using-shanforge/SKILL.md`：本次规则事实源。

## 未读 / 已排除上下文

- 已按 doc-map 回源技术选型与系统架构；不修改正式产品设计或架构事实。
- 其他历史 work item 正文：不影响本次两个 Skill 的职责重构。

## 禁止动作

- 不得重复执行已关闭的 `UI-DESIGN-MASTER-001-T01`。
- 不得重复执行已关闭的 `UI-VISUAL-QUALITY-001`；后续真实 UI A/B 须有明确任务范围。
- 不得把本地完成误报为远端发布。
- 不得从旧 memory 历史条目恢复已关闭 Gate。

## 恢复入口

- `.factory/workitems/UI-VISUAL-QUALITY-001/ledger.jsonl`
- `.factory/workitems/UI-VISUAL-QUALITY-001/plan.md`
- `.factory/workitems/UI-VISUAL-QUALITY-001/reviews/dispatch-receipts.jsonl`
- `.factory/workitems/UI-VISUAL-QUALITY-001/evidence/verification.md`
- `.factory/workitems/UI-VISUAL-QUALITY-001/reviews/independent-rereview.md`
