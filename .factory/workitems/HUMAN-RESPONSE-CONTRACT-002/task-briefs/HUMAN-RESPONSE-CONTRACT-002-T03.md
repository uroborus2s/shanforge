# HUMAN-RESPONSE-CONTRACT-002-T03：测试、Bug 与修复任务卡合同

## 工作项

- 工作项：`HUMAN-RESPONSE-CONTRACT-002`
- 任务：`HUMAN-RESPONSE-CONTRACT-002-T03`
- 状态：`completed`
- 优先级：`P0`
- 任务层级：`system`
- 关联目标：`HRC-REQ-003`、`HRC-REQ-004`、`HRC-REQ-005`、`HRC-REQ-006`
- 强关系：`IMPLEMENTS`

## 模型路由

- control_model: `gpt-5.6-sol`
- task_complexity: `complex`
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
- route_reason: `跨调试、TDD、验证合同和行为测试的中风险改动，派发 Terra。`
- escalation_triggers: `scope_expanded | input_conflict | risk_increased | verification_failed_twice | human_gate`

## 允许修改

- `skills/systematic-debugging/SKILL.md`
- `skills/tdd-workflow/SKILL.md`
- `skills/verification-before-completion/SKILL.md`
- `tests/test_verification_debugging_workflow_skills.py`

## 禁止修改

- 总控、共享回写合同、其他 Skill、其他测试、其他工作项、memory、远端和生产状态。

## 验证

```bash
uv run pytest -q tests/test_verification_debugging_workflow_skills.py
uv run ruff check tests/test_verification_debugging_workflow_skills.py
```

## 返回

- `ready_for_review | blocked`
- 修改文件、测试结果和 concerns；不得扩大范围或提交。

## 实现结果

- 已增加测试八列汇总、失败项解释、Bug 事实与修复 TaskCard 三分支决策。
- worker 定向测试：`8 passed`；Ruff 与 diff check 通过。
