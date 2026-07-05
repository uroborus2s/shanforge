# SF-SP-009 Review Response

## F1：评分公式和归一化缺失

- 处理：Fixed
- 修改：`skills/using-shanforge/references/black-box-flow-eval.md` 增加计算公式，明确每条 critical assertion 按 `2/1/0` 计分、最高可能得分、实际得分和百分制总分。
- 验证：`tests/test_black_box_workflow_eval.py` 已断言公式文本。

## F2：结构测试偏弱

- 处理：Fixed
- 修改：`tests/test_black_box_workflow_eval.py` 增加结构断言，覆盖每个场景必须有期望行为、critical assertions、评分说明、至少 3 条 critical assertion，以及 evidence 字段完整性。
- 验证：目标测试从加严后 `3 failed, 3 passed` 修复到 `6 passed`。

## F3：正式计划范围口径残留

- 处理：Fixed
- 修改：`docs/04-project-development/05-development-process/superpowers-workflow-integration-plan.md` 将 `SF-SP-009` 任务表从 4 类场景更新为 6 类场景。
- 验证：`tests/test_black_box_workflow_eval.py` 覆盖计划状态文本。

## 验证命令

- `.venv/bin/pytest tests/test_black_box_workflow_eval.py` -> `6 passed`
- `.venv/bin/ruff check tests/test_black_box_workflow_eval.py` -> passed
- `python3 skills/skill-creator/scripts/quick_validate.py skills/using-shanforge` -> passed
- `.venv/bin/pytest tests/test_black_box_workflow_eval.py tests/test_execution_workflow_skills.py tests/test_review_workflow_skills.py tests/test_verification_debugging_workflow_skills.py tests/test_pr_commit_workflow_rules.py` -> `28 passed`
- `git diff --check` -> passed
