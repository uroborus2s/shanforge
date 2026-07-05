# SF-SP-006 Review Brief

- Work item：`SF-SP-006`
- Review 类型：Spec Review + Quality Review
- Review 范围：评审类 workflow skill 本地化。
- 请求状态：`review_requested`

## 输入

- `tests/test_review_workflow_skills.py`
- `skills/requesting-code-review/SKILL.md`
- `skills/requesting-code-review/references/task-review-template.md`
- `skills/requesting-code-review/references/pr-review-template.md`
- `skills/requesting-code-review/references/independent-review-task-template.md`
- `skills/requesting-code-review/references/review-score-rubric.md`
- `skills/requesting-code-review/agents/openai.yaml`
- `skills/receiving-code-review/SKILL.md`
- `skills/receiving-code-review/references/feedback-triage-template.md`
- `skills/receiving-code-review/references/review-response-template.md`
- `skills/receiving-code-review/agents/openai.yaml`
- `.factory/workitems/SF-SP-006/reports/implementer-report.md`
- `.factory/workitems/SF-SP-006/evidence/test-report.md`

## Spec Check

- 是否保留请求 review 的早评审、独立输入包、severity 和处理反馈语义。
- 是否保留接收 review 的先核实、澄清、pushback、逐项处理和验证语义。
- 是否全部改为 Shanforge work item、ledger、review-ledger、人工确认门。

## Quality Check

- `SKILL.md` 是否保持流程简洁。
- 长模板是否进入 `references/`。
- 是否存在旧 Superpowers 路径或不合适的表演式同意句。
- 测试是否覆盖本地化关键契约。
