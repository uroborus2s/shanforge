# 任务简报：T03 模型路由治理测试

## 工作项

- 工作项：`MODEL-DISPATCH-RUNTIME-001`
- 任务：`MODEL-DISPATCH-RUNTIME-001-T03`
- 状态：`completed`
- 优先级：`P1`
- 任务层级：`system`
- 关联目标：`MODEL-DISPATCH-RUNTIME-001`
- 强关系：`DEPENDS_ON`
- 依赖：`T01`、`T02`

## 模型路由

- control_model: `gpt-5.6-sol`
- task_complexity: `standard`
- risk_level: `medium`
- execution_model: `gpt-5.6-terra`
- execution_authorized: `true`
- write_policy: `source_or_test_write`
- current_gate: `closed`
- dispatch_role: `worker`
- dispatch_required: `true`
- dispatch_mode: `subagent`
- requested_reasoning_effort: `medium`
- fork_turns: `none`
- route_reason: 测试需要跨配置、Skill 与文档验证同一运行时合同。
- escalation_triggers: `scope_expanded | input_conflict | risk_increased | verification_failed_twice | human_gate`

## 允许修改

- `tests/test_model_tier_routing.py`

## 禁止修改

- 其他所有文件；不得提交或远端。

## 验证命令

- `uv run pytest tests/test_model_tier_routing.py -q -p no:cacheprovider`
- `uv run ruff check tests/test_model_tier_routing.py`
- `git diff --check -- tests/test_model_tier_routing.py`

## 完成口径

- 测试解析真实 TOML，不只匹配说明文字。
- 测试锁定 Sol 主控、Luna/Terra 模型与推理强度、reviewer 只读。
- 测试锁定 `dispatch_required/subagent`、显式 spawn 参数、父回执和失败关闭。
- 三条验证命令通过，并返回测试数量和 exit code。
