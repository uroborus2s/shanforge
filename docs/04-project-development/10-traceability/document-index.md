# 文档索引

## 1. 文档目标

集中登记项目正式文档、负责人、状态、主要读者和关联追踪 ID。

## 2. 当前正式文档索引

| 文档路径 | 文档类型 | 主要读者 | 负责人 | 状态 | 关联编号 |
|---|---|---|---|---|---|
| `docs/01-getting-started/project-overview.md` | 入门说明 | 新读者、协作者 | 仓库维护者 | 已发布 | DOC-START-001 |
| `docs/02-user-guide/user-guide.md` | 用户指南 | 使用者、协作者 | 仓库维护者 | 已发布 | REQ-006 |
| `docs/03-developer-guide/interface-reference.md` | 开发者指南 | 开发者、集成方 | 仓库维护者 | 已发布 | API-* |
| `docs/04-project-development/03-requirements/prd.md` | 需求文档 | 产品、研发、测试 | 仓库维护者 | 已确认基线 | REQ-* |
| `docs/04-project-development/04-design/solution-overview.md` | 总体设计 | 架构、维护者 | 仓库维护者 | 已确认基线 | MOD-* |
| `docs/04-project-development/04-design/action-registry-and-autonomy-policy.md` | 架构设计 | 架构、脚本维护者、平台维护者 | 仓库维护者 | 已发布 | API-010, API-011, ADR-004, ADR-005 |
| `docs/04-project-development/04-design/frontend-adapters-and-multi-agent-coordination.md` | 架构设计 | 架构、平台维护者、协作负责人 | 仓库维护者 | 已发布 | API-012, API-013, ADR-006 |
| `docs/04-project-development/04-design/skill-evolution-mechanism.md` | 能力治理设计 | 技能维护者、平台维护者、QA | 仓库维护者 | 已发布 | GAP-006 |
| `docs/04-project-development/04-design/source-docs-standard-upgrade-analysis.md` | 升级分析 | 架构、文档维护者、脚本维护者 | 仓库维护者 | 已发布 | TASK-006 ~ TASK-010 |
| `docs/04-project-development/05-development-process/software-development-process.md` | 过程文档 | 项目协调者、维护者 | 仓库维护者 | 已发布 | PROC-* |
| `docs/04-project-development/05-development-process/implementation-plan.md` | 实施计划 | 项目协调者、文档维护者、QA | 仓库维护者 | 已发布 | TASK-* |
| `docs/04-project-development/06-testing-verification/test-plan.md` | 测试文档 | 测试、维护者 | 仓库维护者 | 已发布 | TC-* |
| `docs/04-project-development/07-release-delivery/release-notes.md` | 发布文档 | 维护者、使用者 | 仓库维护者 | 已发布 | REL-* |
| `docs/04-project-development/08-operations-maintenance/deployment-guide.md` | 运维文档 | 维护者、发布负责人 | 仓库维护者 | 已发布 | OPS-* |
| `docs/04-project-development/10-traceability/requirements-matrix.md` | 追踪矩阵 | 项目协调者、维护者 | 仓库维护者 | 已发布 | TRACE-* |

## 3. 维护规则

- 新增正式文档时同步登记。
- 文档 owner 变化时同步更新负责人。
- 需求、接口、函数、发布、运维文档都要带可追踪编号。
- 废弃文档不要直接删除索引记录，应标记状态和替代文档。
