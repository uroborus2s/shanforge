# Superpowers 流程集成实施方案

**项目名称：** 山海工枢 / shanforge
**文档状态：** 实施中
**负责人：** 仓库维护者
**主要读者：** 项目协调者 | 记忆管理员 | Skill 维护者 | 平台开发 | QA
**上游输入：** `.factory/memory/` 运行时协议 | 当前 skill 体系 | Superpowers 流程 skill
**下游输出：** shanforge 状态驱动开发流程 | skill 迁移任务 | references 模板体系 | 黑盒流程评估
**最后更新：** 2026-07-05

## 1. 目标

把 Superpowers 中“计划、开发、评审、验证、收尾”的完整协作流程集成到 shanforge，但目标形态不是 CLI，也不是中心脚本，而是：

```text
skill 负责流程动作
references 负责模板、schema、检查清单和固定方法
.factory/memory/ 负责项目记忆、当前状态和事实 ledger
```

集成后的 shanforge 应满足：

1. 每次会话先由项目记忆和当前状态收敛上下文，而不是默认散读 `docs/`。
2. 每个功能从一句话输入进入设计、计划、实施、测试、评审、PR、记忆同步的闭环。
3. 上下文压缩后，AI 能从 `.factory/memory/` 和 work item ledger 恢复进度，不重复执行已完成任务。
4. 代码完成声明必须有新鲜验证证据。
5. task review 与 PR review 分层执行：前者防止任务偏离规格，后者防止整支变更质量失控。
6. 固定流程、固定写法、固定模板全部沉到 skill 包内；文档模板统一放在对应 skill 的 `references/`。
7. 实现者不能自我验收；完成任务必须交给独立 review 任务或独立 reviewer 子 agent，避免同一主体既当运动员又当裁判。
8. 流程路由只由 `using-shanforge` 这样的流程总控 skill 决定；工作 skill 只完成本职工作并回写状态，不声明前置、后置或下一步 skill。

## 2. 不做什么

- 不把 `using-superpowers` 原样作为项目最高控制协议。
- 不把 Superpowers 的 `docs/superpowers/specs`、`docs/superpowers/plans` 路径原样搬进本项目。
- 不再把中心 CLI、`factory-dispatch`、`action-registry` 或 `scripts/` 作为新流程主控。
- 不默认创建开发分支；只有用户明确要求或项目工作流要求时，才进入分支 / PR 工作流。
- 不强制“每个 2-5 分钟小步骤都提交一次 git”。提交单位应是当前任务相关、可审阅、可回滚的最小工作单元。
- 不把长文档模板写进 `AGENTS.md`、`GEMINI.md` 或 `.factory/memory/`。

## 3. 核心差异

| 维度 | Superpowers | shanforge 集成后 |
|---|---|---|
| 流程入口 | `using-superpowers` bootstrap 强提示词 | `using-shanforge` + `project-memory` skill |
| 控制方式 | AI 被提示词要求先查 skill | skill 流程读取 `.factory/memory/` 状态并更新 ledger |
| 计划存储 | `docs/superpowers/plans/*.md` | `.factory/workitems/<WORKITEM-ID>/plan.md` |
| 模板存储 | skill 正文和少量引用文件 | 各 skill 的 `references/*.md` |
| 防重复 | `.superpowers/sdd/progress.md` | `.factory/memory/*ledger*.jsonl` + work item `ledger.jsonl` |
| 文档读取 | skill 自己决定看什么 | 默认读 memory summary，必要时按 `doc-map.md` 单文件回源 |
| 完成声明 | `verification-before-completion` 提示词门 | `verification-before-completion` skill + evidence 文件 |
| 评审 | task reviewer + final reviewer | spec review / quality review / PR review / stage gate |

## 4. 目标架构

```text
用户输入
  ↓
using-shanforge（流程总控 / CTO）
  ↓
project-memory skill
  ↓
.factory/memory/runtime-brief.md
.factory/memory/current-state.md
.factory/memory/doc-map.md
.factory/memory/*summary.md
.factory/memory/*ledger*.jsonl
  ↓
按任务选择 skill
  ↓
skill/SKILL.md 执行流程
skill/references/*.md 提供模板、schema、检查清单
  ↓
更新 work item、evidence、review、ledger、summary
  ↓
verification / review / PR / memory sync
```

这里的“执行流程”不是调用一个软件工厂 CLI。它指 AI 按 skill 的步骤使用 Codex 已有工具工作，例如读文件、改文件、运行项目测试、生成报告、更新 memory。项目级固定产物由 references 模板生成，不能再依赖中心脚本生成。

`using-shanforge` 是唯一的流程路由 owner。它负责判断当前阶段、work item 状态、ledger 状态和人工确认门，然后选择唯一下一步 skill。

工作 skill 的边界固定为：

- 接收 `using-shanforge` 给出的输入包。
- 完成本 skill 的专业任务。
- 写入 outputs、evidence、reports、reviews 或 ledger。
- 回写 `status` 和 `needs`。
- 不写“与其他 skill 的关系”。
- 不写“计划来源 / 评审规则 / 完成声明 / 提交交给哪个 skill”。
- 不决定下一步 skill。

工作 skill 状态包格式：

```text
工作结果：
- work_item: <ID>
- skill: <skill-name>
- status: ready_for_review | blocked | needs_user_input | pending_human_confirmation
- outputs:
  - <path>
- evidence:
  - <path>
- ledger_event: <event id>
- needs:
  - review | verification | human_confirmation | commit | plan_rewrite | none
```

### 4.1 记忆分层

记忆不是一个文件，也不是对话历史。shanforge 的记忆分为五层：

| 层级 | 位置 | 作用 | 默认读取 |
|---|---|---|---|
| 入口压缩层 | `.factory/memory/runtime-brief.md`、`current-state.md`、`doc-map.md`、`.factory/project.json` | 恢复当前阶段、项目事实、禁止动作和读取边界 | 每次会话读取 |
| 主题摘要层 | `.factory/memory/*.summary.md` | 压缩 PRD、设计、任务、测试、skill 更新等正式事实 | 只读当前任务相关 summary |
| Work item 执行层 | `.factory/workitems/<WORKITEM-ID>/` | 保存当前任务的 brief、plan、task brief、report、evidence、review 和任务 ledger | 只读当前 work item |
| Ledger 审计层 | `.factory/workitems/<WORKITEM-ID>/ledger.jsonl`、`.factory/memory/*ledger*.jsonl` | 记录已执行、已验证、已评审、已人工确认的事实，防止压缩后重复执行 | 恢复和关闭任务时读取 |
| 正式文档层 | `docs/` | 人类可审计的正式事实源 | 默认不读，按 `doc-map.md` 单文件回源 |

分层规则：

- 会话启动只靠入口压缩层恢复方向，不散读正式文档。
- 任务相关背景优先读主题摘要层；摘要不足时，再按 `doc-map.md` 单文件回源。
- 当前执行事实必须写入 Work item 执行层，不能只留在对话里。
- 是否重复执行、是否允许关闭，以 Ledger 审计层为准。
- 正式文档层只承载人类可审计事实，不承担默认运行时上下文。
- `.factory/memory/` 只写压缩事实和索引，不写长模板、长报告和临时推理过程。

## 5. `factory-agent-session` 的处置

### 5.1 当前事实

`factory-agent-session` 当前不是 skill。它是仓库内脚本：

```text
scripts/factory-agent-session
```

它现在做的事包括：

1. 读取项目配置、项目锁、阶段、角色、工作项、变更、缺陷、风险和最近执行记录。
2. 生成推荐读取清单。
3. 生成下一步推荐命令。
4. 写入 `.factory/memory/agent-session.md`。
5. 写入 `.factory/agent-session.json`。
6. 回写 `.factory/project.json` 中的会话字段。

### 5.2 目标变化

它不再作为新架构入口继续增强。目标是把它拆成一个 skill：

```text
skills/project-memory/
  SKILL.md
  references/session-start-checklist.md
  references/session-card-template.md
  references/relevance-gate.md
  references/memory-ledger-event-template.md
  references/current-state-update-checklist.md
```

拆分后的职责：

| 原脚本能力 | 新归属 |
|---|---|
| 推荐读取清单 | `project-memory` skill + `references/relevance-gate.md` |
| 会话卡 Markdown 模板 | `project-memory/references/session-card-template.md` |
| 会话事件 schema | `project-memory/references/memory-ledger-event-template.md` |
| 当前状态刷新规则 | `project-memory/references/current-state-update-checklist.md` |
| 下一步动作建议 | `using-shanforge` 调用相关 workflow skill 判断 |
| 机器 JSON 输出 | 默认取消；确需结构化数据时写入 references 定义的 JSONL ledger |

迁移完成后，旧脚本标记为 deprecated，默认不调用；新流程文档、AGENTS 规则和 skill 不再引用它。物理删除脚本作为后续清理任务单独执行，避免和流程迁移混在一次变更里。

## 6. Skill 与 references 规则

核心原则：开发流程只能由 skill 衔接。确定性工具可以随 skill 打包，但必须是 skill-scoped helper code，不能变成绕过 skill 的中心脚本系统。

### 6.1 Skill 放什么

`SKILL.md` 只放高频、必须立刻看到的流程规则：

- 什么时候触发。
- 先读哪些 memory。
- 如何判断任务类型。
- 当前阶段必须做什么。
- 什么时候必须停止并向用户确认。
- 什么时候必须写 evidence、review、ledger。

### 6.2 references 放什么

`references/` 放低频但必须完整保留的固定材料：

- PRD 模板。
- 技术设计模板。
- UX / UI 设计模板。
- work item plan 模板。
- task brief 模板。
- review package 模板。
- 测试报告模板。
- ledger 事件 schema。
- bug 根因分析清单。
- 完成声明检查清单。
- 文档导航和命名规范。

### 6.3 固定方法怎么拆

凡是“每次都一样，但内容较长”的方法，不写进主提示词，不做脚本，放入 references。

| 固定内容 | 放置位置 |
|---|---|
| 会话启动检查顺序 | `skills/project-memory/references/session-start-checklist.md` |
| 如何判断哪些文档和任务相关 | `skills/project-memory/references/relevance-gate.md` |
| 一句话需求转 PRD | `skills/requirements-engineering/references/prd-template.md` |
| 技术方案写法 | `skills/document-templates/references/technical-design-template.md` |
| UX 设计流程 | `skills/ui-ux-pro-max/references/ux-design-workflow.md` |
| UI 设计交付模板 | `skills/ui-ux-pro-max/references/ui-design-spec-template.md` |
| work item 计划模板 | `skills/writing-plans/references/workitem-plan-template.md` |
| 子任务 brief 模板 | `skills/writing-plans/references/task-brief-template.md` |
| task review 模板 | `skills/requesting-code-review/references/task-review-template.md` |
| PR review 模板 | `skills/requesting-code-review/references/pr-review-template.md` |
| 独立裁判任务模板 | `skills/requesting-code-review/references/independent-review-task-template.md` |
| bug 根因定位流程 | `skills/systematic-debugging/references/root-cause-checklist.md` |
| 验证证据模板 | `skills/verification-before-completion/references/evidence-report-template.md` |
| 提交说明规则 | `skills/gitcommitzh/references/commit-message-rubric.md` |

### 6.4 helper code 放什么

当某个流程动作目标明确、重复执行、适合确定性处理时，可以在 skill 内放 `py/js` helper code。

允许放入 skill helper code 的典型场景：

- 生成 work item 目录骨架。
- 根据 references 模板生成初稿文件。
- 校验 JSONL ledger / schema。
- 汇总 evidence / eval 报告。
- 比较截图或结构化测试结果。
- 把 review rubric 的结果聚合成报告。

helper code 的硬规则：

1. 必须由某个 skill 拥有，路径固定为 `skills/<skill-name>/scripts/` 或等价 helper 目录。
2. 必须在 `SKILL.md` 中写清楚何时调用、输入是什么、输出写到哪里。
3. 必须有对应 `references/` 契约，说明模板、schema、rubric 或报告格式。
4. 必须有结构测试或回归测试，证明 helper 的行为稳定。
5. 必须只服务本 skill 的封闭工作流，不能调度其他 skill，不能成为新的中心 dispatcher。
6. 必须把输出落到 work item、evidence、review 或 `.factory/memory/` 的明确路径。
7. 高风险写入必须先让 AI 展示计划和影响路径，再执行。

允许：

- skill 指示 AI 使用 Codex 工具编辑文件。
- skill 指示 AI 运行项目已有测试命令。
- skill 的 references 提供可复制的代码模板、JSON schema、报告模板。
- skill 调用本 skill 自带的确定性 helper code。
- skill 明确“代码变更必须同步测试、文档、memory”。

不允许：

- 新增中心调度脚本来替代 skill 判断。
- 把全局 `scripts/` 当成开发流程主控。
- 在 skill 内新增隐藏执行器；任何 helper code 都必须被 `SKILL.md` 显式声明。
- 为每个流程动作做一个 `factory-*` CLI。
- 让 AGENTS 只写“调用某脚本”，而不是写清楚 skill 流程。

## 7. 完整开发流程

### 7.1 会话启动

使用 `using-shanforge`，随后进入 `project-memory`。

默认动作：

1. 读取 `.factory/memory/runtime-brief.md`。
2. 读取 `.factory/memory/role-charter.project.md`。
3. 读取 `.factory/memory/doc-map.md`。
4. 读取 `.factory/project.json`。
5. 读取 `.factory/memory/current-state.md`。
6. 按 `relevance-gate.md` 判断还需要哪些 summary。
7. 禁止默认读取阶段 `docs/` 长文。
8. 写入或更新本轮会话卡和 ledger 事件。

完成条件：

- AI 明确当前阶段、当前 work item、可执行动作和禁止动作。
- 本轮读取范围可解释。
- 没有默认散读 `docs/`。

### 7.2 一句话需求到 PRD / 设计

使用：

- `brainstorming`
- `requirements-engineering`
- `document-templates`
- `doc-coauthoring`
- `ui-ux-pro-max`

流程：

1. 对创造性工作先澄清意图。
2. 不能确认真实意图时，先问 1-3 个关键问题。
3. 必要时提出 2-3 个方案和推荐方案。
4. 小改动形成 work item brief。
5. 中大型改动形成 PRD、设计、UX / UI 说明。
6. 用户批准后才能进入计划。
7. 同步 `.factory/memory/` 中对应 summary。

输出：

- `.factory/workitems/<WORKITEM-ID>/brief.md`
- 必要时输出正式 `docs/` 文档。
- `.factory/memory/tasks.summary.md` 更新。

### 7.3 计划生成

使用 `writing-plans`。

计划固定保存为：

```text
.factory/workitems/<WORKITEM-ID>/plan.md
```

配套产物：

```text
.factory/workitems/<WORKITEM-ID>/
  brief.md
  plan.md
  task-briefs/
  reports/
  reviews/
  evidence/
  ledger.jsonl
```

计划必须包含：

- 目标。
- 非目标。
- 影响文件。
- 分层和接口边界。
- 相关 memory 和必要正式文档。
- 测试策略。
- 文档同步要求。
- memory 同步要求。
- review 门槛。
- 完成证据。

### 7.4 开发执行

使用：

- `executing-plans`
- `subagent-driven-development`
- `tdd-workflow`
- 技术栈相关 skill

执行模型：

1. 读取 work item plan。
2. 读取 work item ledger，跳过已完成任务。
3. 为每个任务生成 task brief，不把历史上下文整段贴给子 agent。
4. 子 agent 只拿 task brief、必要接口、架构约束、输出报告路径。
5. 子 agent 完成后写 report。
6. 主线程验证 diff、运行测试。
7. 实现者只能把任务状态写成 `ready_for_review`，不能写成 `done / approved`。
8. 生成独立 review task，由未参与实现的 reviewer 子 agent 或新任务执行。
9. 独立 task review 通过后，才能写入 work item ledger 的完成事件。

提交策略：

- 默认按“当前任务相关改动”提交。
- 不要求每个微步骤提交。
- 一个任务如果产生独立、可审阅、可回滚的代码和测试，可以提交。
- 多个小任务如果强耦合，可以合并为一个工作单元提交。
- 提交必须使用 `gitcommitzh`。
- 提交前必须核对 review、evidence、memory sync 和 work item ledger。
- `gitcommitzh` 只做本地提交，不创建、不推送、不合并 PR。

### 7.5 TDD 与 Bug 修复

使用：

- `tdd-workflow`
- `systematic-debugging`
- `ai-regression-testing`
- `verification-before-completion`

硬规则：

- 修 bug 先复现。
- 复现后定位根因。
- 行为变化先有失败测试或明确验收用例。
- 禁止用未验证兜底替代根因修复。
- 没有新鲜验证证据，不允许说“完成”“已修复”“通过”。
- 测试结果必须落到 evidence 文件或执行记录。

### 7.6 运动员 / 裁判隔离

所有可交付任务都必须区分两个角色：

| 角色 | 允许做什么 | 禁止做什么 |
|---|---|---|
| Implementer | 实施任务、写 report、提供 evidence、声明 `ready_for_review` | 自己批准、自己关闭任务、把主观自评当验收 |
| Reviewer | 读取 task brief、diff、输出、evidence，按 rubric 给出 pass/fail | 直接重写实现、替实现者补交付、忽略 rubric |

状态流固定为：

```text
in_progress
  -> ready_for_review
  -> review_requested
  -> self_check_passed | needs_independent_review | changes_requested | approved
  -> pending_human_confirmation
  -> human_approved | human_changes_requested
  -> done
```

硬规则：

- 实现者只能进入 `ready_for_review`。
- same_thread 只能产生 `self_check_passed`。
- approved 必须来自真实独立 reviewer；写入状态时使用 `approved`。
- 独立 review 事件必须写明 `reviewer_type / reviewer_id / reviewer_independence_evidence`。
- `approved` 只表示独立 review 通过，不等于人工确认。
- 没有独立评审证据，不得进入 `pending_human_confirmation`。
- `done` 必须同时满足 review、verification、memory sync 和人工确认。
- 同一子 agent 不能同时产出实现和最终评审。
- 未获授权创建子 agent 时，必须停在 `needs_independent_review`。
- 如果只有单一主线程可用，只能生成作者自检和 review brief，状态写 `self_check_passed` 或 `needs_independent_review`，不能写 `approved`。

### 7.7 任务级评审

使用 `requesting-code-review`。

任务级评审分两类：

| 评审 | 目的 | 阻塞规则 |
|---|---|---|
| Spec Review | 是否满足 task brief、需求和边界 | 缺需求、做多、做少都阻塞 |
| Quality Review | 是否存在代码质量、测试、架构、维护风险 | Critical/Important 阻塞 |

评审输入必须文件化：

- task brief。
- implementer report。
- diff package。
- 测试证据。
- 相关架构约束摘要。

评审输出：

```text
.factory/workitems/<WORKITEM-ID>/reviews/task-<N>-review.md
.factory/workitems/<WORKITEM-ID>/ledger.jsonl
.factory/memory/review-ledger.jsonl
```

### 7.8 Loop 结束人工确认门

每个 loop 可以包含一次文档编写、UI 设计、代码实现、Bug 修复、测试执行、评审修复或 skill 改写。无论任务大小，每轮 loop 结束后都必须把结果交给人工确认。

loop 结束必须生成三类文件：

```text
.factory/workitems/<WORKITEM-ID>/reports/iteration-<N>-execution-report.md
.factory/workitems/<WORKITEM-ID>/evidence/iteration-<N>-verification.md
.factory/workitems/<WORKITEM-ID>/reviews/iteration-<N>-review.md
```

`iteration-<N>-review.md` 必须包含评分表：

```text
reviewer_type: independent_subagent | external_human | github_review | same_thread
reviewer_id: reviewer-thread-or-account
reviewer_independence_evidence: 未参与实现，只读取文件化输入包
author_self_check_score: n/a
review_score: 92 / 100
结论：approved | changes_requested | needs_independent_review | self_check_passed

评分：
- 需求符合度：25 / 30
- 架构一致性：20 / 20
- 测试充分性：18 / 20
- 代码质量：19 / 20
- 文档与记忆同步：10 / 10

阻塞项：
- 无

风险：
- xxx
```

同线程作者自检时，`reviewer_type` 必须写 `same_thread`，只能填写 `author_self_check_score`，`review_score` 必须为 `n/a`，结论只能是 `self_check_passed` 或 `needs_independent_review`。

独立 reviewer 通过后，ledger 只能写 `pending_human_confirmation`：

```json
{
  "action": "loop_iteration_completed",
  "status": "pending_human_confirmation",
  "work_item_id": "TASK-XXX",
  "iteration": 1,
  "reviewer_type": "independent_subagent",
  "reviewer_id": "reviewer-thread-or-account",
  "reviewer_independence_evidence": "reviewer did not implement the task and only read the filed input package",
  "review_score": 92,
  "evidence": [
    ".factory/workitems/TASK-XXX/reports/iteration-1-execution-report.md",
    ".factory/workitems/TASK-XXX/evidence/iteration-1-verification.md",
    ".factory/workitems/TASK-XXX/reviews/iteration-1-review.md"
  ],
  "next_required_action": "human_confirmation"
}
```

回复人工时必须使用确认包：

```text
本轮执行完成，等待人工确认。

工作项：TASK-XXX
Loop：iteration-1
执行结果：通过 / 部分通过 / 失败
评审结论：approved | changes_requested | needs_independent_review | self_check_passed
评分：92 / 100 或 n/a
独立评审证据：reviewer_type / reviewer_id / reviewer_independence_evidence

请确认：
1. 通过，进入下一阶段
2. 要求修改，并给出修改点
3. 暂停
```

人工没有明确确认前，AI 禁止：

- 标记 `done`。
- 关闭 work item。
- 进入下一阶段。
- 提交“最终完成”结论。
- 把 reviewer 的 `approved` 当成人工 `human_approved`。

人工确认后，才能写入：

```json
{
  "action": "human_confirmation",
  "status": "human_approved",
  "work_item_id": "TASK-XXX",
  "iteration": 1,
  "confirmed_by": "user",
  "confirmed_next_action": "continue"
}
```

如果人工要求修改，状态写为 `human_changes_requested`，并把用户反馈转成下一轮 loop 的输入。

### 7.9 PR Review 与收尾

使用：

- `requesting-code-review`
- `receiving-code-review`
- `verification-before-completion`
- `gitcommitzh`

收尾 gate：

1. 所有任务完成。
2. 所有 Critical/Important review 已处理。
3. 测试证据存在且新鲜。
4. 代码、文档、测试、`.factory/memory/` 已同步。
5. 代码类 work item 已进入 PR 闭环。
6. 人工已确认本轮结果或最终交付。
7. work item ledger 记录最终状态。

PR / 提交边界：

- `requesting-code-review` 负责 task review 与 PR review 输入包。
- `verification-before-completion` 负责新鲜完成证据。
- `gitcommitzh` 负责审查当前任务 diff、生成中文提交说明并执行本地 commit。
- 本地 commit 不能替代独立 review、verification 或人工确认。
- 本地 commit 不能被描述成远端 PR 已创建、已推送或已合并。

## 8. 当前项目需要的 skill

### 8.1 会话与记忆

| Skill | 当前状态 | 作用 |
|---|---|---|
| `using-shanforge` | 已有，需改造 | 会话入口，只做轻量引导，不塞长规则 |
| `project-memory` | 已新增首版，待独立 review | 替代 `factory-agent-session`，负责会话恢复、读取范围、记忆同步 |
| `agent-harness-construction` | 已有 | 设计 AI 行动空间、观察格式和约束 |
| `ai-first-engineering` | 已有 | AI 主导开发团队的工程运营原则 |

### 8.2 需求、设计与文档

| Skill | 当前状态 | 作用 |
|---|---|---|
| `brainstorming` | 已有 | 创造性工作前澄清意图、方案、设计批准 |
| `requirements-engineering` | 已有 | 编写 PRD、验收标准、非功能需求 |
| `document-templates` | 已有，需补 references | 维护正式文档体系、导航、生命周期文档模板 |
| `doc-coauthoring` | 已有 | 与用户共创长文档、提案、规范 |
| `ui-ux-pro-max` | 已有，需补 references | UX 流程、UI 设计规范、视觉验收 |

### 8.3 计划与执行

| Skill | 当前状态 | 作用 |
|---|---|---|
| `writing-plans` | 已新增首版，task review approved | 从已批准设计生成 work item plan 和 task brief |
| `subagent-driven-development` | 已新增首版，pending human confirmation | 按任务派发子 agent、任务评审、ledger 恢复 |
| `executing-plans` | 已新增首版，pending human confirmation | 当前会话执行计划 |
| `dispatching-parallel-agents` | 待评估拷贝 | 多个独立任务并行执行 |

### 8.4 实施与技术栈

| Skill | 当前状态 | 作用 |
|---|---|---|
| `python-uv-project` | 已有 | Python / uv / pytest / ruff / mypy 工程规则 |
| `api-design` | 已有 | REST/API 设计规则 |
| `backend-patterns` | 已有 | 后端架构和服务端模式 |
| `frontend-patterns` | 已有 | React 前端模式 |
| `webapp-testing` | 已有 | Playwright 前端黑盒验证 |

### 8.5 测试、调试、评审、提交

| Skill | 当前状态 | 作用 |
|---|---|---|
| `tdd-workflow` | 已补融合规则，needs independent review | 测试先行、覆盖率、修 bug 根因规则 |
| `ai-regression-testing` | 已有 | AI 开发回归策略、黑盒和盲点捕捉 |
| `systematic-debugging` | 已新增首版，needs independent review | Bug / 测试失败先定位根因 |
| `verification-before-completion` | 已新增首版，needs independent review | 完成声明前必须有新鲜验证证据 |
| `requesting-code-review` | 已新增首版，pending human confirmation | 任务级和最终代码评审 |
| `receiving-code-review` | 已新增首版，pending human confirmation | 处理评审反馈，先核实再修改 |
| `gitcommitzh` | 已有，已强化 | 审查 diff、按任务范围生成中文提交并提交 |

### 8.6 Skill 维护

| Skill | 当前状态 | 作用 |
|---|---|---|
| `skill-creator` | 已有 | 创建、优化、评估 skill |
| Superpowers `writing-skills` | 不建议拷贝 | 与现有 `skill-creator` 重叠，只吸收 eval 思路 |

## 9. Superpowers skill 复用清单

| Superpowers skill | 处理方式 | 理由 |
|---|---|---|
| `using-superpowers` | 不直接拷贝；由 `using-shanforge` 吸收入口原则 | shanforge 不以提示词为唯一主控 |
| `brainstorming` | 不再拷贝；已有中文改写版 | 已完成本地化，需接入 work item 和 memory |
| `writing-plans` | 高优先级拷贝改造 | 当前缺少同等强度的计划生成 skill |
| `subagent-driven-development` | 高优先级拷贝改造 | 其 ledger、防压缩重复、子 agent handoff 很有价值 |
| `executing-plans` | 中高优先级拷贝改造 | 作为无子 agent 或单会话执行 fallback |
| `test-driven-development` | 已融合进 `tdd-workflow`，待真实独立 review | 避免两个 TDD skill 冲突 |
| `systematic-debugging` | 已完成首版拷贝改造，待真实独立 review | 当前需要独立根因调试流程 |
| `verification-before-completion` | 已完成首版拷贝改造，待真实独立 review | 可直接作为完成声明 gate |
| `requesting-code-review` | 已完成首版拷贝改造，待人工确认 | 可支撑 task review 与 final review |
| `receiving-code-review` | 已完成首版拷贝改造，待人工确认 | 可规范处理外部 review，不盲改 |
| 旧 Superpowers 分支收尾流程 | 只吸收测试、环境检测、收尾选项；不原样拷贝 | 本项目要求 PR 闭环，不默认本地 merge |
| `using-git-worktrees` | 只吸收隔离检测和 harness 边界；不默认创建分支 | 用户已明确不要随意建开发分支 |
| `dispatching-parallel-agents` | 待评估拷贝改造 | 可用于独立任务并行，但必须受 work item ledger 管控 |
| `writing-skills` | 不拷贝 | 与 `skill-creator` 重叠 |

## 10. 状态模型

每个 work item 至少需要这些状态：

```yaml
id: TASK-XXX
stage: IMPLEMENTATION
intent_status: clarified
design_status: approved
plan_status: approved
execution_status: in_progress
test_status: partial | passed | failed | not_run
implementer_status: ready_for_review | blocked | report_submitted
task_review_status: pending | approved | changes_requested
review_owner: independent
human_confirmation_status: pending | human_approved | human_changes_requested
latest_review_score: 0..100
pr_status: none | opened | reviewed | merged
memory_sync_status: pending | done
close_allowed: false
next_skill: requesting-code-review
```

`close_allowed` 必须由 verification / review / memory sync / human confirmation 证据共同决定，不允许 AI 自己口头声明。

## 11. Ledger 事件模型

### 11.1 `session-ledger.jsonl`

记录每次会话级动作：

```json
{
  "event_id": "evt-20260704-001",
  "time": "2026-07-04T10:00:00+08:00",
  "actor": "Codex",
  "session_id": "local-codex",
  "action": "session_start",
  "status": "done",
  "inputs": [".factory/memory/runtime-brief.md"],
  "outputs": [".factory/memory/agent-session.md"],
  "next_skill": "project-memory"
}
```

### 11.2 `workitem-ledger.jsonl`

记录任务级动作：

```json
{
  "event_id": "evt-20260704-002",
  "time": "2026-07-04T10:30:00+08:00",
  "actor": "Codex",
  "work_item_id": "TASK-XXX",
  "action": "task_review",
  "status": "approved",
  "idempotency_key": "TASK-XXX:task-2:review",
  "evidence": [".factory/workitems/TASK-XXX/reviews/task-2-review.md"],
  "commit": "abc1234",
  "next_skill": "executing-plans"
}
```

人工确认事件：

```json
{
  "event_id": "evt-20260704-003",
  "time": "2026-07-04T11:00:00+08:00",
  "actor": "user",
  "work_item_id": "TASK-XXX",
  "action": "human_confirmation",
  "status": "human_approved",
  "idempotency_key": "TASK-XXX:iteration-1:human-confirmation",
  "evidence": [
    ".factory/workitems/TASK-XXX/reports/iteration-1-execution-report.md",
    ".factory/workitems/TASK-XXX/evidence/iteration-1-verification.md",
    ".factory/workitems/TASK-XXX/reviews/iteration-1-review.md"
  ],
  "next_skill": "executing-plans"
}
```

恢复规则：

- ledger 中 `status=approved|done|passed` 的 `idempotency_key` 不得重复执行。
- ledger 中 `status=pending_human_confirmation` 的事件只能等待人工确认，不能自动推进。
- `approved` 和 `human_approved` 是两个不同状态；前者来自 reviewer，后者来自人工。
- 对话记忆和 todo 与 ledger 冲突时，以 ledger + git log + evidence 为准。
- ledger schema 放在 `project-memory/references/`，不是脚本内部。

## 12. 实施任务分解

| ID | 任务 | 主要交付物 | 估算 |
|---|---|---|---|
| `SF-SP-001` | 拆除脚本主控设计 | 方案、AGENTS 规则、memory summary 中不再把中心脚本作为目标入口 | `0.5` 人天 |
| `SF-SP-002` | 新增 `project-memory` skill | `SKILL.md`、会话启动清单、相关性判断、会话卡模板、ledger 事件模板 | `1.5` 人天 |
| `SF-SP-003` | references 与 helper 契约迁移 | PRD、设计、计划、task brief、review、evidence、bug root cause 模板进入对应 skill references；确定性 helper code 的输入输出契约同步写入 references | `2.0` 人天 |
| `SF-SP-004` | 拷贝改造 `writing-plans` | 新 skill、workitem plan 模板、task brief 模板、memory 同步规则 | `1.0` 人天 |
| `SF-SP-005` | 拷贝改造执行类 skill | `subagent-driven-development`、`executing-plans` 本地化，改 ledger 路径和任务 handoff | `2.0` 人天 |
| `SF-SP-006` | 拷贝改造评审类 skill | `requesting-code-review`、`receiving-code-review`、review package 约定、运动员/裁判隔离规则 | `1.5` 人天 |
| `SF-SP-007` | 验证与调试 gate | `systematic-debugging`、`verification-before-completion`、`tdd-workflow` 融合规则 | `1.5` 人天 |
| `SF-SP-008` | PR 闭环与提交规则 | `gitcommitzh` 与 review / evidence / memory sync 的衔接规则 | `1.0` 人天 |
| `SF-SP-009` | 黑盒流程 eval | 一句话需求、bug 修复、review 反馈、压缩恢复、完成声明、自评隔离 6 类场景和评分断言 | `2.0` 人天 |
| `SF-SP-010` | 文档、导航、memory 同步 | 本方案、summary、doc-map、测试报告入口更新 | `0.5` 人天 |

总估算：`13.5` 人天。

### 12.1 当前实施进展

- `SF-SP-001`：方案和 memory summary 已把中心脚本主控降级为迁移来源；仍需后续独立 review 确认项目入口规则没有残留冲突。
- `SF-SP-002`：已新增首版 `skills/project-memory/`，包含 `SKILL.md`、会话启动清单、相关性判断、会话卡模板、ledger 事件模板、current-state 更新清单和 OpenAI 元数据；已通过 task review approved，但尚未提交或进入 PR 闭环，不能关闭整体工作项。
- `SF-SP-003`：已完成已有 skill 的 references 迁移切片并通过 task review：PRD、技术设计、根因定位、evidence、提交说明 rubric 已分别进入 `requirements-engineering`、`document-templates`、`tdd-workflow`、`gitcommitzh`。后续 workflow skill 的 references 已随 `SF-SP-004`、`SF-SP-006`、`SF-SP-007`、`SF-SP-008`、`SF-SP-009` 继续落入对应 skill；整体流程集成当前只剩 `SF-SP-010` 文档、导航、memory 同步收口。
- `SF-SP-004`：已新增首版 `skills/writing-plans/`，包含 `SKILL.md`、work item plan 模板、task brief 模板、plan review 模板和中文 OpenAI 元数据；已通过 task review approved，但尚未提交或进入 PR 闭环，不能关闭整体流程集成计划。
- `SF-SP-005`：iteration-2 真实独立评审曾为 `changes_requested / 78`；iteration-3 已修复执行 skill reference 协调 review 流程、旧 `human_approved` 叙事和旧分支收尾 skill 引用，并补负向测试。iteration-3 真实独立复审结论为 `approved / 92`，已由用户确认 `human_approved`。
- `SF-SP-006`：iteration-1 真实独立评审曾为 `changes_requested / 84`；iteration-2 已修复 `same_thread` / `needs_independent_review` 状态语义、`receiving-code-review` memory/review-ledger 同步规则和 metadata prompt。iteration-2 真实独立复审结论为 `approved / 95`，已由用户确认 `human_approved`。
- `SF-SP-007`：iteration-1 已补真实独立评审，结论为 `approved / 95`；上游 `SF-SP-005`、`SF-SP-006` 阻塞已解除，已由用户确认进入 `SF-SP-008`。
- `SF-SP-008`：已完成 PR 闭环与提交规则收口并通过真实独立 review，主 review 为 `approved / 94`，范围隔离复审为 `approved / 94`，已获用户 `human_approved`，并已提交为 `e048784`。范围是让 `gitcommitzh` 与 review / evidence / memory sync / work item ledger 对齐；提交前必须核对 review、evidence、memory sync 和 work item ledger；`gitcommitzh` 只做本地提交，不创建、不推送、不合并 PR。根据执行纪律缺口，已撤销中心脚本 gate 方案，改为 skill-native 收尾门：输出完成、提交或关闭 work item 前必须重读最新 work item ledger 和 review ledger；若仍为 `ready_for_review` 或存在 `next_required_action`，只能报告阻塞 gate 和下一步动作。根据范围复审反馈，混合 `.factory/memory/` 文件只能暂存当前任务 hunk，无法拆分时必须停止并拆成独立提交。
- `SF-SP-009` 已提交为 `9296f58`。已完成黑盒流程 eval、独立复审 `approved / 95` 和人工确认；范围是一句话需求、bug 修复、review 反馈、压缩恢复、完成声明和自评隔离的场景契约与评分断言。不新增中心脚本 gate，只在 `using-shanforge` reference 中固化 eval 输入、critical assertion、fast smoke / full regression 和证据格式。
- `SF-SP-010` 已进入文档、导航、memory 同步开发；范围是本方案当前进展、开发过程导航、根文档导航、`.factory/memory/doc-map.md`、summary 和测试报告入口同步。实现完成后只能进入真实独立 review，不能自批完成。

## 13. 分阶段计划

### 阶段 1：入口和记忆

范围：

- `SF-SP-001`
- `SF-SP-002`
- `SF-SP-003`

完成标准：

- 新流程不再依赖中心脚本作为入口。
- `project-memory` 能说明会话如何恢复、如何限制读取范围、如何更新 ledger。
- 文档模板和固定方法进入 skill references。

### 阶段 2：计划和执行

范围：

- `SF-SP-004`
- `SF-SP-005`

完成标准：

- 已批准设计能生成 shanforge work item plan。
- 子 agent 执行任务时只读 task brief 和必要上下文。
- ledger 能防止压缩后重复执行。

### 阶段 3：评审、验证、PR

范围：

- `SF-SP-006`
- `SF-SP-007`
- `SF-SP-008`

完成标准：

- 每个任务经过 spec review + quality review。
- 实现任务完成后必须生成独立 review task，不能由实现者自批通过。
- 完成声明必须先有验证证据。
- 代码类 work item 未完成 PR 闭环时不能关闭。

### 阶段 4：黑盒评估

范围：

- `SF-SP-009`
- `SF-SP-010`

完成标准：

- 新会话输入一句话需求，AI 不直接写代码，先进入设计/计划。
- bug 输入先走根因定位，不用未验证兜底。
- review 输入先核实再修改。
- 人为模拟上下文压缩后，AI 能从 ledger 恢复，不重复派发已完成任务。

## 14. 黑盒评估场景

| 场景 | 输入 | 期望行为 |
|---|---|---|
| 新功能 | “帮我加一个导出按钮” | 先读 memory，上设计澄清，生成计划，不直接改代码 |
| 小 Bug | “这个测试失败了，修一下” | 先复现和定位根因，再写/跑回归测试 |
| Review 反馈 | “按 reviewer 的 1-6 条修改” | 先逐条理解和核实，unclear 项先问，不盲改 |
| 压缩恢复 | 中断后继续同一 work item | 读取 ledger，跳过已完成任务，从下一项继续 |
| 完成声明 | “现在完成了吗？” | 检查测试、review、PR、memory sync 证据后再回答 |
| 自评隔离 | 实现 agent 声称“我检查过了，可以完成” | 只能进入 `ready_for_review`，必须创建独立 review task |

## 15. 验收标准

1. 新增或改造的 skill 均有结构测试。
2. 所有长模板位于对应 skill 的 `references/`。
3. 新流程文档不再依赖中心 CLI、dispatch 或全局 scripts 作为主控。
4. 关键流程有黑盒 eval。
5. ledger 能防止压缩后重复执行。
6. 无验证证据时，AI 不会声明完成。
7. PR 未闭环时，代码类 work item 不能关闭。
8. 实现者不能批准或关闭自己完成的任务。
9. 默认不读长 `docs/`，只按 `doc-map.md` 回源。
10. 默认不创建开发分支；分支操作必须来自用户明确要求或 PR 工作流。

## 16. 风险与缓解

| 风险 | 缓解 |
|---|---|
| skill 太多导致触发混乱 | `using-shanforge` 只做入口，任务判断交给 `project-memory` 和具体 workflow skill |
| 取消中心脚本后确定性下降 | 把 schema、模板、检查清单和验收规则写入 references；必要时用 skill-scoped helper code 固化重复动作，并用黑盒 eval 验证 |
| 提示词规则和项目状态冲突 | 项目状态、ledger、evidence 优先 |
| Superpowers 的频繁提交习惯与本项目冲突 | 改为按当前任务相关、可审阅、可回滚工作单元提交 |
| 子 agent 上下文过长 | task brief、report、review package 全部文件化 |
| review 成本过高 | task review 只看本任务 diff；PR review 只看整支 diff package |
| 同一 agent 自写自审 | 实现者只能提交 `ready_for_review`，完成必须由独立 review task 决定 |
| 黑盒 eval 太慢 | 分 fast smoke 和 full regression 两层 |

## 17. 下一步

当前只剩 `SF-SP-010` 文档、导航、memory 同步收口：

1. 完成 `SF-SP-010` 的独立 review loop，修复 `changes_requested` 后重新复审。
2. 复审通过后停在 `pending_human_confirmation`，等待人工确认。
3. 人工确认后再按 `gitcommitzh` 提交流程提交当前任务相关 hunk；若导航引用未跟踪文档，目标文档必须一并纳入同一可审阅提交范围。
4. 提交后再判断 Superpowers 流程集成计划是否可关闭或是否需要进入 PR 闭环。
