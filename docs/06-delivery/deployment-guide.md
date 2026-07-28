# 部署手册

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `OPS-DEPLOYMENT-GUIDE-001` |
| 正式版本 | `v4.0.0` |
| 来源候选 | `SKILL-FIRST-PM-001` |
| 负责人 | `HUMAN_RELEASE_OPERATIONS_LEAD` |
| 修改 / 审核 / 批准 | `uroborus` / `uroborus` / `uroborus` |
| 状态 | 已批准并生效 |

## 当前交付形态

Shanforge 不部署服务，也不向目标项目安装 Python runtime。交付单元是完整 skill 目录。

使用仓库同步入口：

```bash
uv run python scripts/sync-codex-skills
```

该命令把每个 skill 目录链接到已配置的 Codex、Gemini CLI 和 Agents skill 目录，
因此 `SKILL.md`、`references/` 与 `scripts/` 同步生效。

## 验证

```bash
python3 tests/test_using_shanforge_snapshot.py
uv run pytest -q
uv run ruff check skills tests scripts
uv lock --check
git diff --check
```

项目状态快照从已安装 `using-shanforge` skill 目录运行
`scripts/project_snapshot.py --project-root <目标项目>`。目标项目不需要 Shanforge
源码仓保持存在。

## 回滚

本地 skill 通过符号链接同步时，回滚使用 Git 恢复上一提交。缓存位于目标项目
`.factory/cache/site/`，可以删除重建；正式项目事实不得随缓存删除。

## 正式版本历史

| 版本 | 日期 | 变更 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v4.0.0` | 2026-07-28 | 改为 skill 目录交付，移除 Python runtime 部署 | `uroborus` | `uroborus` | `uroborus` |
| `v3.1.0` | 2026-07-20 | 旧 Python 平台工作区本地验证边界 | `AI_EXECUTOR` | 独立 Reviewer | `uroborus` |
