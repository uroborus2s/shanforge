---
name: stratix-admin-web
description: Stratix 管理后台前端开发规范。用户提到 Stratix admin、web-admin、admin CRUD、admin-page、管理后台页面、运营后台页面、后台公共组件或后台 UI 复用时必须使用；普通非 Stratix 前端任务优先使用 frontend-patterns。
---

# Stratix Admin Web

用于 Stratix 管理后台前端开发。目标是先识别重复 UI，再沉淀公共组件，最后逐页实现页面和页面逻辑。少写代码，复用现有能力，禁止为了“以后可能用”堆抽象。

## 适用边界

- Stratix `app web-admin` 项目。
- `stratix generate admin-page` 或 `stratix generate admin-crud` 生成的页面。
- 管理后台、运营后台、控制台、配置页、列表页、详情页、表单页和 CRUD 页面。
- 后台 UI 组件复用、页面结构、页面状态、权限动作、表格筛选和表单交互。

不适用于：

- 非 Stratix 的普通前端页面。
- 营销站、官网、内容页、游戏和纯视觉稿。
- 后端 API、配置加密、release gate 或 Stratix 服务生产化验证；这些交给 `stratix-service`。
- 只需要 UI/UX 评审且不涉及开发落地；优先交给 `ui-ux-pro-max`。

## 输入

- 页面清单、路由、权限角色和业务流程。
- 已有组件、样式 token、图标、表格、表单、请求 client 和状态管理方式。
- API 契约、OpenAPI、mock 数据或 `admin-mock` 输出。
- 目标验证命令、浏览器检查范围和移动端要求。

## 总原则

- 先读现有页面和组件。已有组件能用就用，别重写。
- 先总结相似组件，再开发公共组件，再开发每个页面和页面逻辑。
- 公共组件只承载 UI 和稳定交互契约。数据请求、权限判断、业务校验和页面编排默认留在页面层。
- 两个不同页面出现相同 UI 和交互契约时，提升到公共 UI 组件。
- 只有样式相似、业务含义不同或 props 会膨胀时，不提升组件；用 CSS class、token 或局部组件即可。
- 不写万能表格、万能表单、万能详情页、万能 schema renderer。重复真实出现两次再抽。
- 不新增 UI 框架、状态库、表单库、图表库或拖拽库，除非项目已经使用或用户明确要求。
- 原生 HTML、CSS、浏览器能力和项目已有依赖优先。

## Stratix 工作流

1. 先探测项目和 CLI：
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

1. 梳理页面清单：页面名、路由、权限、API、主要状态和提交动作。
2. 梳理组件清单：候选组件、使用页面、状态、事件、数据输入、是否已有实现、是否公共化。
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
- needs:
  - review | verification | user_input | none
```

`blocked` 用于缺页面清单、API 契约、权限模型、项目无法安装或 CLI 能力无法确认，导致无法安全实现。

`needs_user_input` 用于必须由用户决定后台信息架构、角色权限、危险操作策略或设计系统取舍。
