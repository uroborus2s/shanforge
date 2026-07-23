# T02 Review Response

## Fixed

- `T02-I1`：Schema 补齐中文 pattern、20 字说明、REQ/NFR 稳定 ID pattern，以及
  至少一个常用成功码和错误码的双条件。
- `T02-I2`：typed YAML extractor 在生成任何实体前调用对应 domain validator；
  composition 注入真实代码 route 集合和严格 repository 的 design path 集合。
- `T02-I3`：组合 registry 保存完整登记定义，`read_bytes/stat` 同时核对 source ID
  和完整 `SourceDefinition`，伪造路径失败关闭。
- `T02-M1`：删除不存在的默认 server；宿主尚未声明监听地址时不发布占位服务器。

## Verified

- T02/T03 联合定向回归：`48 passed`
- 英文 summary extractor 负例：抛出 `CHINESE_SUMMARY_REQUIRED`
- forged source definition 负例：抛出 definition mismatch
- Ruff：`All checks passed!`
- Mypy：8 个源文件无问题
- 真实 `api validate --json` 与 `project index rebuild --json` 均成功

## Iteration 2

- `T02-I1`：不再枚举少数响应码。Schema 通过对象属性名规则要求至少一个
  `2xx/3xx` 和至少一个 `4xx/5xx`，domain 同步要求严格三位状态码。
- 说明长度规则增加首尾空白等价约束；`"中" + 19 个空格` 在 Schema 与 domain
  均失败。
- 新增 Draft 2020-12 行为测试：`206 + 418` 在两者均通过，缺成功或缺错误响应
  在两者均失败。

验证：OpenAPI 定向测试 `11 passed`；Ruff 与 Mypy 均通过。

## Iteration 3

- `T02-I1`：domain 不再忽略非法 response key；除三位 `100-599` 和 `default`
  外统一返回 `INVALID_RESPONSE_STATUS_CODE`。
- 增加 `206 + 418 + 2XX` 与 `206 + 418 + 600` 两个同样例，Schema/domain 均拒绝。
