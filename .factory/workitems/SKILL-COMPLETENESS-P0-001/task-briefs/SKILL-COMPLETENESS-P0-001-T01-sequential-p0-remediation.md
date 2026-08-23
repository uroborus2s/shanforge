# 任务简报

## 身份

- 工作项：`SKILL-COMPLETENESS-P0-001`
- 任务：`SKILL-COMPLETENESS-P0-001-T01`
- 状态：`completed`
- 优先级：`P0`
- 任务层级：`cross_cutting`
- 上游计划：`.factory/workitems/SKILL-COMPLETENESS-P0-001/plan.md`
- 流水账：`.factory/workitems/SKILL-COMPLETENESS-P0-001/ledger.jsonl`

## 模型路由

- control_model: `gpt-5.6-sol`
- task_complexity: `complex`
- risk_level: `medium`
- execution_model: `gpt-5.6-sol`
- execution_authorized: `true`
- route_reason: `跨脚本、复用型 Skill、正式事实和回归守卫，需要顺序收口且避让并发改动`
- escalation_triggers: `input_conflict | scope_expanded | verification_failed_twice | human_gate`

## 执行合同

- 严格按计划的五项顺序执行；每项定向验证通过后再进入下一项。
- 修改前读取真实调用方和当前文件内容，优先在共享根因处修复。
- `skills/document-templates/**` 与 `.factory/memory/**` 当前被 `TEST-GOVERNANCE-001` 使用，写入前必须确认并发任务已完成并重新读取。
- 禁止新增依赖、中心注册表、平台运行时或修改无关用户改动。

## 验证

```bash
uv run pytest -q -p no:cacheprovider
uv run ruff check .
git diff --check
```
