# T03 Review Feedback Triage

五项反馈均通过代码与反例核实，技术上成立，并可在 T03 原范围内修复。

| ID | 严重度 | 决定 |
|---|---|---|
| T03-C1 | Critical | 失败关闭伪通过，锁定步骤到整体状态的确定性聚合 |
| T03-I1 | Important | 测试数据值限定为 JSON 标量或对象 |
| T03-I2 | Important | domain 补 catalog 稳定 ID |
| T03-I3 | Important | trusted result 增加 run ID，报告必须同批次 |
| T03-I4 | Important | Draft 2020-12 与 domain 共用正反样例 |
| T03-M1 | Minor | 更新新鲜测试计数 |

## Iteration 2

复审指出 YAML 非 JSON 值和 report 共享负例仍有缺口，核实成立：

- `NaN/Infinity`、非字符串对象键和嵌套 set 不能无损表示为 JSON；
- 报告计数/跨 run 属于 domain 语义负例，但仍需要 Schema/domain 共用结构负例。

决定：domain 递归验证 JSON 值；Schema 继续描述合法 JSON 实例。增加 report 非法状态、
SHA 与未知字段的 Draft 2020-12/domain 共用负例。

## Iteration 3

复审发现顶层/嵌套数组语义和 YAML 自引用缺口，核实成立。锁定规则为：

- `test_data.value` 顶层仍只允许 JSON 标量或对象；
- 对象内部允许标准 JSON 数组；
- 所有容器执行 active-path identity 环检测；
- 最大嵌套深度 64，超过时结构化失败。

report 三个结构负例拆成独立参数化样例。
