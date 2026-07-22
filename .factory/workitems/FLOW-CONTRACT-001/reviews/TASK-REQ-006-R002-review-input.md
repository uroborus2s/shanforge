# TASK-REQ-006 R002 独立需求评审输入

## Dispatch

- Work item：`FLOW-CONTRACT-001`
- Task：`TASK-REQ-006-project-knowledge-index-and-deterministic-docs`
- Review type：任务级需求 Spec + Quality Review
- Reviewer：未参与需求编制的独立只读 Reviewer
- Reviewer 唯一允许写入：`.factory/workitems/FLOW-CONTRACT-001/reviews/TASK-REQ-006-R002-independent-review.md`
- 禁止：修改候选、正式 docs、代码、测试、ledger、memory、Git 或外部系统

## Inputs

1. `.factory/workitems/FLOW-CONTRACT-001/task-briefs/TASK-REQ-006-project-knowledge-index-and-deterministic-docs.md`
2. `.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001-R001.md`
3. `.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.contract.R001.json`
4. `.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001-R002.md`
5. `.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.contract.R002.json`
6. `.factory/workitems/FLOW-CONTRACT-001/reports/TASK-REQ-006-R001-requirements-report.md`
7. `.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-REQ-006-R001-author-verification.md`
8. `.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-REQ-006-R002-author-verification.md`

## Relevant existing formal constraints

- `docs/04-product/prd.md`：`WF-CTL-001/009/010`、SQLite 只作可重建投影、`MemoryRecoveryContext/v1` 8 KiB 与 200 条/1 MiB/1,000 ms 上限、Artifact `PT168H`、`NFR-AI-WORKFLOW-005`、`AC-G6`。
- `AGENTS.md`：`access -> application -> domain -> runtime -> settings`；SQLite/装配不得破坏分层。
- 当前 `TASK-IMPLEMENT-002-R001` 已冻结在独立精确 Hash 人工 Gate，本候选必须保持隔离。

## Review questions

1. 是否完整覆盖用户七类意图，且没有把同义能力重复成新 Workflow？
2. `docs/.factory/SQLite/generated` 事实边界是否清晰、无互相覆盖？
3. 单一记忆点与 `ContextReadTicket` 是否既限制扩散又允许必要回源？
4. “事件驱动为主、计划维护兜底、会话内不定时压缩”是否可执行且无隐藏正确性依赖？
5. TTL、容量、事件/字节阈值是否有依据、是否应配置化或留给设计验证？
6. 命令面与性能/NFR 是否可测试，是否过度设计？
7. 是否遗漏 cache legal hold、路径安全、SQLite 重建、快照原子性或 HTML 权限问题？
8. Baseline 影响是否足以阻止在正式需求批准前修改设计和实现？
9. PM 去事实化、每个权限/查询只保留 `current.html` 和刷新指纹是否安全且不会无限产生 scope 目录？

## Required output

按 `requesting-code-review` rubric 写独立性元数据、Spec/Quality 结论、分项评分、Critical/Important/Minor Findings、真实验证命令和 Gate。任一 Critical/Important 必须 `changes_requested`；无阻塞 Finding 才可 `approved`，但不能标记任务完成或冒充人工批准。
