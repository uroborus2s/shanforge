# 38 个 Skill 基线审计

## 方法与证据

- 动态发现：`skills/*/SKILL.md`，共 38 个唯一目录。
- 完整读取：逐项检查 frontmatter、触发/排除、专业工作流、状态与失败语义、资源路由和项目化边界。
- 自动基线：38/38 `quick_validate.py` 通过；完整 pytest `242 passed / 4 subtests passed`；Ruff 通过；94 个 Markdown 本地链接全部可达。
- 结论口径：这里只记录 implementer finding，不给独立分数；最终分数只能由 T06 reviewer 写入。

## 逐项结论

| Skill | 基线结论 | Finding / 保留理由 | T02-T04 动作 |
|---|---|---|---|
| agent-harness-construction | no_change_required | 触发、观察、恢复、输出和失败语义完整 | 保留 |
| ai-first-engineering | no_change_required | 团队工程规则边界明确，不替代实现/评审 owner | 保留 |
| ai-regression-testing | no_change_required | 根因、多路径一致性和风险验证完整 | 保留 |
| algorithmic-art | fix | `ALG-M1`：非项目状态只列 done/blocked，但正文存在必须用户选择的分支 | 补 `needs_user_input` |
| api-design | no_change_required | 契约决策、风险和测试追踪闭环 | 保留 |
| art-asset-pipeline | no_change_required | 候选跨会话、双确认和最终包边界已闭环 | 保留 |
| article-writing | no_change_required | 来源、语气、写作与事实边界清楚 | 保留 |
| brainstorming | no_change_required | 快速通道、项目化 brief 和批准边界清楚 | 保留 |
| browser-control | no_change_required | 工具路由、外部副作用确认和结果回读完整 | 保留 |
| crawler4j-model-project | fix | `CRAWLER-M1`：三份按需资料用裸路径，未进入可点击/可自动检查的 progressive-disclosure 链 | 改为 Markdown 链接 |
| doc-coauthoring | fix | `DOC-M1`：非项目状态缺 `needs_user_input`，与失败语义不一致 | 补状态枚举 |
| document-templates | no_change_required | 已登记项目优先与新项目回退边界明确 | 保留 |
| docx | fix | `DOCX-I1`：Skill 自带脚本按目标项目 `scripts/` 解析；`DOCX-M1`：正文 partial 未进入状态枚举 | 使用 `<skill-dir>`；补 partial |
| executing-plans | no_change_required | 授权包、STOP、批次质量和回写边界完整 | 保留 |
| frontend-patterns | no_change_required | 平台能力优先、风险分级和可访问性边界完整 | 保留 |
| gitcommitzh | fix | `GIT-I1`：触发边界把 `human_approved` 写成普遍前置，与“只在真实人工 Gate 才要求确认”冲突 | 收敛为真实 Gate + 已授权提交 |
| go-developer | no_change_required | 四件套触发严格，专业规则按 references 分层 | 保留 |
| humanizer | fix | `HUM-M1`：正文 partial 未进入项目状态枚举 | 补 partial |
| java-developer | no_change_required | 阶段、工作方式和 references 路由简洁 | 保留 |
| pdf | fix | `PDF-I1`：Skill 自带脚本按目标项目 `scripts/` 解析；`PDF-M1`：partial 未进入状态枚举 | 使用 `<skill-dir>`；补 partial |
| project-memory | no_change_required | 有界读取、事实优先级和 current-state 生命周期完整 | 保留 |
| python-uv-project | no_change_required | uv 工具链、迁移和 Bug owner 边界完整 | 保留 |
| receiving-code-review | no_change_required | feedback 核实、triage、整改和 memory 闭环完整 | 保留 |
| release-deployment | fix | `REL-M1`：专业发布回执未说明在项目化时如何承载 task 身份与 ledger/needs | 补共享合同承载说明 |
| requesting-code-review | no_change_required | 独立性、C/I/M、N/A 和真实人工 Gate 规则完整 | 保留 |
| requirements-engineering | no_change_required | 场景、analysis locator、baseline 影响和状态边界完整 | 保留 |
| shadcn | fix | `SHADCN-I1`：frontmatter 要求优先读取全部资料，正文却要求最小相关读取；`SHADCN-M1`：非项目状态缺 needs_user_input | 修触发描述；补状态 |
| stratix-admin-web | no_change_required | 触发足够严格，公共组件抽取门槛明确 | 保留 |
| stratix-service | fix | `STRATIX-I1`：32 个工作 Skill 中唯一未链接共享项目化回写合同 | 补共享合同链接 |
| subagent-driven-development | no_change_required | 独立写集、模型路由与批次汇总边界完整 | 保留 |
| systematic-debugging | no_change_required | 根因阶段、STOP 次数和 owner 交接完整 | 保留 |
| tdd-workflow | no_change_required | Red/Green、根因门和风险验证完整 | 保留 |
| ui-ux-pro-max | fix | `UI-I1`：自带搜索脚本硬编码 Shanforge 仓库相对路径，目标项目无法解析 | 使用 `<skill-dir>` |
| using-shanforge | no_change_required | 虽入口较长，但核心路由、Gate 和状态信封均为每次项目化动作所需；条件能力已通过 references 路由 | 保留 |
| verification-before-completion | no_change_required | 新鲜证据、完成层级和测试治理合同完整 | 保留 |
| webapp-testing | fix | `WEB-I1`：自带 server helper 按目标项目 `scripts/` 解析；`WEB-M1`：partial 与 `test_environment_contract` 未进入状态包 | 使用 `<skill-dir>`；补状态/needs |
| writing-plans | no_change_required | 任务粒度、模板、验证与批次质量门完整 | 保留 |
| xlsx | fix | `XLSX-I1`：自带脚本按目标项目 `scripts/` 解析；`XLSX-M1`：partial 未进入状态枚举 | 使用 `<skill-dir>`；补 partial |

## 分组统计

- `fix`：13。
- `no_change_required`：25。
- Critical：0。
- Important：8（脚本路径 5、Git Gate 1、shared contract 1、shadcn progressive disclosure 1）。
- Minor：10。

## T01 结论

`baseline_ready`。后续只修改上述 13 个 Skill 及直接对应测试；其余 25 项保留，并在最终 optimization results 中登记无修改证据。
