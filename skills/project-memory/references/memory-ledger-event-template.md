# Memory Ledger 事件模板

Ledger 是恢复事实源。对话记忆和 todo 与 ledger 冲突时，以 ledger、git log 和 evidence 为准。

## 会话事件

写入 `.factory/memory/session-ledger.jsonl`。

```json
{
  "event_id": "evt-20260705-001",
  "time": "2026-07-05T10:00:00+08:00",
  "actor": "Codex",
  "event_type": "session_start",
  "action": "session_start",
  "status": "done",
  "idempotency_key": "session:20260705:project-memory:start",
  "inputs": [
    ".factory/memory/runtime-brief.md",
    ".factory/memory/current-state.md"
  ],
  "outputs": [
    ".factory/memory/agent-session.md"
  ],
  "task_card_id": "SF-SP-002-T01",
  "wbs_id": "SF-SP-002-T01",
  "current_gate": "status-memory-workflow",
  "next_status": "ready_for_workitem_routing",
  "next_required_action": "hand_back_to_using_shanforge"
}
```

## Work item 事件

写入 `.factory/workitems/<WORKITEM-ID>/ledger.jsonl`。

```json
{
  "event_id": "evt-20260705-002",
  "time": "2026-07-05T10:30:00+08:00",
  "actor": "Codex",
  "event_type": "workitem_event",
  "work_item_id": "SF-SP-002",
  "action": "implement_project_memory_skill",
  "status": "ready_for_review",
  "task_card_id": "SF-SP-002-T01",
  "wbs_id": "SF-SP-002-T01",
  "current_gate": "independent_review",
  "idempotency_key": "SF-SP-002:project-memory-skill:implement",
  "evidence": [
    "tests/test_project_memory_skill.py"
  ],
  "next_status": "ready_for_review",
  "next_required_action": "request_independent_review"
}
```

## 恢复规则

- `status=approved|done|passed` 且 `idempotency_key` 相同的事件不得重复执行。
- `ready_for_review` 不是完成，只表示实现者报告已提交。
- `approved` 必须来自独立 review task 或未参与实现的 reviewer。
- `done` 必须同时有验证、review、PR 或 memory sync 证据。
- 事件只能记录已发生的动作，不能预填计划。
- 会话卡、session ledger 与 work item ledger 都必须记录相同的 `task_card_id`、`wbs_id`、`current_gate`、
  `next_required_action`；无活动任务时四个字段显式记录 `none`，不得省略。
