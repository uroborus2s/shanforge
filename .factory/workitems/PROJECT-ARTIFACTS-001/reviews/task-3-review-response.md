# T03 Review Response

## Fixed

- `T03-C1`：整体状态由步骤按
  `error > failed > blocked > cancelled > passed/skipped/not_run` 确定；
  `passed` 必须有步骤、登记证据，且每个步骤引用证据。
- `T03-I1`：Schema/domain 均拒绝数组测试数据，仅允许 JSON 标量或对象。
- `T03-I2`：domain 强制 `TEST-CATALOG-*` 稳定 ID。
- `T03-I3`：`ValidatedTestResult` 保存 `run_id`，报告逐项核对同一运行批次。
- `T03-I4`：真实 Draft 2020-12 validator 与 domain 共用 catalog/result/report
  正反样例，包括伪通过样例。
- `T03-M1`：证据更新为当前树 `59 passed`。

## Verified

- T03 定向合同、提取器、索引：`68 passed`
- Ruff：通过
- Mypy：通过

## Iteration 2

- `T03-I1`：新增递归 JSON value gate；拒绝非有限数字、非字符串对象键、数组、
  set 及任何嵌套非 JSON 值。JSON Schema 描述合法 JSON 实例，YAML 到 JSON 的
  可无损转换由 domain 在投影前失败关闭。
- `T03-I4`：新增 report 共享结构负例；非法状态、非法 SHA 与未知字段同时经过
  Draft 2020-12 validator 和 domain。跨 run 与计数一致性仍由 domain 语义校验。

## Iteration 3

- `T03-I1`：顶层数组继续禁止，对象内部允许 JSON 数组；递归 gate 增加环检测和
  64 层上限，自引用 YAML 返回 `INVALID_TEST_DATA_VALUE`，不抛异常。
- `T03-I4`：report 的非法状态、非法 SHA、未知字段拆成三个独立共用负例。
