# TASK-REQ-006 R005 独立需求评审输入包

## Review 类型

- 类型：真实隔离的只读需求评审。
- 候选状态：`ready_for_independent_review`。
- 目标 Gate：无 Critical/Important 后进入精确 Hash 人工确认。
- Reviewer 禁止修改候选、正式文档、Ledger、Memory、Git 或产品代码。

## 必读输入

1. `.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001-R005.md`
2. `.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.contract.R005.json`
3. `.factory/workitems/FLOW-CONTRACT-001/task-briefs/TASK-REQ-006-project-knowledge-index-and-deterministic-docs.md`
4. `.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-REQ-006-R005-author-verification.md`
5. `.factory/workitems/FLOW-CONTRACT-001/drafts/project-progress-requirement-contract.R014.json`
6. `AGENTS.md`

## 评审问题

1. R005 是否完整且无歧义地替代 R001–R004？
2. 16 条 REQ 和 11 条 NFR 是否可测试、互相一致，并覆盖用户讨论的全部关键决策？
3. `IndexGeneration`、`ProjectProgressSnapshot` 与 `RenderFingerprint` 是否边界清楚？
4. 29 + 10 = 39 表是否无明显缺表、重复事实或不必要永久表？
5. 语义 locator 能否避免标题、行号、代码移动导致的漂移？
6. 静态站点是否明确只读、多页面、全页面详情、完整十要素和来源追踪？
7. durable 异步同步、隔离 worktree、写租约和 Git 生成物边界是否能避免阻塞/污染主任务？
8. 权限撤销、失败恢复、cache 清理和敏感信息边界是否 fail-closed？
9. 是否缺少主流程、异常流程、影响分析、领域 Owner、迁移或回滚验收？
10. `TASK-IMPLEMENT-002-R001` 是否保持隔离？

## 评分与输出

- 使用 `skills/requesting-code-review/references/review-score-rubric.md` 的 100 分结构；本轮“测试充分性/代码质量”解释为需求可测试性与机器合同质量。
- Critical 或 Important 非空则必须 `changes_requested`。
- 输出 reviewer 独立性元数据、逐条 Finding（精确文件/行号）、真实验证命令、评分、`approved|changes_requested` 和下一 Gate。
- Implementer report：N/A，本轮是实现前需求 Gate；请明确接受或拒绝该 N/A。
- 产品代码/测试 diff：N/A，本轮禁止产品实现；请明确接受或拒绝该 N/A。
