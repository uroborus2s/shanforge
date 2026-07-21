# PM 项目状态查看模板契约校准实施计划

> **给执行者：** 计划评审通过后，把状态交还 `using-shanforge` 流程总控判断下一步。

**目标：** 将 Excel 样例的十模块信息架构一次性固化进 HTML 模板，并建立同一固定 H 快照消费、代码计算事实、AI 只做意图识别与专业检查的项目状态查看契约；运行时不回读 Excel 样例。

**架构：** `using-shanforge` 只形成 `IntentCandidate` 并发起一次已注册项目状态查询；固定代码捕获 H、读取/验证/授权快照并渲染，模板不读取事实源也不派生项目状态。模板内原生 JavaScript 只对已渲染 DOM 做只读筛选、排序和来源展开，不访问网络或改变事实。

**技术栈：** Markdown、HTML/CSS、受限原生 JavaScript、Python `pytest`、系统 Chrome headless。

**工作项：** `PM-DASHBOARD-002`

**状态：** `approved_ready_for_commit`

## 输入

- 正式需求：`docs/04-product/prd.md` 的 `WF-CTL-010`。
- 正式设计：`docs/05-design/frontend-design.md` §26.6。
- 任务简报：`.factory/workitems/PM-DASHBOARD-002/task-briefs/PM-DASHBOARD-002-T01.md`。
- 记忆入口：`.factory/memory/agent-session.md`、`.factory/memory/doc-map.md`。
- 原始 Excel：`/Users/uroborus/Documents/项目文档/项目管理/Excel版(可直接套用_非常实用).xls`；已只读核对 `00目录` 和十个业务 sheet。

## 范围

### 目标

- 纠正“所有事实都在 `.factory/pm/`”的歧义，区分 PM 管理事实、正式事实、执行事实、部署事实和生成视图。
- 固化“会话请求 → AI 意图候选 → 唯一工具计划 → 固定 H 快照 → 权限过滤 → 固定代码渲染/核对 → AI 专业检查 → 会话响应”的快速路径。
- 把 HTML 模板改为第一页项目驾驶舱加 Excel 十模块，并提供精确 slot、错误/权限处置和只读交互契约。
- 用静态契约测试与真实 Chrome 固定 fixture 验证五视口、可访问性和只读交互。

### 非目标

- 不实现 137 字段生产快照、HTML/XLSX renderer、SQLite 投影或跨格式核对器。
- 不把手工遍历 `.factory/pm/`、work item ledger 或正式文档包装成“实时查询”。
- 不修改 `src/`、正式 PRD/设计、PM 事实文件、现有混合 work item ledger 或 memory 脏改动。
- 不在模板脚本中计算完成率、状态、风险、权限或业务派生值。
- 不把原始 Excel 样例作为运行时输入；它只用于本次模板信息架构设计。

## 文件

| 类型 | 路径 | 职责 |
|---|---|---|
| 修改 | `skills/using-shanforge/SKILL.md` | 将 PM 查询入口改为单次注册状态查询，不再要求 AI 临时聚合实时事实 |
| 修改 | `skills/using-shanforge/references/pm-dashboard-rendering.md` | 说明事实边界、固定 H 九步路径、slot 和错误/权限合同 |
| 修改 | `skills/using-shanforge/references/status-dashboard-template.html` | 总览 + 十模块、响应式、可访问、只读交互模板 |
| 测试 | `tests/test_pm_dashboard_template_contract.py` | 结构、slot、流程和负向安全契约 |
| 测试 | `tests/test_pm_dashboard_template_browser.py` | 五视口几何、焦点、对比度、交互和截图 |
| 新建 | `.factory/workitems/PM-DASHBOARD-002/evidence/PM-DASHBOARD-002-T01-verification.md` | 红灯、绿灯、浏览器和回归证据 |
| 新建 | `.factory/workitems/PM-DASHBOARD-002/reports/PM-DASHBOARD-002-T01-implementation.md` | 范围、结果与未交付项 |
| 新建 | `.factory/workitems/PM-DASHBOARD-002/reviews/PM-DASHBOARD-002-T01-review-input.md` | 独立任务评审输入 |
| 新建 | `.factory/workitems/PM-DASHBOARD-002/ledger.jsonl` | 仅记录本工作项状态 |

## 边界

- 层级：只改 skill/reference/template/test，不引入 `src/` 依赖。
- 领域：`WF-CTL-010` 项目状态与交付看板。
- 接口 owner：`using-shanforge` 定义意图与交接；固定 renderer 定义事实 slot；模板只消费 slot。
- 下游依赖：未来 `ProjectProgressSnapshot/v2`、`AuthorizedProgressSnapshot/v1`、`RenderManifest/v2` 和 `ReconciliationResult/v2` 实现。
- 禁止耦合：模板不得读取 ledger/Markdown/JSONL/网络，不得写项目事实；AI 不计算或拼装事实看板。

## 稳定 slot 与页面合同

### 总览 slot

| 分组 | 精确 slot |
|---|---|
| 身份与资格 | `PROJECT_NAME`、`PROJECT_ID`、`STAGE_NAME`、`AS_OF_H`、`AS_OF_TIME`、`PROJECT_TIMEZONE`、`VALIDATION_STATUS`、`VALIDATION_MESSAGE` |
| 快照绑定 | `SNAPSHOT_ID`、`SNAPSHOT_SHA256_SHORT`、`SOURCE_ROOT_SHA256_SHORT`、`AUTHORIZATION_DIGEST_SHORT`、`RULE_VERSION`、`RENDER_DISPOSITION` |
| 核心指标 | `TOTAL_TASKS`、`COMPLETED_TASKS`、`COMPLETION_RATE`、`ACTIVE_TASKS`、`PENDING_APPROVALS`、`BLOCKED_OR_OVERDUE_TASKS`、`DEPLOYED_DELIVERABLES` |
| 状态分布 | `STATUS_DISTRIBUTION_SEGMENTS`、`STATUS_DISTRIBUTION_LEGEND` |
| 六类摘要 | `ACTIVE_SUMMARY`、`APPROVAL_SUMMARY`、`RECENT_COMPLETION_SUMMARY`、`DEPLOYMENT_SUMMARY`、`BLOCKED_OVERDUE_SUMMARY`、`NEXT_MILESTONE_SUMMARY` |
| 错误与权限 | `ERROR_CODE`、`AFFECTED_PATHS`、`RECOVERY_ACTION`、`REDACTION_NOTICE`、`OVERVIEW_DETAIL_ROWS` |

`RENDER_DISPOSITION` 只允许 `FULL`、`PARTIAL`、`ERROR_ONLY`：

- `FULL`：展示全部获授权业务区。
- `PARTIAL`：只用于 `incomplete` 且正式验证合同明确允许展示部分字段的情形；展示缺失和脱敏说明，但不得容纳 `conflict`。
- `ERROR_ONLY`：CSS 隐藏全部 `.business-content`；代码只可填充身份、截止点、验证、错误码、受影响路径和恢复动作，源码中不得出现旧业务值。

`VALIDATION_STATUS=conflict|stale|failed` 必须进入 `ERROR_ONLY`。正常业务看板中的每个 `*_CONFLICT_COUNT` 只能是规范化十进制 `0`；非零表示快照资格冲突，必须关闭业务输出而不是把冲突详情混入 `PARTIAL`。

### slot 类型与转义

| 类型 | slot | 生成与转义规则 |
|---|---|---|
| `scalar_text` | 身份、时间、摘要、错误、权限、模块 `EMPTY_REASON` / `SOURCE_DIGEST_SHORT` | 固定 renderer 对原值做 HTML 文本节点转义后插入；禁止进入属性、URL、style 或 script 上下文 |
| `scalar_decimal` | H、七指标、模块 `COUNT` / `MISSING_COUNT` / `CONFLICT_COUNT` | 先由代码按规范化十进制定标，再按文本节点转义；模板和脚本不得重算 |
| `enum_token` | `VALIDATION_STATUS`、`RENDER_DISPOSITION` | renderer 先按封闭枚举校验，再分别写入文本节点和明确登记的 `data-*` 属性；禁止复用未校验字符串 |
| `render_fragment` | `STATUS_DISTRIBUTION_SEGMENTS`、`STATUS_DISTRIBUTION_LEGEND`、`OVERVIEW_DETAIL_ROWS`、十模块 `ROWS` / `SOURCE_DETAILS` | 只能由固定 renderer 从类型化 collection 逐项生成；每个业务值先按上下文转义；仅允许模板登记元素/属性，禁止 script、style、事件属性、任意 URL 或 AI/调用方原始 HTML |

`render_fragment` 不是调用方可传的 HTML 字符串。测试必须拒绝未登记 slot、原始 `<script>`、事件属性和 `javascript:` URL，并证明浏览器 fixture 只通过固定测试 renderer 生成片段。

### 十一页固定顺序

| 顺序 | 中文页名 | 固定 ID | slot 前缀 |
|---:|---|---|---|
| 0 | 项目总览 | `page-overview` | `OVERVIEW_*` |
| 1 | 项目成员 | `module-team` | `TEAM_*` |
| 2 | 项目策划 | `module-charter` | `CHARTER_*` |
| 3 | WBS | `module-wbs` | `WBS_*` |
| 4 | 进度计划 | `module-schedule` | `SCHEDULE_*` |
| 5 | 风险管理 | `module-risks` | `RISKS_*` |
| 6 | 沟通计划 | `module-communications` | `COMMUNICATIONS_*` |
| 7 | 会议与行动 | `module-meetings` | `MEETINGS_*` |
| 8 | 状态报告 | `module-status-reports` | `STATUS_REPORTS_*` |
| 9 | 变更管理 | `module-changes` | `CHANGES_*` |
| 10 | 项目总结 | `module-closure` | `CLOSURE_*` |

每个业务模块前缀必须提供精确后缀：`COUNT`、`MISSING_COUNT`、`CONFLICT_COUNT`、`AS_OF_TIME`、`SOURCE_DIGEST_SHORT`、`EMPTY_REASON`、`ROWS`、`SOURCE_DETAILS`。模板固定列头与只读控件；renderer 只插入已转义内容和机器排序键。

## 任务 1：Excel 十模块项目状态查看契约

### 任务切片

- 设计方案：首屏只放身份/截止点、七指标、互斥分布和六类一行摘要；目录和最多五项明细从首屏下方开始。
- 接口设计：只允许本计划登记的 slot，全部来自同一 `AuthorizedProgressSnapshot/v1`；不得临场增加同义 slot。
- UI：浅色高对比企业驾驶舱；键盘焦点、skip link、语义化 heading/nav/table/details、320–1440px 响应式和 `prefers-reduced-motion`。
- 交互：内联控制器只做预渲染行的文本筛选、`data-sort-value` 稳定排序和 `<details>` 来源展开；不调用网络、不读取源文件、不派生事实。
- 测试设计：静态测试覆盖流程、slot、11 个唯一锚点及顺序、处置、权限、无网络/无事实写入和 AI 边界；浏览器测试覆盖 1440×900、1024×768、768×1024、390×844、320×568 的页面宽度、首屏边界、文本裁切、元素重叠、焦点、4.5:1 对比度、筛选、排序、来源展开及截图。
- review：独立 reviewer 核对正式需求覆盖、无第二事实源、实现边界和验证证据。

### 允许文件

- 修改：`skills/using-shanforge/SKILL.md`
- 修改：`skills/using-shanforge/references/pm-dashboard-rendering.md`
- 修改：`skills/using-shanforge/references/status-dashboard-template.html`
- 新建：`tests/test_pm_dashboard_template_contract.py`
- 新建：`tests/test_pm_dashboard_template_browser.py`
- 新建/修改：`.factory/workitems/PM-DASHBOARD-002/`

### 执行清单

- [x] **Preflight：** 三份目标文件开始时无任务外冲突；全工作区快照输出因超长截断，最终范围以实际 apply-patch 写集、允许路径 status/diff 和精确暂存清单复核。
- [x] **红灯：** 同一套件初始 14 failed，exit 1，原因符合旧模板合同缺口。
- [x] **绿灯：** 更新 skill、reference 和模板；只实现精确 slot 与受限只读交互。
- [x] **定向验证：** 23 项合同/安全/浏览器测试通过；5 视口、3 类交互和 5 张截图通过。
- [x] **相邻回归：** PM 控制面/project-memory 11 passed；完整会话路由/project status response 42 passed。
- [x] **范围检查：** 允许路径 `git diff --check` exit 0；提交仅取本任务文件和 memory 的任务专属 hunk。
- [x] **证据：** evidence、report、review input、work item ledger 和最小 memory 索引已写入。
- [x] **评审门：** 独立 reviewer `approved / 99 / C0-I0-M0`。

## 验证命令与期望

红灯：

```bash
uv run pytest tests/test_pm_dashboard_template_contract.py tests/test_pm_dashboard_template_browser.py -q
```

期望：至少 8 项静态失败，浏览器用例因旧模板缺 DOM/交互失败；不得因未收集或 skip 冒充红灯。

绿灯和浏览器证据：

```bash
uv run pytest tests/test_pm_dashboard_template_contract.py -q
PM_DASHBOARD_SCREENSHOT_DIR=.factory/workitems/PM-DASHBOARD-002/evidence/screenshots uv run pytest tests/test_pm_dashboard_template_browser.py -q
```

期望：静态契约不少于 8 项全部通过；浏览器 5 个视口、3 类交互全部通过，生成 5 张截图。找不到受支持 Chrome 时状态为 `blocked`，不得 skip。

Chrome 发现顺序：任务专用 `SHANFORGE_CHROME_BIN`、`google-chrome`、`google-chrome-stable`、`chromium`、`chromium-browser`、macOS `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`。测试输出被选路径和版本；全部缺失时以包含候选路径的错误失败。

截图有效性：浏览器测试断言每张 PNG 尺寸与目标视口一致、文件非空；验证阶段再使用工作区依赖 Python 的 Pillow 计算每张截图至少包含两种颜色且通道极差大于 16，并由独立 reviewer 查看至少桌面 1440、会话 768 和移动 320 三张截图的首屏关键区。

相邻回归：

```bash
uv run pytest tests/test_project_management_control_plane.py tests/test_project_memory_skill.py -q
uv run pytest tests/test_full_project_session_workflow_routing.py tests/test_project_control_response.py -q
```

期望：两组全绿，测试数量和 exit code 写入 evidence。

## 测试策略

- 红灯：至少 8 个契约失败，覆盖固定 H、完整 slot、十模块顺序、错误处置、权限、AI/代码边界和交互。
- 绿灯：静态契约不少于 8 项全绿。
- 浏览器：固定 fixture 五视口断言 `scrollWidth <= innerWidth + 1`、首屏在视口内、文本不裁切、关键元素重叠不超过 1px、焦点轮廓可见、文本对比度至少 4.5:1，并验证筛选、排序、来源展开。
- 定向回归：PM 控制面与 project-memory。
- 邻近回归：完整会话路由与 project status response。
- 全量回归：不运行；工作区存在大量其他任务改动，本变更只触及 skill/reference/template。
- 未运行：生产 `ProjectProgressSnapshot/v2` → HTML/XLSX 跨格式 E2E 和 137 字段性能基准；生产 renderer 尚未实现，本任务不伪造交付。

## 文档、记忆与提交

- 正式文档：不修改；现有 PRD/设计已批准目标合同。
- memory：现有文件含其他任务脏改动，本任务不直接同步；在 report/ledger 记录并交流程总控处理。
- work item：只写 `.factory/workitems/PM-DASHBOARD-002/`。
- 提交：独立 review、验证和范围检查后只提交允许路径；不包含其他工作区改动。

## 评审门

- 计划评审：`approved / 97`
- 任务评审：`approved / 99`
- 验证：`passed`
- 提交：`ready`
- 记忆同步：`completed_with_task_only_hunks`

## 计划自审

- 规格覆盖：Excel 十模块、首屏总览、同快照、代码渲染、AI 边界、权限、失败关闭、只读交互和五视口。
- 占位符：所有 slot 已精确登记，不允许额外同义 slot。
- 测试：静态、浏览器、定向、邻近和未运行项均有命令与可观察结果。
- UI：非 N/A；可访问性和响应式有真实浏览器证据。
- 可构建性：无依赖安装；使用系统 Chrome。缺 Chrome 明确阻断。
- 工作区隔离：执行前目标冲突检查，执行后允许路径 diff 检查。
- Shanforge 门禁：evidence、review、ledger、memory 安全检查和提交边界齐备。
