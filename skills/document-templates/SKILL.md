---
name: document-templates
description: "创建、审查、整理和升级软件项目正式文档体系。适用于项目章程、需求、架构、模块边界、API/接口契约、交付计划、测试、发布、运维、交接、用户指南、管理员指南和追踪矩阵；默认按 docs-stratego 的 4 大模块组织。"
---

# 文档模板

用于维护软件项目的正式文档体系。主路径是先判断项目状态和读者，再按 `docs-stratego` 的 4 大模块补最少必要文档，最后用结构校验收口。

## 适用边界

适用于：

- 创建、审查、整理和升级软件项目正式文档体系。
- 维护 `docs/`、根 `docs/index.md`、正式文档版本历史和追踪矩阵。
- 把已批准需求、设计或交付事实整理成正式项目文档。
- 按 `docs-stratego` 的 4 大模块校验目录和导航。

不适用于：

- 单篇文章、博客、新闻稿或营销内容。
- 需求尚未澄清时直接生成完整文档包。
- 临时草稿、review 输入包、evidence 或 PM 展示页。
- 代码实现、测试修复、review gate、人工确认或本地提交。
- 没有项目事实来源时批量制造空文档。

流程 gate 只做文档侧检查。阶段路由、独立 review、人工确认和提交闭环由 Shanforge 流程总控处理。

## 先做判断

1. 项目状态：空目录新项目 | 已纳入软件工厂项目 | 历史未纳管项目 | 已纳管但 `docs/` 仍是旧布局。
2. 当前动作：初始化 | 标准升级/重构 | 增量补文档 | 校验收口。
3. 文档模块：入门说明 | 用户指南 | 开发者指南 | 内部项目开发文档。
4. 暴露面：最终用户 | 二次开发/API/SDK/插件 | 自托管/运维 | 仅内部维护。

最小路径：

- 只补单页：读取事实源，更新目标页、版本历史和索引。
- 只校验：运行 `docs-stratego source validate` 或记录无法运行原因。
- 完整重构：先读结构和迁移 references，再按 4 大模块迁移。

## 默认工作流

1. 判断是否已有正式 `docs/` 和 `.factory/`。
2. 已有项目不调用旧仓库脚本；直接维护文档，并用 `docs-stratego` CLI 校验。
3. 如项目尚未纳入软件工厂治理，先交给 `using-shanforge` 判断是否需要项目纳管。
4. 按暴露面决定是否启用 `03-developer-guide/`；不要机械生成。
5. 根 `docs/index.md` 作为唯一导航与权限事实源。
6. 子目录 `index.md` 只写正文概览、边界和推荐阅读顺序。
7. 只创建下一阶段真的会被使用的文档，不批量制造空壳页。
8. 需求分析内容必备，独立文件条件生成：读取 `analysis_mode` 和
   `analysis_locator`；只有 `standalone` 才创建 `requirements-analysis.md`。
9. 修改后运行 `uvx --from docs-stratego docs-stratego source validate --repo-path .`；无法运行时写清替代核查和风险。

## 正式文档治理规则

- 正式文档只放在 `docs/` 的登记路径下。
- 新增正式文档必须在同一改动中同步 `docs/index.md` 或 `.factory/memory/doc-map.md`。
- 修改正式文档必须追加 `版本历史`。
- 每份正式文档必须包含中文 `版本信息` 和 `版本历史`。
- 临时文档只能放在 `.factory/workitems/<WORKITEM-ID>/drafts/`、`evidence/`、`reports/` 或 `reviews/`。
- 只读 HTML 由项目快照 CLI 写入 `.factory/cache/site/current/`；它是可重建展示层，不是文档保存位置，也不作为事实源。
- 临时推理、草稿、review 输入包和验证输出不要写进 `docs/`。

## 按需读取

不要一次性加载全部 references。

- 完整目录、根索引职责和模块边界：读 [repository structure](references/repository-structure.md)。
- 判断不同项目应该补哪些文档：读 [document catalog](references/document-catalog.md)。
- 稳定 ID、阶段关口、旧目录映射和迁移流程：读 [traceability and gates](references/traceability-and-gates.md)。
- 创建正式文档：读 [formal document template](references/formal-document-template.md)。
- 已批准需求转轻量技术设计：读 [technical design template](references/technical-design-template.md)。
- 需要定义测试启动、端口、健康检查、关闭和追踪关系：读 [test environment template](references/test-environment-template.md)。
- 需要测试或发布材料时，复用 `assets/templates/05-quality/test-plan.md`、`test-report.md`、
  `06-release/release-checklist.md` 和 `07-operations/deployment-guide.md`；案例目录、运行结果和聚合报告分开保存。

## 组织规则

- 顶层按 4 大模块组织：`01-getting-started`、`02-user-guide`、`03-developer-guide`、`04-project-development`。
- `04-project-development/` 承载治理、需求、设计、测试、发布、运维和追踪矩阵等内部过程文档。
- 公开稳定说明和内部过程文档分层维护。
- 对外 API / SDK / MCP tools 契约优先放在 `03-developer-guide/`。
- 内部设计期契约放在 `04-project-development/04-design/contracts/`。
- `assets/` 只能放资源文件，不能放 Markdown 页面或契约文件。
- 仓内链接统一使用相对路径，不写机器绝对路径。

## 输出要求

当用户请求“列出需要哪些文档”时：

- 先按 4 大模块列出。
- 再在 `04-project-development/` 内按阶段列出内部文档。
- 明确公开稳定说明、内部过程文档和是否需要 `03-developer-guide/`。

当用户请求“创建文档体系”时：

- 先判断项目状态。
- 先创建或修复根 `docs/index.md` 和必要模块首页。
- 再按当前项目事实补真正需要的正文页。
- 最后执行结构校验。

当用户请求“重构现有文档”时：

- 先识别旧目录、旧索引还是未纳管状态。
- 按 references 做目录和正文重构，不调用旧仓库脚本。
- 重构后执行结构校验。
- 同步受影响的正式文档、追踪矩阵和必要 `.factory/memory/`。

## 状态回写与失败语义

非 Shanforge work item 的简短答复至少包含：

- 本次文档动作。
- 影响路径。
- 已用模板或参考文件。
- 结构校验命令和结果。
- 未决事实、未生成文档和原因。

若在 Shanforge work item 中使用，只返回状态包；流程路由、review、人工确认和提交仍由流程总控判断：

```text
工作结果：
- work_item: <WORKITEM-ID>
- skill: document-templates
- status: ready_for_review | blocked | needs_user_input
- outputs:
  - <path>
- evidence:
  - <docs-stratego validate 输出或核查说明>
- ledger_event: <event id or none>
- needs:
  - review | verification | user_input | none
```

`blocked` 只用于项目状态、目标读者、文档事实源或校验工具缺失，导致无法安全创建或迁移正式文档的情况。能安全补单页时，不因完整文档包未完成而阻塞。

`needs_user_input` 用于必须由用户决定的文档范围、公开级别、目标读者、是否纳管或冲突事实取舍。缺少这些决定时，不批量生成正式文档。

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。
