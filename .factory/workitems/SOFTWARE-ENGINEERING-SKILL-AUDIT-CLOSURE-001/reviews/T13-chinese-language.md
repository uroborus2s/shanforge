# 中文维度复评

| Skill | before | after | delta | reason/evidence |
|---|---:|---:|---:|---|
| agent-harness-construction | 88 | 95 | +7 | `next_actions` 明确为内部候选、用户仅见唯一下一动作；T11 合同测试。 |
| ai-first-engineering | 93 | 94 | +1 | 中文规则完整；T13 记录 38/38 Skill validator 通过。 |
| ai-regression-testing | 93 | 94 | +1 | 多路径、根因和风险分级表述清晰；无新增中文歧义。 |
| algorithmic-art | 92 | 94 | +2 | `SKILL.md:27` 明确默认联网与离线内联/随包边界。 |
| api-design | 91 | 94 | +3 | 术语均落在中文契约决策表和风险规则中，含义可判断。 |
| art-asset-pipeline | 89 | 95 | +6 | 清理职责收敛至收尾规则；`SKILL.md:31,61,66` 前后条件一致。 |
| article-writing | 89 | 95 | +6 | `SKILL.md:14,36` 限定用户提供或明确授权样本，禁止擅自模仿。 |
| brainstorming | 81 | 93 | +12 | 用户确认只针对目标、范围、验收或不可逆取舍；仍保留必要流程术语。 |
| browser-control | 87 | 95 | +8 | `SKILL.md:76` 逐一解释 DOM、state、accessibility snapshot 的选择条件。 |
| crawler4j-model-project | 86 | 93 | +7 | 专有协议词密集但有“模块项目”定义、版本门和明确失败回执。 |
| doc-coauthoring | 93 | 94 | +1 | 中文主导，状态字段仅作机器可读枚举。 |
| document-templates | 87 | 93 | +6 | owner 映射、回源、登记布局均已在上下文中解释。 |
| docx | 89 | 94 | +5 | 按任务分支组织，工具、条件与失败语义不再混淆。 |
| executing-plans | 82 | 95 | +13 | `SKILL.md:44` 已统一为“验收标准”，T12 与执行流程测试覆盖。 |
| frontend-patterns | 88 | 95 | +7 | `SKILL.md:28` 改为“多个兄弟或下游组件共享”，消除“远端组件”歧义。 |
| gitcommitzh | 90 | 94 | +4 | 必要 Git 术语保留，中文前置检查和输出语义明确。 |
| go-developer | 87 | 93 | +6 | 专名较多但触发边界、验证范围和禁令均可直接理解。 |
| humanizer | 95 | 95 | 0 | 三段式状态事实保护规则清楚；无当前中文 Finding。 |
| java-developer | 93 | 94 | +1 | 阶段、工作方式和输出边界简洁明确。 |
| pdf | 90 | 94 | +4 | 工具名保留合理，分支和安全写入规则清楚。 |
| project-memory | 83 | 95 | +12 | `SKILL.md:16,62` 首次释义“读取回执（receipt）”，并明确其非事实写入性质。 |
| python-uv-project | 88 | 93 | +5 | 风险范围与项目例外已有明确说明，仍有必要技术术语。 |
| receiving-code-review | 86 | 95 | +9 | `SKILL.md:64` 改为“基于技术证据提出异议（pushback）”。 |
| release-deployment | 93 | 94 | +1 | 发布回执字段简洁、中文停止规则明确。 |
| requesting-code-review | 85 | 93 | +8 | 术语密度仍高，但 review、人工确认和同范围整改的语义已区分。 |
| requirements-engineering | 86 | 93 | +7 | baseline、owner 等词均位于中文流程与定义语境中。 |
| shadcn | 88 | 94 | +6 | 首次场景已给 registry、preset、diff 的实际任务语境。 |
| stratix-admin-web | 85 | 95 | +10 | `SKILL.md:41,65-66` 明确检查动作、比较内容及页面/组件清单产物。 |
| stratix-service | 86 | 93 | +7 | 分层、总装和版本门有明确中文规则；专名不可避免。 |
| subagent-driven-development | 78 | 95 | +17 | `SKILL.md:57-61` 只引用总控唯一派发定义；`83` 使用“验收标准”。 |
| systematic-debugging | 92 | 94 | +2 | 复现、根因、事实 owner 和交接状态表述清楚。 |
| tdd-workflow | 87 | 94 | +7 | 代码形状禁令已纳入 Red/Green 顺序，术语边界清楚。 |
| ui-ux-pro-max | 83 | 95 | +12 | `SKILL.md:8,77` 明确为“设计知识检索命中/未命中”，不再指向业务数据库。 |
| using-shanforge | 73 | 95 | +22 | `SKILL.md:98` 使用“验收标准”；`192` 按身份、控制/复杂度、风险/范围、派发、Gate/升级分组。 |
| verification-before-completion | 81 | 95 | +14 | `SKILL.md:59,67` 限定局部替代条件、同一声明覆盖、退出码、未覆盖范围和残余风险。 |
| webapp-testing | 88 | 95 | +7 | `SKILL.md:13,84` 只返回浏览器能力候选，由总控路由，不再自行“转交”。 |
| writing-plans | 82 | 95 | +13 | `SKILL.md:36` 已改为“需求和验收标准明确”，无前置结果误读。 |
| xlsx | 91 | 94 | +3 | 写入安全、重读验证与 partial 语义清楚。 |

## 原始 T01 Finding 决策（13/13）

| ID | 严重度 | decision | 精确证据/位置 | 理由 |
|---|---|---|---|---|
| ZH-I01 | Important | verified_fixed | `using-shanforge:98`；`writing-plans:36`；`executing-plans:44`；`subagent-driven-development:83` | 四处前置输入均为“验收标准”，不再把尚未发生的验证写成结果；T12 及 `test_execution_workflow_skills.py` 覆盖。 |
| ZH-I02 | Important | verified_fixed | `subagent-driven-development:57-61` | 子 Skill 仅引用总控“子代理严格派发判定”，重复公式已删除。 |
| ZH-I03 | Important | verified_fixed | `using-shanforge:190-215`，尤其 `192` | 路由字段按任务身份、控制/复杂度、风险/范围、派发、Gate/升级分组，且明确机器字段不改名。 |
| ZH-I04 | Important | verified_fixed | `ui-ux-pro-max:8,77` | 已写为“设计知识检索命中或未命中”，明确只是候选输入。 |
| ZH-I05 | Important | verified_fixed | `frontend-patterns:28` | 已写为“多个兄弟或下游组件共享”，不再暗示远程组件。 |
| ZH-I06 | Important | verified_fixed | `verification-before-completion:59,67,83` | 局部替代仅限列明情形，必须记录未运行完整命令、原因、替代命令和退出码、未覆盖范围、残余风险。 |
| ZH-I07 | Important | verified_fixed | `stratix-admin-web:41,65-66` | 明确查既有文件、记录可复用模式与差异，并产出页面和组件清单。 |
| ZH-M01 | Minor | verified_fixed | `receiving-code-review:64` | 首次写明“基于技术证据提出异议（pushback）”。 |
| ZH-M02 | Minor | verified_fixed | `browser-control:76` | DOM、state、accessibility snapshot 的验证对象和选择场景均有中文说明。 |
| ZH-M03 | Minor | verified_fixed | `article-writing:14,36` | 只允许用户提供或明确授权的样本，禁止自行抓取、推断或模仿未授权个人。 |
| ZH-M04 | Minor | verified_fixed | `art-asset-pipeline:31,61,66` | 未选候选图与 `tmp/` 的清理归于单一收尾规则；流程和通过标准不再重复同一 owner。 |
| ZH-M05 | Minor | verified_fixed | `project-memory:16,62` | 首次释义为“读取回执（receipt）”，并说明其作用和边界。 |
| ZH-M06 | Minor | verified_fixed | `webapp-testing:13,84` | 工作 Skill 仅给候选和能力边界，明确由 `using-shanforge` 总控路由。 |

## 新发现

- Critical：0
- Important：0
- Minor：0

## 汇总

- coverage：`38/38`
- 平均 before：`87.3`
- 平均 after：`94.2`
- 平均 delta：`+6.9`
- remaining C/I/M：`0/0/0`
- 验证依据：T10、T11、T12、T13 集中验证证据；T13 为 `346 passed, 4 subtests passed`、38/38 validator、Ruff 与 `git diff --check` 通过。
- gate_decision：`approved`

下一步：将本中文维度的 13 项结论计入总闭环；本维度无需再改文案。
