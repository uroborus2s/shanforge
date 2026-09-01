# SOFTWARE-LIFECYCLE-GOVERNANCE-001 实现摘要

## 交付结果

本候选把 Shanforge 的正式设计统一到当前 Skill-first 工程事实，并用一张生命周期矩阵说明需求、设计、计划、开发、测试、Review、提交、发布之间的输入、输出、Gate、模型 owner 和回流。没有新增仓内运行时、HTTP API、数据库、UI 应用或依赖。

## 任务执行

| 任务 | 模型路由 | 主要输出 | 结果 |
|---|---|---|---|
| T01 跨文档治理测试 | Terra / medium worker | `TEST-BB-002`、跨文档 pytest、Red/Green evidence | 初始 `5 failed / 1 passed`，最终专项 `8 passed` |
| T02 正式设计事实统一 | Terra / medium worker | 当前方案、技术、模块、数据、API、前端、UI、memory、接口设计；删除旧附件 | Skill-first 边界统一，无 `src/` 平台回退 |
| T03 生命周期与追踪 | Terra / medium worker | 生命周期矩阵、会话/工作流/风险/模型/任务/Gate 合同、索引与需求追踪 | 定向回归 `52 passed` |
| T04 集中质量 | Sol 验证；Terra / high reviewer | evidence、报告、Review 整改与复审输入 | `approved / 97 / C0-I0-M0`；候选全量 `290 passed + 4 subtests` |

## 事实源与删除项

- `docs/05-design/` 继续按领域 owner 保存人类可读正式设计；`docs/document-index.md` 登记正式版本。
- `docs/05-design/workflow-execution-design.md` 是生命周期、行为、工作流、风险、模型派发、任务和 Gate 的正式 owner。
- 删除没有当前消费者的 OpenAPI 文件、两份旧 schema、UI manifest 与 tokens，并从 artifact source registry 移除对应活动 roots。
- `.factory/workitems/SOFTWARE-LIFECYCLE-GOVERNANCE-001/` 保存执行事实；memory 仅投影当前任务和回源指针。

## 回归整改

- 第一次失败说明“压缩文档”不能删除仍被 Skill 和测试消费的现行合同；已恢复当前会话行为、工作流、风险、派发、六类任务、阶段门和质量门，同时拒绝恢复旧平台章节。
- 第二次失败说明同一快速通道事实必须在系统架构、API 和流程设计一致；已统一为先分类、仅项目化恢复、再路由和定界。
- 测试登记从占位 `not_run` 改为绑定单一主需求、真实 TaskCard、可执行命令、文件 evidence、通过结果和环境 ID。

## 当前质量

- pytest：`290 passed, 4 subtests passed`。
- Ruff：通过。
- Skill validator：`38/38`。
- `6 TOML / 176 JSON / 47 JSONL`、测试目录 5/5、diff hygiene：通过。
- 同一 reviewer iteration 3 已关闭 I1–I4，结果 `approved / 97 / C0-I0-M0`；本地提交与提交后干净克隆待后续 Gate。
