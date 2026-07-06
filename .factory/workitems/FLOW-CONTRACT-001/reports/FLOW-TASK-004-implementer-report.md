# FLOW-TASK-004 实现报告

- Work item：`FLOW-CONTRACT-001`
- Task：`FLOW-TASK-004`
- Actor：Codex
- 时间：2026-07-06T20:00:58+08:00
- 状态：`ready_for_review`

## 目标

让 `requirements-engineering` 支持四类场景、需求版本、影响分析、领域模块映射和 baseline 变更建议。

## 实现

- 在 `skills/requirements-engineering/SKILL.md` 增加 `new_project`、`add_requirement`、`change_requirement`、`fix_bug` 场景规则。
- 增加需求版本规则、baseline 影响分析、领域模块映射和 baseline 变更建议。
- 在 `prd-template.md` 增加版本信息、版本历史、场景分类、领域模块映射和 baseline 变更建议字段。
- 在 `tests/test_requirements_engineering_skill.py` 增加场景和模板结构测试。
- 为通过任务卡指定验证，恢复 `tasks.summary.md` 中既有 Superpowers 人工确认短语。

## 范围控制

- 未修改 `FLOW-TASK-005` 或后续任务相关 skill。
- 未修改旧中心脚本。
- 未提交 Git。

## 验证

- Red：`uv run pytest tests/test_requirements_engineering_skill.py` -> `2 failed, 2 passed`，exit code `1`。
- Green：`uv run pytest tests/test_requirements_engineering_skill.py tests/test_superpowers_reference_migration.py` -> `8 passed`，exit code `0`。
- `uv run ruff check tests/test_requirements_engineering_skill.py tests/test_superpowers_reference_migration.py` -> `All checks passed!`，exit code `0`。

## 产物

- Evidence：`.factory/workitems/FLOW-CONTRACT-001/evidence/FLOW-TASK-004-verification.md`
- Review checkpoint：`.factory/workitems/FLOW-CONTRACT-001/reviews/FLOW-TASK-004-review-checkpoint.md`

## 下一状态

实现者状态只到 `ready_for_review`，需要独立 review。
