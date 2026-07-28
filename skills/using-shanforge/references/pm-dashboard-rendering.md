# 项目状态查询与只读站点

本文件定义 `using-shanforge` 自带 PM 快照脚本的调用合同。脚本属于 skill，不依赖
Shanforge 源码仓、虚拟环境、SQLite 或第三方包。

## 调用

从当前 `SKILL.md` 所在目录定位脚本，在目标项目中执行：

```bash
python3 <skill-directory>/scripts/project_snapshot.py --project-root <project-root>
```

只需在 receipt 中返回项目相对路径时增加 `--relative-paths`。该选项不脱敏页面内容，
不得把本地快照直接当作可公开共享产物。不要把 `<skill-directory>` 原样传给 shell；
必须替换成当前已加载 skill 的真实目录。

## 输入与输出

脚本只读取：

- `.factory/project.json`（可选）
- `.factory/memory/agent-session.md`（可选）
- `.factory/workitems/*/brief.md`
- `.factory/workitems/*/task-briefs/*.md`（可选；用于显示当前任务、层级、优先级和需求关系）
- `.factory/workitems/*/ledger.jsonl`

脚本只写可删除重建的：

- `.factory/cache/site/current/index.html`
- `.factory/cache/site/current/snapshot.json`

标准 receipt 为 `SkillProjectSnapshotReceipt/v1`，包含 `status`、`html_path`、
`cache_hit`、`generation_id`、`source_count`、`relative_paths` 和 `read_only_facts`。
输入指纹不变时必须返回 `cache_hit=true`。

## 解释边界

- 页面按登记状态分为需要关注、正在推进、后续待办和已完成；只有卡片明确显示
  “等待你的确认”时才代表真实人工 Gate。
- 页面中的数量是工作项统计，不是产品功能完成率。
- ledger 最后一条事件提供当前状态和下一动作；work item brief 提供业务目标，
  task brief 提供当前任务、层级、优先级、需求关系和完成标准。
- 页面先显示中文业务状态和当前重点；原始 ID、原始状态放在可展开的技术状态中。
- 没有 brief 和 ledger 的分组目录不是工作项，不得显示为“状态未登记”。
- 非法 JSON/JSONL、目标目录不存在或缺少 `.factory/` 时失败关闭。
- 页面只读，不提供编辑、审批、提交或发布入口。
- HTML 和缓存不是项目事实，不写 ledger、不提交 Git。
