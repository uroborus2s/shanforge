# SF-SP-004 Review Brief

- Work item：`SF-SP-004`
- Review 类型：Spec Review + Quality Review
- Review 范围：新增 Shanforge 本地化 `writing-plans` skill。
- 请求状态：`review_requested`

## 输入

- `tests/test_writing_plans_skill.py`
- `skills/writing-plans/SKILL.md`
- `skills/writing-plans/references/workitem-plan-template.md`
- `skills/writing-plans/references/task-brief-template.md`
- `skills/writing-plans/references/plan-review-template.md`
- `skills/writing-plans/agents/openai.yaml`
- `.factory/workitems/SF-SP-004/reports/implementer-report.md`
- `.factory/workitems/SF-SP-004/evidence/test-report.md`

## Spec Check

- 是否保留 Superpowers `writing-plans` 的核心语义。
- 是否把路径改成 `.factory/workitems/<WORKITEM-ID>/`。
- 是否包含 work item plan、task brief、memory sync 和 review gate。
- 是否没有提前实现执行类或评审类 skill。

## Quality Check

- `SKILL.md` 是否保持流程简洁。
- 长模板是否放入 `references/`。
- 测试是否覆盖本地化关键契约。
- 是否存在占位符式计划内容或 Superpowers 旧路径残留。
