# 会话卡模板

```markdown
# 会话卡

- 时间：<ISO-8601>
- Actor：<Codex | Gemini | 其他>
- 阶段：<BRAINSTORM | REQUIREMENTS | DESIGN | PLAN | IMPLEMENTATION | TESTING | ACCEPTANCE | RELEASE | MAINTENANCE>
- 项目整体进度：`<work_item_id> / <task_card_id>`
- 当前工作项：<work_item_id 或 none>
- 当前任务：<task_card_id 或 none>
- 当前 WBS：<wbs_id 或 none>
- 状态：<in_progress | ready_for_review | blocked>
- Gate：<current_gate 或 none>
- 停止原因：<none 或具体原因>
- 唯一下一动作：<next_required_action 或 none>

## 本轮目标

<一句话说明本轮要推进什么。>

## 已读取上下文

- <path>：<为什么读>

## 未读 / 已排除上下文

- <path 或类别>：<为什么不读>

## 当前事实

- <只写已观察到的事实>

## 禁止动作

- <不要散读 docs / 不要自批 done / 不要重复执行 ledger 已通过事件>

## 待决事项

- <需要交回 using-shanforge 判断的动作或 gate>

## 证据

- <测试、review、diff、文档链接>
```

会话卡可以写入 `.factory/memory/agent-session.md` 或 work item 报告。写入前先确认不会覆盖用户正在编辑的内容。
