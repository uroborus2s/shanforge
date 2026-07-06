# FLOW-TASK-010 增加 baseline 设计模板

## 工作项

- 工作项：`FLOW-CONTRACT-001`
- 任务：`FLOW-TASK-010`
- 状态：`draft`
- 上游计划：`.factory/workitems/FLOW-CONTRACT-001/plan.md`
- 流水账：`.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`

## 目标

为领域划分、后端模块、数据库、API 和前端 UI 建立正式模板。

## 输入

- `skills/document-templates/SKILL.md`
- 流程契约需求文档。

## 允许修改

- `skills/document-templates/references/project-baseline-template.md`
- `skills/document-templates/references/backend-module-design-template.md`
- `skills/document-templates/references/database-design-template.md`
- `skills/document-templates/references/api-design-template.md`
- `skills/document-templates/references/frontend-ui-design-template.md`
- 相关 tests。

## 验证命令

```bash
uv run pytest tests/test_sf_sp_010_documentation_navigation.py
```

期望输出：

```text
通过；新增模板结构断言时同步执行。
```

## 完成口径

模板必须包含中文版本信息和版本历史；数据库模板必须包含 ERD；API 模板必须引用 `openapi.yaml`。
