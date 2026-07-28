# REQUIREMENT-TASK-TRACEABILITY-001-T02 任务分层与提取

## 工作项

- 工作项：`REQUIREMENT-TASK-TRACEABILITY-001`
- 任务：`REQUIREMENT-TASK-TRACEABILITY-001-T02`
- 状态：`approved`
- 任务层级：`requirement`
- 关联目标：`REQ-RTT-002`
- 上游计划：`.factory/workitems/REQUIREMENT-TASK-TRACEABILITY-001/plan.md`
- 流水账：`.factory/workitems/REQUIREMENT-TASK-TRACEABILITY-001/ledger.jsonl`

## 目标

让正式任务声明四类任务层级，并将合法 `task_scope` 投影到现有任务实体详情。

## 输入

- 已批准需求：`REQ-RTT-002`
- 工作项简报：`.factory/workitems/REQUIREMENT-TASK-TRACEABILITY-001/brief.md`

## 允许修改

- `skills/writing-plans/SKILL.md`
- `skills/writing-plans/references/task-brief-template.md`
- `src/runtime/project_knowledge/extractors.py`
- `tests/test_project_knowledge_extractors.py`
- `tests/test_task_scope_contract.py`
- `.factory/workitems/REQUIREMENT-TASK-TRACEABILITY-001/**`

## 禁止修改

- `src/settings/project_knowledge/schema.py`
- `.factory/project-knowledge/relation-declarations.json`
- PM 页面和用户已有未归属本任务的脏改动。
- Git 远端和部署。

## 验证命令

```bash
uv run pytest -q tests/test_task_scope_contract.py tests/test_project_knowledge_extractors.py tests/test_writing_plans_skill.py tests/test_system_task_contracts.py::test_system_task_record_has_non_negative_monotonic_heads_and_zero_progress
```

## 完成口径

- 合法层级进入 `details.task_scope`，非法值被明确拒绝。
- 合同测试覆盖 `requirement`、`cross_cutting`、`project` 的关联规则和 `system` 的零产品进度规则。
- 实现者只能推进到 `ready_for_review`。
