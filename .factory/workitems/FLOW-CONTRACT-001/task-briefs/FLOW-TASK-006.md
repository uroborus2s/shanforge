# FLOW-TASK-006 升级项目记忆

## 工作项

- 工作项：`FLOW-CONTRACT-001`
- 任务：`FLOW-TASK-006`
- 状态：`draft`
- 上游计划：`.factory/workitems/FLOW-CONTRACT-001/plan.md`
- 流水账：`.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`

## 目标

让 `project-memory` 明确 docs、work item、memory、PM 视图的事实源优先级，并固定 summary 不复制正式正文。

## 输入

- `skills/project-memory/SKILL.md`
- `.factory/memory/doc-map.md`
- 流程契约需求文档。

## 允许修改

- `skills/project-memory/SKILL.md`
- `skills/project-memory/references/*.md`
- `.factory/memory/doc-map.md`
- 相关测试。

## 验证命令

```bash
uv run pytest tests/test_project_memory_skill.py
```

期望输出：

```text
通过；新增事实源优先级和 PM generated 非事实源断言。
```

## 完成口径

不得把 `.factory/pm/generated/status-dashboard.html` 作为唯一事实源。
