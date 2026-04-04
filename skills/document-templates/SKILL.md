---
name: document-templates
description: "Software project lifecycle document system for D3. Use when Codex needs to create, review, organize, or evolve human-readable project documentation for software work, including project charter, requirements, architecture, module boundaries, API and interface contracts, delivery plans, testing documents, release and deployment guides, operations runbooks, handover materials, user guides, admin guides, and traceability artifacts."
---

# 文档模板技能：面向 `docs-stratego` 的 4 大模块文档系统

## 目标

为软件项目提供一套面向人类阅读、可追踪、可升级的正式文档体系。当前默认结构不是把生命周期目录直接铺在 `docs/` 根下，而是采用 4 大模块单轴结构：

1. `01-getting-started`
2. `02-user-guide`
3. `03-developer-guide`
4. `04-project-development`

其中只有 `04-project-development/` 继续承载治理、需求、设计、测试、发布、运维和追踪矩阵等内部过程文档。

## 先做判断

在写文档前，先做四个判断：

1. 判断项目状态：空目录新项目 | 已纳入软件工厂项目 | 历史未纳管项目 | 已纳管但 `docs/` 仍是旧布局
2. 判断当前动作：初始化 | 标准升级/重构 | 增量补文档 | 校验收口
3. 判断文档模块：入门说明 | 用户指南 | 开发者指南 | 内部项目开发文档
4. 判断暴露面：最终用户使用 | 二次开发/API/SDK/插件扩展 | 自托管/运维 | 仅内部维护

## 默认工作流

1. 先判断项目是不是已经有正式 `docs/` 和 `.factory/`。
2. 对已有项目，不再调用 `factory-docs-*` 旧脚本；改为直接用 `document-templates` skill 维护文档，并用 `docs-stratego` CLI 收口校验：
   - PyPI 已发布 CLI：`uvx --from docs-stratego docs-stratego source validate --repo-path .`
   - 如项目尚未纳入软件工厂治理，可先执行 `factory-dispatch historical-project-onboarding --project "." --owner "<owner>" --goal "<goal>"`，但这一步不再承担 docs 重构职责
3. 按项目暴露面决定 4 大模块是否都需要：
   - `01-getting-started`：大多数项目默认需要
   - `02-user-guide`：只要有人实际使用或维护，默认需要
   - `03-developer-guide`：只有存在 API、SDK、插件、二次开发、自托管交付或稳定集成面时才默认需要
   - `04-project-development`：正式维护项目默认需要
4. 根 `docs/index.md` 作为唯一导航与权限事实源；所有页面顺序、标题和 `public/private` 都写在这里。
5. 子目录 `index.md` 只写正文概览、使用边界和推荐阅读顺序，不再重复声明导航。
6. 只创建“下一阶段真的会被使用”的文档，不批量制造空壳页。
7. 修改后统一收口：
   - 在源仓执行 `docs-stratego source validate`，确认 `docs/` 合规
   - 若项目需要接入 `docs-stratego` 聚合站点，在聚合仓执行 `docs-stratego source add/remove/sync/build`
   - 若项目需要源仓自动通知聚合仓，再执行 `docs-stratego source scaffold-notify`

## 先读哪些参考

按需读取，不要一次性加载全部：

- 需要完整目录结构、根索引职责和模块边界时，读 [references/repository-structure.md](references/repository-structure.md)
- 需要判断不同项目应该补哪些文档时，读 [references/document-catalog.md](references/document-catalog.md)
- 需要看稳定 ID、阶段关口、旧目录映射和重构命令流程时，读 [references/traceability-and-gates.md](references/traceability-and-gates.md)

## 文档组织原则

### 1. 顶层按 4 大模块组织，不再按生命周期平铺

默认结构：

```text
docs/
  index.md
  01-getting-started/
  02-user-guide/
  03-developer-guide/      # 按需启用
  04-project-development/
    01-governance/
    02-discovery/
    03-requirements/
    04-design/
    05-development-process/
    06-testing-verification/
    07-release-delivery/
    08-operations-maintenance/
    09-evolution/
    10-traceability/
.factory/
  memory/
  process/
  workitems/
```

### 2. 根 `docs/index.md` 是唯一导航与权限事实源

- 只有根 `docs/index.md` 使用 YAML front matter
- 只有根 `docs/index.md` 维护 `mkdocs.home_access` 与 `mkdocs.nav`
- 页面节点只允许 `title`、`path`、`access`
- 目录节点只允许 `title`、`children`
- 页面权限只写在页面节点里，不写在目录节点里

### 3. 子目录 `index.md` 只做正文首页

子目录 `index.md` 负责：

- 说明该目录解决什么问题
- 说明读者是谁
- 给目录内页面或契约补上下文

子目录 `index.md` 不再负责：

- 声明 `mkdocs.nav`
- 决定页面顺序
- 决定页面权限

### 4. 公开稳定说明与内部过程文档分层维护

- `01-getting-started`：第一次接触项目的人读什么
- `02-user-guide`：实际使用、配置、操作和支持怎么做
- `03-developer-guide`：稳定的开发、扩展、集成入口怎么做
- `04-project-development`：内部项目事实、阶段文档和 Gate 资产

不要把“给用户的说明”和“内部设计/测试/发布过程”混写在同一个目录。

### 5. 契约文件要和解释文档配套

- 对外公开 API / SDK / MCP tools 契约：优先放在 `03-developer-guide/` 相关目录，并在根导航中声明访问级别
- 内部设计期契约：放在 `04-project-development/04-design/contracts/`
- 契约文件允许使用 `*.openapi.*`、`*.mcp-tools.*`
- `assets/` 只能放资源文件，不能放 Markdown 页面或契约文件

### 6. 仓内链接统一使用相对路径

- 不写机器绝对路径
- 不在 `path` 中写 `../`
- 让 `docs-stratego` 和仓内阅读都能复用同一套链接

## 默认最小文档包

大多数正式维护的软件项目，至少维护：

- `docs/index.md`
- `docs/01-getting-started/index.md`
- `docs/01-getting-started/project-overview.md`
- `docs/01-getting-started/quick-start.md`
- `docs/01-getting-started/document-map.md`
- `docs/02-user-guide/index.md`
- `docs/02-user-guide/user-guide.md`
- `docs/04-project-development/index.md`
- `docs/04-project-development/01-governance/index.md`
- `docs/04-project-development/02-discovery/index.md`
- `docs/04-project-development/03-requirements/index.md`
- `docs/04-project-development/04-design/index.md`
- `docs/04-project-development/05-development-process/index.md`
- `docs/04-project-development/06-testing-verification/index.md`
- `docs/04-project-development/07-release-delivery/index.md`
- `docs/04-project-development/08-operations-maintenance/index.md`
- `docs/04-project-development/09-evolution/index.md`
- `docs/04-project-development/10-traceability/index.md`
- `docs/04-project-development/01-governance/project-charter.md`
- `docs/04-project-development/02-discovery/input.md`
- `docs/04-project-development/02-discovery/brainstorm-record.md`
- `docs/04-project-development/03-requirements/prd.md`
- `docs/04-project-development/03-requirements/requirements-analysis.md`
- `docs/04-project-development/03-requirements/requirements-verification.md`
- `docs/04-project-development/04-design/technical-selection.md`
- `docs/04-project-development/04-design/system-architecture.md`
- `docs/04-project-development/04-design/module-boundaries.md`
- `docs/04-project-development/04-design/api-design.md`
- `docs/04-project-development/05-development-process/implementation-plan.md`
- `docs/04-project-development/06-testing-verification/test-plan.md`
- `docs/04-project-development/07-release-delivery/release-notes.md`
- `docs/04-project-development/08-operations-maintenance/deployment-guide.md`
- `docs/04-project-development/08-operations-maintenance/operations-runbook.md`
- `docs/04-project-development/10-traceability/requirements-matrix.md`

以下情况再补 `03-developer-guide/`：

- 需要让外部团队二次开发
- 有公开 API / OpenAPI / MCP tools / SDK
- 有插件机制、模块扩展点或稳定函数接口
- 需要把开发手册和用户手册明确分层

## 模板资产与输出路径

优先复用这些模板。注意：内部模板资产仍按阶段分组命名，但输出路径已经切到新结构。

- 根索引：`assets/templates/00-root/docs-index.md` -> `docs/index.md`
- 入门目录首页：`assets/templates/01-getting-started/index.md` -> `docs/01-getting-started/index.md`
- 项目概览：`assets/templates/01-getting-started/project-overview.md` -> `docs/01-getting-started/project-overview.md`
- 快速开始：`assets/templates/01-getting-started/quick-start.md` -> `docs/01-getting-started/quick-start.md`
- 文档地图：`assets/templates/01-getting-started/document-map.md` -> `docs/01-getting-started/document-map.md`
- 用户指南目录首页：`assets/templates/02-user-guide/index.md` -> `docs/02-user-guide/index.md`
- 开发者指南目录首页：`assets/templates/03-developer-guide/index.md` -> `docs/03-developer-guide/index.md`
- 内部项目开发文档首页：`assets/templates/04-project-development/index.md` -> `docs/04-project-development/index.md`
- 项目章程：`assets/templates/00-governance/project-charter.md` -> `docs/04-project-development/01-governance/project-charter.md`
- 调研输入：`assets/templates/01-discovery/input.md` -> `docs/04-project-development/02-discovery/input.md`
- 头脑风暴记录：`assets/templates/01-discovery/brainstorm-record.md` -> `docs/04-project-development/02-discovery/brainstorm-record.md`
- PRD：`assets/templates/02-requirements/prd.md` -> `docs/04-project-development/03-requirements/prd.md`
- 需求分析：`assets/templates/02-requirements/requirements-analysis.md` -> `docs/04-project-development/03-requirements/requirements-analysis.md`
- 需求校验：`assets/templates/02-requirements/requirements-verification.md` -> `docs/04-project-development/03-requirements/requirements-verification.md`
- 技术选型：`assets/templates/03-solution/technical-selection.md` -> `docs/04-project-development/04-design/technical-selection.md`
- 系统架构：`assets/templates/03-solution/system-architecture.md` -> `docs/04-project-development/04-design/system-architecture.md`
- 模块边界：`assets/templates/03-solution/module-boundaries.md` -> `docs/04-project-development/04-design/module-boundaries.md`
- API 设计：`assets/templates/03-solution/api-design.md` -> `docs/04-project-development/04-design/api-design.md`
- 后端设计：`assets/templates/03-solution/backend-design.md` -> `docs/04-project-development/04-design/backend-design.md`
- 数据设计：`assets/templates/03-solution/database-design.md` -> `docs/04-project-development/04-design/database-design.md`
- 接口契约说明：`assets/templates/03-solution/interface-contract.md` -> `docs/04-project-development/04-design/contracts/internal/interface-catalog.md`
- UX/UI 设计：`assets/templates/03-solution/ux-ui-design.md` -> `docs/04-project-development/04-design/ux-ui-design.md`
- 实施计划：`assets/templates/04-delivery/implementation-plan.md` -> `docs/04-project-development/05-development-process/implementation-plan.md`
- 执行日志：`assets/templates/04-delivery/execution-log.md` -> `docs/04-project-development/05-development-process/execution-log.md`
- 测试计划：`assets/templates/05-quality/test-plan.md` -> `docs/04-project-development/06-testing-verification/test-plan.md`
- 发布说明：`assets/templates/06-release/release-notes.md` -> `docs/04-project-development/07-release-delivery/release-notes.md`
- 交付包：`assets/templates/06-release/delivery-package.md` -> `docs/04-project-development/07-release-delivery/delivery-package.md`
- 发布检查清单：`assets/templates/06-release/release-checklist.md` -> `docs/04-project-development/07-release-delivery/release-checklist.md`
- 部署说明：`assets/templates/07-operations/deployment-guide.md` -> `docs/04-project-development/08-operations-maintenance/deployment-guide.md`
- 运维手册：`assets/templates/07-operations/operations-runbook.md` -> `docs/04-project-development/08-operations-maintenance/operations-runbook.md`
- 用户指南：`assets/templates/08-handover/user-guide.md` -> `docs/02-user-guide/user-guide.md`
- 管理员指南：`assets/templates/08-handover/admin-guide.md` -> `docs/02-user-guide/admin-guide.md`
- 需求追踪矩阵：`assets/templates/traceability/requirements-matrix.md` -> `docs/04-project-development/10-traceability/requirements-matrix.md`

## 重构 / 迁移流程

### 空目录新项目

- 用 `factory-init`
- 不要手工拼一套伪 `docs/` 骨架
- 初始化后再按当前项目事实裁剪 4 大模块

### 历史未纳管项目

1. 如需先纳入软件工厂治理，可执行 `factory-dispatch historical-project-onboarding --project "." --owner "<owner>" --goal "<goal>"`
2. 用 `document-templates` skill 按 4 大模块手工重构 `docs/`
3. 执行 `uvx --from docs-stratego docs-stratego source validate --repo-path .`
4. 最后人工复核根导航里的 `public/private` 页面级权限

### 已纳管但仍是旧生命周期顶层目录

1. 用 `document-templates` skill 把旧生命周期顶层目录手工迁到 4 大模块结构
2. 修复根 `docs/index.md` 和各目录 `index.md`，确保只有根索引维护导航与权限
3. 执行 `uvx --from docs-stratego docs-stratego source validate --repo-path .`
4. 如需聚合预览或发布，在 `docs-stratego` 根仓执行 `docs-stratego dev/sync/build`

### 只有需求文档结构过旧

- 用 `factory-requirements-upgrade`
- 这不是完整文档体系重构，也不能替代历史项目纳管

### 与 `docs-stratego` 站点集成

- 源仓按新结构维护 `docs/`
- 根 `docs/index.md` 统一维护导航和权限
- 最后用 `docs-stratego source validate` 验证合规性

## 输出要求

当用户请求“列出需要哪些文档”时：

1. 先按 4 大模块列出，而不是直接把旧生命周期顶层目录抄出来
2. 再在 `04-project-development/` 内按阶段列出内部文档
3. 明确哪些是公开稳定说明，哪些是内部过程文档
4. 明确是否需要 `03-developer-guide/`

当用户请求“创建文档体系”时：

1. 先判断是新项目、历史项目纳管还是旧结构升级
2. 先创建或修复根 `docs/index.md` 和 4 大模块首页
3. 再按当前项目事实补真正需要的正文页
4. 最后执行 `docs-stratego source validate` 做结构校验

当用户请求“重构现有文档”时：

1. 先识别旧目录、旧索引还是未纳管状态
2. 直接用 `document-templates` skill 做目录和正文重构，不再调用 `factory-docs-*`
3. 重构后执行 `docs-stratego source validate`
4. 同步更新受影响的正式文档、追踪矩阵和必要的 `.factory/memory/`
