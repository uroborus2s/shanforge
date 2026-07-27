# Skill Flow Completeness Test Iteration 6

- work_item: `SKILL-FLOW-AUDIT-001`
- role: Skill 流程测试工程师
- status: passed
- scanned_skill_count: 36
- total_score: 97 / 100
- Critical: 0
- Important: 0
- Minor: 2

## 结论

当前 36 个 `skills/*/SKILL.md` 中，Shanforge 软件开发闭环的 15 个步骤均已有 owner、input、action、output、gate、失败语义和证据要求。iteration-5 independent review 标记已修复的问题在当前文件中保持成立：S1-S6 dry-run transcript 的 S4/S5 已显式列出 work item ledger 和 review ledger 读取证据；远端 PR / push / merge handoff 仍有独立契约；核心闭环 skill 均有标准状态包。

本轮不声明真实代码修复、commit、push、PR 或 merge 已执行；只记录流程测试和真实验证结果。

## Flow Matrix

| step | owner skill | input | action | output | gate | assessment |
|---|---|---|---|---|---|---|
| 1. 会话恢复 | `project-memory`；子 agent 执行特定任务时忽略 `using-shanforge` 总控 | 当前对话、`.factory/memory/agent-session.md`、work item ledger、必要 summary | 最小读取、恢复阶段/work item、按 ledger 防重复 | 会话卡、已读/排除、禁止动作、待决事项、必要 ledger/memory 更新 | 不散读 docs；正式事实和 ledger 优先；相同 idempotency 不重复 | 满足 |
| 2. 意图澄清 / brief | `brainstorming` | 用户意图、会话卡、work item brief、ledger | 一次一个问题、方案比较、收敛 brief 或设计输入 | `工作结果` 状态包、brief、approval、outputs、evidence、ledger_event、needs | 只回写状态，不决定下一步 skill；作者不得自批 approved/done | 满足 |
| 3. 需求 / AC / NFR | `requirements-engineering` | 已批准 brief、必要事实源、baseline 影响 | 写用户故事、REQ、AC、NFR、非目标、风险、baseline 影响 | `requirements_ready` / `ready_for_review` 状态包、产物、evidence、ledger_event | reviewer approved 和 human_approved 前不得把需求写成已批准 | 满足 |
| 4. 设计 / 文档 / 边界 | `document-templates`；辅助 `doc-coauthoring` / `ui-ux-pro-max` | 已批准需求/设计输入、正式 docs 事实、目标读者和边界 | 创建/更新正式文档、维护 docs-stratego、同步索引/版本历史 | 标准状态包、docs、校验证据、ledger_event | 不恢复旧 factory 脚本；不批量制造空壳；事实冲突先回源 | 满足 |
| 5. 美术方向 / 资源包 | `art-asset-pipeline` | 美术方向、平台、尺寸、资源类型、用户确认记录 | 先候选图，再清单，再资源包；清理未确认 `tmp/` | `art-direction.md`、`sprite-spec.md`、`manifest.json`、preview、标准状态包 | 用户确认方向前不得进入清单；确认清单前不得生产最终包；不自批 approved | 满足；这是 iteration-5 后新增覆盖面 |
| 6. 实施计划 / task brief | `writing-plans` | 已批准 spec/需求/设计/work item brief | 锁定文件范围、拆任务、写 Red/Green/review/memory sync | plan、task briefs、review handoff、evidence、ledger_event、状态包 | 计划只能到 `ready_for_review`；approved 来自 review | 满足 |
| 7. 执行 / evidence / report / ledger | `subagent-driven-development` 或 `executing-plans` | approved plan、task brief、ledger、允许文件范围 | 执行任务、生成 evidence/report/review input、必要 memory sync | evidence、implementer report、review checkpoint、ledger_event、状态包 | 实现者不得自批；缺 evidence/report/review checkpoint 不得 ready | 满足 |
| 8. Bug 修复 / TDD / 根因 | `systematic-debugging` + `tdd-workflow` + `ai-regression-testing` | 失败输出、exit code、复现步骤、调用链、相关测试 | 先复现和根因，再 Red/Green、根因修复和回归 | 根因记录、red/green evidence、回归测试、ledger_event、状态包 | 根因报告获确认前不得修；根因不明只能加诊断 | 满足；见 Minor-1 |
| 9. 完成前验证 | `verification-before-completion` | 要验证的声明、plan/diff/review、命令或检查项 | 跑本轮新鲜完整命令，读取完整输出和 exit code | verification evidence/report、失败/跳过/未运行统计、ledger_event、状态包 | 没有新鲜证据不得声明完成；review 不能替代 verification | 满足 |
| 10. 独立 review / scoring | `requesting-code-review` | task brief、implementer report、evidence、diff、独立性证据 | Spec Review + Quality Review，评分，记录独立性 | review 文件、review ledger、work item ledger、标准状态包 | same-thread 只能 self_check；approved 必须有独立 reviewer 证据 | 满足 |
| 11. review 反馈处理 | `receiving-code-review` | review feedback、PR 评论、任务评审意见 | 逐条 triage、核实、修复或 pushback，每项验证 | triage、response、fix report、verification evidence、ledger_event、状态包 | 禁止盲改和表演式同意；memory sync 缺失不得完成 | 满足 |
| 12. 人工确认门 | `using-shanforge` | independent review approved、score、ledger/evidence/final audit issue report | 停止并输出人工确认包 | `pending_human_confirmation`、评分、阻塞/风险/验证证据、最终审计问题报告 | reviewer approved 不等于 human_approved；确认前不得关闭/提交最终完成 | 满足 |
| 13. 本地提交 | `gitcommitzh` | human approval、ledger、review/evidence/memory sync、当前任务 diff | 审查范围、只暂存当前任务范围、生成中文 commit、执行本地 commit | 真实 commit hash、提交信息、纳入/未纳入文件说明、状态包 | 不用 `git add .` 扩范围；本地 commit 不替代 review/verification/human confirmation | 满足 |
| 14. 远端 PR / push / merge handoff | `using-shanforge` 判断 gate；远端执行 owner 为 Git/GitHub workflow、Codex App、`gh`/`git push` 或人类 owner | 本地 commit hash、分支、远端、base branch、review/evidence/memory sync、human_approved | 判断可进入 handoff；远端工具执行或输出 blocked/failed/conflict/checks_failed | `remote_handoff_ready` / `remote_push_done` / `remote_pr_opened` / `remote_merge_done` 等状态和远端 evidence | 无 PR URL、commit hash、工具结果不得声明远端完成；`gitcommitzh` 不负责远端 | 满足；本轮未执行真实远端动作 |
| 15. 压缩恢复和 idempotency / S1-S6 dry-run | `project-memory` + `using-shanforge` reference | 会话卡、ledger、review ledger、evidence、S1-S6 输入 | 重读最新事件，跳过 done/approved/passed 或相同 idempotency 动作；逐场景记录 observed actions | 恢复状态、排除项、blocker 或下一动作；dry-run transcript | ledger/git/evidence 优先于对话记忆；transcript 只能记录观察事实 | 满足；S4/S5 ledger 证据已补齐 |

## 输出满足性

| step | 输出是否完全满足 Shanforge 要求 | 说明 |
|---|---|---|
| 会话恢复 | 是 | `project-memory` 有读取范围、排除项、ledger/idempotency 和真实事实优先规则。 |
| 意图澄清 / brief | 是 | `brainstorming` 有标准状态包、批准状态、`needs`，且明确不做路由决策。 |
| 需求 / AC / NFR | 是 | `requirements-engineering` 有需求状态、产物、evidence、ledger_event 和 no self-approval。 |
| 设计 / 文档 / 边界 | 是 | `document-templates` 有正式文档治理、校验、状态包和失败语义。 |
| 美术方向 / 资源包 | 是 | 新增 `art-asset-pipeline` 要求用户确认方向和清单、清理 `tmp/`、记录 imagegen/view_image/preview 证据。 |
| 实施计划 / task brief | 是 | plan、task brief、review handoff、evidence、ledger_event 齐全。 |
| 执行 / evidence / report / ledger | 是 | inline 和 subagent 执行路径都有 evidence/report/review checkpoint/ledger。 |
| Bug 修复 / TDD / 根因 | 是 | 复现、根因、Red/Green、回归和禁止兜底规则齐全。 |
| 完成前验证 | 是 | 要求新鲜完整命令、完整输出、exit code、失败/跳过/未运行统计。 |
| 独立 review / scoring | 是 | 独立 reviewer 证据、score、ledger 和 pending_human_confirmation gate 齐全。 |
| review 反馈处理 | 是 | 逐条 triage/response/verification、ledger 和 memory sync 契约齐全。 |
| 人工确认门 | 是 | 确认包必须包含最终审计问题报告、评分、阻塞、风险和验证证据。 |
| 本地提交 | 是 | 只负责本地 commit，要求真实 hash、范围审查和中文提交信息回显。 |
| 远端 PR / push / merge handoff | 是 | handoff reference 定义 owner、输入、工具、evidence、失败语义和状态词。 |
| 压缩恢复 / S1-S6 dry-run | 是 | S1-S6 字段齐全，总分 35/36，S4/S5 已显式列 ledger 和 review ledger。 |

## Findings

### Critical

无。

### Important

无。

### Minor

1. `using-shanforge` 的 Bug 路由表仍把“发现 Bug 或验证失败”的下一步写成 `tdd-workflow / ai-regression-testing`，状态写成 `fix_ready_for_review`；而根因调查 owner 实际是 `systematic-debugging`，下游 `tdd-workflow` / `ai-regression-testing` 的状态包是 `passed | partial | failed | blocked`。当前总流程仍满足，因为 `fix_bug` 场景规则和调试/TDD skill 都强制根因先行；建议把路由表文字与实际 owner/status 对齐。
2. 全量 36 个 skill 状态包扫描仍发现少数非主闭环 skill 未完全统一：`agent-harness-construction`、`ai-first-engineering`、`article-writing` 缺 `work_item` / `ledger_event` 字段，`project-memory` 使用会话卡格式而非标准 `工作结果` 包。这不阻塞 15 步主闭环，但若目标是所有 skill 都能直接作为 Shanforge work item owner，应补齐或明确豁免。

## 验证命令和真实结果

### 1. 目标报告不存在检查

```bash
test ! -e /Users/uroborus/AiProject/shanforge/.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-completeness-test-iteration-6.md
```

真实结果：

```text
exit code: 0
无输出；目标报告此前不存在，本轮未覆盖旧报告。
```

### 2. skill 扫描

```bash
find /Users/uroborus/AiProject/shanforge/skills -mindepth 2 -maxdepth 2 -name SKILL.md -type f | sort
find /Users/uroborus/AiProject/shanforge/skills -mindepth 2 -maxdepth 2 -name SKILL.md -type f | wc -l
```

真实结果：

```text
exit code: 0
扫描到 36 个 SKILL.md。
新增于 iteration-5 报告之后的当前覆盖面：skills/art-asset-pipeline/SKILL.md。
```

### 3. 定向 workflow pytest

```bash
PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/shanforge-uv-cache uv run pytest -p no:cacheprovider tests/test_review_workflow_skills.py tests/test_skill_flow_process_audit.py tests/test_bug_fix_root_cause_skill_rules.py tests/test_browser_control_skill.py tests/test_crawler4j_model_skill_integration.py tests/test_sf_sp_010_documentation_navigation.py tests/test_black_box_workflow_eval.py tests/test_pr_commit_workflow_rules.py tests/test_project_memory_skill.py tests/test_writing_plans_skill.py tests/test_requirements_engineering_skill.py tests/test_brainstorming_skill.py tests/test_execution_workflow_skills.py tests/test_verification_debugging_workflow_skills.py tests/test_independent_review_gate.py tests/test_stratix_admin_web_skill.py tests/test_stratix_service_skill.py tests/test_task_workflow_semantics.py tests/test_skill_creator_skill_principles.py tests/test_deprecated_skill_cleanup.py tests/test_superpowers_reference_migration.py
```

真实结果：

```text
exit code: 0
collected 121 items
121 passed in 0.10s
```

### 4. 定向 workflow ruff

```bash
PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/shanforge-uv-cache uv run ruff check --no-cache tests/test_review_workflow_skills.py tests/test_skill_flow_process_audit.py tests/test_bug_fix_root_cause_skill_rules.py tests/test_browser_control_skill.py tests/test_crawler4j_model_skill_integration.py tests/test_sf_sp_010_documentation_navigation.py tests/test_black_box_workflow_eval.py tests/test_pr_commit_workflow_rules.py tests/test_project_memory_skill.py tests/test_writing_plans_skill.py tests/test_requirements_engineering_skill.py tests/test_brainstorming_skill.py tests/test_execution_workflow_skills.py tests/test_verification_debugging_workflow_skills.py tests/test_independent_review_gate.py tests/test_stratix_admin_web_skill.py tests/test_stratix_service_skill.py tests/test_task_workflow_semantics.py tests/test_skill_creator_skill_principles.py tests/test_deprecated_skill_cleanup.py tests/test_superpowers_reference_migration.py
```

真实结果：

```text
exit code: 0
All checks passed!
```

### 5. 旧中心 gate / 旧远端脚本禁词扫描

```bash
rg -n 'factory-dispatch loop-gate|factory-workitem-loop-gate|scripts/factory-workitem-loop-gate|factory-pr-remote-open|factory-pr-remote-merge|REQUIRED NEXT SKILL|finishing-a-development-branch|docs/superpowers' /Users/uroborus/AiProject/shanforge/skills /Users/uroborus/AiProject/shanforge/.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-4-s1-s6-dry-run-transcript.md
```

真实结果：

```text
exit code: 1
无输出；未在 skills 或 S1-S6 transcript 中命中旧中心 gate、旧远端脚本或旧 superpowers 引用。
```

### 6. S1-S6 transcript 字段扫描

```bash
rg -n 'Scenario:|SF-SP-009-S1|SF-SP-009-S2|SF-SP-009-S3|SF-SP-009-S4|SF-SP-009-S5|SF-SP-009-S6|Observed actions:|Files read:|Files written:|Commands run:|Critical assertions:|Actual score:|Max score:|Normalized score:|Failure reason:|Overall actual score|Overall max score|Overall normalized score|ledger.jsonl|review-ledger.jsonl' /Users/uroborus/AiProject/shanforge/.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-4-s1-s6-dry-run-transcript.md
```

真实结果：

```text
exit code: 0
6 个场景均命中必需字段。
Overall actual score: 35
Overall max score: 36
Overall normalized score: 97
S4/S5 均显式列出 .factory/workitems/SKILL-FLOW-AUDIT-001/ledger.jsonl 和 .factory/memory/review-ledger.jsonl 的读取路径与 tail 命令。
```

### 7. 标准状态包字段扫描

```bash
rg -n '工作结果：|- work_item:|- skill:|- status:|- outputs:|- evidence:|- ledger_event:|- needs:' /Users/uroborus/AiProject/shanforge/skills/brainstorming/SKILL.md /Users/uroborus/AiProject/shanforge/skills/requirements-engineering/SKILL.md /Users/uroborus/AiProject/shanforge/skills/document-templates/SKILL.md /Users/uroborus/AiProject/shanforge/skills/art-asset-pipeline/SKILL.md /Users/uroborus/AiProject/shanforge/skills/writing-plans/SKILL.md /Users/uroborus/AiProject/shanforge/skills/executing-plans/SKILL.md /Users/uroborus/AiProject/shanforge/skills/subagent-driven-development/SKILL.md /Users/uroborus/AiProject/shanforge/skills/systematic-debugging/SKILL.md /Users/uroborus/AiProject/shanforge/skills/tdd-workflow/SKILL.md /Users/uroborus/AiProject/shanforge/skills/ai-regression-testing/SKILL.md /Users/uroborus/AiProject/shanforge/skills/verification-before-completion/SKILL.md /Users/uroborus/AiProject/shanforge/skills/requesting-code-review/SKILL.md /Users/uroborus/AiProject/shanforge/skills/receiving-code-review/SKILL.md /Users/uroborus/AiProject/shanforge/skills/gitcommitzh/SKILL.md /Users/uroborus/AiProject/shanforge/skills/using-shanforge/SKILL.md
```

真实结果：

```text
exit code: 0
核心 15 步 owner skills 均命中标准状态包字段；新增 art-asset-pipeline 也命中 work_item/status/outputs/evidence/ledger_event/needs。
```

### 8. 全量状态包缺口扫描

```bash
for f in /Users/uroborus/AiProject/shanforge/skills/*/SKILL.md; do b=$(basename "$(dirname "$f")"); missing=""; rg -q '工作结果：' "$f" || missing="$missing 工作结果"; rg -q 'work_item:' "$f" || missing="$missing work_item"; rg -q 'status:' "$f" || missing="$missing status"; rg -q 'outputs:' "$f" || missing="$missing outputs"; rg -q 'evidence:' "$f" || missing="$missing evidence"; rg -q 'ledger_event:' "$f" || missing="$missing ledger_event"; rg -q 'needs:' "$f" || missing="$missing needs"; if [ -n "$missing" ]; then printf '%s:%s\n' "$b" "$missing"; fi; done
```

真实结果：

```text
exit code: 0
agent-harness-construction: work_item ledger_event
ai-first-engineering: work_item ledger_event
article-writing: work_item ledger_event
project-memory: 工作结果 work_item status outputs evidence ledger_event needs
```

### 9. 远端 handoff 边界扫描

```bash
rg -n 'remote_handoff_ready|remote_handoff_blocked|remote_push_done|remote_pr_opened|remote_pr_updated|remote_merge_done|remote_failed|remote_conflict|remote_checks_failed|PR URL|commit hash|禁止把本地 commit|禁止把本地提交|gitcommitzh.*不负责' /Users/uroborus/AiProject/shanforge/skills/using-shanforge/SKILL.md /Users/uroborus/AiProject/shanforge/skills/using-shanforge/references/remote-pr-handoff.md /Users/uroborus/AiProject/shanforge/skills/gitcommitzh/SKILL.md /Users/uroborus/AiProject/shanforge/tests/test_pr_commit_workflow_rules.py
```

真实结果：

```text
exit code: 0
命中 using-shanforge 远端 handoff gate、remote-pr-handoff 状态词/evidence/禁止冒充规则、gitcommitzh 不负责远端 PR / push / merge，以及对应测试断言。
```

### 10. 工作区状态观察

```bash
git status --short
```

真实结果：

```text
exit code: 0
工作区在本轮写报告前已有大量修改和新增文件，包括 .factory/memory、SKILL-FLOW-AUDIT-001 evidence/reports/reviews/task-briefs、多个 skills/*/SKILL.md、tests/*，以及新增 skills/art-asset-pipeline/ 和 tests/test_task_workflow_semantics.py。
本测试未 revert、未清理、未提交这些改动。
```

## 相对 iteration-5 的变化

- 扫描数量：35 -> 36。新增 `skills/art-asset-pipeline/SKILL.md`，并已被 `using-shanforge` 路由表纳入“美术方向或开发资源包”场景。
- Flow completeness：iteration-5 为 96 / 100，本轮为 97 / 100。
- Critical：0 -> 0。
- Important：0 -> 0。
- Minor：2 -> 2，但内容变化。iteration-5 的 S4/S5 ledger 证据缺口和 `doc-coauthoring` / `ui-ux-pro-max` 状态包缺口已按 independent review 结论修复；本轮剩余为 Bug route wording/status 对齐和少数非主闭环 skill 状态包统一问题。
- S1-S6 transcript：保持 35/36，normalized 97；S4/S5 已显式列出 ledger 和 review-ledger 文件及命令。
- 定向 pytest：iteration-5 报告为 84 passed，iteration-5 independent review 为 54 passed；本轮相关测试扩展到 121 passed，覆盖新增 task workflow semantics。
- ruff：继续通过。
- 远端边界：仍只验证 handoff 契约；本轮未执行真实 push / PR / merge。

## 最小下一步修复清单

1. 对齐 `using-shanforge` Bug 路由表：把 `systematic-debugging` 明确列为根因调查 owner，并把 `fix_ready_for_review` 改成与下游状态包一致的状态或说明它是汇总状态。
2. 决定是否要求所有 36 个 skill 都能直接作为 Shanforge work item owner。若是，给 `agent-harness-construction`、`ai-first-engineering`、`article-writing` 补 `work_item` / `ledger_event`；若否，在这些 skill 或流程总控中明确它们是辅助输出格式。
3. 明确 `project-memory` 是否豁免标准 `工作结果` 状态包。若不豁免，添加一个很短的 `session_ready | blocked | needs_user_input` 状态包；若豁免，保留当前会话卡格式即可。
