# T03 独立评审输入

- 任务：`PROJECT-ARTIFACTS-001 / T03`
- 目标：测试案例、单次结果、聚合报告三类合同与原子 SQLite 投影
- 任务简报：`task-briefs/T03-test-contracts.md`
- 实施报告：`reports/task-3.md`
- 验证证据：`evidence/task-3.md`

请重点核实：

1. 稳定测试定义是否和单次执行、聚合报告严格分离；
2. 七态、证据路径/hash、报告引用/计数是否失败关闭；
3. catalog 是否只投影为 `definition:*`，没有伪造通过；
4. `pk_test` 与 generation 是否处于同一事务，失败是否回滚；
5. JSON Schema、domain validator、YAML extractor 是否存在规则漂移。
