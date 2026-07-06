# FLOW-TASK-005 实现报告

- Work item：`FLOW-CONTRACT-001`
- Task：`FLOW-TASK-005`
- Actor：Codex
- 时间：2026-07-06T20:19:16+08:00
- 状态：`ready_for_review`

## 目标

让 `using-shanforge` 成为四类场景、baseline work item、gate 和关闭规则的唯一路由 owner。

## 实现

- 在 `skills/using-shanforge/SKILL.md` 增加场景路由与 baseline gate。
- 固定四类场景 ID：`new_project`、`add_requirement`、`change_requirement`、`fix_bug`。
- 固定 baseline work item 规则：领域划分、总体架构、数据库基线、API 基线和整体 UI 设计属于 baseline work item。
- 固定缺 evidence、review、verification、人工确认或最终审计问题报告时阻塞关闭、提交和进入下一阶段。
- 扩展人工确认包，要求输出最终审计问题报告、阻塞问题、已修复问题、残留风险和验证证据，不能只输出评分。
- 在 `black-box-flow-eval.md` 增加 5 个 FLOW-CONTRACT 场景，覆盖新项目、增需、变需、修 bug 和缺 evidence 阻塞关闭。
- 更新 `tests/test_black_box_workflow_eval.py`，用结构断言固定上述规则，并同步既有 `SF-SP-009` 计划口径。

## 范围控制

- 未修改 `FLOW-TASK-006` 或后续任务相关 skill。
- 未恢复旧中心命令、动作注册表、`factory-*` 或旧全局流程脚本。
- 未让 `using-shanforge` 写需求、代码或评审结论；它仍只负责流程路由、gate 和确认包。
- 未提交 Git。

## 验证

- Red：`uv run pytest tests/test_black_box_workflow_eval.py` -> `2 failed, 5 passed`，exit code `1`。
- Green：`uv run pytest tests/test_black_box_workflow_eval.py` -> `7 passed`，exit code `0`。
- `uv run ruff check tests/test_black_box_workflow_eval.py` -> `All checks passed!`，exit code `0`。

## 产物

- Evidence：`.factory/workitems/FLOW-CONTRACT-001/evidence/FLOW-TASK-005-verification.md`
- Review checkpoint：`.factory/workitems/FLOW-CONTRACT-001/reviews/FLOW-TASK-005-review-checkpoint.md`

## 下一状态

实现者状态只到 `ready_for_review`，需要独立 review。
