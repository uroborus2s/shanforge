# T13-R03：兼容检查执行真实 lock 与 CLI smoke

- task_card_id: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001-T13-R03`
- wbs_id: `WBS-AUDIT-13-R03`
- status: `completed`
- owner: `/root/t13_compatibility_smoke_fix`
- depends_on: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001-T10`
- current_gate: `closed`
- next_required_action: `independent_rereview_SE-I05`
- write_policy: `source_or_test_write`
- execution_authorized: `true`
- execution_model: `gpt-5.6-terra`
- requested_reasoning_effort: `medium`
- fork_turns: `none`
- dispatch_id: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001:T13-R03:terra-medium:v1`

## 根因与影响

Crawler4j/Stratix 的 Skill 文本要求交叉读取 lock 并执行 CLI smoke，但现有 checker 和测试只检查声明版本或手工 `--cli-version`，可能把不可运行的 CLI 错判为兼容。

## 写集

- `skills/crawler4j-model-project/scripts/check_compatibility.py`
- `skills/crawler4j-model-project/SKILL.md`
- `tests/test_crawler4j_model_skill_integration.py`
- `skills/stratix-service/scripts/check_compatibility.py`
- `skills/stratix-service/SKILL.md`
- `skills/stratix-service/references/cli-workflow.md`
- `tests/test_stratix_service_skill.py`

## 验收

- Crawler4j 读取合法 manifest lock；版本/协议通过后执行 `crawler4j --version` 与结构 smoke。
- Stratix 读取 lock 版本；矩阵通过后执行 `pnpm exec stratix --help` 与 `pnpm exec stratix doctor`。
- 测试使用可控假 CLI 验证成功、CLI 失败、lock 不一致，以及“不兼容时不得执行 smoke”。
- checker fail closed，不新增依赖；禁止函数套函数和无职责单调用公共 helper。
