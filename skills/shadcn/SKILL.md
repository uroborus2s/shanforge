---
name: shadcn
description: shadcn/ui 项目与组件工作流技能。用于含 components.json 的项目，或用户明确要求 shadcn/ui、组件 registry、preset、组件添加/更新/调试/组合/样式修复时；优先读取本技能 rules、cli.md、customization.md 和 mcp.md，再按项目包管理器执行命令。
---

# shadcn/ui

用于在已有项目约束内使用 shadcn/ui。主入口只定义边界和交付契约；组件规则在 `rules/`，CLI 细节在 `cli.md`，定制与 preset 在 `customization.md`，MCP 说明在 `mcp.md`。

## 何时使用

- 项目存在 `components.json`，或用户明确提到 shadcn/ui、registry、preset、组件 add/update/diff。
- 需要选择、安装、更新、组合或修复 shadcn/ui 组件。
- 需要处理 shadcn 组件导入路径、Tailwind token、base/radix 差异、图标库或 registry 代码质量。
- 用户要求基于 shadcn/ui 创建表单、弹窗、导航、表格、侧边栏、图表、空状态等界面。

## 不使用

- 项目不使用 shadcn/ui，且只是普通 React/Tailwind/CSS UI 任务。
- 用户只要产品级 UI/UX 方向，不涉及 shadcn 组件规则；改用 `ui-ux-pro-max`。
- 需要浏览器截图或交互调试时，本技能只提供组件规则，实际验证交给项目测试或浏览器技能。
- registry、preset 或覆盖策略不明确且会写文件时，不猜测，先请求用户确认。

## 工作方式

1. 先读取项目里的 `components.json`、包管理器和现有组件目录；不要依赖注入式上下文。
2. 根据任务读取最小相关资料：
   - 样式规则：`rules/styling.md`
   - 表单：`rules/forms.md`
   - 组合结构：`rules/composition.md`
   - 图标：`rules/icons.md`
   - base/radix 差异：`rules/base-vs-radix.md`
   - CLI 和更新流程：`cli.md`
   - preset/主题定制：`customization.md`
3. 复用已安装组件；安装或更新前先预览影响，避免覆盖本地修改。
4. 组件代码优先使用语义 token、现有 alias、项目图标库和 shadcn 组合结构；不要手写一套同功能组件。
5. preset code 视为不透明值，直接交给 CLI；不要手动解码或抓取原始文件。

## 输出契约

非 Shanforge work item 的轻量交付至少回写：

- `status`: `done` 或 `blocked`
- `outputs`: 新增/修改组件、配置、样式文件或评审结论
- `evidence`: 已读项目上下文、引用的 rule/reference、CLI 预览或 diff、关键文件位置
- `verification`: 已运行的 typecheck、lint、test、build、组件渲染检查；未运行要说明原因
- `needs`: 仍需用户确认的 registry、preset、覆盖策略或视觉选择

若在 Shanforge work item 中使用，只回写状态包，不替 `using-shanforge` 决定 review、人工确认、提交或下一步 skill：

```text
工作结果：
- work_item: <WORKITEM-ID or none>
- skill: shadcn
- status: ready_for_review | blocked | needs_user_input
- outputs:
  - <component/config/style paths or review notes>
- evidence:
  - <components.json reads, rule/reference reads, CLI preview/diff, verification output, or evidence path>
- ledger_event: <event id or none>
- needs:
  - review | user_input | none
```

## 验证要求

- 添加或更新组件后读取实际落盘文件，检查导入 alias、缺失子组件、无障碍标题、图标库和 token。
- 表单、弹窗、菜单、命令面板、标签页、侧边栏等必须符合对应 `rules/` 文件。
- 会覆盖用户文件的命令必须先有预览或用户明确授权。

## Blocked 语义

返回 `blocked` 的情况包括：找不到项目配置、registry/preset 来源不明确、命令需要联网但失败、会覆盖本地改动且未获授权、所需组件 API 无法确认。`blocked` 必须写清已检查内容、风险和恢复所需的最小决定。

`needs_user_input` 用于必须由用户决定 registry、preset、覆盖策略、视觉取舍或安装授权的情况；可用现有组件安全完成时不要阻塞。

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。
