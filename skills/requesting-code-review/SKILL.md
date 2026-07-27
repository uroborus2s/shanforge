---
name: requesting-code-review
description: 完成任务、阶段性实现、PR 前或需要独立裁判时使用；组织 Shanforge 任务级 review、PR review、独立 review task、评分表和人工确认门。
---

# 请求代码评审

本 skill 用于把实现成果交给独立 reviewer。它不替代实现者自检，也不替代人工确认。

## v1.2.0 运行时路由合同

- `SB-REVIEW` 进入 `review-workflow`，`write_policy: state_or_gate_write`。
- 写 review 或 Gate 前，route 必须有已存在且非空的 `work_item_id`、`task_card_id`，以及精确
  `allowed_paths`、`forbidden_actions`、`current_gate`、`write_policy`。
- Reviewer 只读实现输入；只追加 review、ledger 和 evidence，不改实现。
- 返回 `status`、`outputs`、`evidence`、`ledger_event`、`gate`、`next_required_action`；`approved` 不等于
  Verification 或人工批准。

## 触发

- 单个 task 实现完成，准备进入任务级 review。
- 实现流程到达 review checkpoint。
- 主要功能完成，准备做整体质量 review。
- PR 前需要确认是否 ready to merge。
- 实现者返回 `ready_for_review`。

## 输入

- task brief：`.factory/workitems/<WORKITEM-ID>/task-briefs/`
- implementer report：`.factory/workitems/<WORKITEM-ID>/reports/`
- verification evidence：`.factory/workitems/<WORKITEM-ID>/evidence/`
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

- Review 要早做、常做，防止问题扩散。
- reviewer 只拿精心组织的输入包，不继承实现者会话历史。
- 任务级 review 至少包含 Spec Review 和 Quality Review。
- Critical 必须修。
- Important 必须在继续前处理或明确登记为用户接受风险。
- Minor 可以登记到后续。
- 真实独立 reviewer 结论可以是 `approved` 或 `changes_requested`。
- 不能把 reviewer approved 当成人工确认。
- loop 结束必须进入 `pending_human_confirmation`。
- 同线程作者自检只能输出 `self_check_passed`。
- 禁止把同线程复核写成 `approved`。
- 同线程作者自检的 review 输出状态只能是 `self_check_passed`。
- 同线程作者自检后的下一 gate 状态必须是 `needs_independent_review`。
- 禁止把 `needs_independent_review` 写成 review 通过结论。
- 没有真实独立 reviewer 证据时，下一 gate 状态必须是 `needs_independent_review`。
- `approved` 必须带 `reviewer_type`、`reviewer_id` 和 `reviewer_independence_evidence`。

## 默认流程

1. 确认 review 类型：任务级 review、PR review、真实独立 review task 或整体质量 review。
2. 收集输入包；缺 task brief、report、evidence 或 diff 时先停止。
3. 任务级 review 使用 [task-review-template.md](references/task-review-template.md)。
4. PR review 使用 [pr-review-template.md](references/pr-review-template.md)。
5. 真实隔离 review 使用 [independent-review-task-template.md](references/independent-review-task-template.md)。
6. 按 [review-score-rubric.md](references/review-score-rubric.md) 打分。
7. 发现 Critical 或 Important 时，结论写 `changes_requested`。
8. 无阻塞问题且有真实独立 reviewer 证据时，结论才可以写 `approved`。
9. 写入 review 文件和 `.factory/memory/review-ledger.jsonl`。
10. loop 结束时，只有真实独立 review `approved` 才能把 work item ledger 写为 `pending_human_confirmation`。

## 独立性硬门

- `reviewer_type` 必须写入 `independent_subagent`、`external_human`、`github_review` 或 `same_thread`。
- `reviewer_id` 必须能定位 reviewer、线程、账号或外部评审来源。
- `reviewer_independence_evidence` 必须说明 reviewer 未参与实现，且只读取文件化输入包。
- `same_thread` 表示当前会话作者自检，不是真实独立评审。
- 作者自检不能 `approved`。
- 同线程作者自检只能输出 `self_check_passed`，只能写 `author_self_check_score`，不得写 `review_score`。
- 禁止把同线程复核写成 `approved`。
- 同线程作者自检的 review 输出状态只能是 `self_check_passed`。
- 同线程作者自检后的下一 gate 状态必须是 `needs_independent_review`。
- 禁止把 `needs_independent_review` 写成 review 通过结论。
- 没有真实独立 reviewer 证据时，下一 gate 状态必须是 `needs_independent_review`。
- 需要子 agent 但用户未授权时，必须停止并请求授权。
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

- 禁止跳过 review，因为“改动很小”。
- 禁止 reviewer 直接相信 implementer report。
- 禁止 reviewer 不读 diff 就给结论。
- 禁止 Critical 或 Important 未处理就继续下一阶段。
- 禁止把 reviewer approved 写成 `done`。
- 禁止把 reviewer approved 当成人工确认。
- 禁止用 PR review 替代任务级 Spec Review。
- 禁止同线程作者自检写 `review_score`。
- 禁止缺少 `reviewer_type`、`reviewer_id` 和 `reviewer_independence_evidence` 时写 `approved`。

## 完成状态

本 skill 的完成状态是 review 文件和 ledger 事件已写入，并输出标准状态包。没有独立评审证据时，`status` 只能是 `self_check_passed`，`next_gate_status` 必须是 `needs_independent_review`。是否进入下一阶段，由人工确认门和流程总控决定。

```text
工作结果：
- work_item: <WORKITEM-ID>
- skill: requesting-code-review
- status: approved | changes_requested | self_check_passed | blocked | needs_user_input
- outputs:
  - <review file path>
- evidence:
  - <diff package / reviewer independence evidence / verification summary>
- ledger_event: <review ledger event id or none>
- needs:
  - feedback_fix | independent_review | human_confirmation | user_input | none
```

`blocked` 用于缺 task brief、implementer report、verification evidence、diff package、reviewer 独立性证据或 ledger 写入能力，导致不能给出可信 review 结论的情况。

`needs_user_input` 用于 review 类型、授权子 agent、N/A 风险接受、review 范围或外部 reviewer 身份必须由用户确认的情况。
