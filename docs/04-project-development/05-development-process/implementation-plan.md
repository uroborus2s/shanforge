# 实施计划

**项目名称：** 山海工枢 / shanforge  
**负责人：** 仓库维护者  
**主要读者：** 项目协调者 | 文档维护者 | 脚本维护者 | QA  
**上游输入：** `source-docs-standard-upgrade-analysis.md` | 最新《源文档标准》  
**下游输出：** 脚本改造 | 回归测试 | 存量项目刷新执行清单  
**最后更新：** 2026-04-03

## 1. 目标

把山海工枢当前文档工具链升级到可支撑最新《源文档标准》的状态，并给所有使用山海工枢开发的项目提供统一、可重复执行的 `docs/` 刷新路径。

## 2. 任务清单

| 任务 ID | 任务名称 | 主要输出 | 状态 |
|---|---|---|---|
| `TASK-006` | 支持契约页面自动索引与校验 | `factory_core.py` 支持 `*.openapi.*`、`*.mcp-tools.*` 自动发现与最小校验 | 已完成 |
| `TASK-007` | 调整目录首页生成策略 | 目录 `index.md` 不再生成推荐阅读清单，改为范围/边界说明 | 已完成 |
| `TASK-008` | 形成存量项目 docs 刷新方案 | 历史项目与在建项目的统一刷新步骤、命令序列与人工复核点 | 已完成 |
| `TASK-009` | 保留人工维护的导航分组与顺序 | 根 `docs/index.md` 从“重建 front matter”升级为“合并 front matter” | 已完成 |
| `TASK-010` | 将 docs 重构流程收口到 `document-templates` skill | skill 工作流、模板与现行说明 | 已完成 |
| `TASK-011` | 将 docs 命令入口收口到 `docs-stratego` CLI | `source validate`、`source add/remove/scaffold-notify`、`sync/build/dev` | 已完成 |

## 3. 本轮执行结果

### `TASK-006`

- 将源仓结构校验正式收口到 `docs-stratego source validate`
- 契约页面最小规则由 CLI 统一校验：
  - `*.md`
  - `*.openapi.yaml|yml|json`
  - `*.mcp-tools.yaml|yml|json`
- 仓内不再保留独立 docs 校验主路径

### `TASK-007`

- 根首页正文改为说明适用范围与维护规则，不再引导一套手工目录树。
- 初始化和纳管默认只补根 `docs/index.md` 与顶层模块 `index.md`。
- 深层目录首页不再由山海工枢脚本自动刷新，后续按 `document-templates` skill 手工维护。

### `TASK-008`

- 补齐正式刷新方案，覆盖：
  - 新项目
  - 已纳入山海工枢但文档未升级的项目
  - 非山海工枢历史项目

### `TASK-009`

- 删除仓内“递归生成目录首页 + 合并根导航”作为正式流程。
- 根导航改为人工在 `document-templates` skill 下维护。
- 合规性检查统一由 `docs-stratego source validate` 负责。

### `TASK-010`

- 正式流程改为：
  - 使用 `document-templates` skill 重构源仓 `docs/`
  - 用 `docs-stratego source validate` 做源仓合规校验
  - 不再保留仓内专用 docs 升级脚本入口

### `TASK-011`

- 正式命令入口改为 `docs-stratego` CLI：
  - 源仓校验：`docs-stratego source validate`
  - 聚合接入：`docs-stratego source add/remove/scaffold-notify`
  - 站点同步/构建/预览：`docs-stratego sync/build/dev`

## 4. 面向使用山海工枢项目的刷新方案

### 4.1 已经是山海工枢项目

1. 使用 `document-templates` skill 重构 `docs/`
2. 手工复核根 `docs/index.md`：
   - 是否存在需要例外公开的契约页面
   - 页面标题是否符合对外展示要求
3. 对根导航中声明的目录补齐 `index.md`
4. 执行 `uvx --from docs-stratego docs-stratego source validate --repo-path "."`

### 4.2 历史项目，`docs/` 还是旧结构

1. 直接使用 `document-templates` skill 把旧目录迁到 4 大模块结构
2. skill 完成根索引与顶层模块首页修正
3. 如果项目存在 OpenAPI / MCP tools 契约，按标准补到真实文档目录下，并确保根导航声明的目录都具备 `index.md`
4. 手工复核根导航中的页面级 `access`
5. 执行 `uvx --from docs-stratego docs-stratego source validate --repo-path "."`

### 4.3 非山海工枢历史项目，尚未纳管

1. 先执行历史项目纳管，不要直接刷新 docs：
   - `python3 <shanforge-root>/scripts/factory-dispatch historical-project-onboarding --project "." --owner "<owner>" --goal "<goal>"`
2. 纳管完成后，使用 `document-templates` skill 重构 `docs/`
4. 对存在公开 API 或 Agent tools 的项目，补齐根导航声明、目录首页与页面级权限例外
5. 以 `docs-stratego source validate` 作为收口

## 5. 验收标准

- `docs/index.md` 能覆盖当前正式公开入口和需要暴露给读者的关键页面。
- `docs-stratego source validate` 能识别无效契约和 `assets/` 误放文件。
- 文档维护流程中不再依赖仓内 docs 刷新脚本。
- 子目录首页不再由山海工枢脚本递归生成。

## 6. 风险与后续

- 根导航现在完全由人工维护；如果目录调整后忘记同步，会被 `docs-stratego source validate` 阻断。
- 对私有设计目录中嵌套公开契约的项目，仍需要人工复核根导航中的页面级权限。
- 后续可在 `docs-stratego` CLI 侧继续补专门的源仓 scaffold 能力，但山海工枢不再保留平行实现。

## 7. 变更记录

| 日期 | 变更内容 | 变更人 |
|---|---|---|
| 2026-04-01 | 初始版本，登记《源文档标准》升级实施计划与任务清单 | Codex |
| 2026-04-01 | 完成 `TASK-009` 导航合并与 `TASK-010` 一键升级入口 | Codex |
| 2026-04-01 | 增加 `TASK-011`，提供多项目批量升级入口 | Codex |
| 2026-04-03 | 将实施路径更新为 `document-templates` skill + `docs-stratego` CLI，删除仓内旧 docs 升级命令定位 | Codex |
