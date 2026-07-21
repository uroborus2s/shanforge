# PM-DASHBOARD-002-T01 实现评审反馈分类

- 来源：独立任务评审 `/root/pm_dashboard_plan_review`
- 原决策：`changes_requested`
- 原评分：81/100
- 评审时间：2026-07-21

## I-1 AI 与确定性策略边界矛盾（Important）

- 要求：AI 只形成 `IntentCandidate`，注册工具由确定性策略选择和授权。
- 清晰度：yes。
- 技术核实：正确。reference 核心结论中的旧句与同文件九步流程和已批准计划矛盾。
- 决定：Fixed。
- 改动：删除“AI 选择注册工具”，明确“注册工具由确定性策略系统选择和授权”。
- 验证：`test_rendering_contract_keeps_ai_out_of_fact_computation` 通过。

## I-2 缺安全、权限和失败处置负向测试（Important）

- 要求：证明非法枚举、非合格快照、原始 fragment、script、事件属性、`javascript:`、未知权限字段和 ERROR_ONLY 旧业务值都会被拒绝或移除。
- 清晰度：yes。
- 技术核实：正确。原静态断言只能证明文档存在，不能证明固定 fixture renderer 的失败关闭行为。
- 决定：Fixed。
- 改动：测试 renderer 增加精确 slot、封闭枚举、安全 fragment allowlist、scalar 转义、权限投影和 ERROR_ONLY 源码净化；增加 8 个负向用例。
- 验证：完整 PM 看板套件 22/22 通过。

## I-3 浏览器只验证总览首屏（Important）

- 要求：十模块都要验证布局边界、裁切、重叠、对比度和交互控件焦点。
- 清晰度：yes。
- 技术核实：正确。原探针只把 `[data-first-screen-required]` 纳入几何检查。
- 决定：Fixed。
- 改动：每个模块固定检查 7 个直接内容块、4 个可交互控件、内部表格滚动容器、模块边界、焦点环和模块文本对比度。
- 验证：1440×900、1024×768、768×1024、390×844、320×568 五个精确 CSS 视口全部通过。

## M-1 未记录浏览器路径与版本（Minor）

- 技术核实：正确。
- 决定：Fixed。
- 改动：Playwright 探针返回实际 `browserExecutable` 和 `browserVersion`，测试同时校验 executable 存在和版本格式。
- 实际环境：Chrome for Testing `149.0.7827.55`。

## M-2 截图缺像素和人工检查证据（Minor）

- 技术核实：正确。
- 决定：Fixed。
- 改动：生成五张精确视口 PNG；Pillow 校验尺寸、至少两色和通道极差；人工查看 1440、768、320 三档。
- 结果：五张图颜色数 1537–2209，最大通道极差均为 255，无空白图。

## 结论

## U-1 Excel 只是一份一次性参考样例（用户澄清）

- 要求：读取样例结构后转化到 HTML 模板；项目查询不得每次读取 Excel。
- 清晰度：yes。
- 技术核实：现有运行时路径没有读取 Excel，但文档“Excel 十模块驱动”等措辞容易被理解为每次查询依赖样例。
- 决定：Fixed。
- 改动：增加“Excel 样例的一次性角色”合同；skill 明令运行时不得读取 `.xls` / `.xlsx`；HTML 移除“对应 Excel”用户界面文字；增加静态回归测试。
- 验证：完整 PM 看板套件 23/23 通过。

所有 Critical/Important/Minor 和用户澄清均已处理并有新鲜验证，进入同一独立 reviewer 的实现复审。
