# TASK-SKILL-004-P001 黑盒验证记录

## 场景

- evaluator：`/root/task_skill_004_blackbox_eval`
- 模式：fresh-context、只读；未参与计划或实现。
- 允许读取：`AGENTS.md`、`using-shanforge`、共享回写合同、`api-design`。
- 禁止读取：本任务 plan、brief、evidence、review、memory、ledger 和实现者总结。
- 输入：项目化 work item 中 `api-design` 完成 API 契约草案，题设声称本地 `status=ready_for_review`、`needs=review`；要求区分工作结果和总控状态信封。

## 观察

- `api-design` 本职结果包含 `work_item/task_id/task_type/skill/status/outputs/evidence/ledger_event/needs`，不包含五个项目级字段。
- 评估者发现题设的 `ready_for_review/review` 不属于 `api-design` 当前本地 `status/needs` 枚举，并拒绝为了统一状态包改写专业输出。
- `using-shanforge` 接收执行事实后补 `project_position/completion_level/stop_reason/scope_remaining/next_required_action`。
- 工作 Skill 的 `needs_user_input` 不自动等于项目 human Gate；总控结合 ledger、授权范围和真实 Gate 决定。
- `direct_answer` 与 `lightweight_analysis` 不使用工作 Skill 状态包或项目状态信封。

## 评分

```text
BB-001: 2/2 - 工作 Skill 本职结果排除 5 个项目字段
BB-002: 2/2 - 识别并拒绝归一化 api-design 的本地枚举
BB-003: 2/2 - 总控补齐 5 个项目字段
BB-004: 2/2 - needs_user_input 不自动等于 human Gate，owner 正确
BB-005: 2/2 - direct/lightweight 不使用状态包
Total: 10/10
Result: pass
```

## 执行审计

Files read：

- `AGENTS.md`
- `skills/using-shanforge/SKILL.md`
- `skills/using-shanforge/references/work-skill-return-contract.md`
- `skills/api-design/SKILL.md`

Files written：无。

Commands run：

```text
cat AGENTS.md && cat skills/using-shanforge/SKILL.md && cat skills/using-shanforge/references/work-skill-return-contract.md && cat skills/api-design/SKILL.md
```
