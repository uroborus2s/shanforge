# T06 SQLite rebuild 修复方案

## 状态

- 根因：已由 `uroborus` 于 2026-07-22 确认。
- 方案状态：`ready_for_human_confirmation`
- 修复尚未执行。

## 选择方案

保留当前稳定入口 `.factory/index/project-knowledge.sqlite3`，不引入新的数据库目录指针层。正常增量刷新继续使用 WAL；只有 rebuild 的原子切换窗口把旧库和临时库收口为各自独立、可替换的单文件 SQLite 制品。

### 为什么选择它

- 不改变 CLI、查询路径、source registry、39 张表或 generation 身份。
- 正常 refresh 仍保留 WAL 的读写并发能力。
- rebuild 切换前，SQLite 自己通过锁和 journal mode 切换证明不存在冲突 reader/writer；无法取得安全切换条件时失败关闭并保留旧库。
- 比 immutable database pointer 方案少一套 generation 目录、pointer、reader lease 和维护协议，符合当前第一版范围。

## 精确实施步骤

### 1. 先增加失败回归

在 `tests/test_project_knowledge_integration.py` 增加：

1. 预置合法旧库及其 `-wal/-shm`，再预置上次失败遗留的 `.rebuild`、`.rebuild-wal`、`.rebuild-shm`；执行 rebuild 后首次只读查询必须成功。
2. 临时库在切换前必须通过 `PRAGMA integrity_check`，且 `journal_mode=delete`，临时 sidecar 为 0。
3. 旧库存在活动冲突连接时，切换返回 `CONCURRENT_WRITER / exit 7`，旧 generation 和旧站点保持可读。
4. 在 `before_replace` 注入失败时，旧库保持原 Hash 和 current generation；不得回退为“报告成功”。

### 2. 临时路径只清理登记生成物

`rebuild()` 开始时仅清理以下精确路径：

```text
.factory/index/project-knowledge.sqlite3.rebuild
.factory/index/project-knowledge.sqlite3.rebuild-wal
.factory/index/project-knowledge.sqlite3.rebuild-shm
.factory/index/project-knowledge.sqlite3.rebuild-journal
```

清理前验证 realpath 仍位于 `.factory/index/` 且文件名等于 allowlist；不使用 glob，不触碰正式数据库。

### 3. 临时库收口为单文件

冷构建和 PM 投影完成后，在临时库连接上依次执行：

```text
PRAGMA wal_checkpoint(TRUNCATE)
PRAGMA integrity_check
PRAGMA journal_mode=DELETE
```

只有 checkpoint 完成、integrity 为 `ok`、journal mode 确认为 `delete` 且连接关闭后不存在临时 sidecar，才允许进入切换阶段。

### 4. 正式旧库取得安全切换条件

若正式库存在：

1. 用短 busy timeout 打开正式库。
2. 执行 `PRAGMA wal_checkpoint(TRUNCATE)`。
3. 执行 `PRAGMA journal_mode=DELETE`，让 SQLite 自己取得切换 journal mode 所需的排他条件。
4. 任一步出现 `busy/locked`，映射为 `CONCURRENT_WRITER / exit 7`，关闭连接并保留旧库，不删除正式 sidecar、不替换主文件。
5. 成功后关闭连接；确认正式 `-wal/-shm` 已由 SQLite 收口或为空，再进入原子替换。

活动 reader/writer 不会被强制断开；系统选择拒绝本次 rebuild，由后续重试完成。

### 5. 单文件原子替换

旧库和临时库都已是自洽单文件后，执行一次：

```python
os.replace(temporary, database_path)
```

崩溃语义：

- replace 前崩溃：旧库仍完整。
- replace 后崩溃：新库已完整。
- 下次增量 refresh 打开 writer 时可重新启用 WAL；只读 snapshot 不创建 sidecar。

### 6. 错误与回执

- 冲突锁：exit `7`，`failure_code=CONCURRENT_WRITER`。
- 临时库损坏或 checkpoint/journal 收口失败：exit `6`，`INDEX_CORRUPT_OR_REBUILD_REQUIRED`。
- 所有失败都保留上一有效 index/site，并在 receipt 标记失败阶段；不吞错、不自动把旧库冒充新 generation。

## 修改范围

- `src/settings/project_knowledge/sqlite_index.py`：增加 SQLite 自检、checkpoint 与单文件收口能力。
- `src/settings/composition/project_knowledge.py`：精确临时 sidecar 清理、安全切换编排和 exit 7 映射。
- `tests/test_project_knowledge_integration.py`：根因回归、锁冲突和崩溃点。
- 当前任务 evidence/report/ledger。

不修改冻结 `TASK-IMPLEMENT-002-R001`，不修改 39 表 schema，不迁移正式文档，不执行 Git 提交。

## 验收命令

```bash
PYTHONPATH=src uv run pytest tests/test_project_knowledge_integration.py \
  tests/test_project_knowledge_index.py tests/test_project_knowledge_pm.py \
  tests/test_project_site_renderer.py tests/test_project_cli.py -q
PYTHONPATH=src .venv/bin/python -m settings.composition.project_knowledge \
  project snapshot --html --rebuild --profile local-owner --json
PYTHONPATH=src .venv/bin/python -m settings.composition.project_knowledge \
  project snapshot --html --profile local-owner --json
uv run ruff check <本次修改文件>
uv run mypy <本次修改源码>
```

通过条件：真实 rebuild exit 0，首次读取成功，PM 投影有当前行，第二次 snapshot `cache_hit=true`，预存 sidecar 回归通过，冲突连接严格 exit 7，旧库保留。
