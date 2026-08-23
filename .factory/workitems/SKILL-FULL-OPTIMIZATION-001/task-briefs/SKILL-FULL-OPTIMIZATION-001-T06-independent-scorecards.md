# T06 独立逐项评分

- 工作项：`SKILL-FULL-OPTIMIZATION-001`
- 任务：`SKILL-FULL-OPTIMIZATION-001-T06`
- 状态：`completed`
- 优先级：`P0`
- 任务层级：`system`
- 关联目标：`SKILL-FULL-OPTIMIZATION-001`
- 强关系：`N/A`

## 模型路由

- control_model: `gpt-5.6-sol`
- task_complexity: `complex`
- risk_level: `medium`
- execution_model: `gpt-5.6-terra`
- execution_authorized: `true`
- route_reason: `用户要求 38 项独立评分，需要集中 reviewer 质量门`
- escalation_triggers: `scope_expanded | input_conflict | risk_increased | verification_failed_twice | human_gate`

## 目标

由未参与实现的独立 reviewer 为 38/38 Skill 分别输出五维得分、总分、C/I/M、结论和证据；所有 Skill 达到 `>=90 / C0-I0` 后方可通过。
