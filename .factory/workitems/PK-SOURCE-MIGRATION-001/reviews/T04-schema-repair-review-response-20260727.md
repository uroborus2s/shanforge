# PK T04 Schema 修复评审回应

## Fixed I1

复用 `_TASK_BRIEF_TITLE_LINE`，让 `_task_brief_details` 在同行字段解析前跳过任务身份行。
`## Task` 语义章节仍由同一别名表处理；`- Task: <task-id>` 不再生成 `goal`。

Verified:

- 新增身份字段负例：RED `1 failed`，GREEN 聚焦 `3 passed`。
- 项目知识五文件：`66 passed in 1.05s`。
- Ruff format/lint、Mypy 290 source：通过。
- 最终快照与 Chrome 5 页 × 2 视口：通过。

## Fixed I1-test

新增明确使用 `## Task` 的正例，与 `- Task: <task-id>` 身份负例共同锁定上下文分离。
生产代码未变化。

Verified:

- Task 身份负例 + Task 章节正例：`2 passed in 0.08s`。
- 项目知识五文件：`67 passed in 0.94s`。
- Ruff format/lint、Mypy 290 source：通过。
