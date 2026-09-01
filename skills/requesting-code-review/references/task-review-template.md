# Task Review

用于单个任务完成后的任务级 review。

## Inputs

- Work item：
- Task：
- task brief：
- implementer report：
- verification evidence：
- diff package：
- ledger：

## Spec Review

检查是否满足 task brief：

- 是否实现全部需求。
- 是否有缺失需求。
- 是否有额外工作。
- 是否修改允许范围外文件。
- 是否把计划外行为写成完成。

## Quality Review

检查实现质量：

- 测试是否覆盖真实行为。
- 是否存在 Critical / Important / Minor 问题。
- 是否遵守分层和接口 owner。
- 是否有不必要抽象。
- 是否同步文档和 memory。

## Output

```markdown
# Task Review

- Work item:
- Task:
- reviewer_type: independent_subagent | external_human | github_review | same_thread
- reviewer_id:
- reviewer_independence_evidence:
- review_status: approved | changes_requested | self_check_passed
- next_gate_status: return_to_orchestrator | pending_human_confirmation | needs_independent_review | changes_requested
- author_self_check_score: <0-100 or n/a>
- review_score: <0-100 or n/a>

## Findings

### Critical
- [file:line] <issue> - <impact>

### Important
- [file:line] <issue> - <impact>

### Minor
- [file:line] <issue> - <impact>

## Verification

- <command>: <real result>

## Gate

return_to_orchestrator | pending_human_confirmation | needs_independent_review | changes_requested
```

`approved` 只表示 reviewer 通过。它不等于人工确认。
`approved` 只允许作为 `review_status`，不得改变 TaskCard 生命周期状态；TaskCard 只能是
`planned | active | ready_for_review | completed | closed | blocked`。产品和 WBS 完成只认
`completed | closed | superseded`。
默认 gate 是 `return_to_orchestrator`；只有输入包已存在真实人工 Gate 时才写 `pending_human_confirmation`。

## 独立性门

- `same_thread` 只能输出 `self_check_passed`。
- `same_thread` 只能写 `author_self_check_score`，不得写 `review_score`。
- 没有 `reviewer_type`、`reviewer_id` 和 `reviewer_independence_evidence` 时，`next_gate_status` 必须写 `needs_independent_review`。
- `needs_independent_review` 不是 review 通过结论。
- `approved` 必须来自真实独立 reviewer。
