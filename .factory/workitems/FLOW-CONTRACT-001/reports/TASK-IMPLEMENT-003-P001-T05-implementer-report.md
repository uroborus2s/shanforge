# T05 实现报告：异步同步、缓存维护与资料迁移

## 结果

已交付独立 `ProjectStateSyncQueuePort`、SQLite queue/store/worker、同步命令、登记式 cache maintenance 和可回滚迁移 preparer。主会话只做快速 enqueue；后台 worker 负责索引、站点、memory 状态和可选提交动作，未授权提交以成功处置结束。

## 边界

- 不修改冻结候选 `TASK-IMPLEMENT-002-R001`。
- 不提交 SQLite、HTML、cache 或 runtime queue。
- 不创建常驻 watcher，不把同步失败回滚为业务状态。
- 清理只处理 registry 中登记的 cache root。

## 产物

- `src/application/project_knowledge/sync_service.py`
- `src/settings/project_knowledge/sync_store.py`
- `src/settings/project_knowledge/sync_worker.py`
- `src/settings/project_knowledge/maintenance.py`
- `src/settings/project_knowledge/migration.py`
- `tests/test_project_state_sync.py`
- `tests/test_project_knowledge_maintenance.py`
- `tests/test_project_knowledge_migration.py`

作者状态：`ready_for_review`。
