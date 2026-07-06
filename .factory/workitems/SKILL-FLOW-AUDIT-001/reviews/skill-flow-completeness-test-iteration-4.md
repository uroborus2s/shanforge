# Skill Flow Completeness Test Iteration 4

## 结论

- status: changes_requested
- 总评分：89 / 100
- Critical：1
- Important：3
- Minor：3
- blocked: false

当前 workflow skills 已能静态覆盖 Shanforge 本地软件开发闭环：会话恢复、brief、需求、设计/文档、计划、执行、Bug 根因/TDD、完成前验证、独立 review、review 反馈、人工确认和本地提交都有 owner、输入、动作、输出和 gate。相对 iteration-3，相关 pytest 已从 `74 passed / 1 failed` 提升到 `84 passed`，旧黑盒计划断言失败已修复。

不能声明“完整软件开发流程已真实验证”。原因仍是：`.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/` 下没有可审计的 S1-S6 行为回放 transcript；远端 PR / push / merge 仍只有边界声明和禁止冒充规则，没有 Shanforge owner、状态、evidence 和 gate；少数辅助/评审类 skill 的状态包仍未完全统一。

## Flow matrix

| step | owner skill | input | action | output | gate | assessment |
|---|---|---|---|---|---|---|
| 1. 会话恢复 | `project-memory`；流程总控场景由 `using-shanforge` 判断 | 当前对话、`.factory/memory/agent-session.md`、work item ledger、必要 summary | 最小读取、恢复阶段和 work item、读取 ledger 防重复 | 会话卡、已读/排除、禁止动作、待决事项；必要时 ledger/memory 更新 | 不散读 docs；事实源和 ledger 优先；相同 idempotency 不重复执行 | 完全满足静态契约；真实压缩恢复回放未验证 |
| 2. 意图澄清 / brief | `brainstorming` | 用户意图、会话卡、work item brief、ledger | 一次一个问题、方案比较、收敛 brief 或设计输入 | brief、approval、outputs、evidence、ledger_event、needs | 只回写状态，不指定下一步 skill；作者自检不得 approved/done | 完全满足 |
| 3. 需求 / AC / NFR | `requirements-engineering` | 已批准 brief/设计输入、ledger、必要 summary 或单文件事实源 | 写用户故事、REQ、AC、NFR、非目标、风险、baseline 影响 | brief/PRD、memory summary、ledger_event、状态包 | 未确认需求不得进入计划/实现；reviewer approved 和 human_approved 前不得批准 | 完全满足，较 iteration-3 稳定 |
| 4. 设计 / 文档 / 边界 | `document-templates`；辅助 `doc-coauthoring` / `ui-ux-pro-max` | 已批准需求/设计输入、正式 docs 事实、暴露面 | 维护 4 大模块文档、设计边界、文档结构和校验 | docs、docs-stratego 校验说明、状态回写 | 不调用旧 factory 脚本；不批量制造空壳；正式文档需同步索引/版本历史 | 基本满足；`document-templates` 状态包仍缺 `work_item` / `ledger_event`，辅助 skill 仍是通用 `done/blocked` |
| 5. 实施计划 / task brief | `writing-plans` | 已批准 spec/需求/设计/work item brief | 锁定文件结构、拆任务、写 Red/Green/review/memory sync | `plan.md`、`task-briefs/`、review handoff、ledger_event、状态包 | 计划只能到 `ready_for_review`；approved 来自 review | 完全满足 |
| 6. 执行 / evidence / report / ledger | `subagent-driven-development` 或 `executing-plans` | approved plan、task brief、ledger、evidence/reports/reviews | 按 task brief 执行，生成 evidence、report、review input，更新 memory | evidence、implementer report、review input、ledger_event、状态包 | 实现者不得自批；不得跳号；不得自动 commit；缺 evidence/report/review checkpoint 不得 ready | 完全满足 |
| 7. Bug 修复 / TDD / 根因 | `systematic-debugging` + `tdd-workflow` + `ai-regression-testing` | 失败输出、复现步骤、调用链、相关测试 | 先复现和根因，再 Red/Green、根因修复和多路径回归 | 根因报告、red/green evidence、回归测试、ledger_event、状态包 | 根因不明只能加诊断；禁止兜底式修复声明完成 | 完全满足 |
| 8. 完成前验证 | `verification-before-completion` | 要验证的声明、plan/diff/review、命令或检查项 | 跑本轮新鲜完整命令，读取输出和 exit code，统计失败/跳过/未运行 | verification evidence/report、ledger_event、状态包 | 没有新鲜证据不得声明完成；review 不能替代 verification | 完全满足 |
| 9. 独立 review / scoring | `requesting-code-review` | task brief、implementer report、evidence、diff、review ledger | Spec Review + Quality Review，评分，记录独立性 | review 文件、review ledger、work item ledger；`review_status`、`next_gate_status`、needs | same-thread 只能 self_check；approved 必须有 reviewer_type/id/independence evidence | 基本满足；缺标准 `工作结果` 状态包代码块 |
| 10. review 反馈处理 | `receiving-code-review` | review feedback、PR 评论、task review、外部建议 | 逐条 triage、核实、修复或 pushback，每项验证 | triage、response、fix report、verification evidence、review ledger、memory sync | 禁止盲改和表演式同意；memory sync 缺失不得完成 | 基本满足；仍缺统一 `工作结果` 状态包 |
| 11. 人工确认门 | `using-shanforge` | independent review approved、score、ledger/evidence/final audit issue report | 停止并输出人工确认包 | `pending_human_confirmation`、确认包、阻塞/风险/验证证据 | reviewer approved 不等于 human_approved；人工确认前不得关闭/提交最终完成 | 完全满足静态契约 |
| 12. 本地提交 | `gitcommitzh` | human approval、ledger、review/evidence/memory sync、当前任务 diff | 审查范围、生成中文说明、只暂存当前任务范围、执行本地 commit | 真实 commit hash、实际提交信息、纳入文件、未纳入改动说明 | 不用 `git add .` 扩范围；本地 commit 不替代 review/verification/human confirmation | 完全满足本地提交闭环 |
| 13. 远端 PR / push / merge 边界 | 无固定 Shanforge owner；`gitcommitzh` 明确不负责 | 本地提交、远端目标、分支/PR 状态 | 当前只声明边界：需要 Git/GitHub 工作流，不能冒充远端状态 | 无固定远端 evidence/status 契约 | 禁止把本地 commit 写成 PR 已创建、已推送或已合并 | 不满足完整远端闭环；边界清楚 |
| 14. 压缩恢复和 idempotency | `project-memory` + `using-shanforge` | 会话卡、ledger、git/evidence、summary | 重读最新事件，跳过 done/approved/passed 或相同 idempotency，继续下一未完成动作 | 恢复状态、排除项、blocker 或下一动作 | ledger/git/evidence 优先于对话记忆 | 静态契约满足；缺真实恢复 dry-run transcript |
| 15. 黑盒 S1-S6 行为回放 evidence | `using-shanforge` reference 定义契约；暂无执行 owner 产物 | `black-box-flow-eval.md` 的 S1-S6 输入和 evidence 格式 | 应逐场景记录 allowed context、observed actions、files、commands、score | 应写入 evidence transcript | 无 transcript 不得声明真实行为回放 | 不满足；未发现可审计 transcript |

## 输出满足性

| step | 输出是否完全满足 Shanforge 要求 | 说明 |
|---|---|---|
| 会话恢复 | 基本是 | 状态、读取范围、idempotency 规则完整；缺真实压缩恢复回放。 |
| 意图澄清 / brief | 是 | `brainstorming` 已有 `work_item`、approval、outputs、evidence、ledger_event、needs。 |
| 需求 / AC / NFR | 是 | 已补 Shanforge 输出路径、ledger_event、状态边界和 no self-approval。 |
| 设计 / 文档 / 边界 | 基本是 | `document-templates` 可回写状态，但缺 `work_item` / `ledger_event`；`doc-coauthoring`、`ui-ux-pro-max` 为通用契约。 |
| 实施计划 / task brief | 是 | plan、task brief、review handoff、ledger_event 齐全。 |
| 执行 / evidence / report / ledger | 是 | 两个执行 skill 都要求 evidence、report、review input、ledger 和 memory sync。 |
| Bug 修复 / TDD / 根因 | 是 | 根因、Red/Green、回归测试和禁止兜底规则齐全。 |
| 完成前验证 | 是 | 新鲜命令、exit code、失败/跳过/未运行统计要求齐全。 |
| 独立 review / scoring | 基本是 | 独立性硬门强；但输出仍是 `review_status` 文本契约，不是标准状态包。 |
| review 反馈处理 | 基本是 | triage/response/fix/evidence/memory sync 齐全；缺标准状态包。 |
| 人工确认门 | 是 | 确认包要求包含最终审计问题报告、评分、阻塞、风险和证据。 |
| 本地提交 | 是 | 只负责本地 commit，human approval、范围审查和真实 hash 规则齐全。 |
| 远端 PR / push / merge | 否 | 只有边界和禁止冒充，没有 owner、状态、evidence、gate。 |
| 压缩恢复 / idempotency | 基本是 | 静态契约完整；没有真实恢复 transcript。 |
| 黑盒 S1-S6 行为回放 | 否 | `rg` 未发现 evidence 中有 `Scenario:` / `Observed actions:` / `Actual score:`。 |

## Findings

### Critical

1. 仍没有真实 S1-S6 行为回放 evidence。`skills/using-shanforge/references/black-box-flow-eval.md` 定义了 evidence 格式，但 `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/` 下没有 `Scenario:`、`Observed actions:`、`Actual score:`、`Normalized score:` 等可审计 transcript。结构测试全绿只能证明规则文本存在，不能证明代理真实遵守流程。

### Important

1. 远端 PR / push / merge 仍没有 Shanforge owner。`gitcommitzh` 和计划文档正确禁止本地 commit 冒充远端状态，但完整软件开发闭环仍缺远端 handoff 的 owner、输入、状态、evidence、失败语义和 gate。
2. Review 相关输出契约未完全统一。`requesting-code-review` 输出 `review_status` / `next_gate_status` / `needs`，`receiving-code-review` 要求完成状态与剩余 `needs`，但两者都缺标准 `工作结果` 状态包代码块。
3. 文档/设计辅助 skill 与 Shanforge work item 状态包仍不一致。`document-templates` 缺 `work_item` / `ledger_event`，`doc-coauthoring` 和 `ui-ux-pro-max` 仍使用通用 `done/blocked` 契约；在正式闭环中需要额外包装才能对齐 ledger。

### Minor

1. 当前相关 tests 仍以结构/短语断言为主，不是代理行为回放；适合防回归，不可替代黑盒 dry-run。
2. `document-templates` metadata 仍保留英文 description 和未解释的 D3 口径；这不阻塞流程闭环，但增加入口理解成本。
3. 当前仓库存在大量既有脏改动和未追踪 work item 目录；本审计未修改 skill 文件，也未试图整理无关改动。

## 验证命令和真实结果

### 1. 相关 workflow pytest

沙盒内首次运行因为 `uv` 读取 `~/.cache/uv` 被权限拦截，未形成测试结果：

```bash
PYTHONDONTWRITEBYTECODE=1 uv run pytest -p no:cacheprovider tests/test_bug_fix_root_cause_skill_rules.py tests/test_verification_debugging_workflow_skills.py tests/test_pr_commit_workflow_rules.py tests/test_execution_workflow_skills.py tests/test_deprecated_skill_cleanup.py tests/test_stratix_service_skill.py tests/test_skill_creator_skill_principles.py tests/test_skill_flow_process_audit.py tests/test_review_workflow_skills.py tests/test_project_memory_skill.py tests/test_writing_plans_skill.py tests/test_requirements_engineering_skill.py tests/test_brainstorming_skill.py tests/test_independent_review_gate.py tests/test_black_box_workflow_eval.py
```

真实结果：

```text
exit code: 2
error: failed to open file `/Users/uroborus/.cache/uv/sdists-v9/.git`: Operation not permitted (os error 1)
```

按 sandbox 规则在沙盒外重跑同一验证命令：

```text
exit code: 0
collected 84 items
84 passed in 0.08s
```

### 2. 相关 workflow ruff

沙盒内首次运行同样被 `uv` cache 权限拦截：

```bash
PYTHONDONTWRITEBYTECODE=1 uv run ruff check --no-cache tests/test_bug_fix_root_cause_skill_rules.py tests/test_verification_debugging_workflow_skills.py tests/test_pr_commit_workflow_rules.py tests/test_execution_workflow_skills.py tests/test_deprecated_skill_cleanup.py tests/test_stratix_service_skill.py tests/test_skill_creator_skill_principles.py tests/test_skill_flow_process_audit.py tests/test_review_workflow_skills.py tests/test_project_memory_skill.py tests/test_writing_plans_skill.py tests/test_requirements_engineering_skill.py tests/test_brainstorming_skill.py tests/test_independent_review_gate.py tests/test_black_box_workflow_eval.py
```

真实结果：

```text
exit code: 2
error: failed to open file `/Users/uroborus/.cache/uv/sdists-v9/.git`: Operation not permitted (os error 1)
```

按 sandbox 规则在沙盒外重跑同一验证命令：

```text
exit code: 0
All checks passed!
```

### 3. 旧中心 gate / 自选路由禁词扫描

```bash
rg -n 'factory-dispatch loop-gate|factory-workitem-loop-gate|scripts/factory-|REQUIRED NEXT SKILL|下一步 skill：|给出下一步 skill|只调用 `writing-plans`|finishing-a-development-branch|docs/superpowers' skills/project-memory/SKILL.md skills/brainstorming/SKILL.md skills/requirements-engineering/SKILL.md skills/document-templates/SKILL.md skills/doc-coauthoring/SKILL.md skills/writing-plans/SKILL.md skills/executing-plans/SKILL.md skills/subagent-driven-development/SKILL.md skills/systematic-debugging/SKILL.md skills/tdd-workflow/SKILL.md skills/ai-regression-testing/SKILL.md skills/requesting-code-review/SKILL.md skills/receiving-code-review/SKILL.md skills/gitcommitzh/SKILL.md skills/verification-before-completion/SKILL.md
```

真实结果：

```text
exit code: 1
无输出；工作流 skill 主文件未命中旧中心 gate 或工作 skill 自选下一步禁词。
```

### 4. S1-S6 黑盒回放 evidence 扫描

```bash
rg -n 'Scenario:|SF-SP-009-S1|SF-SP-009-S2|SF-SP-009-S3|SF-SP-009-S4|SF-SP-009-S5|SF-SP-009-S6|Observed actions:|Actual score:|Normalized score:' .factory/workitems/SKILL-FLOW-AUDIT-001/evidence
```

真实结果：

```text
exit code: 1
无输出；未发现 S1-S6 黑盒行为回放 evidence。
```

### 5. 状态包/远端边界抽样扫描

```bash
rg -n '工作结果：|status: .*\\||ledger_event|review_status|next_gate_status|pending_human_confirmation|human_approved|gitcommitzh 不负责创建、推送或合并 PR|不得把本地提交描述成远端 PR' skills/{using-shanforge,project-memory,brainstorming,requirements-engineering,document-templates,doc-coauthoring,ui-ux-pro-max,writing-plans,executing-plans,subagent-driven-development,systematic-debugging,tdd-workflow,ai-regression-testing,verification-before-completion,requesting-code-review,receiving-code-review,gitcommitzh}/SKILL.md
```

真实结果：

```text
exit code: 0
关键命中：多数核心 workflow skill 有 `工作结果：`、`ledger_event` 和明确状态；`requesting-code-review` 命中 `review_status` / `next_gate_status`；`document-templates` 命中状态包但未命中 `work_item` / `ledger_event`；`gitcommitzh` 命中“不负责创建、推送或合并 PR”。
```

## 相对 iteration-3 的变化

- 总分：86 -> 89。
- Critical：1 -> 1。未变化；真实 S1-S6 黑盒行为回放仍缺。
- Important：3 -> 3。远端 owner 和状态包一致性仍在；pytest 旧失败已修复，但 review/document 辅助契约仍未完全统一。
- 相关 pytest：iteration-3 为 `74 passed / 1 failed`；本轮为 `84 passed`。
- 相关 ruff：iteration-3 通过；本轮继续通过。
- 黑盒契约：`tests/test_black_box_workflow_eval.py` 已改为验证当前语义，包括 `SF-SP-009` 本地闭环口径；但 evidence 目录仍无 transcript。
- 远端边界：未变化；仍只能声明本地闭环，不得声明 PR/push/merge 完成。

## 最小下一步修复清单

1. 先补真实 S1-S6 dry-run transcript 到 `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/`，严格按 `black-box-flow-eval.md` 记录 allowed context、observed actions、files read/written、commands、critical assertions、score 和 failure reason；不要新增中心脚本。
2. 给远端 PR / push / merge 定义最小 handoff 契约：owner、输入、本地提交前提、远端命令/工具、evidence、失败语义、状态词和禁止冒充规则；不要塞进 `gitcommitzh`。
3. 给 `requesting-code-review` 和 `receiving-code-review` 补标准 `工作结果` 状态包；保留现有独立性硬门和逐条反馈核实规则。
4. 给 `document-templates` 的 work item 状态包补 `work_item` 和 `ledger_event`；若 `doc-coauthoring` / `ui-ux-pro-max` 用作 Shanforge work item owner，也补同样字段，否则明确它们只输出通用工作状态。
