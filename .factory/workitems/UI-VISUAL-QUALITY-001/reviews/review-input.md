# 实现独立评审输入

- WorkItem: UI-VISUAL-QUALITY-001
- baseline: e39241a
- review_type: 集中代码、语义、测试充分性与中文语言评审
- inputs: brief.md、已批准 plan.md、三个 task brief、reports/implementation.md、evidence/verification.md、evidence/source-observations.md、git diff 和新增文件。
- architecture: skill-first、无仓内 src 运行时、标准库优先、只候选不写正式设计、项目已有组件/平台规范优先。
- current_state: ready_for_review；真实人工 Gate 为 none；approved 后 return_to_orchestrator，不自标任务 done。

审查全部 T01/T02 写集（具体文件列在两个 task brief）及当前 work item / .factory/memory 同步。身份与边界完整的 independent_subagent 不参与任何修改，只读取文件化输入；必要前向 CLI 查询可在临时目录执行，但不修改仓库/用户正式文件。

重点：三个输出形式信息等价，参数矩阵及 stack 平台冲突，零命中真实性，候选路径/碰撞/错误保护；入口是否真正引导产品特异性和参考学习；不同平台组件/交互是否保留；新建和局部任务是否被错误强制出多稿；素材和确认门是否自相矛盾；12 brief 是否足够固定输入且未伪装已完成美术验收。不要只查关键词，也不要以个人审美断言替代具体证据。

输出 reviewer_type/id/independence、按 rubric 五维评分、Critical/Important/Minor 的文件行证据、真实独立命令结果、approved 或 changes_requested。只读报告回给父控制器持久化；reviewer 不写文件、commit 或 push。
