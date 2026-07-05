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
- next_gate_status: pending_human_confirmation | needs_independent_review | changes_requested
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

pending_human_confirmation | needs_independent_review | changes_requested
```

`approved` 只表示 reviewer 通过。它不等于人工确认。

## 独立性门

- `same_thread` 只能输出 `self_check_passed`。
- `same_thread` 只能写 `author_self_check_score`，不得写 `review_score`。
- 没有 `reviewer_type`、`reviewer_id` 和 `reviewer_independence_evidence` 时，`next_gate_status` 必须写 `needs_independent_review`。
- `needs_independent_review` 不是 review 通过结论。
- `approved` 必须来自真实独立 reviewer。
