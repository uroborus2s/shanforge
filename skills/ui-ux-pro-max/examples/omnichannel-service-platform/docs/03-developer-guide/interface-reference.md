# 接口参考

## 版本信息

| 文档编号 | 版本 | 状态 | 读者 | 更新日期 |
|---|---|---|---|---|
| `DOC-API-REF-001` | `0.1.0` | 样例 | 四端开发者、集成方 | 2026-07-24 |

## 版本历史

| 版本 | 修改内容 | 日期 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `0.1.0` | 建立公共接口说明 | 2026-07-24 | AI 示例作者 | 待审核 | 待批准 |

机器契约见 [public-v1.openapi.yaml](openapi/public-v1.openapi.yaml)。

## 认证

- 消费者端使用短期 Bearer Access Token；刷新凭证仅保存于平台安全存储。
- 微信小程序使用登录 `code` 换取平台会话，服务端不得把 `session_key` 返回客户端。
- 管理后台使用组织身份提供方登录，并在每个资源请求执行角色与数据范围授权。

## 关键接口

| ID | 接口 | 作用 |
|---|---|---|
| `API-CATALOG-001` | `GET /v1/services` | 搜索和筛选可售服务，不返回下架草稿 |
| `API-CATALOG-002` | `GET /v1/services/{serviceId}` | 返回服务内容、成交价规则和取消政策 |
| `API-BOOKING-001` | `GET /v1/services/{serviceId}/availability` | 查询人员与时间库存 |
| `API-ORDER-001` | `POST /v1/orders` | 锁定一次预约并创建待支付订单 |
| `API-PAY-001` | `POST /v1/orders/{orderId}/payments` | 创建支付意图，不直接宣称支付成功 |
| `API-ORDER-002` | `GET /v1/orders/{orderId}` | 查询订单、支付与履约聚合状态 |
| `API-AFTER-001` | `POST /v1/orders/{orderId}/cancellations` | 按规则取消并产生退款流程 |
| `API-ADMIN-001` | `GET /v1/admin/orders` | 按权限分页查询订单 |
| `API-ADMIN-002` | `PATCH /v1/admin/services/{serviceId}` | 修改服务草稿或未来价格 |

## 幂等与错误

- 创建订单和支付必须发送 `Idempotency-Key`。
- 同一用户、接口和请求内容在 24 小时内重复提交返回同一资源。
- 错误统一返回稳定 `code`、面向用户的 `message`、字段级 `details` 和 `traceId`。
- 支付回调是最终支付事实入口；客户端轮询只用于展示恢复。
