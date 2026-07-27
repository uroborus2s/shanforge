# FLOW-CONTRACT-001 Brief

## 版本信息

| 项目 | 内容 |
|---|---|
| 文档编号 | `FLOW-CONTRACT-001-BRIEF` |
| 文档类型 | 工作项简报 |
| 当前版本 | `0.2.0` |
| 当前状态 | 已关闭 |
| 最近更新 | 2026-07-27 |

## 版本历史

| 版本 | 修改内容 | 日期 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `0.2.0` | 15 项顺序实施队列全部完成，最终实现已提交并关闭工作项 | 2026-07-27 | Codex | 独立复审通过 | 用户授权收口 |
| `0.1.0` | 建立流程契约工作项，关联正式需求和实施方案 | 2026-07-06 | Codex | 待审核 | 待批准 |

## 目标

把用户关于四类场景、三层文档、记忆结构、项目管理、领域模块、前后端设计、版本管理和防跳步门禁的讨论落为正式需求与实施计划。

## 非目标

- 不直接修改 workflow skill。
- 不提交代码。
- 不关闭需求或任务。

## 背景与当前状态

当前 Shanforge 已完成 Superpowers workflow skill-first 集成，但用户要求进一步建立完整流程契约。正式需求见 `docs/04-project-development/03-requirements/process-workflow-contract-requirements.md`，正式实施方案见 `docs/04-project-development/05-development-process/process-workflow-contract-implementation-plan.md`。

## 用户意图

用户要求先完整设计，再优化每个 skill；设计必须覆盖业务流程管控、代码或 skill 调用图、运行时文档设计、每个 skill 的输入输出和内部流程，并拆成具体任务。

## 成功标准

- 正式需求文档存在并覆盖所有讨论点。
- 正式实施方案存在并包含具体任务。
- 根导航、doc-map 和 memory 摘要同步。
- 本工作项 ledger 记录需求分析和计划输出。

## 影响范围

- `docs/04-project-development/03-requirements/`
- `docs/04-project-development/05-development-process/`
- `docs/index.md`
- `.factory/memory/doc-map.md`
- `.factory/memory/tasks.summary.md`
- `.factory/workitems/FLOW-CONTRACT-001/`

## 需要同步的文档、测试和 memory

- 文档：正式需求、正式实施方案、根导航、开发过程首页。
- memory：`doc-map.md`、`tasks.summary.md`。
- 测试：文档导航和 diff 校验；skill 改造测试后续任务执行。

## 未决问题

- 无。收口提交与其他未关闭 WorkItem 盘点见
  `.factory/workitems/FLOW-CONTRACT-001/reports/FLOW-CONTRACT-001-closeout-and-open-workitems-audit.md`。
