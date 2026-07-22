# T06 SQLite rebuild 根因报告

## 基本信息

- Work item：`FLOW-CONTRACT-001 / TASK-IMPLEMENT-003-P001-T06`
- 问题来源：真实仓 `project snapshot --html --rebuild` 集成验证
- 受影响路径：`src/settings/composition/project_knowledge.py`、`src/settings/project_knowledge/sqlite_index.py`
- 当前状态：`root_cause_found / human_confirmation_required`

## 现象

- Bug 症状：显式 rebuild 返回 exit 6；普通快照还能读取旧索引，但 PM 投影未激活。
- 稳定复现：连续两次真实仓 rebuild 均在新主文件第一次读取时触发 `sqlite3.OperationalError: disk I/O error`。
- 失败证据：`evidence/TASK-IMPLEMENT-003-P001-T06-sqlite-rebuild-investigation.md`。

## 调查

- 最近变化：T06 composition 新增 temporary database rebuild 后 `os.replace`。
- 可工作的相似实现：站点发布以 immutable build directory + symlink pointer 切换；全新 SQLite 路径冷构建也成功。
- 差异：站点切换的是完整 immutable 目录；SQLite rebuild 只切换主文件，同时 provider 使用 WAL 多文件状态。
- 边界证据：失败目录保留正式 `-wal/-shm` 与 rebuild `-shm`；fresh-path 对照只有完整主文件且可读。

## 根因

- 直接原因：`os.replace(temporary, database_path)` 替换 WAL 数据库主文件时，没有同步处理目标路径的 WAL/SHM sidecar，随后连接观察到不匹配的 WAL identity 并报 I/O error。
- 根源原因：设计中的“临时 SQLite 单文件原子替换”与实现启用的 SQLite WAL 多文件语义冲突。
- 最小假设：若在同一发布模型中保证切换单位是一个自洽的 SQLite 制品（而非只换 WAL 主文件），第一次只读连接应成功。
- 假设验证：全新路径的完整冷构建可读；仅有历史 sidecar 的目标路径稳定失败，假设成立。

## 拟议修复边界（尚未执行）

- 优先方案：rebuild 临时库使用非 WAL 的单文件发布格式，发布前对当前库完成受控 checkpoint/关闭，并将目标 sidecar 纳入明确的互斥切换协议；同时新增“预存 destination/rebuild sidecar”失败回归和首次读取断言。
- 若并发 reader 的无缝切换不能用上述协议证明，则升级为 immutable generation database + atomic current pointer，沿用站点发布模型。
- 不采用：吞掉 I/O error、失败后回退旧库、或删除错误后假装 rebuild 成功。

## 结论

- 根因是否明确：是。
- 是否允许修复：否；按 `systematic-debugging` Gate 等待人工确认根因，之后还需确认修复方案。
- 剩余风险：rebuild 未通过；T06 整体资格、浏览器验证、正式迁移和 Git 提交均未开始。
