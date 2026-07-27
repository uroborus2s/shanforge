# Iteration 6 最小路径修复计划

## 结果

- `status`: `ready_for_review`
- 用户决策：采用最小路径。
- 根因处理：用冻结的 8 Skill 整改集合、评分公式和 37 节点测试清单替代
  不可达的全仓平均分 Gate。

## 最小实施

1. 保留旧任务卡和旧评审，新增验收修订，不改写历史。
2. 校验 8 个候选 Skill 的冻结哈希。
3. 运行 37 个相关 workflow 测试节点、相关测试文件 Ruff、JSONL 和 diff check。
4. 独立 reviewer 按冻结公式复评 8 个 Skill。
5. 通过后进入人工确认；不启动全仓 37 Skill 改造。

## 不做

- 不为了分数改动未点名 Skill。
- 不修改当前已通过的 `test_independent_review_gate.py`。
- 不新增评分脚本、中心 registry 或全局 Gate。
- 不修复属于 UI、共享 memory、历史文档迁移等其他 WorkItem 的旧断言。

## 验证结果

- 冻结 37 个相关测试节点：`37 passed`。
- 相关 Ruff：通过。
- 8 个 Skill 与共享回写契约哈希：通过。
- JSONL 与 diff check：通过。

```text
工作结果：
- work_item: SKILL-FLOW-AUDIT-001
- skill: requirements-engineering
- status: ready_for_review
- outputs:
  - .factory/workitems/SKILL-FLOW-AUDIT-001/task-briefs/iteration-6-minimal-acceptance-amendment.md
- evidence:
  - .factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-6-review-root-cause-20260727.md
- ledger_event: skill-flow-audit-001-20260727-098
- needs:
  - verification
  - independent_review
```
