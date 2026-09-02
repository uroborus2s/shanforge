# 沟通维度复评

首轮覆盖：`38/38`。结论 `changes_requested`：`ZH-I01` 在正式计划模板中仍残留。

| Skill | before | after | delta | reason/evidence |
|---|---:|---:|---:|---|
| agent-harness-construction | 82 | 95 | +13 | `next_actions` 仅内部候选，用户只见唯一动作。 |
| ai-first-engineering | 86 | 95 | +9 | 已接入共享本职事实与项目回复合并合同。 |
| ai-regression-testing | 91 | 95 | +4 | 根因、多路径回归和验证摘要可面向用户呈现。 |
| algorithmic-art | 94 | 95 | +1 | 联网默认与离线要求一致。 |
| api-design | 92 | 95 | +3 | 契约、风险、测试与失败语义明确。 |
| art-asset-pipeline | 94 | 95 | +1 | 交付状态、确认点、未验证原因和清理责任可追溯。 |
| article-writing | 86 | 95 | +9 | 授权样本与阻塞/继续边界明确。 |
| brainstorming | 83 | 96 | +13 | 只在范围性变化时一次确认。 |
| browser-control | 93 | 95 | +2 | 能力、snapshot 选择、失败关闭完整。 |
| crawler4j-model-project | 88 | 94 | +6 | 阶段、兼容性结果和 blocked 可回传。 |
| doc-coauthoring | 94 | 95 | +1 | 读者、缺口、验证与最小输入清晰。 |
| document-templates | 92 | 95 | +3 | 文档状态、未生成原因和回传边界清楚。 |
| docx | 94 | 95 | +1 | 能力缺失、partial 与验证失败不会误报完成。 |
| executing-plans | 84 | 94 | +10 | 连续执行与 checkpoint 非人工 Gate 清楚。 |
| frontend-patterns | 93 | 95 | +2 | 行为、风险、验证范围与状态共享明确。 |
| gitcommitzh | 95 | 96 | +1 | 草案、阻塞、提交、远端状态及证据分层准确。 |
| go-developer | 83 | 96 | +13 | 风险分级、未运行全量项和范围明确。 |
| humanizer | 78 | 96 | +18 | 不得删改三段式及关键状态事实。 |
| java-developer | 89 | 95 | +6 | 阶段、根因、验证、阻塞与结果包明确。 |
| pdf | 94 | 95 | +1 | partial、OCR 风险、能力缺失和验证条件明确。 |
| project-memory | 91 | 95 | +4 | 恢复头部固定进度、当前任务、停止原因、唯一动作。 |
| python-uv-project | 85 | 96 | +11 | 定向/全量验证按风险收敛并披露未运行范围。 |
| receiving-code-review | 90 | 95 | +5 | triage、授权写入和技术异议解释明确。 |
| release-deployment | 88 | 96 | +8 | 发布回执、三段式示例与唯一动作闭合。 |
| requesting-code-review | 93 | 96 | +3 | 独立性、整改、人工 Gate 和结论边界明确。 |
| requirements-engineering | 92 | 95 | +3 | 草稿、批准、影响与未决项不混淆。 |
| shadcn | 93 | 95 | +2 | 风险、验证及项目化回传边界明确。 |
| stratix-admin-web | 90 | 95 | +5 | 既有模式比较、差异和清单明确。 |
| stratix-service | 89 | 95 | +6 | 摘要、兼容检查和可读状态完整。 |
| subagent-driven-development | 85 | 94 | +9 | receipt 映射、授权范围和 DONE 不关闭清楚。 |
| systematic-debugging | 95 | 96 | +1 | 现象、直接/根源原因、修复位置和回归完整。 |
| tdd-workflow | 96 | 96 | 0 | Red/Green、根因、覆盖与修复位置完整。 |
| ui-ux-pro-max | 90 | 95 | +5 | 检索、风险、状态和验证可读。 |
| using-shanforge | 91 | 96 | +5 | WBS、测试计数、Bug/修复字段、唯一动作有合同和实际输出。 |
| verification-before-completion | 96 | 96 | 0 | 新鲜证据、局部替代与未覆盖范围完整。 |
| webapp-testing | 93 | 95 | +2 | 断言、环境、partial、失败证据及路由候选清楚。 |
| writing-plans | 93 | 85 | -8 | 主 Skill 已改“验收标准”，直接模板仍要求“验收结果”。 |
| xlsx | 94 | 95 | +1 | 读回验证、partial、缺能力与唯一动作明确。 |

- coverage: `38/38`
- 平均 before: `90.24`
- 平均 after: `94.95`
- 平均 delta: `+4.71`

## 原始 Finding 裁决

| ID | decision | 证据/理由 |
|---|---|---|
| ZH-I01 | partially_fixed | 主 Skill 已用“验收标准”，但 `workitem-plan-template.md:72` 仍写“目标和验收结果”，计划前事实语义错误。 |
| ZH-I02–ZH-I07 | verified_fixed | 派发单一 owner、中文字段分组、设计检索/组件/验证替代/组件盘点均已闭环。 |
| ZH-M01–ZH-M06 | verified_fixed | 首次术语释义、snapshot 中文说明、授权语气样本、清理 owner、receipt 释义、路由 owner 均闭环。 |
| SD-I01–SD-I05 | verified_fixed | 外部能力、浏览器探测、正式身份、写授权、纯状态分支均闭环。 |
| SD-M01 | rejected_with_reason_accepted | algorithmic-art 默认联网、离线随包、p5 1.7.0 边界一致。 |
| SD-M02–SD-M04 | verified_fixed | Office fallback、review owner、共享结果 owner 均闭环。 |
| SE-I01–SE-I05 | verified_fixed | 身份、receipt、evidence、派发黑盒与兼容 fixture 已有证据；软件工程 reviewer 对兼容深度另有整改要求。 |
| SE-M01–SE-M03 | verified_fixed | manifest、AST 形态、Office 往返闭环。 |
| PM-I01–PM-I05 | verified_fixed | 本维度认为 WBS/身份/状态/评审/快照均可读；PM reviewer 对 DAG 与双模板真实性另有整改要求。 |
| PM-M01–PM-M02 | verified_fixed | 停止原因和完整 Gate 表闭环。 |
| CM-I01–CM-I05 | verified_fixed | 三段式保护、32 Skill 接入、确认边界、验证范围和实际黑盒均闭环。 |
| CM-M01–CM-M03 | verified_fixed | 内部候选、发布回执和发布示例闭环。 |

## 用户可读性结论

- WBS：有四态、分母、当前项、未开始/阻塞项和已完成可观察结果。
- 测试：有总数、通过/失败/错误/阻塞/跳过/未运行/取消，失败逐项给归因与 owner。
- Bug：有现象、影响、复现、直接原因、根源原因、风险和回归。
- 修复：每处强制 `file/symbol/change/reason/verification`。
- 下一动作：只显示一个 `next_required_action`。

`planned | current | completed` 是 WBS 展示状态，不是 TaskCard 生命周期。唯一未闭环沟通问题是模板“验收结果”，应改为“目标和验收标准”并增加反向断言。

## 首轮 Gate

- 原始闭环：`verified_fixed=43`、`rejected_with_reason_accepted=1`、`partially_fixed=1`
- remaining: `C0/I1/M0`
- gate_decision: `changes_requested`

## 定向复审补充

- `ZH-I01`：`verified_fixed`。正式模板现为“目标和验收标准”，测试反向禁止“目标和验收结果”。
- WBS 进度状态与 TaskCard 生命周期已明确分离；owner、depends_on、current_gate 与单数 next_required_action 均进入模板和 DAG 校验。
- `writing-plans` 沟通 after 分由 `85` 修订为 `96`；其余 37 项不变。
- after 平均 `95.24`；before `90.24`；delta `+5.00`。
- remaining/new C/I/M：`0/0/0`；最终 `gate_decision: approved`。
