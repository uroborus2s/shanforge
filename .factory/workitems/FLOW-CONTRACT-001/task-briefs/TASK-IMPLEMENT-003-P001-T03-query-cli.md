# T03 稳定定位、关系图与查询 CLI

## 工作项

- 工作项：`FLOW-CONTRACT-001`
- 任务：`TASK-IMPLEMENT-003-P001-T03`
- 状态：`ready_for_review`
- 上游：T01、T02

## 目标

交付 find/show/trace/context/index check|refresh|rebuild 的 application 用例、稳定退出码、JSON receipt 和仓内可直接执行的 composition CLI。

## 允许修改

- `src/application/project_knowledge/query_service.py`
- `src/access/project_cli.py`
- `src/settings/composition/project_knowledge.py`
- `src/settings/project_knowledge/query_store.py`
- `tests/test_project_knowledge_query.py`
- `tests/test_project_cli.py`
- 当前任务 evidence/report/review/ledger 和记忆摘要

## 禁止修改

- CLI 内直接访问 SQLite/文件系统、无关脏文件、远端动作。

## 测试与验证

```bash
PYTHONPATH=src uv run pytest tests/test_project_knowledge_query.py tests/test_project_cli.py -q
```

必须覆盖 alias 环、0/多 locator、4 文件/32 KiB 预算、同边多来源、stable exit code 和 receipt。CLI UI 只提供简短中文摘要与 JSON，不建立 TUI。实现者只能进入 `ready_for_review`。
