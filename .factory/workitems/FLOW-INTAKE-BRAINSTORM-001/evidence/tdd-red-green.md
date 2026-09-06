# TDD Red/Green

## RED

- Command: `uv run pytest -q tests/test_task_workflow_semantics.py tests/test_black_box_workflow_eval.py`
- Exit: `1`
- Result: `2 failed`，缺少轻量新项目分析仍进入无写入头脑风暴的入口合同与黑盒对照文本。

## GREEN

- Command: `uv run pytest -q tests/test_task_workflow_semantics.py tests/test_black_box_workflow_eval.py`
- Exit: `0`
- Result: `23 passed`
- Command: `uv run ruff check tests/test_task_workflow_semantics.py tests/test_black_box_workflow_eval.py`
- Exit: `0`，`All checks passed!`
- Command: `git diff --check`
- Exit: `0`

## 范围

- 修改 4 个授权文件。
- 未修改 `skills/brainstorming/SKILL.md`，未扩大范围。
- worker 未暂存、提交或执行远端动作。

