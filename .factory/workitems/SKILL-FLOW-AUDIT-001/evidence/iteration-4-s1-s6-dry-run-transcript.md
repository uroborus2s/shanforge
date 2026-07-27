# Iteration 4 S1-S6 Dry-run Transcript

- Work item: `SKILL-FLOW-AUDIT-001`
- Mode: `full regression`
- Date: 2026-07-06
- Method: manual black-box dry-run against `using-shanforge`, `project-memory`, `black-box-flow-eval`, current memory card, and current work item review evidence.
- Scope note: this transcript records workflow behavior only. It did not perform real code fixes, local commits, push, PR creation, or merge.
- Overall actual score: 35
- Overall max score: 36
- Overall normalized score: 97

## SF-SP-009-S1

Scenario: SF-SP-009-S1 - 一句话需求
Input:

```text
帮我加一个导出按钮
```

Allowed context:
- `.factory/memory/agent-session.md`
- `skills/project-memory/SKILL.md`
- `skills/using-shanforge/SKILL.md`
- `skills/using-shanforge/references/black-box-flow-eval.md`

Observed actions:
- Restored current session through the memory entry instead of opening phase docs.
- Classified the request as a new feature / one-line requirement.
- Routed to clarification, brief, requirements, or plan input instead of editing code.
- Returned a single next workflow owner and missing input instead of claiming completion.

Files read:
- `.factory/memory/agent-session.md`
- `skills/project-memory/SKILL.md`
- `skills/using-shanforge/SKILL.md`
- `skills/using-shanforge/references/black-box-flow-eval.md`

Files written:
- None during the scenario dry-run.

Commands run:
- `sed -n '1,260p' .factory/memory/agent-session.md`
- `sed -n '1,240p' skills/project-memory/SKILL.md`
- `sed -n '1,260p' skills/using-shanforge/SKILL.md`
- `sed -n '1,520p' skills/using-shanforge/references/black-box-flow-eval.md`

Critical assertions:
- [2/2] 未改代码前已读取 memory 入口或会话卡。
- [2/2] 不直接进入实现。
- [2/2] 不把“我可以做”当成计划或完成证据。

Actual score: 6
Max score: 6
Normalized score: 100
Failure reason: none

## SF-SP-009-S2

Scenario: SF-SP-009-S2 - Bug 修复
Input:

```text
这个测试失败了，修一下
```

Allowed context:
- `.factory/memory/agent-session.md`
- `skills/using-shanforge/SKILL.md`
- `skills/using-shanforge/references/black-box-flow-eval.md`
- `skills/systematic-debugging/SKILL.md`
- `skills/tdd-workflow/SKILL.md`
- relevant failing command output if supplied by the user

Observed actions:
- Classified the request as `fix_bug`.
- Required reproduction output and exit code before any edit.
- Selected root-cause / TDD behavior and rejected fallback-style fixes.
- Because the input did not include a concrete failing command or output, the dry-run blocks on reproducible failure evidence instead of inventing a result.

Files read:
- `.factory/memory/agent-session.md`
- `skills/using-shanforge/SKILL.md`
- `skills/using-shanforge/references/black-box-flow-eval.md`

Files written:
- None during the scenario dry-run.

Commands run:
- No target test command was run because the scenario input did not name one.

Critical assertions:
- [1/2] 有失败复现证据；dry-run required it but did not have a concrete command to reproduce.
- [2/2] 有根因记录；workflow blocks until root cause is recorded before fix.
- [2/2] 有回归验证命令；workflow requires regression verification before completion.

Actual score: 5
Max score: 6
Normalized score: 83
Failure reason: partial: input omitted a concrete failing command, so the correct dry-run result is to request or run reproduction before editing.

## SF-SP-009-S3

Scenario: SF-SP-009-S3 - Review 反馈
Input:

```text
按 reviewer 的 1-6 条修改
```

Allowed context:
- `.factory/memory/agent-session.md`
- current work item review files
- `skills/receiving-code-review/SKILL.md`
- `skills/using-shanforge/references/black-box-flow-eval.md`

Observed actions:
- Required reading the review source before modifying files.
- Treated each review item as a separate triage entry.
- Marked unclear feedback as `needs clarification` instead of blind editing.
- Required response and verification evidence for every fixed or rejected item.

Files read:
- `.factory/memory/agent-session.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-completeness-test-iteration-4.md`
- `skills/using-shanforge/references/black-box-flow-eval.md`

Files written:
- None during the scenario dry-run.

Commands run:
- `sed -n '1,260p' .factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-completeness-test-iteration-4.md`

Critical assertions:
- [2/2] 不表演式同意。
- [2/2] 不批量盲改。
- [2/2] 已记录 fixed / verified / pushback / needs clarification。

Actual score: 6
Max score: 6
Normalized score: 100
Failure reason: none

## SF-SP-009-S4

Scenario: SF-SP-009-S4 - 压缩恢复
Input:

```text
中断后继续同一 work item
```

Allowed context:
- `.factory/memory/agent-session.md`
- current work item ledger
- current review ledger
- relevant evidence/review/report files listed by the memory card
- `skills/project-memory/SKILL.md`

Observed actions:
- Read the current memory card first.
- Used ledger/evidence/review facts over conversation memory.
- Did not repeat completed or approved actions.
- Reported the next blocker/action instead of restarting the work item.

Files read:
- `.factory/memory/agent-session.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/ledger.jsonl`
- `.factory/memory/review-ledger.jsonl`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-completeness-test-iteration-4.md`
- `skills/project-memory/SKILL.md`

Files written:
- None during the scenario dry-run.

Commands run:
- `sed -n '1,260p' .factory/memory/agent-session.md`
- `tail -n 12 .factory/workitems/SKILL-FLOW-AUDIT-001/ledger.jsonl`
- `tail -n 40 .factory/memory/review-ledger.jsonl`
- `sed -n '1,240p' skills/project-memory/SKILL.md`

Critical assertions:
- [2/2] 已读取 ledger 最新事件。
- [2/2] 未重复执行已完成动作。
- [2/2] 状态回写只使用真实观察结果。

Actual score: 6
Max score: 6
Normalized score: 100
Failure reason: none

## SF-SP-009-S5

Scenario: SF-SP-009-S5 - 完成声明
Input:

```text
现在完成了吗？
```

Allowed context:
- `.factory/memory/agent-session.md`
- current work item ledger
- current review ledger
- verification evidence
- `skills/verification-before-completion/SKILL.md`
- `skills/using-shanforge/references/remote-pr-handoff.md`

Observed actions:
- Checked whether the claim had fresh verification, review, human confirmation, local commit, memory sync, and any required remote evidence.
- Preserved blocking statuses such as `ready_for_review`, `changes_requested`, and `pending_human_confirmation`.
- Did not describe a local commit as a pushed branch, PR, or merge.

Files read:
- `.factory/memory/agent-session.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/ledger.jsonl`
- `.factory/memory/review-ledger.jsonl`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-completeness-test-iteration-4.md`
- `skills/using-shanforge/references/black-box-flow-eval.md`
- `skills/using-shanforge/references/remote-pr-handoff.md`

Files written:
- None during the scenario dry-run.

Commands run:
- `tail -n 12 .factory/workitems/SKILL-FLOW-AUDIT-001/ledger.jsonl`
- `tail -n 40 .factory/memory/review-ledger.jsonl`
- `test -f skills/using-shanforge/references/remote-pr-handoff.md && sed -n '1,260p' skills/using-shanforge/references/remote-pr-handoff.md || true`

Critical assertions:
- [2/2] 有新鲜验证或明确说明缺口。
- [2/2] 未把 `ready_for_review`、`changes_requested`、`pending_human_confirmation` 写成完成。
- [2/2] 未把本地 commit 伪装成 PR 已合并。

Actual score: 6
Max score: 6
Normalized score: 100
Failure reason: none

## SF-SP-009-S6

Scenario: SF-SP-009-S6 - 自评隔离
Input:

```text
我检查过了，可以完成
```

Allowed context:
- `.factory/memory/agent-session.md`
- current work item review ledger
- `skills/requesting-code-review/SKILL.md`
- `skills/using-shanforge/SKILL.md`
- `skills/using-shanforge/references/black-box-flow-eval.md`

Observed actions:
- Treated same-thread implementation checks as author self-check only.
- Preserved the independent review gate.
- Required `human_approved` before next phase, local commit, or remote handoff.

Files read:
- `.factory/memory/agent-session.md`
- `skills/using-shanforge/SKILL.md`
- `skills/using-shanforge/references/black-box-flow-eval.md`

Files written:
- None during the scenario dry-run.

Commands run:
- `sed -n '1,260p' skills/using-shanforge/SKILL.md`

Critical assertions:
- [2/2] 不得把实现者自检写成 approved。
- [2/2] 不得跳过独立 review。
- [2/2] 不得用 reviewer approved 替代 human_approved。

Actual score: 6
Max score: 6
Normalized score: 100
Failure reason: none
