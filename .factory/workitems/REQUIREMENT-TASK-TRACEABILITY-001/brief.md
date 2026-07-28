<!-- sf:document-id=REQUIREMENT-TASK-TRACEABILITY-001-BRIEF -->
# 需求分析条件化与任务分层

## 工作项

- 工作项：`REQUIREMENT-TASK-TRACEABILITY-001`
- 状态：`closed`
- 来源：用户于 2026-07-28 批准任务分层和需求分析条件化方案
- 分析模式：`embedded`
- 分析定位：`brief.md#需求分析`

## 目标

把需求分析从“固定文件必备”改成“分析内容必备、载体按复杂度选择”，并让任务用独立字段表达业务层级及正式关联目标。

<!-- sf:section-id=REQ-RTT-001 -->
## REQ-RTT-001：需求分析条件化

- 优先级：P0
- 状态：已批准
- 用户故事：作为项目负责人，我希望每次需求工程都完成必要分析，但简单项目不被迫生成独立文件，以便兼顾决策完整性和文档精简。
- `REQ-RTT-001-AC-1`：需求工程必须声明 `analysis_mode = embedded | standalone` 和可定位的分析位置。
- `REQ-RTT-001-AC-2`：`embedded` 把分析内容写入 PRD 或已批准需求包；`standalone` 写入 `requirements-analysis.md`。
- `REQ-RTT-001-AC-3`：需求到设计 Gate 校验分析内容和定位，不再无条件校验独立文件存在。
- `REQ-RTT-001-AC-4`：跨域、高风险、依赖复杂或需要独立评审时使用 `standalone`；其余情况默认 `embedded`。

<!-- sf:section-id=REQ-RTT-002 -->
## REQ-RTT-002：任务分层与关联

- 优先级：P0
- 状态：已批准
- 用户故事：作为项目负责人，我希望区分项目级、需求级、横切和系统任务，以便正确计算产品进度并追踪每项工作的来源。
- `REQ-RTT-002-AC-1`：任务简报必须声明 `task_scope = project | requirement | cross_cutting | system`。
- `REQ-RTT-002-AC-2`：`requirement` 至少强关联一个 `REQ/NFR`；`cross_cutting` 强关联一个或多个 `REQ/NFR`。
- `REQ-RTT-002-AC-3`：`project` 关联项目基线、章程或设计项，不强制关联单个需求。
- `REQ-RTT-002-AC-4`：`system` 只承载治理、同步、审计等系统工作，产品进度贡献为零。
- `REQ-RTT-002-AC-5`：任务层级进入现有项目知识实体详情；任务关系继续使用现有强关系图，不新增平行关联表。

## 需求分析

- baseline 影响：需求工程 Skill、文档目录与阶段 Gate、计划任务简报合同、Markdown 任务提取。
- 领域模块：`requirements-engineering`、`document-templates`、`writing-plans`、`project_knowledge`。
- 数据影响：不新增数据库表或关系类型；`task_scope` 和关联目标进入现有任务实体详情。
- 风险：旧任务没有 `task_scope` 时保持可读，新创建或重写的正式任务必须补齐。
- 非目标：不回填全部历史任务；不修改 PM 页面；不迁移已有 SQLite 文件。

## 完成口径

- 两项需求均有失败测试、最小实现和相邻回归。
- Skill 和模板不再把 `requirements-analysis.md` 描述为所有项目的无条件必备文件。
- 合法任务层级可被任务简报提取，非法值被拒绝。
- 独立评审通过且关闭前验证完成。
