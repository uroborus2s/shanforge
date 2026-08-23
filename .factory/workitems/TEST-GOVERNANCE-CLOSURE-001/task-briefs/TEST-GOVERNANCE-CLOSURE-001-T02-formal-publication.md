# TEST-GOVERNANCE-CLOSURE-001-T02 任务简报

## 工作项

- 工作项：`TEST-GOVERNANCE-CLOSURE-001`
- 任务：`TEST-GOVERNANCE-CLOSURE-001-T02`
- 状态：`active`
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
- route_reason: 正式测试策略发布和模板合同跨多个 owner。
- escalation_triggers: `scope_expanded | input_conflict | risk_increased | verification_failed_twice | human_gate`

## 目标

补齐三份测试模板的可执行校验合同，并把经用户批准的测试策略发布为 `v3.2.0`。

## 允许修改

- `docs/06-delivery/test-plan.md`
- `docs/06-delivery/index.md`
- `docs/document-index.md`
- `.factory/memory/doc-map.md`
- `skills/document-templates/SKILL.md`
- `skills/document-templates/assets/templates/05-quality/test-plan.md`
- `skills/document-templates/assets/templates/05-quality/test-cases.md`
- `skills/document-templates/assets/templates/05-quality/test-report.md`
- `skills/verification-before-completion/SKILL.md`
- `tests/test_work_skill_status_envelope_ownership.py`

## 禁止修改

- 未登记文档布局和并行工作项。

## 验证命令

`uv run pytest -q tests/test_project_test_governance.py tests/test_work_skill_status_envelope_ownership.py`

## 完成口径

正式计划、导航、模板和 Skill 合同一致，受影响测试通过。
