# FLOW-TASK-006 实现报告

- Work item：`FLOW-CONTRACT-001`
- Task：`FLOW-TASK-006`
- Actor：Codex
- 时间：2026-07-06T20:37:18+08:00
- 状态：`ready_for_review`

## 目标

让 `project-memory` 明确 docs、work item、memory、PM 视图的事实源优先级，并固定 summary 不复制正式正文。

## 实现

- 在 `skills/project-memory/SKILL.md` 增加事实源优先级。
- 在 `relevance-gate.md` 和 `current-state-update-checklist.md` 固定 summary 边界：只写 ID、状态、当前 gate、关键约束和索引，不复制完整正文。
- 在 `.factory/memory/doc-map.md` 增加事实源优先级说明。
- 在 `tests/test_project_memory_skill.py` 增加结构测试，覆盖事实源优先级、summary 边界和 PM generated 非事实源。

## 范围控制

- 未修改 `FLOW-TASK-007` 或后续任务相关 skill。
- 未恢复旧中心命令、动作注册表、`factory-*` 或旧全局流程脚本。
- 未把 `.factory/pm/generated/status-dashboard.html` 作为事实源。
- 未提交 Git。

## 验证

- Red：`uv run pytest tests/test_project_memory_skill.py` -> `1 failed, 4 passed`，exit code `1`。
- Green：`uv run pytest tests/test_project_memory_skill.py` -> `5 passed`，exit code `0`。
- `uv run ruff check tests/test_project_memory_skill.py` -> `All checks passed!`，exit code `0`。

## 产物

- Evidence：`.factory/workitems/FLOW-CONTRACT-001/evidence/FLOW-TASK-006-verification.md`
- Review checkpoint：`.factory/workitems/FLOW-CONTRACT-001/reviews/FLOW-TASK-006-review-checkpoint.md`

## 下一状态

实现者状态只到 `ready_for_review`，需要独立 review。
