# 任务简报

## 工作项

- 工作项：`MODEL-ROUTING-001`
- 任务：`MODEL-ROUTING-001-T02`
- 状态：`draft`
- 优先级：`P0`
- 任务层级：`cross_cutting`
- 关联目标：`MODEL-ROUTING-001`
- 强关系：`DEPENDS_ON MODEL-ROUTING-001-T01`
- 上游计划：`.factory/workitems/MODEL-ROUTING-001/plan.md`

## 目标

以 Sol 作为唯一总体设计与控制模型，确定性判断任务复杂度和风险，并把执行任务授权给 Terra 或 Luna；执行模型不得修改路由等级、扩大范围或自批完成。

## 允许修改

- `docs/05-design/workflow-execution-design.md`
- `docs/02-user-guide/user-guide.md`
- `skills/using-shanforge/SKILL.md`
- `skills/using-shanforge/agents/openai.yaml`
- `skills/writing-plans/SKILL.md`
- `skills/writing-plans/references/task-brief-template.md`
- `skills/subagent-driven-development/SKILL.md`
- `tests/test_model_tier_routing.py`
- `.factory/workitems/MODEL-ROUTING-001/**`

## 禁止修改

- 模型 API、价格、配额或宿主配置。
- 平台运行时、服务、数据库或依赖。
- 远端和生产状态。

## 验证命令

```bash
uv run pytest -q tests/test_model_tier_routing.py tests/test_task_workflow_semantics.py tests/test_execution_workflow_skills.py
```

## 完成口径

正反例和升级路径通过，且相邻流程合同无回归。
