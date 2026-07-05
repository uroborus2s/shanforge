# SF-SP-009 Review Fix Report

## 修复范围

- `skills/using-shanforge/references/black-box-flow-eval.md`
- `tests/test_black_box_workflow_eval.py`
- `docs/04-project-development/05-development-process/superpowers-workflow-integration-plan.md`
- `.factory/workitems/SF-SP-009/*`
- `.factory/memory/*`

## 修复内容

- 补齐黑盒 eval 评分公式：场景默认同权、每条 critical assertion 按 `2/1/0` 计分、最高可能得分、实际得分和百分制总分。
- 增强结构测试：每个场景必须有期望行为、critical assertions、评分说明和至少 3 条 critical assertion；证据格式必须包含实际分、最高分和归一化分。
- 同步正式计划任务表，将 SF-SP-009 从 4 类场景改为 6 类场景。

## 验证

- 加严测试红灯：`3 failed, 3 passed`
- 修复后目标测试：`6 passed`
- 邻近 workflow 回归：`28 passed`
- Ruff、skill validator、JSONL、`git diff --check` 均通过。

## 状态

`ready_for_re_review`
