# UI-UX-FULL-EXAMPLE-001 实施计划

## 授权执行包

- 允许新增：`.factory/workitems/UI-UX-FULL-EXAMPLE-001/**`
- 允许新增：`skills/ui-ux-pro-max/examples/omnichannel-service-platform/**`
- 允许修改：`skills/ui-ux-pro-max/SKILL.md`
- 允许外部写入：用户当前连接的 Penpot 文件
- 禁止：修改 Shanforge 根 `docs/`、业务源码、其他 work item；Push、PR、Merge、部署

## 文件结构

样例采用四大模块 `docs/`，只创建本样例真实使用的页面：

```text
skills/ui-ux-pro-max/examples/omnichannel-service-platform/
├── README.md
└── docs/
    ├── index.md
    ├── 01-getting-started/
    ├── 02-user-guide/
    ├── 03-developer-guide/
    └── 04-project-development/
        ├── 01-governance/
        ├── 03-requirements/
        ├── 04-design/
        ├── 05-development-process/
        ├── 06-testing-verification/
        ├── 07-release-delivery/
        ├── 08-operations-maintenance/
        └── 10-traceability/
```

## 任务

### T01：Penpot 设计基线

- 创建 `00-说明`、`01-设计系统`、`02-iOS`、`03-Android`、`04-微信小程序`、`05-管理后台` 六个页面。
- 创建语义 Token、组件样张和四端 P0 流程画板。
- 页面涵盖正常、加载、空、错误、权限、支付失败和恢复说明。
- 导出关键页面 PNG/SVG 到样例设计资产目录。
- 验收：MCP 返回页面/画板结构，导出文件可读取。

### T02：产品、需求与设计文档

- 创建入门、用户指南、项目章程、PRD、AC/NFR。
- 创建设计总览、架构、模块、数据、UX/UI、跨端矩阵、设计系统和 Penpot 交接。
- 验收：`REQ/NFR -> ARCH/MOD/DATA/UI` 关系完整。

### T03：开发者、API、测试与运维文档

- 创建开发者入口、环境说明、接口说明和 OpenAPI 3.1。
- 创建实施计划、测试计划、测试用例 YAML、测试结果 JSON、测试报告。
- 创建发布说明、回滚、部署和运维手册。
- 验收：OpenAPI、JSON/YAML 可解析；测试用例均引用需求 ID。

### T04：追踪、导航与 Skill 接入

- 创建根导航、各模块首页、需求矩阵和文档索引。
- 在 `ui-ux-pro-max/SKILL.md` 增加样例入口和使用边界。
- 验收：全部相对链接有效，不把样例误称为固定必备模板。

### T05：验证与评审输入

- 校验文件树、版本元数据、稳定 ID、链接和机器文件。
- 核对 Penpot 导出和设计清单。
- 写 evidence、实现报告和 review 输入。
- 验收：无占位语、无空文档、无绝对机器路径、无未解释的“待补充”。

### T06：移动端高保真视觉升级（asset_pack_approved_pending_penpot_sync）

- 保留现有 iOS、Android、微信小程序画板作为信息架构和流程骨架。
- 先生成三套“首页、服务详情、订单详情”高保真方向样张，只用于人工选择。
- 用户确认方向后，才生成资源清单、最终美术资源并原位升级 Penpot 画板。
- 验收：美术资源与交互组件分层；图片可追溯；三端遵守各自平台规范；未经确认的候选图不进入交付包。
- 当前：九项资源、manifest 和本地预览已通过独立评审；Penpot MCP
  实测无已连接插件实例，等待用户在目标文件点击 Connect 后同步移动端画板。

## 验证策略

- 定向：样例专用结构/链接/ID/YAML/JSON/OpenAPI 校验脚本或现有测试。
- 邻近：`uv run pytest` 中与 `ui-ux-pro-max`、文档模板相关的测试。
- 格式：Markdown 人工结构检查；JSON 用 `python -m json.tool`；YAML/OpenAPI 用项目已安装解析器。
- UI：MCP 结构读取 + `export_shape` 导出后视觉检查。
- 不运行：真实支付、微信审核、App Store/Google Play 发布和生产部署；样例不含实现代码。

## Gate

- 实现者最高状态：`ready_for_review`。
- 样例与模板内容完成后等待独立评审和用户视觉确认。
- T06 美术方向和资源清单分别设置人工确认门；任何候选图不得由执行者自行批准。
- 用户确认前，不把该样例上升为全项目正式文档策略。
