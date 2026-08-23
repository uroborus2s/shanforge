# PM-DASHBOARD-005 第七轮显式路线树与紧凑任务看板修复计划

> 第七轮三个根因已由用户确认。本计划是执行候选，只有修复方案获得人工批准后才能修改
> 生成器、测试、渲染合同、主线计划和生成缓存。

**目标：** 用显式 `parent_id` 路线树支持任意层级下钻，并让当前工作看板只展示负责人
范围内的任务，不再以稀疏六列矩阵和重复任务卡掩盖真实进度。

**架构：** 继续使用现有 Markdown、TaskCard 和 ledger 作为事实源。`plan.md` 的
`## Work Breakdown` 改为 `id / parent_id / title / status` 节点表，行顺序决定同级顺序，
空 `parent_id` 表示根节点；标准库脚本校验后递归生成页面。看板复用现有负责人
`visible_work_items` 范围，六种状态只在顶部汇总一次，业务分组内只渲染实际存在的状态段。

**技术栈：** Python 标准库、原生 HTML/CSS、Markdown 事实文件、pytest、Ruff。

**工作项：** `PM-DASHBOARD-005`

**任务：** `PM-DASHBOARD-005-T01`

**状态：** `approved_pending_human_ui_acceptance`

---

## 第七轮输入

- 已确认需求：`brief.md` 中 `REQ-PM-SNAPSHOT-003`、`005`、`007`
- 当前任务简报：`task-briefs/PM-DASHBOARD-005-T01.md`
- 第七轮反馈：`reviews/review-feedback-triage-7.md`
- 已确认根因：`reports/PM-DASHBOARD-005-T01-round-7-root-cause.md`
- 复现证据：`evidence/PM-DASHBOARD-005-T01-round-7-root-cause-evidence.md`
- 当前主线计划：`.factory/workitems/ENTERPRISE-AI-DELIVERY-001/plan.md`
- 当前生成器：`skills/using-shanforge/scripts/project_snapshot.py`
- 渲染合同：`skills/using-shanforge/references/pm-dashboard-rendering.md`

## 第七轮验收口径

1. `## Work Breakdown` 的唯一结构输入是一张四列表：
   `id | parent_id | title | status`；不得再从 H3–H6 推断父子关系。
2. 空 `parent_id` 表示根节点；任意节点可引用任意深度的已登记父节点。同父节点按表格
   行顺序显示，不新增 `order` 字段。
3. 重复 ID、缺失父节点、自引用和父链循环必须让快照生成返回失败 receipt；不得静默丢弃、
   自动重挂或继续生成部分路线。
4. 测试 fixture 至少包含 7 层路线；每个节点都生成自己的 `stages/<NODE-ID>.html`，
   节点页显示直接子节点、全部后代计数和继续下钻入口，深度不受 Markdown H6 限制。
5. 当前工作页不再渲染一套任务摘要卡后又在看板重复同一任务；摘要只说明当前负责人范围、
   主线 Gate 和任务数量，任务详情只由看板承载。
6. 看板任务集合只来自 `visible_work_items`：产品主线和当前选中的一个并行工作项。
   其他活动技术工作进入“未纳入当前会话 / 后续工作”，不得混入主板。
7. 六种状态保留为统一状态语义，并在看板顶部汇总一次；每个需求/工作项折叠面板内只渲染
   该组实际存在的状态段，不生成空状态单元。
8. 分组标题提供需求或计划入口和 `完成数 / 总数`；任务行只显示标题、任务性质、专业类型、
   状态、下一步和详情入口，不重复主分组已经表达的需求关系。
9. 真实 Shanforge 主板中空状态单元为 `0`，同一任务卡重复为 `0`，负责人范围外的
   `SKILL-CLOSEOUT-001`、`STRATIX-SERVICE-GUIDE-001` 和
   `WRITING-PLANS-SIMPLE-GATE-001` 不进入主板。
10. 390×844 与 1440×900 均可完成“项目路线 → 节点页逐层下钻 → 任务/每日进展”和
    “业务分组 → 非空状态段 → 任务/需求详情”，无页面级横向溢出。

## 第七轮范围

### 目标

- 把路线父子关系从 Markdown 排版事实迁移为显式 `parent_id` 项目事实。
- 在一个共享解析入口校验节点唯一性、父节点完整性和无环性。
- 为每个路线节点生成同构详情页，继续使用现有递归渲染器，不增加深度特例。
- 让负责人摘要与任务看板共享同一工作项范围，并消除重复任务展示。
- 保留六种状态语义，删除每个业务组的固定六空格矩阵。

### 非目标

- 不增加 YAML/JSON 路线文件、SQLite 路线表或第二份路线事实。
- 不增加 `order`、依赖、日期、负责人、进度权重或拖拽编辑。
- 不新增 JavaScript、数据库、前端框架或第三方依赖。
- 不改变 EAD T03 客户确认 Gate，不启动 T04/T05。
- 不修改其他工作项事实，不提交、Push、PR、Merge、部署或关闭任务。

## 第七轮文件

| 类型 | 路径 | 职责 |
|---|---|---|
| 修改 | `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/plan.md` | 把现有 H3–H4 路线迁移为显式 `parent_id` 节点表 |
| 修改 | `skills/using-shanforge/scripts/project_snapshot.py` | 解析和校验显式树；生成全部节点页；统一看板范围；生成紧凑非空状态段 |
| 修改 | `skills/using-shanforge/references/pm-dashboard-rendering.md` | 固化路线节点表、失败规则和紧凑看板合同 |
| 测试 | `tests/test_using_shanforge_snapshot.py` | 覆盖任意深度、非法树、看板范围、空单元和重复任务 |
| 生成 | `.factory/cache/site/current/**` | 重建路线、当前工作、任务和计划详情页面 |
| 状态 | `.factory/workitems/PM-DASHBOARD-005/**` | 第七轮证据、报告、评审和 ledger |
| 记忆 | `.factory/memory/tasks.summary.md`、`.factory/memory/tests.summary.md`、`.factory/memory/review-ledger.jsonl` | 同步压缩事实 |

## 第七轮边界

- 层级：路线 schema 与只读 PM 投影，不改变产品业务需求和工作流状态机。
- 领域：`using-shanforge / project snapshot` 与
  `ENTERPRISE-AI-DELIVERY-001 / work breakdown`。
- 接口归属方：路线事实归主线 `plan.md`；解析、校验和 HTML 投影归
  `project_snapshot.py`。
- 下游依赖：`roadmap.html`、`plans/*.html`、每个节点对应的 `stages/*.html`、`tasks/*.html`、
  `work.html` 和缓存指纹。
- 禁止耦合：SQLite 权威索引、旧 `src/` runtime、客户端状态、绝对路径和第三方依赖。

## 任务：PM-DASHBOARD-005-T01 第七轮集成候选

本轮继续使用现有任务卡。路线 schema 和看板布局共享同一个快照生成器、真实页面验收和
用户 UI Gate，拆成多个任务卡只会增加重复状态，不增加独立交付价值。

### 任务切片

- 设计方案：四列 Markdown 节点表作为唯一路线结构；业务折叠面板内只显示非空状态段。
- 接口设计：`_plan_stages()` 返回
  `id/title/status/state/label/parent_id/children/depth`；`depth` 由显式父链派生，
  只用于展示，不作为父子关系来源。CLI receipt schema 保持不变。
- UI：每个路线节点进入自己的节点页，任务详情使用独立动作；六状态汇总条只出现一次，
  业务面板按实际状态分段，任务使用分隔线，不增加卡片层。
- 测试设计：锁定 7 层树、逐节点独立页面、非法父链 fail-closed、根节点识别、负责人
  范围、零空单元、零重复任务和双视口路径。
- 开发：复用 `_route_tree()`、`visible_work_items`、`BOARD_COLUMNS` 和现有
  `<details>/<summary>`；删除固定六列头、跳转和空单元分支。
- 单测：只修改聚焦快照合同测试。
- review：实现者只能进入 `ready_for_review`，由独立 reviewer 检查 schema 迁移、
  页面信息架构和真实生成结果。
- 集成测试：真实快照双生成、链接闭包、缓存命中、桌面和移动浏览器路径。
- 失败断言：任一父子关系仍来自标题深度、非法树仍生成成功、空状态单元非零、任务重复、
  范围外维护任务进入主板或移动端横向溢出即失败。

### 允许文件

- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/plan.md`
- `skills/using-shanforge/scripts/project_snapshot.py`
- `skills/using-shanforge/references/pm-dashboard-rendering.md`
- `tests/test_using_shanforge_snapshot.py`
- `.factory/workitems/PM-DASHBOARD-005/brief.md`
- `.factory/workitems/PM-DASHBOARD-005/plan.md`
- `.factory/workitems/PM-DASHBOARD-005/task-briefs/PM-DASHBOARD-005-T01.md`
- `.factory/workitems/PM-DASHBOARD-005/evidence/PM-DASHBOARD-005-T01-round-7-root-cause-evidence.md`
- `.factory/workitems/PM-DASHBOARD-005/evidence/PM-DASHBOARD-005-T01-round-7-plan-review-fix-verification.md`
- `.factory/workitems/PM-DASHBOARD-005/evidence/PM-DASHBOARD-005-T01-round-7-verification.md`
- `.factory/workitems/PM-DASHBOARD-005/reports/PM-DASHBOARD-005-T01-round-7-root-cause.md`
- `.factory/workitems/PM-DASHBOARD-005/reports/PM-DASHBOARD-005-T01-round-7-plan-review-fix.md`
- `.factory/workitems/PM-DASHBOARD-005/reports/PM-DASHBOARD-005-T01-round-7-implementation.md`
- `.factory/workitems/PM-DASHBOARD-005/reviews/review-feedback-triage-7.md`
- `.factory/workitems/PM-DASHBOARD-005/reviews/PM-DASHBOARD-005-T01-round-7-fix-plan-review.md`
- `.factory/workitems/PM-DASHBOARD-005/reviews/PM-DASHBOARD-005-T01-round-7-plan-review-feedback-triage.md`
- `.factory/workitems/PM-DASHBOARD-005/reviews/PM-DASHBOARD-005-T01-round-7-plan-review-response.md`
- `.factory/workitems/PM-DASHBOARD-005/reviews/PM-DASHBOARD-005-T01-round-7-review-input.md`
- `.factory/workitems/PM-DASHBOARD-005/reviews/PM-DASHBOARD-005-T01-round-7-independent-review.md`
- `.factory/workitems/PM-DASHBOARD-005/ledger.jsonl`
- `.factory/cache/site/current/**`
- `.factory/memory/agent-session.md`
- `.factory/memory/tasks.summary.md`
- `.factory/memory/tests.summary.md`
- `.factory/memory/review-ledger.jsonl`

### 禁止文件与动作

- 其他 work item 的 brief、task brief、ledger、evidence、report 和 review。
- `docs/**`、`src/**`、依赖文件和包配置。
- 用户已有且不属于本任务的工作区或暂存区改动。
- 提交、Push、PR、Merge、部署、关闭任务和 EAD T04/T05 启动。

### 步骤 0：冻结全仓失败集合前像

- [x] 在修改源文件和测试前运行一次全仓 pytest。
- [x] 把 pytest summary 中 7 个失败 node ID 原样登记到 round-7 verification evidence 的
  `pre_change_failed_nodeids`；不得只记录失败数量。
- [x] 记录真实 exit code。当前基线为 `1`，因为存在 7 项范围外失败；若失败数量或
  node ID 与上一轮不符，先调查漂移，不进入 Red。

运行：

```bash
uv run pytest -q
```

期望：exit code `1`，`217 passed / 7 failed`；evidence 保存 7 个精确失败 node ID。

### 步骤 1：显式路线树红灯

- [x] 把 fixture 的 `## Work Breakdown` 改为四列节点表，并登记 7 层父链。
- [x] 断言解析结果完全服从 `parent_id`，Markdown 标题不再产生路线节点。
- [x] 断言根节点由空 `parent_id` 识别，后代 `depth` 和 `children` 正确。
- [x] 断言 7 层树的每个节点都有独立页面，父页的直接子节点链接进入各自页面。
- [x] 用一个测试方法的子用例覆盖重复 ID、孤儿父节点、自引用和循环父链。
- [x] 断言非法路线让 CLI 返回 `status=failed` 和可定位错误，不写部分新页面。

运行：

```bash
uv run pytest tests/test_using_shanforge_snapshot.py::ProjectSnapshotTest::test_plan_stages_use_explicit_parent_ids_at_arbitrary_depth tests/test_using_shanforge_snapshot.py::ProjectSnapshotTest::test_invalid_route_tree_fails_closed -q
```

期望：新增断言失败，失败点命中当前 H3–H6 解析和缺少图校验。

### 步骤 2：显式路线树绿灯与真实计划迁移

- [x] 在 `_plan_stages()` 中解析四列表，先收集全部节点，再校验唯一 ID、父节点、自引用和
  循环，最后按行顺序建立 `children` 并派生 `depth`。
- [x] 让非法表抛出 `SnapshotError`，复用现有 CLI 失败 receipt，不新增错误框架。
- [x] 把根节点选择、任务所属根阶段和阶段页生成从 `level == 3` 改为
  `parent_id is None`。
- [x] 为全部路线节点生成 `stages/<NODE-ID>.html`；节点标题进入节点页，匹配 TaskCard
  时另给“查看任务详情”操作，不能让任务链接替代节点下钻。
- [x] 把 EAD 现有 32 个路线节点原样迁移为节点表，标题和状态不变，根节点
  `parent_id` 为空，原 H4 节点指向对应根节点。
- [x] 更新渲染合同，删除 H3–H6 作为路线权威的描述。

运行：

```bash
uv run pytest tests/test_using_shanforge_snapshot.py -q
uv run ruff check skills/using-shanforge/scripts/project_snapshot.py tests/test_using_shanforge_snapshot.py
uv run ruff format --check skills/using-shanforge/scripts/project_snapshot.py tests/test_using_shanforge_snapshot.py
```

期望：任意深度、非法树、阶段页、任务路线和既有快照测试全部通过，Ruff 通过。

### 步骤 3：紧凑看板红灯

- [x] fixture 登记产品主线、一个当前并行工作项和三个范围外活动维护工作项。
- [x] 断言主板只包含前两个 `visible_work_items` 的任务。
- [x] 断言上方不再生成 `lane-card-link` 任务卡，任务只在主板出现一次。
- [x] 断言六状态汇总只生成一次，业务组只生成非空状态段，空状态单元为零。
- [x] 断言主需求只在分组标题出现，卡内不重复 `board-card__relations`。
- [x] 断言有正式计划的工作项分组标题包含 `plans/<WORKITEM-ID>.html`；无正式计划时包含
  当前任务 `tasks/<TASK-ROUTE>.html`，不得输出纯文本死标题。

运行：

```bash
uv run pytest tests/test_using_shanforge_snapshot.py::ProjectSnapshotTest::test_snapshot_renders_compact_scoped_board_without_duplicate_tasks -q
```

期望：新增断言失败，失败点命中全部活动工作项取数、重复摘要卡和固定六列渲染。

### 步骤 4：紧凑看板绿灯

- [x] 用 `visible_work_items` 直接构造 `board_tasks`，删除第二套 `board_items` 取数。
- [x] 把工作页上方 `lane-grid` 替换为负责人范围摘要，只显示主线 Gate、并行范围和计数，
  不再生成逐任务卡。
- [x] 六状态汇总条复用 `BOARD_COLUMNS` 并各显示一次总数。
- [x] `_grouped_board_cards()` 仍按唯一主需求或工作项生成原生折叠面板，但只遍历该组
  实际存在的状态，顺序服从 `BOARD_COLUMNS`。
- [x] 在任务投影中增加 `work_item_has_plan`；工作项分组有计划时链接
  `plans/<WORKITEM-ID>.html`，无计划时选 `is_current` 任务、否则选组内第一项，
  链接其 `tasks/<TASK-ROUTE>.html`。
- [x] 删除 `board-status-head`、`board-jumps`、`empty-cell` 和固定六列 CSS；非空状态段
  使用自适应 Grid，移动端单列。
- [x] 卡内保留状态、任务性质、专业类型、下一步和详情；主分组已是需求时不再重复需求链。

运行：

```bash
uv run pytest tests/test_using_shanforge_snapshot.py -q
uv run ruff check skills/using-shanforge/scripts/project_snapshot.py tests/test_using_shanforge_snapshot.py
uv run ruff format --check skills/using-shanforge/scripts/project_snapshot.py tests/test_using_shanforge_snapshot.py
```

期望：范围、去重、非空状态段、详情链接、移动单列和既有负责人页面合同全部通过。

### 步骤 5：真实生成与结构验收

- [x] 连续运行两次真实快照；第二次必须 `cache_hit=true` 且 generation id 相同。
- [x] 核实 EAD 32 个路线节点全部存在，根节点 5 个，任意节点父关系与表格一致。
- [x] 核实 `roadmap.html`、32 个路线节点页、任务页和计划页链接闭包。
- [x] 核实主板空状态单元为 0、重复任务卡为 0、六状态汇总为 1。
- [x] 核实范围外三个维护工作项不进入主板，但仍可在后续工作或审计入口找到。

运行：

```bash
uv run python skills/using-shanforge/scripts/project_snapshot.py --project-root . --relative-paths
uv run python skills/using-shanforge/scripts/project_snapshot.py --project-root . --relative-paths
```

期望：两次生成成功、第二次缓存命中、链接和结构计数符合本节断言。

### 步骤 6：桌面与移动验收

- [x] 1440×900：六状态汇总只出现一次；业务面板没有空状态格；任务标题和下一步成为主视觉。
- [x] 390×844：业务面板和非空状态段单列；无嵌套窄卡和页面级横向滚动。
- [x] 自动化 fixture 证明 7 层节点页逐级可达；真实浏览器从 EAD 根节点进入直接子节点，
  再进入任务和每日进展。
- [x] 键盘可聚焦页首导航、状态汇总、业务折叠、任务、需求和路线链接。
- [x] 控制台错误为 0；保存两条核心路径截图和浏览器检查记录。

### 步骤 7：证据、评审和记忆

- [x] 写 `evidence/PM-DASHBOARD-005-T01-round-7-verification.md`。
- [x] 写 `reports/PM-DASHBOARD-005-T01-round-7-implementation.md`。
- [x] 更新任务简报、工作项 ledger、review ledger、测试摘要和任务摘要。
- [x] 生成第七轮独立评审输入包。
- [x] 实现者最高状态为 `ready_for_review`；独立评审后仍需用户 UI 验收。

## 第七轮测试策略

- 红灯：任意深度/非法父链与看板范围/稀疏结构各有独立失败断言。
- 绿灯：聚焦快照测试和 Ruff。
- 定向回归：路线解析、阶段页、计划页、任务页、当前工作、需求页和返回路径。
- 邻近回归：真实双生成、链接闭包、缓存命中和输入指纹。
- 全量回归：独立实现评审前运行，与当前 `217 passed / 7 known out-of-scope failures`
  基线比较；命令为 `uv run pytest -q`。允许 exit code `1` 的唯一条件是
  `post_change_failed_nodeids == pre_change_failed_nodeids` 且仍为 7 项；新增或消失的
  failure 都先调查，不用数量相同代替身份相同。
- 浏览器验收：390×844 和 1440×900 两条真实交互路径；未运行不得写成通过。

## 第七轮文档与状态同步

- 正式渲染合同：`skills/using-shanforge/references/pm-dashboard-rendering.md`
- 主线路线事实：`.factory/workitems/ENTERPRISE-AI-DELIVERY-001/plan.md`
- 工作项事实：`.factory/workitems/PM-DASHBOARD-005/`
- 压缩记忆：`.factory/memory/agent-session.md`、`.factory/memory/tasks.summary.md`、
  `.factory/memory/tests.summary.md`
- HTML：只作为可重建投影，不作为正式事实源。

## 第七轮评审门

- 根因确认：`approved`
- 计划自审：`passed`
- 独立计划评审：`approved_98_C0_I0_M0`
- 修复方案人工确认：`approved`
- 实现授权：`true`
- 实现与验证：`approved`
- 独立任务评审：`approved_99_C0_I0_M0`
- 用户 UI 验收：`pending`
- 提交：`blocked_until_user_ui_acceptance`

## 第七轮计划自审

- 规格覆盖：覆盖显式 `parent_id`、任意深度、非法树阻断、紧凑非空状态段、统一负责人
  范围和零重复任务。
- 占位符扫描：没有未定义文件、函数、数据字段或泛化实施步骤。
- 类型一致性：节点输入四字段、派生 `depth/children`、负责人范围和六状态语义均唯一。
- 可构建性：写入路径、Red/Green 命令、失败点、迁移数量和真实页面断言明确。
- UI 完整性：桌面、移动、键盘、空态、详情、返回和真实视觉验收均有口径。
- Shanforge 门禁：根因已确认；实现、提交和关闭仍受修复方案批准及用户 UI 验收限制。

## 第六轮执行历史

## 输入

- 已确认需求：`brief.md` 中 `REQ-PM-SNAPSHOT-003`、`005`、`007`
- 当前任务简报：`task-briefs/PM-DASHBOARD-005-T01.md`
- 第六轮反馈：`reviews/review-feedback-triage-6.md`
- 已确认根因：`reports/PM-DASHBOARD-005-T01-round-6-root-cause.md`
- 复现证据：`evidence/PM-DASHBOARD-005-T01-round-6-root-cause-evidence.md`
- 设计候选：`reports/PM-DASHBOARD-005-T01-round-6-fix-design.md`
- 当前主线计划：`.factory/workitems/ENTERPRISE-AI-DELIVERY-001/plan.md`
- 渲染合同：`skills/using-shanforge/references/pm-dashboard-rendering.md`

## 拟议验收口径

1. 顶部 5 个阶段分别进入 5 个不同的 `stages/<STAGE-ID>.html`，不得再以同一计划页
   fragment 代替下钻。
2. 路线解析只读取 `## Work Breakdown` 中 `###` 至 `######` 的稳定 ID 标题，并保留
   `level`、`parent_id`、显式状态和子节点；正文项目符号不得自动冒充步骤。
3. 每个阶段页只显示该阶段的摘要和子树。Shanforge 当前 03 阶段显示 8 个直接子步骤：
   7 个完成、1 个当前；其他阶段按已登记计划显示真实数量。
4. 节点 ID 匹配真实 TaskCard 时可进入任务详情和每日 ledger；普通步骤不生成空详情页。
5. 主敏捷看板只包含当前产品主线、活动/需关注的并行工作项及这些工作项的兄弟任务；
   已关闭或已替代工作项的历史终态任务下沉“历史完成”。
6. 一条需求或工作项形成一条横跨六个状态的业务泳道；状态决定任务位置，任务性质和专业
   类型只作为标签。
7. 主板任务行只保留任务名、标签、一行下一动作和详情操作，不再输出目标、需求和下一步
   三段长正文。
8. 390×844 与 1440×900 下能够完成“总路线 → 03 阶段 → 03 任务 → 每日进展”和
   “需求泳道 → 状态任务 → 任务/需求详情”两条路径，无页面级横向溢出。

## 范围

### 目标

- 把路线图的数据合同从平级阶段升级为显式 Markdown 层级。
- 为每个主阶段生成独立阶段详情页和稳定返回路径。
- 用业务泳道统一需求/工作项分组与六列状态。
- 从主板移除无关历史终态，保留活动工作项内有上下文价值的完成任务。
- 更新真实 Shanforge 主线计划，使 5 个阶段都具有来源明确的直接子步骤。

### 非目标

- 不提供在线编辑、拖拽、客户端筛选状态或用户账号。
- 不新增数据库、JavaScript、前端框架、第三方包或第二份路线事实。
- 不为普通路线步骤创建空 TaskCard 或空详情页。
- 不改变 T03 客户确认 Gate，不启动 T04/T05，不补造负责人、日期或完成率。
- 不修改其他工作项 ledger、task brief、报告或终态。
- 不提交、Push、PR、Merge 或部署；用户 UI 验收前不得关闭任务。

## 文件

| 类型 | 路径 | 职责 |
|---|---|---|
| 修改 | `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/plan.md` | 为 5 个真实主阶段登记来源明确的 H4 子步骤和显式状态 |
| 修改 | `skills/using-shanforge/scripts/project_snapshot.py` | 解析路线树、生成阶段页、投影活动范围和业务泳道 |
| 修改 | `skills/using-shanforge/references/pm-dashboard-rendering.md` | 固化层级事实、阶段页面、主板范围和泳道合同 |
| 测试 | `tests/test_using_shanforge_snapshot.py` | 覆盖路线树、独立页面、当前范围、历史下沉和泳道结构 |
| 生成 | `.factory/cache/site/current/stages/*.html` | 可删除重建的阶段详情页 |
| 生成 | `.factory/cache/site/current/{roadmap,work}.html` | 可删除重建的负责人页面 |
| 状态 | `.factory/workitems/PM-DASHBOARD-005/**` | 计划、证据、报告、评审和 ledger |
| 记忆 | `.factory/memory/tasks.summary.md`、`.factory/memory/tests.summary.md`、`.factory/memory/review-ledger.jsonl` | 同步压缩事实 |

## 边界

- 层级：只修改正式主线计划的路线拆分和只读 PM 投影，不改变产品需求或 T03 决策结果。
- 领域：`using-shanforge / project snapshot` 与
  `ENTERPRISE-AI-DELIVERY-001 / work breakdown`。
- 接口归属方：路线事实归主线 `plan.md`；页面解析与生成归 `project_snapshot.py`。
- 下游依赖：`roadmap.html`、`stages/*.html`、`work.html`、`tasks/*.html` 和缓存指纹。
- 禁止耦合：SQLite 权威事实、旧 `src/` runtime、客户端状态、绝对路径和第三方前端依赖。

## 任务：PM-DASHBOARD-005-T01 第六轮集成候选

本任务只交付一套可共同验收的负责人页面候选；路线图与看板共享同一快照事实读取链和同一个
用户 UI Gate，不再创建一组只为流程存在的子任务卡。

### 任务切片

- 设计方案：使用 Markdown 标题层级表达路线；需求/工作项作为跨状态业务泳道。
- 接口设计：把 `_plan_stages()` 收敛为只解析 `Work Breakdown` 的路线树，节点字段固定为
  `id/title/status/state/level/parent_id/children`；不改变 CLI 和 receipt schema。
- UI：独立阶段页、面包屑、路线树、任务链接；桌面六列泳道、移动纵向状态分区、历史折叠。
- 测试设计：分别锁定不同页面身份、树关系、03 真实计数、当前任务范围、历史排除、
  六状态泳道、紧凑任务行和双视口可操作路径。
- 开发：只修改现有标准库生成器和相邻 CSS；不增加 helper，除非同一树遍历在解析、
  计数和渲染三处重复。
- 单测：聚焦快照合同测试文件。
- review：实现后生成代码、事实和页面评审输入包，由独立 reviewer 复核。
- 集成测试：真实快照双生成、页面链接闭包、桌面/移动浏览器交互。
- 失败断言：任一阶段仍指向同一计划页 fragment、03 无独立子树、历史终态进入主板、
  需求组不能跨六状态或任务行恢复长卡片即失败。

### 允许文件

- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/plan.md`
- `skills/using-shanforge/scripts/project_snapshot.py`
- `skills/using-shanforge/references/pm-dashboard-rendering.md`
- `tests/test_using_shanforge_snapshot.py`
- `.factory/workitems/PM-DASHBOARD-005/**`
- `.factory/cache/site/current/**`
- `.factory/memory/tasks.summary.md`
- `.factory/memory/tests.summary.md`
- `.factory/memory/review-ledger.jsonl`

### 禁止文件与动作

- 其他 work item 的 brief、task brief、ledger、evidence、report 和 review。
- `docs/**`、`src/**`、项目依赖和包配置。
- 用户已有且不属于本任务的工作区或暂存区改动。
- 提交、Push、PR、Merge、部署和 T04/T05 启动。

### 步骤 1：路线层级红灯

- [x] 在测试 fixture 的 `plan.md` 增加 H4/H5 路线节点。
- [x] 断言 `_plan_stages()` 当前无法返回父子关系。
- [x] 断言 5 个顶部 href 必须是 5 个不同的 `stages/*.html`。
- [x] 断言 03 页面只包含 03 子树和 8 个直接子步骤，不包含 01、02、04、05 的正文。
- [x] 断言匹配真实 TaskCard 的节点有任务链接，普通节点没有假链接。

运行：

```bash
uv run pytest tests/test_using_shanforge_snapshot.py -q
```

期望：新增路线层级断言失败，既有无关断言保持通过。

### 步骤 2：路线层级绿灯

- [x] 在 `ENTERPRISE-AI-DELIVERY-001/plan.md` 按设计候选登记
  `3 / 6 / 8 / 6 / 4` 个直接子步骤及显式状态。
- [x] 让 `_plan_stages()` 只在 `Work Breakdown` 范围解析 H3-H6，并用标题栈建立父子关系。
- [x] 为每个 H3 主阶段生成 `stages/<ID>.html`，总路线卡显示子步骤计数并进入对应页面。
- [x] 阶段页复用现有页面 shell、导航和 `_markdown()`；树节点使用原生列表或
  `details/summary`，精确匹配 TaskCard 时才链接任务详情。
- [x] 任务详情增加所属路线面包屑，保留现有每日 ledger。

运行：

```bash
uv run pytest tests/test_using_shanforge_snapshot.py -q
uv run ruff check skills/using-shanforge/scripts/project_snapshot.py tests/test_using_shanforge_snapshot.py
uv run ruff format --check skills/using-shanforge/scripts/project_snapshot.py tests/test_using_shanforge_snapshot.py
```

期望：路线层级测试、聚焦回归和 Ruff 全部通过。

### 步骤 3：业务泳道红灯

- [x] fixture 增加一个活动工作项、已完成兄弟任务、关闭历史工作项和多状态需求任务。
- [x] 断言活动工作项的相关任务进入主板，关闭历史工作项只进入历史折叠区。
- [x] 断言每个需求/工作项只生成一条业务泳道，泳道内部有六个状态分区。
- [x] 断言任务只在一个状态分区出现一次。
- [x] 断言主板任务不再输出 3 个 `<p>` 长段落。

运行：

```bash
uv run pytest tests/test_using_shanforge_snapshot.py -q
```

期望：新增主板范围和业务泳道断言失败，失败点命中当前状态优先分组实现。

### 步骤 4：业务泳道绿灯

- [x] 从 `visible_work_items` 的活动/关注项和产品主线确定主板 work item 集合。
- [x] 只把这些 work item 的任务交给新泳道渲染；其余终态任务计入“历史完成”折叠区。
- [x] 按唯一主需求或工作项建立业务泳道，再把任务放入六个状态分区。
- [x] 泳道摘要显示自然语言名称、需求/计划详情入口、任务总数和完成数。
- [x] 任务行只显示标题链接、性质/专业标签、一行下一动作和详情操作。
- [x] 桌面使用六列 Grid；移动端将非空状态分区纵向排列，空状态不占窄卡空间。

运行：

```bash
uv run pytest tests/test_using_shanforge_snapshot.py -q
uv run ruff check skills/using-shanforge/scripts/project_snapshot.py tests/test_using_shanforge_snapshot.py
uv run ruff format --check skills/using-shanforge/scripts/project_snapshot.py tests/test_using_shanforge_snapshot.py
```

期望：主板范围、泳道、紧凑任务行和现有导航/详情合同全部通过。

### 步骤 5：真实生成与页面闭包

- [x] 连续运行两次真实快照，第二次必须 `cache_hit=true` 且 generation id 相同。
- [x] 检查 `roadmap.html` 的 5 个阶段链接、5 个阶段文件及文件内任务链接全部存在。
- [x] 核实真实 03 页面为 `8` 个直接子步骤，状态为 `7 completed / 1 current`。
- [x] 核实主板不再包含 169 个历史终态任务；历史计数与源任务集合一致。
- [x] 核实每个主板任务只出现一次，需求/工作项泳道和六状态分区数量一致。

运行：

```bash
uv run python skills/using-shanforge/scripts/project_snapshot.py --project-root . --relative-paths
```

期望：两次生成成功、链接闭包成立、第二次缓存命中。

### 步骤 6：桌面与移动验收

- [ ] 1440×900：总路线 5 步可扫描，03 进入独立阶段页并逐层展开；业务泳道横跨六列。
- [ ] 390×844：03 路线、任务、返回路径可触控；泳道展开后状态纵向排列，无嵌套窄卡。
- [ ] 键盘可聚焦导航、阶段链接、折叠摘要、任务与需求详情。
- [ ] 页面级横向溢出为 0，控制台错误为 0。
- [ ] 保存两条核心路径截图和浏览器检查记录；无法运行的环境项必须明确写原因，不以静态
  DOM 代替视觉验收。

### 步骤 7：证据、评审和记忆

- [x] 写 `evidence/PM-DASHBOARD-005-T01-round-6-verification.md`。
- [x] 写 `reports/PM-DASHBOARD-005-T01-round-6-implementation.md`。
- [x] 更新渲染合同、任务简报、工作项 ledger、review ledger 和 memory 摘要。
- [x] 生成第六轮独立评审输入包。
- [x] 实现者最高状态为 `ready_for_review`；独立评审后仍需用户 UI 验收。

## 测试策略

- 红灯：路线身份/树关系和主板范围/泳道结构各有独立失败断言。
- 绿灯：聚焦快照测试文件和 Ruff。
- 定向回归：路线图、阶段页、任务页、当前工作、需求页、返回路径、终态归约。
- 邻近回归：真实双生成、链接闭包、缓存命中和 Markdown 输入指纹。
- 全量回归：独立评审前运行并与当前 `216 passed / 7 known out-of-scope failures` 基线比较。
- 浏览器验收：390×844 和 1440×900 两条真实交互路径；未运行不得写成通过。

## 文档与状态同步

- 正式渲染合同：`skills/using-shanforge/references/pm-dashboard-rendering.md`
- 主线路线事实：`.factory/workitems/ENTERPRISE-AI-DELIVERY-001/plan.md`
- 工作项事实：`.factory/workitems/PM-DASHBOARD-005/`
- 压缩记忆：`.factory/memory/tasks.summary.md`、`.factory/memory/tests.summary.md`
- HTML：只作为可重建投影，不作为项目事实提交。

## 评审门

- 根因确认：`approved`
- 计划自审：`passed`
- 修复方案人工确认：`approved`
- 实现授权：`true`
- 实现与验证：`ready_for_review`
- 独立任务评审：`approved_98_C0_I0_M0`
- 用户 UI 验收：`pending_human_confirmation`
- 提交：`blocked_until_user_ui_acceptance`

## 计划自审

- 规格覆盖：覆盖 `REQ-PM-SNAPSHOT-003`、`005`、`007` 及第六轮两个根因。
- 占位符扫描：没有“后续实现”“补充测试”或未定义文件/函数。
- 类型一致性：路线节点字段、页面路径、泳道维度和状态列均在前序设计中定义。
- 可构建性：每个写入路径、Red/Green 命令、失败点和期望结果明确。
- UI 完整性：桌面、移动、键盘、空态、返回和真实视觉验收均有口径。
- Shanforge 门禁：根因确认已发生；跨工作项主线计划写入和实现仍等待本修复方案批准。
