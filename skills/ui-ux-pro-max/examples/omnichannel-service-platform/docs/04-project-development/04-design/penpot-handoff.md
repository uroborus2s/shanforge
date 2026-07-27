# Penpot 设计交接

## 版本信息

| 文档编号 | 版本 | 状态 | 负责人 | 更新日期 |
|---|---|---|---|---|
| `DOC-PENPOT-001` | `0.1.1` | 样例 | UX/UI 负责人 | 2026-07-24 |

## 版本历史

| 版本 | 修改内容 | 日期 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `0.1.1` | 增加管理后台 shadcn/ui 组件交接 | 2026-07-24 | AI 示例作者 | 待审核 | 待批准 |
| `0.1.0` | 记录 MCP 生成与交接规则 | 2026-07-24 | AI 示例作者 | 待审核 | 待批准 |

## 事实源

- Penpot 文件：用户当前连接的真实设计文件。
- 页面与画板：见 [design-artifact-manifest.yaml](contracts/design-artifact-manifest.yaml)。
- 生成器：[`../../../tools/build-penpot-example.js`](../../../tools/build-penpot-example.js)。
- 仓内预览：只在 `export_shape` 成功后生成；当前导出状态见设计资产清单。

## 生成规则

1. MCP 插件必须保持 Connected。
2. Penpot 一次只能修改当前活动页面。
3. 按 `00-说明`、`01-设计系统`、`02-iOS`、`03-Android`、`04-微信小程序`、`05-管理后台` 逐页切换并执行生成器。
4. 同名画板已存在时跳过，防止重复生成。
5. 视觉修改后更新 manifest 的 page/board ID；导出成功时再更新快照和本文档版本历史。

## 开发交接

| 设计项 | 开发映射 |
|---|---|
| `UI-IOS-*` | SwiftUI Screen/View + iOS 平台导航 |
| `UI-AND-*` | Compose Screen + Android 返回/窗口行为 |
| `UI-WX-*` | 小程序 Page/Component + 宿主支付与页面栈 |
| `UI-ADM-*` | React Route/Page + shadcn/ui 组合；列表和详情独立路由 |
| `Yuexiang/Semantic` | 各端生成或手工映射的语义 Token |

管理后台画板的 `component-library` 插件数据固定为 `shadcn/ui`，`component-map` 记录设计角色到组件的映射。真实前端工程以仓内 `components.json` 为 CLI 配置事实源；Penpot 不生成或覆盖生产组件代码。

## 验收

- 画板名称使用稳定 UI ID 和中文标题。
- 核心按钮建立 P0 流程跳转，页面有 Flow 起点。
- 导出预览只是辅助证据；实现验收仍回到 Penpot、平台矩阵和状态要求。
- 任何缺失状态必须在开发前补设计或明确可接受降级，不能让开发自行猜测。

## 当前导出限制

Penpot MCP `export_shape` 对任意画板均返回 `http error`，无论是否指定文件路径。页面、画板、Token、Flow 和交互仍可通过 MCP 读取；本样例不提交不存在的 PNG，也不把导出失败误写成设计失败。
