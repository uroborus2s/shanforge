# Review Fix Report

- finding：`STRATIX-GUIDE-I002`
- status：`approved_ready_for_local_commit`
- root_cause：把 skill 维护者的源码调查清单错误地设计成业务项目运行时 reference。
- fix：删除调查清单；运行时 skill 只保留已提炼规范和项目内版本/CLI 检查；保留标准
  工作 Skill 回写合同。
- unchanged：配置、环境、module、三层和 Kysely 规范内容未删减。
- rereview_iteration_1：`changes_requested / 92 / C0-I1-M0`；测试覆盖缺口已修复，等待 Iteration 2。
- rereview_iteration_2：`approved / 100 / C0-I0-M0`。
- adjacent_contract：仅同步并精确校验 `stratix-service` 的冻结 prefix hash；
  `receiving-code-review`、`writing-plans` 的并行改动不属于本任务。

## STRATIX-GUIDE-I003

- status：`approved_ready_for_local_commit`
- root_cause：共享测试把项目治理链接强制注入每个专业 Skill，导致无业务价值的尾注不能删除。
- fix：治理合同继续由 `using-shanforge` 持有；专业 Skill 可不重复引用。`stratix-service` 仅保留框架规范和精确版本边界。
- unchanged：配置、环境、module、三层和 Kysely 规范内容未改变。
- independent_review：`approved / 100 / C0-I0-M0`。
