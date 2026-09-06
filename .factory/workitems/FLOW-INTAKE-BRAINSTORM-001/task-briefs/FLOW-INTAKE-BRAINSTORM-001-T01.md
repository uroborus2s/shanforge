# FLOW-INTAKE-BRAINSTORM-001-T01

## 目标

用最小合同与回归用例修复新项目初步分析跳过头脑风暴的问题。

## 允许修改

- `skills/using-shanforge/SKILL.md`
- `skills/using-shanforge/references/black-box-flow-eval.md`
- `tests/test_task_workflow_semantics.py`
- `tests/test_black_box_workflow_eval.py`
- `.factory/workitems/FLOW-INTAKE-BRAINSTORM-001/`

## 禁止动作

- 不修改 `skills/brainstorming/SKILL.md`，除非先证明现有合同无法承载修复并停止升级。
- 不修改其他 work item、正式产品文档或历史 evidence。
- 不新增依赖、脚本、分类器或兼容兜底。
- 不提交、不推送、不创建 PR。

## TDD 验收

1. 先补回归断言并运行，确认因缺少新合同而失败。
2. 最小修改总控入口和黑盒场景，使回归由红转绿。
3. 运行：
   - `uv run pytest -q tests/test_task_workflow_semantics.py tests/test_black_box_workflow_eval.py`
   - `uv run ruff check tests/test_task_workflow_semantics.py tests/test_black_box_workflow_eval.py`
   - `git diff --check`

## 路由

- workflow_id: `execution-workflow`
- write_policy: `source_or_test_write`
- task_complexity: `standard`
- risk_level: `medium`
- execution_authorized: `true`
- execution_model: `gpt-5.6-terra`
- requested_reasoning_effort: `medium`
- current_gate: `closed`

