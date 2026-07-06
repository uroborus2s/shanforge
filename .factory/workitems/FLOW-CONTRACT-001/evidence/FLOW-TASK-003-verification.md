# FLOW-TASK-003 验证证据

- Work item：`FLOW-CONTRACT-001`
- Task：`FLOW-TASK-003`
- Actor：Codex
- 时间：2026-07-06T12:21:18+08:00
- 状态：`ready_for_review`

## 队列确认

- `.factory/workitems/FLOW-CONTRACT-001/implementation-queue.md` 标记下一任务为 `FLOW-TASK-003`。
- 本轮未实施 `FLOW-TASK-004` 或后续任务。

## 改动范围

- `skills/document-templates/SKILL.md`
- `skills/document-templates/references/repository-structure.md`
- `skills/document-templates/references/formal-document-template.md`
- `tests/test_sf_sp_010_documentation_navigation.py`

## Red

命令：

```bash
uv run pytest tests/test_sf_sp_010_documentation_navigation.py
```

结果：

```text
2 failed, 6 passed
```

失败点：

- `document-templates` 缺少新增正式文档同步 `docs/index.md` 或 `.factory/memory/doc-map.md` 的结构规则。
- 缺少 `skills/document-templates/references/formal-document-template.md`。

Exit code：`1`

## Green

命令：

```bash
uv run pytest tests/test_sf_sp_010_documentation_navigation.py
```

结果：

```text
8 passed
```

Exit code：`0`

## 附加检查

```text
uv run ruff check tests/test_sf_sp_010_documentation_navigation.py
All checks passed!
Exit code: 0
```

```text
git diff --check -- <FLOW-TASK-003 touched tracked files>
Exit code: 0
```

```text
python3 -c '<parse .factory/workitems/FLOW-CONTRACT-001/ledger.jsonl as JSONL>'
ledger jsonl ok
Exit code: 0
```

## 未运行项

- 未运行 `docs-stratego source validate`：`FLOW-TASK-003` 任务卡指定验证命令为 `uv run pytest tests/test_sf_sp_010_documentation_navigation.py`。
