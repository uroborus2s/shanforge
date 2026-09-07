# 页面设计规则
- work_item_id: UI-CLIENT-CRAFT-001
- task_card_id: UI-CLIENT-CRAFT-001-T01
- wbs_id: WBS-UI-CRAFT-01
- 状态：closed
- owner: terra-worker
- depends_on: none
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
- route_reason: 多处技能合同关联，质量需真实画面验证，非单个静态检查可证明
- escalation_triggers: scope_expanded, input_conflict, risk_increased, verification_failed_twice, human_gate
## 精确写集
- skills/ui-ux-pro-max/SKILL.md
- skills/ui-ux-pro-max/references/visual-direction-and-quality.md
- skills/ui-ux-pro-max/references/mobile-high-fidelity.md
- skills/ui-ux-pro-max/references/design-workflow-and-deliverables.md
- docs/02-user-guide/user-guide.md
- tests/test_ui_ux_pro_max_skill.py
- tests/fixtures/ui-craft-cases.json
## 目标与实现
消费 brief 验收标准，在现有文件内做短而明确的增量；共享规则只定义一次。补足对象/关系到构图、视觉样板、参考看图转化、图片职责与双层验收。给出条件化例子而不是固定时间轴/卡片数量/风格的新模板。不删现有平台、状态、素材授权和局部修复边界。
新增少量结构化真实请求场景作为后续独立执行输入：教练工作端、影像主导客户端、批准基线扩展、局部修复/只读。每个案例固定 ID、原始请求、已知事实、允许范围、可观察成功条件与禁止事项，不预填结果。现有 test 文件只增加案例完整性/引用一致性检查，不把关键词命中当美术验收。
指南同步新增要求，不更改无关治理版本/字段。不要新增脚本或依赖。
## 验证
先运行 UV_CACHE_DIR=/tmp/shanforge-ui-uv-cache uv run pytest -q tests/test_ui_ux_pro_max_skill.py tests/test_ui_design_candidates.py。
更改后重跑同命令；执行 UV_CACHE_DIR=/tmp/shanforge-ui-uv-cache uv run ruff check tests/test_ui_ux_pro_max_skill.py、代码形状检查和 git diff --check。
规则效果交给独立样板试做，不以静态测试宣称美观。
## 禁止
不改写集外文件，不改 ita-club，不提交/推送，不生成独立过程报告，不读取完整 plan；你不是唯一执行者，不回退其他人的改动。
源码/测试不定义函数内命名函数，不抽取单调用点且无独立职责的 helper。
## 返回
DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT；列实际修改、命令 exit code、通过数、未验证与 concerns。不得自批 approved。
