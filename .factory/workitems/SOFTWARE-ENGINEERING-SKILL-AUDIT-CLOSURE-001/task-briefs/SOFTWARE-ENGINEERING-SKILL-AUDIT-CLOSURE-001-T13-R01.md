# T13-R01：更新单一结果包 owner 的旧回归断言

- task_card_id: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001-T13-R01`
- wbs_id: `WBS-AUDIT-13-R01`
- status: `completed`
- priority: `P0`
- task_scope: `system`
- owner: `/root/t13_regression_assertion_fix`
- depends_on: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001-T12`
- risk_level: `medium`
- execution_authorized: `true`
- current_gate: `closed`
- next_required_action: `resume_t13_full_verification`
- write_policy: `source_or_test_write`
- control_model: `gpt-5.6-sol`
- task_complexity: `standard`
- execution_model: `gpt-5.6-terra`
- dispatch_role: `worker`
- dispatch_required: `true`
- dispatch_mode: `subagent`
- requested_reasoning_effort: `medium`
- fork_turns: `none`
- dispatched_to: `/root/t13_regression_assertion_fix`
- dispatch_id: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001:T13-R01:terra-medium:v1`
- route_reason: `三项旧测试仍要求已由共享 reference 单一拥有的重复字段`
- allowed_paths: `tests/test_skill_flow_process_audit.py`, `tests/test_skill_progress_visibility_and_continuation.py`, `tests/test_work_skill_status_envelope_ownership.py`
- forbidden_actions: 修改 Skill/reference/正式文档、放宽真实行为要求、删除测试、函数套函数、单调用点无职责公共 helper、修改 memory/Git/远端

## 根因

T12 删除 `using-shanforge` 中重复的工作 Skill 本职结果包枚举，改由 `work-skill-return-contract.md` 单一拥有；receiving review 写入也改为授权条件式。三个旧测试仍要求总控复制字段或无条件写 response，因此与新合同冲突。

## 验收

- receiving review 测试检查“有授权才写、未授权交还总控”，不再要求无条件 `response 已写入`。
- code shape 字段从共享合同断言；总控只需引用共享合同。
- 本职结果包字段只在共享合同断言，项目状态信封仍只在总控断言。
- 不删除测试或降低项目状态 owner、status/needs 原样转发、代码形状约束。
- 定向三个文件通过，Ruff、代码形状和 diff check 通过；返回 `code_shape_check: passed|failed`。
