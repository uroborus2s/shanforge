# T02 实现者报告

## 产出

- 稳定 source registry：只扫描 allowlist roots/globs，一行一个具体文件，realpath 越界失败关闭。
- 纯 Markdown/JSON/JSONL/Python/Git 提取器，只输出 `SourceContribution/v1` 允许元数据。
- SQLite WAL 增量索引：Hash 未变复用贡献，只有变化才用 `BEGIN IMMEDIATE` 发布新 generation。
- 同实体多来源按 authority rank 合并，同级强定义冲突阻断发布。

## 范围自检

- 未修改 HTML/PM/异步实现或正式 docs。
- 未修改冻结 `TASK-IMPLEMENT-002-R001`。
- `.factory/project-knowledge/*.json` 是稳定配置；SQLite 仍为可删除投影。
