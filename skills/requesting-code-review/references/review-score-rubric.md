# Review Evidence Rubric

默认以证据作出范围结论，不以分数替代判断。历史报告中的分数只读保留，不回写或重算。

## 独立性硬门

- `reviewer_type` 必须写入 `independent_subagent`、`external_human`、`github_review` 或 `same_thread`。
- `reviewer_id` 必须能定位 reviewer、线程、账号或外部评审来源。
- `reviewer_independence_evidence` 必须说明 reviewer 未参与实现，且只读取文件化输入包。
- `same_thread` 只能写 `self_check_passed`。
- `same_thread` 的 `review_status` 只能写 `self_check_passed`。
- `same_thread` 的 `next_gate_status` 必须写 `needs_independent_review`。
- `same_thread` 即使明确请求辅助评分，也只能写 `author_self_check_score`，不得写 `review_score`。
- 没有 reviewer 独立性证据时，不得写 `approved`。
- 没有 reviewer 独立性证据时，`next_gate_status` 必须写 `needs_independent_review`。
- `needs_independent_review` 不是 review 通过结论。
- `approved` 只允许来自 `independent_subagent`、`external_human` 或 `github_review`。

## 默认范围结论

- `本范围通过`：已检查范围的需求、候选、证据和 Finding 均支持 `approved`，且有独立性证据。
- `需整改`：存在 Critical、未接受的 Important 或可定位的需求/质量缺口，对应 `changes_requested`。
- `证据不足`：缺候选、需求版本、覆盖证据或独立性证据；不能因“未发现问题”而通过。

## 可选辅助评分

默认不输出 `review_score` 或 `author_self_check_score`。仅在明确请求辅助评分时才出现整个评分块；评分不能决定通过、整改或 Gate。

| 检查项 | 权重 | 适用与证据 |
|---|---:|---|
| 需求符合度 | 30 | 有对应需求/标准版本与核对证据才计入 |
| 架构一致性 | 20 | 架构约束适用且有检查证据才计入 |
| 测试充分性 | 20 | 测试要求适用且有新鲜证据才计入 |
| 代码质量 | 20 | 有候选与 diff 检查证据才计入 |
| 文档与记忆同步 | 10 | 适用且有同步或 N/A 接受证据才计入 |

仅用户要求评分时，评审前固定具体可验证检查项及权重/适用分母；证据满足记其权重，不满足或缺证据记 0。N/A 须独立接受并公开分母变化，分母为 0 则无法计算。不得按印象给小数或临时改检查项追高分；复审同版本候选的分数变化必须逐项写明 Finding、证据或适用分母的差异依据。

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
scope_conclusion: 本范围通过 | 需整改 | 证据不足
review_status: approved | changes_requested | self_check_passed
next_gate_status: return_to_orchestrator | pending_human_confirmation | needs_independent_review | changes_requested
```

明确请求辅助评分时，独立 reviewer 追加：

```text
review_score: <earned>/<applicable denominator>
- <检查项>: <earned>/<weight>; evidence: <path>; variance: <首次或与前次差异依据>
```

同线程作者仅可追加 `author_self_check_score: <earned>/<applicable denominator>`，仍不得输出 `review_score`。

真实独立 reviewer 的 `approved` 默认使用 `return_to_orchestrator`；只有输入包已声明真实人工 Gate 并提供原因时，才使用 `pending_human_confirmation`。
