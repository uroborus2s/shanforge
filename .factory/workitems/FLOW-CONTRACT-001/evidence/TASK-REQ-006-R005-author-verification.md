# TASK-REQ-006 R005 作者校验证据

## 范围

- 候选：`.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001-R005.md`
- 机器合同：`.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.contract.R005.json`
- 语义：R005 完整替代 R001–R004，不叠加解释。

## 文件 Hash

| 文件 | SHA-256 |
|---|---|
| R005 Markdown | `df688a2bc6846eff0b3bf78b431f8fe2497f5417182f6934ede2c99191e6286f` |
| R005 JSON 合同 | `9e304b72ea77637b1237e7fb140d630b5860e56390846805deb062b0be2670bf` |

## 机器校验

- JSON：`jq -e` 通过。
- 功能需求：16 条，ID 唯一，与机器合同顺序一致。
- NFR：11 条，ID 集合与机器合同一致。
- 验收标准：16 条功能需求均至少包含一条 AC。
- SQLite：知识核心 29 张，PM 投影 10 张，总计 39 张；FTS 虚拟表 2 张。
- Git 边界：合同明确生成 SQLite、FTS、地图、HTML 和 cache 不提交 Git。
- 候选隔离：合同明确排除 `TASK-IMPLEMENT-002-R001`。

## 作者自检结论

R005 已覆盖用户后续讨论形成的增量语义：三类代次/快照/指纹分离、稳定语义 locator、完整 39 表边界、十要素 137 字段、只读多页面站点、页面级 freshness、异步 `PROJECT_STATE_SYNC`、隔离 worktree/写租约、受控维护提交及现有资料迁移。候选可进入独立只读需求评审；作者自检不构成批准。
