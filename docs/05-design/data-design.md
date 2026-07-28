# 数据与存储设计

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `DESIGN-DATA-001` |
| 正式版本 | `v2.0.0` |
| 来源候选 | `SKILL-FIRST-PM-001` |
| 负责人 | `HUMAN_DATABASE_LEAD` |
| 修改 / 审核 / 批准 | `uroborus` / `uroborus` / `uroborus` |
| 状态 | 已批准并生效 |
| 上游 | `system-architecture.md` |
| 下游 | skills、项目记忆、测试与交付文档 |

## 1. 当前数据边界

Shanforge 不运行平台数据库或状态服务。仓库数据分为三类：

| 类型 | 位置 | 是否正式事实 |
|---|---|---|
| 可复用流程资产 | `skills/`、`docs/`、`config/` | 是，受 Git 管理 |
| 项目执行事实 | 目标项目的 `.factory/workitems/`、正式文档和代码 | 是，由目标项目拥有 |
| 可重建投影 | 目标项目的 `.factory/cache/` | 否，可安全删除重建 |

目标项目不得复制 Shanforge 内部状态，也不得依赖 Shanforge 仓库路径、虚拟环境或
已删除的 Python runtime。

## 2. Work item 事实

- `brief.md` 保存目标、范围、状态和验收口径。
- `task-briefs/*.md` 保存当前任务目标、层级、优先级、关系与验证。
- `ledger.jsonl` 追加执行事件；最后一条有效事件可用于当前状态投影。
- evidence、report 和 review 保存可定位证据，不由缓存反向覆盖。
- 正式文档和 ledger 高于 memory summary 与 HTML。

JSONL 每个非空行必须是 JSON object；非法内容失败关闭，不猜测或跳过。

## 3. PM 快照缓存

`using-shanforge/scripts/project_snapshot.py` 只读取目标项目登记事实，写入：

```text
.factory/cache/site/current/index.html
.factory/cache/site/current/snapshot.json
```

`snapshot.json` 保存输入指纹和来源数量。输入未变化时复用现有 HTML。写入使用同目录
临时文件和原子替换；路径解析后必须仍位于目标项目根目录。

快照中的数量是工作项统计，不是产品功能完成率。缓存不进入 ledger、不提交 Git，也不
作为需求、质量、发布或上线事实。

## 4. 安全与生命周期

- 项目秘密、凭证、生产数据和未授权来源不得进入 work item 或快照。
- 符号链接不得把读取或缓存写入引出目标项目根目录。
- `.factory/cache/` 可随时删除；下次查询按登记事实重建。
- 正式事实的保留、归档和删除遵循目标项目自身政策。
- 已删除的 `src/`、SQLite 投影和 `shanforge-di` 仅可从 Git 历史追溯，不得恢复为当前
  执行入口。

## 正式版本历史

| 版本 | 日期 | 变更内容 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v2.0.0` | 2026-07-29 | 删除平台 runtime 数据模型，收口为 skill 与目标项目事实边界 | `uroborus` | `uroborus` | `uroborus` |
