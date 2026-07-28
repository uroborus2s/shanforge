# SKILL-FIRST-PM-001-T01 验证证据

时间：2026-07-29T00:04:39+08:00

## 边界结果

- `src/` 不存在。
- `AGENTS.md`、`README.md`、`skills/`、`docs/`、`.factory/memory/` 中不存在有效的
  `PYTHONPATH=src` 或 `settings.composition.project_knowledge` 调用。
- `using-shanforge` 中不存在 Shanforge 本机绝对路径。

## 自动验证

- 快照及关联 skill 合同测试：`29 passed`
- Ruff check：通过
- Ruff format check：通过
- Mypy：通过
- `uv lock --check`：通过
- `using-shanforge` skill quick validation：通过
- `project-memory` skill quick validation：通过
- 独立复审：`approved / critical=0 / important=0 / minor=0`

## ITA Club 实跑

- 输出：`/Users/uroborus/NodeProject/ita-club/.factory/cache/site/current/index.html`
- receipt：`SkillProjectSnapshotReceipt/v1`
- generation：`86a2c1f9a27a88303c115491150042aa8c31503bdb710361114f13cc3bca4951`
- source_count：63
- 第二次运行：`cache_hit=true`
- 页面统计：7 个工作项、1 个正在推进、0 个需要关注、5 个已完成

## 全仓回归说明

删除 runtime-only 测试后，全仓回归为 `212 passed, 7 failed`。7 个失败均指向本次任务开始前
已存在的其他脏工作项事实冲突或 skill 文本漂移；本任务不修改这些范围，详见实现报告。

## 首轮审查修复验证

- 使用 `--relative-paths` 代替会造成脱敏误解的 profile。
- 缓存冲突返回失败 receipt，不输出 traceback。
- `.factory`、所有输入和输出解析后必须仍位于目标项目根目录。
- ITA Club 计划正文已删除旧跨仓运行时方案。
- 当前数据设计、运维手册、设计入口和 doc-map 已切换到 skill-first。
- 删除前 `src/` 备份：`/private/tmp/shanforge-src-before-delete-20260728T2350.tar.gz`。

## 看板重新验收

用户批准终止 `PM-DASHBOARD-004` 旧 runtime 路线后，剩余看板验收在本脚本上完成：

- 首屏显示当前重点、工作项目标、当前任务和下一步。
- 工作项按需要关注、正在推进、后续待办、已完成分组。
- 当前任务显示层级、优先级、需求关系、任务目标和完成标准。
- 无 brief/ledger 的分组目录不显示；原始 ID 和状态位于折叠技术区。
- `needs_user_input` 位于需要关注；`superseded` 位于已完成归档。

最终 receipt：

| 项目 | generation | source_count | 第二次运行 |
|---|---|---:|---|
| Shanforge | `a545bfac18f4a0234fc52171834403f9935ded4700a219c5f76fb9e794230bd6` | 224 | `cache_hit=true` |
| ITA Club | `86a2c1f9a27a88303c115491150042aa8c31503bdb710361114f13cc3bca4951` | 63 | `cache_hit=true` |

浏览器验收：

| 测试 | 项目 | 视口 | 结果 |
|---|---|---|---|
| `TEST-UI-PM-001` | Shanforge | 390×844 | 通过 |
| `TEST-UI-PM-002` | Shanforge | 1440×900 | 通过 |
| `TEST-UI-PM-003` | ITA Club | 390×844 | 通过 |
| `TEST-UI-PM-004` | ITA Club | 1440×900 | 通过 |

四组均为页面级横向 overflow `0`、console/page errors `0`，并通过首个 Tab 聚焦跳转
链接、Enter 跳到 `#main`、键盘打开归档区。静态 HTML 无服务进程，端口、健康检查和
关闭方式均为 `N/A`。截图位于 `evidence/browser/`。

首次最终浏览器进程在读取 `#focus-title` 时超时并被终止；确认两个最终 HTML 均包含该
元素后，对相同文件完整重跑，4/4 通过。

## 完成层级

- 任务结论：`passed`
- 完成层级：`task`
- 项目级全仓回归：`212 passed / 7 failed`
- 7 项失败属于已登记的范围外事实或测试漂移，不影响本任务结论，也未被越界修复。
- API：`N/A`，本任务不提供 API。
