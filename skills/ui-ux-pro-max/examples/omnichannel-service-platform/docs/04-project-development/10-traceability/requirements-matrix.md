# 需求追踪矩阵

## 版本信息

| 文档编号 | 版本 | 状态 | 负责人 | 更新日期 |
|---|---|---|---|---|
| `DOC-TRACE-MATRIX-001` | `0.1.0` | 样例 | 需求负责人 | 2026-07-24 |

## 版本历史

| 版本 | 修改内容 | 日期 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `0.1.0` | 建立需求到设计和验证的完整关系 | 2026-07-24 | AI 示例作者 | 待审核 | 待批准 |

## 使用说明

- 需求正文和验收标准以 [PRD](../03-requirements/prd.md) 为唯一事实源。
- 本矩阵不复制需求内容，只保存稳定 ID 和可读关系。
- 更新需求时只修改受影响行；不因文档行号变化更新关系。
- SQLite 可索引这些 ID、文档路径和标题锚点，Markdown 仍是可审计事实。

## 功能需求

| 需求 | 领域/数据 | API | UI 画板 | 验证 |
|---|---|---|---|---|
| `REQ-CATALOG-001` | `MOD-CATALOG`；`DATA-SERVICE` | `API-CATALOG-001` | `UI-IOS-001`、`UI-AND-001`、`UI-WX-001`、`UI-ADM-004` | `TC-CATALOG-001` |
| `REQ-CATALOG-002` | `MOD-CATALOG`；`DATA-SERVICE`、`DATA-PROVIDER` | `API-CATALOG-002` | `UI-IOS-002`、`UI-AND-002`、`UI-WX-002`、`UI-ADM-004` | `TC-CATALOG-001` |
| `REQ-BOOKING-001` | `MOD-BOOKING`；`DATA-SLOT` | `API-BOOKING-001` | `UI-IOS-003`、`UI-AND-003`、`UI-WX-003` | `TC-ORDER-001`、`TC-ORDER-002` |
| `REQ-ORDER-001` | `MOD-ORDER`；`DATA-ORDER`、`DATA-EVENT` | `API-ORDER-001`、`API-ORDER-002` | `UI-IOS-003`、`UI-IOS-005`、`UI-AND-003`、`UI-AND-005`、`UI-WX-003`、`UI-ADM-001`、`UI-ADM-002`、`UI-ADM-003` | `TC-ORDER-001`、`TC-ORDER-002`、`TC-ADMIN-001` |
| `REQ-PAY-001` | `MOD-PAYMENT`；`DATA-PAYMENT`、`DATA-EVENT` | `API-PAY-001`、`API-ORDER-002` | `UI-IOS-004`、`UI-IOS-005`、`UI-AND-004`、`UI-AND-005`、`UI-WX-004` | `TC-PAY-001`、`TC-PAY-002` |
| `REQ-FULFILL-001` | `MOD-FULFILLMENT`、`MOD-NOTIFY`；`DATA-EVENT` | `API-ORDER-002` | `UI-IOS-005`、`UI-AND-005`、`UI-ADM-003` | `TC-PAY-002`（状态恢复链路） |
| `REQ-AFTER-001` | `MOD-AFTER`；`DATA-REFUND`、`DATA-EVENT` | `API-AFTER-001` | `UI-IOS-005`、`UI-AND-005`、`UI-ADM-003` | `TC-AFTER-001` |
| `REQ-REVIEW-001` | `MOD-CATALOG`、`MOD-IDENTITY` | 本样例未单列评价端点；实现前扩充 OpenAPI | 订单详情的完成态入口；实现前增加评价表单画板 | 实现前增加评价专项用例 |
| `REQ-ADMIN-001` | `MOD-ADMIN`、`MOD-ORDER`；`DATA-ORDER`、`DATA-AUDIT` | `API-ADMIN-001` | `UI-ADM-001`、`UI-ADM-002`、`UI-ADM-003` | `TC-ADMIN-001`、`TC-ADMIN-002` |
| `REQ-ADMIN-002` | `MOD-ADMIN`、`MOD-CATALOG`；`DATA-SERVICE` | `API-ADMIN-002` | `UI-ADM-004` | `TC-CATALOG-001`（读取）；实现前增加变更专项用例 |
| `REQ-ADMIN-003` | `MOD-IDENTITY`、`MOD-ADMIN`；`DATA-AUDIT` | 管理接口统一授权策略 | `UI-ADM-005` | `TC-ADMIN-002` |

`REQ-REVIEW-001`、`REQ-ADMIN-002` 的专项测试，以及微信小程序的履约/售后详情画板尚未进入本 P0 样例，表中明确写出进入实现前的门禁，不以“待补充”掩盖缺口。

## 非功能需求

| 需求 | 设计落点 | 验证 |
|---|---|---|
| `NFR-SEC-001` | 架构授权边界、数据脱敏、审计与 API 错误语义 | `TC-ADMIN-002`；正式安全测试 |
| `NFR-REL-001` | 订单/支付幂等、事件状态机、对账恢复 | `TC-ORDER-001/002`、`TC-PAY-001/002` |
| `NFR-PERF-001` | 游标分页、查询索引、延迟指标 | `TC-NFR-PERF-001` |
| `NFR-ACC-001` | 四端平台矩阵、设计系统焦点/字号/对比规则 | `TC-NFR-ACC-001` |
| `NFR-COMP-001` | [跨端平台矩阵](../04-design/platform-matrix.md) | 正式发布候选兼容矩阵 |
| `NFR-OBS-001` | traceId、业务指标、审计和运维手册 | 发布后探针与告警演练 |

## 关系入口

- 领域和模块： [系统架构](../04-design/system-architecture.md)
- 数据实体： [数据设计](../04-design/data-design.md)
- API ID： [接口参考](../../03-developer-guide/interface-reference.md)、[API 设计](../04-design/api-design.md) 与 [OpenAPI](../../03-developer-guide/openapi/public-v1.openapi.yaml)
- UI ID： [UX/UI 设计](../04-design/ux-ui-design.md) 与 [Penpot 清单](../04-design/contracts/design-artifact-manifest.yaml)
- 测试 ID： [测试用例](../06-testing-verification/test-cases.yaml)
