# FLOW-TASK-015 方案级独立 Review

## 结论

- Decision：`changes_requested`
- Score：`46 / 100`
- Critical：`3`
- Important：`4`
- Minor：`0`
- Reviewer：`/root/project_knowledge_review`
- Human confirmation required：`false`

Reviewer 未参与方案编制，只读检查任务卡、正式设计、测试、checkpoint、evidence/report、限定 diff 和新鲜验证，未修改文件或 Git。

## Findings

- `FT015-C1`：正式 v1.1.0 已生效控制头与正文内 0.2.0 评审中控制块冲突；必须建立绑定正式基线 hash 的独立候选 delta，批准后再发布。
- `FT015-C2`：行为集合缺项且映射不唯一；工作流表缺 ledger/evidence 独立字段和明确输入输出 Gate。
- `FT015-C3`：WorkItem/TaskCard 可写“待创建”，memory 可作唯一追踪，写入门不是 fail-closed。
- `FT015-I1`：缺每个 workflow 的节点和合法转换；普通 Review 被错误普遍升级成人工 Gate。
- `FT015-I2`：测试只搜索短语，三个 Critical 存在时仍可 4/4 通过。
- `FT015-I3`：证据、报告和历史事件使用不存在的旧路径与过期状态，缺当前候选 delta 和新鲜验证。
- `FT015-I4`：规定相邻组合为 `2 failed / 51 passed`；Gate smoke 和 current-state 测试依赖可变真实任务状态。

## Gate

先做同范围技术整改；正式版本晋升时再进入相应人工治理 Gate。
