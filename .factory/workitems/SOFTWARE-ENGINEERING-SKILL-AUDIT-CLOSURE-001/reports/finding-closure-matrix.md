# 五专家原始 Finding 闭环表

## 当前结论

- 原始 Finding：`45/45` 已登记；Critical `0`、Important `27`、Minor `18`。
- 最终状态：`verified_fixed 44`、`rejected_with_reason_accepted 1`、`partially_fixed 0`、`unresolved 0`。
- 已关闭：`45/45`；尚未关闭：`0`。五位独立专家的最终结论均为 `approved`，最终剩余 `Critical 0 / Important 0 / Minor 0`。
- 修复归属：T10 `7/7`、T11 `11/11`、T12 `10/10` 已完成；`SD-M01` 的不采纳理由已由 T13 Skill 设计专家接受。

状态含义：`verified_fixed` 表示已有当前文件和测试证据；`partially_fixed` 表示只关闭部分现象；`unresolved` 表示问题仍存在；`rejected_with_reason` 只有 T13 独立 reviewer 接受后才算关闭。

## 中文语言专家：ZH（I7 / M6）

| ID | 严重度 | 问题 | 根因与精确位置 | 当前状态与证据 | 修复任务 |
|---|---|---|---|---|---|
| ZH-I01 | Important | 前置条件把尚未发生的“验收标准”写成“验收结果”。 | 术语把输入条件写成执行结论；`using-shanforge/SKILL.md` 简单任务判定、`writing-plans/SKILL.md` 简单任务/默认流程、`executing-plans/SKILL.md` 与 `subagent-driven-development/SKILL.md` 任务 gate。 | `verified_fixed`；四处前置条件均使用“验收标准”；见 `evidence/T12-verification.md`。 | T12 completed |
| ZH-I02 | Important | worker 派发公式在同一 Skill 重复定义。 | `subagent-driven-development/SKILL.md`“授权执行包”连续两段重复 `source_or_test_write + execution_authorized=true` 公式。 | `verified_fixed`；只引用总控唯一派发定义，旧重复公式已删除；见 `evidence/T12-verification.md`。 | T12 completed |
| ZH-I03 | Important | 英文路由字段缺少按身份、风险、派发、升级的中文分组解释。 | `using-shanforge/SKILL.md`“普通项目化路由包追加字段”只列英文块。 | `verified_fixed`；字段按五类中文用途准确且不重复分组；见 `evidence/T12-verification.md`。 | T12 completed |
| ZH-I04 | Important | “数据库命中”易误解为业务数据库。 | `ui-ux-pro-max/SKILL.md` 触发说明未表明这是设计知识检索结果。 | `verified_fixed`；改为设计知识检索命中/未命中；见 `evidence/T12-verification.md`。 | T12 completed |
| ZH-I05 | Important | “多个远端组件共享”易误解为远程组件。 | `frontend-patterns/SKILL.md` 状态提升规则用词错误。 | `verified_fixed`；改为兄弟或下游组件共享；见 `evidence/T12-verification.md`。 | T12 completed |
| ZH-I06 | Important | “完整验证”与局部替代的允许条件不明确。 | `verification-before-completion/SKILL.md`“验证完整命令/偏离原因”没有定义何时可以使用局部替代。 | `verified_fixed`；默认流程已限定替代原因、同声明覆盖、命令与退出码、未覆盖范围和残余风险；见 `evidence/T10-verification.md`。 | T10 completed |
| ZH-I07 | Important | “先总结相似组件”没有比较动作、判定标准和产物。 | `stratix-admin-web/SKILL.md` 默认流程第一步只有抽象描述。 | `verified_fixed`；已有文件、复用模式、差异和清单产物均明确；见 `evidence/T12-verification.md`。 | T12 completed |
| ZH-M01 | Minor | `pushback` 没有中文首次释义。 | `receiving-code-review/SKILL.md`“使用技术理由 pushback”。 | `verified_fixed`；首次写为“基于技术证据提出异议（pushback）”；见 `evidence/T11-verification.md`。 | T11 completed |
| ZH-M02 | Minor | DOM、state、accessibility snapshot 缺中文选择说明。 | `browser-control/SKILL.md` 页面状态章节直接并列英文词。 | `verified_fixed`；三类 snapshot 的验证对象和选择条件已中文说明；见 `evidence/T12-verification.md`。 | T12 completed |
| ZH-M03 | Minor | 模仿个人语气没有限定为用户提供或授权样本。 | `article-writing/SKILL.md` 只写“根据提供的示例”。 | `verified_fixed`；仅允许用户提供或明确授权样本；见 `evidence/T12-verification.md`。 | T12 completed |
| ZH-M04 | Minor | 临时资源清理要求在规则、流程和输出中重复。 | `art-asset-pipeline/SKILL.md` 资源规则、流程、输出三处重复同一 owner。 | `verified_fixed`；清理动作已收敛到单一收尾规则，流程和通过标准不再重复；见 `evidence/T10-verification.md`。 | T10 completed |
| ZH-M05 | Minor | `receipt` 首次出现没有解释为读取回执。 | `project-memory/SKILL.md` 条件读取链。 | `verified_fixed`；首次写为“读取回执（receipt）”；见 `evidence/T11-verification.md`。 | T11 completed |
| ZH-M06 | Minor | 工作 Skill 写“转交 browser-control”，与总控独占路由冲突。 | `webapp-testing/SKILL.md` 路由边界由工作 Skill 自己决定下一 Skill。 | `verified_fixed`；只返回候选与能力边界，总控独占路由；见 `evidence/T11-verification.md`。 | T11 completed |

## Skill 设计专家：SD（I5 / M4）

| ID | 严重度 | 问题 | 根因与精确位置 | 当前状态与证据 | 修复任务 |
|---|---|---|---|---|---|
| SD-I01 | Important | 资源管线硬引用不存在的 `remove_chroma_key.py`。 | `art-asset-pipeline/SKILL.md` 把不存在脚本写成可执行入口。 | `verified_fixed`；当前明确脚本不存在且不得运行，能力缺失 fail closed；`test_external_tool_skill_fallbacks.py` 覆盖。 | 无 |
| SD-I02 | Important | 浏览器 Skill 缺能力探测和全不可用失败关闭。 | `browser-control/SKILL.md` 原流程假设 CLI/插件存在。 | `verified_fixed`；已固定探测顺序、确定性路由和 missing capability 回执；相关测试覆盖。 | 无 |
| SD-I03 | Important | 计划 Skill 同时要求正式身份又允许临时 ID。 | `writing-plans/SKILL.md` 身份 owner 冲突。 | `verified_fixed`；缺身份现在 blocked，正式身份只由 tracking workflow 创建；T01 测试通过。 | 无 |
| SD-I04 | Important | receiving review 无条件同步 ledger/memory，可能越过 allowlist。 | `receiving-code-review/SKILL.md` 默认流程和完成条件把 memory sync 设为无条件动作。 | `verified_fixed`；所有写入需 allowlist 与 write_policy 同时授权，未授权交还总控；见 `evidence/T11-verification.md`。 | T11 completed |
| SD-I05 | Important | 无活动 WorkItem 的纯 `SB-STATUS` 分支不明确。 | `project-memory/SKILL.md` 默认流程仍要求读取 work-item ledger，没有明确跳过规则。 | `verified_fixed`；纯状态无活动任务分支明确跳过 ledger、不阻塞、不写事实；见 `evidence/T11-verification.md`。 | T11 completed |
| SD-M01 | Minor | p5.js viewer 的联网版本与离线自包含边界被认为不清。 | 原审计未纳入 `algorithmic-art/SKILL.md` 已有的交付模式和模板说明。 | `rejected_with_reason_accepted`；现有 Skill 明确默认联网、离线需内联/随包提供，模板固定 p5.js 1.7.0；T13 Skill 设计专家已接受不采纳理由。 | T13 completed |
| SD-M02 | Minor | DOCX/PDF/XLSX 缺能力探测和 blocked fallback。 | 原 Skill 假定依赖存在。 | `verified_fixed`；三个 Skill 均已有探测、missing capability 和唯一动作；合同测试覆盖。 | 无 |
| SD-M03 | Minor | requesting/receiving 对同范围整改是否生成 triage/response 的 owner 不一致。 | `requesting-code-review/SKILL.md` 禁止逐轮产物，`receiving-code-review/SKILL.md` 强制每轮生成。 | `verified_fixed`；requesting 组织评审，receiving 仅在真实 feedback 且获授权时形成 triage/response；见 `evidence/T11-verification.md`。 | T11 completed |
| SD-M04 | Minor | 总控与共享 reference 重复定义工作结果包字段。 | `using-shanforge/SKILL.md`“工作 skill 状态回写协议”复制 `work-skill-return-contract.md` 字段。 | `verified_fixed`；总控只引用共享单一来源并保留专属合并/状态 owner；见 `evidence/T12-verification.md`。 | T12 completed |

## 软件工程专家：SE（I5 / M3）

| ID | 严重度 | 问题 | 根因与精确位置 | 当前状态与证据 | 修复任务 |
|---|---|---|---|---|---|
| SE-I01 | Important | 正式身份和临时 ID 冲突。 | `writing-plans` 与 `using-shanforge` 身份 owner 不唯一。 | `verified_fixed`；正式身份、缺身份 blocked 和模板测试均已落实。 | 无 |
| SE-I02 | Important | worker receipt 与批次控制器状态没有唯一映射。 | `subagent-driven-development/SKILL.md` 原枚举混用。 | `verified_fixed`；四种 receipt 处理表和禁止 `DONE→ready_for_review` 已有测试。 | 无 |
| SE-I03 | Important | 普通任务回执和落盘 evidence 规则冲突。 | verification 主文与 checklist 不一致。 | `verified_fixed`；普通任务可读回执、批次/关闭落盘规则已统一并测试。 | 无 |
| SE-I04 | Important | 黑盒流程没有覆盖真实 worker 派发、授权回执和失败关闭。 | `tests/test_black_box_workflow_eval.py::evaluate_observation` 只覆盖身份、review、verification、commit gate；模型派发仅有静态合同测试。 | `verified_fixed`；FLOW-S11 有 7 条断言与 16 个 mutation，真实父工具回执由 T13 复核；见 `evidence/T12-verification.md`。 | T12 completed |
| SE-I05 | Important | Crawler4j/Stratix 精确版本缺实际兼容 smoke 和可复验来源。 | 两个版本门测试只读取 Markdown 断言短语，没有兼容/不兼容 CLI fixture。 | `verified_fixed`；两个所属 Skill 均有真实兼容检查脚本，测试直接执行兼容/不兼容 fixture，缺能力清晰失败；见 `evidence/T10-verification.md`。 | T10 completed |
| SE-M01 | Minor | 资源 manifest 完整性仍靠人工检查。 | `art-asset-pipeline/SKILL.md` 只有字段列表和检查清单，无确定性 validator/fixture。 | `verified_fixed`；新增确定性 validator 并由合法/非法 fixture 直接执行；见 `evidence/T10-verification.md`。 | T10 completed |
| SE-M02 | Minor | `code_shape_check` 仍由作者自报。 | `tdd-workflow/SKILL.md` 和共享状态包没有机械检查入口。 | `verified_fixed`；新增 AST 入口拒绝局部命名函数并报告单调用候选；见 `evidence/T10-verification.md`。 | T10 completed |
| SE-M03 | Minor | DOCX/XLSX 没有真实 unpack→pack→validate round-trip。 | 两个 Skill 只有单次 validate 或人工重开要求，测试仅检查 blocked 文本。 | `verified_fixed`；DOCX/XLSX 最小样本均执行 unpack→pack→unpack→validate；见 `evidence/T10-verification.md`。 | T10 completed |

## 软件项目管理专家：PM（I5 / M2）

| ID | 严重度 | 问题 | 根因与精确位置 | 当前状态与证据 | 修复任务 |
|---|---|---|---|---|---|
| PM-I01 | Important | 计划模板不生成 PM 快照需要的四列 WBS。 | `workitem-plan-template.md` 与 `project_snapshot.py` 原合同不一致。 | `verified_fixed`；模板、解析器和任意深度树测试已统一。 | 无 |
| PM-I02 | Important | TaskCard/ledger 缺稳定身份、Gate 和下一动作。 | task/ledger/session 恢复字段不一致。 | `verified_fixed`；模板已统一身份与恢复字段，完成层级由总控独占。 | 无 |
| PM-I03 | Important | `approved` 被当作 TaskCard/WBS 完成。 | review 状态和任务生命周期复用同一词表。 | `verified_fixed`；生命周期、review_status 和快照完成判定已分离。 | 无 |
| PM-I04 | Important | plan review 未检查依赖 DAG、状态词表和完整恢复字段。 | `plan-review-template.md` 只增加 WBS/TaskCard 映射，未覆盖 DAG 和生命周期/review 词表。 | `verified_fixed`；已列 DAG、完整生命周期/review_status 与恢复字段检查；见 `evidence/T11-verification.md`。 | T11 completed |
| PM-I05 | Important | 没有“正式模板→TaskCard/ledger→PM 快照”的真实贯通测试。 | 当前集成测试仍手工构造 plan/TaskCard，模板测试仍是关键词断言。 | `verified_fixed`；正式计划模板已实例化并贯通 TaskCard、ledger 和真实 PM snapshot 页面；见 `evidence/T10-verification.md`。 | T10 completed |
| PM-M01 | Minor | session card 缺停止原因。 | `project-memory/references/session-card-template.md` 已补任务、WBS、Gate、下一动作，但没有独立 stop reason。 | `verified_fixed`；会话卡已有独立停止原因；见 `evidence/T11-verification.md`。 | T11 completed |
| PM-M02 | Minor | 计划 Gate 列表缺 Gate ID、owner、进入条件和 evidence path。 | `writing-plans/references/workitem-plan-template.md` 集中质量门只有状态项。 | `verified_fixed`；集中 Gate 表已包含全部字段；见 `evidence/T11-verification.md`。 | T11 completed |

## 沟通专家：CM（I5 / M3）

| ID | 严重度 | 问题 | 根因与精确位置 | 当前状态与证据 | 修复任务 |
|---|---|---|---|---|---|
| CM-I01 | Important | humanizer 可能删除三段式状态事实。 | humanizer 未区分普通 AI 文风和 Shanforge 状态合同。 | `verified_fixed`；保护例外和集成测试已加入。 | 无 |
| CM-I02 | Important | 32 个工作 Skill 没有明确接入共享可读事实。 | 局部结果包和项目化回复边界不清。 | `verified_fixed`；32/32 各引用一次共享合同，字段与 owner 测试通过。 | 无 |
| CM-I03 | Important | brainstorming 逐章节确认制造无意义停顿。 | 章节展示被误当作人工 Gate。 | `verified_fixed`；只有改变目标/范围/验收/不可逆取舍才确认。 | 无 |
| CM-I04 | Important | Go/Python 默认全量验证与风险分级冲突。 | 语言 Skill 自己扩大验证范围。 | `verified_fixed`；普通修改定向、高风险/批次全量并说明未运行范围。 | 无 |
| CM-I05 | Important | 关键词测试不能证明最终回复真正可读。 | 测试没有实际代理输出和失败事实链。 | `verified_fixed`；T08 黑盒 v6 保存完整输入/输出并通过 9/9 断言。 | 无 |
| CM-M01 | Minor | 工具的复数 `next_actions` 没说明只是内部候选。 | `agent-harness-construction/SKILL.md` 可执行后续动作可能直接暴露给用户。 | `verified_fixed`；复数动作仅为内部候选，用户只见唯一下一动作；见 `evidence/T11-verification.md`。 | T11 completed |
| CM-M02 | Minor | 发布 Skill 只返回回执，缺共享状态事实。 | 原发布状态包没有 human/progress/verification/defect/change 合并。 | `verified_fixed`；release Skill 已接入共享回写合同并定义 blocked。 | 无 |
| CM-M03 | Minor | 响应合同测试没有发布类字段填充场景。 | 当前集成测试覆盖开发、测试、Bug、修复，没有 release 示例。 | `verified_fixed`；新增三段式发布示例并逐字段消费验证；见 `evidence/T11-verification.md`。 | T11 completed |

## T10–T12 精确修复清单

### T10：7 项

- ZH-I06、ZH-M04。
- SE-I05、SE-M01、SE-M02、SE-M03。
- PM-I05。

### T11：11 项

- ZH-M01、ZH-M05、ZH-M06。
- SD-I04、SD-I05、SD-M03。
- PM-I04、PM-M01、PM-M02。
- CM-M01、CM-M03。

### T12：10 项

- ZH-I01、ZH-I02、ZH-I03、ZH-I04、ZH-I05、ZH-I07、ZH-M02、ZH-M03。
- SE-I04、SD-M04。

### T13 独立判断：1 项

- SD-M01：独立专家确认现有联网/离线说明足以关闭原 Minor，决定为 `rejected_with_reason_accepted`。

## T13 最终独立复评决定

| 专家 | 覆盖的原始 Finding | 最终决定 | 复评证据 |
|---|---|---|---|
| 中文语言 | ZH-I01～ZH-I07、ZH-M01～ZH-M06 | 13 项 `verified_fixed`，C0 / I0 / M0，`approved` | `../reviews/T13-chinese-language.md` |
| Skill 设计 | SD-I01～SD-I05、SD-M02～SD-M04 | 8 项 `verified_fixed`，C0 / I0 / M0，`approved` | `../reviews/T13-skill-design.md` |
| Skill 设计 | SD-M01 | 1 项 `rejected_with_reason_accepted`，计为关闭 | `../reviews/T13-skill-design.md` |
| 软件工程 | SE-I01～SE-I05、SE-M01～SE-M03 | 8 项 `verified_fixed`，C0 / I0 / M0，`approved` | `../reviews/T13-software-engineering.md` |
| 软件项目管理 | PM-I01～PM-I05、PM-M01～PM-M02 | 7 项 `verified_fixed`，C0 / I0 / M0，`approved` | `../reviews/T13-project-management.md` |
| 沟通 | CM-I01～CM-I05、CM-M01～CM-M03 | 8 项 `verified_fixed`，C0 / I0 / M0，`approved` | `../reviews/T13-communication.md` |

整改后总分和 38 个 Skill 的前后变化见 `post-remediation-scorecard.md`。
