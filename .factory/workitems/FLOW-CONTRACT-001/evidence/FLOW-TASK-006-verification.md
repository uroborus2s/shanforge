# FLOW-TASK-006 验证证据

- Work item：`FLOW-CONTRACT-001`
- Task：`FLOW-TASK-006`
- Actor：Codex
- 时间：2026-07-06T20:37:18+08:00
- 状态：`ready_for_review`

## 队列确认

- `FLOW-TASK-005` 已由用户确认 `human_approved`。
- `.factory/workitems/FLOW-CONTRACT-001/implementation-queue.md` 已进入 `FLOW-TASK-006`。
- 本轮只实施 `FLOW-TASK-006`，未实施 `FLOW-TASK-007` 或后续任务。

## 改动范围

- `skills/project-memory/SKILL.md`
- `skills/project-memory/references/relevance-gate.md`
- `skills/project-memory/references/current-state-update-checklist.md`
- `.factory/memory/doc-map.md`
- `tests/test_project_memory_skill.py`

## Red

命令：

```bash
uv run pytest tests/test_project_memory_skill.py
```

结果：

```text
1 failed, 4 passed
```

失败点：

- `project-memory` 缺少事实源优先级。
- 缺少 `summary 不复制完整正文` 规则。
- 缺少 `PM generated 非事实源` 和不得把 `.factory/pm/generated/status-dashboard.html` 作为唯一事实源的断言。

Exit code：`1`

## Green

命令：

```bash
uv run pytest tests/test_project_memory_skill.py
```

结果：

```text
5 passed
```

Exit code：`0`

## 附加检查

```text
uv run ruff check tests/test_project_memory_skill.py
All checks passed!
Exit code: 0
```
