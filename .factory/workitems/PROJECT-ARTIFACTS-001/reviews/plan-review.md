# 计划评审

**状态：** 发现问题

**问题：**

- [执行前置条件]：目标文件含 `PK-SOURCE-MIGRATION-001-T04` 尚待人工确认的脏改动，
  原计划没有定义基线隔离与提交拆分，无法证明新提交独立。
- [全部任务，可构建性]：任务简报缺少精确文件、接口签名、Red/Green 步骤和预期输出。
- [T01-T03，文件边界]：主计划与任务简报允许路径冲突，共享 CLI/提取器的顺序不明确。
- [T01-T03，机器合同]：三个 schema、OpenAPI 扩展、实体 kind、locator、关系方向和
  `pk_test` 状态映射尚未锁定。
- [T03，规格覆盖]：结果与报告缺规范路径、校验入口、保留策略和 HTML 输入边界。
- [依赖与验证]：PyYAML、`pyproject.toml`、`uv.lock` 和 `uv sync` 未进入计划所有权。
- [T01/T04，HTML 附件]：未说明 PNG/SVG 是仅展示元数据还是复制/嵌入，当前文本发布器
  不能安全发布二进制附件。

**建议：**

- 保留 application-owned port、domain 不读文件、renderer 不解析 YAML 的总体边界。
- 使用 `uv run`，固定回执字段与退出码。
- 第二次快照明确断言 `cache_hit=true` 和未变化页面 hash 不变。
- source registry 只登记稳定定义；TestRunResult/TestReport 留在 evidence/cache。
- Penpot 未连接必须是合法等待状态，不生成伪 `.penpot`。

## 处理

上述问题由计划修订 R2 逐项关闭；修订后重新请求独立评审。

## R5 最终计划评审

**状态：** 通过

**问题：**

- 无阻塞问题。

**结论：**

- T01–T04 的职责、依赖、文件边界和独立验收已经闭合。
- Design manifest 与 OpenAPI 的实体、locator 和关系均有独立测试 node。
- 基线隔离、五层架构、机器合同、SQLite 原子性、派生数据边界和验证策略
  可进入执行候选。
