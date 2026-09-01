# T02 Skill 设计专家评审

- reviewer_type: `independent_skill_design_reviewer`
- reviewer_id: `/root/skill_audit_design`
- reviewer_independence_evidence: 未参与候选实现；只读检查 `96e29da` 和指定输入，未修改文件、Git、ledger、memory 或外部系统。
- coverage: `38/38`
- perspective_score: `86/100`

| Skill | 分数 | C/I/M | 结论 |
|---|---:|:---:|---|
| agent-harness-construction | 87 | 0/0/1 | 边界和失败语义清楚，工具 schema 仍偏原则化。 |
| ai-first-engineering | 88 | 0/0/1 | 角色与根因纪律明确，缺少最小落地格式。 |
| ai-regression-testing | 91 | 0/0/1 | 回归路由清晰，状态枚举待统一。 |
| algorithmic-art | 86 | 0/0/1 | 版权与验证具体，自包含与联网 viewer 边界易误用。 |
| api-design | 91 | 0/0/1 | 风险和验证完整，现有契约事实源读取门可增强。 |
| art-asset-pipeline | 72 | 0/1/0 | 声明的 `remove_chroma_key.py` 不存在。 |
| article-writing | 90 | 0/0/1 | 事实边界完整，核查工具路由可再明确。 |
| brainstorming | 88 | 0/0/1 | 分流明确，落盘与记忆恢复职责略重叠。 |
| browser-control | 74 | 0/1/0 | 把未探测的 CLI/插件当作可执行能力。 |
| crawler4j-model-project | 86 | 0/0/1 | 协议清楚，版本探测失败路径偏弱。 |
| doc-coauthoring | 89 | 0/0/1 | 协作边界简洁，评审交接条件可更具体。 |
| document-templates | 84 | 0/0/1 | 渐进读取良好，外部模板依赖缺探测门。 |
| docx | 83 | 0/0/1 | 写入保护较好，依赖探测和最低交付路径不足。 |
| executing-plans | 84 | 0/0/1 | 授权和停止条件充分，与总控身份规则重复。 |
| frontend-patterns | 91 | 0/0/1 | 触发、平台优先和验证明确。 |
| gitcommitzh | 92 | 0/0/1 | 范围、Gate、Git 回读和远端边界清楚。 |
| go-developer | 89 | 0/0/1 | 工程约束充分，大仓全量测试缺风险例外。 |
| humanizer | 90 | 0/0/1 | 文字、安全写入和交付边界清楚。 |
| java-developer | 87 | 0/0/1 | 阶段和按需读取合理，最低验证 fallback 不足。 |
| pdf | 82 | 0/0/1 | 分支明确，工具依赖缺确定性回退。 |
| project-memory | 80 | 0/1/0 | 无活动 work item 的状态查询分支不闭合。 |
| python-uv-project | 84 | 0/0/1 | uv 规则明确，既存非 uv 项目的迁移界限偏紧。 |
| receiving-code-review | 82 | 0/1/0 | 默认同步动作与 route allowlist 前提不闭合。 |
| release-deployment | 90 | 0/0/1 | 发布、授权、回滚和脱敏边界清楚。 |
| requesting-code-review | 91 | 0/0/1 | 独立性与 Gate 清楚，整改 owner 略重叠。 |
| requirements-engineering | 87 | 0/0/1 | 输入输出明确，PRD 升级判据可更机械化。 |
| shadcn | 85 | 0/0/1 | 渐进披露合理，工具不可用退出语义不足。 |
| stratix-admin-web | 86 | 0/0/1 | 领域触发清楚，生成器不可用路径待统一。 |
| stratix-service | 86 | 0/0/1 | reference 路由明确，CLI/版本探测偏弱。 |
| subagent-driven-development | 85 | 0/0/1 | 派发和失败升级充分，与总控重复较多。 |
| systematic-debugging | 91 | 0/0/1 | 根因、证据和停止猜测边界明确。 |
| tdd-workflow | 90 | 0/0/1 | Red/Green 清楚，多路径判据应单点定义。 |
| ui-ux-pro-max | 86 | 0/0/1 | 平台路由细，外部搜索依赖失败合同不足。 |
| using-shanforge | 83 | 0/1/0 | 577 行入口职责过多并重复工作 Skill 字段。 |
| verification-before-completion | 92 | 0/0/1 | 新鲜验证、退出码和 partial 语义完整。 |
| webapp-testing | 85 | 0/0/1 | 应用边界清楚，Playwright 能力探测不统一。 |
| writing-plans | 77 | 0/1/0 | 临时 ID 分支绕过已有身份路由合同。 |
| xlsx | 84 | 0/0/1 | 写入和验证明确，依赖与公式重算能力探测不足。 |

## Important Findings

1. `skills/art-asset-pipeline/SKILL.md:32-33,49-50,104-109,118`：硬引用不存在的 `remove_chroma_key.py`，透明背景生产路径不可执行；补齐受测工具或删除硬依赖并明确 `blocked`。
2. `skills/browser-control/SKILL.md:28-31,38-41,77-88,117-135`：缺少能力探测、确定性工具优先级和全部不可用时的失败关闭。
3. `skills/writing-plans/SKILL.md:13-17,89-92`：写入要求已有 WorkItem/TaskCard，同时允许生成临时 ID，授权合同自相矛盾；应删除临时 ID 分支。
4. `skills/receiving-code-review/SKILL.md:12-18,45-50,89-98`：无条件同步 ledger/memory 与精确 allowlist 前提冲突；未授权路径应交总控同步。
5. `skills/project-memory/SKILL.md:12-17,65-77`：纯 `SB-STATUS` 且无活动 work item 时没有明确跳过 ledger/写入分支。

## Minor Findings

1. `skills/algorithmic-art/SKILL.md:26-29,34-40,58-63`：自包含交付与联网 p5.js viewer 的版本/离线可复现边界不清。
2. `skills/docx/SKILL.md:17-21`、`skills/pdf/SKILL.md:17-26`、`skills/xlsx/SKILL.md:14-19`：缺统一能力探测和 blocked fallback。
3. `skills/requesting-code-review/SKILL.md:68-79` 与 `skills/receiving-code-review/SKILL.md:36-50`：同范围整改是否生成 triage/response 的 owner 不一致。
4. `skills/using-shanforge/SKILL.md:443-498` 与 `skills/using-shanforge/references/work-skill-return-contract.md:9-37`：共享状态字段重复定义，容易漂移。

## 优先建议

1. 补齐或移除资源管线对不存在脚本的硬依赖。
2. 删除 `writing-plans` 绕过身份门的临时 ID 分支。
3. 给所有外部工具型 Skill 增加最小能力探测和统一 `blocked` fallback。
