---
name: ui-ux-pro-max
description: UI/UX 设计智能与质量检查技能。用于界面结构、视觉风格、交互模式、可访问性、响应式布局、设计系统和前端体验质量评审；可读取本技能 data 与 scripts/search.py 获取颜色、字体、产品类型、UX 规则、图表和技术栈建议。
---

# UI/UX Pro Max

用于把 UI/UX 任务落成可执行的设计判断、实现约束或评审结论。主入口只保留工作契约；数据库、栈规则和样式资料在 `data/` 与 `scripts/search.py` 中按需查询。

## 何时使用

- 用户要设计、实现、重构或评审页面、组件、仪表盘、表单、导航、图表、移动端界面或响应式布局。
- 任务需要选择颜色、字体、间距、动效、信息层级、可访问性、交互状态或设计系统规则。
- UI 看起来“不专业”“难用”“不一致”，需要找出原因并给出可落地修复。
- 前端改动会影响用户看见、点击、阅读、填写、导航或理解的内容。

## 不使用

- 纯后端、数据模型、CLI、脚本、部署或非视觉性能问题。
- 只需要业务逻辑修复，界面行为和视觉不变。
- 已有更具体技能覆盖当前问题，例如 shadcn 组件规则优先交给 `shadcn`，浏览器操作优先交给浏览器测试类技能。
- 用户只要求解释某段非 UI 代码。

## 工作方式

1. 先读现有页面、组件、设计系统和项目约束，不凭空另起一套视觉语言。
2. 需要资料时运行只读查询，例如：
   `python3 skills/ui-ux-pro-max/scripts/search.py "<关键词>" --design-system`
3. 输出最小可执行建议：优先修信息层级、可访问性、布局稳定、交互反馈和响应式问题。
4. 实现时复用项目已有组件、token、图标和样式约定；不要新增无必要设计系统。
5. 评审时按严重度列问题，给出文件位置、影响、最小修复。

## 输出契约

非 Shanforge work item 的轻量交付至少回写：

- `status`: `done` 或 `blocked`
- `outputs`: 设计说明、修改文件、评审清单、截图或原型路径
- `evidence`: 查询命令、参考数据、截图、浏览器检查、文件位置或测试输出
- `verification`: 已运行的构建、测试、截图检查、可访问性/响应式检查；未运行要说明原因
- `needs`: 仍需用户确认的视觉方向、品牌素材、设备范围或业务取舍

若在 Shanforge work item 中使用，只回写状态包，不替 `using-shanforge` 决定 review、人工确认、提交或下一步 skill：

```text
工作结果：
- work_item: <WORKITEM-ID or none>
- skill: ui-ux-pro-max
- status: ready_for_review | blocked | needs_user_input
- outputs:
  - <design notes, changed files, screenshots, prototype, or review checklist>
- evidence:
  - <query commands, reference data, screenshots, browser checks, tests, or evidence path>
- ledger_event: <event id or none>
- needs:
  - review | user_input | none
```

## 验证要求

- 设计建议至少要能映射到具体页面、组件或用户行为。
- 代码改动后优先运行项目已有 lint/test/build；有页面时尽量用浏览器截图检查桌面和移动视口。
- 检查文本不溢出、交互目标可点击、焦点/键盘路径可用、色彩对比和加载/错误状态可见。

## Blocked 语义

只有在缺少关键输入且无法合理默认时才返回 `blocked`，例如无法访问待评审页面、项目依赖无法安装或关键视觉资产缺失。`blocked` 必须列出缺口、已尝试的证据和恢复所需的最小用户输入。

`needs_user_input` 用于必须由用户决定目标用户、品牌约束、设备范围、视觉方向或业务取舍的情况；能用项目现有设计系统合理默认时不要阻塞。

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。
