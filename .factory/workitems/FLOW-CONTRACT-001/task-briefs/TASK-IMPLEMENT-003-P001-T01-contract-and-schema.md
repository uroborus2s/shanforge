# T01 合同内核与 39 表 Schema

## 工作项

- 工作项：`FLOW-CONTRACT-001`
- 任务：`TASK-IMPLEMENT-003-P001-T01`
- 状态：`ready_for_review`
- 上游计划：`.factory/workitems/FLOW-CONTRACT-001/plans/TASK-IMPLEMENT-003-P001.md`

## 目标

交付 Project Knowledge 不可变合同、精确 39 表 DDL、2 张 FTS 虚拟表、schema 校验器和 R009 137 字段 map 启动校验。

## 允许修改

- `src/domain/project_knowledge/`
- `src/application/project_knowledge/ports.py`
- `src/settings/project_knowledge/schema.py`
- `tests/test_project_knowledge_schema.py`
- `tests/test_project_knowledge_contracts.py`
- 当前任务 evidence/report/review/ledger 和记忆摘要

## 禁止修改

- `TASK-IMPLEMENT-002-R001` 候选、远端、部署和无关脏文件。
- access、renderer 和正式文档；它们属于后续切片。

## 测试与验证

先确认目标测试因模块缺失失败，再最小实现：

```bash
PYTHONPATH=src uv run pytest tests/test_project_knowledge_schema.py tests/test_project_knowledge_contracts.py -q
```

完成要求：39 表集合精确、2 FTS、关键非法写入拒绝、137 field ID 恰映射一次。实现者只能进入 `ready_for_review`。
