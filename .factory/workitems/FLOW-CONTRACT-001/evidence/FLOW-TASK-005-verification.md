# FLOW-TASK-005 验证证据

- Work item：`FLOW-CONTRACT-001`
- Task：`FLOW-TASK-005`
- Actor：Codex
- 时间：2026-07-06T20:19:16+08:00
- 状态：`ready_for_review`

## 队列确认

- `FLOW-TASK-004` 已由用户确认 `human_approved`。
- `.factory/workitems/FLOW-CONTRACT-001/implementation-queue.md` 已进入 `FLOW-TASK-005`。
- 本轮只实施 `FLOW-TASK-005`，未实施 `FLOW-TASK-006` 或后续任务。

## 改动范围

- `skills/using-shanforge/SKILL.md`
- `skills/using-shanforge/references/black-box-flow-eval.md`
- `tests/test_black_box_workflow_eval.py`

## Red

命令：

```bash
uv run pytest tests/test_black_box_workflow_eval.py
```

结果：

```text
2 failed, 5 passed
```

失败点：

- `using-shanforge` 缺少四类场景、baseline work item、缺 evidence 阻塞关闭、最终审计问题报告等流程契约断言。
- `tests/test_black_box_workflow_eval.py` 中既有 `SF-SP-009` 计划断言仍停在旧口径。

Exit code：`1`

补充加严后再次运行同一命令，曾继续暴露旧断言 `不新增中心脚本 gate` 与当前正式计划口径不一致；已修正为 `不新增仓库级流程主控脚本`。

## Green

命令：

```bash
uv run pytest tests/test_black_box_workflow_eval.py
```

结果：

```text
7 passed
```

Exit code：`0`

## 附加检查

```text
uv run ruff check tests/test_black_box_workflow_eval.py
All checks passed!
Exit code: 0
```
