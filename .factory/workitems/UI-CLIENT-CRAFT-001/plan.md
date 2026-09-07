# 页面设计与美术质量实施计划

- 工作项：UI-CLIENT-CRAFT-001
- 状态：completed
- 输入：当前用户明确要求结合已讨论的问题实施优化；brief.md 是本次范围与验收事实。
- 架构：保留现有 UI skill 与平台 references；共享页面设计和双层视觉验收只定义一次。独立三页样板留在 evidence，不作为新模板或目标项目源码。
- 风险：medium。无远端、生产、数据写入或新依赖；审美效果不能由静态测试证明。

## 修改与作用

| 修改位置 | 怎么修改 | 解决的问题与作用机制 |
|---|---|---|
| UI skill 体验骨架与视觉方向 reference | 先写对象、关系、决策顺序和异常，再决定同屏比较、阅读顺序、密度与状态变化 | 避免从 Card/Button 清单开始；组件仍统一，但页面不再因此被限定为同一种卡片堆栈 |
| 视觉方向 reference 与用户指南 | 实际看图后记录可学方法、适用条件、项目转化与不照抄项 | 把“搜到案例/选了风格”推进到可观察的设计选择；不把 Star 或链接数当审美证据 |
| 设计交付与移动高保真 reference | 区分方向样板、正式美术资源、原生组件 | 需要摄影/插画时有独立资源质量责任；不需要图片的操作页仍必须设计排版、关系和反馈 |
| 验收入口与独立试做 | 分开检查设计质量、实现还原和功能行为；实际看普通业务页而不只首页 | 防止“忠实实现了粗糙设计”或“测试通过了”掩盖画面问题；不足返回具体页面整改 |

前期学习取其方法而非整套导入：[Anthropic frontend-design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) 的内容特异性、[TasteSkill](https://github.com/Leonxlnx/taste-skill) 的品牌一致性与移动端视觉样板、[Impeccable](https://github.com/pbakaus/impeccable) 的画面 critique 与浏览器复核。Shanforge 已有平台和交付流程，因此不安装重复框架、不照抄其风格偏好或固定组件数量。

## Work Breakdown

| id | parent_id | title | status |
|---|---|---|---|
| WBS-UI-CRAFT-01 | | 页面设计规则与回归场景 | completed |
| WBS-UI-CRAFT-02 | | 独立三页迁移试做 | completed |
| WBS-UI-CRAFT-03 | | 集中验证、中文与设计独立评审 | completed |

## 任务与精确路径

1. UI-CLIENT-CRAFT-001-T01 → WBS-UI-CRAFT-01：修改 SKILL.md、visual-direction-and-quality.md、mobile-high-fidelity.md、design-workflow-and-deliverables.md，均位于 skills/ui-ux-pro-max/；同步 docs/02-user-guide/user-guide.md；新增 tests/fixtures/ui-craft-cases.json 并在 tests/test_ui_ux_pro_max_skill.py 检查场景数据完整性。完整写集与路由见 task-briefs/UI-CLIENT-CRAFT-001-T01.md。
2. UI-CLIENT-CRAFT-001-T02 → WBS-UI-CRAFT-02，依赖 T01：执行者仅获取新版 skill、原始设计稿和用户请求，不提供父分析的布局答案；写集限定 evidence/pilot/ 的 index.html、styles.css、app.js、input.json、design-notes.md、verify.cjs、screens/、verification.json。这是一项独立迁移试做，不是同条件 A/B。
3. UI-CLIENT-CRAFT-001-T03 → WBS-UI-CRAFT-03，依赖 T01/T02：集中验证与独立只读 reviewer；中文表达、过度约束、范围和画面均检查。主控仅写治理与证据，不代写 worker 源码。源码和测试问题交原 owner 同范围修复。

## 实施与检查

- [x] 先运行现有目标测试；以现有教练原稿作为已观察的视觉失败样本。
- [x] T01 替换泛化表达，新增可观察场景，不堆叠普适美术禁令。
- [x] T02 制作并实际渲染三页候选；320/390/430 无横向溢出，导航与训练建议展开返回可用。初始断言不足，已在实际失败和回源反馈后补齐；不伪称全部验证先行。
- [x] 用同视口比较原稿与候选，检查文字、信息关系与细节；完成一次集中视觉整改，另修正运行/源事实与格式问题。未验证长文案和多权益组合已明确记录。
- [x] 运行目标测试、Ruff、skill validator、代码形状和 git diff --check；最终全仓当前为 406 passed / 11 subtests passed。
- [x] 独立 Terra high reviewer 已检查实际候选与变更，approved / 98 / C0-I0-M1；工程评分不作为美术批准。
- [x] 同步本 work item、会话卡与最小摘要。Skill 变更收口；样板仍未人工批准，不写入 ita-club。M-01 登记为正式采用前处理事项。

## 验证命令

使用 UV_CACHE_DIR=/tmp/shanforge-ui-uv-cache：

- uv run pytest -q tests/test_ui_ux_pro_max_skill.py tests/test_ui_design_candidates.py
- uv run ruff check tests/test_ui_ux_pro_max_skill.py
- uv run python skills/tdd-workflow/scripts/check_code_shape.py tests/test_ui_ux_pro_max_skill.py
- uv run python /Users/uroborus/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/ui-ux-pro-max
- node .factory/workitems/UI-CLIENT-CRAFT-001/evidence/pilot/verify.cjs（已有 Playwright 运行时通过 PLAYWRIGHT_MODULE 传入，路径只在命令证据，不进入可移植源码）
- uv run pytest -q
- git diff --check

## 同步与边界

只同步 .factory/memory/agent-session.md、current-state.md、tasks.summary.md、tests.summary.md、skill-updates.summary.md，并按 review 合同向 review-ledger.jsonl 追加本工作项事件；历史事实保留。API、服务、支付、真机和正式产品验收未运行且不在范围。不得修改 ita-club、宿主配置或全局 memory。Skill 机制验收不替用户批准新视觉；样板归档为候选，不成为通用布局模板。

## 计划自审

规格已映射三张任务卡，依赖顺序明确，所有源码/测试有单一 owner；无新依赖或 API；数据安全与正式视觉确认边界明确；现有测试加真实样板可运行。中风险、无公共契约变更，计划自审足够，不另造计划评审门。
