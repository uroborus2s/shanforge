# Skill Flow Completeness Test Iteration 3

## 结论

- status: DONE
- 总评分：86 / 100
- Critical：1
- Important：3
- Minor：3
- blocked: false

当前 workflow skills 覆盖 Shanforge 本地开发闭环：会话恢复、意图澄清、需求、设计/文档、计划、执行、根因/TDD、完成前验证、独立 review、review 反馈、人工确认和本地提交都有 owner、输入、输出和 gate。iteration-2 后语言/提示修复让 `tdd-workflow`、`ai-regression-testing` 和 `document-templates` 的输出契约更接近统一状态回写。

不能声明“完整软件开发流程已真实验证”。原因没变：当前仍只有 skill 文本、结构测试和修复验证，没有 S1-S6 黑盒行为回放 transcript；远端 PR / push / merge 仍只有边界声明，没有 Shanforge owner 与 evidence 契约；相关 pytest 仍有 1 个旧断言失败。

## 流程矩阵

| 步骤 | owner skill | 输入 | 动作 | 输出 | gate | 评估 |
|---|---|---|---|---|---|---|
| 1. 会话恢复 | `using-shanforge` + `project-memory` | 当前对话、会话卡、`.factory/memory/agent-session.md`、work item ledger | 最小读取、恢复阶段和 work item、判断已完成动作 | 会话卡、已读/排除、禁止动作、待决事项 | 不散读 docs；ledger/idempotency 防重复 | 完全满足静态契约 |
| 2. 意图澄清 / brief | `brainstorming` | 用户意图、会话卡、brief/ledger | 一次一个问题、方案比较、形成 brief | `brief.md`、approval、outputs、evidence、ledger_event、needs | 工作 skill 只回写状态，不决定下一步 | 完全满足 |
| 3. 需求 / AC / NFR | `requirements-engineering` | 已批准 brief、ledger、必要 summary | 写用户故事、REQ、AC、NFR、非目标和风险 | brief/PRD、memory summary、ledger、状态包 | 未确认需求不得进入计划/实现；不得写 approved/done | 完全满足 |
| 4. 设计 / 文档 / 边界 | `document-templates`，必要时 `doc-coauthoring` / `ui-ux-pro-max` | 已批准需求/设计输入、docs 事实、项目暴露面 | 维护 4 大模块 docs、边界、技术设计和校验 | docs 文档、docs-stratego 校验、状态包 | 不调用旧 factory 脚本；只生成会用的文档 | 基本满足；状态包仍缺 `work_item` / `ledger_event` |
| 5. 实施计划 / task brief | `writing-plans` | 已批准 spec/需求/设计/brief | 锁定文件结构，拆 Red/Green/review/memory sync | `plan.md`、`task-briefs/`、review handoff、ledger | 计划只能到 `ready_for_review`；approved 来自 review | 完全满足 |
| 6. 执行 / evidence / report / ledger | `subagent-driven-development` 或 `executing-plans` | approved plan、task brief、ledger、evidence/reports/reviews | 按任务执行、写 evidence/report/review input、同步 memory | evidence、reports、review input、ledger、状态包 | 实现者不得自批、不得自动 commit、不得跳过 review | 完全满足 |
| 7. Bug 修复 / TDD / 根因 | `systematic-debugging` + `tdd-workflow` + `ai-regression-testing` | 失败输出、复现步骤、调用链、相关测试 | 先复现和根因，再红绿测试、最小修复和回归 | 根因报告、red/green evidence、ledger、状态包 | 禁止兜底式修复；根因不明只能加诊断 | 完全满足，较 iteration-2 改善 |
| 8. 完成前验证 | `verification-before-completion` | 要验证的声明、plan/diff/review、命令 | 跑新鲜完整命令，读输出和 exit code，统计失败/跳过 | verification report、evidence、ledger、状态包 | 无新鲜证据不得声明完成 | 完全满足 |
| 9. 独立 review / scoring | `requesting-code-review` | task brief、report、evidence、diff、review ledger | Spec Review + Quality Review，记录独立性和评分 | review 文件、review ledger、work item ledger | same-thread 只能 self_check；approved 必须有独立证据 | 完全满足 |
| 10. review 反馈处理 | `receiving-code-review` | review comments、PR comments、task review | 逐条 triage、核实、修复/pushback、逐项验证 | triage、response、fix report、verification evidence、memory sync | 禁止盲改和表演式同意；每项修复后验证 | 基本满足；缺统一状态包模板 |
| 11. 人工确认门 | `using-shanforge` | independent review approved、score、ledger/evidence | 停止并输出确认包，等待用户确认 | `pending_human_confirmation`、确认包 | reviewer approved 不等于 human_approved | 完全满足 |
| 12. 本地提交 | `gitcommitzh` | human approval、ledger、review/evidence/memory、diff | 审查范围、中文说明、只提交当前任务范围、本地 commit | commit message、真实 hash、纳入文件列表 | 不用 `git add .` 扩范围；commit 不冒充 PR/push/merge | 完全满足 |
| 13. 远端 PR / push / merge 边界 | 无固定 Shanforge owner；`gitcommitzh` 明确不负责 | 本地提交、远端目标、PR 状态 | 当前只做边界声明和禁止冒充 | 无固定远端 evidence/status 契约 | 禁止把本地 commit 说成远端 PR/push/merge | 不满足完整闭环；边界清楚 |
| 14. 压缩恢复和 idempotency | `project-memory` + `using-shanforge` | 会话卡、ledger、git/evidence、summary | 读取最新事件，跳过 done/approved/passed 或相同 idempotency | 恢复状态、排除项、下一未完成动作/blocker | ledger/git/evidence 优先于对话记忆 | 静态契约满足；未做真实恢复回放 |

## 输出满足性

| 步骤 | 输出是否完全满足 Shanforge 要求 | 说明 |
|---|---|---|
| 会话恢复 | 是 | 最小读取、排除项、ledger/idempotency 和禁止动作齐全。 |
| 意图澄清 / brief | 是 | 状态包和 `needs` 已明确不做路由决策。 |
| 需求 / AC / NFR | 是 | 已有 PRD/brief、ledger、memory 和状态边界。 |
| 设计 / 文档 / 边界 | 基本是 | `document-templates` 有状态包，但缺 `work_item` 和 `ledger_event` 字段；`doc-coauthoring` 仍偏通用文档协作。 |
| 实施计划 / task brief | 是 | 计划、task brief、验证策略、review handoff 齐全。 |
| 执行 / evidence / report / ledger | 是 | evidence/report/review input/ledger/memory sync 齐全。 |
| Bug 修复 / TDD / 根因 | 是 | `tdd-workflow` 和 `ai-regression-testing` 已补输出契约。 |
| 完成前验证 | 是 | 新鲜命令、exit code、失败/跳过/未运行统计齐全。 |
| 独立 review / scoring | 是 | 独立性元数据、score rubric、same-thread 限制齐全。 |
| review 反馈处理 | 基本是 | 输出路径和 memory sync 齐全，但没有统一 `工作结果` 状态包。 |
| 人工确认门 | 是 | `pending_human_confirmation` 和确认包明确。 |
| 本地提交 | 是 | 提交范围、human approval、真实 hash 和远端边界明确。 |
| 远端 PR / push / merge | 否 | 只有禁止冒充边界，没有 owner、状态、evidence 和 gate。 |
| 压缩恢复 / idempotency | 基本是 | 静态契约完整；缺真实恢复 dry-run transcript。 |

## Findings

### Critical

1. 没有真实行为回放证据。`black-box-flow-eval.md` 定义了 S1-S6，但 work item evidence 下没有 `Scenario:`、`Observed actions:`、`Actual score:` 等 transcript 字段。结构测试只能证明契约存在，不能证明代理真实遵守流程。

### Important

1. 远端 PR / push / merge 没有 Shanforge owner。`gitcommitzh` 正确只做本地提交并禁止冒充远端状态；但完整远端闭环仍缺 owner、输入、状态、evidence 和 gate。
2. 相关 workflow pytest 仍不全绿。`tests/test_black_box_workflow_eval.py::test_workflow_plan_tracks_sf_sp_009_development_scope` 仍期待旧短语“当前已进入黑盒流程 eval 开发”，而当前计划文档写的是 `SF-SP-009` 本地闭环完成。
3. 状态包一致性还没完全收口。`tdd-workflow` 已修好；但 `receiving-code-review` 缺显式 `工作结果` 模板，`document-templates` 状态包缺 `work_item` / `ledger_event`，`doc-coauthoring` 仍是通用 `done/blocked` 契约。

### Minor

1. 当前相关 tests 主要是结构/短语断言，不是流程行为回放；适合防回归，但不能替代黑盒 dry-run。
2. `doc-coauthoring` 作为辅助 skill 可以接受，但若作为正式设计/文档 owner 使用，需要补 Shanforge 状态字段。
3. 黑盒计划测试绑定临时状态文案，容易在文档状态更新后误报；应改成语义断言。

## 验证命令和真实结果

### 1. 相关 workflow pytest

```bash
uv run pytest -p no:cacheprovider tests/test_bug_fix_root_cause_skill_rules.py tests/test_verification_debugging_workflow_skills.py tests/test_pr_commit_workflow_rules.py tests/test_execution_workflow_skills.py tests/test_deprecated_skill_cleanup.py tests/test_stratix_service_skill.py tests/test_skill_creator_skill_principles.py tests/test_skill_flow_process_audit.py tests/test_review_workflow_skills.py tests/test_project_memory_skill.py tests/test_writing_plans_skill.py tests/test_requirements_engineering_skill.py tests/test_brainstorming_skill.py tests/test_independent_review_gate.py tests/test_black_box_workflow_eval.py
```

真实结果：

```text
exit code: 1
collected 75 items
74 passed
1 failed: tests/test_black_box_workflow_eval.py::test_workflow_plan_tracks_sf_sp_009_development_scope
失败原因：断言期待 "`SF-SP-009`：当前已进入黑盒流程 eval 开发"，当前计划文档未包含该旧状态短语。
```

### 2. 相关 workflow ruff

```bash
uv run ruff check --no-cache tests/test_bug_fix_root_cause_skill_rules.py tests/test_verification_debugging_workflow_skills.py tests/test_pr_commit_workflow_rules.py tests/test_execution_workflow_skills.py tests/test_deprecated_skill_cleanup.py tests/test_stratix_service_skill.py tests/test_skill_creator_skill_principles.py tests/test_skill_flow_process_audit.py tests/test_review_workflow_skills.py tests/test_project_memory_skill.py tests/test_writing_plans_skill.py tests/test_requirements_engineering_skill.py tests/test_brainstorming_skill.py tests/test_independent_review_gate.py tests/test_black_box_workflow_eval.py
```

真实结果：

```text
exit code: 0
All checks passed!
```

### 3. 工作 skill 旧 gate / 自选路由禁词扫描

```bash
rg -n 'factory-dispatch loop-gate|factory-workitem-loop-gate|scripts/factory-|REQUIRED NEXT SKILL|下一步 skill：|给出下一步 skill|只调用 `writing-plans`|finishing-a-development-branch|docs/superpowers' skills/project-memory/SKILL.md skills/brainstorming/SKILL.md skills/requirements-engineering/SKILL.md skills/document-templates/SKILL.md skills/doc-coauthoring/SKILL.md skills/writing-plans/SKILL.md skills/executing-plans/SKILL.md skills/subagent-driven-development/SKILL.md skills/systematic-debugging/SKILL.md skills/tdd-workflow/SKILL.md skills/ai-regression-testing/SKILL.md skills/requesting-code-review/SKILL.md skills/receiving-code-review/SKILL.md skills/gitcommitzh/SKILL.md skills/verification-before-completion/SKILL.md
```

真实结果：

```text
exit code: 1
无输出；工作 skill 主文件未命中旧中心 gate 或自选下一步 skill 禁词。
```

### 4. 黑盒回放 evidence 扫描

```bash
rg -n "Scenario:|SF-SP-009-S1|SF-SP-009-S2|SF-SP-009-S3|SF-SP-009-S4|SF-SP-009-S5|SF-SP-009-S6|Observed actions:|Actual score:|Normalized score:" .factory/workitems/SKILL-FLOW-AUDIT-001/evidence
```

真实结果：

```text
exit code: 1
无输出；未发现 S1-S6 黑盒行为回放 evidence。
```

## 相对 iteration-2 的变化

- 总分：82 -> 86。
- Critical：1 -> 1，未变化；真实黑盒行为回放仍缺。
- Important：4 -> 3；`tdd-workflow` 输出契约已补齐，`document-templates` 有了最小状态包，但状态包一致性仍未完全关闭。
- 验证结果：iteration-2 相关结构测试是 60 passed / 1 failed；本轮扩大到 75 个相关测试后是 74 passed / 1 failed。失败用例仍是同一个黑盒计划旧断言。
- 远端边界：未变化；仍只能声明“本地闭环完成”，不能声明 PR/push/merge 完成。

## 最小下一步修复清单

1. 写一份真实 S1-S6 dry-run transcript 到 `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/`，按 `black-box-flow-eval.md` 记录 allowed context、observed actions、files read/written、commands、score 和 failure reason；不要新增中心脚本。
2. 修复 `tests/test_black_box_workflow_eval.py` 的旧状态断言，改成验证当前语义：存在 S1-S6、评分门、`SF-SP-009` 本地闭环口径和远端未闭环边界。
3. 给 `receiving-code-review` 补统一 `工作结果` 状态包；把 `document-templates` 和需要时的 `doc-coauthoring` 补齐 `work_item` / `ledger_event`。
4. 为远端 PR / push / merge 定义最小 handoff 契约：owner、输入、evidence、状态和禁止冒充规则；不要塞进 `gitcommitzh`。
