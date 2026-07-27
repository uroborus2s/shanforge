# Iteration 6 Review Root Cause Report

## 结果

- `status`: `root_cause_found`
- 直接原因：全量平均分低于 97；旧完整测试曾有 1 个断言失败。
- 根源原因：验收合同未冻结评分集合、公式和测试清单，同时把不可兼容的全量
  97 分门槛与 8 项最小整改范围绑定在一起。

## 当前事实

- 旧失败测试当前为 `5 passed`，不能再复现原失败。
- 旧完整 workflow 命令引用已删除测试文件，当前直接退出。
- 当前 Skill 数为 37，不再是旧评分的 36。
- 8 项全满分也无法达到旧全量 97 分门槛。

## 需要人工确认的决策

必须二选一，不能由执行者替项目 owner 决定：

1. 最小路径：把 Iteration 6 验收限定为明确的整改集合，冻结当前文件清单、
   评分公式和现存 workflow 测试清单，再复审。
2. 全量路径：保留全仓平均 `>=97`，新建覆盖当前 37 个 Skill 的全量语言与
   Prompt 改造计划。

确认根因后仍需先形成修复方案并再次确认，才能改 Skill、测试或 Gate。

```text
工作结果：
- work_item: SKILL-FLOW-AUDIT-001
- skill: systematic-debugging
- status: root_cause_found
- outputs:
  - .factory/workitems/SKILL-FLOW-AUDIT-001/reports/iteration-6-review-root-cause-20260727.md
- evidence:
  - .factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-6-review-root-cause-20260727.md
- ledger_event: skill-flow-audit-001-20260727-096
- needs:
  - human_confirmation
```
