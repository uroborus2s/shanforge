# 会话启动清单

按顺序执行。目标是生成压缩会话卡，不是把所有背景文件塞进上下文。

## 条件读取链

- 每一级够用即停，不为“完整背景”继续扩张。
- 当前对话中的新鲜会话卡足够时，读取 memory 文件数必须为 0。
- 若已有同一 work item 的新鲜会话卡，复用它；不要重复读取源 summary。
- 不能只读 `.factory/memory/current-state.md` 就判断权威任务状态。
- 不得固定读取 `agent-session.md`、`runtime-brief.md`、`current-state.md` 三件套。
- 每次扩展读取前先写明事实缺口，从候选来源二选一，一次只读取一个最小片段；补足后立即停止。
- 只有会话卡缺失、过期或不匹配且明确缺口命中时，才读取 `.factory/memory/runtime-brief.md`。

1. 先检查当前对话中是否已有会话卡、当前阶段、work item 和禁止动作；够用即停。
2. 当前对话不足时，读取 `.factory/memory/agent-session.md` 的当前卡；匹配且新鲜时停止。
3. 会话卡缺失、过期或不匹配时，先写缺口，再从 `runtime-brief.md` 或 `current-state.md` 选择一个最小相关片段，不同时读取。
4. 定位到 work item 后，读取当前 TaskCard 与 `.factory/workitems/<WORKITEM-ID>/ledger.jsonl`，核对最新 Gate。
5. 只有需要定位正式事实源时，才读取 `.factory/memory/doc-map.md`。
6. 只有需要角色协作事实时，才读取 `.factory/memory/role-charter.project.md`。
7. 只有需要项目元数据时，才读取 `.factory/project.json`。
8. 只有已明确 summary 能补足当前缺口时，才读对应 summary；一次只选一个。
9. 写入会话 ledger 事件，记录已读文件、每次扩展原因、明确排除项、任务焦点和待决事项。

输出时说明：

- 当前阶段。
- 当前 work item 或临时任务。
- 已读取上下文。
- 未读取 / 已排除的背景文件。
- 明确禁止动作。
- 待决事项，交回 `using-shanforge` 判断。

不要默认读取阶段 `docs/` 长文。只有 relevance gate 命中时才回源单个正式文档。
