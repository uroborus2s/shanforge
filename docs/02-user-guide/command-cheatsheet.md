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

### 原则 2：大多数命令都站在 shanforge 仓库根目录执行，并通过 `uv` 运行

最常见写法是：

```bash
uv run python scripts/<command> --project /path/to/project --owner "<name>" --note "<note>"
```

特殊情况：

- `factory-init` 用 `--path`
- `factory-dispatch` 用动作名
- 少数命令还有 `--workflow`、`profile`、`--item`、`--type` 等额外参数

补充说明：

- 当前仓库正式 Python 基线是 `3.14+`
- 正式脚本入口以 `uv run python scripts/...` 为准
- `docs/` 的内容维护改走 `document-templates` skill
- 文档合规校验、聚合站点接入、同步、构建和预览统一走 `docs-stratego` CLI

## 2. 最常用的三个总入口

| 命令 | 常见写法 | 作用 | 什么时候使用 | 预期 |
|---|---|---|---|---|
| `factory-dispatch` | `uv run python scripts/factory-dispatch <action> ...` | 统一动作分派入口 | 你知道要做什么，但不想记具体脚本名 | 把动作转发给对应 `factory-*` 命令 |
| `factory-command-profiles` | `uv run python scripts/factory-command-profiles <profile> --project <path>` | 运行高层命令画像 | 你想一键启动“需求 kickoff”“设计 kickoff”“发布前收尾”等标准组合动作 | 串行跑一组标准命令，并生成摘要 |
| `factory-workflow-runner` | `uv run python scripts/factory-workflow-runner --project <path> --workflow <name>` | 运行高层工作流 | 你要做 `pre_gate`、`daily_close`、`release_ready`、`handover_ready` | 执行一组收尾/检查/发布相关动作 |
| `factory-frontend-capabilities` | `uv run python scripts/factory-frontend-capabilities --tool codex|gemini|opencode` | 查看前台能力画像 | 你想确认某个前台是否支持子代理、MCP、审批 hook 或降级策略 | 输出前台能力、规则入口和降级说明 |
| `factory-intent-resolver` | `uv run python scripts/factory-intent-resolver <自然语言目标> --project <path> --tool codex|gemini|opencode [--execute-safe|--request-approval]` | 解析自然语言目标 | 你只知道目标，不知道该选哪个高层动作，或者你只知道要推进某个候选 skill 的下一步 | 返回主推荐动作、候选动作、风险和建议命令；同时输出 `approval_guidance` 与固定 `reply_summary`；已支持 skill 生命周期路由；加 `--execute-safe` 时自动执行 `L0/L1` 主推荐动作；加 `--request-approval` 时为 `L2/L3` 生成审批票据 |
| `factory-intent-approval` | `uv run python scripts/factory-intent-approval [<ticket>] [--list|--approve|--reject]` | 查看或处理意图审批票据 | 你已经拿到 `L2/L3` 动作的审批票据，需要显式批准或拒绝 | 列出票据，或在批准后先校验冻结 ownership 与写集冲突，再执行冻结计划并写回票据状态；同时输出固定 `reply_summary` |
| `factory-intent-eval` | `uv run python scripts/factory-intent-eval [--strict]` | 回放评估意图解析能力 | 你想知道自然语言到动作的命中率是否退化 | 输出命中率、失败样本和下一步建议，并写出评估报告；同时输出固定 `reply_summary` |
| `factory-skill-draft` | `uv run python scripts/factory-skill-draft <name> --summary "<summary>" [--triggers "..."] [--target-skill <skill>]` | 生成候选 skill 草案 | 你想把某个反复出现的优化想法先固化成候选 skill，而不是直接改正式 `SKILL.md` | 在 `skills-drafts/` 下生成候选 `SKILL.md`、`proposal.json`、`evals/evals.json`、`evals/eval-report.json` 和 `change-summary.md`，并输出固定 `reply_summary` |
| `factory-skill-eval` | `uv run python scripts/factory-skill-eval <candidate> [--strict]` | 执行候选 skill 正式评估 | 你已经补完候选草案，想正式生成 `passed/failed` 评估结果，而不是手工改 `eval-report.json` | 检查 skill 结构、`evals/evals.json`、输入文件和 `change-summary.md`，并回写正式评估报告与控制面记录 |
| `factory-skill-approval` | `uv run python scripts/factory-skill-approval <candidate|ticket> [--request|--approve|--reject|--list]` | 查看或处理候选 skill 审批票据 | 你已经有候选 skill 草案，并且已经跑出 `passed` 的正式评估，准备把它接进专用审批链路 | 为已通过评估的候选草案创建票据，或批准/拒绝票据，并把结果写回 `skills-drafts/<skill>/approval.json` 与 `proposal.json` |
| `factory-skill-delete-approval` | `uv run python scripts/factory-skill-delete-approval <candidate|ticket> [--request|--approve|--reject|--list]` | 查看或处理首次发布新 skill 的删除回退审批票据 | 你已经把一个新 skill 晋升到正式库，但它没有旧版本备份，现在需要受控删除回退 | 为首次发布的新 skill 创建删除回退票据，或批准/拒绝票据，并把结果写回 `skills-drafts/<skill>/delete-approval.json` 与 `proposal.json` |
| `factory-skill-promote` | `uv run python scripts/factory-skill-promote <candidate> [--check]` | 将候选 skill 晋升到正式 `skills/` | 你已经完成候选草案、评估和审批，准备发布正式 skill | 检查晋升门禁，或把候选 `SKILL.md` 写入正式 `skills/` 并生成晋升记录、候选回写和旧版本备份 |
| `factory-skill-rollback` | `uv run python scripts/factory-skill-rollback <candidate> [--check]` | 将已晋升 skill 回退到旧版本或执行批准后的删除回退 | 你已经晋升了一个覆盖旧 skill 的候选，或者你要删除首次发布的新 skill | 检查是否存在 promotion 备份；有备份时恢复正式 `SKILL.md`，无备份但已批准删除时删除正式文件，并生成回退记录与当前版本备份 |

补充说明：

- 执行 `uv run python scripts/factory-dispatch --list-actions` 可以查看当前已登记动作、别名、风险级别和默认策略。

## 3. 项目初始化与结构修复

| 命令 | 常见写法 | 作用 | 什么时候使用 | 预期 |
|---|---|---|---|---|
| `factory-init` | `uv run python scripts/factory-init --path <dir> --name <name> --idea "<idea>" --stack "<stack>"` | 初始化空目录新项目 | 目标目录为空，准备创建全新软件工厂项目 | 创建 `AGENTS.md`、`GEMINI.md`、`.factory/`、`docs/` |
| `factory-historical-project-onboarding` | `uv run python scripts/factory-historical-project-onboarding --project <path> --owner <name> --goal "<goal>"` | 历史项目纳管 | 已有代码仓库，但还没纳入软件工厂 | 建立当前真实状态基线并补齐最小治理骨架 |
| `factory-project-rules-refresh` | `uv run python scripts/factory-project-rules-refresh --project <path> --owner <name>` | 刷新规则入口文件 | 项目已有 `.factory/` / `docs/`，但 `AGENTS.md` / `GEMINI.md` 需要补齐或刷新 | 重新生成项目规则入口 |
| `factory-project-compress` | `uv run python scripts/factory-project-compress --project <path> --owner <name>` | 生成更短的 AI 入口文档 | 项目文档过大，想压缩 AI 读取入口 | 刷新压缩入口和规则文件 |
| `docs-stratego source validate` | `uvx --from docs-stratego docs-stratego source validate --repo-path <path>` | 校验源仓 docs 合规性 | 你已经用 `document-templates` skill 改完文档，想确认目录、导航、权限和契约页是否符合标准 | 输出源仓文档状态与缺口 |
| `docs-stratego source scaffold-notify` | `uvx --from docs-stratego docs-stratego source scaffold-notify --repo-path <path>` | 生成源仓通知 workflow | 你希望源仓在 `docs/**` 更新后自动通知聚合站点同步 | 生成或删除通知 workflow |
| `docs-stratego source add/remove` | `uvx --from docs-stratego docs-stratego source add/remove ...` | 管理聚合站点源仓登记 | 你要把一个项目接入或移出 `docs-stratego` 聚合站点 | 更新聚合仓配置，并按需登记/移除 source |
| `docs-stratego sync/build/dev` | `uvx --from docs-stratego docs-stratego sync/build/dev ...` | 同步、构建或预览聚合站点 | 你要在聚合站点工作区里做聚合同步、构建或本地预览 | 生成聚合站点输入，或本地预览 |

## 4. 需求、设计与计划

| 命令 | 常见写法 | 作用 | 什么时候使用 | 预期 |
|---|---|---|---|---|
| `factory-prd-bootstrap` | `uv run python scripts/factory-prd-bootstrap --project <path> --owner <name>` | 初始化需求阶段文档 | 新项目或需求阶段刚开始 | 生成 PRD、需求分析等骨架 |
| `factory-requirements-upgrade` | `uv run python scripts/factory-requirements-upgrade --project <path> --owner <name>` | 升级旧需求文档结构 | 历史项目的需求文档太旧，不符合当前字段结构 | 把旧需求文档迁到新版结构 |
| `factory-requirements-verify` | `uv run python scripts/factory-requirements-verify --project <path> --owner <name>` | 做需求一致性校验 | 需求阶段收口、准备进入设计前 | 输出需求覆盖率和缺口结果 |
| `factory-design-bootstrap` | `uv run python scripts/factory-design-bootstrap --project <path> --owner <name>` | 初始化设计阶段文档 | 需求已确认，准备进入设计 | 生成技术选型、架构、模块边界、API、后端、数据库、UX/UI 文档骨架 |
| `factory-tech-profile` | `uv run python scripts/factory-tech-profile --project <path> --owner <name>` | 登记技术画像 | 想把技术选型、必装模块、规则纳入正式工作流 | 写入技术画像并影响后续执行规则 |
| `factory-design-assets` | `uv run python scripts/factory-design-assets --project <path> --owner <name>` | 登记可视化设计交付物 | UI 图、原型、流程图需要正式入档 | 更新 UX/UI 文档和设计资产记录 |
| `factory-iteration-plan` | `uv run python scripts/factory-iteration-plan --project <path> --iteration "<name>" --owner <name>` | 初始化迭代计划 | 设计已确认，准备拆分实施任务 | 生成实施计划、WBS、任务分解，可选创建 `TASK-*` |
| `factory-next-stage` | `uv run python scripts/factory-next-stage --project <path> --owner <name>` | 推进项目阶段 | 当前阶段确认完成，要正式进入下一阶段 | 更新当前阶段和执行记录 |
| `factory-update-singlefile-doc` | `uv run python scripts/factory-update-singlefile-doc --project <path> --doc <path>` | 按单文件演化规则更新正式文档 | 你要针对单个正式文档做持续演进 | 原地更新文档而不是生成 v2 副本 |

## 5. 工作项、变更与追踪

| 命令 | 常见写法 | 作用 | 什么时候使用 | 预期 |
|---|---|---|---|---|
| `factory-new-workitem` | `uv run python scripts/factory-new-workitem --project <path> --type task|bug|change --title "<title>" --owner <name>` | 创建工作项 | 需要创建 `TASK-*`、`BUG-*`、`CR-*` | 生成对应工作项文件 |
| `factory-change-impact` | `uv run python scripts/factory-change-impact --project <path> --item <id>` | 记录影响分析 | `BUG` 或 `CR` 进入正式处理前 | 影响分析写回变更文档和记忆 |
| `factory-risk-register` | `uv run python scripts/factory-risk-register --project <path> --owner <name>` | 维护风险台账 | 项目出现交付风险、技术风险、范围风险 | 更新风险登记和摘要 |
| `factory-trace-link` | `uv run python scripts/factory-trace-link --project <path> --source <id> --targets <ids>` | 维护追踪关系 | 需要把需求、设计、任务、测试串起来 | 更新追踪矩阵和 AI 图谱 |
| `factory-workblock-refine` | `uv run python scripts/factory-workblock-refine --project <path> --item <id>` | 修复工作块拆解质量 | 任务太大、工作块太粗 | 重新细化工作块 |
| `factory-run-task` | `uv run python scripts/factory-run-task --project <path> --item <id> --work-block <wb>` | 推进工作块状态 | 正在执行某个任务、缺陷或变更 | 更新工作项执行状态 |
| `factory-sync-change` | `uv run python scripts/factory-sync-change --project <path> --item <id>` | 同步变更结果 | 变更完成后需要把日志、测试、记忆同步起来 | 更新日志、测试报告和 AI 记忆 |
| `factory-auto-sync` | `uv run python scripts/factory-auto-sync --project <path> --item <id>` | 自动做同步和收尾 | 你想减少手工同步动作 | 自动完成同步、关单、日报、快照等 |
| `factory-close-workitem` | `uv run python scripts/factory-close-workitem --project <path> --item <id>` | 关闭工作项 | 工作项已经完成并收尾 | 关闭工作项并写回收尾记录 |

## 6. PR、评审与远端协作

| 命令 | 常见写法 | 作用 | 什么时候使用 | 预期 |
|---|---|---|---|---|
| `factory-pr-start` | `uv run python scripts/factory-pr-start --project <path> --item <id> --owner <name>` | 创建或登记 PR | 代码类工作项准备进入 PR 流 | PR 记录建立，可选创建本地分支 |
| `factory-pr-review` | `uv run python scripts/factory-pr-review --project <path> --pr <id> --owner <name>` | 记录 PR 评审结果 | PR 已经有人评审 | 评审结果同步到 PR 记录和工作项 |
| `factory-pr-check` | `uv run python scripts/factory-pr-check --project <path> --pr <id>` | 做 PR 预检查 | 想判断 PR 是否准备好进入评审、合并或 Gate | 输出 PR 当前健康度与缺口 |
| `factory-pr-board` | `uv run python scripts/factory-pr-board --project <path>` | 生成 PR 看板 | 想快速看当前 PR 局面 | 生成 PR 协作看板 |
| `factory-pr-handover` | `uv run python scripts/factory-pr-handover --project <path> --prs <ids>` | 生成 PR 交接包 | 某个 PR 要交给别人或别的 Agent | 生成 PR 交接材料 |
| `factory-pr-merge` | `uv run python scripts/factory-pr-merge --project <path> --pr <id>` | 本地合并 PR | 本地 PR 流完成，准备合并 | 合并 PR，并可选关单 |
| `factory-pr-remote-open` | `uv run python scripts/factory-pr-remote-open --project <path> --pr <id>` | 创建远端 PR | 本地已有 PR 记录，要推到远端仓库 | 记录远端 PR 编号和地址 |
| `factory-pr-remote-sync` | `uv run python scripts/factory-pr-remote-sync --project <path> --pr <id>` | 同步远端 PR 状态 | 想把 GitHub/GitLab 状态同步回本地记录 | 更新远端状态、检查结果、链接 |
| `factory-pr-remote-merge` | `uv run python scripts/factory-pr-remote-merge --project <path> --pr <id>` | 远端合并 PR | 通过 GitHub/GitLab 完成合并 | 远端 PR 合并并可选关单 |
| `factory-review-gate` | `uv run python scripts/factory-review-gate --project <path> --owner <name>` | 记录 Gate 评审结果 | 阶段收口、要确认是否放行 | Gate 结论写入记录，可选推进阶段 |
| `factory-stage-check` | `uv run python scripts/factory-stage-check --project <path> --owner <name>` | 做阶段检查 | 想判断当前阶段必需文档和状态是否齐全 | 生成阶段检查报告 |
| `factory-quality-check` | `uv run python scripts/factory-quality-check --project <path> --owner <name>` | 做质量检查 | 发布前或阶段收口前 | 生成质量检查报告和 AI 摘要 |

## 7. 会话入口、诊断与项目状态

| 命令 | 常见写法 | 作用 | 什么时候使用 | 预期 |
|---|---|---|---|---|
| `factory-agent-session` | `uv run python scripts/factory-agent-session --project <path> --owner <name> --focus "<focus>"` | 生成会话入口 | 重新进入项目上下文、开始新一轮会话前 | 生成当前会话应该先读什么、先做什么 |
| `factory-chat-bootstrap` | `uv run python scripts/factory-chat-bootstrap --project <path> --tool codex|gemini|opencode --role <role>` | 生成角色化对话入口 | 想让不同角色或不同工具快速接手 | 生成角色化启动入口文档 |
| `factory-intent-resolver` | `uv run python scripts/factory-intent-resolver 继续下一步 --project <path> --tool codex|gemini|opencode [--execute-safe|--request-approval]` | 解析自然语言到高层动作 | 只知道目标，不确定该用 `doctor`、`docs-upgrade` 还是 `onboarding` | 输出主推荐动作、候选动作和风险策略；如主推荐动作为 `L0/L1`，可用 `--execute-safe` 直接执行；如为 `L2/L3`，可用 `--request-approval` 生成票据 |
| `factory-intent-approval` | `uv run python scripts/factory-intent-approval <ticket> --approve --owner <name>` | 查看或处理审批票据 | `intent-resolver` 已经为高风险动作生成票据 | 批准后先校验冻结 ownership，再执行计划；拒绝后把状态写回控制面 |
| `factory-state-doctor` | `uv run python scripts/factory-state-doctor --project <path> --owner <name>` | 诊断项目状态 | 不确定当前缺什么、卡在哪里、规则是否健康 | 输出诊断结果与建议动作 |
| `factory-refresh-memory` | `uv run python scripts/factory-refresh-memory --project <path>` | 刷新 AI 记忆 | 做完一轮变更后，想同步记忆层 | 更新 `.factory/memory/` 摘要与快照 |
| `factory-daily-status` | `uv run python scripts/factory-daily-status --project <path> --owner <name> --focus "<focus>"` | 生成每日报告 | 日终收尾或阶段汇报 | 更新日报并同步文档与 `.factory` |
| `factory-project-snapshot` | `uv run python scripts/factory-project-snapshot --project <path> --owner <name>` | 生成项目快照 | 想冻结当前阶段状态，便于回溯或交接 | 生成项目内部快照 |
| `factory-release-pack` | `uv run python scripts/factory-release-pack --project <path> --owner <name>` | 生成发布包 | 发布前准备交付材料 | 生成发布交付包 |
| `factory-handover-pack` | `uv run python scripts/factory-handover-pack --project <path> --owner <name>` | 生成交接包 | 换人、换 Agent、准备交接 | 生成交接材料 |
| `factory-retrospective` | `uv run python scripts/factory-retrospective --project <path> --owner <name>` | 生成项目复盘 | 一轮迭代或阶段完成后 | 生成复盘文档和 AI 摘要 |

## 8. 角色与团队协作

| 命令 | 常见写法 | 作用 | 什么时候使用 | 预期 |
|---|---|---|---|---|
| `factory-role-assign` | `uv run python scripts/factory-role-assign --project <path> --role <role> --owner <name> [--write-targets docs/,scripts/]` | 分派角色责任 | 需要明确某个角色当前负责什么，以及它会写哪些文件/目录 | 记录角色、工具、工作项和写入集合；默认阻断与其他角色分派的显式写集冲突 |
| `factory-role-workbench` | `uv run python scripts/factory-role-workbench --project <path> --role <role>` | 生成角色工作台 | 某个角色需要集中看自己的上下文和动作 | 生成角色执行工作台 |
| `factory-role-sync` | `uv run python scripts/factory-role-sync --project <path> --role <role>` | 同步角色状态 | 某个角色完成一轮动作后 | 刷新角色视图和状态 |
| `factory-role-review` | `uv run python scripts/factory-role-review --project <path> --role <role>` | 复核角色状态 | 想看某个角色当前执行得对不对 | 输出角色复核结果 |
| `factory-role-handoff` | `uv run python scripts/factory-role-handoff --project <path> --from <role> --to <role>` | 记录角色交接 | 一个角色把工作交给另一个角色 | 生成角色交接记录 |
| `factory-role-closeout` | `uv run python scripts/factory-role-closeout --project <path> --role <role>` | 执行角色收尾 | 某个角色一轮工作结束 | 完成角色收尾与状态更新 |
| `factory-role-retro` | `uv run python scripts/factory-role-retro --project <path> --role <role>` | 生成角色复盘 | 想复盘某个角色执行质量 | 生成角色复盘文档 |
| `factory-multi-agent-board` | `uv run python scripts/factory-multi-agent-board --project <path>` | 生成多 Agent 看板 | 多角色或多 Agent 并行协作时 | 生成协作看板，并提示待审批票据、高风险推荐动作、未分派工作项、角色写入集合和写集冲突 |
| `factory-team-sync` | `uv run python scripts/factory-team-sync --project <path> --owner <name>` | 团队级同步 | 需要批量刷新多个角色状态 | 输出团队同步记录 |
| `factory-team-closeout` | `uv run python scripts/factory-team-closeout --project <path> --owner <name>` | 团队级收尾 | 一轮团队工作结束 | 输出团队收尾记录 |
| `factory-team-retro` | `uv run python scripts/factory-team-retro --project <path> --owner <name>` | 团队级复盘 | 一轮协作或阶段结束后 | 输出团队级复盘 |

## 9. 恢复、质量漂移与自进化

| 命令 | 常见写法 | 作用 | 什么时候使用 | 预期 |
|---|---|---|---|---|
| `factory-agent-motivation` | `uv run python scripts/factory-agent-motivation --project <path> --owner <name>` | 刷新团队动能和自治规则 | 团队节奏变弱、多 Agent 协作前校准 | 生成动能、强化和自治文档 |
| `factory-recovery-coach` | `uv run python scripts/factory-recovery-coach --project <path> --item <id>` | 给出恢复教练方案 | 工作项受阻、空转、质量漂移时 | 生成恢复方案和建议动作 |
| `factory-pattern-fix` | `uv run python scripts/factory-pattern-fix --project <path> --item <id>` | 把单点问题扩展为模式级修复 | 你怀疑类似问题不止一个地方 | 生成模式级扫描与修复报告 |
| `factory-evolution-baseline` | `uv run python scripts/factory-evolution-baseline --project <path> --owner <name>` | 沉淀有效做法到基线 | 一轮实践后形成稳定方法 | 刷新项目自进化基线 |
| `factory-intent-eval` | `uv run python scripts/factory-intent-eval [--strict]` | 回放评估意图解析能力 | 修改了 `intent` 规则、自治策略或前台适配后 | 产出命中率、失败样本和固定报告 |
| `factory-skill-draft` | `uv run python scripts/factory-skill-draft <name> --summary "<summary>" [--triggers "..."] [--target-skill <skill>]` | 生成候选 skill 草案 | 你发现某类优化值得固化为 skill，但还不应该直接动正式 `skills/*/SKILL.md` | 在 `skills-drafts/` 下创建候选草案与评估骨架；如指定 `--target-skill`，会记录正式目标 skill 路径 |
| `factory-skill-eval` | `uv run python scripts/factory-skill-eval <candidate> [--strict]` | 执行候选 skill 正式评估 | 你已经补完 `change-summary.md` 和 `evals/evals.json`，要生成正式 `passed/failed` 报告 | 写入 `skills-drafts/<skill>/evals/eval-report.json` 与控制面评估记录；`--strict` 下失败返回退出码 `2` |
| `factory-skill-approval` | `uv run python scripts/factory-skill-approval <candidate|ticket> [--request|--approve|--reject|--list]` | 管理候选 skill 审批票据 | 你已经有 `skills-drafts/<skill>/` 草案，并且 `factory-skill-eval` 已经产出 `passed`，想显式批准它进入后续晋升链路 | 生成专用票据，或批准/拒绝票据并把结果写回候选目录；若评估未通过会直接拒绝申请 |
| `factory-skill-delete-approval` | `uv run python scripts/factory-skill-delete-approval <candidate|ticket> [--request|--approve|--reject|--list]` | 管理首次发布新 skill 的删除回退审批票据 | 你已经把一个新 skill 晋升到正式库，但因为没有旧版本备份，需要在删除回退前显式批准 | 生成专用删除回退票据，或批准/拒绝票据并把结果写回候选目录；若候选已有备份会直接拒绝申请 |
| `factory-skill-promote` | `uv run python scripts/factory-skill-promote <candidate> [--check]` | 执行候选 skill 正式晋升 | 你已经补齐 `eval-report.json`、`change-summary.md` 和 `approval.json`，准备把候选发布到正式 skill 库 | 先检查门禁；通过后写入正式 `skills/<name>/SKILL.md`，并生成晋升记录与旧版本备份 |
| `factory-skill-rollback` | `uv run python scripts/factory-skill-rollback <candidate> [--check]` | 执行已晋升 skill 安全回退 | 你要恢复已有正式 skill 的旧版本，或删除已获批准的首次发布新 skill | 先检查是否有旧版本备份；有备份时回写正式 `skills/<name>/SKILL.md`，无备份但删除审批已通过时删除正式文件，并生成回退记录与当前版本备份 |

## 10. 高层画像与工作流

### `factory-command-profiles`

常见 profile：

| Profile | 作用 | 什么时候使用 | 预期 |
|---|---|---|---|
| `requirements-kickoff` | 初始化需求阶段并生成会话入口 | 新项目刚进入需求阶段 | 需求骨架、校验和会话入口一起生成 |
| `design-kickoff` | 初始化设计阶段并登记技术画像 | 需求已确认，准备进设计 | 设计骨架、技术画像和会话入口一起生成 |
| `iteration-kickoff` | 初始化迭代计划并可选创建任务 | 设计完成，准备进实施计划 | 计划、任务和会话入口一起生成 |
| `pre-gate` | 执行 Gate 前检查组合 | 阶段收口前 | 阶段检查、质量检查和诊断结果 |
| `daily-close` | 执行日终收尾组合 | 每天收尾时 | 日报、记忆刷新、快照；经 `intent` 解析时按 `L2` 审批处理 |
| `release-ready` | 执行发布前组合动作 | 发布准备阶段 | 检查、发布包、交接包、快照；经 `intent` 解析时按 `L2` 审批处理 |
| `handover-ready` | 执行交接前组合动作 | 换人或换 Agent 前 | 交接材料、诊断、快照；经 `intent` 解析时按 `L2` 审批处理 |

### `factory-workflow-runner`

常见 workflow：

| Workflow | 作用 | 什么时候使用 | 预期 |
|---|---|---|---|
| `pre_gate` | 执行阶段检查和质量检查 | Gate 前 | 输出是否通过、关注还是未通过 |
| `daily_close` | 刷新记忆、生成日报、生成快照 | 日终收尾 | 完成当日收尾产物 |
| `release_ready` | 跑发布前检查、日报、发布包、交接包、快照 | 发布前 | 形成完整发布准备包 |
| `handover_ready` | 生成日报、交接包、快照 | 交接前 | 形成接手材料 |

### `factory-intent-resolver`

常见写法：

```bash
uv run python scripts/factory-intent-resolver 继续下一步 --project <path>
uv run python scripts/factory-intent-resolver 开始设计阶段并生成会话入口 --project <path> --execute-safe --owner "<name>"
uv run python scripts/factory-intent-resolver 执行 daily close workflow --project <path>
uv run python scripts/factory-intent-resolver 接管这个历史项目 --project <path> --request-approval --owner "<name>"
uv run python scripts/factory-intent-resolver 继续推进这个 skill intent-governance-coach --project <path>
uv run python scripts/factory-intent-resolver 撤回刚发布的新 skill intent-governance-coach --project <path>
uv run python scripts/factory-intent-approval IA-<ticket> --approve --owner "<name>"
```

使用规则：

- 默认只解析，不执行。
- 显式加 `--execute-safe` 后，只会自动执行主推荐动作中默认策略为 `auto` 的项。
- 显式加 `--request-approval` 后，会为 `L2/L3` 主推荐动作写出冻结审批票据，并附带建议 ownership 角色和写入集合。
- 如果主推荐动作是 `L2/L3` 且没有请求审批，会停在审批边界，不会继续执行。
- 当前输出会附带 `approval_guidance`，明确告诉你是否必须走票据审批。
- 当前已能识别 `command-profiles` 和 `workflow-runner` 的具体子目标；其中工作流型 profile 会自动提升到审批边界。
- 当前已能识别候选 skill 生命周期语义；当候选存在时，会直接路由到 `skill-eval`、`skill-approval`、`skill-promote`、`skill-delete-approval` 或 `skill-rollback`。
- 当自然语言明确命中 skill 生命周期，但当前工作区没有可用候选时，仍会保留对应 skill 动作为主推荐，并显式提示 `skills-drafts` 缺口。

## 11. 按目标反推该用哪个命令

| 你的目标 | 优先命令 |
|---|---|
| 不想记底层命令 | `factory-dispatch` |
| 想一键启动某个标准阶段 | `factory-command-profiles` |
| 想一键跑一组收尾工作流 | `factory-workflow-runner` |
| 只会说目标，不知道该选哪个动作 | `factory-intent-resolver` |
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
- 明明只会描述目标，却不先用 `factory-intent-resolver`
- 对 `L2/L3` 动作误以为 `--execute-safe` 会强行执行
- 为 `L2/L3` 动作申请审批后，却不通过 `factory-intent-approval` 处理冻结票据
- 想做高层动作，却直接从底层命令开始拼

如果你已经知道场景，但不知道该怎么写自然语言，让 AI 自己选这些命令，回看 [提示词速查](./prompt-templates.md)。
