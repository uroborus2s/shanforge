# T13-R04：嵌套 lambda 代码形态门

- task_card_id: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001-T13-R04`
- wbs_id: `WBS-AUDIT-13-R04`
- status: `completed`
- owner: `/root/t13_lambda_shape_fix`
- depends_on: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001-T10`
- current_gate: `closed`
- next_required_action: `independent_rereview_SE-NEW-M01`
- write_policy: `source_or_test_write`
- execution_authorized: `true`
- execution_model: `gpt-5.6-terra`
- requested_reasoning_effort: `medium`
- fork_turns: `none`
- dispatch_id: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001:T13-R04:terra-medium:v1`

## 根因与影响

`ShapeVisitor` 只检查 `FunctionDef/AsyncFunctionDef`，函数体中的 lambda 可绕过“禁止函数套函数”。

## 写集

- `skills/tdd-workflow/scripts/check_code_shape.py`
- `tests/test_code_shape_check.py`

## 验收

- 函数体内 lambda 返回非零并报告精确行号；模块级 lambda 不被误判为嵌套。
- 既有命名局部函数与单调用候选行为不回归。
- 禁止新增 helper 或函数套函数。
