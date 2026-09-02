# T13-R02：正式计划模板与依赖 DAG 闭环

- task_card_id: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001-T13-R02`
- wbs_id: `WBS-AUDIT-13-R02`
- status: `completed`
- owner: `/root/t13_planning_graph_fix`
- depends_on: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001-T12`
- current_gate: `closed`
- next_required_action: `independent_rereview_ZH-I01_PM-I04_PM-I05_PM-N01`
- write_policy: `source_or_test_write`
- execution_authorized: `true`
- execution_model: `gpt-5.6-terra`
- requested_reasoning_effort: `medium`
- fork_turns: `none`
- dispatch_id: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001:T13-R02:terra-medium:v1`

## 根因与影响

- `workitem-plan-template.md` 仍把计划前输入写成“验收结果”。
- 正式 TaskCard 模板没有稳定 `owner` 与结构化 `depends_on`；计划评审只有 DAG 文字要求，没有可执行校验。
- PM 贯通测试只实例化 plan 模板，TaskCard 与 ledger 为手写简化文本，不能证明正式模板彼此一致。
- `current` 是 WBS 进度状态，不是 TaskCard 生命周期；现合同没有明确区分，造成 reviewer 误判。

## 写集

- `skills/writing-plans/references/workitem-plan-template.md`
- `skills/writing-plans/references/task-brief-template.md`
- `skills/writing-plans/references/plan-review-template.md`
- 新建 `skills/writing-plans/scripts/validate_task_graph.py`
- `tests/test_using_shanforge_snapshot.py`
- `tests/test_writing_plans_skill.py`
- `tests/test_response_owner_contracts.py`
- 新建 `tests/test_writing_plan_task_graph.py`

## 验收

- “目标和验收标准”替代“目标和验收结果”，并有反向断言。
- WBS 词表明确为 `planned | current | completed`；TaskCard 生命周期保持 `planned | active | ready_for_review | completed | closed | blocked`，两者不得混用。
- TaskCard 和计划任务均有 `owner`、`depends_on: <TASK-CARD-ID,... | none>`。
- 标准库校验入口拒绝缺 owner、未知依赖、自依赖和依赖环。
- 贯通测试实例化两个正式模板并接入 ledger/PM snapshot；合法样例通过、上述失败样例失败。
- 禁止函数套函数、禁止新增只有一个调用点且无独立职责的公共 helper。
