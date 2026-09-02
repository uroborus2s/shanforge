# T01：补齐技术评估回复因果链

- task_card_id: `TECHNICAL-ASSESSMENT-RESPONSE-001-T01`
- wbs_id: `WBS-TECH-ASSESS-01`
- status: `closed`
- priority: `P0`
- owner: `gpt-5.6-terra`
- depends_on: `none`
- risk_level: `medium`
- execution_authorized: `true`
- current_gate: `closed`
- next_required_action: `none`
- write_policy: `source_or_test_write`
- control_model: `gpt-5.6-sol`
- task_complexity: `standard`
- execution_model: `gpt-5.6-terra`
- dispatch_role: `worker`
- dispatch_required: `true`
- dispatch_mode: `subagent`
- requested_reasoning_effort: `medium`
- fork_turns: `none`

## 目标

在唯一共享响应合同中增加“技术评估”正文，让用户可以沿“需求 → 现象 → 代码 → 原因 → 影响 → 建议”读懂结论。

## 允许修改

- `skills/using-shanforge/references/human-readable-status.md`
- `skills/using-shanforge/references/work-skill-return-contract.md`
- `skills/humanizer/SKILL.md`
- `tests/test_human_response_contract_integration.py`
- `tests/test_response_owner_contracts.py`

## 禁止

- 不修改其他 Skill、测试、正式文档、ledger 或 memory。
- 不新增 reference、schema、运行时脚本或依赖。
- 不批量复制合同到各工作 Skill。
- 禁止函数套函数；禁止新增只有一个调用点且无独立职责的公共函数。
- 不提交、不 push、不自批完成。

## 验收

- RED 测试证明现有合同缺少技术评估字段和可消费示例。
- 工作 Skill 可回写需求上下文、现象、代码证据、因果链、影响、结论和建议。
- 人类正文用业务语言解释每条技术发现，不以术语、文件列表或评分代替。
- humanizer 不得删除或改写技术评估事实链。
- 定向测试和 Ruff 通过，`code_shape_check` 为 `passed`。
