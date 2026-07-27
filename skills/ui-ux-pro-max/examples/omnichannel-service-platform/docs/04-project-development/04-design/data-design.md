# 数据设计

## 版本信息

| 文档编号 | 版本 | 状态 | 负责人 | 更新日期 |
|---|---|---|---|---|
| `DOC-DATA-001` | `0.1.0` | 样例 | 数据与后端负责人 | 2026-07-24 |

## 版本历史

| 版本 | 修改内容 | 日期 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `0.1.0` | 定义核心实体与约束 | 2026-07-24 | AI 示例作者 | 待审核 | 待批准 |

## 核心实体

| ID | 实体 | Owner | 关键字段 |
|---|---|---|---|
| `DATA-SERVICE-001` | service | Catalog | id、name、status、duration、current_price_rule |
| `DATA-PROVIDER-001` | provider | Booking | id、qualification、service_area、status |
| `DATA-SLOT-001` | availability_slot | Booking | provider_id、starts_at、capacity、lock_version |
| `DATA-ORDER-001` | service_order | Order | order_no、user_id、status、service_snapshot、policy_snapshot、amount |
| `DATA-PAYMENT-001` | payment | Payment | channel_txn_id、order_id、status、amount、callback_version |
| `DATA-REFUND-001` | refund | Payment | payment_id、reason、amount、status |
| `DATA-EVENT-001` | order_event | Order | order_id、event_type、actor、occurred_at、trace_id |
| `DATA-AUDIT-001` | audit_log | Admin | actor、action、resource、before、after、reason |

## 关键约束

- `service_order.order_no` 全局唯一，用户可读；内部关联使用 UUID。
- `(user_id, operation, idempotency_key)` 唯一。
- `payment.channel_txn_id` 在渠道内唯一。
- 金额以整数最小货币单位保存，币种显式记录。
- 订单保存服务、价格、政策和展示名称快照。
- 时段扣减使用版本或数据库约束防止超卖，冲突返回业务错误。

## 隐私与保留

| 数据 | 规则 |
|---|---|
| 地址、手机号 | 默认脱敏；按履约需要短期授权；日志不得记录明文 |
| 支付凭证 | 只保存渠道必要标识，不保存银行卡敏感数据 |
| 审计日志 | 防篡改保存，按法规和公司政策设定保留期 |
| 已结束订单 | 业务保留期到期后匿名化，不破坏财务对账 |

## 索引

- 服务：`status + city + category`。
- 时段：`provider_id + starts_at`。
- 订单：`user_id + created_at`、`status + appointment_at`。
- 支付：`order_id`、`channel_txn_id`。
- 审计：`resource_type + resource_id + occurred_at`。
