# SKILL-CLEANUP-001-T01 Index 快照验证

- 时间：`2026-07-27`
- 快照：`/tmp/shanforge-skill-cleanup-index-lZyN04`
- 结论：任务范围通过；3 个 HEAD 基线失败已隔离。

## 完整目标结果

在仅包含 HEAD 与当前 staged diff 的快照中运行 4 个相关测试文件：

- `13 passed`
- `3 failed`

三个失败均可由 HEAD 单独证明为本任务前既存：

1. 两个测试要求 `src/runtime/skills` 与 `src/settings/skills` 不存在，但这 6 个路径仍由 HEAD 跟踪；相关工作树删除属于其他工作项。
2. `document-templates` 当前专业正文已由其他工作项修改，而本任务精确 staged 快照保留 HEAD 的旧 digest。

本任务未暂存上述实现或共享 digest 变化。

## 任务隔离验证

排除上述三个基线断言后：

```text
13 passed, 3 deselected in 0.03s
```

同时验证：

- 4 个相关测试文件 Ruff：`All checks passed!`
- staged Skill 集合：`37`
- `go-developer` 专业正文 digest：匹配
- `git diff --cached --check`：通过
- 两个 WorkItem ledger：JSONL 有效

## Staging 边界

`tests/test_work_skill_status_envelope_ownership.py` 的 staged 内容仅包含：

- `go-backend-developer` 改为 `go-developer` 及 digest 更新；
- 删除 `skill-creator` digest；
- `exactly_32` 改为 `exactly_31`。

`document-templates`、`ui-ux-pro-max` digest 与
`tests/test_deprecated_skill_cleanup.py` 当前工作树 diff 均未暂存。
