# 会话启动清单

按顺序执行。目标是生成压缩会话卡，不是把所有背景文件塞进上下文。

1. 先检查当前对话中是否已有会话卡、当前阶段、work item 和禁止动作。
2. 若已有同一 work item 的新鲜会话卡，复用它；不要重复读取源 summary。
3. 若缺少会话卡，读取 `.factory/memory/agent-session.md`。
4. 只有 `agent-session.md` 缺失、过期或与当前任务不匹配时，才读取 `.factory/memory/runtime-brief.md` 和 `.factory/memory/current-state.md`。
5. 只有需要定位正式事实源时，才读取 `.factory/memory/doc-map.md`。
6. 只有需要角色协作事实时，才读取 `.factory/memory/role-charter.project.md`。
7. 只有需要项目元数据时，才读取 `.factory/project.json`。
8. 按当前任务读取必要 summary，例如 `tasks.summary.md`、`tests.summary.md`、`tech-stack.summary.md`。
9. 检查是否存在 `.factory/workitems/<WORKITEM-ID>/ledger.jsonl`。
10. 写入会话 ledger 事件，记录已读文件、明确排除项、任务焦点和待决事项。

输出时说明：

- 当前阶段。
- 当前 work item 或临时任务。
- 已读取上下文。
- 未读取 / 已排除的背景文件。
- 明确禁止动作。
- 待决事项，交回 `using-shanforge` 判断。

不要默认读取阶段 `docs/` 长文。只有 relevance gate 命中时才回源单个正式文档。
