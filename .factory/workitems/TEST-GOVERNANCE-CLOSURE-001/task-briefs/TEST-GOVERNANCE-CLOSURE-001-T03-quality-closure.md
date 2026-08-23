# TEST-GOVERNANCE-CLOSURE-001-T03 任务简报

## 工作项

- 工作项：`TEST-GOVERNANCE-CLOSURE-001`
- 任务：`TEST-GOVERNANCE-CLOSURE-001-T03`
- 状态：`completed`
- 优先级：`P0`
- 任务层级：`system`
- 关联目标：`TEST-PLAN-001`
- 强关系：`DEPENDS_ON`
- 上游计划：`.factory/workitems/TEST-GOVERNANCE-CLOSURE-001/plan.md`
- 流水账：`.factory/workitems/TEST-GOVERNANCE-CLOSURE-001/ledger.jsonl`

## 模型路由

- control_model: `gpt-5.6-sol`
- task_complexity: `complex`
- risk_level: `medium`
- execution_model: `gpt-5.6-terra`
- execution_authorized: `true`
- route_reason: 批次质量、独立评审和干净克隆收口。
- escalation_triggers: `scope_expanded | input_conflict | risk_increased | verification_failed_twice | human_gate`

## 目标

证明七项审计判断全部符合，生成最终报告并完成本地提交和干净克隆终验。

## 允许修改

- `.factory/workitems/TEST-GOVERNANCE-CLOSURE-001/**`
- `.factory/memory/agent-session.md`
- `.factory/memory/change-summary.md`
- `.factory/memory/tasks.summary.md`
- `.factory/memory/tests.summary.md`
- `.factory/memory/review-ledger.jsonl`

## 禁止修改

- 实现范围外文件和并行工作项。
- push、PR、merge、release、deploy。

## 验证命令

完整 pytest、Ruff、Skill validator、JSON/JSONL、Git hygiene 与干净克隆。

## 完成口径

独立评审无阻断项，最终报告和 evidence 可读，精确提交的干净克隆全绿。
