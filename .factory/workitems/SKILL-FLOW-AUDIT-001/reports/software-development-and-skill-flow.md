# 软件开发过程与 Skill 调用流程

## 已读事实

- `.factory/memory/runtime-brief.md`
- `.factory/memory/role-charter.project.md`
- `.factory/memory/doc-map.md`
- `.factory/project.json`
- `.factory/memory/current-state.md`
- `.factory/memory/motivation-state.md`
- `.factory/memory/autonomy-rules.md`
- `.factory/memory/evolution-baseline.md`
- `.factory/memory/tasks.summary.md`
- `.factory/memory/skill-updates.summary.md`
- `.factory/memory/tests.summary.md`
- `skills/using-shanforge/SKILL.md`
- `skills/project-memory/SKILL.md`
- `docs/04-project-development/05-development-process/software-development-process.md`
- `docs/04-project-development/05-development-process/superpowers-workflow-integration-plan.md`
- `docs/04-project-development/05-development-process/implementation-plan.md`

## 软件开发完整过程

### 1. 会话启动

入口是 `using-shanforge`。它先让 `project-memory` 恢复最小上下文，读取 `.factory/memory/` 压缩入口、当前状态、doc map 和相关 summary。默认不散读 `docs/` 长文。

输出要求：

- 当前阶段。
- 当前 work item。
- 已读和排除的上下文。
- 禁止动作。
- 待决事项。

### 2. 意图澄清

新想法、需求不清或创造性任务先进入 `brainstorming`。目标是把一句话输入变成可审阅 brief，而不是直接写代码。

输出要求：

- `.factory/workitems/<WORKITEM-ID>/brief.md`
- 必要的方案比较。
- 用户需要确认的问题。

### 3. 需求与验收标准

需求明确但未结构化时进入 `requirements-engineering`。要写清 REQ、NFR、验收标准、风险和建议测试点。

输出要求：

- 正式需求或 work item brief。
- 可追踪验收标准。
- 影响范围和风险。

### 4. 设计与边界

涉及架构、模块、接口、UI 或文档体系时进入 `document-templates`、`doc-coauthoring` 或 `ui-ux-pro-max`。代码类任务进入实现前必须核对技术选型和相关架构边界。

输出要求：

- 设计说明。
- 文件落点。
- 分层和接口 owner。
- 不做什么。

### 5. 实施计划

多步骤任务进入 `writing-plans`。计划固定落到 `.factory/workitems/<WORKITEM-ID>/plan.md`，并生成 task brief。

输出要求：

- 目标和非目标。
- 文件结构。
- Red / Green / Review / Memory sync 步骤。
- 测试策略。
- review gate。

### 6. 开发执行

计划批准后，根据任务耦合度进入 `subagent-driven-development` 或 `executing-plans`。子 agent 只拿 task brief 和必要上下文，不读完整历史。

输出要求：

- implementation report。
- evidence。
- ledger 事件。
- 状态只能到 `ready_for_review`、`blocked` 或 `needs_user_input`。

### 7. TDD 与 Bug 修复

新增行为走 `tdd-workflow`。Bug、测试失败、构建失败和异常行为走 `systematic-debugging`。修复前先复现和定位根因，禁止用未验证兜底替代根因修复。

输出要求：

- 失败复现。
- 直接原因和根源原因。
- 最小修复。
- 防回归测试。

### 8. 完成前验证

准备说“完成”“已修复”“通过”“可提交”之前进入 `verification-before-completion`。必须运行新鲜验证命令，读取输出和 exit code。

输出要求：

- `.factory/workitems/<WORKITEM-ID>/evidence/`
- verification report。
- 失败、跳过、未运行项。

### 9. 独立评审

实现者不能批准自己的交付。`requesting-code-review` 组织 task review、PR review 或独立 review task。same-thread 只能产生 `self_check_passed`，真实 `approved` 必须来自独立 reviewer。

输出要求：

- review package。
- review score 或 author self-check score。
- `.factory/workitems/<WORKITEM-ID>/reviews/`
- `.factory/memory/review-ledger.jsonl`

### 10. 评审反馈处理

review 为 `changes_requested` 时进入 `receiving-code-review`。先核实反馈，再逐项修改；不清楚就问，不盲改。

输出要求：

- feedback triage。
- review response。
- 修复报告。
- 新验证证据。

### 11. 人工确认门

独立 reviewer 的 `approved` 不等于人工确认。loop 结束后必须等待用户确认，才能进入下一阶段、关闭 work item 或提交最终完成结论。

输出要求：

- `pending_human_confirmation` ledger 事件。
- 人工确认包。
- 用户确认后再写 `human_approved` 或 `human_changes_requested`。

### 12. 提交与 PR 闭环

用户明确要求提交时使用 `gitcommitzh`。它只做本地提交，不创建、不推送、不合并 PR。提交前必须核对当前任务范围、work item ledger、review ledger、verification evidence 和 memory sync。

输出要求：

- 中文变更说明。
- 中文 commit message。
- 真实 git commit hash。
- 若需要远端闭环，另走 GitHub / PR 流程。

### 13. 发布、维护和复盘

发布前核对测试、文档、追踪矩阵、发布说明和运维文档。维护阶段把缺陷、风险和改进沉淀回 `.factory/memory/`、正式文档和后续 work item。

## Skill 调用完整流程

1. 用户输入或 slash 触发进入当前会话。
2. 命中 Shanforge 项目时，先使用 `using-shanforge`。
3. `using-shanforge` 先交给 `project-memory` 恢复上下文。
4. `project-memory` 输出阶段、work item、读取范围和禁止动作。
5. `using-shanforge` 根据状态和路由表选择唯一下一步 skill。
6. 主 agent 完整读取被选中 skill 的 `SKILL.md`。
7. 若 `SKILL.md` 指向 references，只读取当前任务需要的 reference。
8. 工作 skill 只完成自己的专业任务，不决定下一个 skill。
9. 工作 skill 输出统一状态包：`work_item`、`skill`、`status`、`outputs`、`evidence`、`ledger_event`、`needs`。
10. `using-shanforge` 接收状态包后再判断下一步。
11. 到 review、verification、human confirmation 或 commit gate 时，必须重读 ledger 和证据。
12. 完成声明只能在验证、评审、人工确认和 memory sync 齐备后给出。

## 任务执行完整流程

| 阶段 | owner skill | 输入 | 动作 | 输出 | gate |
|---|---|---|---|---|---|
| 会话恢复 | `project-memory` | memory 入口、会话卡 | 限制读取范围 | 会话卡、ledger | 不散读 docs |
| 路由 | `using-shanforge` | 当前状态、ledger | 选唯一下一步 skill | 输入包 | 不让工作 skill 路由 |
| brief | `brainstorming` | 用户意图 | 澄清和方案 | brief | 用户批准 |
| 需求 | `requirements-engineering` | brief | REQ / NFR / AC | 需求文档 | 验收可测 |
| 设计 | `document-templates` / `doc-coauthoring` / `ui-ux-pro-max` | 需求 | 边界和方案 | 设计文档 | 分层清楚 |
| 计划 | `writing-plans` | 已批准输入 | 拆任务 | plan、task brief | plan review |
| 执行 | `subagent-driven-development` / `executing-plans` | plan、task brief | 实施 | report、evidence | ready_for_review |
| 测试 / debug | `tdd-workflow` / `systematic-debugging` | 需求或失败 | Red-Green、根因 | 测试和修复证据 | 根因已验证 |
| 验证 | `verification-before-completion` | 声明、命令 | 跑新鲜验证 | evidence | exit code 支持结论 |
| 评审 | `requesting-code-review` | diff、report、evidence | 独立 review | review report | approved 或 changes_requested |
| 反馈处理 | `receiving-code-review` | review feedback | 核实并修复 | response、fix report | 重新验证 |
| 人工确认 | `using-shanforge` | review、evidence | 输出确认包 | human gate | 用户明确确认 |
| 提交 | `gitcommitzh` | 当前任务 diff | 审范围并提交 | local commit | 不冒充 PR |

## 本轮创建的子任务

### 中文语言与 Prompt 质量评审

- 子 agent：`019f3329-655c-7a83-84b7-40d8b461b0f6`
- 输入：仓内 `skills/*/SKILL.md`
- 输出：按 skill 的 0-100 分报告、低分项问题、Top 10 问题模式。

### Skill 流程完整性测试

- 子 agent：`019f3329-96f2-7340-8e8d-620329e378db`
- 输入：核心 workflow skills、流程方案相关章节、测试摘要。
- 输出：流程矩阵、缺口、风险、最小测试断言建议。

## 当前边界

本轮主线程已创建子任务并文件化流程。子任务报告返回前，不把本工作项标为 `approved` 或 `done`。

## 子任务结果摘要

中文语言与 prompt 评审已完成，只读未改文件。评分最高的一组包括 `systematic-debugging`、`verification-before-completion`、`using-shanforge`、`browser-control`、`brainstorming`、`project-memory`、`stratix-service`、`writing-plans`；主要问题集中在入口过长、英文/旧生态口径残留、输出契约不统一、教程型内容过多和部分职责边界不清。完整报告见 `reviews/language-prompt-review.md`。

流程测试已完成，只读未改文件。结论是本地软件开发闭环覆盖清楚：从意图澄清到本地提交都有 skill 和门禁；主要缺口是远端 PR / push / merge 只有边界声明，没有固定执行闭环；`requirements-engineering`、`brainstorming` 等需求/文档类 skill 的状态包和 ledger gate 也弱于执行类 skill。完整报告见 `reviews/skill-flow-test-report.md`。

## 后续清理决策

按用户要求复查低分 skill 是否接入开发流程：

- 保留 `ai-regression-testing`：`using-shanforge` 的 Bug / 验证失败路由和 Superpowers 流程方案仍引用它。
- 保留 `agent-harness-construction`：当前流程方案把它列为会话与记忆 / agent 行动空间设计所需 skill。
- 保留 `ai-first-engineering`：当前流程方案把它列为 AI 主导工程运营原则，且根因修复纪律测试仍覆盖它。
- 删除 `find-skills`：未接入当前开发流程、项目配置或测试，只剩历史审计报告引用。
- 删除 `web-artifacts-builder`：未接入当前开发流程、项目配置或测试，只剩历史审计报告引用。

### 追加删除：backend-patterns

用户确认 `backend-patterns` 是通用后端教程，不应继续作为 Shanforge 开发流程 skill 保留。本轮已按 `remove-backend-patterns` 子任务删除该 skill，并清理活跃配置和流程引用。历史语言评审报告中的评分记录保留，不改写历史事实。

### 追加修复：requirements-engineering

按流程测试报告的首要缺口，已创建 `requirements-engineering-flow-contract` 子任务，并补齐 `requirements-engineering` 的 Shanforge 输出路径、memory sync、work item ledger、状态包和自批禁止项。该 skill 现在只回写状态与 `needs`，不决定下一步 skill。

### 追加修复：brainstorming

按 `skill-flow-test-report.md` 的第二项缺口，已创建 `brainstorming-flow-contract` 子任务，并把 `brainstorming` 从“下一步 skill 交接”改为状态回写包。该 skill 现在只回写 brief、批准状态、outputs、evidence、ledger_event 和 `needs`；流程路由仍由 `using-shanforge` 根据阶段、work item 状态和 ledger 判断。

新增结构测试固定以下规则：

- `brainstorming` 不出现 `下一步 skill：`、`给出下一步 skill`、`handed_off` 等路由字段。
- `brainstorming` 的 metadata 不再暗示自己选择后继 skill。
- `spec-document-reviewer-prompt.md` 检查状态回写，而不是检查下一步 skill。
- `skill-flow-test-report.md` 建议的 requirements / brainstorming 两个流程契约缺口均有定向测试覆盖。

验证结果：

- `uv run pytest tests/test_brainstorming_skill.py tests/test_skill_flow_process_audit.py tests/test_requirements_engineering_skill.py`：`11 passed`
- `uv run ruff check tests/test_brainstorming_skill.py tests/test_skill_flow_process_audit.py tests/test_requirements_engineering_skill.py`：通过
- `ledger.jsonl` JSONL 校验：通过

### skill-flow-test-report 缺口处理状态

| 缺口 | 状态 | 处理 |
|---|---|---|
| `requirements-engineering` 缺 Shanforge 状态包、ledger、review gate | 已修复，待独立 review | `requirements-engineering-flow-contract` |
| `brainstorming` 存在下一步 skill 交接冲突 | 已修复，待独立 review | `brainstorming-flow-contract` |
| 黑盒 eval 只有契约结构测试，不是真实行为回放 | 未在本轮实现 | 这是新执行能力，不塞进本次流程契约修复 |
| 远端 PR / push / merge 无固定闭环 | 未在本轮实现 | 当前仍保持边界声明：本地提交不得冒充远端闭环 |
| 真值读取清单与 `project-memory` 最小读取策略差异 | 保持现状 | 以“不散读、可解释读取”为准 |

### 最新独立评审与评分

已创建独立评审子任务，reviewer 未参与实现，只读取文件化输入包、rubric、评审范围内文件、diff 和验证输出。

- Review 文件：`.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-report-fixes-independent-review.md`
- reviewer_type：`independent_subagent`
- reviewer_id：`codex-independent-reviewer-20260706`
- reviewer_agent_id：`019f3353-d96a-7be0-bc83-030c9c45e2cd`
- review_status：`approved`
- review_score：`96 / 100`
- next_gate_status：`pending_human_confirmation`
- Findings：无 Critical、Important 或 Minor。

评分：

- 需求符合度：`29 / 30`
- 架构一致性：`20 / 20`
- 测试充分性：`19 / 20`
- 代码质量：`19 / 20`
- 文档与记忆同步：`9 / 10`

当前状态：本轮修复已通过独立 review，等待人工确认。未获用户确认前，不得写 `human_approved`、关闭 work item 或提交最终完成结论。

## Iteration 2 子任务结果

用户要求重新创建两个子任务，对当前 skill 文本和流程完整性做新一轮评审 / 测试。本轮不覆盖 iteration-1 历史报告。

### 中文语言与 Prompt 质量评审

- 报告：`.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/language-prompt-review-iteration-2.md`
- 子代理：`019f335c-934c-7983-b5ee-0eddc5cfe9d7`
- 状态：`DONE`
- 扫描当前存在的 skill：`34`
- 最低分：`62`（`ui-ux-pro-max`）
- 最高分：`95`（`systematic-debugging`、`verification-before-completion`）
- 主要问题：入口过长、教程化、输出契约不统一、prompt 边界过宽、旧生态 / 英文口径残留。

### Skill 流程完整性测试

- 报告：`.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-completeness-test-iteration-2.md`
- 子代理：`019f335c-d88f-77b2-ac61-c0901276606e`
- 状态：`DONE`
- 总评分：`82 / 100`
- Critical：`1`
- Important：`4`
- 验证：相关 pytest `60 passed / 1 failed`，ruff 通过。
- 失败原因：`tests/test_black_box_workflow_eval.py::test_workflow_plan_tracks_sf_sp_009_development_scope` 仍期待旧短语“当前已进入黑盒流程 eval 开发”，当前计划文档已进入完成态口径。

最新 gate：存在 Critical 和 failing test，不能进入完成 / 人工确认 / 提交；下一步应先分析并修复 flow completeness report 中的 Critical / Important findings。

## Iteration 3 子任务结果

按用户要求，在修复 `language-prompt-review-iteration-2.md` 后重新创建并执行两类子任务。

### 中文语言与 Prompt 质量复评

- 报告：`.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/language-prompt-review-iteration-3.md`
- 子代理：`019f3371-8b9b-7eb3-8334-38af9fbe6e44`
- 状态：`DONE`
- 扫描当前存在的 skill：`34`
- 平均分：`92.3`（iteration-2 为 `85.2`）
- 低于 90 分 skill：`5`（iteration-2 为 `21`）
- 最低 / 最高分：`87 / 95`
- 结论：语言与 prompt 质量明显改善，剩余低分集中在 `skill-creator`、`document-templates`、`gitcommitzh`、`python-uv-project`、`stratix-service`。

### Skill 流程完整性复测

- 报告：`.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-completeness-test-iteration-3.md`
- 子代理：`019f3371-ba85-75b3-ad69-76212325e59c`
- 状态：`DONE`
- 总评分：`86 / 100`（iteration-2 为 `82 / 100`）
- Critical：`1`
- Important：`3`
- 验证：相关 pytest `74 passed / 1 failed`，ruff 通过。
- 仍失败：`tests/test_black_box_workflow_eval.py::test_workflow_plan_tracks_sf_sp_009_development_scope`
- Critical：仍缺 S1-S6 黑盒行为回放 transcript evidence。

当前 gate：`changes_requested`。语言/prompt 修复有效，但流程完整性还有 Critical 和 failing test；不得声明完成、不得进入人工确认、不得提交。
