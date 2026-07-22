# TASK-SKILL-001：重构全平台 UI/UX 与动效设计 skill

## 目标

原位升级 `ui-ux-pro-max`。保留可检索设计数据库和 Shanforge 状态回写契约，补齐 Web、小程序、Apple、Android、桌面端、跨平台与动效设计的完整工作流和验证边界。

## 用户指定范围

- 覆盖 Web、小程序、iOS、Android、PC 客户端及跨平台 UI。
- 覆盖页面、组件、设计系统、交互、微动效、转场、手势和动画交付。
- 学习高 Star、持续维护的开源 AI 设计、设计系统、跨端和动效项目。
- 判断 `art-asset-pipeline` 与仓内 `skill-creator` 是否仍有独立价值。
- 使用系统 `skill-creator` 的结构、校验和 forward-test 方法完成本轮升级。

## 含义保留清单

- 目标：输出可执行的设计判断、实现约束和 UI/UX 评审结论。
- 触发：页面、组件、布局、视觉、交互、可访问性、响应式、动效和设计系统。
- 排除：纯后端、非视觉脚本、业务逻辑不改变界面的任务，以及更具体 skill 的专属工作流。
- 输入：现有页面、组件、设计系统、项目约束、目标用户、品牌和设备范围。
- 步骤：先读项目事实；按需运行 `search.py`；优先解决层级、可访问性、布局稳定、交互反馈和适配问题。
- 输出：设计说明、修改文件、评审清单、截图或原型；保留轻量和 Shanforge work item 两类状态包。
- 禁止：凭空重建设计语言、不必要地新增设计系统、把作者自检写成批准。
- 验收：设计映射到页面/组件/行为；代码改动有实际 lint/test/build 或说明；检查溢出、触控、焦点、对比、加载和错误状态。
- 失败：关键事实或工具缺失时 `blocked`；需要品牌、设备或业务取舍时 `needs_user_input`。
- handoff：项目化执行继续使用共享工作 Skill 回写契约，由 `using-shanforge` 决定后续 Gate。

## 新增能力清单

- 平台选择和跨平台语义映射，不再把 Web/移动端规则混成一套。
- 小程序的宿主能力、包体、设备、权限和真机验证约束。
- Apple、Android 和桌面端的原生导航、输入、窗口、无障碍和适配规则。
- 动效意图、时序、手势、中断、reduced motion、性能和资产格式契约。
- 从研究、流程、状态矩阵、设计系统、平台矩阵到 handoff 的交付物契约。
- 可追溯的开源来源登记、许可证边界和更新策略。
- v2.11.0 稳定数据与桌面技术栈检索能力。
- Codex `agents/openai.yaml` 元数据和真实场景 forward-test。

## 写集

- `skills/ui-ux-pro-max/**`
- `tests/test_ui_ux_pro_max_skill.py`
- `tests/test_work_skill_status_envelope_ownership.py` 中 `ui-ux-pro-max` 哈希一行
- `.factory/workitems/UI-DESIGN-SKILL-001/**`
- `.factory/memory/skill-updates.summary.md` 的本任务单独 hunk
- `.factory/memory/review-ledger.jsonl` 的本任务独立 review 单行事件

## 禁止

- 不修改或删除 `art-asset-pipeline`、仓内 `skill-creator` 及其既有脚本。
- 不触碰 `FLOW-CONTRACT-001` 当前设计、实现、候选和状态。
- 不覆盖工作区任何既有未提交改动。
- 不把开源项目的代码、资产或视觉语言未经许可复制进 skill。
- 作者不得自批 `approved`。

## 验收

- 系统与仓内 quick validation 均通过。
- 上游数据校验、搜索 smoke、定向 pytest、Ruff 和 diff check 通过。
- 至少用 Web、小程序、iOS、Android、桌面与跨平台动效场景做 forward-test。
- 独立 reviewer 给出 `approved`，或同范围整改并复审通过。
