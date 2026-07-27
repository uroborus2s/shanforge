# SKILL-CLOSEOUT-001-T02 已批准候选精确提交

## 状态

`verified_ready_for_local_commit`

## 目标

将 `FLOW-TASK-013`、`FLOW-TASK-014` 与 T01 隔离修复组成可在干净检出通过的自包含本地提交。

## 授权来源

- `FLOW-TASK-013`：`completed_independently_approved`，复审 `98 / C0-I0-M0`。
- `FLOW-TASK-014`：`completed_independently_approved`，复审 `98 / C0-I0-M0`。
- `SKILL-CLOSEOUT-001-T01`：用户批准实施，独立评审 `99 / C0-I0-M0`。
- 用户此前已授权按最小路径本地提交并继续后续任务；远端动作仍未授权。

## 允许提交

- `skills/api-design/SKILL.md`
- `skills/document-templates/SKILL.md`
- `skills/document-templates/references/test-environment-template.md`
- `skills/verification-before-completion/SKILL.md`
- `skills/webapp-testing/SKILL.md`
- `tests/test_project_test_governance.py`
- `skills/project-memory/SKILL.md`
- `skills/project-memory/references/session-start-checklist.md`
- `skills/project-memory/references/current-state-update-checklist.md`
- `tests/test_project_memory_skill.py`
- `.factory/memory/current-state.md` 的 T01 两行
- `docs/06-delivery/test-plan.md` 的 FLOW-TASK-013 hunk
- `.factory/workitems/SKILL-CLOSEOUT-001/**`
- `.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-013.md`
- `.factory/workitems/FLOW-CONTRACT-001/evidence/FLOW-TASK-012-review-fix-verification.md`
- `.factory/workitems/FLOW-CONTRACT-001/reviews/FLOW-TASK-012-independent-rereview-iteration-3.md`
- `.factory/workitems/FLOW-CONTRACT-001/reports/FLOW-TASK-012-implementer-report.md`
- `.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-IMPLEMENT-001-R002-post-release-verification.md`
- `.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl` 中既有的
  `FLOW_TASK_012_COMPLETED_INDEPENDENTLY_APPROVED` 单条事件

## 明确排除

- `docs/06-delivery/test-plan.md` 的 `PROJECT-ARTIFACTS-001` 候选修订。
- `skills/writing-plans/**`。
- 其他 Skill、测试、memory、WorkItem、产品代码和远端动作。

## 验证

- T01 两组定向回归。
- 5 个目标 Skill quick validation。
- Ruff、JSONL、diff check。
- 暂存快照必须只含允许范围；共享测试计划不得含
  `PROJECT-ARTIFACTS-001` 候选修订。
