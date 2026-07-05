# Review Score Rubric

用于 loop 结束 review score。总分 100。

## 独立性硬门

- `reviewer_type` 必须写入 `independent_subagent`、`external_human`、`github_review` 或 `same_thread`。
- `reviewer_id` 必须能定位 reviewer、线程、账号或外部评审来源。
- `reviewer_independence_evidence` 必须说明 reviewer 未参与实现，且只读取文件化输入包。
- `same_thread` 只能写 `self_check_passed`。
- `same_thread` 只能写 `author_self_check_score`，不得写 `review_score`。
- `same_thread` 的 `review_status` 只能写 `self_check_passed`。
- `same_thread` 的 `next_gate_status` 必须写 `needs_independent_review`。
- 没有 reviewer 独立性证据时，不得写 `review_score`。
- 没有 reviewer 独立性证据时，不得写 `approved`。
- 没有 reviewer 独立性证据时，`next_gate_status` 必须写 `needs_independent_review`。
- `needs_independent_review` 不是 review 通过结论。
- `approved` 只允许来自 `independent_subagent`、`external_human` 或 `github_review`。

## 评分

- 需求符合度：30
- 架构一致性：20
- 测试充分性：20
- 代码质量：20
- 文档与记忆同步：10

## 结论

- `90-100`：有真实独立 reviewer 证据时可以 `approved`，但仍需人工确认。
- `70-89`：通常 `changes_requested`，除非所有扣分都是非阻塞 Minor。
- `<70`：必须 `changes_requested`。
- 同线程作者自检无论分数多高，都只能写 `self_check_passed` 或 `needs_independent_review`。

## 阻塞规则

- 有 Critical：必须 `changes_requested`。
- 有 Important：默认 `changes_requested`，除非用户明确接受风险。
- 缺 verification evidence：必须 `changes_requested`。
- 未同步必要 `.factory/memory/`：必须 `changes_requested`。
- 缺 `reviewer_type`、`reviewer_id` 或 `reviewer_independence_evidence`：必须 `needs_independent_review`。

## 输出字段

```text
reviewer_type: independent_subagent | external_human | github_review | same_thread
reviewer_id: <thread / account / reviewer id>
reviewer_independence_evidence: <why this reviewer is independent>
author_self_check_score: <0-100 or n/a>
review_score: <0-100 or n/a>
review_status: approved | changes_requested | self_check_passed
next_gate_status: pending_human_confirmation | needs_independent_review | changes_requested

评分：
- 需求符合度：<N> / 30
- 架构一致性：<N> / 20
- 测试充分性：<N> / 20
- 代码质量：<N> / 20
- 文档与记忆同步：<N> / 10
```

`author_self_check_score` 只能用于作者自检参考。它不能进入 `review_score`，也不能作为 `pending_human_confirmation` 的依据。
