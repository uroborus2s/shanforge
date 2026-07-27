# FLOW-TASK-015 实现报告

## 状态

- 工作项：`FLOW-CONTRACT-001`
- 任务：`FLOW-TASK-015`
- 状态：`ready_for_independent_implementation_review`
- 正式版本：`v1.2.0`，已在工作树原位发布
- 来源候选：`FLOW-TASK-015-C001`
- 发布事务：`FLOW-TASK-015-RELEASE-TX-001`

## 首轮结论

独立 Reviewer：`changes_requested / 46 / C3-I4-M0`。

## 整改

- `FT015-C1`：建立 `.factory` 受控候选 delta，绑定唯一正式文档路径、`v1.1.0` 基线 hash、TaskCard 和发布顺序；不在 `docs/` 新建第二份文档，不把候选写成已生效。
- `FT015-C2`：用 16 个稳定行为 ID 覆盖解释、澄清、需求、变更、方案、计划、执行、Bug、测试、Review、验证、提交、状态查看、恢复、暂停和废弃；每项唯一映射默认工作流，Handler 分列。
- `FT015-C3`：普通写入要求已存在且非空的 WorkItem 和 TaskCard；唯一创建例外只能原子写入 WorkItem、TaskCard 和首条 ledger，其他写入为零；memory 不得单独证明项目事实写入。
- `FT015-I1`：为当前 13 个工作流逐项定义允许节点、合法主路径、停止态和人工 Gate 规则；普通任务 Review 不自动进入人工 Gate。
- `FT015-I2`：结构测试解析 Markdown 表格，验证集合、唯一映射、必需列、非空值、负例、转换和精确基线 hash，不再只搜索短语。
- `FT015-I3`：重建当前路径、hash、前置状态、真实验证和候选 delta 证据；旧 ledger 事件保留为历史，不回写篡改。
- `FT015-I4`：Gate smoke 改为不可变缺 Review 快照；current-state 测试动态对账当前 active task。规定组合从 `2 failed / 47 passed` 恢复为 `56 passed`。

第二轮复审 `changes_requested / 82 / C1-I1-M0` 后继续整改：

- `FT015-C3`：新增优先级 120 的 `tracking-identity-workflow`、身份 intake 路由包、
  `identity_creating -> identity_readback -> reroute` 路径和 proposed ID 精确写集；普通业务写入仍要求已存在身份。
  `SB-RESUME` 的写合同补充条件必需 WorkItem/TaskCard。
- `FT015-I2`：行为、工作流和节点表均校验总行数等于唯一 ID 数和期望集合数；跨表验证 5 个写策略可达，
  并锁定 identity workflow、节点和 reroute。

## 验证摘要

- 结构测试：`7 passed`
- 状态独立回归：`22 passed`
- 规定组合：`56 passed`
- Ruff：通过
- Diff check：通过

## 边界

- 未修改正式 `docs/05-design/workflow-execution-design.md`。
- 未同步 runtime Skills。
- 未自批候选或正式发布。
- 未执行 Git 写动作。

## 下一动作

同一 Reviewer 复核全部 finding。批准后按候选发布顺序进入正式版本治理 Gate。

## 正式实施

- 保留唯一正式文档，原位发布 16 个会话行为、13 个工作流、5 类写入策略、逐工作流节点转换和状态包。
- 删除旧 `0.2.0 / 评审中` 重复控制块，保留统一任务包、六类任务和既有执行验证规则。
- 在 `using-shanforge` 同步唯一行为分类、身份创建例外、普通 route 必填字段和结果包。
- 在 `project-memory`、需求、计划、两种执行、两种 Review、Verification 共 8 个工作 Skill 中同步各自
  workflow、write policy、身份、allowlist、evidence 和 Gate 边界。
- 更新结构测试，使冻结候选、正式 v1.2.0 和 9 个 runtime Skills 同时受断言保护。
- 同步 TaskCard、ledger 和有界 memory 投影；未写远端状态。

## 正式实施验证

- Runtime Red / Green：`1 failed, 7 passed -> 8 passed`
- 规定组合：`57 passed`
- Ruff：`All checks passed!`
- Skill 校验：`9 / 9 valid`
- Diff check：通过
- 补充旧文档迁移测试：`2 failed, 7 passed`；两项均已在 verification evidence 中归因并保持范围外。

## 当前边界

- 未执行本地 commit；等待独立实现 Review。
- 未执行 push、PR、merge、发布部署或其他远端动作。
- Reviewer 若提出同范围 Finding，按既有授权整改并复审；不得扩大 TaskCard allowlist。

## 当前下一动作

独立 Reviewer 只读检查正式发布、runtime Skill 同步、测试与范围边界。

## 独立实现 Review 整改

- 首轮结论：`changes_requested / 76 / C0-I3-M0`。
- `FT015-IMPL-I1`：修复正式合同内两处旧自动人工 Gate 冲突。
- `FT015-IMPL-I2`：把结构测试从全文件短语搜索升级为正式/候选表一致、冲突负例和 runtime 区块精确映射。
- `FT015-IMPL-I3`：同步 implementation queue 与 tests summary，并由测试对账最新 ledger 状态。
- 整改 Red：`2 failed, 6 passed`。
- 整改 Green：定向 `8 passed`、规定组合 `57 passed`、Ruff 通过、Skill validator `9/9`。
- 同一 Reviewer 复审：`approved / 98 / C0-I0-M0`，三项 Finding 全部关闭。
- 当前状态：`approved_ready_for_exact_local_commit`。
