# 任务简报

## 工作项

- 工作项：
- 任务：`<TASK-CARD-ID>`
- task_card_id: `<TASK-CARD-ID>`
- wbs_id: `<WBS-ID>`
- 状态：`planned | active | ready_for_review | completed | closed | blocked`
- owner: `<owner>`
- depends_on: `<TASK-CARD-ID,... | none>`
- review_status: `not_requested | self_check_passed | approved | changes_requested`
- 优先级：`P0 | P1 | P2`
- 任务层级：`project | requirement | cross_cutting | system`
- 关联目标：
  - `<稳定 ID；按任务层级声明一个或多个目标>`
- 强关系：`IMPLEMENTS | DEPENDS_ON | N/A`
- 上游计划：
- 流水账：
- current_gate:
- next_required_action:

## 模型路由

- control_model: `gpt-5.6-sol`
- task_complexity: `simple | standard | complex`
- risk_level: `low | medium | high`
- execution_model: `gpt-5.6-luna | gpt-5.6-terra`
- execution_authorized: `true | false`
- write_policy: `source_or_test_write | project_fact_write | state_or_gate_write | no_project_write`
- dispatch_role: `worker | reviewer | none`
- dispatch_required: `true | false`
- dispatch_mode: `subagent | direct`
- requested_reasoning_effort: `low | medium | high`
- fork_turns: `none`
- route_reason:
- escalation_triggers: `scope_expanded | input_conflict | risk_increased | verification_failed_twice | human_gate`

## 目标

用 1-3 句说明本任务必须完成的可观察结果。

## 输入

- 已批准计划：
- 相关规格 / 需求 / 设计：
- 必读文件：
- 可选参考：

## 允许修改

- `exact/path`

## 禁止修改

- 与本任务无关的文件。
- 用户已有未归属本任务的脏改动。
- 分层边界外的实现。

## 实施步骤

1. 读取必要文件并确认依赖。
2. 新增行为或 Bug 先写最小失败检查；已有测试足以覆盖时直接复用。
3. 写最小实现。
4. 运行必要的定向单元测试或静态检查。
5. 返回实现内容、真实测试结果、文件和 concerns。
6. 继续授权批次；只在跨会话恢复需要时写紧凑 checkpoint。

## 失败断言

- 发现占位语则失败。
- 未运行必要定向检查却声称完成则失败。

## 验证命令

```bash
<命令>
```

期望输出：

```text
<期望输出>
```

## 输出

- 实现内容：
- 测试结果：
- 修改文件：
- concerns：
- 可选 checkpoint：`.factory/workitems/<WORKITEM-ID>/ledger.jsonl`

## 派发回执

仅当 `dispatch_required: true` 时由父 Sol 在调用前生成稳定 `dispatch_id`，并保存真实 `spawn_agent` 成功回执；worker 与独立 reviewer 都适用，子代理自报不算回执。

- dispatch_id: `<父 Sol 调用前生成的稳定 ID>`
- task_card_id: `<TASK-CARD-ID>`
- requested_model: `必须等于 execution_model`
- requested_reasoning_effort:
- fork_turns: `none`
- agent_id / canonical_task:
- status: `accepted（工具调用成功接受，不是子代理完成态）`
- source: `parent_tool_receipt`

## 完成口径

低、中风险任务完成后继续批次，不单独进入 review。只有高风险专项或批次质量候选可以写
`ready_for_review`；`approved` 只允许写入 review_status，且必须来自适用的独立评审。它不改变
TaskCard 生命周期状态；产品和 WBS 完成只认 `completed | closed | superseded`。
