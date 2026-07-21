# TASK-SKILL-004-P001 Review Feedback Triage

## I-001

- 反馈来源：task review / independent subagent
- severity：Important
- 文件：共享回写合同、`using-shanforge`、正式 workflow design、owner 测试

### 理解

- 反馈要求：本职结果包的 `status/needs` 必须使用各工作 Skill 的本地枚举；总控和正式设计不得给出会覆盖本地信号的固定枚举；测试必须直接断言原样透传。
- 是否清楚：yes
- 需要澄清的问题：无

### 技术核实

- 是否技术正确：yes
- 证据：`api-design` 使用 `product_decision/compatibility_review/tests`，`systematic-debugging` 使用 `more_information/more_diagnostics/architecture_decision`，`writing-plans` 使用 `plan_review`；当前三处模板仍固定为总控枚举，和紧随其后的“不得统一或改写”正文冲突。
- 是否会破坏现有功能：no；改为占位符只消除歧义，不修改消费者专业正文。
- 是否与用户决策冲突：no
- 是否违反 YAGNI：no
- 当前实现是否有历史或兼容原因：固定枚举来自旧统一任务包，但第二批去重要求已经把项目 owner 与本地结果分层，旧模板不再适用。

### 处理决定

`Fixed`（待 finding-level RED/GREEN 和同一 reviewer 复审确认）。

### 验证

- 先新增 `test_local_status_and_needs_are_forwarded_without_normalization`，确认当前实现 RED。
- 最小修改三处模板后运行该测试、两个 owner 测试文件和相邻 Skill 回归。
