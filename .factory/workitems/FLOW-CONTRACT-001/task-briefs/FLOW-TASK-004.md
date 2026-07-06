# FLOW-TASK-004 升级需求工程流程

## 工作项

- 工作项：`FLOW-CONTRACT-001`
- 任务：`FLOW-TASK-004`
- 状态：`draft`
- 上游计划：`.factory/workitems/FLOW-CONTRACT-001/plan.md`
- 流水账：`.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`

## 目标

让 `requirements-engineering` 支持四类场景、需求版本、影响分析、领域模块映射和 baseline 变更建议。

## 输入

- `skills/requirements-engineering/SKILL.md`
- `skills/requirements-engineering/references/prd-template.md`
- 流程契约需求文档。

## 允许修改

- `skills/requirements-engineering/SKILL.md`
- `skills/requirements-engineering/references/prd-template.md`
- 相关结构测试。

## 验证命令

```bash
uv run pytest tests/test_superpowers_reference_migration.py
```

期望输出：

```text
通过；新增需求场景测试另行补充。
```

## 完成口径

缺场景覆盖时不得进入 review。
