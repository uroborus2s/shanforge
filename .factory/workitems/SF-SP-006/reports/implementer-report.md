# SF-SP-006 Implementer Report

- Work item：`SF-SP-006`
- 实现者状态：`ready_for_review`
- 范围：新增评审类 workflow skill。
- 日期：2026-07-05

## 本次完成

- 新增 `tests/test_review_workflow_skills.py`。
- 新增 `skills/requesting-code-review/SKILL.md`。
- 新增 `skills/requesting-code-review/references/task-review-template.md`。
- 新增 `skills/requesting-code-review/references/pr-review-template.md`。
- 新增 `skills/requesting-code-review/references/independent-review-task-template.md`。
- 新增 `skills/requesting-code-review/references/review-score-rubric.md`。
- 新增 `skills/requesting-code-review/agents/openai.yaml`。
- 新增 `skills/receiving-code-review/SKILL.md`。
- 新增 `skills/receiving-code-review/references/feedback-triage-template.md`。
- 新增 `skills/receiving-code-review/references/review-response-template.md`。
- 新增 `skills/receiving-code-review/agents/openai.yaml`。

## 保留的 Superpowers 语义

- `requesting-code-review` 保留“早 review、常 review”的质量门。
- reviewer 只拿输入包，不继承实现者会话历史。
- Critical 必须修，Important 必须在继续前处理或登记风险。
- `receiving-code-review` 保留先读、理解、核实、评估、回应、再实现的顺序。
- 反馈不清楚时必须先问。
- 外部 reviewer 反馈必须先核实，不盲从。
- 禁止表演式同意和盲改。

## Shanforge 改造

- review 输出固定进入 `.factory/workitems/<WORKITEM-ID>/reviews/`。
- review ledger 固定进入 `.factory/memory/review-ledger.jsonl`。
- loop 结束后 reviewer approved 只能进入 `pending_human_confirmation`。
- feedback triage 和 response 模板进入 `receiving-code-review/references/`。

## 未完成

- `verification-before-completion` 尚未本地化。
- `systematic-debugging` 尚未本地化。
- 当前变更尚未提交，也未进入 PR 闭环。

## 验证

见 `evidence/test-report.md`。
