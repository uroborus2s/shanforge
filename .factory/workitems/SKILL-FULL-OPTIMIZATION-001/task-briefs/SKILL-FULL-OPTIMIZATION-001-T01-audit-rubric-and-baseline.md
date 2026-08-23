# SKILL-FULL-OPTIMIZATION-001-T01 任务简报

## 身份

- 工作项：`SKILL-FULL-OPTIMIZATION-001`
- 任务：`SKILL-FULL-OPTIMIZATION-001-T01`
- 状态：`completed`
- 优先级：`P0`
- 任务层级：`system`
- 关联目标：`SKILL-FULL-OPTIMIZATION-001`
- 强关系：`N/A`
- 上游计划：`.factory/workitems/SKILL-FULL-OPTIMIZATION-001/plan.md`
- 流水账：`.factory/workitems/SKILL-FULL-OPTIMIZATION-001/ledger.jsonl`

## 模型路由

- control_model: `gpt-5.6-sol`
- task_complexity: `complex`
- risk_level: `medium`
- execution_model: `gpt-5.6-terra`
- execution_authorized: `true`
- route_reason: `38 项跨域语义审计，需要分批计划和统一评分口径`
- escalation_triggers: `scope_expanded | input_conflict | risk_increased | verification_failed_twice | human_gate`

## 目标

建立 38 个 Skill 的动态清单、逐项评分 rubric、基线审计表和后续分批优化输入。

## 允许范围

- `.factory/workitems/SKILL-FULL-OPTIMIZATION-001/**`
- 只读 `skills/**`、现有测试和当前项目合同。

## 禁止动作

- 本任务未形成计划前不修改 `skills/**`。
- 不新增注册表、运行时、依赖、SHA 快照或远端动作。

## 预期输出

- 完整 brief。
- 100 分制单项评分 rubric。
- 38 项基线清单与分批计划输入。

## 验证命令

```bash
for skill in skills/*; do uv run python /Users/uroborus/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$skill"; done
```

期望：动态发现的 38 个 Skill 全部验证成功，基线报告包含 38 个唯一名称。
