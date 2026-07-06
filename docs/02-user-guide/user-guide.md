# 使用指南

这篇文档说明如何用当前的 `shanforge`。

## 1. 一句话理解

`shanforge` 不是 GUI，也不是命令大全。它是一套让 `Codex` / `Gemini CLI` 按软件工厂规则推进项目的 skills、文档和记忆体系。

你通常只做三件事：

1. 用自然语言说明项目路径、当前状态、目标和禁止事项。
2. 让 `using-shanforge` 判断当前流程位置。
3. 让对应 skill 完成需求、设计、计划、实现、评审、验证或提交。

## 2. 使用前准备

进入仓库根目录后，确认这些目录存在：

- `skills/`
- `docs/`
- `.factory/memory/`

如果需要把仓内 skills 同步到本地宿主，可以执行：

```bash
uv run python scripts/sync-codex-skills
```

这只是同步工具，不是项目流程入口。

## 3. 第一轮会话怎么说

推荐直接给 AI 这些信息：

```text
项目路径：[项目路径]
当前状态：[空目录 / 已有代码 / 已纳管项目 / 不确定]
本轮目标：[一句话目标]
禁止事项：[不要散读 docs / 不要直接编码 / 不要提交等]
完成后输出：[需要的结果]
```

AI 应该先走 `using-shanforge`，必要时用 `project-memory` 恢复上下文，再选择唯一下一步 skill。

## 4. 常见场景

| 场景 | 正确入口 |
|---|---|
| 不知道下一步 | 让 `using-shanforge` 判断当前阶段和阻塞项 |
| 需要恢复上下文 | 使用 `project-memory` |
| 需要澄清想法或范围 | 使用 `brainstorming` |
| 需要需求或验收标准 | 使用 `requirements-engineering` |
| 需要文档体系或技术文档 | 使用 `document-templates` |
| 已有需求，需要计划 | 使用 `writing-plans` |
| 已有计划，需要执行 | 使用 `subagent-driven-development` 或 `executing-plans` |
| 需要评审 | 使用 `requesting-code-review` |
| 需要处理评审意见 | 使用 `receiving-code-review` |
| 准备声明完成 | 使用 `verification-before-completion` |
| 用户明确要求提交 | 使用 `gitcommitzh` |

## 5. 完成标准

一次任务不能只靠“代码改了”算完成。至少要有：

- 代码、文档、测试和 `.factory/memory/` 同步。
- 新鲜验证命令和结果。
- 需要评审时，独立 review 结论。
- 需要人工确认时，等待用户明确通过。

## 6. 不要做什么

- 不要把 skill 当命令目录。
- 不要把旧中心命令当流程主控。
- 不要默认全文读取阶段文档。
- 不要把“准备执行”写成“已经完成”。
- 不要在未确认范围时提交整个工作区。
