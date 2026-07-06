# Language And Prompt Review Iteration 3

## Role

中文语言专家 + prompt 专家。

## Goal

After the language/prompt fixes, re-review all current `skills/*/SKILL.md`.

Focus on:

- verbose or repetitive wording;
- unclear semantics;
- prompt boundary problems;
- missing output contract, evidence, status, or failure semantics;
- old ecosystem / English wording.

## Inputs

- Current `skills/*/SKILL.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reports/language-prompt-review-iteration-2-fix-report.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/language-prompt-review-iteration-2.md` only as previous baseline.

## Output

Write:

`.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/language-prompt-review-iteration-3.md`

Report must include:

1. Actual skill count and file list.
2. Every skill score, 0-100.
3. Remaining skills below 90, grouped by verbose/repetition, unclear semantics, prompt boundary, output contract, old wording.
4. Score delta versus iteration 2 for changed skills.
5. Top 10 remaining common issues.
6. Minimal next fix list.

## Forbidden

- Do not edit skill files.
- Do not overwrite iteration-2 report.
- Do not score deleted skills.
- Do not mark suggestions as already fixed.
