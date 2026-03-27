---
name: web-artifacts-builder
description: 一套用于使用现代前端 Web 技术（React、Tailwind CSS、shadcn/ui）创建复杂的 claude.ai HTML artifact 的工具。适用于需要状态管理、路由或 shadcn/ui 组件的复杂 artifact，而非简单的单文件 HTML/JSX artifact。
license: 完整条款请参阅 LICENSE.txt
---

# Web Artifact 构造器

要构建强大的前端 claude.ai artifact，请遵循以下步骤：
1. 使用 `scripts/init-artifact.sh` 初始化前端仓库。
2. 通过编辑生成的代码开发你的项目。
3. 使用 `scripts/bundle-artifact.sh` 将所有代码打包成单个 HTML 文件。
4. 向用户展示生成的 artifact。
5. （可选）测试该 artifact。

**技术栈**：React 19 + TypeScript + Vite + Parcel (打包) + Tailwind CSS + shadcn/ui

## 设计与风格指南

非常重要：为避免产生所谓的“AI 废话感 (AI slop)”，请避免过度使用居中布局、紫色渐变、统一的圆角以及 Inter 字体。

## 快速入门

### 第 1 步：初始化项目

运行初始化脚本以创建一个新的 React 项目：
```bash
bash scripts/init-artifact.sh <项目名称>
cd <项目名称>
```

这将创建一个配置齐全的项目，包含：
- ✅ React + TypeScript (通过 Vite)
- ✅ 带有 shadcn/ui 主题系统的 Tailwind CSS 3.4.1
- ✅ 配置好的路径别名 (`@/`)
- ✅ 预装了 40 多个 shadcn/ui 组件
- ✅ 包含所有 Radix UI 依赖项
- ✅ 为打包配置好了 Parcel (通过 .parcelrc)
- ✅ Node 18+ 兼容性（自动检测并锁定 Vite 版本）

### 第 2 步：开发你的项目

通过编辑生成的文件来构建 artifact。请参考下文的**常见开发任务**进行指导。

### 第 3 步：打包成单个 HTML 文件

要将 React 应用打包成单个 HTML artifact：
```bash
bash scripts/bundle-artifact.sh
```

这将创建 `bundle.html` —— 一个包含所有内联 JavaScript、CSS 和依赖项的自包含文件。该文件可以直接作为 artifact 在 Claude 对话中分享。

**要求**：你的项目根目录下必须有一个 `index.html`。

**脚本作用**：
- 安装打包依赖项 (parcel, @parcel/config-default, parcel-resolver-tspaths, html-inline)
- 创建支持路径别名的 `.parcelrc` 配置
- 使用 Parcel 进行构建（无 source maps）
- 使用 html-inline 将所有资源内联到单个 HTML 中

### 第 4 步：与用户分享 Artifact

最后，在对话中与用户分享打包好的 HTML 文件，以便他们将其作为 artifact 查看。

### 第 5 步：测试/可视化 Artifact（可选）

注意：这是一个完全可选的步骤。仅在必要或应要求时执行。

要测试/可视化 artifact，请使用可用工具（包括其他技能或内置工具如 Playwright 或 Puppeteer）。通常，避免预先测试 artifact，因为这会增加从请求到看到成品之间的延迟。如有要求或出现问题，请在展示 artifact 后再进行测试。

## 参考资料

- **shadcn/ui 组件库**：https://ui.shadcn.com/docs/components
