# 实现批次评审前验证

## 自动测试

```text
37 passed in 0.28s
```

覆盖：

- 条件化需求分析合同。
- 四类任务层级及关联合同。
- Markdown 任务简报提取。
- requirements-engineering、writing-plans 相邻合同。
- document-templates 相关导航合同。
- system task 零产品进度合同。

## 静态检查

```text
ruff check: All checks passed
ruff format --check: 4 files already formatted
```

## Skill 校验

```text
requirements-engineering: Skill is valid
document-templates: Skill is valid
writing-plans: Skill is valid
```

## 完整性

- WorkItem ledger：有效 JSONL。
- scoped `git diff --check`：通过。
- 共享脏改动：未修改、未纳入本任务。
