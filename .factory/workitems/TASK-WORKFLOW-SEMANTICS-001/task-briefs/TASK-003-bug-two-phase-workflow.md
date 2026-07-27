# TASK-003 Bug Two Phase Workflow

## 目标

把 Bug 修复固化成“调查确认 -> 修复执行”的两段式流程。

## 允许修改

- `skills/systematic-debugging/SKILL.md`
- `skills/tdd-workflow/SKILL.md`
- `tests/test_bug_fix_root_cause_skill_rules.py`
- `tests/test_verification_debugging_workflow_skills.py`

## 验收

- Investigation Task 只做复现、诊断、直接原因 / 根源原因和根因报告。
- 不能复现时先要求更多信息，不修行为。
- 根因报告获人工确认前不得进入修复。
- TDD 修复只在根因确认和修复方案确认 Gate 通过后执行。

## 状态

ready_for_review
