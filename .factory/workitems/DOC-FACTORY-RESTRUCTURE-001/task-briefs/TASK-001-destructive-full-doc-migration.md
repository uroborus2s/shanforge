# 任务简报

## 工作项

- 工作项：`DOC-FACTORY-RESTRUCTURE-001`
- 任务：`TASK-001-destructive-full-doc-migration`
- 状态：`ready_for_review`
- 上游计划：`.factory/workitems/DOC-FACTORY-RESTRUCTURE-001/plan.md`
- 流水账：`.factory/workitems/DOC-FACTORY-RESTRUCTURE-001/ledger.jsonl`

## 目标

完成 `docs/04-project-development` 和 `.factory` 的破坏性重做型全量文档结构迁移：新增任务执行契约，删除旧资产和旧结构，重写正式导航、索引、doc-map 和当前配置，确保只保留最新正式资产和正式内容。

## 输入

- 用户要求按六类任务结构重构 `04-project-development` 和 `.factory`。
- 用户补充要求：旧资产旧结构都删除，只保留最新正式资产和正式内容。
- 用户署名要求：正式文档不得署名为 `Codex`。
- `skills/document-templates/SKILL.md`
- `skills/using-shanforge/SKILL.md`
- `skills/project-memory/SKILL.md`
- `skills/writing-plans/SKILL.md`
- `skills/executing-plans/SKILL.md`
- `skills/tdd-workflow/SKILL.md`
- `skills/ui-ux-pro-max/SKILL.md`

## 允许修改

- `docs/index.md`
- `docs/04-project-development/**`
- `.factory/README.md`
- `.factory/project.json`
- `.factory/tech-profile.json`
- `.factory/multi-agent-board.json`
- `.factory/memory/doc-map.md`
- `.factory/memory/tasks.summary.md`
- `.factory/memory/current-state.md`
- `.factory/memory/tests.summary.md`
- `.factory/pm/README.md`
- `.factory/workitems/implementation/README.md`
- `.factory/workitems/DOC-FACTORY-RESTRUCTURE-001/`
- `tests/test_doc_factory_restructure.py`

## 禁止修改

- 历史 work item evidence、reports、reviews 和 ledger。
- 业务代码。
- 无关脏改动。

## 实施步骤

1. 设计方案：确认正式白名单和删除清单。
2. 接口设计：统一状态包字段和 doc-map 回源接口。
3. UI：`N/A`，无界面交付。
4. 测试设计：结构测试固定路径、删除清单、署名和关键字段。
5. 开发：写 Markdown、JSON 和测试，删除旧资产。
6. 单测：运行定向 pytest。
7. 文档校验：运行 docs-stratego validate。
8. review：写 review 输入简报。
9. 写验证证据。
10. 写实现报告。
11. 更新流水账和记忆摘要。

## 失败断言

- 缺测试设计则失败。
- UI 写 `N/A` 但无原因则失败。
- 新正式文档未进入根导航、文档索引或 doc-map 则失败。
- 已删除旧路径仍存在或仍被正式入口引用则失败。
- 正式文档负责人、执行人或版本历史署名为 `Codex` 则失败。
- `.factory` 根 README 仍采用非破坏性迁移口径则失败。

## 验证命令

```bash
uv run pytest tests/test_doc_factory_restructure.py
uvx --from docs-stratego docs-stratego source validate --repo-path .
jq empty .factory/project.json .factory/tech-profile.json .factory/multi-agent-board.json
git diff --check
```

## 输出报告

- 验证证据：`.factory/workitems/DOC-FACTORY-RESTRUCTURE-001/evidence/TASK-001-verification.md`
- 实现报告：`.factory/workitems/DOC-FACTORY-RESTRUCTURE-001/reports/TASK-001-implementer-report.md`
- 评审输入简报：`.factory/workitems/DOC-FACTORY-RESTRUCTURE-001/reviews/TASK-001-review-input.md`
- 流水账事件：`.factory/workitems/DOC-FACTORY-RESTRUCTURE-001/ledger.jsonl`

## 完成口径

实现者只能写 `ready_for_review`。`approved` 必须来自独立评审。
