# T11：补齐响应、评审和状态 owner 合同

- task_card_id: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001-T11`
- wbs_id: `WBS-AUDIT-11`
- status: `completed`
- priority: `P0`
- task_scope: `system`
- owner: `/root/t11_response_owner_contracts`
- depends_on: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001-T10`
- risk_level: `medium`
- execution_authorized: `true`
- current_gate: `closed`
- next_required_action: `activate_t12`
- write_policy: `source_or_test_write`
- control_model: `gpt-5.6-sol`
- task_complexity: `complex`
- execution_model: `gpt-5.6-terra`
- dispatch_role: `worker`
- dispatch_required: `true`
- dispatch_mode: `subagent`
- dispatched_to: `/root/t11_response_owner_contracts`
- dispatch_id: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001:T11:terra-medium:v2`
- requested_reasoning_effort: `medium`
- fork_turns: `none`
- route_reason: `跨 review/memory/shared-contract 的中风险 source/test 工作`
- allowed_paths: `skills/receiving-code-review/SKILL.md`, `skills/requesting-code-review/SKILL.md`, `skills/project-memory/SKILL.md`, `skills/project-memory/references/session-card-template.md`, `skills/writing-plans/references/plan-review-template.md`, `skills/writing-plans/references/workitem-plan-template.md`, `skills/webapp-testing/SKILL.md`, `skills/agent-harness-construction/SKILL.md`, `skills/release-deployment/SKILL.md`, `skills/using-shanforge/references/work-skill-return-contract.md`, `skills/using-shanforge/references/human-readable-status.md`, `tests/test_review_workflow_skills.py`, `tests/test_project_memory_skill.py`, `tests/test_work_skill_status_envelope_ownership.py`, `tests/test_remaining_skill_project_status_contract.py`, `tests/test_human_response_contract_integration.py`, `tests/test_response_owner_contracts.py`
- forbidden_actions: 批量改 32 个已合规 Skill、改写项目状态 owner、函数套函数、单调用点无职责公共 helper、修改 memory/Git/远端

## 验收

- triage/response owner 唯一，未授权路径交还总控。
- 无活动 WorkItem 的 `SB-STATUS/no_project_write` 行为明确。
- plan review 检查依赖 DAG、完整生命周期/review 词表和恢复字段；计划 Gate 有 ID、owner、进入条件、evidence path。
- session card 有停止原因；读取回执（`receipt`）、基于技术证据提出异议（`pushback`）均中文在前。
- 内部候选 next actions、发布类状态和 webapp-testing 路由边界不越过总控 owner；发布类必须有与开发/测试/Bug/修复同级的真实三段式响应示例和集成断言。
- 32 个工作 Skill 共享合同引用检查通过；已合规文件保持不变。
- 返回 `code_shape_check: passed|failed`。
