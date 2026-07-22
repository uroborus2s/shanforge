# TASK-REQ-006 R006 同一 Reviewer 复审输入

## Reviewer

- reviewer_id: `/root/req006_r005_review`
- 模式：只读；不得修改文件。

## 输入

1. `.factory/workitems/FLOW-CONTRACT-001/reviews/TASK-REQ-006-R005-independent-review.md`
2. `.factory/workitems/FLOW-CONTRACT-001/reviews/TASK-REQ-006-R005-review-feedback-triage-R006.md`
3. `.factory/workitems/FLOW-CONTRACT-001/reviews/TASK-REQ-006-R005-review-response-R006.md`
4. `.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001-R006.md`
5. `.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.contract.R006.json`
6. `.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.pm-field-map.R006.json`
7. `.factory/workitems/FLOW-CONTRACT-001/drafts/project-progress-requirement-contract.R014.json`
8. `.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-REQ-006-R006-review-fix-verification.md`
9. `AGENTS.md`

## 工作

- 逐项判断 `R005-C-001`、`R005-I-001..006` 为 closed / open / regressed。
- 检查 R006 是否产生新的 Critical/Important，尤其是 security profile、R014/field map pin、137 字段覆盖、时间规范化、symbol identity、64 AC 机器语义和 22 条状态转移。
- Critical/Important 非空必须 `changes_requested`。
- 输出独立性证据、真实命令、评分、决定和下一 Gate；不得把 Reviewer approved 冒充人工批准。
