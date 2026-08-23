# MODEL-DISPATCH-RUNTIME-001 实现摘要

## 交付结果

本候选没有新增 Shanforge 平台运行时。Sol 保留会话判断、任务分级、授权、质量门和收口；Codex 原生 `spawn_agent` 承担执行。项目配置提供 Sol、Luna worker、Terra worker 和只读 Terra reviewer；每次实现派发仍以父会话显式参数与工具接受回执为准。

## 执行任务

| 任务 | Sol 裁决 | 实际执行者 | 结果 |
|---|---|---|---|
| T01 Codex 配置 | `simple / low -> Luna` | `/root/model_dispatch_luna_config` | 四个 TOML 可解析，模型/推理强度/沙箱符合任务包 |
| T02 派发合同 | `standard / medium -> Terra` | `/root/model_dispatch_terra_contract` | 显式 spawn、父回执、失败关闭、稳定入口和人类文档完成 |
| T03 治理测试 | `standard / medium -> Terra` | `/root/model_dispatch_terra_tests` | Iteration 2 基线 Red 8 failed/1 passed；候选 Green 9 passed |
| T04 质量门 | `complex / medium` | Sol 验证 + 独立 Terra reviewer | Iteration 3 `approved / 96 / C0-I0-M0`；完整候选 `273 passed` |

## 关键边界

- `execution-workflow + source_or_test_write + authorized` 是 worker；完整的独立 `review-workflow + state_or_gate_write` 是 reviewer；错配或重叠失败关闭交回 Sol。
- `simple + low` 唯一映射 Luna；其他已授权实现映射 Terra。
- Luna/low、Terra/medium、独立 reviewer Terra/high；实现者固定 `fork_turns=none`，只拿完整 task brief。
- 工具未暴露、模型不可用、调用失败、回执缺失或模型不一致时失败关闭；Sol 不代写、不换模型。
- 父回执只能证明请求参数和工具接受，不能证明模型内部身份。

## 当前验证

- 完整 pytest：`273 passed`。
- Ruff：通过。
- Skill validator：`38/38`。
- TOML/JSON/JSONL 和 diff check：通过。
- 当前候选已通过独立终审，尚未提交；干净克隆验证在精确提交后执行。

## Review 整改

- I1：拆开 worker 与 independent reviewer 两个互斥 subagent 分支，增加 `dispatch_role` 与确定性表。
- I2：WorkItem/plan 创建事件改为 direct；T01–T03 执行 task brief 明确 `source_or_test_write/worker`，T04 明确 `state_or_gate_write/reviewer`。
- I3：模板和四张 task brief 补 `write_policy/current_gate/dispatch_role` 与精确验证命令；治理测试结构化解析表、brief 和 ledger。
- 完整回归发现并修复一次工作 Skill 跨边界点名，最终 `273 passed`。
- Iteration 2 删除重复兼容表，只保留严格派发事实源；补 workflow/write_policy 联合条件、冲突负例、T03 验证命令和 memory/ledger 稳定投影。
