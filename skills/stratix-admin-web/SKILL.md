---
name: stratix-admin-web
description: Stratix 管理后台前端开发规范。仅在用户明确提到 Stratix admin、Stratix web-admin、Stratix admin CRUD、stratix generate admin-page/admin-crud，或当前仓库事实显示是 Stratix web-admin 项目时使用；普通 admin-web、管理后台、运营后台或非 Stratix 前端任务不触发，优先使用 frontend-patterns 或项目实际技术栈。
---

# Stratix Admin Web

用于 Stratix 管理后台前端开发。只有明确 Stratix 线索或仓库事实显示是 Stratix web-admin 时才使用。目标是先识别重复 UI，再沉淀公共组件，最后逐页实现页面和页面逻辑。少写代码，复用现有能力，禁止为了“以后可能用”堆抽象。

## 适用边界

- Stratix `app web-admin` 项目。
- `stratix generate admin-page` 或 `stratix generate admin-crud` 生成的页面。
- Stratix 管理后台、运营后台、控制台、配置页、列表页、详情页、表单页和 CRUD 页面。
- Stratix 后台 UI 组件复用、页面结构、页面状态、权限动作、表格筛选和表单交互。

不适用于：

- 非 Stratix 的普通前端页面。
- 未说明 Stratix 的 admin-web、管理后台、运营后台或控制台项目。
- 营销站、官网、内容页、游戏和纯视觉稿。
- 后端 API、配置加密、release gate、`STRATIX_SENSITIVE_CONFIG` 或 Stratix 服务生产化验证；这些交给 `stratix-service`。
- 只需要 UI/UX 评审且不涉及开发落地；优先交给 `ui-ux-pro-max`。

## 输入

- 页面清单、路由、权限角色和业务流程。
- 已有组件、样式 token、图标、表格、表单、请求 client 和状态管理方式。
- API 契约、OpenAPI、mock 数据或 `admin-mock` 输出。
- 目标验证命令、浏览器检查范围和移动端要求。

## 版本兼容门

任何 Stratix 指导或生成前，先核对项目/生成器/CLI 版本与能力：读取 `package.json`、lockfile 和已安装包元数据，确认 `create-stratix --help` 与 `pnpm exec stratix --help`。本 skill 支持 `@stratix/create` `1.1.2` 和 `@stratix/forge` `1.1.4`；项目声明或安装的相关 `@stratix/*` 包也必须与对应 Stratix 支持矩阵一致，生成器能力必须实际列出 `app web-admin`、`admin-page` 或 `admin-crud` 才能使用相应命令。

未知或不兼容时，立即 `blocked`；回执列出相关项目/生成器/CLI 的 `detected`、`required`、`difference`、未执行的生成命令和唯一 `next_required_action`。不自动安装或升级，也不运行任何生成命令。

## 总原则

- 先读现有页面和组件。已有组件能用就用，别重写。
- 先检查既有页面和组件：记录查过的页面/组件文件、可复用模式和本页差异；据此列出公共组件候选后再实现页面。
- 公共组件只承载 UI 和稳定交互契约。数据请求、权限判断、业务校验和页面编排默认留在页面层。
- 两个不同页面出现相同 UI 和交互契约时，提升到公共 UI 组件。
- 只有样式相似、业务含义不同或 props 会膨胀时，不提升组件；用 CSS class、token 或局部组件即可。
- 不写万能表格、万能表单、万能详情页、万能 schema renderer。重复真实出现两次再抽。
- 不新增 UI 框架、状态库、表单库、图表库或拖拽库，除非项目已经使用或用户明确要求。
- 原生 HTML、CSS、浏览器能力和项目已有依赖优先。

## Stratix 工作流

1. 先通过版本兼容门，再探测项目和 CLI：
   - 读 `package.json`、lockfile 和已有目录。
   - 已有项目优先用 `pnpm exec stratix --help`。
   - 新项目先查 `create-stratix list templates` 和 `create-stratix list presets`。
2. 新建后台前端时，候选命令是：
   - `create-stratix app web-admin demo-admin --preset admin-mock,testing --no-install`
3. 生成页面时，先看实际 help，再选：
   - `stratix generate admin-page user`
   - `stratix generate admin-crud user`
4. `admin-mock` 只用于本地开发和测试。真实接口以项目 API client、OpenAPI 或已有后端契约为准。
5. 前端不得写入密钥、数据库配置、服务端 token 或 `STRATIX_SENSITIVE_CONFIG` 明文。

## 开发顺序

1. 查既有页面和组件：记录页面/组件文件路径、可复用布局/状态/交互模式，以及与目标页面的差异。
2. 产出页面清单和组件清单：页面名、路由、权限、API、主要状态、提交动作；候选组件、使用页面、状态、事件、数据输入、已有实现和是否公共化。
3. 先实现已确认会被两个以上页面复用的公共组件。
4. 再逐页实现页面结构、数据加载、表单提交、错误处理、权限动作和空状态。
5. 开发过程中发现第二个页面复制同一段 UI 时，立即停下提取公共 UI 组件。
6. 提取后删掉两处重复代码，只保留最小 props 和 callback。
7. 页面完成后跑最小验证，不扩大到无关测试。

## 公共组件边界

常见候选，不要默认全建：

- `AdminPageShell`：标题、面包屑、页面级 action。
- `AdminFilterBar`：筛选表单、重置、搜索。
- `AdminTableToolbar`：批量动作、刷新、密度、列设置。
- `AdminDataState`：loading、empty、error、permission denied。
- `AdminFormSection`：表单分组、说明、保存栏。
- `AdminStatusBadge`：状态文本、颜色和 tooltip。
- `DangerConfirmAction`：删除、禁用、重置等危险动作确认。

提升组件时检查：

- 两个页面的视觉结构一致。
- 交互事件一致。
- loading、empty、error、disabled 和 permission 状态一致。
- props 不超过当前真实需要。
- 组件名描述 UI，不绑定某个页面业务。

不提升组件时保留原因：

- 只有一个页面使用。
- 只是颜色、间距或文案相似。
- 两个页面后续会按不同业务演进。
- 抽出来会产生大量 boolean props 或 render callback。

## 页面逻辑规则

- 页面负责路由参数、权限分支、数据加载、提交、错误归因和跳转。
- 公共 UI 组件通过 props 接收数据，通过 callback 通知事件。
- 列表页必须覆盖 loading、empty、error、分页、筛选重置和权限不可见状态。
- 表单页必须覆盖初始值、校验失败、提交中、提交失败、成功跳转或停留策略。
- 删除、禁用、重置、批量操作必须有确认和失败反馈。
- 可访问性不能省：按钮语义、label、焦点、键盘路径和对比度要可用。

## 验证

- 静态改动：跑相关 lint、typecheck 或现有组件测试。
- 页面逻辑：补最小组件测试或页面 smoke test。
- 管理后台页面：用浏览器检查桌面和移动视口，确认文本不溢出、表格不挤爆、按钮可点击、错误状态可见。
- CLI 生成或 Stratix 项目结构变化：跑 `pnpm exec stratix doctor` 或项目已有等价诊断。
- 只报告真实运行过的命令和结果。

## 输出契约

交付时说明：

- 页面清单和组件清单。
- 新增或复用的公共组件路径。
- 哪些重复 UI 被提升，哪些没有提升以及原因。
- 页面实现范围、API/mock 来源和权限状态。
- 验证命令、结果和未覆盖风险。

```text
工作结果：
- work_item: <WORKITEM-ID or none>
- skill: stratix-admin-web
- status: ready_for_review | blocked | needs_user_input
- outputs:
  - <skill/page/component/test paths>
- evidence:
  - <commands, screenshots, smoke checks, or self-check notes>
- ledger_event: <event id or none>
- needs:
  - review | verification | user_input | none
```

版本未知或不兼容时也必须 `blocked`。`blocked` 用于缺页面清单、API 契约、权限模型、项目无法安装或 CLI 能力无法确认，导致无法安全实现。

`needs_user_input` 用于必须由用户决定后台信息架构、角色权限、危险操作策略或设计系统取舍。

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。
