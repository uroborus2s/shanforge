# Skill Flow Completeness Test Iteration 5

- work_item: `SKILL-FLOW-AUDIT-001`
- role: Skill 流程测试工程师
- date: 2026-07-06
- status: passed
- total_score: 96 / 100
- Critical: 0
- Important: 0
- Minor: 2

## 结论

当前 skill 流程已覆盖 Shanforge 本地软件开发闭环，并补齐 iteration-4 报告中的主要缺口：S1-S6 dry-run transcript 已存在且字段完整；远端 PR / push / merge 已有 handoff owner、输入、evidence、失败语义和状态词；`document-templates`、`requesting-code-review`、`receiving-code-review` 已补标准 `工作结果` 状态包。

本轮不声明真实远端 PR / push / merge 已执行，也不把 dry-run transcript 当成真实代码修复、commit、push、PR 或 merge。残留问题只影响证据精细度和辅助 skill 直接作为 work item owner 时的一致性。

## Flow matrix

| step | owner skill | input | action | output | gate | assessment |
|---|---|---|---|---|---|---|
| 1. 会话恢复 | `project-memory`；流程路由由 `using-shanforge` 判断 | 当前对话、`.factory/memory/agent-session.md`、work item ledger、必要 summary | 最小读取、恢复阶段/work item、按 ledger 防重复 | 会话卡、已读/排除、禁止动作、待决事项、必要 ledger/memory 更新 | 不散读 docs；正式事实和 ledger 优先；相同 idempotency 不重复 | 满足 |
| 2. 意图澄清 / brief | `brainstorming` | 用户意图、会话卡、work item brief、ledger | 一次一个问题、方案比较、收敛 brief 或设计输入 | `工作结果` 状态包、brief、approval、outputs、evidence、ledger_event、needs | 只回写状态，不指定下一步 skill；作者不得自批 approved/done | 满足 |
| 3. 需求 / AC / NFR | `requirements-engineering` | 已批准 brief、必要事实源、baseline 影响 | 写用户故事、REQ、AC、NFR、非目标、风险、baseline 影响 | `requirements_ready` / `ready_for_review` 状态包、产物、evidence、ledger_event | reviewer approved 和 human_approved 前不得把需求写成已批准 | 满足 |
| 4. 设计 / 文档 / 边界 | `document-templates`；辅助 `doc-coauthoring` / `ui-ux-pro-max` | 已批准需求/设计输入、正式 docs 事实、目标读者和边界 | 创建/更新正式文档、维护 docs-stratego、同步索引/版本历史 | `document-templates` 标准状态包、docs、校验证据、ledger_event | 不恢复旧 factory 脚本；不批量制造空壳；事实冲突先回源 | 满足；辅助 skill 直接做 work item owner 时仍需包装 |
| 5. 实施计划 / task brief | `writing-plans` | 已批准 spec/需求/设计/work item brief | 锁定文件范围、拆任务、写 Red/Green/review/memory sync | plan、task briefs、review handoff、evidence、ledger_event、状态包 | 计划只能到 `ready_for_review`；approved 来自 review | 满足 |
| 6. 执行 / evidence / report / ledger | `subagent-driven-development` 或 `executing-plans` | approved plan、task brief、ledger、允许文件范围 | 执行任务、生成 evidence/report/review input、必要 memory sync | evidence、implementer report、review checkpoint、ledger_event、状态包 | 实现者不得自批；缺 evidence/report/review checkpoint 不得 ready | 满足 |
| 7. Bug 修复 / TDD / 根因 | `systematic-debugging` + `tdd-workflow` + `ai-regression-testing` | 失败输出、exit code、复现步骤、调用链、相关测试 | 先复现和根因，再 Red/Green、根因修复和回归 | 根因记录、red/green evidence、回归测试、ledger_event、状态包 | 根因不明只能加诊断；禁止兜底式修复声明完成 | 满足 |
| 8. 完成前验证 | `verification-before-completion` | 要验证的声明、plan/diff/review、命令或检查项 | 跑本轮新鲜完整命令，读取完整输出和 exit code | verification evidence/report、失败/跳过/未运行统计、ledger_event、状态包 | 没有新鲜证据不得声明完成；review 不能替代 verification | 满足 |
| 9. 独立 review / scoring | `requesting-code-review` | task brief、implementer report、evidence、diff、独立性证据 | Spec Review + Quality Review，评分，记录独立性 | review 文件、review ledger、work item ledger、标准状态包 | same-thread 只能 self_check；approved 必须有独立 reviewer 证据 | 满足 |
| 10. review 反馈处理 | `receiving-code-review` | review feedback、PR 评论、任务评审意见 | 逐条 triage、核实、修复或 pushback，每项验证 | triage、response、fix report、verification evidence、ledger_event、状态包 | 禁止盲改和表演式同意；memory sync 缺失不得完成 | 满足 |
| 11. 人工确认门 | `using-shanforge` | independent review approved、score、ledger/evidence/final audit issue report | 停止并输出人工确认包 | `pending_human_confirmation`、评分、阻塞/风险/验证证据、最终审计问题报告 | reviewer approved 不等于 human_approved；确认前不得关闭/提交最终完成 | 满足 |
| 12. 本地提交 | `gitcommitzh` | human approval、ledger、review/evidence/memory sync、当前任务 diff | 审查范围、只暂存当前任务范围、生成中文 commit、执行本地 commit | 真实 commit hash、提交信息、纳入/未纳入文件说明 | 不用 `git add .` 扩范围；本地 commit 不替代 review/verification/human confirmation | 满足 |
| 13. 远端 PR / push / merge handoff | `using-shanforge` 判断 gate；远端执行 owner 为 Git/GitHub workflow、Codex App、`gh`/`git push` 或人类 owner | 本地 commit hash、分支、远端、base branch、review/evidence/memory sync、human_approved | 判断可进入 handoff；远端工具执行或输出 blocked/failed/conflict/checks_failed | `remote_handoff_ready` / `remote_push_done` / `remote_pr_opened` / `remote_merge_done` 等状态和远端 evidence | 无 PR URL、commit hash、工具结果不得声明远端完成；`gitcommitzh` 不负责远端 | 满足；本轮未执行真实远端动作 |
| 14. 压缩恢复和 idempotency | `project-memory` + `using-shanforge` | 会话卡、ledger、review ledger、evidence、summary | 重读最新事件，跳过 done/approved/passed 或相同 idempotency 动作 | 恢复状态、排除项、blocker 或下一动作 | ledger/git/evidence 优先于对话记忆 | 基本满足；S4 transcript 的 ledger 读取证据可更明确 |
| 15. S1-S6 dry-run transcript | `using-shanforge` reference 定义契约；评估者记录 transcript | `black-box-flow-eval.md` 的 S1-S6 输入和证据格式 | 逐场景记录 allowed context、observed actions、files、commands、critical assertions、score | `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-4-s1-s6-dry-run-transcript.md` | transcript 只能记录观察事实，不得冒充真实修复/commit/push/PR/merge | 满足；manual dry-run，不是自动黑盒 runner |

## 输出满足性

| step | 输出是否完全满足 Shanforge 要求 | 说明 |
|---|---|---|
| 会话恢复 | 是 | `project-memory` 有读取范围、排除项、ledger/idempotency 和真实事实优先规则。 |
| 意图澄清 / brief | 是 | `brainstorming` 有标准状态包和 `needs`，且明确不做路由决策。 |
| 需求 / AC / NFR | 是 | `requirements-engineering` 有需求状态、产物、evidence、ledger_event 和 no self-approval。 |
| 设计 / 文档 / 边界 | 是 | `document-templates` 已补 `work_item` / `ledger_event`；辅助 skill 不阻塞主闭环。 |
| 实施计划 / task brief | 是 | plan、task brief、review handoff、evidence、ledger_event 齐全。 |
| 执行 / evidence / report / ledger | 是 | inline 和 subagent 执行路径都有 evidence/report/review checkpoint/ledger。 |
| Bug 修复 / TDD / 根因 | 是 | 复现、根因、Red/Green、回归和禁止兜底规则齐全。 |
| 完成前验证 | 是 | 要求新鲜完整命令、完整输出、exit code、失败/跳过/未运行统计。 |
| 独立 review / scoring | 是 | 已补标准状态包，保留独立 reviewer 和 pending_human_confirmation gate。 |
| review 反馈处理 | 是 | 已补标准状态包；逐条 triage/response/verification 契约齐全。 |
| 人工确认门 | 是 | 确认包必须包含最终审计问题报告、评分、阻塞、风险和验证证据。 |
| 本地提交 | 是 | 只负责本地 commit，要求真实 hash 和范围审查。 |
| 远端 PR / push / merge handoff | 是 | handoff reference 定义 owner、输入、工具、evidence、失败语义和状态词。 |
| 压缩恢复 / idempotency | 基本是 | 规则满足；S4 transcript 应把 ledger 文件/命令列得更实。 |
| S1-S6 dry-run transcript | 是 | 6 个场景字段齐全，总分 35/36，normalized 97，无 `[0/2]`。 |

## Findings

### Critical

无。

### Important

无。

### Minor

1. S1-S6 transcript 的 S4/S5 场景声明检查了 ledger / review ledger，但 `Files read` 和 `Commands run` 没有显式列出 `.factory/workitems/SKILL-FLOW-AUDIT-001/ledger.jsonl` 或 `.factory/memory/review-ledger.jsonl`。这不推翻流程覆盖结论，但下一轮 transcript 应把 ledger 读取证据写全。
2. `doc-coauthoring` 和 `ui-ux-pro-max` 仍是通用 `done` / `blocked` 输出；当前由 `document-templates` 承担正式文档/设计闭环 owner，所以不阻塞。若后续让它们直接作为 Shanforge work item owner，应补同样的 `work_item/status/outputs/evidence/ledger_event/needs` 状态包。

## 验证命令和真实结果

### 1. 相关 workflow pytest

```bash
PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/shanforge-uv-cache uv run pytest -p no:cacheprovider tests/test_review_workflow_skills.py tests/test_skill_flow_process_audit.py tests/test_bug_fix_root_cause_skill_rules.py tests/test_browser_control_skill.py tests/test_crawler4j_model_skill_integration.py tests/test_sf_sp_010_documentation_navigation.py tests/test_black_box_workflow_eval.py tests/test_pr_commit_workflow_rules.py tests/test_project_memory_skill.py tests/test_writing_plans_skill.py tests/test_requirements_engineering_skill.py tests/test_brainstorming_skill.py tests/test_execution_workflow_skills.py tests/test_verification_debugging_workflow_skills.py tests/test_independent_review_gate.py
```

真实结果：

```text
exit code: 0
collected 84 items
84 passed in 0.08s
```

### 2. 相关 workflow ruff

```bash
PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/shanforge-uv-cache uv run ruff check --no-cache tests/test_review_workflow_skills.py tests/test_skill_flow_process_audit.py tests/test_bug_fix_root_cause_skill_rules.py tests/test_browser_control_skill.py tests/test_crawler4j_model_skill_integration.py tests/test_sf_sp_010_documentation_navigation.py tests/test_black_box_workflow_eval.py tests/test_pr_commit_workflow_rules.py tests/test_project_memory_skill.py tests/test_writing_plans_skill.py tests/test_requirements_engineering_skill.py tests/test_brainstorming_skill.py tests/test_execution_workflow_skills.py tests/test_verification_debugging_workflow_skills.py tests/test_independent_review_gate.py
```

真实结果：

```text
exit code: 0
All checks passed!
```

### 3. 旧中心 gate / 旧远端脚本禁词扫描

```bash
rg -n 'factory-dispatch loop-gate|factory-workitem-loop-gate|scripts/factory-workitem-loop-gate|factory-pr-remote-open|factory-pr-remote-merge|REQUIRED NEXT SKILL|finishing-a-development-branch|docs/superpowers' skills/using-shanforge/SKILL.md skills/using-shanforge/references/black-box-flow-eval.md skills/using-shanforge/references/remote-pr-handoff.md .factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-4-s1-s6-dry-run-transcript.md skills/project-memory/SKILL.md skills/brainstorming/SKILL.md skills/requirements-engineering/SKILL.md skills/document-templates/SKILL.md skills/doc-coauthoring/SKILL.md skills/ui-ux-pro-max/SKILL.md skills/writing-plans/SKILL.md skills/executing-plans/SKILL.md skills/subagent-driven-development/SKILL.md skills/systematic-debugging/SKILL.md skills/tdd-workflow/SKILL.md skills/ai-regression-testing/SKILL.md skills/verification-before-completion/SKILL.md skills/requesting-code-review/SKILL.md skills/receiving-code-review/SKILL.md skills/gitcommitzh/SKILL.md
```

真实结果：

```text
exit code: 1
无输出；未命中旧中心 gate、旧远端脚本或旧 superpowers 引用。
```

### 4. S1-S6 transcript 字段扫描

```bash
rg -n 'Scenario:|SF-SP-009-S1|SF-SP-009-S2|SF-SP-009-S3|SF-SP-009-S4|SF-SP-009-S5|SF-SP-009-S6|Observed actions:|Files read:|Files written:|Commands run:|Critical assertions:|Actual score:|Max score:|Normalized score:|Failure reason:' .factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-4-s1-s6-dry-run-transcript.md
```

真实结果：

```text
exit code: 0
6 个场景均命中必需字段；总体记录为 Overall actual score 35 / Overall max score 36 / Overall normalized score 97。
S2 为 5/6，因为输入未给具体失败命令；没有 `[0/2]` 断言。
```

### 5. 标准状态包字段扫描

```bash
rg -n '工作结果：|- work_item:|- skill:|- status:|- outputs:|- evidence:|- ledger_event:|- needs:' skills/brainstorming/SKILL.md skills/requirements-engineering/SKILL.md skills/document-templates/SKILL.md skills/writing-plans/SKILL.md skills/executing-plans/SKILL.md skills/subagent-driven-development/SKILL.md skills/systematic-debugging/SKILL.md skills/tdd-workflow/SKILL.md skills/ai-regression-testing/SKILL.md skills/verification-before-completion/SKILL.md skills/requesting-code-review/SKILL.md skills/receiving-code-review/SKILL.md skills/using-shanforge/SKILL.md
```

真实结果：

```text
exit code: 0
核心 workflow skills 均命中标准状态包字段；`document-templates`、`requesting-code-review`、`receiving-code-review` 已命中 `work_item`、`status`、`outputs`、`evidence`、`ledger_event`、`needs`。
```

### 6. 远端 handoff 边界扫描

```bash
rg -n 'remote_handoff_ready|remote_handoff_blocked|remote_push_done|remote_pr_opened|remote_pr_updated|remote_merge_done|remote_failed|remote_conflict|remote_checks_failed|PR URL|commit hash|禁止把本地 commit|禁止把本地提交|gitcommitzh.*不负责' skills/using-shanforge/SKILL.md skills/using-shanforge/references/remote-pr-handoff.md skills/gitcommitzh/SKILL.md tests/test_pr_commit_workflow_rules.py
```

真实结果：

```text
exit code: 0
命中 `using-shanforge` 远端 handoff gate、`remote-pr-handoff.md` 状态词/evidence/禁止冒充规则、`gitcommitzh` 不负责远端 PR / push / merge，以及对应测试断言。
```

### 7. 工作区状态观察

```bash
git status --short
```

真实结果：

```text
exit code: 0
 M .factory/workitems/SKILL-FLOW-AUDIT-001/ledger.jsonl
?? .factory/workitems/SKILL-FLOW-AUDIT-001/reviews/iteration-4-fixes-independent-review.md
?? .factory/workitems/SKILL-FLOW-AUDIT-001/task-briefs/chinese-language-review-iteration-5.md
?? .factory/workitems/SKILL-FLOW-AUDIT-001/task-briefs/prompt-engineering-review-iteration-5.md
?? .factory/workitems/SKILL-FLOW-AUDIT-001/task-briefs/skill-flow-completeness-test-iteration-5.md
```

说明：这些是本轮写入 review 前已存在的工作区事实。本测试未 revert、未整理、未提交这些改动。

## 相对 iteration-4 的变化

- 总分：89 -> 96。
- 结论：`changes_requested` -> `passed`。
- Critical：1 -> 0。S1-S6 dry-run transcript 已存在，字段齐全，总分 35/36，normalized 97。
- Important：3 -> 0。远端 PR / push / merge handoff 已有 owner、输入、evidence、失败语义和状态词；review 相关 skill 已补标准状态包；`document-templates` 已补 `work_item` / `ledger_event`。
- Minor：3 -> 2。遗留问题从流程缺口降为 transcript 证据精细度和辅助 skill 直接 owner 一致性问题。
- pytest：iteration-4 为 84 passed；本轮仍为 84 passed。
- ruff：iteration-4 通过；本轮继续通过。
- 远端边界：从“只有禁止冒充”变为“有 handoff 契约”，但本轮仍未执行真实远端 push / PR / merge。

## 最小下一步修复清单

1. 更新 S1-S6 transcript 的 S4/S5，把实际 ledger / review ledger 读取文件和命令列全；不需要新增脚本。
2. 若要让 `doc-coauthoring` 或 `ui-ux-pro-max` 直接承担 Shanforge work item owner，再补标准 `工作结果` 状态包；否则继续让 `document-templates` / `using-shanforge` 包装即可。
3. 暂不建设自动黑盒 agent runner；当前结构测试 + manual dry-run 已覆盖本轮风险。等 dry-run 成本或误判率变高，再考虑自动化。
