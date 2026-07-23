# T02 Review Feedback Triage

四项反馈均已通过负例核实，技术上成立，且可在 T02 原范围内修复。

| ID | 严重度 | 核实 | 决定 |
|---|---|---|---|
| T02-I1 | Important | Schema 确实接受 domain 拒绝的 operation | Fixed |
| T02-I2 | Important | 英文 summary 仍被 extractor 投影 | Fixed |
| T02-I3 | Important | forged `SourceDefinition` 可读取 `README.md` | Fixed |
| T02-M1 | Minor | 不存在的默认 server 会误导 OpenAPI 客户端 | Fixed |

整改不改变四条 route，不新增运行服务，不扩大 source root。

## Iteration 2

复审指出 `T02-I1` 尚未完全关闭，核实成立：

- Schema 仅枚举少数响应码，domain 却接受完整 `2xx/3xx` 与 `4xx/5xx`；
- Schema 的 `minLength` 会把首尾空格计入长度，domain 会先 `strip`；
- 原测试只检查 Schema 结构，没有执行 Draft 2020-12 行为。

决定：继续在 T02 原范围修复。Schema 以 property-name 前缀规则表达成功/错误响应
各至少一个；domain 同步只接受三位状态码；使用 Draft 2020-12 验证器对同一正反样例
同时验证 Schema 与 domain。

## Iteration 3

复审抽测发现混入 `2XX` 或 `600` 时 Schema 拒绝、domain 忽略，核实成立。决定继续
失败关闭：domain 对所有 response key 强制 `100-599 | default`；`default` 可存在但
不计入成功/错误集合。新增“合法 206/418 加非法键”的同样例回归。
