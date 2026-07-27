# TASK-006 Integration Verification

## 目标

整合并行子任务结果，运行目标验证，输出本轮状态。

## 允许修改

- 仅修正前五个任务产生的冲突或测试失败。

## 验收

- `uv run pytest tests/test_task_workflow_semantics.py tests/test_black_box_workflow_eval.py tests/test_writing_plans_skill.py tests/test_execution_workflow_skills.py tests/test_bug_fix_root_cause_skill_rules.py tests/test_requirements_engineering_skill.py`
- `uv run ruff check tests/test_task_workflow_semantics.py tests/test_black_box_workflow_eval.py tests/test_writing_plans_skill.py tests/test_execution_workflow_skills.py tests/test_bug_fix_root_cause_skill_rules.py tests/test_requirements_engineering_skill.py`
- 不混入无关脏改动。

## 状态

ready_for_review
