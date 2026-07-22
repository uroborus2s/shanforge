# T06 SQLite rebuild 根因调查证据

- 时间：2026-07-22T09:41:44Z
- 状态：`root_cause_found`
- 调查范围：只复现、读取状态和建立 fresh-path 对照；未修改 rebuild 行为。

## 稳定复现

命令：

```bash
PYTHONPATH=src .venv/bin/python -m settings.composition.project_knowledge \
  project snapshot --html --rebuild --profile local-owner --json
```

结果：CLI exit `6`，`sqlite3.OperationalError: disk I/O error`。绕过 CLI 的完整堆栈把失败定位到 rebuild 返回后，`SQLiteSiteDataStore.current_input_token()` 首次打开刚替换的正式数据库时。

## 边界状态

失败目录同时存在：

```text
project-knowledge.sqlite3
project-knowledge.sqlite3-shm
project-knowledge.sqlite3-wal
project-knowledge.sqlite3.rebuild-shm
```

`rebuild()` 只执行 `temporary.unlink(missing_ok=True)` 和 `os.replace(temporary, database_path)`；没有把 WAL/SHM 作为同一个 SQLite 数据库状态处理。索引 provider 每次连接又固定执行 `PRAGMA journal_mode = WAL`。

## 对照实验

在全新的 `/tmp/shanforge-sqlite-rebuild-diagnosis.a1OI1t/fresh.sqlite3` 路径运行相同 registry、extractor 和 index service：

```text
source_count=456
parsed_count=456
changed=True
目录最终只有 fresh.sqlite3
```

冷构建成功，证明来源、extractor、schema 和数据量不是触发条件。已有 rebuild/destination sidecar 状态才是差异。

## 数据流反向追踪

- 症状：新 rebuild 已返回，但随后的只读连接报 `disk I/O error`。
- 直接原因：正式主文件被 `os.replace` 换成另一个 SQLite 数据库后，目标路径原数据库的 `-wal/-shm` 仍留在同名位置；主文件与 sidecar 不是同一 WAL identity。
- 上一层调用：`snapshot()` 调用 `rebuild()`，随后创建 `SQLiteSiteDataStore` 读取 current generation。
- 继续向上追踪：`rebuild()` 把 WAL 模式 SQLite 当成单文件制品，只替换主文件；`SQLiteProjectKnowledgeIndex._connect()` 则明确启用 WAL。
- 源头：原子发布模型与 SQLite WAL 多文件持久状态模型不一致。

## Hash 证据

- `src/settings/composition/project_knowledge.py`: `f248e0c89cea5c730eeafaa7650c138a11f3b5cbe1206d25b3c0abbf305417ad`
- `src/settings/project_knowledge/sqlite_index.py`: `c667b8fa2140667db5b96482a678113c62c5a1cc2016ed172126e56ace17ce5d`
