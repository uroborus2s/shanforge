# T08 独立评审输入

- work_item_id: `SOFTWARE-ENGINEERING-SKILL-REMEDIATION-001`
- task_card_id: `SOFTWARE-ENGINEERING-SKILL-REMEDIATION-001-T08`
- wbs_id: `WBS-REM-08`
- baseline: `d6f8745fdcbcb6fbcdd5fe0de9ca429be15ea077`
- candidate: 当前未提交工作树
- reviewer_type: `independent_subagent`
- write_policy: `state_or_gate_write`

## 必读输入

- `brief.md`
- `plan.md`
- `reports/T08-implementation-summary.md`
- `evidence/T08-verification.md`
- 当前 `git diff` 和全部新增文件

## 评审问题

1. T01-T08 是否逐项满足计划验收，不把测试、review、TaskCard 或产品状态混在一起。
2. 开发、测试、Bug、修复回复是否让非技术用户直接看懂；测试零值、failed/error、完整基线/定向重跑是否无损。
3. 修复报告是否给出真实 file、symbol/章节、change、reason、verification；是否遵守两条代码形态禁令。
4. 工具和版本缺失是否 fail closed，是否仍有不可执行命令或错误承诺。
5. 是否存在范围外改动、不必要抽象、重复合同或回归风险。

## 通过门

- Critical: `0`
- Important: `0`
- Minor 可记录但不阻塞；必须说明是否建议同范围立即修复。
- reviewer 只读，不得修改任何文件、Git、ledger、memory 或外部状态。
