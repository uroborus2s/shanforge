# WRITING-PLANS-SIMPLE-GATE-001-T01 验证

## 根因复现

共享本地状态合同仍只接受旧状态枚举，组合测试得到 `2 failed / 21 passed`：

- writing-plans 新增 `not_applicable` 后，旧状态字符串断言失败。
- 冻结专业前缀存在已落库但未同步的历史哈希，测试先在
  `receiving-code-review` 停止。

## Green

- writing-plans、相邻执行流程、共享合同定向组合：`20 passed`。
- Ruff lint：通过。
- Ruff format：`2 files already formatted`。
- Skill validator：`Skill is valid!`。
- 限定 diff check：通过。
- failed / error / skipped / not_run：`0 / 0 / 0 / 0`。

## 候选规则

- 简单局部代码加对应单测：`not_applicable / simple_change`，零计划产物。
- 明确要求正式计划，或涉及复杂拆分/高风险边界：正常生成计划。
- 状态和 needs 仍由共享工作 Skill 回写合同原样转发。

## 前向测试

独立 agent 仅收到候选 Skill 和原始请求：“在现有解析函数补空字符串 guard，并加一条
对应单测；不改公共接口、schema、依赖、迁移或发布方式。”

结果：

- `status: not_applicable`
- `reason: simple_change`
- `outputs: []`
- `evidence: []`
- `ledger_event: none`
- 不创建正式 plan 或 task brief，直接进入实现和定向验证。

## 暂存快照

干净 HEAD 加暂存差异上的直接候选节点：

- writing-plans 专属、共享状态、共享回写合同和冻结哈希：`10 passed`
- Ruff lint、format、Skill validator、JSONL、cached diff check：通过

扩大组合另有 3 个 HEAD 基线失败，均未纳入本候选：

- 2 个节点引用 HEAD 不存在的旧流程文档。
- 1 个节点等待另一任务尚未提交的 runtime skill 目录删除。
