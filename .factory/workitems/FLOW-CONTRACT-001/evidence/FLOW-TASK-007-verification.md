# FLOW-TASK-007 验证证据

- Work item：`FLOW-CONTRACT-001`
- Task：`FLOW-TASK-007`
- Actor：Codex
- 时间：2026-07-06T20:49:25+08:00
- 状态：`ready_for_review`

## 队列确认

- `FLOW-TASK-006` 已由用户确认 `human_approved`。
- `.factory/workitems/FLOW-CONTRACT-001/implementation-queue.md` 已进入 `FLOW-TASK-007`。
- 本轮只实施 `FLOW-TASK-007`，未实施 `FLOW-TASK-008` 或后续任务。

## 改动范围

- `skills/writing-plans/SKILL.md`
- `skills/writing-plans/references/workitem-plan-template.md`
- `skills/writing-plans/references/task-brief-template.md`
- `tests/test_writing_plans_skill.py`

## Red

命令：

```bash
uv run pytest tests/test_writing_plans_skill.py
```

结果：

```text
1 failed, 3 passed
```

失败点：

- `writing-plans` 缺少“计划只能生成候选执行输入，不执行代码”口径。
- 计划模板和任务 brief 缺设计方案、接口设计、UI 或 `N/A`、测试设计、开发、单测、review、集成测试。
- 缺“缺测试设计则失败”“UI 写 `N/A` 但无原因则失败”“发现占位语则失败”断言。

Exit code：`1`

## Green

命令：

```bash
uv run pytest tests/test_writing_plans_skill.py
```

结果：

```text
4 passed
```

Exit code：`0`

## 附加检查

```text
uv run ruff check tests/test_writing_plans_skill.py
All checks passed!
Exit code: 0
```
