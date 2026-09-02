# T12：清理专业歧义和重复合同

- task_card_id: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001-T12`
- wbs_id: `WBS-AUDIT-12`
- status: `completed`
- priority: `P1`
- task_scope: `system`
- owner: `/root/t12_ambiguity_dispatch_contracts`
- depends_on: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001-T11`
- risk_level: `medium`
- execution_authorized: `true`
- current_gate: `closed`
- next_required_action: `activate_t13`
- write_policy: `source_or_test_write`
- control_model: `gpt-5.6-sol`
- task_complexity: `complex`
- execution_model: `gpt-5.6-terra`
- dispatch_role: `worker`
- dispatch_required: `true`
- dispatch_mode: `subagent`
- dispatched_to: `/root/t12_ambiguity_dispatch_contracts`
- dispatch_id: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001:T12:terra-medium:v4`
- requested_reasoning_effort: `medium`
- fork_turns: `none`
- route_reason: `跨 UI/frontend/Stratix/总控文本合同的中风险 source/test 工作`
- allowed_paths: `skills/ui-ux-pro-max/SKILL.md`, `skills/frontend-patterns/SKILL.md`, `skills/stratix-admin-web/SKILL.md`, `skills/browser-control/SKILL.md`, `skills/article-writing/SKILL.md`, `skills/writing-plans/SKILL.md`, `skills/executing-plans/SKILL.md`, `skills/subagent-driven-development/SKILL.md`, `skills/using-shanforge/SKILL.md`, `skills/using-shanforge/references/work-skill-return-contract.md`, `skills/using-shanforge/references/human-readable-status.md`, `skills/using-shanforge/references/pm-dashboard-rendering.md`, `skills/using-shanforge/references/black-box-flow-eval.md`, `tests/test_ui_ux_pro_max_skill.py`, `tests/test_stratix_admin_web_skill.py`, `tests/test_browser_control_skill.py`, `tests/test_writing_plans_skill.py`, `tests/test_execution_workflow_skills.py`, `tests/test_black_box_workflow_eval.py`, `tests/test_residual_audit_contracts.py`
- forbidden_actions: 新增总控层、新 schema、新 reference、无证据大重构、函数套函数、单调用点无职责公共 helper、修改 memory/Git/远端

## 验收

- 三个专业歧义词改成可执行且不会误导范围的表述。
- “验收标准/验收结果”、DOM/state/accessibility snapshot、用户授权语气样本均有准确边界。
- 派发黑盒覆盖完整身份/写策略/授权/派发模式/模型一致性、父工具回执、worker 回执、未授权/失败关闭、`close_allowed=false` 和禁止 Sol 静默代写。
- 子代理派发公式只保留一份规范定义；总控路由字段按任务身份、控制/复杂度、风险/范围、派发、Gate/升级准确分组且字段不重复。
- `using-shanforge` 只删除已由上述现有 reference 单一拥有且测试覆盖的重复规则。
- 没有新增抽象或依赖；返回 `code_shape_check: passed|failed`。
