# Skill 设计维度复评

## 结论

`gate_decision: changes_requested`。正式计划模板仍输出与自身评审词表冲突的状态，且贯通测试把该非法状态当作正常样例。因此原始 `ZH-I01`、`PM-I04`、`PM-I05` 只能判定 `partially_fixed`。其余均有当前文本、脚本或测试证据；`SD-M01` 的不采纳理由可接受。

## 38/38 评分

| Skill | before | after | delta | reason/evidence |
|---|---:|---:|---:|---|
| agent-harness-construction | 87 | 92 | +5 | `next_actions` 仅为内部候选且用户只见一个 next action；`test_response_owner_contracts.py` 覆盖。 |
| ai-first-engineering | 88 | 91 | +3 | 根因修复、兜底禁令与状态包边界清楚；无专门行为验证，未给 95+。 |
| ai-regression-testing | 91 | 93 | +2 | 多路径根因回归和风险分级完整；无本轮专门结构/行为用例。 |
| algorithmic-art | 86 | 94 | +8 | `SKILL.md:26-27` 明定联网默认与离线/自包含内联或随包；viewer 固定 p5.js `1.7.0`。 |
| api-design | 91 | 92 | +1 | 契约、风险与验证边界可用；无新增行为验证。 |
| art-asset-pipeline | 72 | 96 | +24 | 不再调用不存在脚本；`validate_manifest.py` 与合法/非法 manifest 的直接执行测试证明 fail-closed。 |
| article-writing | 90 | 92 | +2 | 仅用户提供/授权样本，禁止自行抓取、推断或模仿未授权个人；残余测试覆盖。 |
| brainstorming | 88 | 89 | +1 | 人工确认只限范围性决策；无本轮直接行为验证。 |
| browser-control | 74 | 93 | +19 | 能力探测、固定优先级、全不可用 `blocked`、快照选择语义完整；合同测试可复核。 |
| crawler4j-model-project | 86 | 96 | +10 | 先跑真实兼容检查器；兼容/不兼容/缺 CLI 无 traceback 夹具均覆盖。 |
| doc-coauthoring | 89 | 90 | +1 | 读者、事实、blocked/needs 边界充分；无新增专门验证。 |
| document-templates | 84 | 85 | +1 | 渐进读取和外部校验 fallback 清楚；外部模板探测仍主要依赖文字合同。 |
| docx | 83 | 93 | +10 | 能力探测与唯一 blocked 动作；`unpack→pack→unpack→package validation` 实测。 |
| executing-plans | 84 | 86 | +2 | 前置条件改为“验收标准”；仍与总控有一定规则重叠。 |
| frontend-patterns | 91 | 93 | +2 | 状态提升准确改为兄弟/下游组件共享；残余合同测试。 |
| gitcommitzh | 92 | 93 | +1 | 原有 Gate、范围和回读约束保持明确；无本轮新增执行证据。 |
| go-developer | 89 | 92 | +3 | 定向/全量验证边界和未运行项披露已明确。 |
| humanizer | 90 | 93 | +3 | 保护 Shanforge 三段式状态事实；集成合同可复核。 |
| java-developer | 87 | 88 | +1 | 阶段与按需读取合理；最低验证 fallback 仍主要是文字规则。 |
| pdf | 82 | 92 | +10 | 探测、fail-closed 与唯一下一动作明确；缺少真实 PDF 能力矩阵测试。 |
| project-memory | 80 | 94 | +14 | 无活动 WorkItem 的纯 `SB-STATUS` 跳过 ledger、不阻塞、不写事实；合同测试覆盖。 |
| python-uv-project | 84 | 90 | +6 | 非全量验证范围与根因纪律明确；无本轮专门行为验证。 |
| receiving-code-review | 82 | 94 | +12 | 写 triage/response/ledger/memory 必须 allowlist 与 write policy 同时授权；owner 已收敛。 |
| release-deployment | 90 | 93 | +3 | 发布只回本职回执，项目可读状态由共享合同和总控合并。 |
| requesting-code-review | 91 | 94 | +3 | 不再生成 triage/response；真实 feedback 的 owner 只在 receiving skill。 |
| requirements-engineering | 87 | 88 | +1 | 输入输出边界稳定；PRD 升级判据仍偏判断型。 |
| shadcn | 85 | 86 | +1 | 按需读取与工具不可用退出基本可用；无新增行为证据。 |
| stratix-admin-web | 86 | 93 | +7 | 先记录既有页面/组件、可复用模式和差异，再列清单；合同测试覆盖。 |
| stratix-service | 86 | 96 | +10 | 固定矩阵兼容检查器实际执行兼容、不兼容和非法依赖夹具。 |
| subagent-driven-development | 85 | 95 | +10 | 派发规则单一 owner；worker receipt 不得直接提升批次状态；FLOW-S11 与 T13 实际回执支持。 |
| systematic-debugging | 91 | 93 | +2 | 根因、事实 owner、风险和停止条件持续清晰；无本轮专门结构测试。 |
| tdd-workflow | 90 | 96 | +6 | AST 检查器实际拒绝命名局部函数并报告单调用 helper；测试直接执行。 |
| ui-ux-pro-max | 86 | 90 | +4 | “设计知识检索命中”语义已消歧；外部检索失败合同仍缺行为验证。 |
| using-shanforge | 83 | 96 | +13 | 派发判定、状态包单一 owner、共享合同、黑盒流程和真实父工具回执相互印证。 |
| verification-before-completion | 92 | 94 | +2 | 局部替代完整验证的条件、证据和残余风险披露明确。 |
| webapp-testing | 85 | 88 | +3 | 只返回 browser-control 候选与能力边界，总控独占路由；能力探测仍无直接执行测试。 |
| writing-plans | 77 | 85 | +8 | 临时 ID 已删除、Gate 表补齐，但正式模板仍有 `current`/“验收结果”残留，不能进入 90+。 |
| xlsx | 84 | 94 | +10 | 能力探测与 blocked 合同完整，最小 Office 往返在夹具中真实运行。 |

- coverage: `38/38`
- 平均 before: `86.0`
- 平均 after: `91.9`
- 平均 delta: `+5.9`

## 原始 Finding 逐项裁决

| ID | 严重度 | decision | 精确证据 / 理由 |
|---|---|---|---|
| ZH-I01 | Important | partially_fixed | 四个主 Skill 已改“验收标准”，但 `writing-plans/references/workitem-plan-template.md:72` 仍写“目标和验收结果”，是计划执行前输入，仍会误写未发生事实。 |
| ZH-I02 | Important | verified_fixed | `subagent-driven-development/SKILL.md:57-61` 仅引用总控唯一派发判定；残余合同测试断言旧重复公式已消失。 |
| ZH-I03 | Important | verified_fixed | `using-shanforge/SKILL.md:192-212` 按身份、控制/复杂度、风险/范围、派发、Gate/升级分组。 |
| ZH-I04 | Important | verified_fixed | `ui-ux-pro-max/SKILL.md:8,77` 使用“设计知识检索命中/未命中”。 |
| ZH-I05 | Important | verified_fixed | `frontend-patterns/SKILL.md:28` 改为多个兄弟或下游组件共享。 |
| ZH-I06 | Important | verified_fixed | `verification-before-completion/SKILL.md:57-68` 限定替代完整验证的条件、exit code、未覆盖范围和风险。 |
| ZH-I07 | Important | verified_fixed | `stratix-admin-web/SKILL.md` 要求记录既有文件、复用模式、差异和清单。 |
| ZH-M01 | Minor | verified_fixed | `receiving-code-review/SKILL.md` 首次写“基于技术证据提出异议（pushback）”。 |
| ZH-M02 | Minor | verified_fixed | `browser-control/SKILL.md:76` 分别说明三种 snapshot 的对象与选择条件。 |
| ZH-M03 | Minor | verified_fixed | `article-writing/SKILL.md:14,36` 限为用户提供或明确授权样本。 |
| ZH-M04 | Minor | verified_fixed | `art-asset-pipeline/SKILL.md:30-31,60-66` 将清理收敛到收尾规则。 |
| ZH-M05 | Minor | verified_fixed | `project-memory/SKILL.md:16,67` 首次释义“读取回执（receipt）”。 |
| ZH-M06 | Minor | verified_fixed | `webapp-testing/SKILL.md` 只返回 browser-control 候选，由总控路由。 |
| SD-I01 | Important | verified_fixed | `art-asset-pipeline/SKILL.md:33,94-96` 明示脚本不存在且新增 manifest validator；测试直接验真/验假。 |
| SD-I02 | Important | verified_fixed | `browser-control/SKILL.md:26-31,35,78` 先探测、固定路由、不可用关闭。 |
| SD-I03 | Important | verified_fixed | `writing-plans/SKILL.md:10-16,89-92` 缺正式身份即 blocked，不生成临时 ID。 |
| SD-I04 | Important | verified_fixed | `receiving-code-review/SKILL.md:12-17,45-54` 写入须 allowlist 与 write policy 同时授权。 |
| SD-I05 | Important | verified_fixed | `project-memory/SKILL.md:16,76-77` 纯状态无任务跳过 ledger。 |
| SD-M01 | Minor | rejected_with_reason_accepted | `algorithmic-art/SKILL.md:26-27` 明示默认联网，离线/自包含必须内联或随包；`templates/viewer.html:8,23` 固定联网边界及 p5.js `1.7.0`。 |
| SD-M02 | Minor | verified_fixed | `docx`、`pdf`、`xlsx` 均有能力探测、缺失能力、未执行步骤和唯一下一动作。 |
| SD-M03 | Minor | verified_fixed | requesting 不写 triage/response；receiving 仅实际反馈且授权时形成。 |
| SD-M04 | Minor | verified_fixed | `using-shanforge/SKILL.md:445-460` 只引用共享合同；字段由 `work-skill-return-contract.md` 单一拥有。 |
| SE-I01 | Important | verified_fixed | 正式身份完整性与临时 ID 禁令已在 planning route 固化。 |
| SE-I02 | Important | verified_fixed | `subagent-driven-development/SKILL.md:89-102` 将四种 worker receipt 映射为唯一动作，禁止 `DONE→ready_for_review`。 |
| SE-I03 | Important | verified_fixed | `verification-before-completion/SKILL.md:45-68` 区分普通回读回执与批次/关闭落盘 evidence。 |
| SE-I04 | Important | verified_fixed | `FLOW-S11` 覆盖派发、回执、模型/fork、失败关闭；T13 有 E029/E030 实际回执。 |
| SE-I05 | Important | verified_fixed | 两个兼容检查器均被兼容/不兼容/缺失或非法输入夹具实际执行。 |
| SE-M01 | Minor | verified_fixed | manifest validator 检查来源、相对路径、临时路径和文件存在性；夹具直接执行。 |
| SE-M02 | Minor | verified_fixed | AST 实现由 `test_code_shape_check.py` 直接验证拒绝与报告。 |
| SE-M03 | Minor | verified_fixed | `test_office_skill_roundtrip.py` 对 DOCX/XLSX 执行真实往返验证。 |
| PM-I01 | Important | verified_fixed | WBS 四列与 PM snapshot 贯通用例存在。 |
| PM-I02 | Important | verified_fixed | TaskCard/ledger/session 复用稳定身份、gate 与下一动作。 |
| PM-I03 | Important | verified_fixed | `test_review_approval_does_not_complete_task_card_or_wbs` 分离 approved 与 completed/closed。 |
| PM-I04 | Important | partially_fixed | `plan-review-template.md:21` 检查合法词表，但正式 `workitem-plan-template.md:56` 输出 `current`，正是该检查禁止的值。 |
| PM-I05 | Important | partially_fixed | 贯通测试实例化模板时将状态替换为 `current`；只证明投影能渲染，未证明正式模板满足生命周期合同。 |
| PM-M01 | Minor | verified_fixed | session card 有独立停止原因。 |
| PM-M02 | Minor | verified_fixed | Gate 表包含 ID、owner、进入条件、evidence path、状态。 |
| CM-I01 | Important | verified_fixed | humanizer 保留 Shanforge 三段式事实；集成合同已覆盖。 |
| CM-I02 | Important | verified_fixed | 共享合同定义本职结果包和项目化合并；T13 响应合同检查通过。 |
| CM-I03 | Important | verified_fixed | brainstorming 只在目标/范围/验收/不可逆取舍变更时确认。 |
| CM-I04 | Important | verified_fixed | Go/Python Skill 要求披露已运行范围和未运行全量项。 |
| CM-I05 | Important | verified_fixed | 响应集成测试保存可消费的三段式响应并逐字段断言。 |
| CM-M01 | Minor | verified_fixed | `next_actions` 只为内部候选。 |
| CM-M02 | Minor | verified_fixed | release 只拥有发布回执；共享合同负责最终合并。 |
| CM-M03 | Minor | verified_fixed | shared contract 有 release_summary，集成测试覆盖发布可读响应。 |

## 残留与下一步

- remaining C/I/M: `0/3/0`
- 新发现 C/I/M: `0/0/0`；残留均为原 Finding 的未完整整改，不重复计数。
- 影响：正式模板会生成 `current`，而 plan review 又要求拒绝该值；同一计划可能在生成后即不符合自身 Gate，生命周期数据也无法作为一致事实源。
- 下一步：将 `workitem-plan-template.md:56` 的状态样例改为允许词表，并将第 72 行“验收结果”改为“验收标准”；更新贯通测试为合法 `planned/active/ready_for_review` 样例，同时新增“模板值被 plan review 接受、`current` 被拒绝”的断言。完成后重新运行相关 snapshot、plan-review 与全量质量门。

## 定向复审补充

- `ZH-I01`：`verified_fixed`。`workitem-plan-template.md` 已改为“目标和验收标准”，旧“验收结果”有反向断言。
- `PM-I04`：`verified_fixed`。`plan-review-template.md` 和正式模板明确 WBS `planned | current | completed` 是进度状态，TaskCard 生命周期是独立字段；首轮把 `current` 当非法 TaskCard 状态的判断撤回。
- `PM-I05`：`verified_fixed`。PM snapshot 测试同时实例化正式 plan 与 TaskCard 模板，并用 WBS=`current`、TaskCard/ledger=`active` 证明两套状态不互相污染。
- 首轮派生的 owner/depends_on 缺口：`verified_fixed`。两个正式模板均有稳定 owner/depends_on；`validate_task_graph.py::main` 拒绝缺 owner、未知依赖、自依赖、环和跨模板不一致，允许合法菱形 DAG。
- 新鲜证据：定向 `30 passed, 4 subtests passed`；全量 `356 passed, 11 subtests passed`；Ruff、38/38 validator、代码形态、ledger、黑盒与 diff check 通过。
- `writing-plans` Skill设计 after 分由 `85` 修订为 `94`；其余 37 项不变。
- 38 项 after 平均：`92.1`；相对 before `86.0`，delta `+6.1`。
- remaining/new C/I/M：`0/0/0`。
- 最终 `gate_decision: approved`。
