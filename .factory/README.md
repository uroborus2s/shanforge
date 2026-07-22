# .factory 工作区治理

`.factory` 存放 AI 协作执行事实、恢复摘要、机器配置和本地派生物。正式产品事实仍以 `docs/` 为人类可审计来源；执行事实以 work item ledger/evidence 为准；`.factory` 的索引和 cache 不替代这些事实。

## 目录职责

| 路径 | 职责 | 事实边界 |
|---|---|---|
| `.factory/project.json` | 项目元数据、阶段、正式文档画像和角色入口 | 稳定配置事实 |
| `.factory/project.lock` | 项目配置锁定结果 | 稳定配置事实 |
| `.factory/tech-profile.json` | 当前技术画像 | 稳定配置事实 |
| `.factory/memory/` | 会话恢复摘要、doc-map、状态摘要、review ledger | 摘要和索引，不复制正式正文 |
| `.factory/workitems/` | 可追踪 work item 的 brief、plan、task brief、evidence、report、review 和 ledger | 执行事实源 |
| `.factory/catalog/` | 机器可读的文档 Catalog source 与发布策略 | 受控机器配置，不放入 `docs/` |
| `.factory/project-knowledge/` | 来源登记、稳定 alias 和强关系声明 | 受控机器配置；声明关系必须回指正式事实 |
| `.factory/index/` | SQLite 当前知识投影 | 本地可删除重建；由 `.gitignore` 排除 |
| `.factory/cache/` | 当前静态站点、页面构建与临时迁移包 | 本地可删除重建；由 `.gitignore` 排除并受维护策略限制 |
| `.factory/runtime/` | 异步同步队列与租约状态 | 本地运行态；不得作为项目历史提交 |

## Work item 标准结构

项目化任务必须使用以下结构：

```text
.factory/workitems/<WORKITEM-ID>/
  brief.md
  plan.md
  task-briefs/
  evidence/
  reports/
  reviews/
  ledger.jsonl
```

字段约束：

- `brief.md`：目标、非目标、背景、成功标准、影响范围。
- `plan.md`：文件范围、任务拆分、测试策略、文档同步、review gate。
- `task-briefs/`：单个可验收任务的授权输入。
- `evidence/`：真实命令、截图、检查和验证结果。
- `reports/`：实现报告、收口报告、最终审计问题报告。
- `reviews/`：review 输入包、review 结果、反馈响应。
- `ledger.jsonl`：状态事件、gate、下一动作和幂等键。

## 破坏性迁移规则

本仓当前采用“只保留最新正式资产和正式内容”的文档基线：

1. `docs/04-project-development` 只保留根导航和文档索引登记的正式页面，以及页面引用的必要资产。
2. 旧过程页、旧专题页、旧原型、旧生成页面和旧 memory 快照不再作为正式资产保留。
3. `.factory/process/`、`.factory/pm/` 和 `.factory/memory/history/` 属于旧结构；完成对账迁移后不纳入正式基线，也不得恢复为第二套事实源。
4. 已存在的 `.factory/workitems/<ID>/ledger.jsonl`、`evidence/`、`reports/` 和 `reviews/` 是执行审计事实；除非另有单独归档方案，不批量删除。
5. 当前执行人字段代表“用户授权代执行”，正式文档版本历史不得署名为 `Codex`。

## 禁止事项

- 不把临时推理、长命令输出或完整子 agent 输出写入 `.factory/memory/`。
- 不把按需生成的 HTML 展示页当作事实源。
- 不提交 `.factory/index/`、`.factory/cache/` 或 `.factory/runtime/*.sqlite3*`；它们必须能从受控事实重建。
- 不把作者自检写成 `approved`。
- 不把计划、占位或未运行命令写成完成事实。
- 不恢复旧中心命令、动作注册表、`factory-*` 或旧全局流程脚本。

## 状态包

项目化任务收口时必须返回：

```text
工作结果：
- work_item: <WORKITEM-ID>
- skill: <skill-name>
- status: ready_for_review | blocked | needs_user_input | passed | partial | failed
- outputs:
  - <path>
- evidence:
  - <path>
- ledger_event: <event id or path>
- needs:
  - review | verification | human_confirmation | commit | plan_rewrite | none
```
