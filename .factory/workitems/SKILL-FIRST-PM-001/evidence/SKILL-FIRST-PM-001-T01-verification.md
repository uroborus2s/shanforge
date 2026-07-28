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
