# PK T04 最终验证失败证据（Iteration 2）

- 时间：`2026-07-27T19:30:00+08:00`
- status：`failed`
- 本轮在用户确认预览后尝试正式化；验证失败后已恢复候选态。

## 新鲜复现

```text
uv run pytest -p no:cacheprovider -q \
  tests/test_project_knowledge_extractors.py \
  tests/test_project_knowledge_index.py \
  tests/test_project_site_renderer.py \
  tests/test_project_knowledge_security.py \
  tests/test_project_knowledge_pm.py

exit code: 1
61 passed, 1 failed
```

失败节点：

`tests/test_project_knowledge_extractors.py::test_all_registered_task_briefs_project_a_work_item_entity`

四份已登记任务简报没有投影出 `goal / work_items / deliverables /
completion_conditions / verification` 任一字段：

1. `SKILL-CLEANUP-001-T01.md`
2. `iteration-6-minimal-acceptance-amendment.md`
3. `STATE-RECONCILIATION-001-T01.md`
4. `T06-mobile-hifi-art-direction.md`

单节点 `-vv` 复现同样失败。

## 边界证据

- Registry 会登记 `task-briefs/*.md` 的全部 Markdown。
- `_task_brief_details()` 只消费 `_TASK_BRIEF_FIELD_LINE` 或
  `_TASK_BRIEF_SECTION_KEYS` 能识别的字段。
- `_TASK_BRIEF_FIELD_LINE` 独立维护一份字段白名单，并要求冒号后同一行有非空值；
  `_TASK_BRIEF_SECTION_KEYS` 又维护另一份别名表。
- 新简报使用了空值后嵌套列表、`目的`、`本轮交付`、`决策` 等合法人类写法，
  但没有写侧 schema 或登记前验证阻止其进入 Registry。

## 未执行

因 pytest 已失败，没有继续把 Ruff、Mypy、文档发布验证或静态站点刷新写成通过。
