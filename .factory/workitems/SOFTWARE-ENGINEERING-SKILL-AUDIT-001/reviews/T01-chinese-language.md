# T01 中文语言专家评审

- reviewer_type: `independent_readonly_language_reviewer`
- reviewer_id: `/root/skill_audit_chinese`
- reviewer_independence_evidence: 未参与这些 Skill 的实现；只读检查全部入口及必要 direct reference，未写文件、Git、ledger、memory 或外部系统。
- coverage: `38/38`
- perspective_score: `87.3/100`

| Skill | 分数 | C/I/M | 结论 |
|---|---:|:---:|---|
| agent-harness-construction | 88 | 0/0/1 | 中英混排和括号释义偏密。 |
| ai-first-engineering | 93 | 0/0/1 | 少量 must/should/optional 未中文化定义。 |
| ai-regression-testing | 93 | 0/0/1 | 少数“路径”在不同上下文语义较宽。 |
| algorithmic-art | 92 | 0/0/1 | 未区分环境缺失与交付阻塞。 |
| api-design | 91 | 0/0/1 | 英文技术术语缺统一中文呈现。 |
| art-asset-pipeline | 89 | 0/1/0 | 清理要求在多处重复。 |
| article-writing | 89 | 0/1/0 | 模仿个人语气的授权措辞不足。 |
| brainstorming | 81 | 0/1/0 | 流程和纪律重复、英文状态密集。 |
| browser-control | 87 | 0/1/0 | DOM/state/snapshot 等未统一解释。 |
| crawler4j-model-project | 86 | 0/1/0 | 长句叠加大量英文协议词。 |
| doc-coauthoring | 93 | 0/0/1 | 仅有少量英文状态字段。 |
| document-templates | 87 | 0/1/0 | 登记、回源、owner 映射缺短定义。 |
| docx | 89 | 0/1/0 | 单行叠加工具、命令、条件和例外。 |
| executing-plans | 82 | 0/1/0 | 前置“验收结果”容易与实际结果混淆。 |
| frontend-patterns | 88 | 0/1/0 | “远端组件共享”术语不自然且易误读。 |
| gitcommitzh | 90 | 0/0/1 | 必要 Git 术语合理，局部句子偏长。 |
| go-developer | 87 | 0/1/0 | 中英文专名密集，部分禁令句过长。 |
| humanizer | 95 | 0/0/1 | 中文自然且边界清楚。 |
| java-developer | 93 | 0/0/1 | 阶段、边界和输出简洁。 |
| pdf | 90 | 0/0/1 | 工具名保留合理。 |
| project-memory | 83 | 0/1/0 | 会话卡、summary、Gate、receipt 混用。 |
| python-uv-project | 88 | 0/1/0 | 强度层级与既有项目例外可更显式。 |
| receiving-code-review | 86 | 0/1/0 | pushback、triage、response 混排偏重。 |
| release-deployment | 93 | 0/0/1 | 回执字段明确，正文简洁。 |
| requesting-code-review | 85 | 0/1/0 | reviewer/review/Gate/loop 密集且重复。 |
| requirements-engineering | 86 | 0/1/0 | baseline、owner 等混排提高成本。 |
| shadcn | 88 | 0/1/0 | registry/preset/diff 可增加首次中文释义。 |
| stratix-admin-web | 85 | 0/1/0 | “先总结相似组件”不具体。 |
| stratix-service | 86 | 0/1/0 | 根级三层、总装等表达不直观。 |
| subagent-driven-development | 78 | 0/1/0 | 派发与状态规则高度重复和符号化。 |
| systematic-debugging | 92 | 0/0/1 | 阶段、证据和交接清楚。 |
| tdd-workflow | 87 | 0/1/0 | 代码形状禁令嵌入主步骤分散重点。 |
| ui-ux-pro-max | 83 | 0/1/0 | 入口密度高，“数据库命中”有歧义。 |
| using-shanforge | 73 | 0/1/0 | 协议、例外和路由表过度堆叠。 |
| verification-before-completion | 81 | 0/1/0 | 完整命令与局部替代的边界不清。 |
| webapp-testing | 88 | 0/1/0 | “转交”措辞与总控独占路由有张力。 |
| writing-plans | 82 | 0/1/0 | 前置“验收结果”易被误读为测试事实。 |
| xlsx | 91 | 0/0/1 | 写入安全和验证步骤简洁。 |

## Important Findings

1. `skills/using-shanforge/SKILL.md:98`、`skills/writing-plans/SKILL.md:35`、`skills/executing-plans/SKILL.md:44`、`skills/subagent-driven-development/SKILL.md:91`：开始前使用“验收结果”会被误读为已经测试通过；应统一改为“验收标准（及必要验证命令）”。
2. `skills/subagent-driven-development/SKILL.md:57,65`：worker 派发公式重复；保留一处规范公式，另一处引用并补中文释义。
3. `skills/using-shanforge/SKILL.md:190`：大量英文协议字段无中文分组；应按身份、风险、派发、升级四组解释。
4. `skills/ui-ux-pro-max/SKILL.md:8`：“数据库命中”易被理解为业务数据库；改为“设计检索数据库的候选结果”。
5. `skills/frontend-patterns/SKILL.md:28`：“多个远端组件共享”易被理解为远程组件；改为“多个相距较远的组件共享状态”。
6. `skills/verification-before-completion/SKILL.md:46,57`：完整验证和局部替代的允许条件不明确。
7. `skills/stratix-admin-web/SKILL.md:35`：“先总结相似组件”缺明确动作和产物。

## Minor Findings

1. `skills/receiving-code-review/SKILL.md:63`：`pushback` 应写为“以技术理由提出异议（push back）”。
2. `skills/browser-control/SKILL.md:72`：DOM、页面状态和无障碍快照应给中文选择说明。
3. `skills/article-writing/SKILL.md:14`：个人语气模仿应限定用户提供或确认可使用的样本。
4. `skills/art-asset-pipeline/SKILL.md:31,69,143`：临时资源清理要求重复。
5. `skills/project-memory/SKILL.md:61`：首次出现 `receipt` 时应解释为读取回执。
6. `skills/webapp-testing/SKILL.md:83`：“转交”应改为“在结果中说明由流程总控处理”。

## 优先建议

1. 全仓区分前置“验收标准”和后置“验收结果”。
2. 精简总控与子代理执行 Skill 的重复派发规则，并为高频协议词加首次中文释义。
3. 修复会改变专业理解的具体措辞，而不是做无差别润色。
