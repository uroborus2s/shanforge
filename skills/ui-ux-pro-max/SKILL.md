---
name: ui-ux-pro-max
description: 全平台 UI/UX 与动效设计、实现约束和质量评审。用于 Web、响应式网站、微信/支付宝等小程序、iOS/iPadOS/macOS、Android、Windows/Linux 桌面端，以及 Flutter、React Native、Taro、Avalonia 等跨平台产品；覆盖用户流、信息架构、线框、视觉方向、设计系统、组件状态、适配、可访问性、原型、微交互、页面转场、手势动效、设计交付和界面质量检查。纯后端或只生成最终图片资源时不使用。
---

# UI/UX Pro Max

把产品意图转成可实现、可验证、尊重平台习惯的 UI/UX 与动效方案。先复用项目事实，再补设计判断；不要把趋势、数据库命中或单一平台规范当成通用答案。

## 硬边界

- 先读现有页面、设计稿、组件、token、品牌约束和目标用户；已有设计系统优先。
- 先定义共同的产品语义，再为各平台做原生映射；禁止把一套像素稿机械缩放到所有端。
- 官方平台规范和项目事实高于开源样例；开源项目用于学习工作流和结构，不用于照抄视觉、代码或受限资产。
- 只做 UI 结构、视觉、交互和动效方案时由本 skill 负责。需要生产图标、插画、启动图、精灵图或最终资源包时，转交 `art-asset-pipeline`。
- `shadcn` 负责含 `components.json` 的 shadcn/ui 组件工作流；`frontend-patterns` 负责前端代码架构；`webapp-testing` 负责可重复的页面交互验证。本 skill 保留设计决策与体验验收 owner。
- 修改或创建 Codex skill 才使用 `skill-creator`；普通 UI 任务不得因此加载 skill 编写流程。

## 按需读取

只读取当前任务需要的 reference：

| 任务 | 必读 |
|---|---|
| 新设计、重构、设计评审或交付 | [设计流程与交付物](references/design-workflow-and-deliverables.md) |
| Web、H5、响应式页面、PWA | [Web 设计](references/web.md) |
| 微信、支付宝、抖音等小程序 | [小程序设计](references/mini-programs.md) |
| iOS、iPadOS、macOS、SwiftUI/UIKit | [Apple 平台](references/apple-platforms.md) |
| Android、Compose、传统 View | [Android 平台](references/android.md) |
| Windows、macOS、Linux 桌面应用 | [桌面端设计](references/desktop.md) |
| 多端共用产品、Flutter、React Native、Taro、Avalonia | [跨平台映射](references/cross-platform.md) 和每个目标平台的 reference |
| 微交互、转场、手势、Lottie/Rive、动画验收 | [动效系统](references/motion.md) |
| 选择或更新外部参考 | [开源项目来源登记](references/open-source-landscape.md) |

## 工作流

### 1. 定义任务与证据

确认任务属于新设计、现有界面改进、实现约束、设计评审或动效设计。提取：

- 产品目标、核心用户、主要任务、业务优先级和成功指标。
- 目标平台、设备等级、方向、窗口尺寸、输入方式、语言和无障碍范围。
- 已有品牌、组件库、设计 token、技术栈、平台限制和必须保留的行为。
- 交付层级：方向说明、用户流、线框、视觉稿、组件规范、动效稿、可运行原型、实现或评审报告。

能从仓库、设计文件或页面确认的事实不要反问用户。缺少会实质改变方向的品牌、平台或业务取舍时才返回 `needs_user_input`。

### 2. 建立体验骨架

先完成用户任务流、信息架构、页面/窗口清单、主次操作和状态矩阵，再选视觉风格。每个核心界面至少覆盖：

- 默认、加载、空、错误、离线、无权限、禁用、成功和部分完成状态。
- 首次使用、权限请求、登录/失效、返回/撤销、破坏性操作和恢复路径。
- 小屏、大屏、横屏、分屏、窗口缩放、键盘、触控、鼠标或手柄中适用的输入状态。

### 3. 形成设计系统

项目没有可复用设计系统时，先运行：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<产品 行业 语气 密度>" --design-system -p "<项目名>"
```

已有系统或只做局部评审时，不重新生成整套视觉语言。按需查询：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<关键词>" --domain <product|style|color|typography|chart|ux|landing|icons|gsap>
python3 skills/ui-ux-pro-max/scripts/search.py "<关键词>" --stack <react|nextjs|vue|swiftui|jetpack-compose|flutter|react-native|javafx|wpf|winui|avalonia|uno|uwp>
```

检索结果只是候选输入。根据品牌、平台规范、可访问性、内容和实现成本筛选；不要把命中项原样拼成方案。

设计系统至少定义语义色、字体角色、间距、圆角、层级、图标、布局、组件状态、焦点、响应式/自适应规则和动效 token。页面级差异只写 override，不复制整套 token。

### 4. 做平台映射

先写共同语义，例如“返回上一级”“主操作”“多选”“导航层级”“临时浮层”，再映射到各平台控件、导航、单位、输入和系统行为。

跨平台方案必须给出矩阵，明确：共同内容、共享 token、平台专属组件、导航差异、输入差异、适配规则、能力降级和验收设备。平台差异不应被包装成主题色差异。

### 5. 设计动效

只为状态变化、空间关系、层级、反馈、注意力或品牌表达使用动效。每条动效写清：

- 触发、起止状态、属性、时长/弹簧参数、缓动和层级关系。
- 是否可中断、手势如何跟手、快速重复操作如何处理。
- `reduced motion`、低性能设备、后台恢复和动画失败时的替代行为。
- 实现载体、资产来源、性能预算和验证方法。

动效不阻塞输入，不用动画掩盖慢接口，不让装饰性运动抢过核心任务。

### 6. 交付或实现

按用户要求交付最小充分产物。设计稿必须能映射到页面、组件、状态和用户行为；实现必须复用既有组件、token、图标和框架约定。禁止在未授权时新增另一套设计系统或改写业务逻辑。

### 7. 验证

按目标平台执行适用检查：

- 核心任务流、返回/撤销、错误恢复和权限路径可走通。
- 文本放大、长文案、本地化、RTL、明暗主题和高对比度不破版。
- 键盘/焦点、屏幕阅读器、触控目标、颜色对比和非颜色提示符合目标规范。
- 安全区、系统栏、横竖屏、分屏、窗口缩放、折叠屏或多显示器行为明确。
- 动画可中断、尊重 reduced motion、不引发布局跳动，并在目标设备上测量流畅度。
- 有可运行页面时，优先使用项目 lint/test/build、浏览器截图、模拟器或真机；未运行必须写明原因和风险。

## 风险与失败语义

- `blocked`：无法访问待评审界面或关键设计事实、目标平台工具不可用且无法替代验证，或授权/许可证不允许继续。
- `needs_user_input`：必须由用户选择品牌方向、目标平台、关键交互取舍或交付层级；能从项目事实合理确定时不要阻塞。
- `ready_for_review`：设计或实现产物、证据和实际验证齐备；作者不得自批 `approved`。
- 不声称已做用户研究、真机测试、无障碍审计或性能验证，除非存在真实记录。

## 输出契约

非 Shanforge work item 的最终响应结尾必须单独回写：

- `status`: `done`、`blocked` 或 `needs_user_input`
- `outputs`: 设计说明、流程、状态矩阵、组件/动效规范、修改文件、原型、截图或评审清单
- `evidence`: 项目事实、检索命令、官方规范、设计文件、截图、浏览器/模拟器/真机记录或测试输出
- `verification`: 实际运行的检查及结果；未运行项和原因
- `needs`: 仍需确认的品牌、平台、设备、业务或资源问题

不得只把这些信息散落在正文中；字段无内容时写 `none`，未执行的验证写清原因。

若在 Shanforge work item 中使用，只回写状态包，不替 `using-shanforge` 决定评审、人工确认、提交或下一步：

```text
工作结果：
- work_item: <WORKITEM-ID or none>
- skill: ui-ux-pro-max
- status: ready_for_review | blocked | needs_user_input
- outputs:
  - <design notes, changed files, screenshots, prototypes, motion specs, or review checklist>
- evidence:
  - <project facts, source references, queries, screenshots, device checks, tests, or evidence path>
- ledger_event: <event id or none>
- needs:
  - review | user_input | none
```

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。
