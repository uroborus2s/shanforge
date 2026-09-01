# T05 沟通专家评审

- reviewer_type: `independent_subagent`
- reviewer_id: `/root/skill_audit_communication`
- reviewer_independence_evidence: 未参与候选实现；只读检查任务输入、38 个 Skill、共享会话状态合同和相关测试。
- coverage: `38/38`
- perspective_score: `90/100`

| Skill | 分数 | C/I/M | 结论 |
|---|---:|:---:|---|
| agent-harness-construction | 82 | 0/1/0 | next_actions 与唯一下一动作边界未澄清。 |
| ai-first-engineering | 86 | 0/1/0 | 状态模板未显式呈现共享人类事实。 |
| ai-regression-testing | 91 | 0/0/1 | 项目化交接依赖共享合同理解。 |
| algorithmic-art | 94 | 0/0/1 | 交付、未验证原因和选择清楚。 |
| api-design | 92 | 0/0/1 | 契约、风险和测试建议明确。 |
| art-asset-pipeline | 94 | 0/0/1 | 确认点、产物状态和未完成原因清楚。 |
| article-writing | 86 | 0/0/1 | 核验阻塞与继续草稿边界略紧。 |
| brainstorming | 83 | 0/1/0 | 逐章节确认易制造额外停顿。 |
| browser-control | 93 | 0/0/1 | 执行事实、副作用和介入点明确。 |
| crawler4j-model-project | 88 | 0/0/1 | 面向用户的阶段/影响摘要不足。 |
| doc-coauthoring | 94 | 0/0/1 | 目标读者、缺口、验证和最小输入清楚。 |
| document-templates | 92 | 0/0/1 | 文档状态和未生成原因可追溯。 |
| docx | 94 | 0/0/1 | partial 和验证失败不会误报为完成。 |
| executing-plans | 84 | 0/1/0 | 本地模板未直观承接进度和未完成事实。 |
| frontend-patterns | 93 | 0/0/1 | 用户行为、风险和验证范围清楚。 |
| gitcommitzh | 95 | 0/0/1 | 草案、阻塞、提交和远端事实区分准确。 |
| go-developer | 83 | 0/1/0 | 默认全量测试与全局风险定向验证冲突。 |
| humanizer | 78 | 0/1/0 | 可能删除总控强制的三段式状态外壳。 |
| java-developer | 89 | 0/0/1 | 阶段、根因、验证和阻塞明确。 |
| pdf | 94 | 0/0/1 | partial、OCR 风险和验证条件清楚。 |
| project-memory | 91 | 0/0/1 | 恢复准确，输出仍偏内部状态卡。 |
| python-uv-project | 85 | 0/1/0 | 无条件全量检查未按风险收敛。 |
| receiving-code-review | 90 | 0/0/1 | triage、整改和 reviewer 边界明确。 |
| release-deployment | 88 | 0/1/0 | 只返回回执与共享人类摘要存在歧义。 |
| requesting-code-review | 93 | 0/0/1 | 独立性、结论和人工 Gate 清楚。 |
| requirements-engineering | 92 | 0/0/1 | 草稿、评审、批准和影响不会混淆。 |
| shadcn | 93 | 0/0/1 | 覆盖风险、验证和选择边界明确。 |
| stratix-admin-web | 90 | 0/0/1 | 信息完整但输出面较宽。 |
| stratix-service | 89 | 0/0/1 | 用户摘要依赖共享合同。 |
| subagent-driven-development | 85 | 0/1/0 | 子流程人类事实未在模板中显性化。 |
| systematic-debugging | 95 | 0/0/1 | 根因、owner、修复位置和回归完整。 |
| tdd-workflow | 96 | 0/0/1 | Red/Green、覆盖和修复位置表达完整。 |
| ui-ux-pro-max | 90 | 0/0/1 | 状态和风险明确但篇幅较重。 |
| using-shanforge | 91 | 0/0/1 | 三段式、层级和唯一下一动作完整。 |
| verification-before-completion | 96 | 0/0/1 | 新鲜证据、七态和完成层级清楚。 |
| webapp-testing | 93 | 0/0/1 | 断言、环境、partial 和副作用清楚。 |
| writing-plans | 93 | 0/0/1 | 计划适用性和任务粒度清楚。 |
| xlsx | 94 | 0/0/1 | 输出、部分处理和验证失败表达准确。 |

## Important Findings

1. `skills/humanizer/SKILL.md:24-30,38` 可能删除 `skills/using-shanforge/SKILL.md:260-266` 强制的三段式响应外壳；应增加 Shanforge 状态回复保护例外。
2. `skills/using-shanforge/references/work-skill-return-contract.md:7-25` 要求人类事实字段，但 32 个工作 Skill 的局部“只回写”模板没有显式指向这些补充字段；应增加统一短注释，不复制整份合同。
3. `skills/brainstorming/SKILL.md:77-85` 要求逐章节/选择确认，与 `skills/using-shanforge/SKILL.md:272-278` 只在真实 Gate 停止冲突；应合并为一次实质决策确认。
4. `skills/go-developer/SKILL.md:60`、`skills/python-uv-project/SKILL.md:86-97` 的默认全量验证与 `skills/using-shanforge/SKILL.md:117-126` 的风险定向策略冲突。
5. `tests/test_remaining_skill_project_status_contract.py:79-90` 与 `tests/test_skill_progress_visibility_and_continuation.py:12-60` 主要检查关键词，不能证明最终响应保留进度、测试、根因、修复位置和唯一下一动作。

## Minor Findings

1. `skills/agent-harness-construction/SKILL.md:45-49` 的复数 `next_actions` 应明确为内部候选，用户只看到总控归并的唯一下一动作。
2. `skills/release-deployment/SKILL.md:39,66-68` 的“只返回回执”应补充阻塞缺口和共享状态事实。
3. `tests/test_work_skill_status_envelope_ownership.py:59-99` 未覆盖非测试、测试、Bug、发布四类结果如何填充共享字段。

## 优先建议

1. 固化“局部结果模板 + 共享人类事实字段”的单一可执行写法并增加行为回归。
2. 保护三段式状态外壳，并只为真正改变范围/验收的决策设置确认。
3. 对齐 Go/Python 与全局风险分级验证策略。
