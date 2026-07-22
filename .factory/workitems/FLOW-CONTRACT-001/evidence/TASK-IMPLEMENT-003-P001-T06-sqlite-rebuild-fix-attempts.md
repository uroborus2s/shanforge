# T06 SQLite rebuild 修复尝试证据

- 时间：2026-07-22T10:00:28Z
- 规则：`systematic-debugging` 三次失败后停止
- 当前结果：第三次定向回归 `2 passed / 1 failed`

## 尝试 1

- 实现 checkpoint、integrity、`journal_mode=DELETE` 和原子 replace。
- 结果：`0/3` 通过中的两个 rebuild 用例在临时库 journal 切换处失败；崩溃点旧库保留用例通过。
- 新证据：临时库还有未关闭连接。

## 尝试 2

- 显式关闭 composition 的 PM projection/progress snapshot 连接。
- 结果：仍为 `1 passed / 2 failed`。
- 新证据：`SQLiteProjectKnowledgeIndex` 与 query store 的 `with connection` 也只管理事务，不关闭连接。

## 尝试 3

- 索引和查询 provider 统一改为 `contextlib.closing`，写路径显式 commit。
- 结果：`2 passed / 1 failed`。
- 已通过：
  - 活动 reader 时严格 `CONCURRENT_WRITER / exit 7`，旧 generation 保留。
  - `before_replace` 注入失败时旧数据库保持可读。
- 剩余失败：stale sidecar 用例的测试夹具自身使用：

```python
with sqlite3.connect(database) as connection:
    ...
```

该上下文退出只 commit/rollback，不 close。夹具因此保留了一个活动连接；实现按照已批准方案正确拒绝 rebuild 并返回 exit 7。失败栈明确停在正式旧库 `PRAGMA journal_mode=DELETE`，不是临时库。

## Hash

- `sqlite_index.py`: `f831a43a0e052b186beffacac12ec996b80262b3c386102681812aee5766c452`
- `query_store.py`: `760fe78f0d5c7c9359bd000f396528666a8b09dd141a6b64ea5d2c17c9591c87`
- `composition/project_knowledge.py`: `a853776096de350ccac0ddd9a408782ff90f2b330a918736786498fab7ebcef7`
- `test_project_knowledge_integration.py`: `74ad08b1d1dde69d5da42b2a03241780414ad7da3c2a7468ad01fc8297ee6118`

## 下一步请求

不再修改生产实现。只把 stale-sidecar 测试夹具的连接改为 `closing(sqlite3.connect(...))`，明确表达“准备完成后连接已关闭”，再运行定向回归。若仍失败，则升级为架构决策，不继续追加补丁。

## 人工授权后的夹具复验

- 用户已确认只修正测试夹具连接关闭方式。
- 复验结果仍为 `2 passed / 1 failed`，但生产 rebuild 不再报锁。
- 唯一失败发生在夹具前置断言：连接显式关闭后，SQLite 自动删除了空 `-wal/-shm`，因此夹具没有制造出它声称要测试的 destination-sidecar 前置状态。
- 失败发生在第二次 rebuild 调用之前；没有新的生产实现失败证据。
- 按既定停止边界，不继续修改夹具，升级为架构/测试策略选择。
