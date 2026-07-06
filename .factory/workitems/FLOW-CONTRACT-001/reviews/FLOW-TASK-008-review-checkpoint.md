# FLOW-TASK-008 Review Checkpoint

- 工作项：`FLOW-CONTRACT-001`
- 任务：`FLOW-TASK-008`
- 状态：`ready_for_review`
- 时间：2026-07-06 21:06:17 +08:00

## Review 输入

- 任务卡：`.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-008.md`
- Evidence：`.factory/workitems/FLOW-CONTRACT-001/evidence/FLOW-TASK-008-verification.md`
- Implementer report：`.factory/workitems/FLOW-CONTRACT-001/reports/FLOW-TASK-008-implementer-report.md`
- 相关文件：
  - `skills/executing-plans/SKILL.md`
  - `skills/subagent-driven-development/SKILL.md`
  - `tests/test_execution_workflow_skills.py`

## 自检

- 只实施 `FLOW-TASK-008`。
- 执行类 skill 已加入任务 gate。
- 缺设计、测试或 evidence 时阻塞的规则已加入并由测试固定。
- 子 agent 不决定下一步 skill 的规则已加入并由测试固定。
- 实现者未写 `approved`，当前仅为 `ready_for_review`。

## 验证

- `uv run pytest tests/test_execution_workflow_skills.py` -> `9 passed`
- `uv run ruff check tests/test_execution_workflow_skills.py` -> `All checks passed!`

## Reviewer 关注点

- gate 是否覆盖任务卡要求的设计、测试和 evidence 缺口。
- 子 agent 边界是否足以防止工作 skill 反向路由流程。
- 新增测试是否能阻止任务 gate 和不路由规则回退。
- 是否误触 `FLOW-TASK-009` 或后续范围。

## 下一门

需要独立 review。实现者不得自批 `approved`。
