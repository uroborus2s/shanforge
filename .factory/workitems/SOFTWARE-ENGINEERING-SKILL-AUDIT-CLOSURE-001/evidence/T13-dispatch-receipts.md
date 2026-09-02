# T13 父工具派发回执补充证据

原始 `worker_dispatched` 事件保留不变。以下实际父工具回执按原 `dispatch_id` 追加到 ledger，未使用 worker 自报模型补足：

| Task | dispatch_id | requested_model | effort | fork | canonical_task | status | source |
|---|---|---|---|---|---|---|---|
| T10 | `...:T10:terra-medium:v1` | `gpt-5.6-terra` | medium | none | `/root/t10_executable_validation` | accepted | parent_tool_receipt |
| T11 | `...:T11:terra-medium:v1` | `gpt-5.6-terra` | medium | none | `/root/t11_response_owner_contracts` | accepted | parent_tool_receipt |
| T12 | `...:T12:terra-medium:v1` | `gpt-5.6-terra` | medium | none | `/root/t12_ambiguity_dispatch_contracts` | accepted | parent_tool_receipt |

三项 canonical task 均返回了可回读完成回执；完成事实仍由各自父级验证事件判断，`accepted` 不代表任务完成。T13-R01 和五位 reviewer 的派发从创建时即直接保存相同字段。

校验：ledger 每行 JSON 合法；三个 `dispatch_receipt_audited` 事件字段完整；event ID 与 idempotency key 唯一。
