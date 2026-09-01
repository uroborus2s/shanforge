# 软件工程 Skill 五专家综合审计

## 结论

仓内 38 个 Skill 的触发边界、安全意识、根因纪律和会话状态表达总体可用，系统矩阵得分 `85.6/100`。主要问题不是单个 Skill 完全不可用，而是总控、计划、TaskCard、ledger、子代理、验证和用户回复之间的共享合同存在重复、冲突或只靠文字自报。当前没有 Critical；存在 Important 缺陷，结论为 `changes_recommended`，本报告不代表整改已完成。

## 第一优先级：先修跨 Skill 合同闭环

1. **计划身份规则自相矛盾。** `skills/writing-plans/SKILL.md:14,90` 一边要求写入前已有 WorkItem/TaskCard，一边允许生成临时 ID；与 `skills/using-shanforge/SKILL.md:38` 的身份创建门冲突。删除临时 ID，统一由总控登记正式身份。
2. **WBS、TaskCard、ledger 和快照没有闭合。** `skills/writing-plans/references/workitem-plan-template.md:52` 不生成快照要求的四列 WBS；task brief 和 ledger 模板也缺稳定 `task_card_id/wbs_id/current_gate`。补齐单一数据合同和映射。
3. **状态词跨层复用。** `approved` 同时出现在 review、TaskCard 和 WBS 投影中；`subagent-driven-development` 又存在两套 worker/控制器状态枚举。拆分 `review_status`、生命周期状态和 worker receipt，并提供唯一映射表。
4. **验证证据合同冲突。** `verification-before-completion` 主文允许低中风险只返回状态包，checklist 又要求 evidence 落盘；“完整命令”与局部替代条件也不够明确。统一什么是完成声明的最小持久化证据。
5. **缺少跨 Skill 行为回归。** 现有测试大量固定关键词，未覆盖“计划→任务→ledger→快照→恢复”和“工作结果→三段式用户回复”。新增最小参数化集成测试，不新增测试框架。

## 第二优先级：消除实际不可执行和工具假设

1. `skills/art-asset-pipeline/SKILL.md:32-33,49-50,104-109,118` 硬引用不存在的 `remove_chroma_key.py`。补齐受测工具，或删除硬依赖并明确失败关闭。
2. `browser-control`、Office/PDF/XLSX、UI 搜索、Stratix、Crawler4j 等外部工具型 Skill 缺统一“能力探测→选择→全部不可用时 blocked”合同。
3. `crawler4j-model-project` 与 `stratix-service` 固化精确外部版本/CLI，但缺版本证据和兼容 smoke。
4. DOCX/XLSX 脚本只有语法级检查，缺最小 round-trip 样本；资源 manifest 和代码形状检查也主要依赖人工自报。

## 第三优先级：让响应合同真正可消费

1. `skills/humanizer/SKILL.md:24-30,38` 可能删除总控强制的三段式状态外壳。增加 Shanforge 状态回复保护例外。
2. 32 个工作 Skill 的局部“只回写”模板未明确补齐共享 `human_summary/progress/verification/defect/change` 字段。保留共享合同为单一事实源，各模板只加一行强引用。
3. `brainstorming` 的逐章节确认与总控“只有真实人工 Gate 才停止”冲突。只合并确认会改变目标、范围、验收或不可逆取舍的决策。
4. Go/Python 默认全量验证与总控风险分级的定向验证策略冲突。默认定向，批次、发布、高风险或项目 Gate 才全量，并明确未运行范围。
5. 全仓统一前置“验收标准”和后置“验收结果”；为 reviewer、Gate、owner、receipt 等高频协议词增加首次中文释义。

## 局部但应修的问题

- `receiving-code-review` 无条件同步 memory/ledger 与精确 allowlist 前提冲突；未授权路径交总控同步。
- `project-memory` 缺无活动 WorkItem 的纯 `SB-STATUS/no_project_write` 明确分支。
- `requesting-code-review` 和 `receiving-code-review` 对同范围整改是否生成 triage/response 的 owner 不一致。
- `ui-ux-pro-max` 的“数据库命中”、`frontend-patterns` 的“远端组件”、`stratix-admin-web` 的“总结相似组件”存在会改变专业理解的歧义。
- `using-shanforge` 主入口 577 行，承担过多运行时细节和重复字段；应保留路由决策，逐步下沉机器合同到单一 reference，不新增新的总控层。

## 建议整改批次

### 批次 A：合同一致性

- 文件范围：`writing-plans`、`using-shanforge`、`project-memory`、`subagent-driven-development`、`verification-before-completion` 及直接模板/测试。
- 完成标准：身份、WBS、状态、evidence 四条链路各有单一合同和行为测试。

### 批次 B：会话可读性

- 文件范围：`humanizer`、`brainstorming`、共享回写合同、代表性工作 Skill、Go/Python 验证规则。
- 完成标准：三段式不被破坏；局部结果可生成完整进度/测试/Bug/下一动作；确认点只对应真实 Gate。

### 批次 C：工具可执行性

- 文件范围：`art-asset-pipeline`、`browser-control`、Crawler4j、Stratix、DOCX/PDF/XLSX 及 smoke tests。
- 完成标准：工具先探测；缺能力明确 blocked；固定版本可复验；最小 round-trip/manifest 验证可运行。

三个批次应按 A→B→C 顺序推进。A 影响项目事实正确性，优先于文案优化和工具便利性。
