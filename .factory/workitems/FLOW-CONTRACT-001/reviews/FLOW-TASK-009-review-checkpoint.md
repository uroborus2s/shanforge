# FLOW-TASK-009 Review Checkpoint

- 工作项：`FLOW-CONTRACT-001`
- 任务：`FLOW-TASK-009`
- 状态：`ready_for_review`
- 时间：2026-07-06 22:08:18 +08:00

## Review 输入

- 任务卡：`.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-009.md`
- Evidence：`.factory/workitems/FLOW-CONTRACT-001/evidence/FLOW-TASK-009-verification.md`
- Implementer report：`.factory/workitems/FLOW-CONTRACT-001/reports/FLOW-TASK-009-implementer-report.md`
- 相关文件：
  - `skills/requesting-code-review/SKILL.md`
  - `skills/receiving-code-review/SKILL.md`
  - `skills/verification-before-completion/SKILL.md`
  - `tests/test_review_workflow_skills.py`
  - `tests/test_verification_debugging_workflow_skills.py`

## 自检

- 只实施 `FLOW-TASK-009`。
- review 已明确作者自检不能 `approved`。
- review 已明确 N/A 必须由 reviewer 接受或拒绝。
- verification 已明确关闭前必须有新鲜命令、exit code、输出和 evidence。
- review、verification、human confirmation 三者不能互相替代。
- 实现者未写 `approved`，当前仅为 `ready_for_review`。

## 验证

- `uv run pytest tests/test_review_workflow_skills.py tests/test_verification_debugging_workflow_skills.py` -> `13 passed`
- `uv run ruff check tests/test_review_workflow_skills.py tests/test_verification_debugging_workflow_skills.py` -> `All checks passed!`

## Reviewer 关注点

- N/A gate 是否足以防止未经 reviewer 接受的 N/A 通过 review。
- 关闭 gate 是否足以防止无 evidence、无新鲜命令或无 exit code 的完成声明。
- 是否误触 `FLOW-TASK-010` 或后续范围。

## 下一门

需要独立 review。实现者不得自批 `approved`。
