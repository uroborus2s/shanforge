# 命令速查

这篇文档是 `shanforge` 的命令参考手册。

目标不是让你死记所有命令，而是让你在需要下钻时，知道：

- 这个命令怎么调用
- 它解决什么问题
- 什么时候该用
- 运行后你应该期待看到什么

## 1. 先记住两条原则

### 原则 1：优先用高层入口，不要默认从底层命令开始

大多数场景优先级如下：

1. `factory-dispatch`
2. `factory-command-profiles`
3. `factory-workflow-runner`
4. 某个具体 `factory-*` 命令

### 原则 2：大多数命令都站在 shanforge 仓库根目录执行

最常见写法是：

```bash
python3 scripts/<command> --project /path/to/project --owner "<name>" --note "<note>"
```

特殊情况：

- `factory-init` 用 `--path`
- `factory-dispatch` 用动作名
- 少数命令还有 `--workflow`、`profile`、`--item`、`--type` 等额外参数

## 2. 最常用的三个总入口

| 命令 | 常见写法 | 作用 | 什么时候使用 | 预期 |
|---|---|---|---|---|
| `factory-dispatch` | `python3 scripts/factory-dispatch <action> ...` | 统一动作分派入口 | 你知道要做什么，但不想记具体脚本名 | 把动作转发给对应 `factory-*` 命令 |
| `factory-command-profiles` | `python3 scripts/factory-command-profiles <profile> --project <path>` | 运行高层命令画像 | 你想一键启动“需求 kickoff”“设计 kickoff”“发布前收尾”等标准组合动作 | 串行跑一组标准命令，并生成摘要 |
| `factory-workflow-runner` | `python3 scripts/factory-workflow-runner --project <path> --workflow <name>` | 运行高层工作流 | 你要做 `pre_gate`、`daily_close`、`release_ready`、`handover_ready` | 执行一组收尾/检查/发布相关动作 |

## 3. 项目初始化与结构修复

| 命令 | 常见写法 | 作用 | 什么时候使用 | 预期 |
|---|---|---|---|---|
| `factory-init` | `python3 scripts/factory-init --path <dir> --name <name> --idea "<idea>" --stack "<stack>"` | 初始化空目录新项目 | 目标目录为空，准备创建全新软件工厂项目 | 创建 `AGENTS.md`、`GEMINI.md`、`.factory/`、`docs/` |
| `factory-historical-project-onboarding` | `python3 scripts/factory-historical-project-onboarding --project <path> --owner <name> --goal "<goal>"` | 历史项目纳管 | 已有代码仓库，但还没纳入软件工厂 | 建立当前真实状态基线并补齐最小治理骨架 |
| `factory-project-rules-refresh` | `python3 scripts/factory-project-rules-refresh --project <path> --owner <name>` | 刷新规则入口文件 | 项目已有 `.factory/` / `docs/`，但 `AGENTS.md` / `GEMINI.md` 需要补齐或刷新 | 重新生成项目规则入口 |
| `factory-project-compress` | `python3 scripts/factory-project-compress --project <path> --owner <name>` | 生成更短的 AI 入口文档 | 项目文档过大，想压缩 AI 读取入口 | 刷新压缩入口和规则文件 |
| `factory-docs-profile-detect` | `python3 scripts/factory-docs-profile-detect --project <path>` | 检测文档画像 | 你不确定项目需要哪些顶层文档模块 | 输出或写回 `docs_profile` 判断结果 |
| `factory-docs-migrate-structure` | `python3 scripts/factory-docs-migrate-structure --project <path> --owner <name>` | 迁移旧版 docs 结构 | 项目 docs 仍是旧目录布局 | 调整 docs 目录到新结构 |
| `factory-docs-index-refresh` | `python3 scripts/factory-docs-index-refresh --project <path> --owner <name>` | 刷新 docs 索引 | 新增、删除、移动页面后 | 更新 `docs/index.md` 和相关概览页 |

## 4. 需求、设计与计划

| 命令 | 常见写法 | 作用 | 什么时候使用 | 预期 |
|---|---|---|---|---|
| `factory-prd-bootstrap` | `python3 scripts/factory-prd-bootstrap --project <path> --owner <name>` | 初始化需求阶段文档 | 新项目或需求阶段刚开始 | 生成 PRD、需求分析等骨架 |
| `factory-requirements-upgrade` | `python3 scripts/factory-requirements-upgrade --project <path> --owner <name>` | 升级旧需求文档结构 | 历史项目的需求文档太旧，不符合当前字段结构 | 把旧需求文档迁到新版结构 |
| `factory-requirements-verify` | `python3 scripts/factory-requirements-verify --project <path> --owner <name>` | 做需求一致性校验 | 需求阶段收口、准备进入设计前 | 输出需求覆盖率和缺口结果 |
| `factory-design-bootstrap` | `python3 scripts/factory-design-bootstrap --project <path> --owner <name>` | 初始化设计阶段文档 | 需求已确认，准备进入设计 | 生成技术选型、架构、模块边界、API、后端、数据库、UX/UI 文档骨架 |
| `factory-tech-profile` | `python3 scripts/factory-tech-profile --project <path> --owner <name>` | 登记技术画像 | 想把技术选型、必装模块、规则纳入正式工作流 | 写入技术画像并影响后续执行规则 |
| `factory-design-assets` | `python3 scripts/factory-design-assets --project <path> --owner <name>` | 登记可视化设计交付物 | UI 图、原型、流程图需要正式入档 | 更新 UX/UI 文档和设计资产记录 |
| `factory-iteration-plan` | `python3 scripts/factory-iteration-plan --project <path> --iteration "<name>" --owner <name>` | 初始化迭代计划 | 设计已确认，准备拆分实施任务 | 生成实施计划、WBS、任务分解，可选创建 `TASK-*` |
| `factory-next-stage` | `python3 scripts/factory-next-stage --project <path> --owner <name>` | 推进项目阶段 | 当前阶段确认完成，要正式进入下一阶段 | 更新当前阶段和执行记录 |
| `factory-update-singlefile-doc` | `python3 scripts/factory-update-singlefile-doc --project <path> --doc <path>` | 按单文件演化规则更新正式文档 | 你要针对单个正式文档做持续演进 | 原地更新文档而不是生成 v2 副本 |

## 5. 工作项、变更与追踪

| 命令 | 常见写法 | 作用 | 什么时候使用 | 预期 |
|---|---|---|---|---|
| `factory-new-workitem` | `python3 scripts/factory-new-workitem --project <path> --type task|bug|change --title "<title>" --owner <name>` | 创建工作项 | 需要创建 `TASK-*`、`BUG-*`、`CR-*` | 生成对应工作项文件 |
| `factory-change-impact` | `python3 scripts/factory-change-impact --project <path> --item <id>` | 记录影响分析 | `BUG` 或 `CR` 进入正式处理前 | 影响分析写回变更文档和记忆 |
| `factory-risk-register` | `python3 scripts/factory-risk-register --project <path> --owner <name>` | 维护风险台账 | 项目出现交付风险、技术风险、范围风险 | 更新风险登记和摘要 |
| `factory-trace-link` | `python3 scripts/factory-trace-link --project <path> --source <id> --targets <ids>` | 维护追踪关系 | 需要把需求、设计、任务、测试串起来 | 更新追踪矩阵和 AI 图谱 |
| `factory-workblock-refine` | `python3 scripts/factory-workblock-refine --project <path> --item <id>` | 修复工作块拆解质量 | 任务太大、工作块太粗 | 重新细化工作块 |
| `factory-run-task` | `python3 scripts/factory-run-task --project <path> --item <id> --work-block <wb>` | 推进工作块状态 | 正在执行某个任务、缺陷或变更 | 更新工作项执行状态 |
| `factory-sync-change` | `python3 scripts/factory-sync-change --project <path> --item <id>` | 同步变更结果 | 变更完成后需要把日志、测试、记忆同步起来 | 更新日志、测试报告和 AI 记忆 |
| `factory-auto-sync` | `python3 scripts/factory-auto-sync --project <path> --item <id>` | 自动做同步和收尾 | 你想减少手工同步动作 | 自动完成同步、关单、日报、快照等 |
| `factory-close-workitem` | `python3 scripts/factory-close-workitem --project <path> --item <id>` | 关闭工作项 | 工作项已经完成并收尾 | 关闭工作项并写回收尾记录 |

## 6. PR、评审与远端协作

| 命令 | 常见写法 | 作用 | 什么时候使用 | 预期 |
|---|---|---|---|---|
| `factory-pr-start` | `python3 scripts/factory-pr-start --project <path> --item <id> --owner <name>` | 创建或登记 PR | 代码类工作项准备进入 PR 流 | PR 记录建立，可选创建本地分支 |
| `factory-pr-review` | `python3 scripts/factory-pr-review --project <path> --pr <id> --owner <name>` | 记录 PR 评审结果 | PR 已经有人评审 | 评审结果同步到 PR 记录和工作项 |
| `factory-pr-check` | `python3 scripts/factory-pr-check --project <path> --pr <id>` | 做 PR 预检查 | 想判断 PR 是否准备好进入评审、合并或 Gate | 输出 PR 当前健康度与缺口 |
| `factory-pr-board` | `python3 scripts/factory-pr-board --project <path>` | 生成 PR 看板 | 想快速看当前 PR 局面 | 生成 PR 协作看板 |
| `factory-pr-handover` | `python3 scripts/factory-pr-handover --project <path> --prs <ids>` | 生成 PR 交接包 | 某个 PR 要交给别人或别的 Agent | 生成 PR 交接材料 |
| `factory-pr-merge` | `python3 scripts/factory-pr-merge --project <path> --pr <id>` | 本地合并 PR | 本地 PR 流完成，准备合并 | 合并 PR，并可选关单 |
| `factory-pr-remote-open` | `python3 scripts/factory-pr-remote-open --project <path> --pr <id>` | 创建远端 PR | 本地已有 PR 记录，要推到远端仓库 | 记录远端 PR 编号和地址 |
| `factory-pr-remote-sync` | `python3 scripts/factory-pr-remote-sync --project <path> --pr <id>` | 同步远端 PR 状态 | 想把 GitHub/GitLab 状态同步回本地记录 | 更新远端状态、检查结果、链接 |
| `factory-pr-remote-merge` | `python3 scripts/factory-pr-remote-merge --project <path> --pr <id>` | 远端合并 PR | 通过 GitHub/GitLab 完成合并 | 远端 PR 合并并可选关单 |
| `factory-review-gate` | `python3 scripts/factory-review-gate --project <path> --owner <name>` | 记录 Gate 评审结果 | 阶段收口、要确认是否放行 | Gate 结论写入记录，可选推进阶段 |
| `factory-stage-check` | `python3 scripts/factory-stage-check --project <path> --owner <name>` | 做阶段检查 | 想判断当前阶段必需文档和状态是否齐全 | 生成阶段检查报告 |
| `factory-quality-check` | `python3 scripts/factory-quality-check --project <path> --owner <name>` | 做质量检查 | 发布前或阶段收口前 | 生成质量检查报告和 AI 摘要 |

## 7. 会话入口、诊断与项目状态

| 命令 | 常见写法 | 作用 | 什么时候使用 | 预期 |
|---|---|---|---|---|
| `factory-agent-session` | `python3 scripts/factory-agent-session --project <path> --owner <name> --focus "<focus>"` | 生成会话入口 | 重新进入项目上下文、开始新一轮会话前 | 生成当前会话应该先读什么、先做什么 |
| `factory-chat-bootstrap` | `python3 scripts/factory-chat-bootstrap --project <path> --tool codex|gemini --role <role>` | 生成角色化对话入口 | 想让不同角色或不同工具快速接手 | 生成角色化启动入口文档 |
| `factory-state-doctor` | `python3 scripts/factory-state-doctor --project <path> --owner <name>` | 诊断项目状态 | 不确定当前缺什么、卡在哪里、规则是否健康 | 输出诊断结果与建议动作 |
| `factory-refresh-memory` | `python3 scripts/factory-refresh-memory --project <path>` | 刷新 AI 记忆 | 做完一轮变更后，想同步记忆层 | 更新 `.factory/memory/` 摘要与快照 |
| `factory-daily-status` | `python3 scripts/factory-daily-status --project <path> --owner <name> --focus "<focus>"` | 生成每日报告 | 日终收尾或阶段汇报 | 更新日报并同步文档与 `.factory` |
| `factory-project-snapshot` | `python3 scripts/factory-project-snapshot --project <path> --owner <name>` | 生成项目快照 | 想冻结当前阶段状态，便于回溯或交接 | 生成项目内部快照 |
| `factory-release-pack` | `python3 scripts/factory-release-pack --project <path> --owner <name>` | 生成发布包 | 发布前准备交付材料 | 生成发布交付包 |
| `factory-handover-pack` | `python3 scripts/factory-handover-pack --project <path> --owner <name>` | 生成交接包 | 换人、换 Agent、准备交接 | 生成交接材料 |
| `factory-retrospective` | `python3 scripts/factory-retrospective --project <path> --owner <name>` | 生成项目复盘 | 一轮迭代或阶段完成后 | 生成复盘文档和 AI 摘要 |

## 8. 角色与团队协作

| 命令 | 常见写法 | 作用 | 什么时候使用 | 预期 |
|---|---|---|---|---|
| `factory-role-assign` | `python3 scripts/factory-role-assign --project <path> --role <role> --owner <name>` | 分派角色责任 | 需要明确某个角色当前负责什么 | 记录角色、工具和工作项分配 |
| `factory-role-workbench` | `python3 scripts/factory-role-workbench --project <path> --role <role>` | 生成角色工作台 | 某个角色需要集中看自己的上下文和动作 | 生成角色执行工作台 |
| `factory-role-sync` | `python3 scripts/factory-role-sync --project <path> --role <role>` | 同步角色状态 | 某个角色完成一轮动作后 | 刷新角色视图和状态 |
| `factory-role-review` | `python3 scripts/factory-role-review --project <path> --role <role>` | 复核角色状态 | 想看某个角色当前执行得对不对 | 输出角色复核结果 |
| `factory-role-handoff` | `python3 scripts/factory-role-handoff --project <path> --from <role> --to <role>` | 记录角色交接 | 一个角色把工作交给另一个角色 | 生成角色交接记录 |
| `factory-role-closeout` | `python3 scripts/factory-role-closeout --project <path> --role <role>` | 执行角色收尾 | 某个角色一轮工作结束 | 完成角色收尾与状态更新 |
| `factory-role-retro` | `python3 scripts/factory-role-retro --project <path> --role <role>` | 生成角色复盘 | 想复盘某个角色执行质量 | 生成角色复盘文档 |
| `factory-multi-agent-board` | `python3 scripts/factory-multi-agent-board --project <path>` | 生成多 Agent 看板 | 多角色或多 Agent 并行协作时 | 生成协作看板 |
| `factory-team-sync` | `python3 scripts/factory-team-sync --project <path> --owner <name>` | 团队级同步 | 需要批量刷新多个角色状态 | 输出团队同步记录 |
| `factory-team-closeout` | `python3 scripts/factory-team-closeout --project <path> --owner <name>` | 团队级收尾 | 一轮团队工作结束 | 输出团队收尾记录 |
| `factory-team-retro` | `python3 scripts/factory-team-retro --project <path> --owner <name>` | 团队级复盘 | 一轮协作或阶段结束后 | 输出团队级复盘 |

## 9. 恢复、质量漂移与自进化

| 命令 | 常见写法 | 作用 | 什么时候使用 | 预期 |
|---|---|---|---|---|
| `factory-agent-motivation` | `python3 scripts/factory-agent-motivation --project <path> --owner <name>` | 刷新团队动能和自治规则 | 团队节奏变弱、多 Agent 协作前校准 | 生成动能、强化和自治文档 |
| `factory-recovery-coach` | `python3 scripts/factory-recovery-coach --project <path> --item <id>` | 给出恢复教练方案 | 工作项受阻、空转、质量漂移时 | 生成恢复方案和建议动作 |
| `factory-pattern-fix` | `python3 scripts/factory-pattern-fix --project <path> --item <id>` | 把单点问题扩展为模式级修复 | 你怀疑类似问题不止一个地方 | 生成模式级扫描与修复报告 |
| `factory-evolution-baseline` | `python3 scripts/factory-evolution-baseline --project <path> --owner <name>` | 沉淀有效做法到基线 | 一轮实践后形成稳定方法 | 刷新项目自进化基线 |

## 10. 高层画像与工作流

### `factory-command-profiles`

常见 profile：

| Profile | 作用 | 什么时候使用 | 预期 |
|---|---|---|---|
| `requirements-kickoff` | 初始化需求阶段并生成会话入口 | 新项目刚进入需求阶段 | 需求骨架、校验和会话入口一起生成 |
| `design-kickoff` | 初始化设计阶段并登记技术画像 | 需求已确认，准备进设计 | 设计骨架、技术画像和会话入口一起生成 |
| `iteration-kickoff` | 初始化迭代计划并可选创建任务 | 设计完成，准备进实施计划 | 计划、任务和会话入口一起生成 |
| `pre-gate` | 执行 Gate 前检查组合 | 阶段收口前 | 阶段检查、质量检查和诊断结果 |
| `daily-close` | 执行日终收尾组合 | 每天收尾时 | 日报、记忆刷新、快照 |
| `release-ready` | 执行发布前组合动作 | 发布准备阶段 | 检查、发布包、交接包、快照 |
| `handover-ready` | 执行交接前组合动作 | 换人或换 Agent 前 | 交接材料、诊断、快照 |

### `factory-workflow-runner`

常见 workflow：

| Workflow | 作用 | 什么时候使用 | 预期 |
|---|---|---|---|
| `pre_gate` | 执行阶段检查和质量检查 | Gate 前 | 输出是否通过、关注还是未通过 |
| `daily_close` | 刷新记忆、生成日报、生成快照 | 日终收尾 | 完成当日收尾产物 |
| `release_ready` | 跑发布前检查、日报、发布包、交接包、快照 | 发布前 | 形成完整发布准备包 |
| `handover_ready` | 生成日报、交接包、快照 | 交接前 | 形成接手材料 |

## 11. 按目标反推该用哪个命令

| 你的目标 | 优先命令 |
|---|---|
| 不想记底层命令 | `factory-dispatch` |
| 想一键启动某个标准阶段 | `factory-command-profiles` |
| 想一键跑一组收尾工作流 | `factory-workflow-runner` |
| 不知道当前缺什么 | `factory-agent-session` + `factory-state-doctor` |
| 新建空目录项目 | `factory-init` |
| 接手老项目 | `factory-historical-project-onboarding` |
| 补齐规则入口 | `factory-project-rules-refresh` |
| 继续需求 | `factory-prd-bootstrap` + `factory-requirements-verify` |
| 继续设计 | `factory-design-bootstrap` + `factory-tech-profile` |
| 拆任务 | `factory-iteration-plan` + `factory-workblock-refine` |
| 跑单个工作项 | `factory-run-task` |
| 管理 PR | `factory-pr-start` / `factory-pr-review` / `factory-pr-merge` |
| 发布前检查 | `factory-stage-check` + `factory-quality-check` |
| 做恢复 | `factory-recovery-coach` |

## 12. 使用命令时最常见的错误

- 不传项目路径
- 在历史项目上直接跑 `factory-init`
- 只跑实现命令，不同步文档和记忆
- 明明只是不确定下一步，却跳过 `factory-state-doctor`
- 想做高层动作，却直接从底层命令开始拼

如果你已经知道场景，但不知道该怎么写自然语言，让 AI 自己选这些命令，回看 [提示词速查](./prompt-templates.md)。
