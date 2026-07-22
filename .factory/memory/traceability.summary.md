# 追踪摘要

- 更新时间：2026-07-15 01:45:15 +0800
- 正式需求基线：PRD `v3.1.0`
- 正式需求矩阵：`v3.1.0`
- 正式文档索引：`v1.1.0`
- 权威来源：`docs/04-project-development/03-requirements/prd.md`
- 追踪矩阵：`docs/04-project-development/10-traceability/requirements-matrix.md`
- 结构化图：`.factory/memory/graph/traceability.json`

## 当前追踪关系

- 原 `REQ-001` 至 `REQ-010` 和 `NFR-001` 至 `NFR-005` 平台基线继续保留原设计、任务和测试关系。
- `REQ-AI-WORKFLOW-001` 至 `053` 已作为正式需求发布，当前正式载体为 PRD `v3.1.0`，下游设计任务为 `TASK-DESIGN-001`。
- `NFR-AI-WORKFLOW-001` 至 `011` 已作为正式非功能需求发布，当前正式载体为 PRD `v3.1.0`，下游设计任务为 `TASK-DESIGN-001`。
- `REQ-CHANGE-WF-CTL-010-001` 已由 `TASK-REQ-002-R014` 发布并完整并入 `WF-CTL-010`；需求任务已正式化，机器合同为受控设计输入，`TASK-DESIGN-001` 状态为“需求变更影响待更新”。
- 123 条需求级 Workflow 映射保存在 `.factory/workitems/FLOW-CONTRACT-001/drafts/workflow-norm-mapping.candidate.jsonl`，只作为正式 Workflow Catalog 建立前的受控设计输入。
- 结构化图已登记 53 条治理 REQ、11 条治理 NFR 和 1 条正式需求变更到 PRD、任务和下游设计的关系；不复制需求正文。

## 当前缺口

- `TASK-DESIGN-001` 必须以正式 PRD `v3.1.0` 重新建立输入包和影响分析，并覆盖 R014 的进度快照、工具计划、HTML/Excel、准确性、权限和性能合同；现有候选在完成该更新前不得正式落档。
- 正式 Workflow Catalog 接管前，需求级 JSONL 仍保持 `design_required`，不得宣称流程已实现。
