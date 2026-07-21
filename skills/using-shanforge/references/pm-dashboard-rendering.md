# PM 项目状态查询与看板渲染

本文件供 `using-shanforge` 在人类要求查看项目状态、PM 看板、阶段/任务进度、风险、变更、审批或交付状态时读取。它定义查询与展示合同，不是事实文件，也不是运行时 renderer 的替代实现。

## 核心结论

- `.factory/pm/` 不是全部事实源；它承载 PM 管理事实和周期性记录。
- 项目实时状态不得由 AI 在会话里临时扫描文件、自由聚合或计算。
- 固定代码从登记来源捕获同一不可变高水位 `H`，生成、验证、授权并渲染同一快照。
- AI 只形成意图候选、核对结果并给出有证据的专业检查；注册工具由确定性策略系统选择和授权。
- `skills/using-shanforge/references/status-dashboard-template.html` 是展示合同；生成页不是事实源。

## Excel 样例的一次性角色

用户提供的 Excel 只用于一次性提取页面名称、管理分区、列语义和阅读顺序，并把这些设计结果固化进 HTML 模板与 slot 合同。完成转换后：

- 标准项目状态查询不得打开、解析或依赖原始 `.xls` / `.xlsx` 文件。
- Excel 样例不是事实源、运行时输入、模板数据库或每次查询的前置步骤。
- renderer 每次只消费同一 `AuthorizedProgressSnapshot/v1` 和已固化的 HTML 模板。
- 即使用户另行要求 XLSX 输出，也由代码从同一快照生成新文件，不回读本次设计样例。

## 事实来源边界

| 来源 ID | 内容 | 仓内主要承载位置 |
|---|---|---|
| `SRC-PROJECT-MASTER-001` | 项目身份、负责人和稳定项目资料 | `.factory/project.json`、经批准的项目资料 |
| `SRC-FORMAL-DOC-MAP-001` | `doc-map` 指向的正式需求、设计和交付版本 | `docs/` 与 `.factory/memory/doc-map.md` 的受控索引 |
| `SRC-WORKITEM-LEDGER-001` | WorkItem、TaskCard、状态、评审和人工 Gate 事件 | `.factory/workitems/*/ledger.jsonl`、`reviews/` |
| `SRC-PM-EVENT-001` | 风险、里程碑、沟通、会议、状态报告、变更和总结 | `.factory/pm/` 的管理事实与事件 |
| `SRC-TASK-EVIDENCE-001` | 测试、构建、评审和任务证据 | `.factory/workitems/*/evidence/`、`reports/` |
| `SRC-DEPLOYMENT-EVENT-001` | 发布、部署、回滚和健康证据 | 经登记的交付/部署事件 |

`.factory/pm/dashboard.md` 是方便人类和 AI 浏览的 PM 摘要，不替代 work item ledger、正式文档、evidence 或部署事件。`.factory/pm/generated/` 只允许存放可再生成的展示结果；生成页不是事实源，不能反向更新项目状态。

## 会话中的固定九步流程

标准总览最多一次主工具调用；只有主结果返回合同登记的缺失、冲突、过期或异常标志时，才允许一次补充诊断调用，并记录原因。

1. **AI 意图候选**：AI 从用户原话、当前项目和允许的会话上下文形成 `IntentCandidate`，只表达候选意图、项目、范围、时间、格式、深度和歧义。
2. **确定性计划**：策略系统校验字面参数、默认值、认证主体、权限和注册表，输出唯一 `ToolCallPlan/v1`；真正影响唯一计划的歧义才追问一个最小问题。
3. **投影与截止点**：投影器捕获不可变高水位 `H`，检查 checkpoint、来源链和兼容性；查询不持久化追平，不改变项目业务状态。
4. **一次注册查询**：注册工具和只读查询层按计划读取同一 `H`，返回完整验证的 `ProjectProgressSnapshot/v2` 和 `ToolExecutionReceipt/v1`。
5. **权限过滤**：权限系统从受信会话 principal 产生 `AuthorizedProgressSnapshot/v1`；无权限字段在交给 AI 和 renderer 前已省略或脱敏。
6. **固定代码渲染**：renderer 只消费同一获授权快照和已固化模板，生成固定文本、会话 HTML、独立 HTML/按需 XLSX 输出和 `RenderManifest/v2`；不再次读取事实或 Excel 样例。
7. **逐字段核对**：核对器用 `ReconciliationResult/v2` 比较区、行、字段、来源、快照和授权摘要；任何不一致都失败关闭。
8. **AI 专业检查**：AI 只基于核对通过的摘要形成 `AIInspectionResult/v1`，检查范围、新鲜度、真实活动、审批、阻塞、逾期、风险、完成和上线证据。
9. **会话装配**：`SessionResponseAssembly/v1` 先逐字节放置代码事实看板，再放置独立 AI 检查；禁止改字、重排、补写或覆盖事实。

## AI 与代码边界

- AI 不计算完成率。
- AI 不计算状态、风险等级、偏差、逾期、权限或上线健康。
- AI 不拼装 HTML、Excel 或事实摘要。
- AI 不覆盖代码事实，也不把建议写进事实看板。
- AI 可以说明用户意图、工具选择、证据限制和专业建议。
- 每条 AI 发现必须给出严重度、事实陈述、证据引用、影响、建议动作和未验证假设。

会话响应固定分为两个区块：

1. **事实看板**：固定代码生成并通过核对，保持原字节。
2. **AI 专业检查**：独立建议区，明确不是项目事实。

## 看板信息架构

HTML 固定为第一页项目总览加十个管理页；页面结构已从一次性参考样例固化，不在查询时回读样例：

| 顺序 | 页面 | 固定 ID |
|---:|---|---|
| 0 | 项目总览 | `page-overview` |
| 1 | 项目成员 | `module-team` |
| 2 | 项目策划 | `module-charter` |
| 3 | WBS | `module-wbs` |
| 4 | 进度计划 | `module-schedule` |
| 5 | 风险管理 | `module-risks` |
| 6 | 沟通计划 | `module-communications` |
| 7 | 会议与行动 | `module-meetings` |
| 8 | 状态报告 | `module-status-reports` |
| 9 | 变更管理 | `module-changes` |
| 10 | 项目总结 | `module-closure` |

第一页首屏只显示：项目身份、阶段、固定 `H`、截止时间、验证状态；有效任务总数、完成数、完成率、真正进行中、待审批、阻塞/逾期和已上线；互斥状态分布；真正进行中、待审批、近期完成、已上线、阻塞/逾期和下一里程碑各一行摘要。目录和最多五项明细从首屏下方开始。

每个后续管理页必须显示数据条数、缺失项、冲突项、截止时间、来源摘要和无数据原因，并支持只读筛选、稳定排序、来源展开和键盘操作。

## 模板 slot

总览 scalar slot：

```text
PROJECT_NAME PROJECT_ID STAGE_NAME AS_OF_H AS_OF_TIME PROJECT_TIMEZONE
VALIDATION_STATUS VALIDATION_MESSAGE SNAPSHOT_ID SNAPSHOT_SHA256_SHORT
SOURCE_ROOT_SHA256_SHORT AUTHORIZATION_DIGEST_SHORT RULE_VERSION RENDER_DISPOSITION
TOTAL_TASKS COMPLETED_TASKS COMPLETION_RATE ACTIVE_TASKS PENDING_APPROVALS
BLOCKED_OR_OVERDUE_TASKS DEPLOYED_DELIVERABLES ACTIVE_SUMMARY APPROVAL_SUMMARY
RECENT_COMPLETION_SUMMARY DEPLOYMENT_SUMMARY BLOCKED_OVERDUE_SUMMARY
NEXT_MILESTONE_SUMMARY ERROR_CODE AFFECTED_PATHS RECOVERY_ACTION REDACTION_NOTICE
```

总览 fragment slot：`STATUS_DISTRIBUTION_SEGMENTS`、`STATUS_DISTRIBUTION_LEGEND`、`OVERVIEW_DETAIL_ROWS`。

十模块前缀依次为 `TEAM`、`CHARTER`、`WBS`、`SCHEDULE`、`RISKS`、`COMMUNICATIONS`、`MEETINGS`、`STATUS_REPORTS`、`CHANGES`、`CLOSURE`。每个前缀固定拥有：

```text
COUNT MISSING_COUNT CONFLICT_COUNT AS_OF_TIME SOURCE_DIGEST_SHORT
EMPTY_REASON ROWS SOURCE_DETAILS
```

### slot 类型和转义

- `scalar_text`：renderer 做 HTML 文本节点转义；禁止进入 URL、style、script 或未登记属性。
- `scalar_decimal`：代码先规范化十进制，再按文本节点转义；模板和脚本不得重算。
- `enum_token`：先按封闭枚举校验，再写入登记的文本和 `data-*` 属性。
- `render_fragment`：只能由固定 renderer 从类型化 collection 逐项生成；所有业务值按上下文转义；禁止原始 script/style、事件属性、任意 URL 或 AI/调用方 HTML。

## 验证状态和输出处置

`RENDER_DISPOSITION` 只允许：

- `FULL`：验证完整，展示全部获授权业务区。
- `PARTIAL`：只用于 `incomplete` 且合同明确允许部分输出；显示缺失与脱敏说明。
- `ERROR_ONLY`：`conflict|stale|failed` 必须使用；只显示身份、H、截止时间、验证、错误码、受影响路径和恢复动作，源码不得包含旧业务值。

可见业务看板中的模块 `CONFLICT_COUNT` 必须为 `0`。非零表示资格冲突，必须进入 `ERROR_ONLY`，不能把冲突业务详情混入 `PARTIAL`。

## 权限与安全

- 权限过滤先于 renderer 和 AI。
- 联系方式、财务、风险、变更和审批按字段权限省略、脱敏或显示“无权限”；禁止用 0 代替隐藏金额。
- HTML 源码、嵌入内容和只读交互脚本不得包含越权明文。
- 模板不得读取 `.factory/pm/`、work item ledger、Markdown、JSONL、cookie、local storage 或网络。
- 模板脚本只可筛选/排序已渲染行和展开来源，不计算业务事实，不执行项目写入。

## 输出与失败语义

- 客户端支持时，默认直接返回会话 HTML 事实看板；否则返回固定文本摘要和独立 HTML 入口。
- 用户明确要求独立 HTML 时，固定 renderer 可以使用 `status-dashboard-template.html` 写入 `.factory/pm/generated/status-dashboard.html`。
- 查询、渲染和查看不得创建 WorkItem、修改事实、更新 memory、提交 Git 或生成永久归档。
- 工具未注册、投影未就绪、来源链损坏、快照过期、权限不明或跨格式不一致时返回稳定错误；不得由 AI 退回手工扫描并声称“实时”。

## 当前实现边界（2026-07-21）

当前代码已存在 `ProjectStatusAPI` / `ProjectStatusService`、GET route 声明、固定 H 上下文、九字段位置绑定、权限过滤、disposition 和 15 行 `ProjectStatusResponse/v4` renderer。默认本地 composition 仍使用固定的 in-memory 项目状态夹具。

以下能力尚不能按事实宣称已交付：会话中的已注册项目状态工具、六类来源的完整生产投影、十区/137 字段获授权快照、总览加十页生产 HTML renderer、可选 XLSX 输出 renderer、`RenderManifest/v2` / `ReconciliationResult/v2` 跨格式核对和正式性能门。因此旧的“AI 读取文件后填模板”不是实时状态实现；本 reference 和 HTML 只完成查询/展示契约校准，不冒充生产 renderer 已完成。
