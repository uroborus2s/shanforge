# 动态子模型派发交付

- 当前状态：实现、独立终审和最终集成验证通过，进入本地提交。
- 本批范围：20个当前合同、角色、正式说明与测试文件；不评定 Shanforge 全产品完成度。
- 选择责任：用户决定主会话模型；父会话按每个子任务的复杂度、风险、推理需求和实际宿主能力选档。

| 任务 | 默认模型与推理强度 |
|---|---|
| 明确、局部且低风险 | Luna / low |
| 日常明确实现 | Terra / medium |
| 设计判断、跨模块或复杂任务 | Astra / high |
| 普通独立审查 | Terra / high |
| 深度排查或高风险任务/审查 | Astra / xhigh |
| 有复现和排查证据仍未解的单个难题 | Astra / max |

唯一模型决策表位于 skills/using-shanforge/SKILL.md，其他合同引用它。每次显式传 model、reasoning_effort、fork_turns=none。Ultra不作普通子任务默认effort；它不会因任务量大而替所有子代理设最高档。

授权worker必须真实派发；analyst只做已有项目中的只读分析；独立reviewer不参与自身实现。模型、effort或只读role不可用时失败关闭。换模型/强度/角色需要新dispatch_id及新spawn，保留旧回执；followup_task不能重配既有代理。

## 验证和边界

- 显式真实派发回执：reviews/dispatch-receipts.jsonl。
- 12个独立决策模拟：evidence/forward-trial.json；不是12次真实宿主派发。
- v5独立评审批准20文件；MODEL-DYN-I-01已关闭，首轮漏检与整改证据完整保留。
- 最终主目录420 passed / 11 subtests passed；Ruff、3个skill校验通过；代码形状与HEAD比较无新增违规。
- 初始隔离418 passed/2 failed、首次集成419 passed/1 failed的历史均保留；最终全部测试通过。代码形状仍有HEAD既有local permits，未扩改。
- task-reader只完成文件/TOML校验，新会话宿主加载/执行未实测，合同禁止把未暴露角色当成可用。
- 使用现有技能软链接，无需复制安装；未变更全局配置、用户并发值或外部服务，不推送。
