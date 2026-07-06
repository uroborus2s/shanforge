# 应用开发

## 1. 开发入口

应用开发以仓库内的 `skills/`、`docs/` 和 `.factory/memory/` 为主要协作面。

AI 运行时会维护自己的内部控制面，但那不是开发者默认阅读入口；开发者默认看正式文档、代码和命令入口。

开发前建议先读：

1. [总体方案与协作总览](../04-project-development/04-design/solution-overview.md)
2. [技术选型与工程规则](../04-project-development/04-design/technical-selection.md)
3. [系统架构设计](../04-project-development/04-design/system-architecture.md)
4. [模块边界文档](../04-project-development/04-design/module-boundaries.md)

## 2. 开发原则

- 需求未确认，不直接写实现。
- 设计未落文档，不直接扩边界。
- 代码变更要同步测试、文档和必要的运行摘要。
- 公开函数和接口变更，要同步更新开发者文档。

## 3. 推荐工作流

1. 确认需求与设计基线。
2. 拆任务。
3. 编码与测试。
4. 更新文档。
5. 进入 PR 闭环。
