# FLOW-TASK-003 升级文档治理规则

## 工作项

- 工作项：`FLOW-CONTRACT-001`
- 任务：`FLOW-TASK-003`
- 状态：`draft`
- 上游计划：`.factory/workitems/FLOW-CONTRACT-001/plan.md`
- 流水账：`.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`

## 目标

让 `document-templates` 固定正式文档、临时文档、中文版本信息、版本历史和导航同步规则。

## 输入

- 正式需求：`docs/04-project-development/03-requirements/process-workflow-contract-requirements.md`
- 正式实施方案：`docs/04-project-development/05-development-process/process-workflow-contract-implementation-plan.md`
- `skills/document-templates/SKILL.md`

## 允许修改

- `skills/document-templates/SKILL.md`
- `skills/document-templates/references/repository-structure.md`
- `skills/document-templates/references/*template*.md`
- 相关结构测试。

## 禁止修改

- 旧中心脚本。
- 与文档治理无关的 skill。

## 验证命令

```bash
uv run pytest tests/test_sf_sp_010_documentation_navigation.py
```

期望输出：

```text
通过；新增断言覆盖正式文档登记和版本历史。
```

## 完成口径

实现者只能写 `ready_for_review`。
