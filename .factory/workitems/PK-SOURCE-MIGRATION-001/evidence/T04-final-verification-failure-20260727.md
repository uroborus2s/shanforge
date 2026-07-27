# T04 最终验证失败证据（2026-07-27）

- Work item：`PK-SOURCE-MIGRATION-001`
- Task：`PK-SOURCE-MIGRATION-001-T04`
- Actor：`AI_EXECUTOR`
- 结论：`failed`

## 复现

```bash
uv run pytest tests/test_project_knowledge_extractors.py tests/test_project_knowledge_index.py tests/test_project_site_renderer.py tests/test_project_knowledge_security.py tests/test_project_knowledge_pm.py -q
```

- exit code：`1`
- passed：`61`
- failed：`1`
- errors：`0`
- skipped：`0`

失败用例：

```text
tests/test_project_knowledge_extractors.py::test_all_registered_task_briefs_project_a_work_item_entity
```

失败输入：

```text
.factory/workitems/UI-UX-FULL-EXAMPLE-001/task-briefs/T06-mobile-hifi-art-direction.md
```

该文件当前为未追踪文件，并被 `SRC-WORKITEM-BRIEF` 的
`**/task-briefs/*.md` include 自动纳入项目知识来源。

## 同轮其他结果

- Ruff：`All checks passed`，exit code `0`。
- Mypy：`Success: no issues found in 290 source files`，exit code `0`。
- 文档结构校验：exit code `0`。
- `git diff --check`：exit code `0`。
- 固定静态站点刷新：exit code `0`，
  `generation:238316458890a43d173a040c529b7294aa88561a83f7b8ba08d9ced3dcc10eeb`，
  `rendered_pages=15`，`reused_pages=2204`。

## 最小诊断

原始简报使用 `目的`、`本轮交付`、`禁止` 等行内字段。当前
`_TASK_BRIEF_FIELD_LINE` 不接受这些中文键，因此提取结果只有任务身份、标题和默认状态，
没有 `goal`、`deliverables` 等正式语义。

仅在内存中把 `目的` 改为 `目标`、把 `本轮交付` 改为 `交付结果` 后重新调用同一个
`MarkdownExtractor`，结果立即产生：

```text
goal=把现有移动端流程骨架升级为可开发、可验收的高保真界面……
deliverables=三套方向样张，每套包含首页、服务详情、订单详情。
```

诊断过程未修改该范围外任务简报。
