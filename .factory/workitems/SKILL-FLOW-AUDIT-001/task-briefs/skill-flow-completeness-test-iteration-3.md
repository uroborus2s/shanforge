# Skill Flow Completeness Test Iteration 3

## Role

Skill 流程测试工程师。

## Goal

After the language/prompt fixes, test whether the skill flow still covers the full Shanforge software development process and whether each step output satisfies requirements.

## Inputs

- Current workflow skills under `skills/`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reports/language-prompt-review-iteration-2-fix-report.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-completeness-test-iteration-2.md` only as previous baseline.
- Relevant tests.

## Test Steps

Check:

1. session recovery;
2. intent clarification / brief;
3. requirements / AC / NFR;
4. design / docs / boundaries;
5. implementation plan / task brief;
6. execution / evidence / report / ledger;
7. bug fix / TDD / root cause;
8. verification before completion;
9. independent review / scoring;
10. review feedback handling;
11. human confirmation gate;
12. local commit;
13. remote PR / push / merge boundary;
14. compaction recovery and idempotency.

## Output

Write:

`.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-completeness-test-iteration-3.md`

Report must include:

1. Flow matrix: step, owner skill, input, action, output, gate, assessment.
2. Whether every step output fully satisfies Shanforge requirements.
3. Critical / Important / Minor findings.
4. Real verification commands and results.
5. Total score 0-100.
6. Delta versus iteration 2.
7. Minimal next fix list.

## Forbidden

- Do not edit skill files.
- Do not add center scripts or old `factory-*` gates.
- Do not claim real behavior replay unless evidence exists.
- Do not treat local commit as remote PR / push / merge closure.
