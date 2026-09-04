# 独立中文语言评审任务

## 身份

- reviewer_type: `independent_subagent`
- reviewer_role: `中文语言专家`
- work_item_id: `UI-DESIGN-WORKFLOW-001`
- task_card_id: `UI-DESIGN-WORKFLOW-001-T01`
- write_policy: `state_or_gate_write`
- current_gate: `needs_independent_review`

## 只读输入

- `.factory/workitems/UI-DESIGN-WORKFLOW-001/brief.md`
- `.factory/workitems/UI-DESIGN-WORKFLOW-001/task-briefs/UI-DESIGN-WORKFLOW-001-T01.md`
- `.factory/workitems/UI-DESIGN-WORKFLOW-001/evidence/implementation-verification.md`
- 三个任务范围文件的 `git diff`

## 评审目标

1. 准确：关键页面确认门不改变原有设计顺序；UI/UX 与美术资源职责边界正确。
2. 简洁：新增中文没有重复、堆砌、空泛修饰或可删除成分。
3. 一致：术语与原文一致，路由条件互斥且不会漏掉既有能力。
4. 可执行：测试断言锁定行为语义，而非无关格式。

## 输出

- 结论：`approved` 或 `changes_requested`。
- 问题按 Critical / Important / Minor 分级并定位文件、行和原句。
- 每个问题给出最短替换文本；没有问题时明确写 `C0 / I0 / M0`。
- 不修改任何文件、ledger、Git 或外部系统。
