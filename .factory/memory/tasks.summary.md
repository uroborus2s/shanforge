# 任务摘要

- 当前阶段：`MODEL-ROUTING-001 / completed`
- 当前焦点：事实源、干净基线和 Sol/Terra/Luna 路由均已闭环。

> 历史读取规则：以下所有带日期条目都是记录发生时的历史快照。条目中的“当前”“下一步”只表示当时状态，不得覆盖本文件顶部的当前焦点和当前动作。

- 2026-08-23：T02 已固化 Sol 唯一控制和复杂度/风险路由包；仅 `simple + low` 给 Luna，
  其他已授权任务给 Terra，五类升级信号交还 Sol。Red `4 failed`、Green `4 passed`，
  与相邻工作流联合 `21 passed`；未增加运行时、API 或依赖，进入 T03 集中质量门。

- 2026-08-23：T03 首轮 review 的唯一 Important 已用表格驱动语义测试关闭；复审为
  `approved / 98 / C0-I0-M0`，全量 `233 passed / 4 subtests passed`。当前进入精确本地提交和最终干净克隆复验。

- 2026-08-23：路由提交 `c9f02cb` 的 `--no-local` 干净克隆为 `233 passed / 4 subtests passed`，
  Ruff、JSON/JSONL、Git clean 与 diff check 全部通过；`MODEL-ROUTING-001` 已关闭。

- 2026-08-23：T01 独立复审最终 `approved / 97 / C0-I0-M0`，本地基线提交
  `9245946`。从该提交新建干净克隆后，完整 pytest `228 passed / 4 subtests passed`，
  Ruff、JSON/JSONL、Git 状态和 diff check 全部通过；T01 关闭并进入 T02。

- 2026-08-23：`MODEL-ROUTING-001-T01` 已备份并裁剪约 95MB 历史过程资产，统一正式
  PRD、追踪矩阵、项目配置和当前 memory 到 skill-first 边界。完整 pytest
  `228 passed / 4 subtests passed`，根 Ruff、JSON/JSONL 与 diff check 通过；下一门为
  独立只读 review、本地基线提交及提交后干净克隆复验。

- 2026-07-30：并行任务 `PM-DASHBOARD-005-T01` 第七轮已按获批方案完成实现与验证。
  EAD `Work Breakdown` 已迁移为显式 `parent_id` 四列表，32 个节点全部生成独立页面；
  非法父链 fail-closed。主板只含产品主线和一个并行工作项，共 3 张唯一任务，六状态
  汇总一次、空状态段 0、上方重复任务卡 0。聚焦 `10 passed / 4 subtests`，Ruff 通过；
  全仓 `219 passed / 7 个与前像相同的范围外失败 / 4 subtests`。1440×900 和
  390×844 浏览器路径无横向溢出，控制台错误 0。独立任务评审为
  `approved / 99 / C0-I0-M0`；当前等待用户 UI 验收，验收前不得提交或关闭。
- 2026-07-30：并行任务 `PM-DASHBOARD-005-T01` 第六轮候选被用户再次退回。用户已确认
  三项根因和路线目标：显式 `parent_id` 任意层级树、取消每组固定六空格、统一负责人
  范围并去除重复任务。第七轮计划采用四列路线节点表、每节点独立页面、一次六状态汇总和
  组内非空状态段。独立计划评审 Iteration 1 为 `changes_requested / 84 / C0-I2-M1`；
  精确 allowlist、工作项分组链接断言和全仓失败身份前像整改后，Iteration 2 为
  `approved / 98 / C0-I0-M0`。当前 Gate 为 `round_7_fix_plan_confirmation`；
  实现授权为 `false`，未修改源文件、测试、主线计划或缓存，未提交。
- 2026-07-29：并行任务 `PM-DASHBOARD-005-T01` 已按退回意见完成管理视图重做：
  10 类底层内容收敛为 6 个独立负责人页面，产品主线与看板维护分离。第三轮退回的
  “按需求分组后按层级/类型分类”、全部当前工作卡详情链接、独立页面与稳定返回、
  路线图下钻到计划/任务/每日 ledger 进展均已实现。独立接手复核为
  `approved / 96 / C0-I0-M0`，但第四轮真实 UI 验收再次退回。已稳定复现移动路线图
  默认隐藏、7 张路线卡仅 2 张可点、整张任务卡不可点、错误的“需求优先”分组层级和
  closeout 事件重新激活已完成任务；用户已确认四个根因并批准第四轮修复方案。
  “任务性质优先 + 需求任务二级分组 + 显式操作 + 终态校正”已完成测试先行实现。
  第四轮独立复核发现 2 个 Important 和 1 个 Minor：重叠需求组、需求 ID 不可点击、
  显式重开分支缺少自动化；三项已整改并由同一 reviewer 复核关闭，最终
  `approved / 100 / C0-I0-M0`，但第五轮真实 UI 验收再次退回：顶部 5 个路线阶段
  `0/5` 可点击；看板分类继续使用嵌套容器且 40 个需求/工作项组都不是折叠面板。两个
  根因和第五轮修复计划均已获用户确认；第五轮候选已完成“5/5 阶段锚点下钻 +
  40/40 原生折叠业务组 + 174/174 性质/专业标签 + 扁平任务行”。Red 两项按根因失败，
  Green `2 passed`，聚焦 `7 passed`，全仓 `216 passed / 7 failed` 且失败集合未扩大。
  自动浏览器受本地 `file://` 安全策略限制；独立评审按静态 HTML 和新鲜验证给出
  `approved / 97 / C0-I0-M0`，但第六轮真实 UI 验收再次退回：5 个阶段都只进入同一
  总计划页的不同锚点，没有阶段自己的子路线；看板仍以状态优先切分全部 174 个任务，
  其中 169 个终态任务占据“已完成”主列。两个根因已由用户确认；第六轮计划候选改为
  “H3-H6 显式路线树 + 5 个独立阶段页 + 活动工作项业务泳道 + 历史终态下沉”，03
  显示 8 个直接子步骤。用户批准后已完成测试先行实现：Red `3 failed`，Green
  `3 passed`，聚焦快照 `8 passed`，Ruff check/format 通过。真实页面为 5 个独立
  阶段页，03 为 `7 completed / 1 current`；当前看板只保留 7 张有效任务卡，
  167 条终态历史下沉折叠。全仓 `217 passed / 7 failed`，失败集合与前轮相同。
  自动浏览器受本地 `file://` 安全策略限制，未冒充视觉通过。独立评审 Iteration 1
  发现状态静默推断和移动端 CSS 未锁定两项 Important；整改后同一 reviewer 复审为
  `approved / 98 / C0-I0-M0`。当前等待用户 UI 验收，尚未提交。
- 2026-07-29：`SKILL-FIRST-PM-001-T01` 以 skill-local 标准库脚本替代旧 runtime 看板；
  Shanforge / ITA Club 第二次生成均缓存命中，四组浏览器验收通过，定向 `3 passed`，
  全仓 `212 passed / 7 failed`，7 项均为范围外既有漂移。首轮和复审 findings 已关闭，
  独立复审 `approved / C0-I0-M0`；本地提交 `ac67036`、`4f5ed56`，状态 `closed`。
- 2026-07-28：`PM-DASHBOARD-004-T03` 已完成业务分组、稳定任务合并、严格状态映射、诚实完成度和业务卡片实现，renderer `22 passed`。真实快照为当前交付 0、待办 1、待治理 139、归档 60、系统 0；根因是 `sqlite_index` 未从任务简报补回 `task_scope/priority/traceability_targets`，范围外实现等待用户批准最小写集扩展。
- 2026-07-28：用户批准 T03 最小写集扩展；SQLite 合并根因测试 `1 failed → 1 passed`，索引与 renderer 联合 `41 passed`。新快照为当前交付 1、待办 2、待治理 137、归档 60、系统 0，T03 已显示 P0、跨需求任务和三项强需求关系，当前 `ready_for_review`。
- 2026-07-28：T03 首轮独立评审 `74 / C0-I3-M0`；`project` 层级、强 `IMPLEMENTS` 关系和稳定 ID 最终排序三项反例均由 `1 failed` 转绿，联合回归更新为 `43 passed`，当前 `ready_for_same_reviewer_rereview`。
- 2026-07-28：T03 iteration 2 同一 reviewer 复审 `approved / 100 / C0-I0-M0`，三项 Finding 全部关闭；当前进入 T04 质量汇总与长文档阅读。
- 2026-07-28：T04 将质量页分为测试资产、执行证据和诊断，技术明细默认折叠；长文档在正文前显示用途、读者、状态和稳定章节链接。定向 `31 passed`、相邻 SQLite 投影联合 `50 passed`，真实质量计数 `851 / 0 / 216`，当前 `ready_for_review`。
- 2026-07-27：旁路工作项 `STRATIX-SERVICE-GUIDE-001-T01` 已把 Stratix 源码调查与业务开发规范分离：删除运行时 `source-locations.md`，所有业务项目直接遵循 skill 内统一规范；回归 `19 passed`，独立复审 `approved / 100 / C0-I0-M0`，进入精确范围本地提交，不改变顶部主项目 Gate。
- 2026-07-27：T03 首轮评审 `84 / C0-I1-M1`；已补客户 6 项确认包内的
  5 组强制 actor 分离，并让 Validator 回读 T02 的 45 条转移、覆盖完整 A/R、
  未确认客户、AI actor 和职责分离负例；Iteration 2 独立复审
  `approved / 100 / C0-I0-M0`，当前等待客户岗位授权确认。
- 2026-07-27：T02 已由本地提交 `f5ed0e4` 收口。T03 已定义 6 个通用岗位、
  14 个 RACI 活动和 6 类门禁；真实 actor 映射保持
  `pending_customer_confirmation`。
- 2026-07-27：T02 Iteration 4 独立复审 `approved / 98 / C0-I0-M1`；
  陈旧字段计数 Minor 已修正，最终验证通过，当前
  `approved_ready_for_local_commit`，WorkItem 保持开放。
- 2026-07-27：T02 Iteration 3 复审为 `changes_requested / 89 / C0-I1-M0`；
  已统一公共信封 `schema_version`、唯一 `data` 对象与 validator 前像，并冻结
  golden digest，当前再次 `ready_for_review`。
- 2026-07-27：T02 Iteration 2 复审为 `changes_requested / 87 / C0-I1-M1`；
  已固定 RFC 8785 digest 前像和 mismatch 拒绝，并补 actor、AI reviewer、
  revision、digest、redaction 5 个治理负例，当前再次 `ready_for_review`。
- 2026-07-27：T02 首轮独立评审 `changes_requested / 68 / C0-I4-M1`；
  已补齐稳定 actor 与版本审计、6 类模型、45 条封闭状态转移、4 个非法转移负例、
  独立验收记录和 memory 精确 hunk 策略，当前 `ready_for_review`。
- 2026-07-27：用户批准 EAD 最小路径，T01 已由本地提交 `314983e` 收口。
  T02 已定义 5 类数据模型、6 类 Agent 契约、统一人审与失败边界，当前
  `ready_for_review`；完整 Web、数据库、API 和客户系统接入未启动。
- 2026-07-27：`EAD-TASK-001` 独立评审 `approved / 95 / C0-I0-M1`，
  Minor 已修正；13 文件候选精确暂存但未提交。真实 Gate 要求用户确认
  “咨询实施包 + 半自动 Agent + 人工脱敏导入 + 2 个需求/P0-P1 缺陷”最小路径，
  WorkItem 保持开放，T02–T05 未启动。
- 2026-07-27：`SKILL-CLEANUP-001` 与 `GO-BACKEND-SKILL-001` 已由本地提交
  `89982b3` 完成：Go Skill 更名为 `go-developer` 并补齐规范和可运行模板，
  仓内 `skill-creator` 及专属工具/测试退役。独立评审 `96/98`，两个 WorkItem
  均已关闭；项目实际待办由 8 个降为 6 个。
- 2026-07-27：`STATE-RECONCILIATION-001-T01` 已核实 6 个本地提交并为 12 个历史
  WorkItem 各补记唯一 `closed` 事件；JSONL、最新状态、唯一性与 Git 祖先关系检查通过，
  独立评审 `approved / 99 / C0-I0-M1`，当前已关闭。
- 2026-07-27：`FLOW-CONTRACT-001` 已关闭。`FLOW-TASK-015` 实现复审
  `approved / 98 / C0-I0-M0`，本地提交 `f21654d`；15/15 项队列完成。
  其他 WorkItem 盘点为 8 个仍有实际后续动作、12 个仅缺 ledger 显式关闭事件；
  详见 `.factory/workitems/FLOW-CONTRACT-001/reports/FLOW-CONTRACT-001-closeout-and-open-workitems-audit.md`。
- 2026-07-23：`FLOW-TASK-015` 方案 Review 依次为 `46/C3-I4`、`82/C1-I1`、最终 `approved / 98 / C0-I0-M1`。v1.2.0 候选绑定正式 v1.1.0 基线，包含 16 个行为、13 个工作流、可达的身份创建控制流、fail-closed 写入矩阵和逐工作流节点转换；结构 7、规定组合 56、Ruff 和 diff check 通过。候选 hash 已冻结，正式文档和 runtime Skills 未修改，当前等待人工治理确认。
- 2026-07-23：`FLOW-TASK-014` 启动记忆和非活跃任务降级规则完成。当前会话事实足够时零 memory 读取，缺口按一个最小片段扩展；`current-state.md` 收敛为 45 行、2331 bytes、5 条最近事实，历史 ledger/evidence/review/report 保留；目标 9、直接相邻 33 通过，同一 Reviewer 最终 `approved / 98 / C0-I0-M0`。
- 2026-07-23：`FLOW-TASK-013` 项目级测试治理完成。正式测试计划保持 `v3.1.0`，当前治理修订明确为未发布候选；4 个稳定测试 ID 分别绑定需求、任务、可执行入口、evidence、结果和 2 个真实环境。目标 9、相邻 30、黑盒入口 13、UI 入口 18、API 入口 5 均通过；同一 Reviewer 最终 `approved / 98 / C0-I0-M0`。
- 2026-07-22：旁路工作项 `SKILL-CLEANUP-001` 已退役仓内 `skills/skill-creator` 及其 eval、benchmark、报告和打包工具，不新增 `skill-evaluation`；本地脚本依赖与专属测试已清理，范围验证见 `.factory/workitems/SKILL-CLEANUP-001/evidence/completion-verification.md`，当前 `ready_for_review`，不改变顶部主工作项进度。
- 2026-07-22：`SKILL-CLEANUP-001` 将 `go-backend-developer` 改名为 `go-developer`，并同步 Codex 全局项目 Skill 软链接；仓内与全局链接均为 37 项，名称、目标路径和有效性完全一致，验证见 `.factory/workitems/SKILL-CLEANUP-001/evidence/go-developer-rename-and-global-link-sync-verification.md`，当前 `ready_for_review`。
- 2026-07-22：`uroborus` 回复“确认”，精确批准 R009 Manifest `8be9d829…77ae` 与 candidate root `ce079fcd…df68`。需求 Gate 已关闭，授权原位正式化、设计、计划、实现、测试、迁移及验证后当前任务本地提交；不包含 `TASK-IMPLEMENT-002-R001`、远端、PR、Merge 或部署。
- 2026-07-21：`TASK-REQ-006` R001–R004 精确需求候选已冻结，8 个语义 Artifact root `5ab03160…94c5`，Manifest `8338d35e…d160`；同一独立 Reviewer 最终 `approved / 96 / C0-I0-M0`。候选固定 `docs` 仅人类当前文档、SQLite 非权威关联索引、单 8 KiB 记忆点、事件驱动压缩、有界 cache、`.factory/pm` 去事实化、每 scope 单一 `current.html` 与授权 fail-closed。当前等待人工计划确认，正式文档、设计、代码、Git 和发布均未执行。
- 2026-07-21：用户后续讨论使 R004 Manifest 失效；合并 R005 独立评审 `changes_requested / 58 / C1-I6-M0`。R006 已在原范围整改：分级离线/受限发布、R014 双 Hash pin、137 字段唯一 field map、固定 as_of、stable symbol ID、16 REQ/64 AC/11 NFR 机器合同和 22 条封闭状态转移；当前同一 Reviewer 复审，尚未人工批准。
- 2026-07-21：R006 复审 `changes_requested / 78 / C0-I4-M0`。R007 将 13 个 PM row model 绑定 R014 record identity/命名空间键，16/64/11 与 Markdown 逐字段 JCS Hash 对账，10 个非终态改为 50 条互斥穷尽事件转移，并统一 canonical `ProjectProgressSnapshot/v2`；当前同一 Reviewer 复审。
- 2026-07-21：R007 复审 `changes_requested / 89 / C0-I1-M0`，仅剩 root 前像歧义。R008 固定 `{requirements,nfrs}` 规范对象、不含派生字段的 JCS 前像，canonical bytes 23717、SHA-256 `96be53fe…045e`；复用未变化的 R007 PM field map，当前同一 Reviewer 复审。
- 2026-07-21：R008 独立复审 `approved / 98 / C0-I0-M0`；freeze 前事实审计发现 R014 机器合同的 `candidate_unapproved` 是冻结历史字段，权威 release manifest `ea84805f…ef4e` 已记录用户批准并 `released`。R009 仅修正发布状态 Owner、绑定 release manifest 并重算规范 root，当前同一 Reviewer 回归。
- 2026-07-21：R009 发布状态事实修正经同一 Reviewer `approved / 99 / C0-I0-M0`；16/64/11、23720-byte root、137 fields、50 transitions、Snapshot v2 与 R014 release pin 全部复核通过，进入精确 Hash 人工 Gate 编制。
- 2026-07-21：R009 精确候选已冻结，6 个 Artifact root `ce079fcd…df68`，Manifest `8be9d829…77ae`；`design_or_implementation_authorized=false`，等待用户精确 Hash 确认。
- 2026-07-21：TASK-IMPLEMENT-002 T01–T08 8/8 完成，11/11 候选需求实现；T08 Spec/Quality 和整体独立 Review 均 `approved / 100 / C0-I0-M0`。Final candidate 38 artifacts，root `3d52c5…d770`，formal release false；当前唯一 Gate 为精确 manifest hash 批准。
- 2026-07-21：旁路工作项 `PM-DASHBOARD-002-T01` 已把 Excel 样例信息架构一次性固化进 HTML 状态模板；运行时禁止回读 `.xls/.xlsx`。独立复审 `approved / 99 / C0-I0-M0`，最终定向 23、相邻 11+42、Ruff 和五视口截图门通过；不改变顶部主工作项进度或正式产品事实。
- 2026-07-21：T08 定向924、全仓1249、静态门与性能/11追踪全绿；pre-review manifest `d267e9…d330` 不可批准，当前 task-level Review。
- 2026-07-21：T07 focused Spec/Quality `approved / 100 / C0-I0-M0`，34 个定向集成/scaffold 与隔离/静态探针通过。P001 完成 7/8，进入 T08。
- 2026-07-21：T06 最终 focused Spec/Quality `approved / 100 / C0-I0-M0`，三项 Finding 全闭；finding 4、visibility 12 与静态门通过。P001 完成 6/8，进入 T07。
- 2026-07-21：T05 最终 Spec/Quality `approved / 100 / C0-I0-M0`，六项 Finding 全闭；末轮按 fast-path 仅 exact race 1、affected projection 50 和静态门。P001 完成 5/8，进入 T06。
- 2026-07-21：T05 完成 Red/Green 与作者验证：172/79/101/323 tests、Ruff/format/mypy 全绿，当前独立 Review。P001 完成仍为 4/8，无人工 Gate。
- 2026-07-21：T04 最终 Spec/Quality `approved / 100 / C0-I0-M0`，五项 Finding 全闭；29/101/121/286 tests、事务/竞态探针与静态门全绿。P001 完成 4/8，进入 T05。
- 2026-07-21：T04 完成 Red/Green：21/93/113/286 tests 与 Ruff/format/mypy 全绿，当前独立 Spec/Quality Review。P001 完成仍为 3/8，无人工 Gate。
- 2026-07-21：T03 Spec `approved / 100`；Quality 两项 Important 已整改并由同一 reviewer 复验为 `approved / 100 / C0-I0-M0`。Finding 12、T03 20、联合 272、相邻 18 passed，静态门全绿。P001 完成 3/8，T04 实现中。
- 2026-07-21：T03 提供一次 commit 的 application service、typed command/result 和薄 access API；T03 8、联合260、相邻18 passed，静态门全绿，当前独立 Review。
- 2026-07-21：T02 经三轮 Spec Review/整改最终 Spec/Quality 均 `approved / 100 / C0-I0-M0`；72/252/105 tests 和静态门全绿。P001 完成 2/8 并进入 T03，无人工 Gate。
- 2026-07-21：T02 initial Spec Review `changes_requested / 84 / C0-I2-M0`；same-version schema drift 与 qualification/receipt binding 两项已进入同范围 TDD 整改，Quality not_run，无人工 Gate。
- 2026-07-21：T02 已实现 versioned SQLite、独立 staging qualification、单事务正式晋升、逐对象回读、不可变 event/receipt、幂等 replay 和并发序列；定向 59、联合 239、project-control 105 passed，静态门全绿。当前独立 Review，无人工 Gate。
- 2026-07-21：T01 经 8 次 Spec Review/定向整改循环最终收口；replacement independent reviewer 最终 Spec/Quality 均 `approved / 100 / C0-I0-M0`，T01 focused `180 passed`，Ruff/format/mypy/diff check 全绿。P001 完成 `1/8` 并直接进入 T02，无人工 Gate。
- 2026-07-20：用户授权连续完成 TASK-IMPLEMENT-002 P001 的 T01–T08 代码、测试、独立 Review、同范围整改和 R001 候选编制。执行从 T01 开始，内部 checkpoint 不停人工确认；正式发布、Git、远端和部署仍排除。
- 2026-07-20：T01 合同内核已完成 Red/Green，主协调器新鲜复验 28 passed，Ruff/format/mypy/diff check 通过；当前独立 Spec/Quality Review 进行中，通过后直接进入 T02。
- 2026-07-20：T01 独立 Spec Review `changes_requested / 41 / C3-I1-M0`，Quality not_run；四项真实缺口已进入同范围 TDD 整改，无人工 Gate，整改后回同一 reviewer 复审。
- 2026-07-21：T01 C3-I1 已用三轮 Red/Green 关闭；focused suite 96 passed，Ruff/format/mypy/diff check 全绿。当前同一独立 reviewer Spec re-review + Quality Review，内部连续执行。
- 2026-07-21：T01 re-review iteration 1 确认 C-001/C-002 关闭，剩余 split security C1 与 merge identity I1；当前第二轮 TDD 整改，无人工 Gate。
- 2026-07-21：T01 剩余 C1/I1 已完成第二轮 Red/Green，focused suite 123 passed，Ruff/format/mypy/diff check 全绿；当前同一 reviewer 第二次 Spec 复验 + Quality Review。
- 2026-07-21：T01 re-review iteration 2 关闭 merge identity，新增 path-aware security C1 与 aggregate false-positive I1；当前第三轮 TDD 整改，无人工 Gate。
- 2026-07-21：T01 path-aware security 整改已完成，focused suite 137 passed，Ruff/format/mypy/diff check 全绿；当前同一 reviewer iteration 3 + Quality Review。
- 2026-07-21：T01 re-review iteration 3 仅剩两个 nested sibling authorization bypass；当前最后一轮定向 TDD 整改，无人工 Gate。
- 2026-07-21：T01 最后 finding 已完成定向 Red/Green，focused suite 147 passed；当前同一 reviewer iteration 4 + Quality Review。
- 2026-07-21：T01 re-review iteration 4 仅剩两个 nested scope exact bypass；当前递归路径语义摘要整改，无人工 Gate。
- 2026-07-20：`TASK-IMPLEMENT-002` 精确 11 项范围已转为 P001 和 8 个代码任务。Iteration 1 `76/C0-I6-M3`、Iteration 2 `88/C0-I1-M1` 均自动整改；Iteration 3 最终 `approved / 98 / C0-I0-M0`。计划采用非权威 staging qualification、只追加权威事件、单事务正式晋升、双状态、背压/lease 和精确候选 Review 路径。当前只等待代码实施授权，没有修改本增量产品代码。
- 2026-07-20：R001 正式文档事务 `DELIVERY-DOCS-ACTIVATION-TX-R001-G001` 完成。6 个正式目标与冻结 after-image 字节相同，formal manifest `cad74cb3…dc27`、root `632e705a…869c`；发布后 validator、832 pytest、Ruff、format299、mypy236、Skill38、docs-stratego、lock/JSONL/diff 全绿。完成层级为第 8/8 步当前本地交付闭环；项目产品范围仍剩余 108 项。
- 2026-07-20：`uroborus` 已批准 `TASK-DELIVERY-001-R001`，批准绑定当前唯一冻结 manifest `4dcd7ad0…3f0c`；交付内容验收完成。完成层级是 `delivery_content_accepted`，不是第 8/8 步或项目整体完成；正式 docs 尚未激活，正式需求实现仍为 15/123。
- 2026-07-20：第 8/8 步已连续执行到最终内容验收 Gate。`TASK-DELIVERY-001-R001` artifact root `632e705a…869c`，独立复审 `approved / 100 / 0-0-0`；主线程复验 source 10/10、artifacts/docs 6/6、攻击 6/6、pytest 832/832、Ruff 0、format 299、mypy 0/236、Skill 38/38 和文档结构门全绿。完成层级仍是交付候选，不是项目整体完成；正式需求 123，产品代码实现 15，剩余 108。
- 2026-07-20：R002 candidate `6f701da5…43fdc` 经独立复审 `approved / 100 / 0-0-0` 和人工批准后，由本地事务正式激活。Formal manifest `eae82c90…77c0a`，released event 唯一计数 1；发布后 832/832、Ruff 0、mypy 0/236、format 299、Skill 38/38、17+8 负向攻击全部通过。完成层级为第 7/8 步；正式需求 123，产品代码实现 15。
- 2026-07-19：TASK-SKILL-002 为剩余 32 个工作 Skill 增加 `project_position`、`completion_level`、`stop_reason`、`scope_remaining` 四字段及路由边界；不改变专业触发语义、人工 Gate 或流程 owner。与 TASK-SKILL-001 合计覆盖顶层 Skill `38/38`。RED 2/2、GREEN 4、定向 11、相邻 136、全仓 828 passed；独立初审 1 Important / 1 Minor 全部关闭，最终 `approved / 100 / 0-0-0`。产品代码需求实现数仍为 15，本任务不增加该计数。

- 2026-07-19：TASK-SKILL-001 修改 6 个顶层流程 Skill，使会话先报告项目整体位置，内部实现/验证/只读 review/同范围整改不再逐项确认，真实人工 Gate 继续硬停止。RED 6/1，GREEN 7；首轮两项 Important 和复审一个 Minor 全部关闭，最终 `approved / 100 / 0-0-0`；定向 12、相邻 40、全仓 824 passed。

- 2026-07-19：用户撤销未发布的 R001 并授权删除未使用的 runtime Skill 管理链路。TASK-QUALITY-002 删除 6 个 Skill 源码文件、专属 ports、context/session 字段、settings/composition/catalog 和旧行为测试，增加防回退结构测试并同步设计事实；Ruff、format、mypy src、817 项 pytest 和 diff check 通过。同一独立 reviewer 最终 `approved / 100 / 0-0-0`，I-001/I-002 全部关闭。当前无活动候选或人工 Gate。

- 2026-07-19：P001 T08 与整个开发实施批次完成。T08 Spec C-001（重复权限来源静默覆盖）和 Quality I-001（event-log 计数 oracle 恒真）均经 RED→GREEN 整改关闭，最终 Spec/Quality Re-review 均 `approved / 100 / 0-0-0`。主代理新鲜验证 target `22 passed`、项目控制 `519 passed`、全仓 `809 passed`，failed/skipped/not_run=`0/0/0`；T08 changed-file Ruff/format、隔离 mypy、diff check 通过。全仓既有 Ruff/mypy 债务仍为 `33/73`，精确登记为 concern。第 5/8 步“开发实现”完成，正式发布、Git、远端、部署均未执行。

- 2026-07-19：P001 T06 快速验证与 durable transfer 完成。replay outcome 单调性、readback qualification receipt、orphan dispatcher/worker 拒绝及 POSIX 同线程 deadline 已完成 TDD 整改；Spec Recheck 5 与 Quality Re-review 均 `approved / 98 / 0-0-0`。主代理新鲜复验 target `89 passed`、T05+T06 `131 passed`、direct POSIX `1 passed`，Ruff/mypy/format 通过。T06 状态 `ready_for_next_task`，已按连续授权进入 T08。

- 2026-07-19：P001 T04 权限安全十五行状态回复完成。Quality Review 发现 raw facts 可自授权的 Critical，TDD 整改为独立 exact-context permission grant/port；整改后 Spec/Quality Re-review 均 `approved / 100 / 0-0-0`。主代理新鲜复验 target `38 passed`、相邻 `303 passed`、contract/provenance `74 passed`，Ruff/mypy/format 通过。T04 状态 `ready_for_next_task`，无新增人工门。

- 2026-07-19：P001 T07 provenance/hygiene 完成。独立 Spec Re-review 2 与 Quality Re-review 均 `approved / 100 / 0-0-0`；registry authority、final receipt qualification、跨 adapter JSONL once-only、深层不可变性均已关闭。最终 target `64 passed`、相邻 `404 passed`、定向攻击 `8 passed`，Ruff/mypy 通过。T07 状态 `ready_for_next_task`，无新增人工门。

- 2026-07-19：P001 T02 fixed-H 位置查询完成。Spec Re-review 与 Quality Re-review 均 `approved / 100 / 0-0-0`；deep event immutability、stage-map canonical hash、显式 high-water port 与主动行为 spy 全部关闭。复审验证 contracts+position `73 passed`、adjacent disposition `197 passed`，Ruff/mypy 通过；并行切片联合 `388 passed`。T02 状态 `ready_for_next_task`，既有授权已直接启动 T04。

- 2026-07-19：P001 T05 evidence/Gate CAS 完成。Quality 初审的 replay eligibility、SQLite lifecycle/concurrency 与 datetime coverage 经 TDD 整改，独立 Quality Re-review `approved / 100 / 0-0-0`；新鲜目标 `42 passed`、相邻 `249 passed`、定向攻击 `10 passed`，Ruff/mypy 通过。T05 状态 `ready_for_next_task`，既有批次授权已直接启动依赖任务 T06，无新增人工门。

- 2026-07-19：P001 T03 disposition/Gate 完成。Spec 的 proof trim/whitespace Finding 经攻击测试整改，Spec Re-review `approved / 100 / 0-0-0`；Quality Review `approved / 97 / 0-0-1`，仅剩非阻塞 purity-test alias Minor，独立 `asdict()` 探针已证明运行时输入不变。共享 T02 契约变化后，主代理联合复验 contracts+position+disposition+evidence 为 `303 passed`，Ruff 通过，mypy 27 files 通过。既有批次授权满足内部转移，T03 状态 `ready_for_next_task`，没有新增人工门。

- 2026-07-19：P001 T01 合同内核已完成。初始 Red 为模块缺失，Green 9/9；Spec Review `changes_requested / 56` 的 1 Critical+3 Important 经攻击测试整改后复审 `approved / 100`；Quality Review `changes_requested / 84` 的深层可变性问题经 JSON list/mutation/hash 攻击整改后复审 `approved / 100`。最终主代理验证 pytest `12 passed`、Ruff、mypy 通过。T01 状态仅为 `ready_for_next_task`，依据既有 T01–T08 连续授权进入 T02/T03/T05/T07 并行层，不新增人工确认。

- 2026-07-19：`uroborus` 回复“授权进行开发实施”，一次授权覆盖 P001 T01–T08 本地产品代码、测试、独立代码评审和同范围整改循环；不包含正式发布、Git、远端或部署。项目进入第 5/8 步“开发实现”，当前 T01 合同内核进行中。

- 2026-07-19：用户要求把正式设计转换为实施计划和代码任务。P001 生成主计划、主 TaskCard、8 个纵向代码任务、scope anchor、validator、自审和 Review 输入；作者最终 `194/194`。首轮独立 Review `changes_requested / 89 / 0-1-0` 发现 T06/T04 fixture owner 冲突；按技术核实将跨切片断言唯一移到 T08，复审 `approved / 96 / 0-0-0`。计划 SHA-256 `fd6c7600...2a9f`，Decision `20e2e2c...e839`。当前无开放 Finding；未修改 `src/`/`tests/`，下一步需一次代码实施授权。

- 2026-07-19：`uroborus` 明确批准完整 R020 设计内容并授权正式发布与发布后验证。事务 `DESIGN-RELEASE-TX-R020-G001` 原子写入 49 个目标，将 docs 由 68/17 迁移为 37/7；formal after-image root `7bf3fcd9…ea8c`。事务内与独立新鲜复验均为 pytest 287/287，十个测试消费者 Ruff、CAS、syntax 和 diff check 通过。默认 UV 用户缓存的沙箱拒绝经事务缓存单变量复验确认为环境路径问题，无需改实现或回滚。R020 状态 `released`，本轮没有用户待办。

- 2026-07-19：用户连续授权范围已执行到唯一停止点。R019 未激活树精确回滚；R020 纳入 10 个测试消费者、doc-map 和 49 项正式事务合同。R1 `R020-I-001` 经技术核实后最小修复，R2 独立复审 `APPROVED / 100 / 0-0-0`；真实离线 `uv run pytest` 287/287。候选 root `17ea01a3…6230`、manifest `91263f32…38b6`、Decision `f2d92420…e693`。当前等待人工精确哈希批准。

- 2026-07-18：用户确认发布后验证器根因并授权最小修复。TDD 回归由 `37/68` RED 转 GREEN，正式复验 38/38。随后全仓 pytest 后像为 28 failed/259 passed，精确前像隔离对照为 2 failed/285 passed；差分确定 27 个新增失败来自 10 个测试文件仍绑定退役 `docs/04-project-development` 路径。根因是 R019 声明 tests 为 required consumer，却未把真实测试纳入 exact write set，也未在 release-ready 门运行仓库 pytest。Finding `R019-RELEASE-C-004` 已登记；未回滚、未激活、未改测试。

- 2026-07-18：`uroborus` 授权基于已批准 R019 执行正式设计发布事务。事务完成 68 文件/17 目录到 37 文件/7 目录迁移，38 个目标 after-image root 为 `d887ca63...18002`，写入阶段校验 0 失败。发布后复验命令因验证器先执行发布前基线检查而误报 `37/68`；正式树仍处于 `formal_tree_committed_pending_activation`，回滚副本保留，未追加 `released`。根因报告已形成，按调试门等待人工确认后再做最小修复与最终复验。

- 2026-07-18：`uroborus` 回复“批准 R019”，精确绑定 candidate root `768969d5...e00`、manifest `36bf78de...6fb`、独立 Decision `83a246a8...250` 和 final-hygiene receipt `930cdcd9...b46`。批准登记前只读 CAS 核验确认 24 present / 3 absent 均未漂移。R019 状态改为 `candidate_approved`；该批准不授权正式设计发布、Git、远端或部署，下一 Gate 为正式设计发布事务授权。

- 2026-07-18：用户授权按 `R018-RELEASE-C-001..003` 编制 R019 并自动完成作者验证、独立只读复审及必要整改循环。R019 R1/R2 的 1 Critical、2 Important 均经技术核实和同范围整改关闭；R3 最终 `approved / 100`，0/0/0 Finding。required `63/63`、full `1321/1321`、review gate `84/84` 和唯一一次 final hygiene `24 present / 3 absent / 27 passed` 均通过。精确 candidate root `768969d5...e00`、manifest `36bf78de...6fb`、Decision `83a246a8...250`；当前只停在 R019 精确哈希人工批准门，未执行正式发布、Git、远端或部署。

- 2026-07-18：`uroborus` 已授权基于批准 R018 执行正式设计发布事务。预检在正式树写入前发现 `R018-RELEASE-C-001..003`：正式 source 路径未登记，Builder basename 合同与正式路径不兼容，且 PRD/需求矩阵/文档索引 CAS 前像仍绑定 R003 发布前哈希。为保持精确候选哈希、CAS 和未登记写入阻断规则，事务未触碰 docs、未追加 released；下一 Gate 是授权修订候选的编制、作者验证和独立只读复审，停止于新候选精确 hash 人工批准。

- 2026-07-18：`uroborus` 通过“批准 R018”与“R018 是什么？通过”批准此前精确确认包绑定的 candidate root `012d1d3f...6305`。批准登记前后 24 个在场文件 hash/bytes 与 final receipt 相符、3 个 no-transfer async 路径仍 absent。R018 候选现为 `candidate_approved`；正式设计发布、Git 和远端操作没有被该批准授权。

- 2026-07-18：R018 R5 独立只读复审最终 `approved / 100`，0 Critical、0 Important、0 Minor；唯一格式兼容项由同一 Reviewer 最小修正并重新绑定，review gate `84/84`。唯一一次 final hygiene 证明 24 present / 3 no-transfer async absent、27/27，receipt `R018-G001-FINAL-HYGIENE-a380f7e1d0a20390` 已落 ledger。当前精确 candidate root `012d1d3f...6305` 等待人工批准；没有后台任务，未执行正式发布、Git 或远端操作。

- 2026-07-18：R018 R4 独立复审为 `changes_requested / 94`，0 Critical、1 Important；预算项已关闭，只剩 registry/result 同步变更绕过权威 hash。R5 已从 source 54 seeds + 6 contracts 独立派生完整 registry，并跨 report identity/reuse/manifest 绑定 hash，五类组合 mutation 全部拒绝；作者 full `1293/1293`。新 root `012d1d3f...6305` 和 R5 input `23be854e...6410` 已派发，用户无需操作。

- 2026-07-18：R018 R3 独立复审为 `changes_requested / 88`，0 Critical、2 Important。R4 已把 required result ID 与冻结 registry 精确绑定，并为 12 个预算 seed 建立独立期望表及逐项 8 类 drift mutation；作者 `60/60`、`86/86`、full `1283/1283`。新 root `4c3b146e...8961` 和 R4 review input `ed182fc5...6a14` 已派发同一 Reviewer，用户无需操作。

- 2026-07-18：R018 R2 独立复审为 `changes_requested / 80`，0 Critical、2 Important。R3 已补齐完整 reuse eligibility、实际 package normalized command、36 组 state matrix、12 个预算边界和 10k/100k 全量性能投影；作者 `60/60`、`86/86`、full `1281/1281`。新 root `9b62e085...421b` 和 R3 review input `57473702...00665` 已派发同一 Reviewer，用户无需操作。

- 2026-07-18：R018 首轮独立评审为 `changes_requested / 58`，Finding 1 Critical、4 Important，涉及未执行 test seeds、正式 15+5 identity、transfer CAS、writer provenance 和 final receipt。作者在 R018 授权写集内完成整改：60 项 exact required registry 全运行，full `1274/1274`；新 root `1e49b292...46b8d`，R2 review input `ccb233d0...2be45` 已派发同一 Reviewer，用户无需操作。

- 2026-07-18：`uroborus` 批准 P022 精确 SHA-256 `c3d6a598...e2b1`，授权自动执行 R018 候选编制、作者验证、独立只读复审及必要整改循环，只在 R018 精确候选哈希人工批准门停止；正式发布、Git 和远端操作仍未授权。

- 2026-07-18：P022 独立只读复审完成，Decision `approved / 97`，0 Critical、0 Important、0 Minor；`P021-I-001` 及 P020/P019/P018 继承项全部 closed。20/20 冻结 hash、Red、author 232/232、package 257/257 与 R018 0/27 均经主流程复核。当前进入精确 P022 计划 SHA-256 人工批准门，未生成 R018，未执行正式发布或 Git/远端动作。

- 2026-07-18：用户授权按 `P021-I-001` 编制并复审 P022。P022 将 hygiene/final receipt 升级为 branch-aware v2，作者验证 `232/232 passed`，冻结 review input `c3415225...b3f1`；当前继续派发原 Reviewer，只允许其写一份 P022 Decision。未生成 R018，未执行正式发布或 Git/远端动作。

- 2026-07-18：P021 独立复审完成，Decision `changes_requested / 88`，0 Critical、1 Important、0 Minor。`P021-I-001` 确认 no-transfer 与静态 24/3→27 hygiene/final manifest 冲突：合法 no-transfer 应为 pre-T06 21 present/6 absent、final 24 present/3 async absent；transfer 才是 24/3 和 27。P020-I-002 closed，P020-I-001/I-003 open；结果完整性核验通过，P021 不得进入人工计划批准。下一 Gate 是用户授权编制并复审 P022。

- 2026-07-18：用户授权按 `P020-I-001..I-003` 编制并复审 P021。P021 已把 quick verification 改为 session-level absolute deadline + 5000ms reserve + remaining-budget admission，分离 no-transfer/transfer；把 15 字段 execution identity 与结果端 20 字段 reuse key 分离；以 control-plane ArtifactWriteAttestation 和 27 文件外 FinalHygieneReceipt 建立 provenance。作者验证 `226/226 passed`，当前进入独立只读复审派发 Gate；未生成 R018，未执行正式发布或 Git/远端动作。

- 2026-07-18：P020 独立复审完成，Decision `changes_requested / 78`，0 Critical、3 Important、0 Minor。P019-M-001 已关闭，P019-I-001/I-002 仍开放；新增 `P020-I-001..I-003`，分别要求 session-level 60 秒预算与 dispatch reserve/双分支、执行前 `EvidenceExecutionIdentity` 与执行后 EvidenceReuseKey 分离、权威 writer attestation 和 27 文件外 final receipt。Decision 完整性与技术依据核验通过，P020 不得进入人工计划批准。下一 Gate 是用户授权编制并复审 P021。

- 2026-07-18：用户授权按 `P019-I-001`、`P019-I-002`、`P019-M-001` 编制并复审 P020。P020 已补齐 versioned RegressionTask、`fork_context=false`、59s/60s/61s、L1-L4 预计/实际转移、正式五字段 CAS、完整状态与 parent Gate；把内容卫生改为 T05 的 24 present/3 absent 和 T06 的 final 27，并修正 anchor `27-path` 同源计数。作者验证 `228/228 passed`，当前进入独立只读复审 Gate；未生成 R018，未执行正式发布或 Git/远端动作。

- 2026-07-18：P019 独立复审完成，Decision `changes_requested / 82`，0 Critical、2 Important、1 Minor。关闭 P018 七项中的 5 项，`P018-I-005` 与 `P018-M-001` 仍开放；新增/细化 `P019-I-001`、`P019-I-002`、`P019-M-001`。Decision 完整性和技术依据核验通过，P019 不得进入人工计划批准。下一 Gate 是用户授权编制并复审 P020。

- 2026-07-18：用户授权“按7项Finding编制并复审P019”。P019 已统一 candidate root、progress conflict 失败码、L1-L4、EvidenceReuseKey、60 秒 durable async V4、27 路径 registry 和 content-hygiene；作者验证 `242/242 passed`，冻结 review input `b533a572...9fdb`。下一步真实派发原 Reviewer `/root/p018_plan_review`；P019 approved 前不提交人工计划批准，P019 人工批准前不生成 R018。

- 2026-07-18：P018 独立只读计划复审完成，Decision 为 `changes_requested / 71`，Finding 为 0 Critical、6 Important、1 Minor；阻塞项分别涉及候选身份、progress conflict 失败码、验证层定义、EvidenceReuseKey、V4 异步路径和 exact write set，另有未跟踪新文件 `git diff --check` 空通过 Minor。六份 UI `N/A` 全部接受，限无产品 GUI。P018 不可提交人工计划批准；下一 Gate 是用户授权编制 P019 整改版。

- 2026-07-18：用户明确“授权独立子代理只读复审 P018”。人工授权以后置 ledger 事件绑定冻结 review input SHA-256 `9189747a...e6716` 和计划 SHA-256 `79dfb17c...a9f9`；独立 Reviewer `/root/p018_plan_review` 以 `fork_context=false` 派发，只能读取冻结输入并写一份 Decision，禁止修改计划、Task Brief、正式文档、代码、Memory、ledger 或 Git 状态。

- 2026-07-18：用户授权编制新的设计重基线计划 `TASK-DESIGN-001-P018`。AI 基于 PRD/需求矩阵 `v4.0.0` 和索引 `v2.0.0` 冻结 P018 主计划、T01..T06 六个 Task Brief、scope anchor、validator、作者验证、自评和独立复审输入。首轮作者验证真实失败 8 项，逐项补齐 `NFR-VIS-002/003/004` 与 `REQ-AI-WORKFLOW-042/045/046/047/054` 后 `255/255` 通过。当前停在独立只读计划复审授权门；未生成 R018，未修改正式设计/产品代码/测试，未执行 Git 或远端动作。

- 2026-07-18：`uroborus` 批准 R003 精确 SHA-256 `4515c91e...34665b`、确认 `MAJOR` 并授权正式需求发布。AI 将 `REQ-CHANGE-AI-EXEC-VISIBILITY-001` 融入 PRD `v4.0.0`，同步需求矩阵 `v4.0.0` 和文档索引 `v2.0.0`；正式发布不恢复 P017/R017，不包含新设计、实现或 Git/远端动作。

- 2026-07-18：R002 同一 Reviewer 复审为 `changes_requested / 78`，原 8 项关闭 6、开放 2，新增 2 个 Important。R003 改用唯一 snapshot reducer + 纯 position adapter，evidence 重算 hash 并绑定当前 Gate，权限侧信道和十类旧资格进入真实 evaluator，scope 前像由编制前 ledger 事件/独立 anchor 锚定，回复变更明确为 `MAJOR`。首轮 exact write set 验证真实失败 6 项，修正完整路径后 `124/124` 通过。

- 2026-07-18：用户授权独立子代理只读评审 `TASK-REQ-005-R001`。Reviewer `/root/req005_review` 在隔离上下文核对 9 个冻结 hash 后给出 `changes_requested / 50`，发现 1 Critical、7 Important。R002 将状态改为不具 Gate 权限的派生处置维度，绑定唯一正式 lifecycle artifact/stage-map/H，闭合 Review 派发、证据恢复 CAS、权限过滤和 P017/R017 十类旧资格失效，并用 104 条语义/攻击断言验证通过。下一步为同一 Reviewer R002 复审。

- 2026-07-15：Reviewer Arendt 对 R009 的同一 Reviewer 只读复审为 `changes_requested / 66`，5 项关闭，`I-003` 和 `I-006` 因验证假通过保持开放。R010 已精确闭合 13 条 canonical edge、9 个 ActionSpec 上游引用和 11 个接口；56 个 fixture 由 56 个逐编号 evaluator 执行 183 条语义断言，69 个 mutation 各有唯一 operator、目标和已发布语义探针绑定。56/56、69/69、9 个定向攻击、全部旧 profile、需求影响、158 项暂存发布和三处失败恢复通过；下一步交同一 Reviewer Arendt 复审，通过后停在人类四哈希确认门。

- 2026-07-15：Reviewer Arendt 对 R008 的独立只读评审为 `changes_requested / 52`，0 Critical、6 Important、1 Minor。七项均已由主流程复现，并在同一 `TASK-DESIGN-001` 内形成 R009：修正 P006 绑定和 9 个需求指针，补齐九步 typed dataflow、工具回执、SQLite 复合外键与完整校验快照，把 56 条夹具和 69 条变异改为逐条实际执行，并清理过期描述。56/56、69/69、SQLite 探针、全部 profile 和 7 个定向篡改探针通过；下一步由同一 Reviewer Arendt 复审，复审通过后停在人类四哈希确认门。

- 2026-07-15：用户批准 `TASK-DESIGN-001-P006` 精确哈希并激活条件化写集。R008 已在同一 TaskCard 内完成：`WF-CTL-010` 九步链、4006 条 Catalog、77 条需求覆盖、9 张 SQLite 表、216 状态组合、9 工具、137 字段、56 fixture 和 69 类风险绑定；IA 保持 36 文件/7 目录/68 处置。`bootstrap、cp01、cp02、cp03、cp04、requirement-impact、final` 全部退出 0，source-red 按预期退出 2，158 项暂存发布和三处失败恢复通过。四哈希为设计 `637c52e4...47e2`、Catalog `fba1bf31...dc92`、validator `6db443ff...a69`、发布清单 `5936fbdf...590e`。当前等待独立只读评审授权，尚未派发 Reviewer。

- 2026-07-15：用户授权在原 `TASK-DESIGN-001` 内修复 P005 的 5 个 Important 和 1 个 Minor，生成 P006，并由同一 Reviewer Popper 只读复审。P006 补齐九步会话链、R008 IA 候选/生成器、条件化写集和状态事件、真实 validator、R008 四哈希停止点及 Excel 绝对路径；作者验证 `66/66 passed`。Popper 复审 `approved / 96`，原六项全部关闭，新增 1 个任务卡状态投影 Minor 已随结果登记关闭。当前等待用户批准计划 SHA-256 `bdeff4bb...3c5e`。

- 2026-07-15：用户授权独立 AI 子代理只读评审 `TASK-DESIGN-001-P005`。Reviewer Popper 写集为空，结论 `changes_requested / 64`：0 Critical、5 Important、1 Minor。问题涉及九步工作流遗漏会话适配器、R008 docs 信息架构产物缺失、TaskCard/ledger/memory 状态转换写集缺失、校验命令不可执行、依赖已禁止的 P004 发布事务，以及 Excel 正式输入路径未冻结。P005 计划本体未修改，当前停在整改授权门。

- 2026-07-15：用户指令“进行下一步”已路由到原 `TASK-DESIGN-001` 的 PRD `v3.1.0` 影响重基线，不新建任务。当前计划重写为 `TASK-DESIGN-001-P005`，计划 SHA-256 `fdc06418...7c58`，作者验证 `22/22 passed`，评审输入已冻结。P005 将增量设计拆为输入覆盖、事实与 SQLite、快照与准确性、意图与工具、HTML/Excel/权限、验收与 R008 冻结六包；当前停在独立计划评审授权门，未修改 R007 设计候选或正式文档。

- 2026-07-15：用户明确批准将 `TASK-REQ-002-R014` 正式写入 PRD。已在原任务登记人工批准，将 `REQ-CHANGE-WF-CTL-010-001` 完整融入 `WF-CTL-010`，同步需求矩阵、文档索引和最小记忆；批准候选归档，冻结机器合同由发布清单绑定为受控设计输入。正式化校验 `35/35`、文档树 56 页、相关测试 `33 passed`，任务状态 `formalized`。本轮未修改设计或实现，未提交、未 Push、未创建 PR。

- 2026-07-13：`GO-BACKEND-SKILL-001 / TASK-SKILL-001` 已按人工变更请求升级 Gin + GORM + Logrus + Consul 开发 skill：补充 GitHub 候选取舍、Ponytail/YAGNI、单次调用 helper 禁令、嵌套硬上限、Go 式对象设计、模式采用门槛和 fallback/兼容扩张禁令；模板从 9 文件减到 6 文件。revision 4 独立 review 经 `88 -> 92 -> approved / 98` 收敛，3 个 finding 全部关闭，无新增或回归。当前 `pending_human_confirmation`，人工确认后才使用 `gitcommitzh` 提交本任务范围。

## 文档与工厂结构治理

- 2026-07-08：`DOC-FACTORY-RESTRUCTURE-001` 已改为破坏性重做型全量文档结构迁移。正式保留 `task-execution-contract.md`、实施计划、当前设计白名单、测试/发布/运维/追踪矩阵和必要 draw.io 资产；删除旧 discovery / requirements / design / development-process / evolution 页面、旧静态原型、`.factory/process/`、`.factory/memory/history/`、`.factory/pm/generated/`、空资产索引和临时备份资产。当前状态：`ready_for_review`；下一动作：`independent_review`。
- 2026-07-09：用户反馈上述迁移仍未讲清 `docs` 目录、记忆目录、设计目录、领域/模块和任务拆分逻辑。已新增 `TASK-002-docs-memory-structure-redesign` 任务简报和报告，建议采用“目录是树，关系是矩阵”。该版本后续已被最小结构草案取代。
- 2026-07-09：按用户 `ponytail` 反馈重写 TASK-002 草案，删除上一版多层设计目录和 memory 分组建议。新目标是最小 docs 白名单、最小 memory 白名单、统一 `document-change-log.md`，并明确讨论方案不得直接新增正式 `docs` 文档。当前状态：`needs_user_input`；下一动作：`user_confirm_minimal_structure_then_rewrite_plan`。
- 2026-07-09：用户再次澄清 TASK-002 重点是会话行为必须全部进入固定工作流，不允许随性改代码、写文档或改任务。已重写报告为三层事实结构、会话入口总规则、路由包模板、会话行为与工作流表、写入位置规则和 docs 写入锁；方案讨论只能进入 work item 草案或报告，正式 docs 只有 document merge gate 后才能写。当前状态：`needs_user_input`；下一动作：`user_confirm_workflow_structure_then_rewrite_plan`。
- 2026-07-09：按用户要求执行下一步写需求任务。复用 `FLOW-CONTRACT-001`，新增 `TASK-REQ-001-ai-collaboration-workflow-requirements`，输出 `REQ-AI-WORKFLOW-001` 需求草案、任务简报和需求报告；该需求作为 `DOC-FACTORY-RESTRUCTURE-001 / TASK-002` 的上游需求。当前状态：`requirements_ready`；下一动作：`user_confirm_requirements_or_request_changes`。
- 2026-07-09：按用户反馈补充需求草案，新增 `REQ-AI-WORKFLOW-006`，要求项目化会话最终回复必须解释本轮做了什么、写到了哪里、当前状态、需要用户确认什么、下一步、未做事项和验证结果；后续设计必须定义不同会话类型的回复模板。
- 2026-07-10：按用户要求解释 `WorkItem` 并执行下一步。已复用 `FLOW-CONTRACT-001`，新增 `TASK-WF-PRD-001-requirement-clarification-to-prd-workflow`，输出 `WF-REQ-TO-PRD-001` 工作流草案和任务报告，定义“需求澄清到完整 PRD”的节点、用户动作、AI 动作、输入依据、输出产物、写入位置、停止点和回复模板。当前状态：`requirements_ready`；下一动作：`user_confirm_requirement_to_prd_workflow_or_request_changes`。
- 2026-07-10：按用户反馈补充中间草案处置规则。正式方案形成后，草案应删除或归档；归档文件默认禁止 AI 读取，只有当前 TaskCard、ledger、review 或用户明确指向时才能读取。
- 2026-07-10：用户确认中间草案处置策略后，已执行 PRD 编写任务 `TASK-PRD-001-ai-collaboration-workflow-prd`，输出 `PRD-AI-WORKFLOW-001` 草案、任务卡、PRD 报告和 `prd.summary`。当前状态：`requirements_ready`；下一动作：`user_review_prd_or_request_changes`。
- 2026-07-10：用户确认 `PRD-AI-WORKFLOW-001` 草案并要求进入设计阶段。已将 PRD 标记为 `human_approved_for_design`，创建并执行 `TASK-DESIGN-001-ai-collaboration-workflow-design`，输出 `DESIGN-AI-WORKFLOW-001` 设计草案和设计报告。当前状态：`design_ready`；下一动作：`user_review_design_or_request_changes`。
- 2026-07-10：用户纠正任务边界并要求回到原 `TASK-PRD-001`。已把正式落档、版本更新、验证、评审和草案处置归入同一任务，新增 `drafts/document-change.md`，暂停 `TASK-DESIGN-001`。当前缺少真实变更人、审核人、批准人及独立子代理评审授权；状态 `needs_project_information`。
- 2026-07-10：用户补齐人员信息并授权独立只读评审。已生成正式 PRD、需求矩阵和文档索引候选稿及验证证据；临时文档树 `docs-stratego` 通过 `pages=56`，需求和追踪计数、JSON 与格式检查通过。当前 `ready_for_review`，正式版本未生效。
- 2026-07-10：独立评审 Iteration 1 为 `changes_requested / 74`。4 个 Important 和 2 个 Minor 已修复并验证：旧需求语义 diff 无差异，5 条旧 NFR 完整，TaskCard 口径和状态一致，候选哈希绑定临时树，修复后 `docs-stratego pages=56`。当前 `ready_for_re_review`。
- 2026-07-10：Iteration 2 有效独立复审为 `changes_requested / 86`。I-05 和 M-03 已修复：条件式 TaskCard 规则在 REQ、AC、NFR、矩阵四方一致；会话卡已精简，历史摘要已有读取规则。记录当时进入 `ready_for_re_review`，等待 Iteration 3。
- 2026-07-10：Iteration 3 首次执行超时且无结论；Retry 为 `changes_requested / 88`，确认前 7 项无回退，仅 I-05 完整句精确一致性未闭环。现已统一四处完整句，精确检查为 `PRD 3 / 矩阵 1`，重新验证临时文档树通过，等待 Iteration 4。
- 2026-07-10：Iteration 4 独立复审为 `approved / 100`，无 Critical、Important、Minor，8 个历史问题全部关闭。当前 `pending_human_confirmation`；用户明确批准前不得覆盖正式源、激活版本、处置草案或恢复设计任务。
- 2026-07-10：用户在人工确认门退回旧范围候选。反馈指出需求必须覆盖完整软件开发生命周期 Agent，定义所有阶段、工作流和原子动作的规则、依据、产物、工具、Gate 和回复，禁止大模型自由发挥。旧 Iteration 4 结论只对旧范围有效，任务恢复为 `changes_requested`。
- 2026-07-10：已在原 `TASK-PRD-001` 重写 `v3.0` 候选：新增 28 条治理需求，总计 40 条；第 10 章登记 123 条核心 Workflow；第 11 章定义 ActionSpec、ActionRun、RouteRule、ToolPolicy 和继续/停止状态机；矩阵、索引和旧草案状态已同步。旧需求语义、ID/Workflow 结构、候选绑定和 `docs-stratego pages=56` 验证通过，当前 `ready_for_review`。
- 2026-07-10：在派发新独立评审前，用户进一步明确第一层必须是四套规范体系。原 v3 验证证据和评审输入已标记 superseded/not dispatched；当前继续在同一 TaskCard 修订，不新建任务。
- 2026-07-10：已新增 REQ 041 至 048 和 PRD 第 10 章四套规范：14 阶段流程表、角色/决策矩阵、人和 AI 工作规范、Session 状态机、回答/落盘/停止/交接规则、Artifact 分层和阶段输入输出基线。48 条治理需求、矩阵、123 条 Workflow、旧需求保留和 `docs-stratego pages=56` 通过，当前等待用户确认第一层结构。
- 2026-07-10：用户在确认门指出未批准候选被错误标记为正式版本。已在同一 `TASK-PRD-001` 修正 `REQ-AI-WORKFLOW-009`、`048`、文档规范和 `WF-CTL-009`：候选使用 `TASK-PRD-001-R001` 及 hash，审核/批准绑定该修订；正式版本只在发布事务成功时分配；退回、未批准和发布失败记录不进入正式版本历史。当前等待用户确认四套规范和版本规则。
- 2026-07-10：用户要求“用户与角色”明确标注人类和 AI。已按刚建立的修订规则使 `R001` 失效并生成 `TASK-PRD-001-R002`；角色目录新增`主体类型`，拆分人类 Reviewer 和独立 AI Reviewer，新增人工批准人、Role Assignment、Node/ActionRun `actor_type`、权限阻断 AC 和 `GAP-AI-011`。当前等待用户确认四套规范、角色分类和版本规则。
- 2026-07-11：用户要求补齐 Artifact 分层、事实资格、生命周期和验收要求。已在同一 `TASK-PRD-001` 生成 R003：53 条治理 REQ、11 条治理 NFR、17 类 Artifact、14 个事实域、14 项 Artifact 量化验收；R002 已失效。候选与矩阵/索引、隔离文档树和 `docs-stratego pages=56` 验证通过，当前等待需求层确认，不是最终发布批准。
- 2026-07-11：用户确认 R003 顶层基线并授权展开 123 条 Workflow。R004 首次映射因 9 条高风险流程缺固定 human 授权节点失效；R005 补齐 15 / 15 高风险授权后，独立评审 `changes_requested / 83` 发现两项真实 review 节点由作者 AI 执行。R006 已修正 Reviewer selector、独立评审 Gate 和验证器语义规则，独立复审 `approved / 100`，无 Critical/Important/Minor；当前等待用户最终确认，正式落档尚未执行。
- 2026-07-11：用户明确批准 R006 四个冻结 hash 正式落档。已在原 `TASK-PRD-001` 内发布 PRD `v3.0.0`、需求矩阵 `v3.0.0` 和文档索引 `v1.0.0`，同步追踪图、任务报告和 memory，删除被正式事实取代的旧草案，并把 R006 审核候选与失效设计归档。正式文档树、发布语义、123 条 Workflow 映射和 JSON 结构验证均通过；状态 `formalized`，下一动作 `start_TASK-DESIGN-001_rewrite_from_prd_v3.0.0`。
- 2026-07-11：用户要求进行下一项“基于 PRD v3.0.0 重写完整设计”，并询问是否先理解、建任务和计划再执行。已确认设计任务卡早已存在，不新建重复任务；重写 WorkItem 唯一 `plan.md` 为 `TASK-DESIGN-001-P001`，并修正任务边界，使设计草案、review、人工批准、正式落档、版本更新和草案处置都留在同一 TaskCard。计划结构自检通过：10 个工作包、123 条 Workflow、597 动作槽、369 场景；当前等待独立计划评审授权或人类计划评审，设计未执行。
- 2026-07-11：用户授权独立 AI 子代理只读评审 P001。Reviewer 返回 `changes_requested / 68`；已在同一 TaskCard 处理 7 个 Important 和 2 个 Minor，生成 P002。P002 补齐 76/76 逐 ID 覆盖、1089 个身份源指针、1359 个待设计槽、2448 条总迁移、17 方法域、对象/字段 owner、持久 validator、补偿发布事务、CP-01 至 CP-04 和 UI N/A Reviewer 裁决字段。机器校验通过，当前等待 P002 新授权或人类 Reviewer；P001 授权不得沿用，设计未执行。
- 2026-07-11：用户授权独立 AI 子代理只读复审 P002。Reviewer 独立复算 hash 和核心计数后返回 `changes_requested / 74`，0 Critical、5 Important、0 Minor；8 个 UI N/A 全部接受。已在同一 TaskCard 生成 P003：新增 `prompt_template`，把 validator bootstrap 提前到 WP-01 并定义 7 个 profile，增加 checkpoint scope/影响重审，批准前冻结 22 个物理路径和四 hash，并把发布改为独占写入、逐目标条件写入/恢复、最后 `released` 生效。当前等待 P003 新授权或人类 Reviewer；设计未执行。
- 2026-07-11：用户授权独立 AI 子代理只读复审 P003。Reviewer 返回 `changes_requested / 86`，0 Critical、2 Important、0 Minor；P002 的 4 项已关闭，正确生效顺序仍有状态循环，8 个 UI N/A 继续 accepted。已在同一 TaskCard 生成 P004：人工批准和 `released` 均定义固定 schema、稳定幂等键、冻结 payload、append/fsync/readback、重复冲突与不确定恢复；TaskCard 加入第 23 个发布目标；六个 Memory 文件与 TaskCard 先写待生效投影，由同一 `released` 同时激活正式事实、TaskCard `completed` 和 WorkItem `design_formalized`。当前等待 P004 新授权或人类 Reviewer；设计未执行。
- 2026-07-12：用户回复“现在我批准一次性授权”。按紧邻会话约定，用户以 `HUMAN_REVIEWER` 和人工批准人身份批准 P004、授权开始设计，并持续授权 CP-01 至 CP-04及最终设计候选的独立 AI 只读评审；中间执行、最多两轮反馈修正和复验自动继续。授权不含最终正式落档、提交、push、PR、merge 或部署。当前进入 WP-01。
- 2026-07-12：WP-01、WP-02 完成后，CP-01 R001 独立评审为 `changes_requested / 52`，指出 8 个 Important 和 1 个 Minor。第 1 轮自动整改已建立全局冲突优先级、确定性授权求值、唯一 Artifact 定位/处置、双向事实绑定、逐类别闭合状态图、真实 evaluator fixture、WP-02 coverage 结算和可独立重算共享 hash；R002 已追加冻结，等待同一 Reviewer 只读复审，尚未进入 WP-03。
- 2026-07-12：CP-01 R002 复审为 `changes_requested / 64` 后完成第 2 轮整改并冻结 R003；R003 复审提升到 `82 / 100`，但仍有 2 个既有 Important，触发“两轮上限/重复 finding”停止条件。当前人工决策包提供 A 例外整改、B 风险接受、C 需求变更三种选择；未明确决定前不生成 R004、不进入 WP-03。
- 2026-07-12：CP-01、CP-02 已分别在 R005 由独立 Reviewer 评审为 `approved / 100` 并关闭；WP-05 至 WP-07 已完成。CP-03 R001 冻结设计 `16015a3a...24af`、Catalog `1e00ef4d...d2e`、validator `99faf909...3fd1`，完整 `cp03` 对 3943 条记录退出 0；Reviewer `Russell` 只读评审中，写集为空，下一动作 `await_CP03_R001_independent_readonly_review`。
- 2026-07-12：CP-03 R001 独立评审为 `changes_requested / 30`，3 Critical、6 Important、1 Minor；10 项均经独立复现后完成第 1 轮整改。当前 `cp03@0.3.0`、WP-05、WP-06、CP-02、WP-03、CP-01 和 bootstrap 回归通过，原攻击探针全部拒绝。因高风险 ActionSpec 绑定变化，当前候选须同时形成 CP-02 R006 影响快照；下一动作 `freeze_CP03_R002_and_CP02_R006_then_same_reviewer_readonly_rereview`。
- 2026-07-12：CP-03 经两轮自动整改后仍有 3 项开放问题，用户批准 R004 定向例外整改。R004 完成红绿验证并由同一独立 AI Reviewer Russell 复审为 `approved / 100`；CP-02 R008 当前候选影响也为 `approved`，10 项问题全部关闭。当前停在人工转段门，等待决定关闭 CP-03 并进入 WP-08 或暂停；未正式落档、提交或创建 PR。
- 2026-07-12：用户确认关闭 CP-03 并继续到下一人工确认门。WP-08 已消除旧 `cp04` 对 369 个延期测试的假通过，形成 369 个可执行场景、1 个 Catalog 完整性测试、12 个真实内存变异和 4 个正式输入兼容检查；完整 `cp04@0.2.0` 对 3944 条记录错误 0。CP-04 R001 已冻结并交独立 AI Reviewer Socrates 只读评审；WP-09 尚未开始。
- 2026-07-12：CP-04 R001 独立评审为 `changes_requested / 42`，2 Critical、2 Important。final 状态互斥、场景语义交换、兼容路径伪造和负例登记脱节均已复现并在第 1 轮整改中融入原候选。R002 完整 `cp04@0.3.0` 错误 0，369/369、16/16、4/4、2524/2524 和 final 正例 1/1 通过；R002 已冻结并交同一 Reviewer Socrates 只读复审，WP-09 尚未开始。
- 2026-07-12：同一 Reviewer Socrates 对 CP-04 R002 复审 `approved / 100`，4 个原 Finding 全部关闭，开放、新增和回退 Finding 为 0，UI N/A 接受，写集为空。当前停在人工转段门；人类确认前不关闭 CP-04、不开始 WP-09。
- 2026-07-13：用户明确确认关闭 CP-04 并开始 WP-09。当前在原 TaskCard 内生成 `TASK-DESIGN-001-R001` 最终候选、待批准发布清单和最终评审包；授权不包含正式落档、正式版本生效、提交、Push 或 PR。

## 企业 AI 交付闭环评估

- 2026-07-07：`ENTERPRISE-AI-DELIVERY-001 / EAD-TASK-001` 已由执行任务卡 `EAD-TASK-001-COMPLETE` 推进到 `ready_for_review`，并按用户反馈补充正式评估报告 `reports/EAD-TASK-001-capability-assessment-report.md`。配套产物为 `reports/EAD-TASK-001-implementer-report.md`、`evidence/EAD-TASK-001-verification.md`、`reviews/EAD-TASK-001-review-input.md`；ledger 最新要求为 `independent_review`，未进入 `approved` 或 `complete`。

## 流程集成计划

- 2026-07-06：新增 `FLOW-CONTRACT-001` 草稿工作项，用于把用户关于四类场景、三层文档、记忆结构、PM、版本管理、领域模块、前后端设计和防跳步机制的讨论落为正式流程契约。已新增正式需求 `docs/04-project-development/03-requirements/process-workflow-contract-requirements.md` 和正式实施方案 `docs/04-project-development/05-development-process/process-workflow-contract-implementation-plan.md`，并登记 `.factory/workitems/FLOW-CONTRACT-001/brief.md`、`plan.md`、`ledger.jsonl`。当前尚未修改 skill，不能声明 skill 改造已完成。
- 2026-07-06：`FLOW-CONTRACT-001` 已补充整体黑盒测试、UI 测试、接口测试、测试环境启动、端口管理、启动记忆读取和非活跃任务降级规则。新增任务卡 `FLOW-TASK-013` 项目级测试治理和 `FLOW-TASK-014` 启动记忆 / 非活跃任务降级；当前仍是设计与计划阶段，未改 skill。
- 2026-07-06：`FLOW-CONTRACT-001` 按用户反馈修正启动记忆设计：不固定读取 `agent-session.md`、`runtime-brief.md`、`current-state.md` 三件套，而是条件读取链，够用即停；目标是生成小型会话卡，避免把压缩记忆重新扩张进上下文。
- 2026-07-06：`FLOW-CONTRACT-001` 实施前独立评审已通过。reviewer `codex-flow-contract-001-pre-reviewer-20260706` / subagent `019f3582-d446-7a22-b00a-1bf276a20770` 给出 `approved / 94`；review 文件为 `.factory/workitems/FLOW-CONTRACT-001/reviews/implementation-pre-review.md`。当前 gate 是 `pending_human_confirmation`，等待用户人工确认后才能进入实施。
- 2026-07-06：用户已确认 `FLOW-CONTRACT-001` 实施前评审通过，ledger 已写入 `human_approved`。下一阶段是按 `FLOW-TASK-001` 至 `FLOW-TASK-015` 逐项改造 workflow skill；每个任务必须产出 evidence、implementer report 和 review checkpoint，不能自批完成。
- 2026-07-06：按用户要求新增 `.factory/workitems/FLOW-CONTRACT-001/implementation-queue.md`，只登记顺序实施队列，不在本会话实施任务。`FLOW-TASK-001` 和 `FLOW-TASK-002` 作为设计交付已由实施前评审覆盖；下一新任务是 `FLOW-TASK-003`，之后严格按任务号顺序逐项实施。
- 2026-07-06：`FLOW-TASK-003` 已完成首轮实现并进入 `ready_for_review`，尚未独立 review、人工确认或关闭。小任务自循环下一步应停留在 `FLOW-TASK-003` 的独立 review；如 review 返回 `changes_requested`，继续在 `FLOW-TASK-003` 内修复和复审，不进入 `FLOW-TASK-004`。本轮只升级 `document-templates` 文档治理规则：正式文档登记、临时文档边界、中文版本信息、版本历史和导航 / doc-map 同步；新增 evidence、implementer report、review checkpoint 和结构测试。验证：`uv run pytest tests/test_sf_sp_010_documentation_navigation.py` 通过 `8 passed`。
- 2026-07-06：`FLOW-TASK-003` 独立 review 已通过，reviewer `codex-flow-task-003-reviewer-20260706` / subagent `019f35ba-c241-7432-ab2b-c063716ef7cf` 给出 `approved / 94`；无 Critical / Important，1 个 Minor 审计精度备注非阻塞。当前 gate 是 `pending_human_confirmation`，人工确认前不得进入 `FLOW-TASK-004`。
- 2026-07-06：用户已确认 `FLOW-TASK-003` 通过并允许进入 `FLOW-TASK-004`。`FLOW-TASK-004` 已完成首轮实现，升级 `requirements-engineering` 的四类场景、需求版本、baseline 影响分析、领域模块映射和 baseline 变更建议；新增 `tests/test_requirements_engineering_skill.py` 场景覆盖。验证：`uv run pytest tests/test_requirements_engineering_skill.py tests/test_superpowers_reference_migration.py` 通过 `8 passed`，ruff 通过。当前 gate 是 `ready_for_review`，不能进入 `FLOW-TASK-005`。
- 2026-07-06：`FLOW-TASK-004` iteration-1 独立 review 返回 `changes_requested / 86`，唯一 Important 为本摘要顶部仍停在 `FLOW-TASK-003 pending_human_confirmation`，与 queue / ledger 冲突；本轮按反馈同步当前焦点为 `FLOW-TASK-004 ready_for_review`，等待复审。
- 2026-07-06：`FLOW-TASK-004` iteration-2 独立复审已通过，reviewer `codex-flow-task-004-rereviewer-20260706` / subagent `019f3753-22d1-7601-acd8-155cede389e4` 给出 `approved / 95`；无 Critical / Important / Minor。当前 gate 是 `pending_human_confirmation`，人工确认前不得进入 `FLOW-TASK-005`。
- 2026-07-06：用户已确认 `FLOW-TASK-004` 通过并允许进入 `FLOW-TASK-005`，同时要求后续人工确认包必须包含最终审计审查问题报告，不能只输出评分。`FLOW-TASK-005` 已完成首轮实现，升级 `using-shanforge` 四类场景路由、baseline work item、缺 evidence 阻塞关闭、人工确认最终审计问题报告要求，并扩展黑盒流程 eval 场景。验证：`uv run pytest tests/test_black_box_workflow_eval.py` 通过 `7 passed`，ruff 通过。当前 gate 是 `ready_for_review`，不能进入 `FLOW-TASK-006`。
- 2026-07-06：`FLOW-TASK-005` 独立 review 已通过，reviewer `codex-flow-task-005-reviewer-20260706` / subagent `019f3760-ecda-71f2-b822-51fc8293bc5b` 给出 `approved / 96`；无 Critical / Important / Minor。最终审计问题报告为 `.factory/workitems/FLOW-CONTRACT-001/reports/FLOW-TASK-005-final-audit-issue-report.md`，阻塞问题 none，残留风险为当前测试主要是结构断言而非完整黑盒回放；该风险在任务范围内可接受。当前 gate 是 `pending_human_confirmation`，人工确认前不得进入 `FLOW-TASK-006`。
- 2026-07-06：用户已确认 `FLOW-TASK-005` 通过并允许进入 `FLOW-TASK-006`。`FLOW-TASK-006` 已完成首轮实现，升级 `project-memory` 事实源优先级、summary 不复制完整正式正文、PM generated 非事实源，并在 `doc-map.md` 固定事实源边界。验证：`uv run pytest tests/test_project_memory_skill.py` 通过 `5 passed`，ruff 通过。当前 gate 是 `ready_for_review`，不能进入 `FLOW-TASK-007`。
- 2026-07-06：`FLOW-TASK-006` 独立 review 已通过，reviewer `codex-flow-task-006-reviewer-20260706` / subagent `019f3770-c318-7633-bc60-cd35f21b7cd4` 给出 `approved / 95`；无 Critical / Important / Minor。最终审计问题报告为 `.factory/workitems/FLOW-CONTRACT-001/reports/FLOW-TASK-006-final-audit-issue-report.md`，阻塞问题 none，残留风险为当前工作树有大量跨任务未提交改动，后续提交必须只纳入 006 范围。当前 gate 是 `pending_human_confirmation`，人工确认前不得进入 `FLOW-TASK-007`。
- 2026-07-06：用户已确认 `FLOW-TASK-006` 通过并允许进入 `FLOW-TASK-007`。`FLOW-TASK-007` 已完成首轮实现，升级 `writing-plans` 和计划模板，强制包含设计方案、接口设计、UI 或 N/A、测试设计、开发、单测、review、集成测试，并增加缺测试设计、UI N/A 缺原因和占位语失败断言。验证：`uv run pytest tests/test_writing_plans_skill.py` 通过 `4 passed`，ruff 通过。当前 gate 是 `ready_for_review`，不能进入 `FLOW-TASK-008`。
- 2026-07-06：`FLOW-TASK-007` 独立 review 已通过，reviewer `codex-flow-task-007-reviewer-20260706` / subagent `019f377b-a477-7041-bd38-c788fbd7ae4a` 给出 `approved / 95`；无 Critical / Important / Minor。最终审计问题报告为 `.factory/workitems/FLOW-CONTRACT-001/reports/FLOW-TASK-007-final-audit-issue-report.md`，阻塞问题 none，残留风险为当前工作树有大量跨任务未提交改动，后续提交必须只纳入 007 范围。当前 gate 是 `pending_human_confirmation`，人工确认前不得进入 `FLOW-TASK-008`。
- 2026-07-06：用户已确认 `FLOW-TASK-007` 通过并允许进入 `FLOW-TASK-008`。`FLOW-TASK-008` 已完成首轮实现，升级 `executing-plans` 和 `subagent-driven-development` 任务 gate：缺设计方案、接口设计、UI 或 N/A 原因、测试设计时阻塞，缺 verification evidence / evidence / implementer report / review checkpoint / ledger 事件时不得进入 `ready_for_review`；同时固定子 agent 不决定下一步 skill。验证：`uv run pytest tests/test_execution_workflow_skills.py` 通过 `9 passed`，ruff 通过。当前 gate 是 `ready_for_review`，不能进入 `FLOW-TASK-009`。
- 2026-07-06：`FLOW-TASK-008` 独立 review 已通过，reviewer `codex-flow-task-008-reviewer-20260706` / subagent `019f378b-faa5-7d00-baa9-d4fae9e8b00d` 给出 `approved / 94`；无 Critical / Important / Minor。最终审计问题报告为 `.factory/workitems/FLOW-CONTRACT-001/reports/FLOW-TASK-008-final-audit-issue-report.md`，阻塞问题 none，残留风险为当前工作树有大量跨任务未提交改动且测试主要是结构断言；这些风险在任务范围内可接受。当前 gate 是 `pending_human_confirmation`，人工确认前不得进入 `FLOW-TASK-009`。
- 2026-07-06：用户已确认 `FLOW-TASK-008` 通过并允许进入 `FLOW-TASK-009`。`FLOW-TASK-009` 已完成首轮实现，升级 `requesting-code-review`、`receiving-code-review` 和 `verification-before-completion`：作者自检不能 `approved`，N/A 必须由 reviewer 明确接受或拒绝，关闭前必须检查新鲜命令、exit code、输出和 evidence，无 evidence 不能关闭，review / verification / human confirmation 不能互相替代。验证：`uv run pytest tests/test_review_workflow_skills.py tests/test_verification_debugging_workflow_skills.py` 通过 `13 passed`，ruff 通过。当前 gate 是 `ready_for_review`，不能进入 `FLOW-TASK-010`。
- 2026-07-06：`FLOW-TASK-009` 独立 review 已通过，reviewer `codex-flow-task-009-reviewer-20260706` / subagent `019f37c4-51d7-7a81-b964-be4811b5c2ab` 给出 `approved / 95`；无 Critical / Important / Minor。最终审计问题报告为 `.factory/workitems/FLOW-CONTRACT-001/reports/FLOW-TASK-009-final-audit-issue-report.md`，阻塞问题 none，残留风险为当前工作树有大量跨任务未提交改动且测试主要是结构断言；这些风险在任务范围内可接受。当前 gate 是 `pending_human_confirmation`，人工确认前不得进入 `FLOW-TASK-010`。
- 2026-07-06：用户已确认 `FLOW-TASK-009` 通过并允许进入 `FLOW-TASK-010`。`FLOW-TASK-010` 已完成首轮实现，新增 `document-templates` 的 project baseline、backend module、database、API 和 frontend UI 设计模板；模板均包含中文版本信息和版本历史，数据库模板包含 ERD，API 模板引用 `openapi.yaml`。验证：`uv run pytest tests/test_sf_sp_010_documentation_navigation.py` 通过 `9 passed`，ruff 通过。当前 gate 是 `ready_for_review`，不能进入 `FLOW-TASK-011`。
- 2026-07-06：`FLOW-TASK-010` 独立 review 已通过，reviewer `codex-flow-task-010-reviewer-20260706` / subagent `019f37df-9844-7860-98a8-3da39a7a5035` 给出 `approved / 95`；无 Critical / Important / Minor。最终审计问题报告为 `.factory/workitems/FLOW-CONTRACT-001/reports/FLOW-TASK-010-final-audit-issue-report.md`，阻塞问题 none，残留风险为当前工作树有大量跨任务未提交改动，后续提交必须只纳入 010 范围。当前 gate 是 `pending_human_confirmation`，人工确认前不得进入 `FLOW-TASK-011`。
- 2026-07-07：用户已确认 `FLOW-TASK-010` 通过并允许进入 `FLOW-TASK-011`。`FLOW-TASK-011` 尚未实施；下一步必须先读取该任务卡并在任务内完成 evidence、implementer report、review checkpoint 和独立 review，不能跳到 `FLOW-TASK-012`。
- 2026-07-07：按用户反馈补充 `FLOW-REQ-018` 输出持久化契约，明确任务完成后哪些内容返回当前会话、哪些写正式文档、ledger、evidence/report 或 memory summary。已更新正式需求、正式实施方案、`using-shanforge`、`project-memory` 和结构测试；验证 `uv run pytest tests/test_project_memory_skill.py` 通过 `6 passed`，ruff 通过。当前状态 `ready_for_review`，下一动作 `independent_review`；未执行 `FLOW-TASK-011`。
- 2026-07-07：继续按用户反馈补充当前会话可见性协议，要求任务开始、阶段切换、文件编辑前、关键命令前后、子 agent / 自循环返回、长时间执行、阻塞和最终收口都在当前会话返回事实摘要。已更新正式需求、正式实施方案、`using-shanforge` 和结构测试；验证 `uv run pytest tests/test_project_memory_skill.py` 通过 `6 passed`，ruff 通过，`using-shanforge` quick_validate 通过。当前仍为 `ready_for_review`，下一动作 `independent_review`；未执行 `FLOW-TASK-011`。
- 2026-07-09：按用户明确指令创建并执行 `FLOW-TASK-015` 的正式方案切片，用于重塑完整软件项目会话行为与工作流归因契约。正式方案已写入 `docs/04-project-development/05-development-process/task-execution-contract.md`，新增 `tests/test_full_project_session_workflow_routing.py`；验证 `45 passed`，ruff 和 `using-shanforge` quick_validate 通过。当前状态 `ready_for_review`，下一动作 `independent_review`；本轮未把新方案同步到各 workflow skill 运行规则，`FLOW-TASK-011` 至 `FLOW-TASK-014` 仍未执行。
- 2026-07-06：`SKILL-FLOW-AUDIT-001` 已按 `language-prompt-review-iteration-2.md` 修复 21 个低分 skill 入口，范围包括 P0 入口、教程型开发 skill、文件/文本工具和流程契约小问题。验证：相关结构测试 `45 passed`，ruff 通过，21 个编辑过的 skill 均通过 `quick_validate`，旧口径扫描无命中。当前状态是 `ready_for_review`，下一步按用户要求重新创建中文语言 / prompt 评审子任务和 skill flow 完整性测试子任务；`skill-flow-completeness-test-iteration-2.md` 的 Critical / Important 尚未处理，不能声明整体完成。
- 2026-07-06：`SKILL-FLOW-AUDIT-001` iteration-3 复评完成。语言/prompt 复评分数从 iteration-2 平均 `85.2` 提升到 `92.3`，低于 90 分 skill 从 `21` 降到 `5`。流程完整性复测从 `82 / 100` 提升到 `86 / 100`，但仍有 `1` 个 Critical 和 `3` 个 Important；相关 pytest `74 passed / 1 failed`，失败仍是黑盒 eval 文档状态旧断言，且缺 S1-S6 真实行为回放 evidence。当前 gate 是 `changes_requested`，下一步先修 flow completeness Critical / Important，不能进入完成、人工确认或提交。
- 2026-07-06：`SKILL-FLOW-AUDIT-001` iteration-4 按用户要求拆成三个独立子任务：中文语言专家评审、prompt 专家评审、skill 流程完整性测试。中文语言评审扫描 34 个 skill，平均 `92.1`，8 个低于 90；prompt 评审扫描 34 个 skill，平均 `91.6`，10 个低于 90；流程完整性测试评分 `89 / 100`，`84 passed`、ruff 通过，但仍有 `1` 个 Critical、`3` 个 Important、`3` 个 Minor。当前 gate 仍是 `changes_requested`：缺 S1-S6 真实行为回放 transcript，远端 PR / push / merge 缺 Shanforge owner / evidence / gate，部分状态包未统一。
- 2026-07-06：`SKILL-FLOW-AUDIT-001` iteration-4 feedback 已按用户要求拆两项修复子任务并完成到 `ready_for_review`。语言 / prompt 合同修复补齐 6 个 skill 的状态包和失败语义；流程完整性修复新增 S1-S6 dry-run transcript、远端 PR / push / merge handoff 契约和结构测试。主线程联合验证 `uv run pytest ...` 通过 `45 passed`，ruff 通过。下一步是真实独立 review；本轮未提交、未 push、未创建 PR、未 merge。
- 2026-07-06：`SKILL-FLOW-AUDIT-001` iteration-4 修复独立评审已通过，reviewer `codex-skill-flow-audit-001-iteration-4-reviewer-20260706` / subagent `019f37f7-c9ec-7763-8100-bc3f7361a5ed` 给出 `approved / 92`；无 Critical / Important，2 个 Minor 残留风险。按用户要求重新创建并完成 iteration-5 三个子任务：中文语言评审扫描 35 个 skill，平均 `92.1`，5 个低于 90；Prompt 工程评审扫描 35 个 skill，平均 `92.2`，5 个低于 90；Skill 流程完整性测试 `passed / 96`，0 Critical / 0 Important / 2 Minor，workflow pytest `84 passed`，ruff 通过。当前下一步是 triage iteration-5 findings；本轮未提交、未 push、未创建 PR、未 merge。
- 2026-07-06：`SKILL-FLOW-AUDIT-001` iteration-5 反馈已拆成三个顺序实现子任务并修复到 `ready_for_review`。中文语言 95+ 修复压缩 `skill-creator`、`gitcommitzh`、`stratix-service`、`document-templates`、`requirements-engineering` 等长入口并下沉 reference；Prompt 工程 95+ 修复补齐 `doc-coauthoring`、`algorithmic-art`、`shadcn`、`ui-ux-pro-max` 等 work item 状态包；流程完整性 Minor 修复补齐 S4/S5 transcript 的 ledger / review-ledger 证据并锁结构测试。合并验证：`54 passed`，ruff 通过，10 个 touched skill quick_validate 通过，JSONL 解析通过，旧中心 / 未验证脚本扫描无命中，`git diff --check` 通过。下一步是真实独立 review；本轮未提交、未 push、未创建 PR、未 merge。
- 2026-07-07：`SKILL-FLOW-AUDIT-001` iteration-5 fixes 独立 review 已通过，reviewer subagent `019f3828-c993-7850-9a84-c1465c740540` 给出 `approved / 96`；中文语言评分 `96`，Prompt 工程评分 `96`，流程完整性 `passed`；无 Critical / Important / Minor 返工项。最终审计问题报告为 `.factory/workitems/SKILL-FLOW-AUDIT-001/reports/iteration-5-final-audit-issue-report.md`。当前 gate 是 `pending_human_confirmation`；确认前不得关闭、提交或进入下一阶段。
- 2026-07-07：用户已确认 `SKILL-FLOW-AUDIT-001` iteration-5 fixes 通过；iteration-5 gate 解除。iteration-6 三个评审 / 测试子任务已在进行中，下一步等待子任务报告。
- 2026-07-07：`TASK-WORKFLOW-SEMANTICS-001` 独立 review iteration-1 返回 `changes_requested / 76`，指出 bug 两段式 gate 未落到流程总控路由、direct analysis 与 tracked task 输出契约不一致、`Method` / `Tool` 概念缺失，以及 `tdd-workflow` 有重复句。已按反馈修复到 `ready_for_review`：补概念边界、改 bug 路由为根因确认 Gate + 修复方案确认 Gate、统一需求核心输出契约、删除重复句并补测试。验证：`43 passed`，ruff 通过，JSONL 解析通过，`git diff --check` 无输出。下一步是真实独立复审；复审通过前不得进入人工确认。
- 2026-07-07：`TASK-WORKFLOW-SEMANTICS-001` 独立复审 iteration-2 已通过：`approved / 94`。无 Critical / Important / Minor；最终审计问题报告为 `.factory/workitems/TASK-WORKFLOW-SEMANTICS-001/reports/final-audit-issue-report.md`。当前 gate 是 `pending_human_confirmation`；人工确认前不得关闭、提交或宣称完成。
- 2026-07-07：按用户要求完成 `SKILL-FLOW-AUDIT-001` iteration-6 三个子任务报告。中文语言评审：36 个 skill，平均 `93.4`，最低 `91`，0 个低于 90，无 Critical / Important。Prompt 工程评审：36 个 skill，平均 `93.5`，最低 `89`，3 个低于 90，无 Critical，3 个 Important，集中在 `agent-harness-construction`、`ai-first-engineering`、`article-writing` 缺 `work_item` / `ledger_event` 等状态包字段。流程完整性测试：`97 / 100`，0 Critical / 0 Important / 2 Minor，workflow pytest `121 passed`，ruff 通过。下一步是 triage 并修复 Prompt Important，按需处理 Minor。
- 2026-07-07：按用户要求创建并派发 `SKILL-FLOW-AUDIT-001` iteration-6 合并修复子任务 `iteration-6-fix-language-prompt-97`。worker `Helmholtz / 019f3ac4-80f0-7b43-8015-b1ee125ef067`，任务目标是后续独立复评中文语言平均分和 Prompt 平均分都 `>=97`，Critical / Important 均为 0；当前状态 `in_progress`，下一步等待子任务报告。
- 2026-07-07：`SKILL-FLOW-AUDIT-001` iteration-6 合并修复子任务 `iteration-6-fix-language-prompt-97` 已完成到 `ready_for_review`。修改 8 个 skill 和 3 个测试文件；worker 自评中文语言平均 `97.1`、Prompt 平均 `97.2`，Critical / Important 为 0，Minor 为 2。验证：8 个受影响 skill quick_validate 通过，主线程复跑相关 pytest `30 passed`，ruff 通过，`git diff --check` 无输出。独立复评已派发给 `Hume / 019f3b96-12e1-74e3-b311-ca0c47c6978e`，当前等待报告。
- 2026-07-07：`SKILL-FLOW-AUDIT-001` iteration-6 97 分修复独立复评返回 `changes_requested`。中文语言评分 `93.8`，Prompt 评分 `94.2`，Critical / Important / Minor 为 `0 / 2 / 2`。阻塞项：全量 36 skill 平均分仍低于 97；完整 workflow pytest `122 passed / 1 failed`，失败点为 `tests/test_independent_review_gate.py::test_requesting_code_review_forbids_same_thread_approved`。下一步是 `fix_review_feedback`。
- 2026-07-05：Superpowers 流程集成计划已按本地口径闭环。`SF-SP-001/002/003/004/005/006/007` 已人工确认并提交为 `efac627`，`SF-SP-008` 已提交为 `e048784`，`SF-SP-009` 已提交为 `9296f58`，`SF-SP-010` 已提交为 `3b0e9a5`；10 项均已有开发、独立 review、人工确认和本地提交证据。当前没有 push / PR / merge 证据，不能声明远端闭环完成。
- 2026-07-05：完成旧全局流程脚本物理清理。`superpowers-workflow-integration-plan.md` 和 closeout report 已从 `3 / 10` 本地闭环更新为 `10 / 10`；活跃入口 `AGENTS.md`、`GEMINI.md`、`runtime-brief.md`、`agent-session.md`、用户指南、配置和测试不再推荐中心脚本主控。旧脚本调用方、旧用户文档和旧功能测试已清理。
- 2026-07-05：PM 控制面新增需求生命周期快速查看页，并把需求实时跟踪表直接并入 `.factory/pm/generated/status-dashboard.html` 首页。首页按“需求、分析、任务、设计、开发、测试、review、人工确认、提交 / PR、关闭”展示正式 REQ 和当前 Superpowers 流程集成需求；`SF-SP-001` 到 `SF-SP-010` 每个关联任务都有页内锚点、当前状态、关闭判断和下一动作。`.factory/pm/generated/requirements-lifecycle.html` 保留为详情页；页面仍只是展示层，事实源仍是需求矩阵、Superpowers 方案、PM 台账和 work item ledger。
- 2026-07-05：继续 Superpowers 流程集成收尾。`superpowers-workflow-integration-plan.md` 中显式任务只有 `SF-SP-001` 到 `SF-SP-010` 共 10 个；当前不新增 `SF-SP-011`。该轮先补 `SF-SP-001` ledger、coverage evidence、closure report 和 review brief，并发现 `SF-SP-002/003/004` 的旧 task review 含单线程 fallback 口径，不能当最终独立评审；此缺口已被后续 20:05 的真实独立 review / 复审结果取代。详细报告见 `.factory/workitems/SF-SP-010/reports/superpowers-workflow-integration-closeout-report.md`。
- 2026-07-05：用户已确认 `SF-SP-010` iteration-1 独立复审，状态为 `human_approved`。下一步只有在用户明确要求提交 / commit 时才进入提交流程；提交范围必须仅包含 `SF-SP-010` 文档、导航、memory、review/evidence/report/ledger、测试和必要导航目标文档。
- 2026-07-05：`SF-SP-010` iteration-1 独立复审已通过，reviewer `codex-sf-sp-010-rereviewer-20260705` 给出 `approved / 95`。复审确认旧下一步文案、PM 导航目标检查和 JSONL evidence 一致性均已修复；当前 gate 是 `pending_human_confirmation`，不得自动提交、关闭或标记 done。
- 2026-07-05：`SF-SP-010` iteration-1 独立 review 为 `changes_requested / 82`，已按反馈修复并进入 `ready_for_re_review`。修复项包括 Superpowers 方案旧下一步文案、PM 控制面导航目标存在性测试、JSONL evidence 命令与计数记录。下一步是真实独立复审；复审通过前不得进入人工确认或提交。
- 2026-07-05：`SF-SP-009` 已提交为 `9296f58`，`SF-SP-010` 已进入文档、导航、memory 同步开发。当前收口范围是 Superpowers 方案当前进展、开发过程导航、根文档导航、`.factory/memory/doc-map.md`、summary 和测试报告入口；实现完成后只能进入真实独立 review，不能自批完成或直接关闭。
- 2026-07-05：`SF-SP-009` 已进入黑盒流程 eval 开发并完成 iteration-1 实现，当前为 `ready_for_review`，下一步是真实独立 review。新增 `skills/using-shanforge/references/black-box-flow-eval.md`，并在 `using-shanforge` 中加入 `SF-SP-009` / 黑盒流程评估入口；eval contract 覆盖一句话需求、bug 修复、review 反馈、压缩恢复、完成声明和自评隔离，定义 `fast smoke`、`full regression`、证据格式、`2/1/0` 评分和 critical assertion 失败门。不新增中心脚本 gate，不调用外部模型 judge。
- 2026-07-05：`SF-SP-009` iteration-1 独立 review 为 `changes_requested / 84`，已按反馈修复并进入 `ready_for_re_review`。修复项包括评分归一化公式、证据格式中的 Actual / Max / Normalized score、每场景 critical assertion 可评分结构测试，以及正式计划 6 类场景口径。验证：加严红灯 `3 failed`，修复后目标测试 `6 passed`，邻近 workflow 回归 `28 passed`，ruff、skill validator、JSONL 和 `git diff --check` 通过。
- 2026-07-05：`SF-SP-009` iteration-1 独立复审已通过，状态为 `approved / 95`，当前 gate 为 `pending_human_confirmation`。人工确认前不得提交、关闭 work item 或进入 `SF-SP-010`。
- 2026-07-05：用户已确认 `SF-SP-009` iteration-1 独立复审，状态为 `human_approved`，并要求进入提交流程后开始 `SF-SP-010` 开发。提交范围必须仅包含 `SF-SP-009` 黑盒 eval 契约、测试、review/evidence/report/ledger 和相关 memory hunk。
- 2026-07-05：`SF-SP-008` 已完成真实独立 review 并获用户 `human_approved`。主 review 为 `approved / 94`，范围隔离复审为 `approved / 94`；用户要求进入提交流程，提交后直接进入 `SF-SP-009` 开发。针对 loop 未闭环问题，已追加 skill-native 收尾门并撤销中心脚本 gate 方案；`using-shanforge` / `gitcommitzh` 在完成声明、提交或关闭 work item 前必须重读最新 work item ledger 和 review ledger。针对范围复审反馈，混合 `.factory/memory/` 文件只能暂存当前任务 hunk，无法拆分时停止并拆成独立提交。
- 2026-07-05：PM HTML 页面已升级为完整项目管理查看面，并纳入最新 `SF-SP-008`。`status-dashboard.html` 作为总览，包含甘特图、项目任务看板、评审链路总览、WBS 和 PM 十模块入口；`workitems.html` 作为任务详情，按任务摘要、事件时间线、评审链路和每轮评审结果详情展示；`pm-details.html` 作为十模块明细，并提供完整项目进度入口。页面仍只是渲染视图，事实源仍是 `.factory/pm/`、`.factory/workitems/*/ledger.jsonl` 和 review / evidence 文件。
- 2026-07-05 补充：项目任务看板主列固定为“未开始任务 / 正在进行 / 已完成 / 已经审批”。不要再把主列按“待独立评审 / 待人工确认 / 已通过 / 风险”这类流程门拆分；这些信息应放进卡片说明和评审链路。
- 2026-07-05：`SF-SP-008` 已完成首版实现并进入 `ready_for_review`。本轮新增 `skills/gitcommitzh/references/pr-closure-checklist.md`，并更新 `gitcommitzh`、`using-shanforge`、Codex 工具参考、Superpowers 流程方案和结构测试，固定提交前必须核对 review、evidence、memory sync 和 work item ledger；`gitcommitzh` 只做本地提交，不创建、不推送、不合并 PR。用户“现在开始继续做 SF-SP-008”已记录为接受 `SF-SP-005/006/007` 独立 review 结果并进入本任务的人工确认事件。该阶段曾将后续焦点收敛到 `SF-SP-010`，但已被 19:01 收尾校准取代。
- 2026-07-05：`SF-SP-005` 和 `SF-SP-006` 的独立复审已完成并入档。`SF-SP-005` iteration-3 为 `approved / 92`，`SF-SP-006` iteration-2 为 `approved / 95`；两者 review 文件、evidence、work item ledger 和 `.factory/memory/review-ledger.jsonl` 均已同步。该轮当时共同 gate 是 `pending_human_confirmation`，随后已由用户确认进入 `SF-SP-008`。
- 2026-07-05：已修复 `SF-SP-005` 和 `SF-SP-006` 的独立 review 阻塞项。`SF-SP-005` iteration-3、`SF-SP-006` iteration-2 均已写入 review feedback triage、response、fix report、verification evidence 和 ledger，状态为 `ready_for_review`，下一步是真实独立复审。复审通过前仍不得进入 `SF-SP-008`。
- 2026-07-05：前序任务真实独立评审已补齐并入档，但不是全部通过。`SF-SP-005` iteration-2 为 `changes_requested / 78`，`SF-SP-006` iteration-1 为 `changes_requested / 84`，`SF-SP-007` iteration-1 为 `approved / 95`。下一步必须先按独立 reviewer 意见修复 `SF-SP-005` 和 `SF-SP-006`，补测试后重新独立 review；在两者通过前不得进入 `SF-SP-008`。

- 2026-07-05：评审独立性硬门修复已完成自检但未独立批准。新增 `tests/test_independent_review_gate.py`，并更新 `skills/requesting-code-review/`、review rubric、review templates 与 `superpowers-workflow-integration-plan.md`，强制 `same_thread` 只能写 `self_check_passed`，`approved / review_score / pending_human_confirmation` 必须有 `reviewer_type / reviewer_id / reviewer_independence_evidence`。`SF-SP-007` 仍为 `needs_independent_review`，进入 `SF-SP-008` 前必须补真实独立评审或取得明确子 agent 授权。
- 2026-07-05：新增 PM 控制面首版，将项目管理 Excel 模板理念融入 shanforge。核心不是输出表格模板，而是建立管理控制面：目标 / WBS / 责任 / 风险 / 沟通 / 状态 / 变更 / 复盘在 `.factory/pm/` 汇总，执行事实仍由 `.factory/workitems/<ID>/ledger.jsonl`、evidence 和 review 承担。人类快速查看入口为 `.factory/pm/generated/status-dashboard.html`，AI 默认读取 `.factory/pm/dashboard.md`；HTML 只作展示，不作为唯一事实源。不新增独立 PM skill，由 `using-shanforge` 按需从 PM 台账和 work item ledger 渲染状态页。
- 2026-07-05：`SF-SP-007` 已新增首版验证与调试 gate，但 review 状态已更正为 `needs_independent_review`。`verification-before-completion`、`systematic-debugging` 和 `tdd-workflow` 融合 reference 已实现，新增 `tests/test_verification_debugging_workflow_skills.py` 固定本地化契约、旧路径禁止项和路由回退禁止项；联合 workflow 回归 `22 passed`，三个 skill validator 通过。此前 iteration-1 review 的 `approved / 96 / pending_human_confirmation` 是同线程作者自检，不是真实独立 review，不能作为进入 `SF-SP-008` 的依据。
- 2026-07-05：用户已确认 `SF-SP-006` iteration-1 通过，`SF-SP-006` ledger 已写入 `human_approved`，可以进入 `SF-SP-007`。`SF-SP-007` 范围限定为验证与调试 gate：本地化 `verification-before-completion`、`systematic-debugging`，并补齐与 `tdd-workflow` 的融合规则、完成声明证据模板、根因定位清单和对应结构测试；仍需在 loop 结束时停在 `pending_human_confirmation`。
- 2026-07-05：`SF-SP-006` 已新增首版评审类 workflow skill 并进入人工确认门。`requesting-code-review` 现在只负责组织 task review、PR review、独立 review task、评分表、review ledger 和 `pending_human_confirmation`；`receiving-code-review` 只负责 review feedback triage、技术核实、逐项处理、response、修复报告和验证证据。两者均不声明前置、后置或下一步 skill，流程路由继续由 `using-shanforge` 统一决定。新增 `tests/test_review_workflow_skills.py` 固定 review package、中文元数据、旧路径禁止项和路由回退禁止项；iteration-1 review 评分 `96 / 100`，等待人工确认后才能进入 `SF-SP-007`。
- 2026-07-05：`SF-SP-004` iteration-2 收到人工 `human_changes_requested`：`writing-plans/references` 还没有完全使用中文重写。已修正并进入 `ready_for_review`：三份 references 模板已中文化标题、字段、章节、TDD 步骤、验证说明、评审检查项和完成口径；对应测试现在要求中文模板并禁止旧英文模板短语回退。等待独立 review 后才能再次标记通过。
- 2026-07-05：`SF-SP-005` iteration-1 收到人工 `human_changes_requested`：执行类 skill 不应关心工作前置、后继或把结果交给哪个 skill。iteration-2 已修正并进入 `ready_for_review`：`using-shanforge` 是唯一流程路由 owner；工作 skill 只接受输入包、完成专业任务、写 outputs/evidence/reports/ledger，并回写 `status` 与 `needs`。`subagent-driven-development`、`executing-plans`、`writing-plans` 不再写“与其他 skill 的关系”，也不再硬编码 review、verification、commit 等下一步 skill。等待独立 review 后才能再次进入人工确认门。
- 2026-07-05：Superpowers 流程集成方案已补齐记忆分层和人工确认门。后续 `project-memory`、`executing-plans`、`requesting-code-review`、`verification-before-completion` 改造时，必须区分入口压缩层、主题摘要层、work item 执行层、ledger 审计层和正式文档层；每轮 loop 结束必须提交 execution report、verification evidence、review score，并停在 `pending_human_confirmation`，不得把 reviewer `approved` 直接等同人工 `human_approved`。
- 2026-07-05：`brainstorming` 已完成中文化后的流程评审修正。后续该 skill 不再把所有创造性请求强制推到固定后继 skill，也不再默认读取一串项目背景文件；它优先消费当前对话、`project-memory` 会话卡和当前 work item brief/ledger，缺上下文时先交给 `project-memory` 恢复最小会话卡。输出路径改为 `.factory/workitems/<WORKITEM-ID>/brief.md`、`ledger.jsonl`、必要的正式 `docs/04-project-development/` 文档和 memory summary。可视化伴侣改为中文指南，持久化文件进入 `.factory/workitems/<WORKITEM-ID>/design-assets/brainstorm/`。
- 2026-07-05：`SF-SP-002` 已完成 task review 并进入 `approved`，但仍未关闭：新增首版 `skills/project-memory/`，覆盖会话恢复、读取范围、会话卡、ledger 模板、current-state 更新清单和 OpenAI 元数据；后续会话恢复先复用已有会话卡和压缩记忆，只有缺口明确时才增量读取 summary 或正式事实，并在会话卡输出“未读 / 已排除上下文”。新增 `tests/test_project_memory_skill.py` 固定结构约束；`.factory/workitems/SF-SP-002/reviews/task-1-review.md` 已给出 task review 通过结论。该任务尚未提交或进入 PR 闭环，不能标记整体 `done`；`SF-SP-003` 的跨 skill 模板迁移仍未开始。
- 2026-07-05：`SF-SP-003` 已完成首个模板迁移切片并通过 task review，状态为 `approved_for_slice`，目标限于已有 skill 的 references：`requirements-engineering` 的 PRD 模板、`document-templates` 的技术方案模板、`tdd-workflow` 的根因定位与 evidence 模板、`gitcommitzh` 的提交说明 rubric。新增 `tests/test_superpowers_reference_migration.py` 固定该切片和未完成边界；`.venv/bin/pytest tests/test_superpowers_reference_migration.py` 通过 `2 passed`，ruff 和 4 个 skill validator 均通过；`.factory/workitems/SF-SP-003/reviews/task-1-review.md` 已给出切片 review 通过结论。后续 workflow skill references 已随 `SF-SP-004`、`SF-SP-006`、`SF-SP-007`、`SF-SP-008`、`SF-SP-009` 持续迁移；当前整体完成度以后续收尾校准为准，不能把总计划标记完成。
- 2026-07-05：`SF-SP-004` 已新增首版 `skills/writing-plans/` 并通过 task review，状态为 `approved`。该 skill 将已批准 spec、需求、设计或 work item brief 转成 `.factory/workitems/<WORKITEM-ID>/plan.md` 和 `task-briefs/`，并包含文件结构先行、TDD 小步骤、真实命令、期望输出、memory sync、ledger 和 review gate。新增 `tests/test_writing_plans_skill.py`，当前定向验证 `3 passed`，SF-SP-003/SF-SP-004 联合验证 `5 passed`，ruff、skill validator 和 `git diff --check` 通过。该任务尚未提交或进入 PR 闭环，不能标记整体闭环完成。
- 2026-07-05：`SF-SP-005` 已新增首版 `skills/subagent-driven-development/` 和 `skills/executing-plans/`，iteration-1 review 评分 `96 / 100`，并已由用户确认 `human_approved`。前者执行 `.factory/workitems/<WORKITEM-ID>/plan.md` 中的独立任务，按 task brief、evidence、implementer report、Spec Review、Quality Review 和 ledger 推进；后者作为当前会话 inline fallback，先批判性 review plan，再逐步执行并设置 review checkpoint。新增 `tests/test_execution_workflow_skills.py`，当前定向验证 `4 passed`，SF-SP-003/004/005 联合验证 `10 passed`，ruff、两个 skill validator 和 `git diff --check` 通过。下一步进入 `SF-SP-006`。
- 2026-07-05：`skill-creator` 已补齐“修改 skill / 编写 skill”的通用原则。后续所有 workflow skill 改造都必须先建立含义保留清单，按中文短句完整保留原文语义，作者自检只到 `ready_for_review`，再由独立 reviewer 或 review task 决定 `approved / changes_requested`；模板、schema、rubric 和长背景进入 `references/`，helper code 只作为 skill-scoped 工具存在。
- 2026-07-05：Superpowers 流程集成方案已修正 skill helper code 规则。后续流程工具集成不走中心 CLI/dispatch 主控，但允许把目标明确、重复、确定性的 `py/js` helper code 放入对应 skill，并要求 `SKILL.md` 显式声明调用边界、`references/` 提供模板/schema/rubric 契约、测试验证 helper 行为、独立 review 审查改动。
- 2026-07-05：Superpowers 流程集成方案已加入“运动员 / 裁判隔离”规则。后续 `subagent-driven-development`、`executing-plans`、`requesting-code-review` 改造时，必须固定状态流 `in_progress -> ready_for_review -> review_requested -> changes_requested|approved -> done`；实现者不能批准或关闭自己的任务，完成必须来自独立 review task。
- 2026-07-04：新增 [Superpowers 流程集成实施方案](../../docs/04-project-development/05-development-process/superpowers-workflow-integration-plan.md)，将 Superpowers 的 `brainstorming -> writing-plans -> subagent-driven-development / executing-plans -> TDD -> task review -> final review -> finishing` 链路改造成 shanforge 的 skill-first 状态驱动流程。方案要求后续优先落 `SF-SP-001` 拆除脚本主控设计、`SF-SP-002` 新增 `project-memory` skill、`SF-SP-003` references 模板迁移；再推进计划、执行、评审、验证类 skill 和黑盒流程 eval。
- 2026-07-04 补充：`factory-agent-session` 不再作为目标入口继续增强，而是作为迁移来源拆入 `skills/project-memory/`。会话启动清单、相关性判断、会话卡模板、ledger 事件模板、current-state 更新清单统一进入 `project-memory/references/`；具体 work item 计划固定存放到 `.factory/workitems/<WORKITEM-ID>/plan.md`。

## 进行中

- `MG-WP-001`：记忆治理模型显式化
  - 当前已完成：`src/domain/memory/governance.py` 已落地 `RecallGovernancePolicy / MemoryProviderGovernancePolicy / MemoryLifecyclePolicy` 与对应 decision 模型；`DefaultMemoryDomainService` 现会先生成 recall/provider 领域决策，再分别驱动 `RecallPlannerPort` 与 provider manager；`DefaultRecallPlanner` 已改成只把 `RecallGovernanceDecision` 物化成带预算的 `RecallPlan`
- `MG-WP-002 / MG-WP-003`：Recall / Provider 治理继续收口
  - 当前已完成：`RecallPlan` 现已冻结 `within_scope_order / overflow_order / overflow_fill_enabled` 这组显式排序指令，`DefaultRecallRanker` 与 `DefaultMemoryDomainService.preview_recall()` 已按 plan 执行同一套 bucket/overflow 顺序；`MemoryProviderManagerPort` 与 `DefaultMemoryProviderManager` 现已直接消费 `MemoryProviderGovernanceDecision`，manager 本身不再持有 writable / delegation gate
  - 当前缺口：继续把 preview explainability 里的排序原因命名、以及 manager diagnostics 中仍残留的 provider-local 策略痕迹进一步收口到更纯的执行语义
- `MG-WP-004`：Lifecycle Governance 补齐
  - 当前已完成：`MemoryLifecyclePolicy` 现已补齐最小正式状态机、conflict supersede、forced manual override 与 metadata-driven decay forget；`DefaultMemoryDomainService.explain_session_memory()` 也已开始输出 scoped `lifecycle_evaluations` 与 `lifecycle_queue_summary`，能回答 memory 为什么 retained / superseded / forgotten；同时 `review_lifecycle / load_lifecycle_queue / apply_lifecycle` 已通过 `MemoryGovernanceService + MemoryAPI` 暴露成最小 review queue / batch apply 闭环
  - 当前已继续推进：`apply_lifecycle()` 现已按 `MemoryProviderGovernanceDecision.allow_lifecycle_writeback` 触发专门的 `lifecycle_apply` provider 通道，并把刷新后的 diagnostics / assembly manifest durable 保存回 session ledger
  - 当前已继续推进：lifecycle review queue 现已从 explainability 投影升级为 durable queue object；新增 `MemoryLifecycleQueueRepositoryPort` 与 `update_lifecycle_queue(...)`，queue entry 正式持久化 `pending / dismissed / applied` review state，`apply_lifecycle()` 成功后会同步把对应 entry 标记为 `applied`
  - 当前已继续推进：lifecycle review/apply 现已新增独立 audit trail；`MemoryLifecycleAuditRepositoryPort`、`load_lifecycle_audit(...)` 与 `lifecycle_audit_summary` 已落地，能回读 `review_status_updated / lifecycle_applied` 的 actor/action/status 历史
  - 当前已继续推进：显式 review workflow 已开始成形；`reopen_lifecycle_queue(...)` 已落地，且同状态 note update 现会被收口为独立 `review_note_updated` 审计动作，不再混入 status update
  - 当前已继续推进：queue 运维已开始支持 `queue_filter` 驱动的批量 review；`update_lifecycle_queue(...)` 与 `reopen_lifecycle_queue(...)` 都可直接按 filter 命中 queue item 全集做 `dismiss / reopen`，不再只接受显式 `record_ids`
  - 当前已继续推进：review workflow 现已补 reviewer resolution taxonomy；`update_lifecycle_queue(..., resolution=...)` 可持久化人工结论，`reopen_lifecycle_queue(...)` 回到 `pending` 时会清空 resolution，queue/audit summary 也开始稳定投影 `resolution_counts`
  - 当前已继续推进：audit read model 已开始面向 reviewer 收口；`MemoryLifecycleAuditFilter.latest_per_record_only` 已落地，`lifecycle_audit_summary.latest_entries` 改成真正的最新优先，同时新增 `latest_by_record`
  - 当前已继续推进：queue projection 已开始直接给 reviewer guidance；`MemoryLifecycleQueueItem` 现会投影 `resolution_required`、推荐 `resolution_options` 与建议 note 模板
  - 当前缺口：仍未引入更完整的人工复核流程与专门的审核运维能力
- `MG-WP-005`：记忆治理专项回归与 explainability 校验
  - 当前已完成：新增 `tests/test_memory_governance_regression.py`，将 `TC-013 ~ TC-016` 收口为独立治理回归入口；`TC-015` 对应的最小 lifecycle 事实现已补到 `MemoryStatus.FORGOTTEN` 与默认状态机，`explain_session_memory()` 也已稳定投影 `promotion_reasons / promotion_decisions / recalled_memory_statuses / memory_provider_binding / recall_plan / lifecycle_queue_summary`
  - 当前已继续推进：provider-aware lifecycle writeback 的领域级、执行级与容器级回归已补齐，`preview_recall().augmentation_preview.diagnostics.writeback_trace.detail_reports.lifecycle_apply` 现可稳定回读；queue review state 的 durable JSONL / container persistence 回归也已补齐；audit trail 的 JSONL / access-application / container persistence 回归也已补齐；显式 `reopen / review_note_updated / review_resolution` 语义也已纳入专项回归
  - 当前缺口：后续主要剩更完整的人工审核流与跨 provider 的更细粒度回放断言

- `TASK-017`：基础能力层具体函数实现阶段
  - 当前已完成：`file_access`、`session_search` 的本地最小可用行为，`web_access`、`terminal`、`browser` 的首轮 local bridge 与治理接线，以及 `profile_source`、`rule_source`、`clock_identity` 的正式实现和 runtime-to-domain 适配；原 runtime `skills` 能力已按 TASK-QUALITY-002 删除
  - 当前缺口：补强 `web / terminal / browser` 的治理细节、provider profile 化与更真实 backend
- `TASK-016`：Session Search 与装配解释查询框架
  - 当前已完成：`SessionArchiveHit` / `SessionTranscriptSlice` / `SessionAssemblyManifest` / `SubAgentDigest` 已形成正式读模型；`SessionArchiveQueryPort`、`SessionTranscriptSlicePort`、`SessionAssemblyQueryPort`、`MemoryAssemblyQueryPort`、`SessionAssemblyStorePort`、`DelegationDigestStorePort`、`SessionInspectionService`、`MemoryAPI` 与 `SessionSearchQueryAdapter` 已接线；`prepare_session` 现在会把 assembly snapshot 同时写入 session context 与专门 `SessionAssemblyStorePort`；`SessionAssemblyManifest` 现已暴露 `selected_model / model_bindings / backend_bindings`，并能区分默认装配选择与 step 级实际模型调用历史；`RecallPlannerPort / RecallRankerPort` 已落地，recall 主链现已改为 `RecallGovernancePolicy -> plan -> scan -> rank`；`preview_recall` 现已通过独立 `MemoryInspectionService` 落地，并由 `MemoryAPI` 聚合暴露；`RecallPreview` 现已显式给出 `scope_breakdowns / record_rankings / augmentation_preview`
  - 当前已完成：`preview_recall` 的 augmentation diagnostics 已统一补到 `jsonl / jsonl_vector / remote_http`，当前可稳定回读 `query_terms / source_breakdown / result_truncated / budget_trace / rank_trace / hit_provenance / contract_trace / access_trace / writeback_trace`；`DefaultMemoryProviderManager` 现已在 runtime 输出侧直接使用 compact canonical diagnostics，而 `DefaultMemoryDomainService` 仍会在读取冻结的 session/manifest augmentation diagnostics 时复用同一套 trace-first normalizer，并把落盘 diagnostics 压成 compact trace-first 口径；本轮进一步把 stored replay 的 legacy 输入过滤也收口到 `project_stored_augmentation_diagnostics()`，不再在 service 内维护单独 `allowed_keys`，并开始基于 `provider_id` 推断默认 contract metadata、基于 `memory_provider_binding.metadata.recall_endpoint_url` 恢复 access 默认值，使 `bridge_kind / provider_kind / storage_kind / retrieval_kind / response_contract / response_contract_source / endpoint_url` 不再需要继续作为 replay 顶层输入；preview diagnostics 继续保持 canonical trace-first 字段，不再输出 `legacy_aliases`；`signature/bearer selection`、`retry/timeout`、`secret catalog source`、prefetch `response_validation_error` 与 writeback `successes / response_oks / response_statuses / response_messages / response_report_ids / failure_policies / response_validation_errors` 摘要继续并回 `access_trace / contract_trace / writeback_trace`，同时把 canonical drill-down 字段正式定为 `detail_reports`，旧的 `reports` 仅作为 replay/normalize 输入兼容，并把 `hit_count / hit_ids / query_text_present` 进一步并入 `budget_trace.selected_hit_count / selected_hit_ids / query_text_present`
  - 当前缺口：继续减少 legacy 输入兼容面，优先评估 `writeback_reports` 这批 replay alias 是否也能逐步下沉到 trace 默认值或更稳定的写回摘要
- `TASK-020`：外部 DI 技术库接入与容器收敛
  - 当前已完成：`shanforge-di` 依赖接入、`component_bindings.py` 业务绑定、本地 thin container、composition 回归测试、`workspace/file/git/shell/web/browser` 首轮 local bridge 接线、settings layer catalog 与 `embedding/http/blob/search/vector` 骨架入口、workspace profile/backend/provider catalogs 及其对默认容器的 provider/backend 选择接线、access 层协议 owner 与本地 CLI launcher 的边界收口、`capability_registry / approval_policy / delegation_transport` 的 Hermes-backed adapter 契约测试与 assembly explainability 投影、settings/composition 的 provider binding manager，以及 external `memory_provider` family 的首轮装配治理；`memory_provider:jsonl / jsonl_vector / remote_http` 现已作为 external backend/source 接入默认容器，其中 `remote_http` 已支持真实 `HTTP/file` 读桥、`metadata_file` durable source、签名类 auth、retry/timeout 治理、`prefetch_response_validation`、canonical 签名串、`secret_catalog_file` 驱动的 key rotation、内建 `remote_memory_prefetch_v1 / remote_memory_writeback_ack_v1` response contract、secret selection-source audit，以及稳定的 `writeback_reports` 成功/失败读模型；上一轮已把 durable secret 选择逻辑抽成 `src/settings/workspace/secret_catalog.py` 的 `LocalSecretCatalogProvider` 并注册为 `secret_catalog` family，本轮又把 `recall/sync/session_end/delegation` 的 endpoint、request_options、response_contract、response_validation_mode、failure_policy 与 legacy alias fallback 统一抽成 `src/settings/memory/remote_http_metadata.py` 的 `RemoteHttpRequestGovernance`，并把 `query_terms / source_breakdown / result_truncated / budget_trace / rank_trace / hit_provenance / contract_trace / access_trace / writeback_trace` 进一步对齐到 `jsonl / jsonl_vector / remote_http`；与此同时，`DefaultMemoryProviderManager` 与 `DefaultMemoryDomainService` 现会共用一套 augmentation diagnostics normalizer，并把 session/context 与 manifest diagnostics 落盘压成 compact trace-first 口径，`remote_http` provider 自身开始去掉重复顶层 diagnostics
  - 当前缺口：继续减少 recall 读取与 normalize 阶段仍保留的 legacy 顶层诊断重复，并把 provider-specific 治理信息继续压进统一 trace

## 已完成里程碑

- `M2`：平台主闭环、基础能力骨架和 `file / session_search` 首轮可用实现已稳定；Skill 仅保留为顶层宿主资产
- `M3`：行动平面首轮实现已可运行，`web / terminal / browser / session_search` 均已接上最小可用 bridge，并通过回归测试

## 下一顺位

- 优先考虑 lifecycle review queue 的人工审核闭环：把当前已完成的 durable queue/audit/update/apply/provider-writeback 语义继续接到更完整的 review 操作面与审计模型
- 优先补 `TASK-020` 后续治理项：在现有 `profiles.json + backend-bindings.json + provider-bindings.json + memory_provider:jsonl / jsonl_vector / remote_http + preview_recall` 基础上，继续把 normalize/backfill 阶段仍保留的 legacy 顶层键压缩到最小集合
- 紧接补 `TASK-016` 后续项：在现有 `scope_breakdowns / record_rankings / augmentation_preview` 之上，继续减少仍散落在 top-level 或 report-only 的 provider-specific explainability
- 完成后再进入 promotion policy、dataset 筛选和真实 summarizer/provider 的进一步治理
- 2026-07-20：`TASK-SKILL-003-simple-task-fast-path` 第一批实现已完成，独立 reviewer iteration 3 为 `approved / 96 / C0 I0 M0`，最终新鲜验证已收口：入口先做当前消息初判；direct/lightweight 直接返回且零仓内写入，项目化请求恢复事实后再完成路由。范围不含 32 个工作 skill 的状态字段收敛。
- 2026-07-21：`TASK-SKILL-004-work-skill-status-envelope-owner` 第二批实现已独立复审通过：精确 32 个工作 Skill 去除四个重复项目状态字段并保留专业正文哈希；总控生成项目状态信封，本地 `status/needs` 原样透传。首次 `gitcommitzh` 因必要文件混有上游内容而 blocked；用户随后明确授权纳入形成完整提交所必需的同文件范围外改动，当前进入受限候选文件集本地提交。
- 2026-07-23：`TASK-IMPLEMENT-003-P001` 已完成 39 表知识索引、137 字段 PM 投影、稳定 locator/query CLI、异步项目状态同步、缓存维护与只读多页面站点；第四轮独立终审 `approved / 98 / C0-I0-M0`，精确范围本地提交已创建。
- 2026-07-23：`TASK-IMPLEMENT-003-P001` 第五轮整改完成：修复旧 ledger 事件状态丢失、任务去重/时区/父子状态推断和增量投影外键安全问题；项目总览改为六列中文敏捷看板，卡片中文标题、每列最近 10 条、“更多”展开及独立详情页均已落地。自动独立终审 `approved / 96 / C0-I0-M0`，当前进入精确范围本地提交。
- 2026-07-19 历史事件：`TASK-QUALITY-001-P001` 完成全仓静态债务清理并曾生成 `TASK-IMPLEMENT-001-R001`。该候选随后已被用户明确撤销，从未正式发布；原精确哈希 Gate 已关闭且不得恢复。当前状态只以本文件顶部 TASK-QUALITY-002 焦点为准。
- 2026-07-21：`PM-DASHBOARD-003` 页面原型已响应用户 Important 反馈：Excel 项目管理十要素从隐式映射改为显式、可点击驾驶舱，并补齐字段级详情映射；静态验证通过，`file://` 浏览器自动化受安全策略阻断，当前等待人工视觉复审。该旁路设计任务不改变主项目 Gate，未实现生产 renderer 或本地服务。
- 2026-07-23：`PK-SOURCE-MIGRATION-001-T04` 将任务详情改为目的、具体工作、交付结果和完成口径四段式，将需求页改为产品到验收标准四层树；138/138 注册任务简报均形成唯一任务实体并至少提取一类正式任务语义，任务简报与 Ledger 的父工作项限定身份已统一，推测性空态已删除。第三轮独立复审 `approved / 98 / C0-I0-M0`，两份设计增补保持候选未发布，当前等待用户确认预览；不改变 `FLOW-TASK-015` 的正式人工确认 Gate。
- 2026-07-23：`PROJECT-ARTIFACTS-001-T01` 已完成 Penpot 设计资产合同首轮评审整改：manifest/domain 必填与 ID 约束、Penpot 状态 Schema、路径链 symlink 拒绝、Token 独立解析/限长/校验及 CLI 回归均已验证；`v1.2.0` 保持候选未发布，当前等待同一独立 Reviewer 复审。整个工作项的 OpenAPI、测试资产、SQLite 投影和统一 HTML 展示仍在实施中。
- 2026-07-23：`PROJECT-ARTIFACTS-001-T01` Iteration 2 已继续封闭组件状态类型/唯一性、Schema 点段路径和合法 Token 集成 fixture；完整合同回归为 `33 passed`，当前再次等待同一独立 Reviewer 复审。
- 2026-07-23：`PROJECT-ARTIFACTS-001-T01` Iteration 3 独立复审通过，`approved / 97 / C0-I0-M0`；无伪 `.penpot`，`v1.2.0` 继续保持候选未发布。工作项进入 T02 OpenAPI 与稳定 YAML 索引。
- 2026-07-23：`PROJECT-ARTIFACTS-001-T02` 首轮独立评审 `changes_requested / 76 / C0-I3-M1`；Schema/domain、索引前验证门、完整 source definition 和占位 server 已同范围整改，联合回归 `48 passed`，当前等待同一 Reviewer 复审。
- 2026-07-23：`PROJECT-ARTIFACTS-001` 四项任务均已实现并独立批准：T01 Penpot 资产合同 `97`、T02 OpenAPI 详细合同 `99`、T03 测试合同与 SQLite 投影 `98`、T04 单一项目文档入口与增量快照 `96`。仓库不伪造 `.penpot`；真实源文件仍需在 Penpot 打开目标文件并连接本地插件后导出。
- 2026-07-27：`TASK-WORKFLOW-SEMANTICS-001` 已获用户关闭确认并通过新鲜关闭验证，完整语义套件 `50 passed`、Ruff 通过，终态为 `closed`。
- 2026-07-27：`SKILL-FLOW-AUDIT-001` 的隔离关闭门方案已获批准，但执行发现 `agent-harness-construction`、`article-writing` 缺少现有隔离测试节点；唯一聚合节点还读取 4 个范围外 Skill。任务按批准方案异常流程停在 `blocked`，尚未修改 Skill/Test；解阻需批准仅拆分 `tests/test_skill_flow_process_audit.py` 的现有断言。
- 2026-07-27：`PK-SOURCE-MIGRATION-001-T04-SCHEMA-REPAIR` 首轮独立评审为
  `changes_requested / 86 / C0-I1-M0`；`Task:` 身份元数据会被同行解析误当作 `goal`。
  生产缺陷已修复；Iteration 2 复审为 `changes_requested / 89 / C0-I1-M0`，仅缺
  `## Task` 章节正例以锁定上下文分离。该正例已补齐，双场景 `2 passed`、五文件
  `67 passed`；Iteration 3 最终复审 `approved / 99 / C0-I0-M0`。当前唯一 Gate
  是人工确认两份正式设计候选精确哈希；候选仍未发布。
- 2026-07-27：用户已确认 PK T04 重新冻结的两份候选精确哈希并授权正式化、验证、
  关闭和精确本地提交；同时批准 SKILL 仅拆分
  `tests/test_skill_flow_process_audit.py` 的现有聚合断言，不授权修改 Skill、其他测试
  或远端。
- 2026-07-27：`PK-SOURCE-MIGRATION-001-T04` 与 Schema repair 已正式关闭；
  data-design `v1.4.0`、frontend-design `v1.6.0` 生效。正式化后五文件
  `67 passed`、Ruff、Mypy 290、docs-stratego、固定快照和 Chrome 10/10 全绿；
  父 WorkItem 已完成，进入精确本地提交。
- 2026-07-27：`SKILL-FLOW-AUDIT-001` 隔离关闭门已按批准范围完成：仅拆分
  `tests/test_skill_flow_process_audit.py` 的现有聚合断言，关闭门收紧为 9 个候选/
  共享合同专属节点；`9 passed`、Ruff、9/9 SHA-256、JSONL 与 diff-check 通过，
  当前等待独立只读评审。
- 2026-07-27：SKILL 隔离关闭门独立评审已通过，`approved / 99 / C0-I0-M0`；
  Reviewer 确认 9 个节点不读取范围外 Skill、动态集合、历史 WorkItem 或共享 memory，
  最终关闭验证 `9 passed`、Ruff、9/9 SHA-256、JSONL 与 diff-check 全绿；
  `SKILL-FLOW-AUDIT-001` 已关闭，进入精确本地提交。
- 2026-07-27：`PM-DASHBOARD-003-T01` 已按人工批准完成一行 `minmax(0, 1fr)` CSS 根因修复；独立评审 `approved / 98 / C0-I0-M0`，桌面与 390px 移动端关闭验证通过，任务终态为 `closed`。父工作项仍是原型人工视觉评审状态，不代表生产 renderer、发布或部署获批。
- 2026-07-28：`STRATIX-SERVICE-GUIDE-001-T01` 已处理 I003：移除专业 Skill 的项目治理尾注并写明实际版本基线；四组定向契约测试 `28 passed`，独立复审 `approved / 100 / C0-I0-M0`，进入最终验证和精确本地提交。
- 2026-07-28：`PM-DASHBOARD-004-T02` 经同一 reviewer 复审 `approved / 100 / C0-I0-M0`，`T02-I1` 关闭，最终定向回归 `33 passed`。当前进入 T03，有效任务清理、确定性排序和业务首页实现中；T04-T05 尚未实施。
- 2026-08-23：`TEST-GOVERNANCE-001` 已完成旧平台测试引用、案例/报告模板和状态合同整改；首轮独立评审 `changes_requested / 80 / C0-I2-M1`，现已用精确暂存 hunk 隔离并行工作项并完成整改，隔离候选 `236 passed + 4 subtests`、Ruff、Skill validator 和 JSON/JSONL 全绿，等待同一 reviewer 复审。
- 2026-08-23：`TEST-GOVERNANCE-001` 同一 reviewer 复审 `approved / 98 / C0-I0-M0`，I1/I2/M1 全部关闭，无人工 Gate；下一动作是精确本地提交和提交后干净克隆验证。
- 2026-08-23：`TEST-GOVERNANCE-001` 已关闭；实现提交 `c4534ba` 的干净克隆为 `236 passed + 4 subtests`，Ruff、两个 Skill validator、25 JSON、36 JSONL、Git 状态和 diff check 全绿。
