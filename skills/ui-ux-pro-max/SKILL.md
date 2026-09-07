---
name: ui-ux-pro-max
description: 全平台 UI/UX、动效与 UI 素材交付。用于 Web、响应式网站、微信/支付宝等小程序、iOS/iPadOS/macOS、Android、Windows/Linux 桌面端，以及 Flutter、React Native、Taro、Avalonia 等跨平台产品；覆盖用户流、信息架构、线框、高保真确认、设计系统、UI 素材、组件状态、适配、可访问性、原型、微交互、页面转场、手势动效、开发交付和界面质量检查。UI 项目全流程归本 skill；不含 UI 设计且只需单张最终图片时直接用 `imagegen`；需要成套不属于 UI 项目流程的独立美术或游戏资源包时用 `art-asset-pipeline`。
---

# UI/UX Pro Max

把产品意图转成可实现、可验证、尊重平台习惯的 UI/UX 与动效方案。先复用项目事实，再补设计判断；不要把趋势、设计知识检索命中或单一平台规范当成通用答案。

## 硬边界

- 先读现有页面、设计稿、组件、token、品牌约束和目标用户；已有设计系统优先。
- 先定义共同的产品语义，再为各平台做原生映射；禁止把一套像素稿机械缩放到所有端。
- 官方平台规范和项目事实高于开源样例；开源项目用于学习工作流和结构，不用于照抄视觉、代码或受限资产。
- UI 项目从结构、视觉、交互、高保真确认、全页面/平台扩展、UI 素材到开发交付均由本 skill 负责；需要位图时直接使用 `imagegen`。`art-asset-pipeline` 只处理不属于 UI 项目流程的独立美术或游戏资源包。
- `shadcn` 负责含 `components.json` 的 shadcn/ui 组件工作流；`frontend-patterns` 负责前端代码架构；`webapp-testing` 负责可重复的页面交互验证。本 skill 保留设计决策与体验验收 owner。
- 新 React 管理后台的组件、图标和动效选型必须遵循 [管理后台设计](references/admin-web.md)，禁止页面级另选技术栈。
- 移动端要求高保真、品牌化或真实美术表现时，必须遵循 [移动端高保真设计](references/mobile-high-fidelity.md)；禁止把低保真 Penpot 画板或整张 AI 位图当成最终 UI 交付。
- 修改或创建 Codex skill 才使用 `skill-creator`；普通 UI 任务不得因此加载 skill 编写流程。

## 按需读取

只读取当前任务需要的 reference：

| 任务 | 必读 |
|---|---|
| 新设计、重构、设计评审或交付 | [设计流程与交付物](references/design-workflow-and-deliverables.md) 和 [视觉方向与质量](references/visual-direction-and-quality.md) |
| Web、H5、响应式页面、PWA | [Web 设计](references/web.md) |
| React 管理后台、运营后台、数据后台 | [Web 设计](references/web.md) 和 [管理后台设计](references/admin-web.md) |
| iOS、Android、小程序高保真视觉与美术交付 | [移动端高保真设计](references/mobile-high-fidelity.md)、目标平台 reference 和 [设计流程与交付物](references/design-workflow-and-deliverables.md) |
| 微信、支付宝、抖音等小程序 | [小程序设计](references/mini-programs.md) |
| iOS、iPadOS、macOS、SwiftUI/UIKit | [Apple 平台](references/apple-platforms.md) |
| Android、Compose、传统 View | [Android 平台](references/android.md) |
| Windows、macOS、Linux 桌面应用 | [桌面端设计](references/desktop.md) |
| 多端共用产品、Flutter、React Native、Taro、Avalonia | [跨平台映射](references/cross-platform.md) 和每个目标平台的 reference |
| 微交互、转场、手势、Lottie/Rive、动画验收 | [动效系统](references/motion.md) |
| 选择或更新外部参考 | [开源项目来源登记](references/open-source-landscape.md) |

## 工作流

### 1. 定义任务与证据

确认任务属于新设计/整体重设计、已有批准方向的扩展、局部修复、只读评审或动效设计。先确定目标平台和平台限制，再选视觉；已有批准方向只继承并扩展，局部修复直接解决目标问题，只读评审不写设计产物。新建或整体重设计才按 [视觉方向与质量](references/visual-direction-and-quality.md) 比较少量方向。提取：

- 产品目标、核心用户、主要任务、业务优先级和成功指标。
- 目标平台、设备等级、方向、窗口尺寸、输入方式、语言和无障碍范围。
- 已有品牌、组件库、设计 token、技术栈、平台限制和必须保留的行为。
- 交付层级：方向说明、用户流、线框、视觉稿、组件规范、动效稿、可运行原型、实现或评审报告。

能从仓库、设计文件或页面确认的事实不要反问用户。缺少会实质改变方向的品牌、平台或业务取舍时才返回 `needs_user_input`。

### 2. 建立体验骨架

先完成用户任务流、信息架构、页面/窗口清单、主次操作和状态矩阵，再选视觉风格。把业务对象、对象间关系和用户动作映射为页面区域、阅读顺序、主次密度与状态切换；不要先堆基础组件或按商品类型套页面。每个核心界面至少覆盖：

- 默认、加载、空、错误、离线、无权限、禁用、成功和部分完成状态。
- 首次使用、权限请求、登录/失效、返回/撤销、破坏性操作和恢复路径。
- 小屏、大屏、横屏、分屏、窗口缩放、键盘、触控、鼠标或手柄中适用的输入状态。

### 3. 形成设计系统

先按 `persuade`（说服/转化）、`operate`（高密度操作）、`read`（阅读/理解）、`experience`（沉浸体验）标记页面 surface；一个产品可以有多个 surface。先从产品事实写品牌方向记录：任务与内容优先级、布局骨架、字体层级/CJK、影像主体、1–2 个识别点、反方向、平台约束与截图/行为验证。`operate` 是高效完成具体工作，不等于后台模板；即使工具页不需要图片，也应以信息关系、排版、密度和状态反馈建立精致感。检索只服务这个已明确的意图，不能先替产品决定构图、品牌或字体；真实参考必须按 [视觉方向与质量](references/visual-direction-and-quality.md) 转化为本项目可验证的设计选择。

项目没有可复用设计系统且已有明确检索意图时，可运行：

以下 `<skill-dir>` 表示当前 `SKILL.md` 所在目录；执行前替换为该目录的实际绝对路径，不假设目标项目包含本 Skill 的 `scripts/`。

```bash
python3 <skill-dir>/scripts/search.py "<保留原意的中英文关键词>" --design-system -p "<项目名>" --platform <platform> --surface <surface> --locale <locale>
```

已有系统或只做局部评审时，不重新生成整套视觉语言。按需查询：

```bash
python3 <skill-dir>/scripts/search.py "<关键词>" --domain <product|style|color|typography|chart|ux|landing|icons|gsap>
python3 <skill-dir>/scripts/search.py "<关键词>" --stack <react|nextjs|vue|swiftui|jetpack-compose|flutter|react-native|javafx|wpf|winui|avalonia|uno|uwp>
```

设计知识检索命中或未命中都只是候选输入。中文请求由设计者在保留原意后提取中英文关键词，脚本不声称翻译；根据品牌、平台规范、可访问性、内容和实现成本筛选，不要把命中项原样拼成方案。未决项保留为未决，不以通用 Hero、字体或颜色补齐。

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

### 6. 高保真、素材与交付

按“低保真 → 少量代表性关键页确认 → 全页面/平台扩展”推进。仅在摄影、插画或纹理确为视觉必要时使用位图；方向样张可用 `imagegen`，但并非每个任务都必须生成。经美术方向确认与资源清单确认后，才生产正式素材并放入 `assets/`，以 manifest 记录路径、用途、尺寸、格式、来源和许可。组件、文字和通用图标保持可编辑的原生或代码实现；样板、正式美术资源和实现还原的职责与验收分离见 [设计流程与交付物](references/design-workflow-and-deliverables.md)。

可编辑设计源或项目链接，并标明版本，是主交付；PNG/PDF 页面图只作评审或归档预览。普通控件、真实文字、状态和通用图标由组件、平台能力或既有图标库实现，不烘焙进图片。

### 7. 交付或实现

按用户要求交付最小充分产物。设计稿必须能映射到页面、组件、状态和用户行为；实现必须复用既有组件、token、图标和框架约定。禁止在未授权时新增另一套设计系统或改写业务逻辑。

### 8. 验证

按目标平台执行适用检查：

- 核心任务流、返回/撤销、错误恢复和权限路径可走通。
- 文本放大、长文案、本地化、RTL、明暗主题和高对比度不破版。
- 键盘/焦点、屏幕阅读器、触控目标、颜色对比和非颜色提示符合目标规范。
- 安全区、系统栏、横竖屏、分屏、窗口缩放、折叠屏或多显示器行为明确。
- 动画可中断、尊重 reduced motion、不引发布局跳动，并在目标设备上测量流畅度。
- 有可运行页面时，优先使用项目 lint/test/build、浏览器截图、模拟器或真机；未运行必须写明原因和风险。
- 视觉样板/设计质量先以实际截图 critic：列出最多三项优先问题，修改后在同一视口复核；实现还原再独立核对设计源、组件、状态和交互。内容是否清晰、排版是否可读、资产是否一致、核心交互是否基本可用任一未达标时，不得仅凭自评推进。测试、静态检查或 AI 自评不能证明“好看”，只可证明各自覆盖的行为或约束。

## 风险与失败语义

- `blocked`：无法访问待评审界面或关键设计事实、目标平台工具不可用且无法替代验证，或授权/许可证不允许继续。
- `needs_user_input`：必须由用户选择品牌方向、目标平台、关键交互取舍或交付层级；能从项目事实合理确定时不要阻塞。
- `ready_for_review`：设计或实现产物、证据和实际验证齐备；作者不得自批 `approved`。
- 不声称已做用户研究、真机测试、无障碍审计或性能验证，除非存在真实记录。

## 完整样例

需要查看 Android、iOS、微信小程序和管理后台如何共享产品语义，又分别遵循平台习惯时，使用 [全渠道生活服务平台样例](examples/omnichannel-service-platform/README.md)。样例包含可复现的 Penpot 生成器、PRD、架构、数据、UX/UI、OpenAPI、测试、发布、运维和追踪关系。

把样例用于真实项目时，只复制该项目实际需要的文档；保留稳定 ID 和版本历史，删除不适用页面，不创建空模板或同一事实的平行版本。

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
