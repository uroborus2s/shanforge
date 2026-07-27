# EAD-TASK-001-COMPLETE 完成能力评估任务卡

## Task

把 `ENTERPRISE-AI-DELIVERY-001` 下已创建的 `EAD-TASK-001 能力评估与差距分析` 从任务卡状态推进到 `ready_for_review`。

## Parent

- Work item: `ENTERPRISE-AI-DELIVERY-001`
- Parent task card: `EAD-TASK-001`

## Inputs

- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/brief.md`
- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/plan.md`
- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/task-briefs/EAD-TASK-001-capability-assessment.md`
- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/reports/initial-capability-assessment.md`
- 售前材料分析结论和 PPT：`/Users/uroborus/Documents/Codex/2026-07-07/ni/outputs/cscec-industrial-worker-platform-ai-delivery-loop-sales-deck.pptx`

## Allowed Changes

- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/reports/`
- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/evidence/`
- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/reviews/`
- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/ledger.jsonl`
- 必要时同步 `.factory/memory/tasks.summary.md`，但不得覆盖当前 FLOW/SKILL 活跃任务事实。

## Required Outputs

- `reports/EAD-TASK-001-implementer-report.md`
- `evidence/EAD-TASK-001-verification.md`
- `reviews/EAD-TASK-001-review-input.md`
- `ledger.jsonl` 新增 `ead_task_001_ready_for_review` 事件。

## Execution Checklist

- 复核 `brief.md`、`plan.md` 和 `EAD-TASK-001` task brief。
- 检查 `initial-capability-assessment.md` 是否覆盖：
  - 当前 Shanforge 能解决什么。
  - 当前 Shanforge 不能直接解决什么。
  - 需要补齐什么能力。
  - AI 如何提速、增效和规范化。
  - 多岗位如何协同。
  - 如何形成输入、结构化、人审、执行、验证、复盘、沉淀闭环。
- 若报告缺项，最小修改补齐报告。
- 运行 JSONL parse 检查。
- 运行文档内容检查，至少确认关键章节存在。
- 写 implementer report。
- 写 verification evidence。
- 写 review input，交给独立 review。
- ledger 状态只能推进到 `ready_for_review`，不得写 `approved` 或 `complete`。

## Done Definition

- EAD-TASK-001 有执行报告、验证证据和 review 输入。
- ledger 最新事件为 `ead_task_001_ready_for_review`，`next_required_action` 为 `independent_review`。
- 没有跳过 review、verification 或 human confirmation。

## Non-goals

- 不开发完整企业工作台。
- 不接入客户系统。
- 不提交 git commit。
- 不关闭整个 work item。
