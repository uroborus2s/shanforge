# T03 软件工程专家评审

- reviewer_type: `independent_subagent`
- reviewer_id: `/root/skill_audit_engineering`
- reviewer_independence_evidence: 未参与候选实现；只读检查审计输入、38 个 Skill、直接支撑材料和可运行脚本。
- coverage: `38/38`
- perspective_score: `81/100`

| Skill | 分数 | C/I/M | 结论 |
|---|---:|:---:|---|
| agent-harness-construction | 78 | 0/1/0 | 缺可执行 schema、失败样本或 eval fixture。 |
| ai-first-engineering | 83 | 0/0/1 | 缺可运行的团队规则验证。 |
| ai-regression-testing | 86 | 0/0/1 | 缺可复用断言和样例。 |
| algorithmic-art | 82 | 0/0/1 | 未验证模板实际可运行。 |
| api-design | 87 | 0/0/1 | 缺机器可校验的契约模板。 |
| art-asset-pipeline | 76 | 0/1/0 | manifest 与溯源缺 schema/验证器。 |
| article-writing | 85 | 0/0/1 | 工程自动化不适用。 |
| brainstorming | 76 | 0/1/0 | 与总控重叠且无路由测试。 |
| browser-control | 83 | 0/0/1 | CLI 可用性和命令合同未验证。 |
| crawler4j-model-project | 74 | 0/1/0 | 缺版本快照和兼容 smoke。 |
| doc-coauthoring | 88 | 0/0/1 | 输入、事实和输出边界清楚。 |
| document-templates | 79 | 0/1/0 | 外部 CLI 缺离线/失败路径验证。 |
| docx | 84 | 0/0/1 | 缺代表性 DOCX 端到端样本。 |
| executing-plans | 71 | 0/1/0 | 与身份创建和状态模型存在冲突。 |
| frontend-patterns | 87 | 0/0/1 | 最小实现、可访问性和验证合理。 |
| gitcommitzh | 86 | 0/0/1 | 范围、Gate 和 Git 回读明确。 |
| go-developer | 85 | 0/0/1 | 依赖详细 reference 的正确性。 |
| humanizer | 90 | 0/0/1 | 事实保真和安全写入边界清楚。 |
| java-developer | 78 | 0/1/0 | 关键工程/安全规则下沉到未验证 reference。 |
| pdf | 86 | 0/0/1 | 写入保护、结构和视觉验证较完整。 |
| project-memory | 80 | 0/1/0 | 复杂读取/压缩不变量缺回归测试。 |
| python-uv-project | 82 | 0/0/1 | 工具链和根因修复规则清楚。 |
| receiving-code-review | 78 | 0/1/0 | route 契约依赖上游且缺集成测试。 |
| release-deployment | 84 | 0/0/1 | 候选、授权、回滚和脱敏要求合理。 |
| requesting-code-review | 82 | 0/0/1 | 缺防止 reviewer 结论错误升级的自动化测试。 |
| requirements-engineering | 79 | 0/1/0 | 受身份创建路由矛盾影响。 |
| shadcn | 82 | 0/0/1 | 现有 eval 未证明全流程。 |
| stratix-admin-web | 84 | 0/0/1 | 依赖真实 CLI/项目验证。 |
| stratix-service | 72 | 0/1/0 | 固定版本和命令合同缺兼容验证。 |
| subagent-driven-development | 68 | 0/1/0 | worker 与控制器状态枚举未映射。 |
| systematic-debugging | 88 | 0/0/1 | 根因、归因和高风险 Gate 较强。 |
| tdd-workflow | 79 | 0/1/0 | 代码形状禁令缺自动校验。 |
| ui-ux-pro-max | 80 | 0/1/0 | 质量声明依赖人工执行，缺交付物校验。 |
| using-shanforge | 70 | 0/1/0 | 身份合同复杂且缺核心黑盒回归证据。 |
| verification-before-completion | 75 | 0/1/0 | 低中风险 evidence 持久化规则冲突。 |
| webapp-testing | 85 | 0/0/1 | 环境和副作用控制良好。 |
| writing-plans | 68 | 0/1/0 | 临时 ID 路径违反身份前置条件。 |
| xlsx | 84 | 0/0/1 | 非覆盖写入和 readback 验证清楚。 |

## 审计输入复核

- 原输入将快照写成 `Candidate`，被理解为 commit-diff review；主流程已改为完整工作树 `HEAD=96e29da` 的现状审计。原 reviewer 复核后关闭该项，Critical 调整为 `0`，本视角总分由 `79` 调整为 `81`。

## Important Findings

1. `skills/writing-plans/SKILL.md:14,90` 与 `skills/using-shanforge/SKILL.md:38`：已有身份前置条件与临时 ID 分支矛盾，可能产生孤立计划；删除临时 ID，统一交总控创建正式身份。
2. `skills/subagent-driven-development/SKILL.md:95,108,191`：完成状态与 worker 返回枚举没有映射；增加唯一映射表并明确只有控制器可写 `ready_for_review`。
3. `skills/verification-before-completion/SKILL.md:36` 与 `references/completion-claim-checklist.md:14`：低中风险状态包是否等价于落盘 evidence 的规则冲突。
4. `skills/using-shanforge/SKILL.md:356`：核心流程缺少覆盖身份、派发、review、verification、commit gate 的可执行黑盒回归。
5. `skills/crawler4j-model-project/SKILL.md:10` 与 `skills/stratix-service/SKILL.md:21`：精确版本/CLI 事实缺可复验来源和兼容 smoke。

## Minor Findings

1. `skills/art-asset-pipeline/SKILL.md:88`：资源 manifest 完整性依赖人工检查，缺最小 schema validator。
2. `skills/tdd-workflow/SKILL.md:53`：`code_shape_check` 缺机械判定口径，只能作者自报。
3. `skills/docx/SKILL.md:63` 与 `skills/xlsx/SKILL.md:59`：脚本语法检查不能证明真实 round-trip。

## 优先建议

1. 统一身份创建、worker 状态映射和 verification evidence 合同。
2. 为核心治理流程增加最小黑盒 fixture/runner。
3. 为固定外部生态版本提供探测和兼容 smoke。
