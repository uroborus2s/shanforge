# 实施计划

**项目名称：** 山海工枢 / shanforge  
**负责人：** 仓库维护者  
**主要读者：** 项目协调者 | 文档维护者 | 脚本维护者 | QA  
**上游输入：** `source-docs-standard-upgrade-analysis.md` | 最新《源文档标准》  
**下游输出：** 脚本改造 | 回归测试 | 存量项目刷新执行清单  
**最后更新：** 2026-04-01  

## 1. 目标

把山海工枢当前文档工具链升级到可支撑最新《源文档标准》的状态，并给所有使用山海工枢开发的项目提供统一、可重复执行的 `docs/` 刷新路径。

## 2. 任务清单

| 任务 ID | 任务名称 | 主要输出 | 状态 |
|---|---|---|---|
| `TASK-006` | 支持契约页面自动索引与校验 | `factory_core.py` 支持 `*.openapi.*`、`*.mcp-tools.*` 自动发现与最小校验 | 已完成 |
| `TASK-007` | 调整目录首页生成策略 | 目录 `index.md` 不再生成推荐阅读清单，改为范围/边界说明 | 已完成 |
| `TASK-008` | 形成存量项目 docs 刷新方案 | 历史项目与在建项目的统一刷新步骤、命令序列与人工复核点 | 已完成 |
| `TASK-009` | 保留人工维护的导航分组与顺序 | 根 `docs/index.md` 从“重建 front matter”升级为“合并 front matter” | 已完成 |
| `TASK-010` | 提供一键升级入口 | `factory-docs-standard-upgrade` / `factory-dispatch docs-standard-upgrade` | 已完成 |
| `TASK-011` | 提供批量升级入口 | `factory-docs-standard-upgrade-batch` / `factory-dispatch docs-standard-upgrade-batch` | 已完成 |

## 3. 本轮执行结果

### `TASK-006`

- 扩展自动索引支持的页面类型：
  - `*.md`
  - `*.openapi.yaml|yml|json`
  - `*.mcp-tools.yaml|yml|json`
- 在 `docs_stratego_source_status` 中增加：
  - 页面路径合法性检查
  - OpenAPI 最小字段检查
  - MCP tools 最小字段检查
  - `assets/` 契约文件阻断

### `TASK-007`

- 根首页正文改为说明适用范围与维护规则，不再引导一套手工目录树。
- 子目录首页改为说明范围、读者和维护边界，不再自动列出页面清单。
- 契约目录 `openapi/`、`tools/` 生成专门说明文案。

### `TASK-008`

- 补齐正式刷新方案，覆盖：
  - 新项目
  - 已纳入山海工枢但文档未升级的项目
  - 非山海工枢历史项目

### `TASK-009`

- 新增受限 `mkdocs.nav` 解析与合并逻辑。
- 刷新根 `docs/index.md` 时保留：
  - 目录节点标题
  - 已有目录分组顺序
  - 页面节点顺序
- 对新增页面与缺失目录，按生成结果自动补齐，不再整体重建导航。

### `TASK-010`

- 新增统一升级入口：
  - `python3 scripts/factory-docs-standard-upgrade --project <path>`
  - `python3 scripts/factory-dispatch docs-standard-upgrade --project <path>`
- 行为收口为三步：
  - 需要时迁移旧 docs 结构
  - 刷新根索引和目录首页
  - 做最终 `docs-stratego` 就绪校验

### `TASK-011`

- 新增批量升级入口：
  - `python3 scripts/factory-docs-standard-upgrade-batch --root <dir>`
  - `python3 scripts/factory-dispatch docs-standard-upgrade-batch --root <dir>`
- 默认只扫描已纳管的山海工枢项目：
  - 必须存在 `.factory/project.json`
  - 必须存在 `docs/`
- 支持：
  - 多个 `--root`
  - 多个 `--project`
  - `--check`
  - `--max-depth`

## 4. 面向使用山海工枢项目的刷新方案

### 4.1 已经是山海工枢项目

1. 优先执行 `python3 <shanforge-root>/scripts/factory-dispatch docs-standard-upgrade --project "."`
2. 如果项目中新增了契约目录，补齐对应目录首页：
   - `docs/.../openapi/index.md`
   - `docs/.../tools/index.md`
3. 手工复核根 `docs/index.md`：
   - 是否存在需要例外公开的契约页面
   - 页面标题是否符合对外展示要求
4. 执行 `python3 <shanforge-root>/scripts/factory-dispatch docs-standard-upgrade --project "." --check`

### 4.2 历史项目，`docs/` 还是旧结构

1. 直接执行 `python3 <shanforge-root>/scripts/factory-dispatch docs-standard-upgrade --project "."`
2. 命令会按需完成结构迁移与索引刷新
3. 如果项目存在 OpenAPI / MCP tools 契约，按标准补到真实文档目录下，并补齐目录 `index.md`
4. 手工复核根导航中的页面级 `access`
5. 执行 `python3 <shanforge-root>/scripts/factory-dispatch docs-standard-upgrade --project "." --check`

### 4.3 非山海工枢历史项目，尚未纳管

1. 先执行历史项目纳管，不要直接刷新 docs：
   - `python3 <shanforge-root>/scripts/factory-dispatch historical-project-onboarding --project "." --owner "<owner>" --goal "<goal>"`
2. 纳管完成后，执行 `python3 <shanforge-root>/scripts/factory-dispatch docs-standard-upgrade --project "."`
4. 对存在公开 API 或 Agent tools 的项目，补齐契约目录首页与页面级权限例外
5. 以 `docs-standard-upgrade --check` 作为收口

## 5. 验收标准

- `docs/index.md` 能覆盖所有正式 Markdown 页面与契约页面。
- `docs-index-refresh --check` 能识别无效契约和 `assets/` 误放文件。
- 刷新不会覆盖人工维护的根首页正文、`home_access` 和页面级 `access`/`title`。
- 刷新会尽量保留以真实目录为锚点的人工导航分组和顺序。
- 子目录首页不再生成推荐阅读清单。

## 6. 风险与后续

- 当前的导航合并以“真实目录 + 概览页”作为锚点；若手工写出完全脱离目录结构的包装分组，仍需人工复核。
- 对私有设计目录中嵌套公开契约的项目，仍需要人工复核根导航中的页面级权限。
- 后续可继续把统一升级入口接入更高层的项目纳管和修复工作流。

## 7. 变更记录

| 日期 | 变更内容 | 变更人 |
|---|---|---|
| 2026-04-01 | 初始版本，登记《源文档标准》升级实施计划与任务清单 | Codex |
| 2026-04-01 | 完成 `TASK-009` 导航合并与 `TASK-010` 一键升级入口 | Codex |
| 2026-04-01 | 增加 `TASK-011`，提供多项目批量升级入口 | Codex |
