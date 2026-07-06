# FLOW-TASK-001 固化流程契约需求

## 工作项

- 工作项：`FLOW-CONTRACT-001`
- 任务：`FLOW-TASK-001`
- 状态：`ready_for_review`
- 上游计划：`.factory/workitems/FLOW-CONTRACT-001/plan.md`
- 流水账：`.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`

## 目标

把用户讨论落为正式需求文档，覆盖四类场景、三层文档、baseline、领域模块、前后端设计、版本管理、PM 和防跳步机制。

## 输入

- 用户本轮讨论。
- `skills/requirements-engineering/SKILL.md`
- `skills/document-templates/SKILL.md`

## 允许修改

- `docs/04-project-development/03-requirements/process-workflow-contract-requirements.md`
- `docs/index.md`
- `.factory/memory/doc-map.md`
- `.factory/memory/tasks.summary.md`

## 验证命令

```bash
git diff --check
```

期望输出：

```text
无 trailing whitespace 或 patch 格式错误。
```

## 完成口径

实现者只能写 `ready_for_review`。`approved` 必须来自独立评审。
