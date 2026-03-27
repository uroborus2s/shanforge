---
name: find-skills
description: 当用户提出诸如“我该如何做某事”、“为某事找一个 skill”、“有没有可以做某事的 skill...”等问题，或表现出扩展能力的兴趣时，帮助用户发现并安装 agent skills。当用户寻找可能存在的可安装功能时，应使用此 skill。
---

# 查找 Skills (Find Skills)

此 skill 帮助你从开放的 agent skills 生态系统中发现并安装 skills。

## 何时使用此 Skill

当用户满足以下情况时使用此 skill：

- 询问“我该如何做 X”，而 X 可能是已有 skill 覆盖的常见任务。
- 说“为 X 找一个 skill”或“有没有关于 X 的 skill”。
- 询问“你能做 X 吗”，而 X 是一项专业能力。
- 表现出扩展 agent 能力的兴趣。
- 想要搜索工具、模板或工作流。
- 提到他们希望在特定领域（设计、测试、部署等）获得帮助。

## 什么是 Skills CLI？

Skills CLI (`npx skills`) 是开放 agent skills 生态系统的包管理器。Skills 是模块化的软件包，通过专业知识、工作流和工具来扩展 agent 的能力。

**核心命令：**

- `npx skills find [query]` - 通过交互方式或关键字搜索 skills。
- `npx skills add <package>` - 从 GitHub 或其他来源安装 skill。
- `npx skills check` - 检查 skill 更新。
- `npx skills update` - 更新所有已安装的 skills。

**浏览 skills 地址：** https://skills.sh/

## 如何帮助用户查找 Skills

### 第一步：理解用户需求

当用户寻求帮助时，确定以下内容：

1. **领域**（例如：React、测试、设计、部署）。
2. **具体任务**（例如：编写测试、创建动画、评审 PR）。
3. **普遍性**：这是否是一个足够通用的任务，以至于很可能已经存在相关的 skill。

### 第二步：优先检查排行榜 (Leaderboard)

在运行 CLI 搜索之前，先查看 [skills.sh 排行榜](https://skills.sh/)，了解该领域是否已有知名的 skill。排行榜按总安装量对 skills 进行排名，展示最受欢迎且经过验证的选择。

例如，Web 开发领域的顶级 skills 包括：
- `vercel-labs/agent-skills` — React, Next.js, 网页设计 (每个均有 10W+ 安装量)
- `anthropics/skills` — 前端设计, 文档处理 (10W+ 安装量)

### 第三步：搜索 Skills

如果排行榜没有覆盖用户的需求，请运行查找命令：

```bash
npx skills find [查询词]
```

例如：

- 用户问“如何让我的 React 应用更快？” → `npx skills find react performance`
- 用户问“你能帮我做 PR 评审吗？” → `npx skills find pr review`
- 用户问“我需要创建一个变更日志 (changelog)” → `npx skills find changelog`

### 第四步：推荐前验证质量

**不要仅根据搜索结果推荐 skill。** 务必验证：

1. **安装量** — 优先选择安装量在 1K+ 以上的 skills。对于低于 100 的要保持谨慎。
2. **来源信誉** — 官方来源（如 `vercel-labs`, `anthropics`, `microsoft`）比未知作者更值得信任。
3. **GitHub Stars** — 检查源仓库。如果仓库 Stars 少于 100，应持怀疑态度。

### 第五步：向用户展示选项

找到相关的 skills 后，向用户展示：

1. Skill 名称及其功能。
2. 安装量和来源。
3. 用户可以运行的安装命令。
4. 在 skills.sh 了解更多详情的链接。

示例回答：

```
我找到了一个可能对你有帮助的 skill！"react-best-practices" 提供了来自 Vercel Engineering 的 React 和 Next.js 性能优化指南。
(18.5W 安装量)

安装命令：
npx skills add vercel-labs/agent-skills@react-best-practices

了解更多：https://skills.sh/vercel-labs/agent-skills/react-best-practices
```

### 第六步：提议安装

如果用户想继续，你可以为他们安装该 skill：

```bash
npx skills add <owner/repo@skill> -g -y
```

`-g` 标志表示全局安装（用户级），`-y` 标志跳过确认提示。

## 常见的 Skill 类别

搜索时，可以考虑以下常见类别：

| 类别 | 示例查询词 |
| --------------- | ---------------------------------------- |
| Web 开发 | react, nextjs, typescript, css, tailwind |
| 测试 | testing, jest, playwright, e2e           |
| DevOps          | deploy, docker, kubernetes, ci-cd        |
| 文档 | docs, readme, changelog, api-docs        |
| 代码质量 | review, lint, refactor, best-practices   |
| 设计 | ui, ux, design-system, accessibility     |
| 生产力 | workflow, automation, git                |

## 有效搜索的技巧

1. **使用特定关键字**：“react testing” 比单纯的 “testing” 更好。
2. **尝试备选术语**：如果 “deploy” 不起作用，尝试 “deployment” 或 “ci-cd”。
3. **检查热门来源**：许多 skills 来自 `vercel-labs/agent-skills` 或 `ComposioHQ/awesome-claude-skills`。

## 未找到 Skill 时

如果没有相关的 skill 存在：

1. 告知用户未找到现有的 skill。
2. 提议使用你的通用能力直接帮助完成任务。
3. 建议用户可以使用 `npx skills init` 创建自己的 skill。

示例：

```
我搜索了关于 "xyz" 的 skills，但没有找到匹配项。
我仍然可以直接帮你完成这项任务！需要我继续吗？

如果你经常需要做这件事，你也可以创建自己的 skill：
npx skills init my-xyz-skill
```
