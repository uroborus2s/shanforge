---
name: document-templates
description: "Software project lifecycle document system for D3. Use when Codex needs to create, review, organize, or evolve human-readable project documentation for software work, including project charter, requirements, architecture, module boundaries, API and interface contracts, delivery plans, testing documents, release and deployment guides, operations runbooks, handover materials, user guides, admin guides, and traceability artifacts."
---

# 文档模板技能：软件项目全生命周期文档系统

## 目标

为软件项目提供一套按阶段交付、可追踪、对人类友好的文档体系。不要把“项目文档”局限为开发文档；同时覆盖立项、需求、方案设计、接口与模块边界、测试、发布、部署、运维、交接和最终用户文档。

## 先做判断

在写文档之前，先做三个判断：

1. 判断项目类型：新项目 | 存量迭代 | 内部工具 | 外部产品 | 集成型项目 | 高风险/受监管项目
2. 判断当前阶段：立项 | 需求 | 方案 | 开发计划 | 测试 | 发布 | 运维 | 交接 | 退役
3. 判断当前要交付给谁：管理者 | 产品/需求 | 架构/开发 | 测试/验收 | 发布/运维 | 支持团队 | 最终用户

## 默认工作流

1. 先列出当前阶段必须交付给下一环节的文档，而不是一次性生成整套空文档。
2. 明确区分三类产物：
   - 人类阅读文档：给管理者、实施者、测试者、运维者、用户阅读。
   - 机器可消费合同：如 `openapi.yaml`、`asyncapi.yaml`、`*.proto`、JSON Schema、迁移脚本、IaC。
   - AI 摘要与索引：给代理压缩读取，不替代正式文档。
3. 每份正式文档都写清楚：
   - 目标读者
   - 负责人
   - 上游输入
   - 下游交付对象
   - 关联追踪 ID
4. 优先从 `assets/templates/` 里选择最接近的模板创建或更新文档。
5. 同步维护追踪矩阵、变更记录和状态，不创建 `v1`/`v2` 副本。

## 先读哪些参考

按需读取，不要把所有参考一次性塞进上下文：

- 需要完整的软件工程文档清单时，读 [references/document-catalog.md](references/document-catalog.md)
- 需要初始化或重构项目 `docs/` 目录时，读 [references/repository-structure.md](references/repository-structure.md)
- 需要确定编号规则、阶段关口和最小交付包时，读 [references/traceability-and-gates.md](references/traceability-and-gates.md)

## 文档组织原则

### 1. 按阶段组织，而不是按角色堆放

默认按生命周期编号组织：

```text
docs/
  index.md
  00-governance/
    index.md
  01-discovery/
    index.md
  02-requirements/
    index.md
  03-solution/
    index.md
  04-delivery/
    index.md
  05-quality/
    index.md
  06-release/
    index.md
  07-operations/
    index.md
  08-handover/
    index.md
  09-evolution/
    index.md
  traceability/
    index.md
.factory/
  memory/
  process/
  workitems/
```

阶段编号的目的不是形式化，而是让“下一环节要接什么”一眼可见。

补充约束：

- `docs/index.md` 作为项目总入口页；每个 `docs/` 子目录也必须维护自己的 `index.md`。
- 只有根 `docs/index.md` 使用 YAML front matter，并在 `mkdocs.home_access` / `mkdocs.nav` 中声明全站目录树、页面路径和页面权限。
- 子目录 `index.md` 只是正文首页和资源权限锚点，不再声明 `mkdocs.nav`，也不单独维护页面权限。
- 仓内 Markdown 链接统一使用相对路径，不写机器绝对路径。
- `docs-stratego` 可以通过 Git 子模块挂载源仓，但不会反向改写源文档。

### 2. 同时维护“解释文档”和“契约文件”

对于接口、模块边界、事件、部署等内容，不要只给机器文件：

- API 需要 `api-design.md` + `openapi.yaml`
- 事件接口需要 `event-overview.md` + `asyncapi.yaml` 或 schema 文件
- 内部模块边界需要 `module-boundaries.md` + 必要的 schema / 示例
- 部署需要 `deployment-guide.md` + 回滚方案 + 配置矩阵（风险较高时必备）

### 3. 模块边界文档必须明确约束

模块边界文档至少说明：

- 模块职责与不负责的范围
- 模块拥有的数据与状态
- 暴露的接口与调用方向
- 依赖的外部模块
- 禁止耦合关系
- 错误与降级策略
- 关联需求、测试和运维责任

### 4. 用户文档、管理员文档、运维文档不能混写

至少区分三类读者：

- 最终用户：关注操作步骤、常见任务和问题排查
- 管理员/实施者：关注配置、权限、初始化、变更和维护
- 运维/支持：关注部署、监控、告警、回滚、应急处理

## 默认最小文档包

对于大多数“非一次性脚本”的软件项目，至少维护以下文档：

- `docs/index.md`
- `docs/04-project-development/01-governance/index.md`
- `docs/04-project-development/02-discovery/index.md`
- `docs/04-project-development/03-requirements/index.md`
- `docs/04-project-development/04-design/index.md`
- `docs/04-project-development/05-development-process/index.md`
- `docs/04-project-development/06-testing-verification/index.md`
- `docs/04-project-development/07-release-delivery/index.md`
- `docs/04-project-development/08-operations-maintenance/index.md`
- `docs/02-user-guide/index.md`
- `docs/04-project-development/09-evolution/index.md`
- `docs/04-project-development/10-traceability/index.md`
- `00-governance/project-charter.md`
- `01-discovery/input.md`
- `01-discovery/brainstorm-record.md`
- `02-requirements/prd.md`
- `02-requirements/requirements-analysis.md`
- `02-requirements/requirements-verification.md`
- `03-solution/technical-selection.md`
- `03-solution/system-architecture.md`
- `03-solution/module-boundaries.md`
- `03-solution/api-design.md`
- `04-delivery/implementation-plan.md`
- `04-delivery/execution-log.md`
- `05-quality/test-plan.md`
- `06-release/release-notes.md`
- `07-operations/deployment-guide.md`
- `08-handover/user-guide.md`
- `traceability/requirements-matrix.md`

项目复杂度升高时，再从参考目录中补齐更多文档，而不是一开始就创建几十个空壳文件。

## 什么时候用哪个模板

优先复用这些模板资产：

- 立项与治理：`assets/templates/00-governance/project-charter.md`
- 调研输入：`assets/templates/01-discovery/input.md`
- 调研与头脑风暴：`assets/templates/01-discovery/brainstorm-record.md`
- 需求：`assets/templates/02-requirements/prd.md`
- 需求分析：`assets/templates/02-requirements/requirements-analysis.md`
- 需求校验：`assets/templates/02-requirements/requirements-verification.md`
- 技术画像：`assets/templates/03-solution/technical-selection.md`
- 架构：`assets/templates/03-solution/system-architecture.md`
- 模块边界：`assets/templates/03-solution/module-boundaries.md`
- API 设计：`assets/templates/03-solution/api-design.md`
- 后端设计：`assets/templates/03-solution/backend-design.md`
- 数据设计：`assets/templates/03-solution/database-design.md`
- UX/UI 设计：`assets/templates/03-solution/ux-ui-design.md`
- 交付计划：`assets/templates/04-delivery/implementation-plan.md`
- 执行日志：`assets/templates/04-delivery/execution-log.md`
- 测试方案：`assets/templates/05-quality/test-plan.md`
- 发布说明：`assets/templates/06-release/release-notes.md`
- 交付包：`assets/templates/06-release/delivery-package.md`
- 部署说明：`assets/templates/07-operations/deployment-guide.md`
- 运维手册：`assets/templates/07-operations/operations-runbook.md`
- 用户指南：`assets/templates/08-handover/user-guide.md`
- 管理员指南：`assets/templates/08-handover/admin-guide.md`
- 追踪矩阵：`assets/templates/traceability/requirements-matrix.md`

## 生成和更新规则

### 原地更新

- 所有正式文档都在原文件上持续演进
- 每次修改追加变更记录，不新建 `xxx-v2.md`
- 让 Git 负责历史版本，不让目录结构负责版本膨胀
- 新增、删除或移动页面后，同步刷新根 `docs/index.md` 的目录树，并更新对应子目录 `index.md` 的概览内容

### 只创建“即将被使用”的文档

以下情况再创建对应文档：

- 下一阶段真的需要它
- 当前存在明确风险、依赖或合规要求
- 项目规模已经让口头同步失效

不要为了“看起来完整”创建一堆无人维护的文档。

### 人类优先

- 先写人类能看懂、能交接的说明
- 再补机器契约和 AI 摘要
- 不要让 `.factory/memory/`、OpenAPI 或代码注释替代正式项目文档

## 与 D3 流程的关系

- `/brainstorm` 之后优先写 `01-discovery/brainstorm-record.md`
- `/requirements` 阶段优先产出 `02-requirements/prd.md`、`requirements-analysis.md` 和 `requirements-verification.md`
- 进入设计或实施前，至少补齐 `technical-selection.md`、架构、模块边界、API/接口说明和交付计划
- 发布前，至少补齐测试、发布、部署和运行文档
- 对外或跨团队交付前，至少补齐用户指南、管理员指南和交接说明

## 输出要求

当用户请求“列出需要哪些文档”时：

1. 先按生命周期列出阶段
2. 每个阶段说明“必须有”和“条件性补充”的文档
3. 明确每份文档交给谁、解决什么问题
4. 对接口和边界类文档，补充说明人类说明文档与契约文件如何配套

当用户请求“创建文档体系”时：

1. 先根据项目类型挑选最小文档包
2. 按 `references/repository-structure.md` 初始化目录
3. 先创建 `docs/index.md` 和各目录 `index.md`，根入口写清全站目录树、权限和与 `docs-stratego` 的关系，子目录入口写清该目录说明与推荐阅读顺序
4. 用 `assets/templates/` 创建首批真正需要的文档
5. 生成或刷新目录索引，确保所有页面都被根 `docs/index.md` 的 `mkdocs.nav` 覆盖，子目录 `index.md` 保持为正文概览页
6. 再视项目复杂度补齐其他模板
