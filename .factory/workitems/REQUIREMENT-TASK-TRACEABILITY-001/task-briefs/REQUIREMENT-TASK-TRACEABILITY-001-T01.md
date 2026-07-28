# REQUIREMENT-TASK-TRACEABILITY-001-T01 需求分析条件化

## 工作项

- 工作项：`REQUIREMENT-TASK-TRACEABILITY-001`
- 任务：`REQUIREMENT-TASK-TRACEABILITY-001-T01`
- 状态：`approved`
- 任务层级：`requirement`
- 关联目标：`REQ-RTT-001`
- 上游计划：`.factory/workitems/REQUIREMENT-TASK-TRACEABILITY-001/plan.md`
- 流水账：`.factory/workitems/REQUIREMENT-TASK-TRACEABILITY-001/ledger.jsonl`

## 目标

让需求分析内容始终存在，但独立 `requirements-analysis.md` 只在复杂度、风险或独立评审需要时生成。

## 输入

- 已批准需求：`REQ-RTT-001`
- 工作项简报：`.factory/workitems/REQUIREMENT-TASK-TRACEABILITY-001/brief.md`

## 允许修改

- `skills/requirements-engineering/SKILL.md`
- `skills/requirements-engineering/references/prd-template.md`
- `skills/document-templates/SKILL.md`
- `skills/document-templates/references/repository-structure.md`
- `skills/document-templates/references/document-catalog.md`
- `skills/document-templates/references/traceability-and-gates.md`
- `skills/document-templates/assets/templates/02-requirements/requirements-analysis.md`
- `tests/test_requirements_analysis_mode_contract.py`
- `.factory/workitems/REQUIREMENT-TASK-TRACEABILITY-001/**`

## 禁止修改

- PM 页面和 SQLite schema。
- 用户已有未归属本任务的脏改动。
- Git 远端和部署。

## 验证命令

```bash
uv run pytest -q tests/test_requirements_analysis_mode_contract.py tests/test_requirements_engineering_skill.py tests/test_sf_sp_010_documentation_navigation.py
```

## 完成口径

- 合同测试由红转绿。
- 实现者只能推进到 `ready_for_review`。
