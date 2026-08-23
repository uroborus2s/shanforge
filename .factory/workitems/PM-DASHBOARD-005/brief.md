# PM-DASHBOARD-005：完整项目实时看板恢复

- 阶段：`IMPLEMENTATION`
- 状态：`in_progress`
- 用户目标：让项目负责人进入看板后，先按阶段看懂当前正在做什么，再按需求模块和任务类型理解任务关系，并能继续查看项目治理、质量和交付事实。
- 当前任务：`PM-DASHBOARD-005-T01`

## 需求

### REQ-PM-SNAPSHOT-001：完整项目快照

作为项目负责人，我希望每次打开同一个实时看板，都能看到项目总览、阶段位置、业务需求模块、分类任务、里程碑、风险、质量、交付物、追踪关系、版本变更和下一步，以便不阅读内部日志也能判断项目做到哪里、为什么做以及谁需要采取什么行动。

### REQ-PM-SNAPSHOT-002：技术文档快速入口

作为半途接手的项目负责人或技术负责人，我希望从看板快速打开需求、设计、开发、测试、发布与运维文档，以便先理解当前结论，再按需回到正式技术事实。

### REQ-PM-SNAPSHOT-003：可操作的敏捷任务看板

作为项目负责人，我希望当前工作页使用“待开始、进行中、测试中、待评审、待确认 /
阻塞、已完成”六种状态的敏捷任务看板，并能点击任务进入详情、点击关联需求进入需求详情，
以便从状态判断继续动作并追溯业务原因；六种状态只汇总一次，业务分组内不生成空状态格。

### REQ-PM-SNAPSHOT-004：项目接手说明与可读文档

作为半途接手的负责人，我希望首页先说明项目是什么、解决什么问题、最终交付什么、当前主线计划和真实进度，并在站内阅读渲染后的正式文档，以便不用查看 Markdown 源码或机器 ID 也能理解项目。

### REQ-PM-SNAPSHOT-005：按需求分组和按任务分类

作为项目负责人，我希望任务先按正式需求或项目工作项分组；组内使用项目任务、需求任务、
跨领域任务和系统任务等性质标签，以及设计、开发、测试、评审、提交与收尾等专业标签，
并只展示实际存在的状态段，以便先看懂业务归属，再判断状态和专业环节。

### REQ-PM-SNAPSHOT-006：独立负责人页面和稳定返回路径

作为项目负责人，我希望 6 个负责人视图分别位于独立页面，页首 Tab 在移动端也直接可见；
所有当前工作卡显示明确的详情操作，并从任务、需求、计划和文档详情页返回对应模块，以便
不猜测文字是否可点击，也不在浏览长内容后丢失当前位置。

### REQ-PM-SNAPSHOT-007：可下钻的任务级路线图

作为项目负责人，我希望当前工作页有直接可见的路线图入口，并且路线图中的每张可见工作项卡
都有明确下钻操作，从项目主线逐层展开到工作项、计划阶段、任务和每日进展，以便按日核对
已完成、当前动作和后续路线；没有正式计划时进入任务路线，不生成死卡。

### REQ-PM-SNAPSHOT-008：终态和 closeout 事件正确投影

作为项目负责人，我希望已提交、已关闭的任务不会因为后续 closeout 评审或验证事件重新显示为
进行中，以便看板只展示真实当前工作；只有明确的 reopen 或 changes requested 事件才能重新
打开终态任务。

### 验收标准

1. 保留项目总览、阶段、需求、任务、里程碑、风险与决策、质量、交付物、追踪链和版本变更 10 类底层内容，收敛为项目总览、路线图、当前工作、阻塞与决策、交付就绪、文档与审计 6 个负责人视图。
2. 首屏在 30 秒内回答项目做什么、产品主线做到哪、卡在哪里、交付影响是什么、现在需要谁做什么；看板维护任务不得冒充产品主线。
3. 产品主线以当前会话卡登记的工作项/任务身份为入口，再以该工作项最新 ledger 校正状态、Gate 和下一动作；会话卡与 ledger 冲突时显式采用较新的 ledger 事实。
4. 当前工作明确产品主线、当前并行范围和后续工作；任务进入固定六状态敏捷看板，
   卡片显示需求模块和任务类型，较长历史任务下沉“更多”。
5. 未登记需求模块、任务类型、责任人、日期或产品完成率必须明确显示数据缺口，不得根据标题或路径补造。
6. 质量使用当前任务的验证、评审和 Gate 结论，不用事件数量冒充通过率；交付物、追踪链、版本和内部路径默认下沉审计详情。
7. 文档视图按需求、设计、开发、测试、发布与运维分类，提供可点击的项目相对路径；优先复用 `.factory/project.json` 和 `.factory/memory/doc-map.md`，不新建文档数据库。
8. 页面为只读静态 HTML，在 390×844 和 1440×900 下无页面级横向溢出，键盘可访问，无控制台错误。
9. 当前工作必须显示六种敏捷状态及任务数量；六状态汇总只出现一次，业务分组使用原生
   折叠面板，面板内只显示非空状态段，不得用每组固定六格的稀疏矩阵冒充可读看板。
10. 每张任务卡可点击进入独立详情页；详情页显示业务目标、上级工作项/计划、关联需求、状态、下一动作和审计信息。存在关联需求时，需求名称和 ID 均可点击进入需求详情。
11. 正式 Markdown 文档链接必须进入站内渲染后的 HTML 阅读页，包含返回入口、文档标题、章节结构和可读正文；不得直接打开 `.md` 源文件。
12. 首屏必须用自然语言说明 Shanforge 当前产品形态、解决的问题和交付边界，并区分项目长期目标、当前产品主线和看板维护支线。
13. 路线图必须展示当前主线的完整计划、已完成步骤、当前 Gate、未开始步骤和下一里程碑；缺少正式全项目生命周期分母时明确说明不能计算产品总完成率，同时提供可核验的当前主线 `完成数 / 总步骤数`。
14. 敏捷看板先按正式需求或项目工作项分组；组内以标签区分 `project`、`requirement`、
    `cross_cutting`、`system`。显式 `task_scope` 优先，有正式 `REQ-*` 关系但无层级时
    投影为需求任务，无需求关系且无层级时投影为项目任务，并在审计详情保留原始缺口。
15. 需求任务和跨领域任务按唯一主 `REQ-*` 分组，同一需求只进入一个需求组，需求名称和
    ID 均可点击；项目或系统任务按工作项分组，不得再使用“未拆分独立需求”作为业务分组。
16. 组内以显式任务类型映射设计、开发、测试和评审；缺少任务类型时只允许依据正式状态
    映射“提交与收尾”等管理标签，不根据标题猜测。
17. 产品主线、并行工作、暂停工作和敏捷看板任务都必须显示明确的“查看详情”操作；
    触屏无需 hover 即可识别，键盘可聚焦。
18. 六个负责人页面使用同一组页首 Tab；在 320px 及以上视口不得把整组 Tab 藏进默认
    关闭的菜单，允许导航自身横向滚动。
19. 当前工作页必须提供直接可见的“查看分层路线图”入口；路线图每张可见工作项卡都有
    下钻操作：有计划进入计划，无计划进入当前任务路线，不得出现静态死卡。
20. 计划详情列出阶段和任务并可进入任务详情；任务详情按日期展示 ledger 已登记的每日
    进展。没有日计划或日期时显示“未登记”，不得补造进度。
21. 工作项或任务已有明确终态时，后续 closeout review / verification / commit-ready
    事件不得自动重开；只有显式 reopen 或 changes requested 能覆盖终态。
22. 路线图顶部根节点必须全部可见、可聚焦并进入各自节点页；每个路线节点都必须进入
    自己的节点页，并继续链接直接子节点。已拆任务另行进入任务详情和按日期 ledger，
    未拆叶节点停在真实路线空态，不得出现静态步骤或死链接。
23. 需求/工作项使用原生可展开收回面板；任务性质和设计、开发、测试、评审、提交与
    收尾等专业分类使用标签。状态汇总、业务分组和非空状态段之外不得再增加 bordered
    surface，任务使用分隔线形成扁平列表，视觉上不得框套框。
24. 路线事实必须在 `plan.md` 的 `## Work Breakdown` 四列表中显式登记
    `id / parent_id / title / status`；空 `parent_id` 表示根节点，任意深度父链均可递归
    展示并逐节点下钻，不得从 Markdown 标题深度推断父子关系。
25. 路线节点 ID 必须唯一，非根父节点必须存在，父链不得自引用或成环；违反任一规则时
    快照生成必须失败，不得静默丢弃、重挂或输出部分新路线。
26. 主看板只投影产品主线和当前选中的并行工作项；上方摘要不再重复逐任务卡，分组内只
    生成非空状态段，空状态单元和同一任务重复数都必须为零。

## 需求变更历史

| 版本 | 修改内容 | 日期 | 状态 |
|---|---|---|---|
| `0.3.0` | 所有任务先按需求分组，缺需求进入“未拆分独立需求” | 2026-07-29 | 用户验收拒绝 |
| `0.4.0-candidate` | 改为任务性质优先、唯一需求主分组、显式操作和终态校正 | 2026-07-29 | 用户验收拒绝 |
| `0.5.0-candidate` | 同页阶段锚点、业务分组折叠、性质/专业分类标签化 | 2026-07-30 | 用户验收拒绝 |
| `0.6.0-candidate` | 独立阶段页、H3-H6 路线树、活动工作项业务泳道、历史终态下沉 | 2026-07-30 | 用户验收拒绝 |
| `0.7.0-candidate` | 显式 parent_id 任意层级路线树、统一负责人范围、紧凑非空状态看板 | 2026-07-30 | 等待用户 UI 验收 |

## 需求分析

- `analysis_mode`: `embedded`
- `analysis_locator`: `PM-DASHBOARD-005/brief.md#需求分析`
- 场景：`fix_bug`。
- 根因：`reports/PM-DASHBOARD-005-T01-round-7-root-cause.md`；第七轮三个根因已定位，
  已由用户确认。
- 依赖：现有 `.factory/project.json`、当前会话卡、`doc-map.md`、work item brief、task brief 和 ledger。
- 优先级：P0。
- 可行性：在现有标准库快照脚本内完成，不恢复旧 runtime，不增加依赖。
- 风险：历史任务元数据不完整且会话卡可能滞后；看板必须用当前主线 ledger 校正状态并暴露其余缺口，不自动补造模块、类型、责任人、日期或产品完成率。
- UI baseline 影响：有。当前实现先作为可验收候选，用户评判后再决定是否写入正式 UI baseline。
- 领域模块：`using-shanforge / project snapshot`。

## 边界

- `work_item_id`: `PM-DASHBOARD-005`
- `task_card_id`: `PM-DASHBOARD-005-T01`
- `current_gate`: `round_7_user_ui_acceptance`
- `write_policy`: `state_or_gate_write`
- `allowed_paths`:
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
  - `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/plan.md`
  - `skills/using-shanforge/scripts/project_snapshot.py`
  - `skills/using-shanforge/references/pm-dashboard-rendering.md`
  - `tests/test_using_shanforge_snapshot.py`
  - `.factory/cache/site/current/**`
  - `.factory/memory/agent-session.md`
  - `.factory/memory/tasks.summary.md`
  - `.factory/memory/tests.summary.md`
  - `.factory/memory/review-ledger.jsonl`
- `forbidden_actions`:
  - 恢复 `src/` runtime
  - 新增前端框架、数据库或第三方依赖
  - 修复方案获得人工批准前修改源文件、测试、渲染合同、主线计划或缓存
  - 修改其他工作项事实
  - 用推断值填充缺失的需求模块或产品完成率
  - 修改其他工作项的 brief、task brief、ledger、evidence、report 或 review
  - Push、PR、Merge 或部署
