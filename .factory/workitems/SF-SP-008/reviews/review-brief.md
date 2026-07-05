# SF-SP-008 Review Brief

## Review 目标

确认 PR 闭环与提交规则是否满足 `SF-SP-008` 范围。

## 输入

- `skills/gitcommitzh/SKILL.md`
- `skills/gitcommitzh/references/pr-closure-checklist.md`
- `skills/using-shanforge/SKILL.md`
- `skills/using-shanforge/references/codex-tools.md`
- `docs/04-project-development/05-development-process/superpowers-workflow-integration-plan.md`
- `tests/test_pr_commit_workflow_rules.py`
- `.factory/workitems/SF-SP-008/reports/implementer-report.md`
- `.factory/workitems/SF-SP-008/evidence/test-report.md`

## 检查点

- 提交前是否必须核对 work item ledger、review ledger、verification evidence 和 memory sync。
- `pending_human_confirmation` 是否仍需要人工确认或同轮明确继续提交指令。
- `gitcommitzh` 是否只做本地提交，不创建、不推送、不合并 PR。
- sandbox / detached HEAD 收尾是否只允许提交当前任务范围。
- 测试是否覆盖提交闭环规则。

## 禁止误判

- 不要把实现者 `ready_for_review` 当作 `approved`。
- 不要把本地 commit 当作远端 PR 已合并。
- 不要把 reviewer `approved` 当作人工 `human_approved`。
