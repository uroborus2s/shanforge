# 项目状态查询与只读站点

本文件定义 `using-shanforge` 自带 PM 快照脚本的调用合同。脚本属于 skill，不依赖
Shanforge 源码仓、虚拟环境、SQLite 或第三方包。

## 调用

从当前 `SKILL.md` 所在目录定位脚本，在目标项目中执行：

```bash
python3 <skill-directory>/scripts/project_snapshot.py --project-root <project-root>
```

只需在 receipt 中返回项目相对路径时增加 `--relative-paths`。该选项不脱敏页面内容，
不得把本地快照直接当作可公开共享产物。不要把 `<skill-directory>` 原样传给 shell；
必须替换成当前已加载 skill 的真实目录。

## 输入与输出

脚本只读取：

- `.factory/project.json`（可选）
- `.factory/memory/agent-session.md`（可选）
- `.factory/memory/doc-map.md`（可选；用于定位正式技术文档）
- `project.json` / `doc-map.md` 明确登记且实际存在的 `docs/**/*.md`（可选；用于文档入口和缓存指纹）
- `.factory/workitems/*/brief.md`
- `.factory/workitems/*/plan.md`（可选；用于完整主线路线图和阶段进度）
- `.factory/workitems/*/task-briefs/*.md`（可选；用于显示当前任务、层级、优先级和需求关系）
- `.factory/workitems/*/ledger.jsonl`

脚本只写可删除重建的：

- `.factory/cache/site/current/index.html`
- `.factory/cache/site/current/roadmap.html`
- `.factory/cache/site/current/work.html`
- `.factory/cache/site/current/decisions.html`
- `.factory/cache/site/current/readiness.html`
- `.factory/cache/site/current/documents.html`
- `.factory/cache/site/current/tasks/*.html`
- `.factory/cache/site/current/requirements/*.html`
- `.factory/cache/site/current/plans/*.html`
- `.factory/cache/site/current/stages/*.html`
- `.factory/cache/site/current/documents/*.html`
- `.factory/cache/site/current/snapshot.json`

标准 receipt 为 `SkillProjectSnapshotReceipt/v1`，包含 `status`、`html_path`、
`cache_hit`、`generation_id`、`source_count`、`relative_paths` 和 `read_only_facts`。
输入指纹不变时必须返回 `cache_hit=true`。

## 完整项目快照合同

页面不是任务列表，而是项目负责人接手和决策入口。保留项目总览、阶段、需求、任务、
里程碑、风险与决策、质量、交付物、追踪链和版本变更 10 类底层内容，收敛为 6 个固定视图：

1. 项目总览：30 秒内说明项目是什么、解决什么、交付什么，以及产品主线、当前任务、
   主线状态、停止原因和唯一下一动作。
2. 路线图：只读取产品主线 `plan.md` 的 `## Work Breakdown` 四列表
   `id | parent_id | title | status`。空 `parent_id` 是根节点，同父节点按表格行顺序显示；
   每个节点都进入自己的阶段页，页面只列直接子节点、全部后代进度和精确同 ID 任务入口。
   任务详情继续显示按 ledger 日期整理的每日进展。
   缺少正式日计划或全局批准范围分母时必须显示数据缺口，不得伪造日路线或产品整体完成百分比。
3. 当前工作：负责人范围固定为产品主线和按更新时间选中的一个并行工作项，其他活动事项进入
   “未纳入当前会话 / 后续工作”。页面顶部只汇总
   `待开始`、`进行中`、`测试中`、`待评审`、`待确认 / 阻塞`、`已完成` 六种状态一次；
   看板按正式需求或项目工作项生成可展开业务组，组内只显示实际存在的状态段，不生成空列。
   多需求任务以第一个正式关系作为唯一主分组，其余需求保留在任务详情中；需求名称和
   ID 使用同一个分组标题链接。设计、开发、测试、评审、提交与收尾等专业类别只作为标签。缺少
   显式层级时，有 `REQ-*` 关系投影为需求任务，无关系投影为项目任务；原始缺口只在详情审计
   中保留，不从标题推断。
   当前区只纳入活动工作项的当前、已完成兄弟和明确计划任务；终态工作项全部下沉折叠历史区。
   当前范围摘要不生成任务卡，任务只在主板出现一次；需求分组标题进入需求详情，有计划的
   工作项标题进入计划页，无计划时进入当前任务。移动端把非空状态段纵向排列。
4. 阻塞与决策：原因、影响、责任人、截止日期和下一动作；未登记字段保持可见。
5. 交付就绪：按需求、设计、实现、验证、审批和发布说明已登记事实，不计算虚假完成率。
6. 文档与审计：先按需求、设计、开发、测试、发布与运维快速打开渲染后的正式 HTML
   文档；不得把 `.md` 源文件作为负责人阅读页面。交付物、追踪链、版本、质量事件和
   内部路径默认下沉。

“下一步”是总览和当前工作中的行动字段，不再作为第 11 个同级栏目。

6 个负责人视图分别生成独立顶层 HTML，并使用同一组始终直接可见、可横向滚动的页首 Tab
切换，不得在窄屏放入默认关闭菜单。当前工作提供明确的分层路线图入口；路线图中每张工作项
卡都显示下钻操作，有计划进入计划页，无计划进入当前任务路线。任务与需求详情返回
`work.html`，计划详情返回 `roadmap.html`，技术文档详情返回 `documents.html`，不得统一跳回
`index.html` 页首。

路线图顶部每个根节点必须是可见、可聚焦的整卡链接，进入 `stages/<node-id>.html`。
路线结构只服从显式 `parent_id`，不从 Markdown 标题深度推断，支持任意层级。重复 ID、
缺失父节点、自引用或父链循环必须让快照返回失败 receipt，保留上一份完整快照，不生成部分
路线。每个节点页只显示直接子节点入口，并统计全部后代；匹配同 ID 任务时另给任务详情和
每日 ledger 入口，节点链接不得被任务链接替代。缺少状态时显示“状态未登记”，不得默认为
`planned`；未登记任务时不生成虚假任务页或死链接。

看板的需求或工作项业务分组使用原生 `<details>/<summary>` 展开收回；当前相关组默认展开。
项目、需求、跨领域、系统等任务性质和设计、开发、测试、评审、提交与收尾等专业分类只作为
任务标签，不再各自生成 bordered surface。业务泳道是唯一分组 surface，状态单元用分隔线，
任务使用扁平列表，避免框套框。

## 解释边界

- 只有卡片明确显示“等待你的确认”时才代表真实人工 Gate。
- 工作项和任务数量不是产品功能完成率；缺少批准范围分母时必须显示“产品完成率暂不可计算”。
- 当前会话卡只用于定位产品主线 work item / task；该主线 ledger 的有效事件提供状态、
  Gate 和下一动作。`approved` 只属于 review_status，不得作为 TaskCard 生命周期或产品/WBS
  完成依据；产品和 WBS 完成只认 `completed`、`closed` 或 `superseded`。工作项或任务已有
  `closed`、`completed` 或 `superseded`
  终态时，后续 closeout review、verification 或 commit-ready 事件只进入审计，不得重开；
  只有显式 `reopen` 或 `changes_requested` 重开终态。会话卡与 ledger 冲突时，负责人视图
  采用该规则归约后的较新事实，不展示已失效动作。
- 工作项终态只由 `completion_level=work_item`、明确的 work-item close 事件或不绑定任务的
  终态事件冻结；单个任务完成不能阻止同一工作项的后续任务进入当前状态。
- 只有 ledger 最后一条事件明确指向的
  task 才进入当前执行状态。其他 task 只在自身或父工作项已经终态时显示为已完成，否则
  不进入负责人当前工作，避免旧 task 事件重新冒充当前任务。
- work item brief 提供业务目标和阶段，task brief 提供模块、类型、层级、优先级、
  需求关系和完成标准。
- 已关闭或已替代工作项下的旧任务随父工作项归档，避免旧 task brief 状态重新变成当前任务。
- 原始 ID、原始状态放在可展开的技术记录中；业务首屏不得由状态码和哈希主导。
- 任务卡必须使用可理解标题并进入独立任务详情；已登记需求和计划必须能继续点击查看。
- 需求、任务、计划和文档详情由同一次快照生成，快照不得依赖 Shanforge 仓库中的旧站点文件。
- 看板维护、流程改进和产品主线必须分栏；任意较新的维护任务不得覆盖会话卡登记的产品主线。
- 技术文档入口只使用项目相对路径；不建立第二份文档数据库，不读取绝对路径补造文档。
- 没有 brief 和 ledger 的分组目录不是工作项，不得显示为“状态未登记”。
- 非法 JSON/JSONL、目标目录不存在或缺少 `.factory/` 时失败关闭。
- 页面只读，不提供编辑、审批、提交或发布入口。
- HTML 和缓存不是项目事实，不写 ledger、不提交 Git。
