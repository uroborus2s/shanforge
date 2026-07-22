# T05 异步同步、有界维护与资料迁移

## 工作项

- 工作项：`FLOW-CONTRACT-001`
- 任务：`TASK-IMPLEMENT-003-P001-T05`
- 状态：`ready_for_review`
- 上游：T01–T04、R009 独立 project-knowledge queue；不依赖冻结 system-task 候选

## 目标

交付不修改冻结 system-task 候选的独立 `PROJECT_STATE_SYNC` durable queue/worker、50 transition 模型、有界 cache/Memory 维护和 Catalog/旧 PM 资料 dry-run + apply 迁移；不阻塞主会话，不把生成物提交 Git。

## 允许修改

- `src/application/project_knowledge/sync_service.py`
- `src/settings/project_knowledge/sync_worker.py`
- `src/settings/project_knowledge/sync_store.py`
- `src/settings/project_knowledge/maintenance.py`
- `src/settings/project_knowledge/migration.py`
- `src/access/project_cli.py`（只增加 `project sync enqueue` parser/dispatch）
- `src/settings/composition/project_knowledge.py`（只注入独立 queue port）
- `.gitignore`
- `.factory/cache/project-knowledge/migration/<job_id>/after-images/`（唯一 prepare 写入根，生成且不提交 Git）
- `docs/05-design/ai-sdlc-catalog.source.json`（只读迁移输入，T05 不删除）
- `docs/05-design/ai-sdlc-catalog.manifest.json`（只读迁移输入，T05 不删除）
- `.factory/pm/README.md`、`project-brief.md`、`team-raci.md`、`milestones.md`、`wbs.md`、`risk-register.jsonl`、`communication-plan.md`、`meeting-notes/*.md`、`status-reports/*.md`、`change-register.jsonl`、`closure-report.md`、`dashboard.md`（只读迁移输入，T05 不删除）
- `tests/test_project_state_sync.py`
- `tests/test_project_knowledge_maintenance.py`
- `tests/test_project_knowledge_migration.py`
- 当前任务 evidence/report/review/ledger 和记忆摘要

## 禁止修改

- Push/PR/Merge/部署、主工作树并发提交、未登记目录删除、直接丢弃未对账资料。

## 测试与验证

```bash
PYTHONPATH=src uv run pytest tests/test_project_state_sync.py tests/test_project_knowledge_maintenance.py tests/test_project_knowledge_migration.py -q
```

必须覆盖冻结 `SystemTaskKind`/store 的文件 Hash 不变、独立 queue、`project sync enqueue` CLI、50 transition 穷尽、coalesce/supersede、fencing、5 次重试、commit_not_authorized 收口、realpath/owner/legal hold、每个迁移源/目标/before Hash/rollback、T05 legacy 删除数为 0 和预期强关系 0 丢失。实现者只能进入 `ready_for_review`。
