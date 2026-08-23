# TASK-001 Verification

## 基本信息

- Work item：`DOC-FACTORY-RESTRUCTURE-001`
- Task：`TASK-001-destructive-full-doc-migration`
- Actor：用户授权代执行
- 时间：2026-07-08T19:48:30+08:00
- 状态：passed

## 验证命令与真实结果

```bash
uv run pytest tests/test_doc_factory_restructure.py
```

真实结果：

```text
9 passed in 0.01s
```

```bash
uv run pytest tests/test_doc_factory_restructure.py tests/test_project_memory_skill.py tests/test_project_management_control_plane.py tests/test_sf_sp_010_documentation_navigation.py tests/test_superpowers_reference_migration.py tests/test_execution_workflow_skills.py tests/test_black_box_workflow_eval.py tests/test_pr_commit_workflow_rules.py tests/test_independent_review_gate.py tests/test_deprecated_skill_cleanup.py tests/test_brainstorming_skill.py
```

真实结果：

```text
72 passed in 0.08s
```

```bash
uv run ruff check tests/test_doc_factory_restructure.py tests/test_project_memory_skill.py tests/test_project_management_control_plane.py tests/test_sf_sp_010_documentation_navigation.py tests/test_superpowers_reference_migration.py tests/test_execution_workflow_skills.py tests/test_black_box_workflow_eval.py tests/test_pr_commit_workflow_rules.py tests/test_independent_review_gate.py tests/test_deprecated_skill_cleanup.py tests/test_brainstorming_skill.py
```

真实结果：

```text
All checks passed!
```

docs-stratego 初次运行：

```bash
uvx --from docs-stratego docs-stratego source validate --repo-path .
```

真实结果：

```text
failed to open file `/Users/uroborus/.cache/uv/sdists-v9/.git`: Operation not permitted
```

处理：按权限规则在沙箱外重跑同一命令。

docs-stratego 提升权限后运行：

```bash
uvx --from docs-stratego docs-stratego source validate --repo-path .
```

真实结果：

```text
shanforge: home_access=public pages=56 contracts=0 docs_root=/Users/uroborus/AiProject/shanforge/docs
```

```bash
jq empty .factory/memory/graph/traceability.json .factory/project.json .factory/tech-profile.json .factory/multi-agent-board.json
```

真实结果：exit code `0`，无输出。

```bash
git diff --check
```

真实结果：exit code `0`，无输出。

## 覆盖范围

- 任务执行契约已登记到根导航、项目开发首页、开发过程首页、文档索引和 doc-map。
- 旧 04 项目文档页面、旧静态原型、旧 `.factory/process`、旧 `.factory/memory/history`、旧 `.factory/pm/generated`、空资产索引和临时备份资产已删除。
- 当前正式入口不再引用已删除路径。
- `.factory/README.md` 已声明破坏性迁移规则和执行审计事实保留边界。
- 正式文档负责人、执行人和版本历史不署名为 `Codex`。
- `.factory/memory/graph/traceability.json`、`.factory/project.json`、`.factory/tech-profile.json`、`.factory/multi-agent-board.json` JSON 结构有效。
- 受迁移影响的旧测试口径已更新，不再要求已删除文档存在。

## 结论

`passed`
