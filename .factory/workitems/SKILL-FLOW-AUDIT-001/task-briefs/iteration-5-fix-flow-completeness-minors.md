# SKILL-FLOW-AUDIT-001 Iteration 5 Flow Completeness Minor Fixes

## 目标

修复 [skill-flow-completeness-test-iteration-5.md](../reviews/skill-flow-completeness-test-iteration-5.md) 中全部 Minor 问题。

此任务必须在 `iteration-5-fix-prompt-engineering-95` 完成后执行，避免与状态包修复互相覆盖。

## 必读输入

- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-completeness-test-iteration-5.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-4-s1-s6-dry-run-transcript.md`
- `skills/doc-coauthoring/SKILL.md`
- `skills/ui-ux-pro-max/SKILL.md`
- 前两个 iteration-5 修复任务的 report / evidence / review input

## 允许修改

- `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-4-s1-s6-dry-run-transcript.md`
- `skills/doc-coauthoring/SKILL.md`
- `skills/ui-ux-pro-max/SKILL.md`
- 直接对应的结构测试：
  - `tests/test_black_box_workflow_eval.py`
  - `tests/test_skill_flow_process_audit.py`
- 本任务自己的 report / evidence / review input
- `.factory/workitems/SKILL-FLOW-AUDIT-001/ledger.jsonl`

不要修改 memory；由主线程统一同步。

## 修复要求

1. S1-S6 transcript 的 S4/S5 必须显式列出读取 `.factory/workitems/SKILL-FLOW-AUDIT-001/ledger.jsonl` 和 `.factory/memory/review-ledger.jsonl` 的文件或命令。
2. `doc-coauthoring` 和 `ui-ux-pro-max` 若直接作为 Shanforge work item owner，必须有同样的 `work_item/status/outputs/evidence/ledger_event/needs` 状态包。
3. 不建设自动黑盒 runner。当前报告明确不需要，新增 runner 是过度设计。

## 验证

至少运行：

```bash
uv run pytest tests/test_black_box_workflow_eval.py tests/test_skill_flow_process_audit.py
uv run ruff check tests/test_black_box_workflow_eval.py tests/test_skill_flow_process_audit.py
git diff --check
```

## 输出

- `.factory/workitems/SKILL-FLOW-AUDIT-001/reports/iteration-5-fix-flow-completeness-minors-report.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-5-fix-flow-completeness-minors-verification.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/iteration-5-fix-flow-completeness-minors-review-input.md`
- ledger event：`iteration-5-fix-flow-completeness-minors:implementation`
