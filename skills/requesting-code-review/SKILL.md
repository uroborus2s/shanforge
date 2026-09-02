---
name: requesting-code-review
description: 批次或里程碑开发完成、PR 前、高风险专项或需要独立裁判时使用；组织 Shanforge 集中代码 review、必要任务级 review、PR review 和人工确认门。普通低中风险任务不逐项触发。
---

# 请求代码评审

本 skill 用于把实现成果交给独立 reviewer。它不替代实现者自检，也不替代人工确认。

## v1.2.0 运行时路由合同

- `SB-REVIEW` 进入 `review-workflow`，`write_policy: state_or_gate_write`。
- 写 review 或 Gate 前，route 必须有已存在且非空的 `work_item_id`、`task_card_id`，以及精确
  `allowed_paths`、`forbidden_actions`、`current_gate`、`write_policy`。
- Reviewer 只读实现输入；只追加 review、ledger 和 evidence，不改实现。
- 返回 `status`、`outputs`、`evidence`、`ledger_event`、`gate` 和本地 `needs`；`approved` 不等于
  Verification 或人工批准。

## 触发

- 全部授权开发任务或已批准里程碑完成，准备做集中质量 review。
- 高风险设计或实现到达专项 review checkpoint。
- PR 前需要确认是否 ready to merge。
- 用户明确要求任务级 review。

## 输入

- 已批准目标、计划或适用的 task brief。
- 批次实现摘要和最终 verification evidence；高风险专项可只提供受影响范围摘要。
- diff package：`git diff`、暂存 diff、文件清单或 PR diff
- work item ledger：`.factory/workitems/<WORKITEM-ID>/ledger.jsonl`
- review ledger：`.factory/memory/review-ledger.jsonl`

## 输出

- task review：`.factory/workitems/<WORKITEM-ID>/reviews/task-N-review.md`
- PR review：`.factory/workitems/<WORKITEM-ID>/reviews/pr-review.md`
- independent review task：`.factory/workitems/<WORKITEM-ID>/reviews/independent-review-task.md`
- review ledger event：`.factory/memory/review-ledger.jsonl`
- work item ledger event：`.factory/workitems/<WORKITEM-ID>/ledger.jsonl`

## 含义保留清单

- 普通低、中风险任务不逐项 review；高风险问题尽早 review，其他问题在批次末集中处理。
- reviewer 只拿精心组织的输入包，不继承实现者会话历史。
- 集中 review 同时覆盖 Spec Review（需求符合度）和 Quality Review（代码质量）；高风险任务级 review
  只覆盖受影响范围。
- Critical 必须修。
- Important 必须在继续前处理或明确登记为用户接受风险。
- Minor 可以登记到后续。
- 真实独立 reviewer 结论可以是 `approved` 或 `changes_requested`。
- 不能把 reviewer approved 当成人工确认。
- loop 结束必须输出 `human_confirmation_required` 和原因；只有真实人工 Gate 才进入 `pending_human_confirmation`。
- 同线程作者自检只能输出 `self_check_passed`，下一 gate 必须是 `needs_independent_review`，不得写成 `approved` 或 review 通过。
- `approved` 必须带 `reviewer_type`、`reviewer_id` 和 `reviewer_independence_evidence`。

## 默认流程

1. 确认 review 类型：批次 / 里程碑 review、高风险任务级 review、PR review 或真实独立 review task。
2. 收集最小输入：批准目标、diff、最终验证摘要、风险和未决问题；不要求逐任务 report 或 evidence。
3. 批次或高风险任务级 review 使用 [task-review-template.md](references/task-review-template.md)。
4. PR review 使用 [pr-review-template.md](references/pr-review-template.md)。
5. 真实隔离 review 使用 [independent-review-task-template.md](references/independent-review-task-template.md)。
6. 按 [review-score-rubric.md](references/review-score-rubric.md) 打分。
7. 发现 Critical 或 Important 时，结论写 `changes_requested`。
8. 无阻塞问题且有真实独立 reviewer 证据时，结论才可以写 `approved`。
9. 每个批次只写一份最终 review 和一条 review ledger event。
10. reviewer 返回 `changes_requested` 时直接在原 diff 上整改并重跑受影响测试；只有 Critical、Important
    或高风险路径变化才复审受影响范围；不写 triage 或 response，只组织 review 与原范围整改。
11. loop 结束时写明 `human_confirmation_required: true | false` 和 `gate_reason`。只有真实人工 Gate 才写 `pending_human_confirmation`；普通任务 review 通过则返回流程总控继续既有授权范围内的验证、后续任务或收口。

## 只读评审与同范围整改

- 只读独立评审是已授权任务的内部质量动作。任务已授权且 reviewer 只读取任务输入包时，无需为只读派发单独请求人工授权。
- review 派发不扩大原授权范围，也不得授权 reviewer 修改代码、正式文档、ledger、Git 或外部系统。
- `changes_requested` 中的技术 Finding 可以在原目标、允许文件和风险边界内修复时，自动进入同范围整改循环；
  只有阻断级或高风险变化需要复审。
- Finding 需要产品取舍、风险接受、新文件或新系统范围、忽略 Critical/Important，或破坏性或外部动作时，才设置 `human_confirmation_required: true`。
- reviewer `approved` 只代表独立质量结论，不能冒充 `human_approved`；但也不自动制造人工确认 Gate。

## 独立性硬门

- `reviewer_type` 必须写入 `independent_subagent`、`external_human`、`github_review` 或 `same_thread`。
- `reviewer_id` 必须能定位 reviewer、线程、账号或外部评审来源。
- `reviewer_independence_evidence` 必须说明 reviewer 未参与实现，且只读取文件化输入包。
- `same_thread` 表示当前会话作者自检，不是真实独立评审。
- 作者自检不能 `approved`。
- 同线程作者自检只能输出 `self_check_passed`，只能写 `author_self_check_score`，不得写 `review_score`。
- 同线程作者自检的 review 输出状态只能是 `self_check_passed`。
- 同线程作者自检后的下一 gate 状态必须是 `needs_independent_review`。
- 禁止把 `needs_independent_review` 写成 review 通过结论。
- 没有真实独立 reviewer 证据时，下一 gate 状态必须是 `needs_independent_review`。
- 只读 reviewer 已包含在用户授权任务的内部质量范围时，无需重复请求子 agent 授权；若 reviewer 需要写入、访问外部系统或超出输入包，必须停止并请求授权。
- 没有独立证据时，禁止写 `pending_human_confirmation`。

## N/A 审查门

- N/A 必须由 reviewer 明确接受或拒绝。
- reviewer 接受 N/A 时，必须写明接受理由和覆盖范围。
- reviewer 拒绝 N/A 时，必须列为 `changes_requested` 或登记为用户接受风险。
- 未被 reviewer 接受的 N/A 不得通过 review。

## Severity

- `Critical`：错误行为、安全风险、数据损坏、不可用、违背核心需求。
- `Important`：明显架构、测试、维护、兼容或需求缺口。
- `Minor`：不阻塞的风格、文档、命名或后续优化。

## 禁止

- 禁止为普通低、中风险任务强制逐项独立 review。
- 禁止 reviewer 直接相信 implementer report。
- 禁止 reviewer 不读 diff 就给结论。
- 禁止 Critical 或 Important 未处理就继续下一阶段。
- 禁止把 reviewer approved 写成 `done`。
- 禁止把 reviewer approved 当成人工确认。
- 禁止用 PR review 替代任务级 Spec Review。
- 禁止同线程作者自检写 `review_score`。
- 禁止缺少 `reviewer_type`、`reviewer_id` 和 `reviewer_independence_evidence` 时写 `approved`。

## 完成状态

本 skill 的完成状态是批次或高风险专项 review 文件和 ledger 事件已写入，并输出标准状态包。
需要独立评审但没有独立证据时，`status` 只能是 `self_check_passed`，`next_gate_status` 必须是
`needs_independent_review`。普通低、中风险任务不会单独进入本 skill。

```text
工作结果：
- work_item: <WORKITEM-ID>
- skill: requesting-code-review
- status: approved | changes_requested | self_check_passed | blocked | needs_user_input
- human_confirmation_required: true | false
- gate_reason: <none | product_decision | risk_acceptance | scope_expansion | destructive_or_external_action | governance_gate>
- outputs:
  - <review file path>
- evidence:
  - <diff package / reviewer independence evidence / verification summary>
- ledger_event: <review ledger event id or none>
- needs:
  - feedback_fix | independent_review | human_confirmation | user_input | none
```

`blocked` 用于批次缺批准目标、diff、最终 verification evidence、reviewer 独立性证据或 ledger 写入能力，
导致不能给出可信 review 结论的情况。

`needs_user_input` 用于 review 类型、N/A 风险接受、review 范围或外部 reviewer 身份必须由用户确认的情况。已授权任务内的独立只读 reviewer 派发不属于该状态。
