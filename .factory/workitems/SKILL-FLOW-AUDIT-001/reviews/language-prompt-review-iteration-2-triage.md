# Language Prompt Review Iteration 2 Triage

## Feedback Source

- Source: `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/language-prompt-review-iteration-2.md`
- Request: fix issues first, then run a new language/prompt review and a new flow completeness test.

## Scope

修复当前 34 个 skill 中低于 90 分的主要问题。高分 skill 只在必要时避免被测试误伤，不主动改。

## Fixed Batches

| Batch | Files | Feedback | Decision |
|---|---|---|---|
| P0 low-score entrances | `ui-ux-pro-max`, `shadcn`, `doc-coauthoring`, `algorithmic-art` | 入口过长、英文/旧口径、触发过宽、输出契约缺失 | Fix |
| Dev workflow tutorials | `frontend-patterns`, `tdd-workflow`, `ai-regression-testing`, `api-design` | 长教程、框架绑定、状态包缺失 | Fix |
| File/text tools | `docx`, `pdf`, `xlsx`, `humanizer`, `webapp-testing` | 工具速查过长、任务分支不清、验证/失败语义弱 | Fix |
| Flow/minor contracts | `agent-harness-construction`, `ai-first-engineering`, `article-writing`, `document-templates`, `gitcommitzh`, `skill-creator`, `stratix-service`, `subagent-driven-development` | 输出契约、边界、重复门禁和状态语义 | Fix |

## Non-Goals

- 不改已删除 skill。
- 不改 `.factory/project.json` 或 skill 注册配置。
- 不新增中心脚本或旧 `factory-*` gate。
- 不实现 flow completeness report 的 Critical / Important，本轮只处理 language/prompt review。
- 不把修复写成 approved；修复后仍需新一轮子任务评审和测试。
