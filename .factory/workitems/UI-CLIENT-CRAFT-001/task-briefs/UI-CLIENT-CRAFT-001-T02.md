# 独立教练端迁移试做
- work_item_id: UI-CLIENT-CRAFT-001
- task_card_id: UI-CLIENT-CRAFT-001-T02
- wbs_id: WBS-UI-CRAFT-02
- 状态：closed
- owner: terra-worker
- depends_on: UI-CLIENT-CRAFT-001-T01
- review_status: approved
- 优先级：P1
- 任务层级：project
- 关联目标：UI-CLIENT-CRAFT-001
- 强关系：IMPLEMENTS
- 上游计划：.factory/workitems/UI-CLIENT-CRAFT-001/plan.md
- 流水账：.factory/workitems/UI-CLIENT-CRAFT-001/ledger.jsonl
- current_gate: closed
- next_required_action: none
## 路由
- workflow_id: execution-workflow
- write_policy: source_or_test_write
- control_model: gpt-5.6-sol
- task_complexity: standard
- risk_level: medium
- execution_model: gpt-5.6-terra
- execution_authorized: true
- dispatch_role: worker
- dispatch_required: true
- dispatch_mode: subagent
- requested_reasoning_effort: medium
- fork_turns: none
- route_reason: 隔离三页视觉原型，无生产副作用；审美与交互不能由静态检查证明
- escalation_triggers: scope_expanded, input_conflict, risk_increased, verification_failed_twice, human_gate
## 精确写集
.factory/workitems/UI-CLIENT-CRAFT-001/evidence/pilot/ 内的 index.html、styles.css、app.js、input.json、design-notes.md、verify.cjs、screens/、verification.json。
## 任务输入
使用更新后的 skills/ui-ux-pro-max/SKILL.md 完成：ita-club 教练端很多页面只有基础组件堆砌，请在品牌约束内优化工作台、日程、学员详情三个页面，形成可点击候选。只做这三页，不扩展正式业务动作；现有 API、权限与首页不变。
只读输入为 /Users/uroborus/NodeProject/ita-club/docs/ui/miniapp-handoff/flow-redesign/coach/{design.md,data.js,index.html,styles.css,workbench-390.png,schedule-390.png,student-detail-390.png}。
保留真实 fixture 的内容与来源，必要时取三个页面所需最小子集；不得复制实际账号、支付参数或 token。日期按 fixture 明确标为样例日期，不声称今日实时数据。
一次候选试做预算：同一品牌内一个方向、三个关键页；这不是完整产品重新定向。不得在终端访问远端业务 API。外部参考仅允许公开只读；无法看图必须说明。
## 验收
生成便携静态 HTML/CSS/JS，无新依赖、无外部字体或素材下载，系统中文字形。可在 320/390/430 查看；导航/返回/阅读展开真实可用，范围外动作明确不可用，不假装已完成签到、保存或支付。
设计说明记录已观察的参考、事实到画面的转化、素材选择和未验证项。用浏览器实际检查三页，记录截图和实际行为。节点依赖用已有可用运行时，不提交本机依赖路径；verify.cjs 可消费 PLAYWRIGHT_MODULE 环境变量。
此样板不是正式批准设计，也不是随机盲评 A/B；不得自称 improved/approved。
## 禁止
不读父 plan/报告/预期答案，不修改原 ita-club、技能或其余文件；不提交/推送。你不是唯一执行者，不回退别人改动。不定义函数内命名函数，不抽取一次转发 helper。
## 返回
DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT；实际文件/命令/截图/未验证，不能自批美术验收。
