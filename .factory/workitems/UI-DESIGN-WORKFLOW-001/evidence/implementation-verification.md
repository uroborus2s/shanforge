# 实现验证

- WorkItem：`UI-DESIGN-WORKFLOW-001`
- TaskCard：`UI-DESIGN-WORKFLOW-001-T01`
- 状态：`ready_for_review`

## TDD

- RED：新增语义断言后，`2 failed, 11 passed`；失败原因是通用关键页面确认门和互斥路由文字尚不存在。
- GREEN：`uv run pytest tests/test_ui_ux_pro_max_skill.py tests/test_task_workflow_semantics.py -q`，结果 `21 passed`。

## 静态检查

- `uv run ruff check tests/test_ui_ux_pro_max_skill.py`：通过。
- `uv run python /Users/uroborus/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/ui-ux-pro-max`：`Skill is valid!`
- `git diff --check`：通过。

## 修改范围

- `skills/ui-ux-pro-max/references/design-workflow-and-deliverables.md`
- `skills/using-shanforge/SKILL.md`
- `tests/test_ui_ux_pro_max_skill.py`

未修改 `art-asset-pipeline`、移动端高保真规则、依赖、脚本、模板或设计资产。
