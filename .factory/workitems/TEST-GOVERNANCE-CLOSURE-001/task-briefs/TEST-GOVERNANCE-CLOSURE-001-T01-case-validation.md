# TEST-GOVERNANCE-CLOSURE-001-T01 任务简报

## 工作项

- 工作项：`TEST-GOVERNANCE-CLOSURE-001`
- 任务：`TEST-GOVERNANCE-CLOSURE-001-T01`
- 状态：`completed`
- 优先级：`P0`
- 任务层级：`system`
- 关联目标：`TEST-PLAN-001`
- 强关系：`IMPLEMENTS`
- 上游计划：`.factory/workitems/TEST-GOVERNANCE-CLOSURE-001/plan.md`
- 流水账：`.factory/workitems/TEST-GOVERNANCE-CLOSURE-001/ledger.jsonl`

## 模型路由

- control_model: `gpt-5.6-sol`
- task_complexity: `complex`
- risk_level: `medium`
- execution_model: `gpt-5.6-terra`
- execution_authorized: `true`
- route_reason: 跨正式文档、Skill 资源和自动校验合同。
- escalation_triggers: `scope_expanded | input_conflict | risk_increased | verification_failed_twice | human_gate`

## 目标

建立正式案例目录和标准库校验器，能验证案例结构、自动化入口与报告聚合一致性。

## 允许修改

- `docs/06-delivery/test-cases.md`
- `skills/document-templates/scripts/validate_test_documents.py`
- `tests/test_project_test_governance.py`

## 禁止修改

- 并行工作项和旧平台资产。
- 第三方依赖与中心注册表。

## 验证命令

`uv run pytest -q tests/test_project_test_governance.py`

## 完成口径

Red 原因与预期一致；有效案例和报告通过，失效入口与聚合错误被拒绝。
