# 应用开发

## 1. 开发入口

应用开发以仓库内的 `scripts/`、`skills/`、`docs/` 和 `.factory/` 为基础协作面。

开发前建议先读：

1. [总体方案与协作总览](../04-project-development/04-design/solution-overview.md)
2. [技术选型与工程规则](../04-project-development/04-design/technical-selection.md)
3. [系统架构设计](../04-project-development/04-design/system-architecture.md)
4. [模块边界文档](../04-project-development/04-design/module-boundaries.md)

## 2. 开发原则

- 需求未确认，不直接写实现。
- 设计未落文档，不直接扩边界。
- 代码变更要同步测试、文档和 AI 记忆。
- 公开函数和接口变更，要同步更新开发者文档。

## 3. 推荐工作流

1. 确认需求与设计基线。
2. 拆任务。
3. 编码与测试。
4. 更新文档。
5. 进入 PR 闭环。
