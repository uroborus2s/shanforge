# T02 Source Registry、提取器与增量索引

## 工作项

- 工作项：`FLOW-CONTRACT-001`
- 任务：`TASK-IMPLEMENT-003-P001-T02`
- 状态：`ready_for_review`
- 上游：T01 schema/contract

## 目标

交付 allowlist registry、Markdown/JSON/JSONL/Python/Git 提取器、SourceContribution/v1 和 SQLite 单事务 generation 发布；未变来源解析数必须为 0。

## 允许修改

- `.factory/project-knowledge/*.json`
- `src/runtime/project_knowledge/`
- `src/application/project_knowledge/index_service.py`
- `src/settings/project_knowledge/sqlite_index.py`
- `src/settings/project_knowledge/source_registry.py`
- `tests/test_project_knowledge_extractors.py`
- `tests/test_project_knowledge_index.py`
- 当前任务 evidence/report/review/ledger 和记忆摘要

## 禁止修改

- HTML/PM/异步实现、正式文档、无关脏文件。

## 测试与验证

```bash
PYTHONPATH=src uv run pytest tests/test_project_knowledge_extractors.py tests/test_project_knowledge_index.py -q
```

必须覆盖 stable section 的 `document_id+section_id`、AST 符号、JSON Pointer、event UID、同 registry 多文件 concrete source、同实体多来源删除一源仍保留其余贡献、幽灵贡献删除、失败回滚、并发读与 cold rebuild。UI 为 N/A，因为本切片没有用户界面。实现者只能进入 `ready_for_review`。
