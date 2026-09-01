# T08 独立评审

- reviewer_type: `independent_subagent`
- reviewer_id: `/root/remediation_t08_independent_review`
- reviewer_independence_evidence: 实现、全量验证和黑盒完成后新建；未参与实现；全程只读。
- review_status: `changes_requested`
- next_gate_status: `changes_requested`

## Critical

无。

## Important

1. `skills/subagent-driven-development/SKILL.md:136` 仍按 ledger 中 `approved` 或 `done` 跳过任务。`approved` 只属于 review_status，新 TaskCard 完成态是 `completed | closed`；旧规则可能漏执行未完成任务或重执行已完成任务。最小修法：只按生命周期终态跳过，review approved 不作为依据，并加反例测试。
2. `skills/stratix-service/references/cli-workflow.md:15` 仍读取 `npm view ... dist-tags` 后给未固定版本的 `create-stratix` 命令，可绕过主 Skill 的固定版本矩阵。最小修法：删除 latest 路径或把它限制为只记录 detected；任何创建命令前先验证显式/已安装版本兼容，否则 blocked，并加反例测试。
3. `evidence/T08-verification.md` 未保存 validator 精确命令和黑盒 v6 完整输入、输出、逐项断言；现有静态测试不能单独证明真实会话行为。最小修法：保存完整黑盒 artifact 和工具回执，并补 validator 精确命令与结果摘要。

## Minor

无当前范围内必须修复的 Minor。

## 计划验收

- T01、T05、T06：通过。
- T02/T03：因旧跳过规则未通过。
- T04：合同文本通过，黑盒证据需补强。
- T07：Crawler4j 和主 Stratix 门通过，CLI 引用未通过。
- T08：存在 3 个 Important，未通过。

## code_shape_check

`passed`。本次 diff 未新增函数内命名函数或单调用点公共 helper。
