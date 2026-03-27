# 山海工枢项目文档

**项目名称：** 山海工枢 / shanforge  
**文档状态：** 已建立基线  
**主要读者：** 项目维护者 | 规则设计者 | 协作者 | 最终使用者  
**最后更新：** 2026-03-27

## 1. 这套文档解决什么问题

本目录是当前仓库面向人类的唯一正式项目文档入口。

它的目标不是替代代码、脚本或 AI 记忆，而是把这套山海工枢（`shanforge`）项目的需求规划、方案设计、使用说明和演进策略整理成一组可阅读、可交接、可持续演进的正式文档。

当前文档体系采用两层分工：

- `docs/`：正式的人类阅读文档，作为需求、设计、使用说明和追踪关系的事实来源。
- `.factory/`：在被管理项目中生成的 AI 压缩记忆、过程记录和工作项，不替代 `docs/`。

说明：

- 与软件工厂项目本身直接相关的人类说明文档，已经全部收敛到 `docs/`。
- `workflows/` 目录不再承载这类正式项目说明；它只保留与个别专项技能或临时流程相关的辅助资料。

## 2. 推荐阅读路径

如果你第一次接触这个项目，建议按下面顺序阅读：

1. [项目章程](./00-governance/project-charter.md)
2. [产品需求文档](./02-requirements/prd.md)
3. [总体方案与协作总览](./03-solution/solution-overview.md)
4. [系统架构设计](./03-solution/system-architecture.md)
5. [用户指南](./08-handover/user-guide.md)
6. [高主动性与自进化集成方案](./09-evolution/agent-motivation-autonomy-integration.md)
7. [历史项目纳管 checklist](./04-delivery/historical-project-onboarding-checklist.md)
8. [历史项目标准提示词模板](./08-handover/historical-project-prompt-templates.md)

如果你是维护者，继续读：

1. [需求分析文档](./02-requirements/requirements-analysis.md)
2. [技术选型与工程规则](./03-solution/technical-selection.md)
3. [模块边界文档](./03-solution/module-boundaries.md)
4. [API 设计文档](./03-solution/api-design.md)
5. [需求追踪矩阵](./traceability/requirements-matrix.md)
6. [高主动性与自进化集成方案](./09-evolution/agent-motivation-autonomy-integration.md)
7. [历史项目纳管自动化入口设计](./03-solution/historical-project-onboarding-automation.md)

## 3. 目录说明

| 目录/文档                                                 | 用途                                            | 主要读者             |
| --------------------------------------------------------- | ----------------------------------------------- | -------------------- |
| `00-governance/project-charter.md`                        | 说明项目目标、范围、成功标准和风险              | 项目负责人、维护者   |
| `01-discovery/input.md`                                   | 记录原始创意、边界和当前要确认的问题            | 产品、需求、架构     |
| `01-discovery/brainstorm-record.md`                       | 保留方案比较与决策过程                          | 产品、需求、架构     |
| `01-discovery/current-state-analysis.md`                  | 作为历史项目纳管时的现状基线模板                | 协作者、架构、维护者 |
| `02-requirements/prd.md`                                  | 给出正式需求、场景、验收和 NFR                  | 产品、开发、测试     |
| `02-requirements/requirements-analysis.md`                | 分析优先级、依赖、可行性和设计影响              | 架构、开发、测试     |
| `02-requirements/requirements-verification.md`            | 校验本轮需求文档是否可进入设计                  | 产品、架构、QA       |
| `03-solution/technical-selection.md`                      | 说明 CLI-first 技术路线和工程规则               | 架构、开发、维护者   |
| `03-solution/solution-overview.md`                        | 汇总产品定位、分层方案、生命周期与协作治理      | 维护者、架构、协作者 |
| `03-solution/system-architecture.md`                      | 说明系统分层、组件关系和关键数据流              | 架构、开发、测试     |
| `03-solution/module-boundaries.md`                        | 明确模块职责、依赖和禁止耦合                    | 架构、开发、测试     |
| `03-solution/api-design.md`                               | 说明 CLI 命令接口和文件契约                     | 开发、集成方、维护者 |
| `03-solution/historical-project-onboarding-automation.md` | 说明历史项目纳管自动化入口的设计与 MVP 实现边界 | 架构、脚本维护者     |
| `04-delivery/historical-project-onboarding-checklist.md`  | 给出历史项目纳管的执行清单与退出标准            | 项目协调者、维护者   |
| `08-handover/user-guide.md`                               | 面向实际用户的使用说明和常见任务                | 使用者、协作者       |
| `08-handover/historical-project-prompt-templates.md`      | 提供历史项目纳管和后续维护的标准提示词模板      | 使用者、协作者       |
| `09-evolution/agent-motivation-autonomy-integration.md`   | 说明高主动性、恢复、自进化如何并入软件工厂      | 维护者、协作者       |
| `traceability/requirements-matrix.md`                     | 追踪需求与设计、接口和验证关系                  | 维护者、QA           |

## 4. 文档维护原则

- 所有正式文档都采用单文件演进，不额外创建 `v2`、`final` 一类副本。
- 需求、设计和使用说明的稳定标识统一使用 `REQ-*`、`NFR-*`、`MOD-*`、`API-*`、`TASK-*` 等前缀。
- 影响项目行为的改动，至少同步更新代码/脚本、`docs/` 和相关说明入口。
- 不再依赖 `workflows/` 作为正式项目说明入口；相关内容如需长期保留，应并入 `docs/`。

## 5. 当前范围说明

这次文档建设先完成最小可用人类文档包，重点覆盖：

- 项目定位与范围
- 需求规划
- 系统设计
- 用户使用说明
- 高主动性与自进化集成说明
- 历史项目纳管资料
- 需求到设计的追踪关系

发布、运维、管理员、交接等文档仍可在后续阶段继续补齐。

## 6. 变更记录

| 日期       | 变更内容                                                               | 变更人 |
| ---------- | ---------------------------------------------------------------------- | ------ |
| 2026-03-25 | 初始化正式 `docs/` 文档体系并建立需求、设计、用户指南基线              | Codex  |
| 2026-03-25 | 将相关人类说明文档全部收敛到 `docs/`，不再把 `workflows/` 作为正式入口 | Codex  |
| 2026-03-26 | 补充历史项目纳管 checklist、提示词模板和自动化入口设计                 | Codex  |
| 2026-03-26 | 将历史项目纳管自动化入口更新为已实现 MVP，并同步索引与接口口径         | Codex  |
| 2026-03-27 | 将项目中文名统一为“山海工枢”，英文名统一为 `shanforge`，并同步路径引用 | Codex  |
