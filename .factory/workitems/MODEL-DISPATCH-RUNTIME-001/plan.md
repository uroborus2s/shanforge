# Sol / Terra / Luna 真实调度实施计划

**目标：** 用 Codex 原生项目配置、子代理工具和 Shanforge 授权任务包实现可审计、失败关闭的 Sol/Terra/Luna 自动派发。

**架构：** Sol 主会话保留需求、设计、复杂度/风险裁决、派发和质量门；Codex 原生 subagent 是唯一执行机制。项目不新增中心运行时，模型绑定由 `.codex` 配置和父会话显式 spawn 参数完成，派发事实由 WorkItem ledger/evidence 记录。

**技术栈：** Codex `.codex/config.toml`、custom agent TOML、Markdown Skill、pytest、Ruff、Git。

**工作项：** `MODEL-DISPATCH-RUNTIME-001`

**状态：** `completed`

## 输入与裁决

- 用户明确要求创建本 WorkItem、真实自动调度并做到干净克隆全绿。
- 任务涉及稳定入口、跨 Skill 执行合同、项目配置、正式设计、测试和真实多模型协作，共四个可验收交付物。
- Sol 裁决整体复杂度为 `complex`、风险为 `medium`；实现默认由 Terra 执行，机械且低风险的 Codex 配置切片由 Luna 执行。
- 当前 Gate 为 `closed`，身份、精确写集和验证命令完整，授权执行。

## 文件与职责

| 类型 | 路径 | 职责 |
|---|---|---|
| 新建 | `.codex/config.toml`、`.codex/agents/*.toml` | Codex 原生控制模型、并发和执行者配置 |
| 修改 | `AGENTS.md` | 稳定自动派发入口，不写临时状态 |
| 修改 | `skills/using-shanforge/SKILL.md` | Sol 分级、派发判定和失败关闭 |
| 修改 | `skills/subagent-driven-development/SKILL.md` | 执行模型绑定、回执和升级语义 |
| 修改 | `skills/subagent-driven-development/references/status-handling-checklist.md` | 删除绕过确定性路由的换模型或 Sol 代写分支 |
| 修改 | `skills/using-shanforge/references/codex-tools.md` | Codex spawn 参数与父回执协议 |
| 修改 | `skills/writing-plans/references/task-brief-template.md` | 持久化真实派发字段 |
| 修改 | `docs/05-design/workflow-execution-design.md` | 正式架构与运行时合同 |
| 修改 | `docs/02-user-guide/user-guide.md` | 人类可执行使用说明 |
| 测试 | `tests/test_model_tier_routing.py` | 配置、映射、派发、失败关闭与证据守卫 |
| 状态 | `.factory/workitems/MODEL-DISPATCH-RUNTIME-001/**` | 计划、任务包、真实回执、报告、评审和验证 |
| 记忆 | `.factory/memory/agent-session.md`、`.factory/memory/current-state.md`、`.factory/memory/tasks.summary.md`、`.factory/memory/tests.summary.md` | 仅在批次收口同步压缩事实 |

## 任务

### T01：Codex 原生模型配置

- 路由：`simple + low -> gpt-5.6-luna`，`model_reasoning_effort: low`，`fork_turns: none`。
- 创建 Sol 主模型、三线程上限、Luna/Terra 执行者和 Terra 只读评审者 TOML。
- 用 Python 标准库 `tomllib` 解析全部配置，拒绝缺字段、错误模型或可写 reviewer。
- 写集仅限 `.codex/config.toml` 与 `.codex/agents/*.toml`。

### T02：真实派发合同与人类文档

- 路由：`standard + medium -> gpt-5.6-terra`，`model_reasoning_effort: medium`，`fork_turns: none`。
- 固化 `dispatch_required`、`dispatch_mode`、显式模型/推理强度、完整任务包、父回执和失败关闭。
- 同步稳定入口、正式设计和用户指南；保持 Skill-first，不新增中心运行时。
- 写集限于本计划登记的入口、Skill、两份 reference、模板和两份正式文档。

### T03：治理回归测试

- 依赖 T01、T02；路由：`standard + medium -> gpt-5.6-terra`，`model_reasoning_effort: medium`，`fork_turns: none`。
- 先新增/运行会在旧实现上失败的新断言，再验证配置、模型映射、派发字段、父回执和失败关闭全部通过。
- 写集仅限 `tests/test_model_tier_routing.py`。

### T04：集中质量、独立评审、提交与干净克隆

- Sol 汇总实际 dispatch receipt 和候选；未参与实现的 Terra reviewer 以 `high`、只读方式评审。
- 首个候选运行完整 pytest、Ruff、全部 Skill validator、TOML/JSON/JSONL 和 Git diff 卫生检查。
- Critical/Important finding 回派原模型整改并复测；最终候选由 `gitcommitzh` 精确提交。
- 从提交创建干净克隆运行同一质量门；随后回写 WorkItem、测试报告和压缩 memory，形成收口提交并再次验证干净克隆。

## 测试策略

- Red：新治理断言在旧合同或缺少 `.codex` 配置时失败。
- Green：`uv run pytest tests/test_model_tier_routing.py -q` 通过。
- 定向回归：相关路由、计划和子代理 Skill 测试通过。
- 批次验证：完整 `uv run pytest`、`uv run ruff check .`、Skill validator、TOML/JSON/JSONL 和 Git 卫生检查。
- 未运行项：无 UI、API、服务或 E2E；本 WorkItem 只修改 Codex/Skill 协作合同，不存在这些运行面。

## 集中质量门

- 计划自审：通过；规格覆盖、路径、依赖、模型和验证命令完整，无占位实现。
- 独立评审：`pending`
- 批次验证：`pending`
- 本地提交：用户以“做到干净克隆全绿”授权精确本地提交。
- 远端动作：`not_authorized`
