# TASK-SKILL-001 Revision 4 评审响应

## GO-R4-I-01：3 层硬上限存在豁免

接受并已修正。

- 删除“说明并增加测试即可超过 3 层”的例外。
- 明确 function literal、callback、事务闭包、goroutine 以及 `if/for/switch/select` 的计层口径。
- 无法降到 3 层时返回 `needs_user_input`，作者不能自行放行。

## GO-R4-M-01：Ponytail 决策顺序遗漏最少代码步骤

接受并已修正。

- 改为前四项均无法满足，且新增依赖或抽象有当前依据、比直接代码更小更安全时才允许采用。

## 执行者补充发现：非法 request ID 被静默替换

虽未被 reviewer 判为 finding，但该行为与“非法显式输入失败、不静默兼容”的严格口径冲突，已一并修正：

- 请求未提供 `X-Request-ID` 时生成安全随机值。
- 请求显式提供非法值时返回 HTTP 400 与稳定错误码 `invalid_request_id`。
- 随机源失败仍返回 HTTP 500，不生成弱 fallback ID。

所有结论待同一独立 reviewer 复核。
