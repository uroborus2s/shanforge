# T04 软件项目管理专家评审

- reviewer_type: `independent_subagent`
- reviewer_id: `/root/skill_audit_pm`
- reviewer_independence_evidence: 未参与快照实现；只读审计 `HEAD=96e29da` 的 38 个 Skill、直接合同、模板、脚本和静态测试。
- coverage: `38/38`
- perspective_score: `81/100`

| Skill | 分数 | C/I/M | 结论 |
|---|---:|:---:|---|
| agent-harness-construction | 83 | 0/0/1 | 输出、失败和验证清楚，不产出项目追踪事实。 |
| ai-first-engineering | 82 | 0/0/1 | 项目化结果依赖共享状态合同。 |
| ai-regression-testing | 86 | 0/0/1 | 根因、多路径和证据链完整。 |
| algorithmic-art | 82 | 0/0/1 | 项目级追踪由共享合同承接。 |
| api-design | 88 | 0/0/1 | 风险分级和 TEST-API 追踪明确。 |
| art-asset-pipeline | 84 | 0/0/1 | 确认、候选和资源清单状态明确。 |
| article-writing | 79 | 0/0/1 | 项目追踪仅由共享合同提供。 |
| brainstorming | 85 | 0/0/1 | brief、批准点、ledger 和跨会话边界明确。 |
| browser-control | 84 | 0/0/1 | 外部动作确认、证据和阻塞语义明确。 |
| crawler4j-model-project | 88 | 0/0/1 | 版本、发布 Gate 和验证顺序充分。 |
| doc-coauthoring | 83 | 0/0/1 | 事实来源、验证和待决项明确。 |
| document-templates | 90 | 0/0/1 | doc-map、版本和正式事实源完整。 |
| docx | 83 | 0/0/1 | 输出、验证、partial/blocked 清楚。 |
| executing-plans | 80 | 0/1/0 | 缺失 WBS/TaskCard 映射。 |
| frontend-patterns | 82 | 0/0/1 | 决策和状态包边界清楚。 |
| gitcommitzh | 87 | 0/0/1 | 提交前 Gate 和范围明确。 |
| go-developer | 84 | 0/0/1 | 阶段、验证和工程 Gate 完整。 |
| humanizer | 79 | 0/0/1 | 轻量边界清晰，追踪依赖共享合同。 |
| java-developer | 82 | 0/0/1 | 阶段、最小变更和验证明确。 |
| pdf | 83 | 0/0/1 | 不可逆动作控制明确。 |
| project-memory | 75 | 0/1/0 | 模板未固化任务身份、Gate 和下一动作。 |
| python-uv-project | 83 | 0/0/1 | 质量门和失败语义明确。 |
| receiving-code-review | 85 | 0/0/1 | triage、整改边界和验证明确。 |
| release-deployment | 90 | 0/0/1 | 候选、授权、健康检查、回滚和回执完整。 |
| requesting-code-review | 89 | 0/0/1 | 独立性、严重度和人工 Gate 清楚。 |
| requirements-engineering | 86 | 0/0/1 | REQ/NFR、基线、验收和版本充分。 |
| shadcn | 82 | 0/0/1 | 组件工作流和验证边界明确。 |
| stratix-admin-web | 84 | 0/0/1 | 页面、权限、验证和状态回写明确。 |
| stratix-service | 85 | 0/0/1 | 框架事实、验证矩阵和发布门明确。 |
| subagent-driven-development | 79 | 0/1/0 | 缺可消费的 WBS—TaskCard 映射。 |
| systematic-debugging | 88 | 0/0/1 | 根因、风险、owner 和 Bug TaskCard 决策充分。 |
| tdd-workflow | 87 | 0/0/1 | Red/Green、风险 Gate 和验证事实充分。 |
| ui-ux-pro-max | 85 | 0/0/1 | 设计证据、状态矩阵和验收充分。 |
| using-shanforge | 76 | 0/1/0 | PM 快照数据合同未被计划模板供给。 |
| verification-before-completion | 89 | 0/0/1 | 七态统计和关闭 Gate 完整。 |
| webapp-testing | 87 | 0/0/1 | TEST-UI、环境和证据明确。 |
| writing-plans | 74 | 0/1/0 | 模板不能满足 WBS、身份和恢复合同。 |
| xlsx | 83 | 0/0/1 | 输入、输出和验证语义明确。 |

## Important Findings

1. `skills/writing-plans/references/workitem-plan-template.md:52` 没有生成 PM 快照要求的 `## Work Breakdown` 四列表；`skills/using-shanforge/references/pm-dashboard-rendering.md:57` 和 `scripts/project_snapshot.py:265` 却只消费该格式。应在计划模板强制生成 `id | parent_id | title | status` 并关联 TaskCard。
2. `skills/writing-plans/references/task-brief-template.md:5,88` 与 `skills/project-memory/references/memory-ledger-event-template.md:35` 未把 `task_card_id`、`wbs_id`、`current_gate`、完成层级和下一动作设为稳定字段，与 `skills/using-shanforge/SKILL.md:38` 的身份硬门冲突。
3. `skills/writing-plans/references/task-brief-template.md:7` 把 `approved` 当 TaskCard 状态；`project_snapshot.py:131,192,309` 对它的待办/完成分类不一致，review 的 approved 也可能被误投影为产品完成。应拆分 `review_status` 与生命周期状态。
4. `skills/writing-plans/references/plan-review-template.md:14` 没有审 WBS 映射、依赖 DAG、状态词表和恢复字段，不能实现 `writing-plans/SKILL.md:134` 声称的拒绝缺层级计划。
5. `tests/test_writing_plans_skill.py:74` 仅做关键词检查；`tests/test_using_shanforge_snapshot.py:16` 手工构造理想 WBS，没有覆盖“计划模板→TaskCard/ledger→PM 快照”的真实链路。

## Minor Findings

1. `skills/project-memory/references/session-card-template.md:6` 缺 `task_card_id`、当前 Gate、停止原因和唯一下一动作。
2. `skills/writing-plans/references/workitem-plan-template.md:149` 的 Gate 列表缺 owner、进入条件、证据路径和 Gate ID。

## 优先建议

1. 补齐并强制 Work Breakdown 与 TaskCard/WBS 映射。
2. 统一 TaskCard/ledger 身份、Gate 和生命周期字段，拆分 review approved 与完成语义。
3. 新增“计划—任务—ledger—快照—恢复”端到端 PM 投影测试。
