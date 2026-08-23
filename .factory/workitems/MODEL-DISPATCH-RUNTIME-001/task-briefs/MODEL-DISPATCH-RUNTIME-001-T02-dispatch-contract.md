# 任务简报：T02 真实派发合同与文档

## 工作项

- 工作项：`MODEL-DISPATCH-RUNTIME-001`
- 任务：`MODEL-DISPATCH-RUNTIME-001-T02`
- 状态：`completed`
- 优先级：`P1`
- 任务层级：`system`
- 关联目标：`MODEL-DISPATCH-RUNTIME-001`
- 强关系：`IMPLEMENTS`

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
- route_reason: 跨稳定入口、Skill 合同、模板和正式文档，需要一致性判断但不涉及高风险边界。
- escalation_triggers: `scope_expanded | input_conflict | risk_increased | verification_failed_twice | human_gate`

## 目标

把文字模型矩阵升级为 Codex 可执行、失败关闭、可审计的派发合同，并同步人类说明。

## 允许修改

- `AGENTS.md`
- `skills/using-shanforge/SKILL.md`
- `skills/subagent-driven-development/SKILL.md`
- `skills/subagent-driven-development/references/status-handling-checklist.md`
- `skills/using-shanforge/references/codex-tools.md`
- `skills/writing-plans/references/task-brief-template.md`
- `docs/05-design/workflow-execution-design.md`
- `docs/02-user-guide/user-guide.md`

## 禁止修改

- 其他所有文件；不得写测试、WorkItem 状态、提交或远端。

## 完成口径

- 已授权 `source_or_test_write` 必须真实 spawn，Sol 不可静默代写。
- 派发显式携带 `model`、`reasoning_effort`、`fork_turns=none` 和完整 task brief。
- 父会话生成稳定 `dispatch_id` 并保存 `task_card_id/requested_model/reasoning/fork_turns/agent_id/status/source` 回执；不得虚构工具必返字段。
- spawn 失败、模型不可用、回执缺失或模型不匹配均失败关闭并交还 Sol。
- 稳定入口和正式文档说明 `.codex` 配置与宿主能力边界。

## 验证命令

```bash
uv run pytest tests/test_model_tier_routing.py -q
uv run ruff check tests/test_model_tier_routing.py
git diff --check
```

期望：路由测试全部通过、Ruff `All checks passed!`、diff check exit code `0`。
