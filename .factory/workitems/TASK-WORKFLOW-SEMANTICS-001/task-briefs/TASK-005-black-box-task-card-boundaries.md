# TASK-005 Black Box Task Card Boundaries

## 目标

补黑盒 eval 场景，锁住“直接分析不建卡”和“系统拆分出的子分析必须建卡”。

## 允许修改

- `skills/using-shanforge/references/black-box-flow-eval.md`
- `tests/test_black_box_workflow_eval.py`
- `tests/test_task_workflow_semantics.py`

## 验收

- `FLOW-S6-direct-analysis-no-task-card` 覆盖直接分析。
- `FLOW-S7-decomposed-analysis-requires-task-card` 覆盖系统拆分子任务。
- 两个场景都要求核心输出契约一致。

## 状态

ready_for_review
