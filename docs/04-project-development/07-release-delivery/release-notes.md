# 发布说明

## 1. 文档目标

汇总本次发布的新增能力、修复项、影响范围和升级说明。

## 2. 当前版本发布摘要

**版本标识：** `2026-04-03-docs-cli-refactor`
**发布日期：** 2026-04-03
**交付范围：** 当前仓库 `docs/`、共享脚本、Python 基线、测试回归

### 2.1 主要变更

- Python 工程基线提升到 `3.14`，并在仓库中显式声明
- 文档正式流程统一改为 `document-templates` skill + `docs-stratego` CLI
- `factory-init` 与历史项目纳管默认只补根 `docs/index.md` 和顶层模块 `index.md`
- `factory-state-doctor` 改为直接调用 `docs-stratego source validate`

### 2.2 影响范围

- 共享脚本使用者
- 需要迁移旧 `docs/` 结构的历史项目
- 依赖章略·墨衡读取 `docs/index.md` 的文档站点

### 2.3 升级注意事项

- 旧项目不再使用 `factory-docs-*` 命令；统一改用 `document-templates` skill 重构后执行 `docs-stratego source validate`
- 根 `docs/index.md` 现在由文档维护者手工维护导航，不再依赖仓内自动合并
- 如果需要更深层的目录首页脚手架，应在 `docs-stratego` CLI 演进后统一补充，不再在山海工枢内平行实现

### 2.4 回滚入口

如果本轮变更导致外部项目异常，可回退对应脚本和文档模板修改，并重新执行回归测试与结构检查。

## 3. 推荐表格

| 类别 | 编号 / 模块 | 变更内容 | 影响范围 | 是否需要迁移 |
|---|---|---|---|---|
| 基线升级 | `pyproject.toml` / `.python-version` | Python 基线切到 `3.14` | 全部使用者 | 是 |
| 脚本收口 | `factory-state-doctor` | 文档校验改走 `docs-stratego source validate` | 全部使用者 | 否 |
| 模板升级 | `factory-init` / `factory-historical-project-onboarding` | 新项目与纳管项目改为根索引 + 顶层 index 初始化 | 新项目 / 历史项目 | 否 |
| 文档重构 | 当前仓库 `docs/*` | 同步为 skill + CLI 流程 | 当前仓库读者 | 否 |
