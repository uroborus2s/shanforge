# TASK-SKILL-004 任务简报

- work_item：`FLOW-CONTRACT-001`
- task：`TASK-SKILL-004-work-skill-status-envelope-owner`
- status：`user_authorized_required_overlap_ready_for_local_commit`
- plan：`.factory/workitems/FLOW-CONTRACT-001/plans/TASK-SKILL-004-P001.md`

## 目标

移除精确 32 个工作 Skill 重复携带的四个项目状态字段，由 `using-shanforge` 独占项目状态信封生成；保留工作 Skill 本职输出和真实阻塞/人工决策语义。

## 允许修改

- TASK-SKILL-002 计划列出的精确 32 个 `skills/*/SKILL.md`。
- `skills/using-shanforge/SKILL.md` 与新共享 reference。
- `docs/05-design/workflow-execution-design.md` 的统一任务包 owner 说明。
- 两个目标测试和必要相邻测试消费者。
- TASK-SKILL-004 artifacts、当前 ledger/review-ledger 和最小 memory summary。

## 禁止修改

- 32 个 Skill 的专业目标、触发、步骤、status 枚举、原输出和真实人工 Gate。
- 其余 5 个流程 owner Skill、`src/`、正式需求数量、候选/发布资产。
- 远端、发布、部署和凭证；本地 Git 仅在全部 Gate 闭合后由 `gitcommitzh` 执行。

## 完成口径

- 32/32 不再含四字段或重复项目化边界正文，只引用共享合同。
- 32/32 重复尾块之前的专业正文 SHA-256 与改动前完全一致。
- 总控工作结果包和项目状态信封分层清楚。
- 共享合同解释 `task_id/task_type` 与 `skill` 的不同职责，不归一化原专业输出。
- 正式设计、测试、黑盒、Skill validator 和独立 review 通过。
- 实现者不自批 approved。
- memory sync 后仅提交可安全分离的当前任务范围；无法与既有脏改动拆分时按 `gitcommitzh` 返回 blocked，不混入范围外文件。
