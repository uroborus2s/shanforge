# 开源项目来源登记

## 使用规则

- 本表用于学习设计工作流、数据结构、平台适配和验证方法，不构成复制授权。
- 引用代码、数据、模板或资产前，必须复核具体文件的当前许可证、版权声明和商标规则。
- 星标和版本会变化。需要据此选择依赖或投入生产时，重新访问 GitHub 与官方文档。
- 项目事实和平台官方规范优先于本表；不得因项目高 Star 就忽略其适用范围。

## 2026-07-22 调研快照

| 项目 | 快照 | 学习点 | 许可证/边界 |
|---|---|---|---|
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 约 109k Star；v2.11.0（2026-07-13） | 可检索设计数据库、设计系统 Master + page overrides、栈规则 | MIT；本 skill 同步其 v2.11.0 数据/脚本并保留许可 |
| [storybookjs/storybook](https://github.com/storybookjs/storybook) | 约 90.6k Star；v10.5.3（2026-07-20） | 组件隔离、状态 story、文档、交互/无障碍/视口测试 | MIT；学习组件状态与验证方法 |
| [penpot/penpot](https://github.com/penpot/penpot) | 约 48.5k Star；v2.15.3（2026-05-14） | 开放标准、design token、组件/variants、Grid/Flex、设计到代码 | MPL-2.0；只吸收方法，不复制其受 MPL 约束源码 |
| [NervJS/taro](https://github.com/NervJS/taro) | 约 37.6k Star；v4.2.1（2026-07-17） | 小程序/Web/App 能力矩阵、跨端不等于行为相同 | MIT；平台规则仍以宿主官方文档为准 |
| [motiondivision/motion](https://github.com/motiondivision/motion) | 约 32.9k Star | Web/React 手势、spring、布局与编排边界 | MIT；不默认把库加入用户项目 |
| [airbnb/lottie-web](https://github.com/airbnb/lottie-web) | 约 32k Star | After Effects 到多端矢量动画的资产管线、特性兼容检查 | MIT；不同运行时支持面必须分别验证 |
| [AvaloniaUI/Avalonia](https://github.com/AvaloniaUI/Avalonia) | 约 31.2k Star；v12.1.0（2026-07-09） | Windows/macOS/Linux/移动/WebAssembly 的窗口与控件适配 | MIT；只作为跨桌面实现 reference |
| [android/compose-samples](https://github.com/android/compose-samples) | 约 23.3k Star | Android 官方 Compose 自适应、导航、状态和 Material 实例 | Apache-2.0；规范仍以 Android 官方文档为准 |
| [thesysdev/openui](https://github.com/thesysdev/openui) | 约 8.1k Star | 生成式 UI 的声明式中间表示、组件库约束和流式输出 | MIT；适合学习生成 UI 契约，不替代产品设计 |
| [open-pencil/open-pencil](https://github.com/open-pencil/open-pencil) | 约 7.2k Star；v0.13.2（2026-05-30） | AI-native 画布、components/variants、token 导出、design-to-code | MIT；项目较新，方法可参考，成熟度单独评估 |
| [ZSeven-W/openpencil](https://github.com/ZSeven-W/openpencil) | 约 4.3k Star | Design-as-Code、MCP、agent 可编辑画布 | MIT；较新且快速变化，不作为稳定规范源 |
| [microsoft/WinUI-Gallery](https://github.com/microsoft/WinUI-Gallery) | 约 3.6k Star；v2.9.3（2026-05-27） | WinUI 控件、Fluent 示例、桌面交互与系统行为 | MIT；Windows 规范仍以 Microsoft 官方文档为准 |

## 本 skill 采用的组合

- 从 UI/UX Pro Max 上游继承检索数据库和技术栈知识。
- 从 Penpot 学习 token、component/variant 和开放设计到代码映射。
- 从 Storybook 学习“组件 × 状态 × 视口 × 主题 × 输入”的验收面。
- 从 OpenUI/OpenPencil 学习结构化、可编辑、可追溯的生成设计产物，而不是只输出截图。
- 从 Taro 学习宿主能力矩阵和跨端分叉。
- 从 Compose Samples、WinUI Gallery、Avalonia 学习原生/桌面平台适配。
- 从 Motion 和 Lottie 学习运行时动效与资产管线边界。

## 更新检查

更新本 skill 前记录：调研日期、上游 tag/commit、许可证、近期开源活动、采用内容、未采用内容和原因。优先同步稳定 tag；不要直接用未发布 `main` 覆盖本地规则。
