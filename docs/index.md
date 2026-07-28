---
title: shanforge
---
# 文档总入口

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `DOC-NAV-ROOT-001` |
| 正式版本 | `v1.2.0` |
| 来源候选 | `SKILL-FIRST-PM-001` |
| 发布事务 | `DESIGN-RELEASE-TX-R019-G001` |
| 负责人 | `HUMAN_PROJECT_OWNER` |
| 修改 / 审核 / 批准 | `uroborus` / `uroborus` / `uroborus` |
| 状态 | 已批准并生效 |
| 上游 | `DOCS-IA-SHANFORGE-001`、`.factory/catalog/document-publication-policy.json` |
| 下游 | `六个模块入口`、`document-index` |

## 按目的进入

1. [项目概览](./01-getting-started/index.md)。
2. [用户指南](./02-user-guide/index.md)。
3. [开发者指南](./03-developer-guide/index.md)。
4. [产品与需求](./04-product/index.md)。
5. [软件技术设计](./05-design/index.md)。
6. [质量与交付](./06-delivery/index.md)。
7. [文档索引](./document-index.md)。

## 项目跟踪边界

正式且面向人类的稳定事实进入本目录；TaskCard、计划、状态、评审、验证证据、机器 Catalog、索引和会话恢复摘要进入 `.factory/`。本目录只包含 Markdown 人类文档。

## 快速查看当前项目

触发 `using-shanforge` 后，由 AI 运行该 skill 自带的
`scripts/project_snapshot.py --project-root <项目根目录>`。输入未变化时复用
`.factory/cache/site/current/index.html`；目标项目不需要 Shanforge 源码或独立 CLI。

## 正式版本历史（仅已发布）

| 版本 | 日期 | 变更内容 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v1.2.0` | 2026-07-28 | 项目快照改为 using-shanforge 自带脚本 | `uroborus` | `uroborus` | `uroborus` |
| `v1.0.0` | 2026-07-18 | 建立六类人类文档总入口 | `uroborus` | `uroborus` | `uroborus` |
| `v1.1.0` | 2026-07-22 | 明确 docs 仅含人类文档，并增加固定 CLI 的项目 HTML 与定向查询入口 | `uroborus` | `uroborus` | `uroborus` |
