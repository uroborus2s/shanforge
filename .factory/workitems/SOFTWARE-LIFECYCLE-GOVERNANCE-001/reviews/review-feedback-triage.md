# Review Feedback Triage

## I1：候选批准与生效标记

- 来源：independent task review；severity：Important。
- 技术要求：在独立 Review 与正式批准前，不得把候选标为已批准并生效或署名用户批准。
- 技术核实：`partially_disputed`。用户的原始命令明确要求“统一正式设计事实源”并“做到干净克隆全绿”，plan 第 15、63 行已登记正式事实变更和本地提交授权；本 WorkItem 也明确无额外人工 Gate。工作区文件是拟提交 after-image，独立 Review 是质量 Gate，不是新增的产品/风险/外部动作人工批准 Gate。若把普通受控文档修改都改成精确哈希人工批准，将违反当前轻门禁与用户连续执行要求。
- 决定：`Pushback`；不伪造新批准证据，不新增人工 Gate。请同一 reviewer 依据用户原始授权、候选 after-image 语义和本 WorkItem 的 `human_confirmation_required=false` 复核。

## I2：测试计划与案例控制漂移

- 来源：independent task review；severity：Important。
- 技术要求：新增正式测试案例时同步版本、来源、日期、历史和总索引，并补回归保护。
- 技术核实：`yes`。两页正文已变更而文档控制仍指向 `TEST-GOVERNANCE-CLOSURE-001`，总索引仍登记旧版本。
- 决定：`Fix`；T01 更新测试文档与断言，T03 同步总索引。

## I3：生命周期矩阵测试可能关键词假绿

- 来源：independent task review；severity：Important。
- 技术要求：解析矩阵真实表头与数据行，验证阶段全集、列数、逐列非空及方法边界。
- 技术核实：`yes`。当前测试从标题读到文件末尾，只检查关键词存在。
- 决定：`Fix`；T01 用最小 Markdown 表解析替换关键词检查，不新增依赖。

## I4：current memory 含退役 runtime 任务

- 来源：independent task review；severity：Important。
- 技术要求：删除 `tasks.summary.md` 中仍以“进行中/下一顺位”表达的旧平台任务，历史只由日期快照、Git 和 WorkItem 回源，并补回归。
- 技术核实：`yes`。`## 进行中` 到 `## 下一顺位` 明确给不存在的 `src/domain`、`src/settings` 和 provider runtime 当前资格。
- 决定：`Fix`；Sol 删除该当前投影块，T01 增加 memory current-scope 防回退断言。

## Iteration 2：I3 语义反例

- 来源：同一 independent reviewer；severity：Important。
- 技术要求：矩阵测试不能只锁列、阶段和关键词，还须拒绝“关键词齐全但含义相反”的关键边界。
- 技术核实：`yes`。reviewer 已用内存反例证明当前函数接受“简单任务可跳过 TDD、旧输出可替代新鲜验证、发布无需授权”。
- 决定：`Fix`；原 T01 Terra owner 按具体列锁定正向/禁止语义并增加最小反例测试，不新增依赖。
