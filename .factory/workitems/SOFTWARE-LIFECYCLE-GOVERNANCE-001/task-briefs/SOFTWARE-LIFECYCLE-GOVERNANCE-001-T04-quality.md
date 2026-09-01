# 任务简报：T04 集中质量与独立评审

## 工作项与路由

- 工作项：`SOFTWARE-LIFECYCLE-GOVERNANCE-001`
- 任务：`SOFTWARE-LIFECYCLE-GOVERNANCE-001-T04`
- 状态：`closed`
- 优先级：`P0`
- 任务层级：`system`
- 关联目标：`SOFTWARE-LIFECYCLE-GOVERNANCE-001`
- 强关系：`IMPLEMENTS`
- control_model: `gpt-5.6-sol`
- task_complexity: `complex`
- risk_level: `medium`
- execution_model: `gpt-5.6-terra`
- execution_authorized: `false`
- write_policy: `state_or_gate_write`
- current_gate: `none`
- dispatch_role: `none`
- dispatch_required: `false`
- dispatch_mode: `direct`
- requested_reasoning_effort: `high`
- fork_turns: `none`
- route_reason: 同一 Terra/high/read-only reviewer iteration 3 已批准；实现提交 `f9654c6` 的 `--no-local` 干净克隆完整质量门全绿，任务关闭。
- escalation_triggers: `scope_expanded | input_conflict | risk_increased | verification_failed_twice | human_gate`

## 目标

对完整候选执行集中验证、独立只读评审、同范围整改、精确本地提交和提交后干净克隆复验。

## 允许修改

- 评审阶段只读实现候选；Sol 只追加本 WorkItem 的 evidence、report、review、ledger 和必要 memory。

## 禁止修改

- reviewer 不得修改实现、测试、正式文档、Git 或外部系统。
- 不执行 push、PR、merge、发布或部署。

## 验证命令

```bash
uv run pytest -q
uv run ruff check .
git diff --check
```

另执行全部 Skill validator、TOML/JSON/JSONL 校验和提交后干净克隆同等验证。
