# FLOW-CONTRACT-001 独立评审任务

你是独立 reviewer。

不要读取实现者会话历史。只读取本文件列出的输入包。

## Inputs

- Work item：`FLOW-CONTRACT-001`
- Review type：实施前独立评审
- Review package：`.factory/workitems/FLOW-CONTRACT-001/reviews/implementation-pre-review-package.md`
- Requirements：`docs/04-project-development/03-requirements/process-workflow-contract-requirements.md`
- Implementation plan：`docs/04-project-development/05-development-process/process-workflow-contract-implementation-plan.md`
- Work item brief：`.factory/workitems/FLOW-CONTRACT-001/brief.md`
- Work item plan：`.factory/workitems/FLOW-CONTRACT-001/plan.md`
- Task briefs：`.factory/workitems/FLOW-CONTRACT-001/task-briefs/`
- Ledger：`.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`
- Memory summaries：
  - `.factory/memory/doc-map.md`
  - `.factory/memory/tasks.summary.md`
  - `.factory/memory/skill-updates.summary.md`

## Job

1. 核对需求覆盖度。
2. 核对实施方案是否可执行。
3. 核对每个核心 skill 的输入、输出、内部流程和禁止项是否清楚。
4. 核对测试治理、测试环境、端口规则和 evidence 规则是否足够。
5. 核对 memory 条件读取链是否避免上下文重新扩张。
6. 核对任务拆解是否能作为后续实施入口。
7. 核对是否存在中心脚本回退、不必要文档或过度设计。
8. 按 rubric 给出 score。
9. 输出 `approved` 或 `changes_requested`。

## Output

写入：

```text
.factory/workitems/FLOW-CONTRACT-001/reviews/implementation-pre-review.md
```

格式：

```markdown
# FLOW-CONTRACT-001 Implementation Pre-Review

- Work item: FLOW-CONTRACT-001
- reviewer_type: independent_subagent | external_human | github_review
- reviewer_id:
- reviewer_independence_evidence:
- review_status: approved | changes_requested
- next_gate_status: pending_human_confirmation | changes_requested
- review_score: <0-100>

## Findings

### Critical
- ...

### Important
- ...

### Minor
- ...

## Score

- 需求符合度：<N> / 30
- 架构一致性：<N> / 20
- 测试充分性：<N> / 20
- 代码质量：<N> / 20
- 文档与记忆同步：<N> / 10

## Verification

- ...

## Gate

pending_human_confirmation | changes_requested
```

`approved` 不等于人工确认。通过后仍必须等待用户确认。
