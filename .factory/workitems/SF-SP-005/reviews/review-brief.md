# SF-SP-005 Review Brief

- Work item：`SF-SP-005`
- Review 类型：Spec Review + Quality Review
- Review 范围：执行类 workflow skill 本地化。
- 请求状态：`review_requested`

## 输入

- `tests/test_execution_workflow_skills.py`
- `skills/subagent-driven-development/SKILL.md`
- `skills/subagent-driven-development/references/implementer-task-template.md`
- `skills/subagent-driven-development/references/spec-review-template.md`
- `skills/subagent-driven-development/references/quality-review-template.md`
- `skills/subagent-driven-development/references/status-handling-checklist.md`
- `skills/subagent-driven-development/agents/openai.yaml`
- `skills/executing-plans/SKILL.md`
- `skills/executing-plans/agents/openai.yaml`
- `.factory/workitems/SF-SP-005/reports/implementer-report.md`
- `.factory/workitems/SF-SP-005/evidence/test-report.md`

## Spec Check

- 是否保留原始 `subagent-driven-development` 的隔离执行、状态处理和双阶段 review 语义。
- 是否保留原始 `executing-plans` 的 plan review、逐步执行和 blocker stop 语义。
- 是否全部改为 Shanforge work item、ledger、evidence、reports、reviews 路径。
- 是否没有提前实现评审类、验证类或调试类 skill。

## Quality Check

- `SKILL.md` 是否只放高频流程规则。
- 长模板是否进入 `references/`。
- 是否仍存在 `docs/superpowers` 或旧 finishing branch 入口。
- 测试是否覆盖本地化关键契约。
