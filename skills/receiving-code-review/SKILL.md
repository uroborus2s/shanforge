---
name: receiving-code-review
description: 收到 review feedback、PR 评论、任务评审意见或外部 reviewer 建议时使用；先核实反馈再修改，禁止盲改和表演式同意。
---

# 处理代码评审反馈

本 skill 用于处理 review feedback。目标是技术正确，而不是显得顺从。

## 触发

- 用户要求处理 review 意见。
- 收到 PR 评论、inline comment、task review 或外部 reviewer 建议。
- 收到 review 结果为 `changes_requested`。
- 反馈不清楚、可能错误或涉及架构取舍。

## 核心原则

- 先核实反馈再修改。
- 不清楚就先问。
- 技术正确优先于表演式同意。
- 禁止表演式同意。
- 禁止盲改。
- 一次处理一个反馈项。
- 每项修复后都要验证。

## 默认流程

1. 完整读取所有 review feedback。
2. 按 [feedback-triage-template.md](references/feedback-triage-template.md) 建立 triage。
3. 对每项反馈复述技术要求。
4. 判断是否清楚；不清楚就先问。
5. 核实反馈是否符合当前代码、测试、架构和用户决策。
6. 判断 severity：Critical、Important、Minor。
7. 先处理阻塞项，再处理简单项，再处理复杂项。
8. 每次只改一个反馈项或一组强相关反馈。
9. 每项修复后运行对应验证。
10. 按 [review-response-template.md](references/review-response-template.md) 写 response。
11. 写入 `.factory/workitems/<WORKITEM-ID>/reports/` 和 `.factory/workitems/<WORKITEM-ID>/reviews/`。
12. 更新 `.factory/workitems/<WORKITEM-ID>/ledger.jsonl`。
13. 执行 memory sync，更新 `.factory/memory/review-ledger.jsonl`、`.factory/memory/tasks.summary.md` 和必要 summary。

## 外部反馈处理

外部 reviewer 的反馈是建议，不是命令。实施前检查：

- 是否技术正确。
- 是否会破坏现有功能。
- 当前实现是否有兼容或历史原因。
- 是否适用于本项目栈和版本。
- 是否与用户已有架构决策冲突。
- 是否违反 YAGNI。

如果反馈错误，使用技术理由 pushback。不要防御性表达。

## 禁止

- 禁止写表演式同意句。
- 禁止在未核实前说要实现。
- 禁止不清楚时先改一部分。
- 禁止把所有反馈混成一个大改动。
- 禁止不跑验证就说 fixed。
- 禁止为未使用功能补“专业化”扩展，除非用户确认需要。

## 输出位置

- triage：`.factory/workitems/<WORKITEM-ID>/reviews/review-feedback-triage.md`
- response：`.factory/workitems/<WORKITEM-ID>/reviews/review-response.md`
- 修复报告：`.factory/workitems/<WORKITEM-ID>/reports/review-fix-report.md`
- 验证证据：`.factory/workitems/<WORKITEM-ID>/evidence/review-fix-verification.md`
- review ledger：`.factory/memory/review-ledger.jsonl`
- task summary：`.factory/memory/tasks.summary.md`

## memory sync

- `.factory/memory/review-ledger.jsonl` 必须记录每个 feedback item 的处理结论。
- `.factory/memory/tasks.summary.md` 必须记录 work item 的最新状态和剩余 `needs`。
- 若修改了流程、skill、测试或正式文档，还必须同步对应 `.factory/memory/*summary.md`。
- memory sync 不是可选附加项；缺失时不得输出完成状态。

## 完成状态

只有反馈已分类、修复已验证、response 已写入、ledger 和 memory 已同步，才能输出完成状态与剩余 `needs`。
