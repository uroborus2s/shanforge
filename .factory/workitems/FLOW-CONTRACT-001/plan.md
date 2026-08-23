# FLOW-CONTRACT-001 当前计划入口

R020 正式设计已经发布并完成发布后验证。当前已把正式设计转换为 [TASK-IMPLEMENT-001-P001 实施计划](plans/TASK-IMPLEMENT-001-P001.md) 和 8 张代码任务卡；作者整改后独立复审 `approved / 96 / 0-0-0`。

| 项目 | 当前事实 |
|---|---|
| WorkItem | `FLOW-CONTRACT-001` |
| 当前 TaskCard | `TASK-IMPLEMENT-001-ai-workflow-platform-implementation` |
| 当前计划 | `TASK-IMPLEMENT-001-P001` |
| 正式设计输入 | `TASK-DESIGN-001-R020` / `DESIGN-RELEASE-TX-R020-G001` |
| 项目整体坐标 | 第 5/8 步“开发实现”进行中 |
| 当前节点 | T01–T08 实现、独立 Review、整改与主代理最终复验全部完成 |
| 当前状态 | `implementation_complete_with_preexisting_static_debt / ready_for_human_candidate_or_release_decision` |
| 计划 SHA-256 | `fd6c760009b295604a0018c335229ad5dba84c18b7d08b63d52ff2d122ad2a9f` |
| 独立复审 | `approved / 96`；Critical/Important/Minor=`0/0/0`；Decision SHA-256 `20e2e2c201eacd08a8181edacf2248b2423c5f55a0074d14a299eb09e521e839` |
| 作者验证 | 最终 validator `194/194 passed`；Node syntax、JSON、diff check 通过 |
| 代码任务 | T01 合同内核；T02 位置查询；T03 处置/Gate；T04 十五行回复；T05 evidence/CAS；T06 快速验证/transfer；T07 provenance；T08 装配/集成 |
| 执行 DAG | T01 → 并行 T02/T03/T05/T07 → T04(T02/T03)、T06(T05) → T08 |
| 产品代码写入 | T01–T08 已完成；正式发布、Git、远端、部署均为 0 |
| 后台任务 | 无；所有实施与复审代理均已结束 |
| 为什么停下 | 第 5/8 步开发实施已经完成，已到新的授权边界 |
| 是否影响下一项工作 | 全仓既有 Ruff/mypy `33/73` 是发布 concern；运行时和全量 pytest 已通过 |
| 下一责任人 | `uroborus` 决定静态债务清理或候选/正式发布授权；获授权后由 `AI_EXECUTOR` 执行 |
| 需要用户做什么 | 当前实施任务无需操作；启动下一阶段时选择授权范围 |
| 自动连续边界 | 获得一次授权后，Red/Green、任务验证、独立代码评审和同范围整改不逐项确认 |
| 仍需单独授权 | 正式发布、Git index/commit、Push/PR/Merge、远端、部署、凭证和不可逆动作 |

已知正式追踪漂移：requirements matrix 的部分行仍写“设计待重基线”。R020 released manifest 是当前实现合同；T08 只生成受控文档变更包，正式文档事务完成前不得声称 matrix 已同步。
