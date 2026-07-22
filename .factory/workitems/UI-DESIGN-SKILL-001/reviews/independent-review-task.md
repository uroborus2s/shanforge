# Independent Review Task

你是 `UI-DESIGN-SKILL-001 / TASK-SKILL-001` 的独立 reviewer。

不要读取实现者会话历史，不要修改文件、Git、ledger 或外部系统。只读取以下文件化输入包和当前任务范围 diff。

## Inputs

- Task brief: `.factory/workitems/UI-DESIGN-SKILL-001/task-briefs/TASK-SKILL-001.md`
- Implementer report: `.factory/workitems/UI-DESIGN-SKILL-001/reports/TASK-SKILL-001-implementation-report.md`
- Verification: `.factory/workitems/UI-DESIGN-SKILL-001/evidence/TASK-SKILL-001-verification.md`
- Forward test: `.factory/workitems/UI-DESIGN-SKILL-001/evidence/TASK-SKILL-001-forward-test.md`
- Ledger: `.factory/workitems/UI-DESIGN-SKILL-001/ledger.jsonl`
- Implementation: `skills/ui-ux-pro-max/**`
- Tests: `tests/test_ui_ux_pro_max_skill.py` and only the `ui-ux-pro-max` hash line in `tests/test_work_skill_status_envelope_ownership.py`
- Memory hunk: only the `UI-DESIGN-SKILL-001` entry in `.factory/memory/skill-updates.summary.md`
- Review ledger hunk: only the `UI-DESIGN-SKILL-001` event in `.factory/memory/review-ledger.jsonl`
- Diff commands: `git diff -- skills/ui-ux-pro-max tests/test_ui_ux_pro_max_skill.py tests/test_work_skill_status_envelope_ownership.py .factory/workitems/UI-DESIGN-SKILL-001 .factory/memory/skill-updates.summary.md`; use `git status --short -- <same paths>` to include untracked files.

## Review job

1. Perform both Spec Review and Quality Review against the task brief.
2. Verify requested platform and motion coverage, routing boundaries, output contract, source/license handling, deterministic helper behavior, tests, and dirty-worktree isolation, including the task-only shared review-ledger hunk.
3. Do not accept claims solely from the report; inspect the actual files and run relevant read-only checks if needed.
4. Grade using `skills/requesting-code-review/references/review-score-rubric.md`.
5. Return reviewer metadata, `Critical / Important / Minor` findings with file and line, verification run, category scores, total score, `approved | changes_requested`, and `pending_human_confirmation | changes_requested`.
6. `approved` is an independent quality conclusion only; it does not mark the task done and does not represent user approval.
