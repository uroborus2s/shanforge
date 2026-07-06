# FLOW-TASK-007 实现报告

- Work item：`FLOW-CONTRACT-001`
- Task：`FLOW-TASK-007`
- Actor：Codex
- 时间：2026-07-06T20:49:25+08:00
- 状态：`ready_for_review`

## 目标

让 `writing-plans` 的任务模板强制包含设计方案、接口设计、UI 或 N/A、测试设计、开发、单测、review 和集成测试。

## 实现

- 在 `skills/writing-plans/SKILL.md` 明确计划只能生成候选执行输入，不执行代码。
- 在 `writing-plans` 默认流程中要求每个任务包含设计方案、接口设计、UI 或 `N/A`、测试设计、开发、单测、review 和集成测试。
- 在 `workitem-plan-template.md` 增加任务切片字段和失败断言。
- 在 `task-brief-template.md` 增加实施步骤字段和失败断言。
- 在 `tests/test_writing_plans_skill.py` 增加结构测试，覆盖任务卡要求。

## 范围控制

- 未修改 `FLOW-TASK-008` 或后续任务相关 skill。
- 未恢复旧中心命令、动作注册表、`factory-*` 或旧全局流程脚本。
- 未让 `writing-plans` 执行代码。
- 未提交 Git。

## 验证

- Red：`uv run pytest tests/test_writing_plans_skill.py` -> `1 failed, 3 passed`，exit code `1`。
- Green：`uv run pytest tests/test_writing_plans_skill.py` -> `4 passed`，exit code `0`。
- `uv run ruff check tests/test_writing_plans_skill.py` -> `All checks passed!`，exit code `0`。

## 产物

- Evidence：`.factory/workitems/FLOW-CONTRACT-001/evidence/FLOW-TASK-007-verification.md`
- Review checkpoint：`.factory/workitems/FLOW-CONTRACT-001/reviews/FLOW-TASK-007-review-checkpoint.md`

## 下一状态

实现者状态只到 `ready_for_review`，需要独立 review。
