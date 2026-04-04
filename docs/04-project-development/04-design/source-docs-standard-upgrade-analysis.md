# 源文档标准升级分析

**项目名称：** 山海工枢 / shanforge  
**负责人：** 仓库维护者  
**主要读者：** 架构 | 文档维护者 | 脚本维护者 | 历史项目纳管负责人  
**上游输入：** `docs-stratego` 最新《源文档标准》 | 当前 `factory-*` 脚本 | 现有 `docs/` 正式文档结构  
**下游输出：** `implementation-plan.md` | 脚本改造 | 存量项目刷新方案  
**最后更新：** 2026-04-03

## 1. 变更摘要

最新《源文档标准》相对当前山海工枢工具链，新增或强化了以下约束：

- 根 `docs/index.md` 的 front matter 成为目录树、页面路径和访问级别的唯一事实源。
- 页面节点除了 Markdown，还允许直接指向 `*.openapi.*` 和 `*.mcp-tools.*`。
- 契约文件必须放在真实文档目录下，并与所在目录的 `index.md` 配套。
- 子目录 `index.md` 只保留正文首页职责，不再重复维护页面清单或推荐阅读顺序。
- 构建器需要对 OpenAPI 和 MCP tools 快照做最小结构校验。

## 2. 当前工具符合性判断

| 能力项 | 当前工具 | 判断 | 说明 |
|---|---|---|---|
| 根 `docs/index.md` 作为唯一导航入口 | `document-templates` skill + `docs-stratego source validate` | 已满足 | 根导航由 skill 维护，合规性由 CLI 校验。 |
| 子目录 `index.md` 不再声明导航 | `document-templates` skill + `docs-stratego source validate` | 已满足 | 目录首页只保留正文职责。 |
| 契约文件纳入自动发现与导航 | `document-templates` skill | 已满足 | skill 已明确 `*.openapi.*`、`*.mcp-tools.*` 的放置规则。 |
| 契约文件最小结构校验 | `docs-stratego source validate` | 已满足 | 统一交由 `docs-stratego` CLI 做最小结构检查。 |
| 目录首页不再重复页面清单 | 目录首页生成逻辑 | 原先不满足，本轮已补齐 | 原先会生成“建议阅读顺序”，现改为范围/边界说明。 |
| 自定义首页正文保留 | 根/目录 `index.md` 合并逻辑 | 已满足 | 既有人工正文仍保留。 |
| 页面访问级别以根导航为准 | 根索引刷新逻辑 | 已满足 | 当前已保留 `home_access` 与页面级 `access`/`title`。 |
| 源仓维护目录分组与顺序 | 根索引刷新逻辑 | 基本满足 | 现在会保留以真实目录概览页为锚点的人工分组、标题与顺序。 |
| 一键升级到最新标准 | `document-templates` skill + CLI 校验 | 已重构 | 不再保留仓内专用升级脚本。 |

## 3. 本轮设计决策

### 3.1 已落地

- 文档重构流程统一收口到 `document-templates` skill。
- 文档合规校验统一收口到 `docs-stratego source validate`。
- 聚合站点接入、通知脚手架、同步、构建与预览统一收口到 `docs-stratego` CLI。
- 仓内 `factory-docs-*` 旧命令不再作为正式流程保留。

### 3.2 仍保留为后续任务

- 当前导航合并依赖“目录概览页”推断真实目录锚点。
- 若手工写出完全脱离真实目录结构的包装分组，仍需要人工复核。

## 4. 对现有命令的影响

| 命令 | 影响 | 结论 |
|---|---|---|
| `factory-docs-index-refresh` | 旧的仓内 docs 刷新入口 | 退场 |
| `factory-docs-migrate-structure` | 旧的仓内 docs 迁移入口 | 退场 |
| `factory-docs-profile-detect` | 旧的仓内 docs 画像入口 | 退场 |
| `factory-docs-standard-upgrade` | 旧的仓内 docs 升级入口 | 退场 |
| `docs-stratego source validate` | 源仓文档合规校验 | 保留，作为正式校验入口 |
| `docs-stratego source add/remove/scaffold-notify` | 聚合站点接入与通知脚手架 | 保留 |
| `docs-stratego sync/build/dev` | 聚合站点同步、构建与预览 | 保留 |

补充边界：

- 本仓库内的文档内容维护，正式入口是 `document-templates` skill。
- `docs-stratego` CLI 承担源仓校验、聚合站点接入、通知脚手架、同步、构建和预览。
- 结论上，这一层已经从“山海工枢本地 docs 脚本 + docs-stratego 边界分层”改成“文档 skill + docs-stratego CLI”。

## 5. 对使用山海工枢项目的影响

对使用山海工枢开发的项目，最新标准意味着：

- 只要项目内出现 `openapi/` 或 `tools/` 契约目录，根 `docs/index.md` 就必须纳入对应页面节点。
- 如果项目需要“私有目录下公开某个契约页面”，必须在根 `docs/index.md` 上设置该页面节点的 `access`，不能只靠目录名。
- 存量项目在刷新后，需要人工复核一次根索引中的页面级权限例外，尤其是公开 API 与私有设计目录并存的场景。

## 6. 结论

结论分两层：

- 从“正式入口”看：仓内旧 docs 处理脚本已经退出主路径，文档维护统一改走 `document-templates` skill，命令执行统一改走 `docs-stratego` CLI。
- 从“还剩什么边角”看：仍然需要人工复核“完全脱离真实目录锚点的包装分组”和页面级权限例外。

## 7. 变更记录

| 日期 | 变更内容 | 变更人 |
|---|---|---|
| 2026-04-01 | 初始版本，完成《源文档标准》升级分析并登记本轮改造结论 | Codex |
| 2026-04-01 | 补充导航合并与统一升级入口落地结论 | Codex |
| 2026-04-03 | 明确本地 docs 维护入口与 `docs-stratego` CLI 校验/聚合入口的分层边界 | Codex |
