# 快速开始

## 1. 先看什么

第一次使用山海工枢，优先阅读：

1. [项目概览](./project-overview.md)
2. [用户指南](../02-user-guide/user-guide.md)
3. [应用开发](../03-developer-guide/application-development.md)
4. [项目章程](../04-project-development/01-governance/project-charter.md)
5. [产品需求文档](../04-project-development/03-requirements/prd.md)

## 2. 最小启动步骤

1. 在仓库根目录阅读 `README.md`、[项目概览](./project-overview.md) 和 [使用指南](../02-user-guide/user-guide.md)。
2. 用自然语言告诉 AI 项目路径、当前状态、第一优先动作和禁止事项；AI 会按项目规则自行读取必要上下文，人类不要手工把内部控制面文件列成阅读清单。
3. 通过自然语言描述目标，优先使用 `factory-dispatch`、`factory-agent-session`、`factory-state-doctor` 等入口推进工作。

## 3. 常用命令

- `scripts/factory-init`
- `scripts/factory-dispatch`
- `scripts/factory-agent-session`
- `scripts/factory-workflow-runner`
- `uv run python scripts/sync-codex-skills`

## 4. 一条最实用的使用原则

先补正式文档，再推进实现；先修事实源，再修摘要和派生入口。
