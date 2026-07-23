# T03 实施报告

## 结果

测试资产已拆成三个不同生命周期的合同：

1. `TestCaseCatalog/v1`：稳定测试定义，可进入来源注册与 SQLite；
2. `TestRunResult/v1`：一次真实执行结果，必须带七态之一和证据摘要；
3. `TestReport/v1`：只聚合已验证结果，不重复保存案例定义。

## 索引语义

- catalog 中每个案例生成稳定 `test:*` 实体和 `VERIFIES` 关系；
- `pk_test.test_status` 固定写为 `definition:<definition_status>`；
- 测试定义没有执行证据，`last_evidence_entity_id` 保持空；
- 只有后续真实 result source 才能表达通过、失败、阻塞等执行状态。

## 用户可见含义

T03 只建立合同与索引事实。T04 的质量页面必须把当前状态显示为
“测试定义已登记，尚未执行”，不得显示“已通过”。
