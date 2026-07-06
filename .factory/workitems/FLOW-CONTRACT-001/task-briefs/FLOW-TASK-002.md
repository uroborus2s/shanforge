# FLOW-TASK-002 固化流程契约实施方案

## 工作项

- 工作项：`FLOW-CONTRACT-001`
- 任务：`FLOW-TASK-002`
- 状态：`ready_for_review`
- 上游计划：`.factory/workitems/FLOW-CONTRACT-001/plan.md`
- 流水账：`.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`

## 目标

写完整实施方案，包含业务流程管控、skill 调用图、运行时文档设计、每个 skill 的输入输出、每个 skill 的内部流程和任务拆解。

## 输入

- `docs/04-project-development/03-requirements/process-workflow-contract-requirements.md`
- `docs/04-project-development/05-development-process/superpowers-workflow-integration-plan.md`
- 相关 workflow skill。

## 允许修改

- `docs/04-project-development/05-development-process/process-workflow-contract-implementation-plan.md`
- `docs/04-project-development/05-development-process/index.md`
- `.factory/workitems/FLOW-CONTRACT-001/plan.md`

## 验证命令

```bash
git diff --check
```

期望输出：

```text
无 trailing whitespace 或 patch 格式错误。
```

## 完成口径

方案只能进入 `ready_for_review`，不能自批为 approved。
