---
name: frontend-patterns
description: 前端开发模式、组件边界、状态管理、性能和可访问性评审。用于实现或审查前端交互时，优先沿用项目既有框架、设计系统和测试栈。
---

# 前端开发模式

用于前端实现建议、代码评审和小范围重构。主入口只给决策路径；框架示例按项目现有技术栈选择，不把 React、动画库或测试框架当作默认答案。

## 何时启用

- 设计或修改组件、页面、表单、导航、状态和数据加载。
- 处理前端性能、可访问性、响应式布局或错误状态。
- 评审前端代码是否符合项目既有 UI 规则和工程模式。

## 边界

- 先读取项目已有组件、样式、状态、路由和数据访问模式。
- 优先使用语义化 HTML、CSS、浏览器能力和已安装依赖。
- 不新增 UI 框架、状态库、动画库或表单库，除非用户明确要求或项目已经使用。
- Bug 根因不清楚时，先进入系统化调试；本 skill 不替代根因调查。
- 完成声明前必须有新鲜验证证据；本 skill 不替代完成前验证。

## 决策表

| 场景 | 默认选择 | 升级条件 |
|---|---|---|
| 局部组件状态 | 本地状态或受控 props | 多个兄弟或下游组件共享且已有全局状态模式 |
| 数据加载 | 项目现有 fetch/client/server action | 需要缓存、重试或并发控制且项目已有工具 |
| 表单 | 原生控件和既有校验方式 | 跨步骤、复杂 schema 或项目已有表单库 |
| 性能 | 先定位真实慢点 | 数据量大、重复渲染可观测、交互卡顿可复现 |
| 动画 | CSS 或已有动效规范 | 复杂编排且项目已有动画方案 |
| 可访问性 | 键盘、焦点、语义、对比度必查 | 复杂控件需要 ARIA 模式和辅助技术验证 |

## 工作流

1. 明确用户流程和变更范围：组件、页面、数据路径、状态来源。
2. 对照现有代码找可复用模式，不重新造 helper。
3. 选择最小实现：能用平台能力就不用库；能局部处理就不扩散到全局。
4. 覆盖 loading、empty、error、disabled、permission 和 mobile 状态。
5. 按风险运行验证，并记录命令、输出摘要和残余风险。

## 风险分级验证

- 低风险：文案、样式、静态布局。运行相关 lint/typecheck 或截图检查即可。
- 中风险：状态、表单、数据加载、组件复用。增加或更新单元/组件测试，并做目标页面 smoke check。
- 高风险：认证、支付、删除、跨端兼容、核心转化流程。运行集成测试或目标 E2E，不扩大到无关端到端套件。

## 输出契约

- 实现任务：说明改动文件、用户可见行为、验证命令。
- 评审任务：按严重度列问题，给文件和行号，只报可执行问题。
- 架构建议：给一个最小可落地方案和不做项。

```text
工作结果：
- work_item: <ID>
- skill: frontend-patterns
- status: ready_for_review | blocked | needs_user_input
- outputs:
  - <files or review notes>
- evidence:
  - <commands, screenshots, or manual checks>
- ledger_event: <event id>
- needs:
  - none | tests | design_decision | human_confirmation
```

`design_decision` 只是 `needs` 值，不是状态。必须由用户决定视觉、交互或产品取舍时，回写 `status: needs_user_input`。

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。
