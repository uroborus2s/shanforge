# PR Review

用于 PR 前或 PR 内整体 review。

## Inputs

- PR：
- Base：
- Head：
- diff package：
- linked work item：
- task review list：
- verification evidence：

## Git Range

```bash
git diff --stat <Base>..<Head>
git diff <Base>..<Head>
```

如果没有 commit range，使用工作区 diff package，并写明来源。

## What to Check

- 是否满足 plan 和需求。
- 是否所有 task review 都已处理。
- 是否仍有 Critical 或 Important。
- 是否测试证据新鲜。
- 是否同步 docs 和 `.factory/memory/`。
- 是否存在无关改动。
- 是否 Ready to merge。

## Severity

- Critical
- Important
- Minor

## Output

```markdown
# PR Review

- reviewer_type: independent_subagent | external_human | github_review | same_thread
- reviewer_id:
- reviewer_independence_evidence:
- review_status: approved | changes_requested | self_check_passed
- next_gate_status: return_to_orchestrator | pending_human_confirmation | needs_independent_review | changes_requested
- author_self_check_score: <0-100 or n/a>
- review_score: <0-100 or n/a>

## Strengths
- <specific strength>

## Issues

### Critical
- [file:line] <issue>

### Important
- [file:line] <issue>

### Minor
- [file:line] <issue>

## Assessment

Ready to merge: Yes | No | With fixes
Reasoning: <1-2 sentences>
```

## 独立性门

- `same_thread` 只能输出 `self_check_passed`。
- `same_thread` 只能写 `author_self_check_score`，不得写 `review_score`。
- 缺 `reviewer_type`、`reviewer_id` 或 `reviewer_independence_evidence` 时，`next_gate_status` 必须写 `needs_independent_review`。
- 真实独立 reviewer 的 `approved` 默认写 `return_to_orchestrator`；仅真实人工 Gate 写 `pending_human_confirmation`。
