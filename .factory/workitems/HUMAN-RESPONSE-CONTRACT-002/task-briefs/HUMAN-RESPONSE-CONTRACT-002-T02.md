# HUMAN-RESPONSE-CONTRACT-002-T02：总控、WBS 与共享回写合同

## 工作项

- 工作项：`HUMAN-RESPONSE-CONTRACT-002`
- 任务：`HUMAN-RESPONSE-CONTRACT-002-T02`
- 状态：`completed`
- 优先级：`P0`
- 任务层级：`system`
- 关联目标：`HRC-REQ-001`、`HRC-REQ-002`、`HRC-REQ-006`
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
- route_reason: `跨总控、共享合同和行为测试的标准以上改动，按 medium 风险派发 Terra。`
- escalation_triggers: `scope_expanded | input_conflict | risk_increased | verification_failed_twice | human_gate`

## 允许修改

- `skills/using-shanforge/SKILL.md`
- `skills/using-shanforge/references/human-readable-status.md`
- `skills/using-shanforge/references/work-skill-return-contract.md`
- `docs/02-user-guide/user-guide.md`
- `tests/test_skill_progress_visibility_and_continuation.py`
- `tests/test_work_skill_status_envelope_ownership.py`

## 禁止修改

- 其他 Skill、其他测试、其他工作项、memory、远端和生产状态。

## 验证

```bash
uv run pytest -q tests/test_skill_progress_visibility_and_continuation.py tests/test_work_skill_status_envelope_ownership.py
uv run ruff check tests/test_skill_progress_visibility_and_continuation.py tests/test_work_skill_status_envelope_ownership.py
```

## 返回

- `ready_for_review | blocked`
- 修改文件、测试结果和 concerns；不得扩大范围或提交。

## 实现结果

- 已增加共享状态头、按工作类型正文与可消费的工作 Skill 事实字段。
- 已将人类可读状态说明同步为用户指南候选修订，未冒充正式发布版本。
- worker 定向测试：`15 passed`；Ruff 与 diff check 通过。
