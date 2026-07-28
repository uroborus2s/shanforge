# T02 验证证据

## Red

```text
uv run pytest -q tests/test_task_scope_contract.py
1 failed

uv run pytest -q \
  tests/test_project_knowledge_extractors.py::test_markdown_task_brief_projects_declared_task_scope_and_targets \
  tests/test_project_knowledge_extractors.py::test_markdown_task_brief_rejects_unknown_task_scope
2 failed
```

预期失败：计划 Skill 和任务模板没有四类层级合同；提取器没有 `task_scope` 字段及枚举校验。

## Green

```text
uv run pytest -q tests/test_task_scope_contract.py \
  tests/test_project_knowledge_extractors.py \
  tests/test_writing_plans_skill.py \
  tests/test_system_task_contracts.py::test_system_task_record_has_non_negative_monotonic_heads_and_zero_progress
31 passed
```

## 覆盖

- 四类任务层级及各自关联规则。
- `system` 零产品进度既有契约。
- 合法 `task_scope` 和关联目标提取。
- 非法 `task_scope` 拒绝。
