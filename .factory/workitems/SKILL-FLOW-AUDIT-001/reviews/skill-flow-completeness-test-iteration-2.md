# Skill Flow Completeness Test Iteration 2

## 结论

- status: DONE
- 总评分：82 / 100
- Critical：1
- Important：4
- Minor：3
- blocked: false

当前 workflow skill 已经覆盖 Shanforge 本地开发闭环：会话恢复、意图澄清、需求、计划、执行、TDD / 根因、验证、独立 review、review 反馈、人工确认和本地提交均有 owner skill、输入、输出和主要 gate。不能声明“完整软件开发全闭环已验证”，因为远端 PR / push / merge 只有边界声明，且当前没有真实 6 场景黑盒行为回放证据。

## 流程矩阵

| 步骤 | owner skill | 输入 | 动作 | 输出 | gate | 评估 |
|---|---|---|---|---|---|---|
| 1. 会话恢复 | `using-shanforge` + `project-memory` | 当前对话、`.factory/memory/agent-session.md`、必要 summary、work item ledger | 恢复阶段、work item、读取范围、禁止动作；按 ledger 防重复 | 会话卡、已读 / 排除列表、待决事项、ledger 事件 | 禁止散读 docs；`idempotency_key` 已完成则不重复执行 | 完全满足静态契约 |
| 2. 意图澄清 / brief | `brainstorming` | 用户意图、会话卡、work item brief / ledger | 澄清范围、一次一个问题、方案比较、记录批准状态 | `.factory/workitems/<WORKITEM-ID>/brief.md`、approval、outputs、evidence、ledger_event、needs | 不直接进入实现；工作 skill 不决定下一步 skill | 完全满足 |
| 3. 需求 / AC / NFR | `requirements-engineering` | 已批准 brief、ledger、必要 summary / 单文件事实源 | 生成 REQ、AC、NFR、风险、非目标，区分事实和待确认项 | brief / PRD、`.factory/memory/prd.summary.md`、tasks summary、ledger、状态包 | 未确认需求不得进入计划；不得写 `approved/done/human_approved` | 基本满足；缺专门需求 review 模板 |
| 4. 设计 / 文档 / 边界 | `document-templates`，必要时 `doc-coauthoring` / `ui-ux-pro-max` | 已批准需求、项目状态、docs 结构 | 维护 4 大模块文档、技术设计、模块边界、文档导航 | `docs/` 正式文档、docs-stratego 校验结果 | 不调用旧 factory 脚本；只创建会被使用的文档 | 部分满足；主 skill 缺统一状态包、ledger、review gate |
| 5. 实施计划 / task brief | `writing-plans` | 已批准 spec / 需求 / 设计 / brief | 锁定文件结构，拆 Red / Green / Review / Memory sync 任务 | `plan.md`、`task-briefs/`、evidence / reports / reviews 目录约定、plan review handoff | 计划只能到 `ready_for_review`；approved 来自 review | 完全满足 |
| 6. 执行 / evidence / report / ledger | `subagent-driven-development` 或 `executing-plans` | approved plan、task brief、ledger、evidence / reports / reviews | 按任务执行、写 evidence、implementer report、review input package、ledger / memory sync | evidence、reports、review input、ledger、状态包 | 实现者只能 `ready_for_review`；禁止自批、自动 commit、并行冲突 | 完全满足 |
| 7. Bug 修复 / TDD / 根因 | `systematic-debugging` + `tdd-workflow` | 失败输出、复现步骤、diff、调用链、数据流 | 先复现和定位根因，再写失败测试 / 复现脚本，最小修复并回归 | 根因报告、复现证据、修复验证、ledger | 禁止猜测式补丁、兜底掩盖根因、3 次失败继续堆补丁 | 基本满足；`tdd-workflow` 本身缺 Shanforge 状态包 |
| 8. 完成前验证 | `verification-before-completion` | 要验证的声明、plan / diff / review、验证命令 | 运行新鲜完整命令，读取输出和 exit code，统计失败 / 跳过 / 未运行项 | completion evidence、verification report、ledger、状态包 | 无新鲜证据不得声明完成；不把测试通过替代需求核对 | 完全满足 |
| 9. 独立 review / scoring | `requesting-code-review` | task brief、report、evidence、diff、work item ledger、review ledger | 组织 task / PR / independent review，执行 Spec Review + Quality Review，按 rubric 打分 | review 文件、review ledger、work item ledger、review_score 或 author_self_check_score | `same_thread` 只能 `self_check_passed`；approved 必须有独立性证据 | 完全满足 |
| 10. review 反馈处理 | `receiving-code-review` | review comments、PR comments、task review | 逐条 triage，先核实再修改，处理 fixed / pushback / clarification | triage、response、fix report、verification evidence、review ledger、tasks summary | 禁止盲改、表演式同意；每项修复后验证 | 基本满足；缺显式 `工作结果` 状态包模板 |
| 11. 人工确认门 | `using-shanforge` | reviewer approved、score、evidence、ledger | 停止并输出确认包，等待用户明确通过 / 修改 / 暂停 | `pending_human_confirmation`、确认包、之后才可 `human_approved` | reviewer approved 不等于人工确认 | 完全满足 |
| 12. 本地提交 | `gitcommitzh` | human approval、ledger、review ledger、evidence、diff / staged diff | 审查范围、生成中文提交说明、只暂存当前任务文件、本地 commit 并回读 hash / message | 中文摘要、commit message、真实 commit hash、纳入文件列表 | 不使用 `git add .` 扩范围；不得把 commit 冒充 PR / push / merge | 完全满足 |
| 13. 远端 PR / push / merge 边界 | `gitcommitzh` 只声明不负责；可转外部 GitHub / PR workflow | 本地提交、PR diff、远端状态 | 当前 Shanforge flow 只防冒充，不执行远端闭环 | 无固定 Shanforge 远端 PR / push / merge 产物 | 禁止把本地提交说成远端 PR 已创建、push 或 merge | 部分满足；边界清楚但闭环缺 owner |
| 14. 压缩恢复和 idempotency | `project-memory` + `using-shanforge` | 会话卡、ledger、git / evidence、summary | 复用新鲜会话卡，读取 ledger 最新事件，跳过已完成 idempotency | 恢复状态、排除项、下一未完成动作或 blocker | ledger / git / evidence 优先于对话记忆 | 完全满足静态契约；未做真实恢复回放 |

## 输出完整性逐项结论

| 步骤 | 输出是否完全满足 Shanforge 要求 | 说明 |
|---|---|---|
| 会话恢复 | 是 | session card、已读 / 排除、禁止动作、ledger / idempotency 规则齐全。 |
| 意图澄清 / brief | 是 | iteration-1 后已去掉工作 skill 自选下一步，改为状态回写。 |
| 需求 / AC / NFR | 基本是 | 输出路径、ledger、memory、状态包已补齐；仍缺需求专用 review / approval 模板。 |
| 设计 / 文档 / 边界 | 否 | `document-templates` 偏文档体系维护，缺 `工作结果` 状态包、ledger、memory sync 和 review gate 模板。 |
| 实施计划 / task brief | 是 | plan、task brief、测试策略、review handoff、禁止占位符齐全。 |
| 执行 / evidence / report / ledger | 是 | evidence、report、review input、ledger、memory sync 和 ready_for_review 边界齐全。 |
| Bug 修复 / TDD / 根因 | 基本是 | `systematic-debugging` 完整；`tdd-workflow` 仍像方法论，未声明 Shanforge 输出包。 |
| 完成前验证 | 是 | 新鲜命令、exit code、失败 / 跳过统计、evidence 和 partial / failed 边界齐全。 |
| 独立 review / scoring | 是 | 独立性元数据、score rubric、same-thread 限制和 gate 齐全。 |
| review 反馈处理 | 基本是 | triage / response / verification / memory sync 齐全，但缺统一状态包。 |
| 人工确认门 | 是 | pending_human_confirmation 和确认包规则明确。 |
| 本地提交 | 是 | 范围审查、中文说明、真实 hash 回读和 PR 边界明确。 |
| 远端 PR / push / merge | 否 | 只有“不冒充”的边界，没有 Shanforge owner skill、状态和 evidence 契约。 |
| 压缩恢复 / idempotency | 是 | 静态契约完整；真实恢复回放未执行。 |

## 缺口 / 风险

### Critical

1. 没有真实行为回放证据。当前只有 skill 文本、模板和结构测试；`skills/using-shanforge/references/black-box-flow-eval.md` 定义了 6 个场景，但本 work item 的 evidence 目录只有 `iteration-1-verification.md`，没有 S1-S6 或 14 步流程 dry-run transcript。因此不能把“结构测试存在”说成“真实行为回放已完成”。

### Important

1. 远端 PR / push / merge 没有 Shanforge owner。`gitcommitzh` 明确只做本地提交，这是正确边界；但流程表没有后续 owner、输入、状态、evidence 和 gate，所以“完整软件开发闭环”只能到本地提交。
2. `document-templates` 未接入统一状态回写协议。它有 docs 结构和 docs-stratego 校验，但缺 work item ledger、memory sync、review handoff、`工作结果` 状态包。
3. 部分工作 skill 的状态包不一致。`tdd-workflow` 和 `receiving-code-review` 有动作纪律和输出路径，但没有像执行 / 验证类 skill 那样的标准 `work_item / skill / status / outputs / evidence / ledger_event / needs` 包。
4. 当前相关 pytest 不全绿。61 个相关结构测试中 60 个通过，`tests/test_black_box_workflow_eval.py::test_workflow_plan_tracks_sf_sp_009_development_scope` 失败；失败断言期待旧短语“当前已进入黑盒流程 eval 开发”，而当前文档已写 `SF-SP-009` 本地闭环完成。需要更新测试断言或文档状态口径。

### Minor

1. `tdd-workflow` 仍包含大量 npm / Jest / Next 示例，作为跨项目 Shanforge workflow skill 容易误导非 JS 项目；建议收敛为原则和 Shanforge 输出契约。
2. `task-brief-template.md` 的状态枚举包含 `approved | changes_requested`，但执行者任务简报本身不应让实现者写 approved；建议拆成 task brief 状态和 review 状态。
3. 旧流程说明报告的“已读事实”列出较多背景文件，和当前 `project-memory` 最小读取策略不完全一致；作为历史报告可保留，但新报告应继续按最小读取。

## 可运行验证命令及真实结果

### 1. 相关 workflow 结构测试

```bash
uv run pytest tests/test_skill_flow_process_audit.py tests/test_execution_workflow_skills.py tests/test_review_workflow_skills.py tests/test_pr_commit_workflow_rules.py tests/test_project_memory_skill.py tests/test_verification_debugging_workflow_skills.py tests/test_writing_plans_skill.py tests/test_requirements_engineering_skill.py tests/test_brainstorming_skill.py tests/test_independent_review_gate.py tests/test_bug_fix_root_cause_skill_rules.py tests/test_deprecated_skill_cleanup.py tests/test_black_box_workflow_eval.py
```

真实结果：

```text
exit code: 1
collected 61 items
60 passed
1 failed: tests/test_black_box_workflow_eval.py::test_workflow_plan_tracks_sf_sp_009_development_scope
失败原因：断言期待 "`SF-SP-009`：当前已进入黑盒流程 eval 开发"，当前计划文档未包含该旧状态短语。
```

### 2. 相关测试 lint

```bash
uv run ruff check tests/test_skill_flow_process_audit.py tests/test_execution_workflow_skills.py tests/test_review_workflow_skills.py tests/test_pr_commit_workflow_rules.py tests/test_project_memory_skill.py tests/test_verification_debugging_workflow_skills.py tests/test_writing_plans_skill.py tests/test_requirements_engineering_skill.py tests/test_brainstorming_skill.py tests/test_independent_review_gate.py tests/test_bug_fix_root_cause_skill_rules.py tests/test_deprecated_skill_cleanup.py tests/test_black_box_workflow_eval.py
```

真实结果：

```text
exit code: 0
All checks passed!
```

### 3. 工作 skill 禁词缩小检查

```bash
rg -n "factory-dispatch loop-gate|factory-workitem-loop-gate|下一步 skill：|给出下一步 skill|handed_off|REQUIRED NEXT SKILL" skills/project-memory/SKILL.md skills/brainstorming/SKILL.md skills/requirements-engineering/SKILL.md skills/writing-plans/SKILL.md skills/subagent-driven-development/SKILL.md skills/executing-plans/SKILL.md skills/requesting-code-review/SKILL.md skills/receiving-code-review/SKILL.md skills/verification-before-completion/SKILL.md skills/systematic-debugging/SKILL.md skills/tdd-workflow/SKILL.md skills/gitcommitzh/SKILL.md
```

真实结果：

```text
exit code: 1
无输出；表示这些工作 skill 主文件未命中旧中心 gate 或自选下一步 skill 禁词。
```

### 4. 当前 work item evidence 文件

```bash
rg --files .factory/workitems/SKILL-FLOW-AUDIT-001/evidence
```

真实结果：

```text
exit code: 0
.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-1-verification.md
```

解释：未发现 iteration-2 或 SF-SP-009 S1-S6 黑盒行为回放 evidence。

## 最小修复任务建议

1. 新增文件化黑盒回放证据，不新增中心脚本：按 `black-box-flow-eval.md` 的 S1-S6 写一份 dry-run transcript 到 work item evidence，逐条记录 allowed context、observed actions、files read / written、commands、score 和 failure reason。
2. 修复 `tests/test_black_box_workflow_eval.py` 的过时状态断言，改为验证当前文档含 `SF-SP-009`、6 类场景、已完成 / 未远端闭环边界，而不是固定“当前已进入开发”旧短语。
3. 给 `document-templates` 增加最小 Shanforge 状态包、ledger、memory sync、review handoff；不要扩大成新文档系统。
4. 给 `tdd-workflow` 和 `receiving-code-review` 补统一状态包，或在 `using-shanforge` 明确它们只是子纪律，由 `systematic-debugging` / `executing-plans` 承担状态回写。
5. 增加远端 PR / push / merge 的显式 handoff 契约：只定义 owner、输入、证据和禁止冒充规则；不要塞进 `gitcommitzh`。

```text
status: DONE
outputs:
  - .factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-completeness-test-iteration-2.md
```
