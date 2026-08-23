# PRD 摘要

## 当前正式基线

- PRD：`docs/04-product/prd.md`
- 版本：`v5.0.0`
- SHA-256：`081778a065c1d8c9420cc6b4a511c0b50b2c4ea6de7032683856c54e0902c8c0`
- 状态：已批准并生效
- 来源：`MODEL-ROUTING-001`
- 负责人 / 变更 / 审核 / 批准：`uroborus`

## 当前产品边界

- Shanforge 是由代理宿主加载的 skill-first 软件工厂资产。
- 仓库不提供 `src/` 平台运行时、模型网关、数据库、公共 API、SDK 或独立服务。
- `using-shanforge` 是唯一流程控制面，专项 skill 执行需求、设计、实现、测试、评审和交付。
- 事实分层为 `docs/` 正式事实、ledger 执行事实、memory 有界恢复摘要。
- 交付候选必须通过工作区与只含 Git 跟踪文件环境的同一验证命令。
- Sol 负责总体设计、分级和路由；Terra/Luna 只执行授权任务包。

## 需求集合

- 当前有效：`REQ-SF-001` 至 `REQ-SF-009`、`NFR-SF-001` 至 `NFR-SF-006`。
- 追踪矩阵：`docs/04-product/requirements-matrix.md`，`v5.0.0`，
  SHA-256 `a0d6875ae91d3bab4b09cb5745db2474b9551083f29d5a00190bcc454448d8ca`。
- 文档索引：`docs/document-index.md`，SHA-256
  `debcfead6c922ebb9b8031c35e6ac313128363a117b2c1844e1149b281dbbfc3`。
- `v4.2.0` 及更早平台运行时正文只存在于 Git 历史，不参与当前实现、完成度或路由。

## 当前停点

- `MODEL-ROUTING-001-T01` 正在整改独立 review finding。
- T01 通过、形成本地基线提交并完成干净克隆复验前，不启动 T02。
