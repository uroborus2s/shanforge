# FLOW-TASK-009 验证证据

- 工作项：`FLOW-CONTRACT-001`
- 任务：`FLOW-TASK-009`
- 状态：`ready_for_review`
- 时间：2026-07-06 22:08:18 +08:00

## 范围

- `skills/requesting-code-review/SKILL.md`
- `skills/receiving-code-review/SKILL.md`
- `skills/verification-before-completion/SKILL.md`
- `tests/test_review_workflow_skills.py`
- `tests/test_verification_debugging_workflow_skills.py`

## Red

命令：

```bash
uv run pytest tests/test_review_workflow_skills.py tests/test_verification_debugging_workflow_skills.py
```

结果：

```text
2 failed, 11 passed
```

失败点：

- review 缺“作者自检不能 `approved`”和 N/A 必须由 reviewer 接受 / 拒绝的断言。
- verification 缺关闭前检查新鲜命令、exit code、输出和 evidence，以及 review / verification / human confirmation 分离断言。

## Green

命令：

```bash
uv run pytest tests/test_review_workflow_skills.py tests/test_verification_debugging_workflow_skills.py
```

结果：

```text
13 passed
```

## Lint

命令：

```bash
uv run ruff check tests/test_review_workflow_skills.py tests/test_verification_debugging_workflow_skills.py
```

结果：

```text
All checks passed!
```

## 结论

任务卡要求的验证已运行并通过。当前实现者状态为 `ready_for_review`，未进入 `FLOW-TASK-010`。
