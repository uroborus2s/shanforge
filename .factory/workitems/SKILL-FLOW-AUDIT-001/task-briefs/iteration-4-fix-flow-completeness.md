# Iteration 4 Fix Flow Completeness

## Goal

修复 Skill 流程完整性测试 iteration-4 的阻塞问题。只做最小闭环：补真实 S1-S6 行为回放 evidence、远端 PR / push / merge handoff 契约，以及相关结构测试。

## Inputs

- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-completeness-test-iteration-4.md`
- `skills/using-shanforge/references/black-box-flow-eval.md`
- `skills/using-shanforge/SKILL.md`
- `skills/using-shanforge/references/codex-tools.md`

## Allowed Files

- `skills/using-shanforge/SKILL.md`
- `skills/using-shanforge/references/black-box-flow-eval.md`
- `skills/using-shanforge/references/remote-pr-handoff.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-4-s1-s6-dry-run-transcript.md`
- `tests/test_black_box_workflow_eval.py`
- `tests/test_pr_commit_workflow_rules.py`
- `tests/test_skill_flow_process_audit.py`

## Required Fixes

1. 写真实 S1-S6 dry-run transcript，按 `black-box-flow-eval.md` 记录 `Scenario`、`Allowed context`、`Observed actions`、`Files read`、`Files written`、`Commands run`、`Critical assertions`、`Actual score`、`Max score`、`Normalized score`、`Failure reason`。
2. 定义远端 PR / push / merge 最小 handoff 契约：owner、输入、本地提交前提、可用远端工具、evidence、失败语义、状态词、禁止冒充规则。
3. 在 `using-shanforge` 中引用该 handoff 契约，但不要让 `gitcommitzh` 负责远端 PR / push / merge。
4. 补测试，固定 S1-S6 transcript 存在、远端 handoff 契约存在、仍禁止旧中心 `factory-*` gate。

## Verification

至少运行：

```bash
uv run pytest tests/test_black_box_workflow_eval.py tests/test_pr_commit_workflow_rules.py tests/test_skill_flow_process_audit.py
uv run ruff check tests/test_black_box_workflow_eval.py tests/test_pr_commit_workflow_rules.py tests/test_skill_flow_process_audit.py
```

## Output

写入：

- `.factory/workitems/SKILL-FLOW-AUDIT-001/reports/iteration-4-fix-flow-completeness-report.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-4-fix-flow-completeness-verification.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/iteration-4-fix-flow-completeness-review-input.md`

## Forbidden

- 不得新增中心脚本或旧 `factory-*` gate。
- 不得修改 `gitcommitzh` 让它负责远端 PR / push / merge。
- 不得把 dry-run transcript 写成实际远端操作完成。
- 不得提交。
- 不得把本任务写成 approved 或 done。
